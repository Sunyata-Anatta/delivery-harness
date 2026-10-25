#!/usr/bin/env python3
"""Delivery Harness preflight: mechanical checks for records and commits.

A single-file, standard-library tool for Python 3.9+. Checks a-i guard records
and commits; checks j-o are the hard constraints H1-H6. It reads the project
record, the Git index/worktree and candidate commit metadata; it never edits
project records. The only write it can perform is the optional commit-msg hook
requested explicitly with --install-hook.

Exit codes: 0 = pass (warnings/skips allowed), 1 = blocked failure,
2 = usage or configuration error.

Run ``python references/preflight.py --help`` for the command line. The
bilingual contract lives in ``references/preflight.md`` and
``references/en/preflight.md``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

SCHEMA = 1
TOOL = "delivery-harness-preflight"

CHECK_TITLES = {
    "a": "record exists and is read/write available",
    "b": "record changes travel with code changes",
    "c": "new evidence lines have resolvable links and increasing numbers",
    "d": "baseline version increases when evidence lines are added",
    "e": "record size stays within configured limits",
    "f": "no secret-like content in the changes to be committed",
    "g": "candidate commit message has no session/share link or agent trailer",
    "h": "effective Git identity matches the configured policy",
    "i": "the batch commit really contains the record change",
    "j": "the state file follows the fixed three-sentence format",
    "k": "evidence entries are one of three kinds; minor batches add none",
    "l": "evidence entries per day stay under the threshold",
    "m": "independent reviews of one change stop at round two unless the owner names a third",
    "n": "rule decisions are traceable and mechanically checkable",
    "o": "work stays on the main line: no new local branches",
}

DEFAULT_CODE_PATHS = [
    "src/**",
    "lib/**",
    "app/**",
    "pkg/**",
    "**/*.py",
    "**/*.js",
    "**/*.jsx",
    "**/*.ts",
    "**/*.tsx",
    "**/*.vue",
    "**/*.svelte",
    "**/*.go",
    "**/*.rs",
    "**/*.java",
    "**/*.kt",
    "**/*.kts",
    "**/*.cs",
    "**/*.fs",
    "**/*.c",
    "**/*.h",
    "**/*.cc",
    "**/*.cpp",
    "**/*.hpp",
    "**/*.rb",
    "**/*.php",
    "**/*.swift",
    "**/*.m",
    "**/*.mm",
    "**/*.scala",
    "**/*.sh",
    "**/*.ps1",
    "**/*.sql",
]

# High-signal patterns only. A project can replace or extend this list.
DEFAULT_SECRET_PATTERNS = [
    {
        "type": "private-key",
        "regex": r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----",
    },
    {"type": "aws-access-key", "regex": r"\bAKIA[0-9A-Z]{16}\b"},
    {"type": "github-token", "regex": r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"},
    {"type": "slack-token", "regex": r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"},
    {
        "type": "bearer-token",
        "regex": r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b",
    },
]

# Opaque collaboration links and agent session trailers are not commit metadata.
DEFAULT_BANNED_LINKS = [
    r"(?i)https?://[^\s)\]>]*\b(?:session|share|conversation|chat)\b[^\s)\]>]*",
    r"(?i)https?://(?:claude\.ai|chatgpt\.com|chat\.openai\.com|gemini\.google\.com|copilot\.microsoft\.com)/[^\s)\]>]*",
]
DEFAULT_BANNED_TRAILERS = [r"(?im)^\s*Claude-[A-Za-z0-9-]+\s*:"]

# Hard-constraint vocabulary (references/hard-constraints.md). Bilingual labels are fixed.
DEFAULT_ID_PATTERN = r"\b[A-Z]{1,2}\d+[a-z]?\b"
DEFAULT_BANNED_TOKENS = ["→", "=>", "->", "TBD", "w/", "&&"]
DEFAULT_MINOR_PATHS = ["**/*.css", "**/*.scss", "**/*.sass", "**/*.less", "**/locales/**", "**/i18n/**"]
VAGUE_WORDS = ["适度", "必要时", "酌情", "尽量", "适当",
               "视情况", "合理", "as needed", "if necessary", "when necessary",
               "appropriate", "reasonable", "where possible"]
EVIDENCE_KIND = re.compile(r"\[(?:门结论|变更|根因|gate|change|root-cause)\]", re.I)
DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
REVIEW_WORD = re.compile(r"复审|\breview", re.I)
ROUND = re.compile(r"第\s*(\d+)\s*轮|\bround\s*(\d+)", re.I)
EVIDENCE_LINE = re.compile(r"^\s*(?:[-*+]\s+)?(?:\[)?{prefix}(\d+)(?:\])?(?=\s|$|[:|.,;!?\-—])")
INLINE_LINK = re.compile(r"\[[^\]\n]*\]\(\s*<?([^)>\s]+)>?")
IDENTITY_LINE = re.compile(r"^(?P<name>.*?) <(?P<email>[^>]*)> (?P<ts>\d+) (?P<tz>[+-]\d{4})$")
WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:[\\/]")


class UsageError(Exception):
    """Bad command line or environment for the requested mode."""


class ConfigError(Exception):
    """Unreadable or invalid preflight configuration."""


class GitError(Exception):
    """A Git command that must succeed failed."""


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def default_config() -> dict:
    return {
        "schema": SCHEMA,
        "record": {
            "path": ".delivery/state.md",
            "tracked": "auto",
            "related_readable": [],
            "mtime_tolerance_seconds": 0,
        },
        "code": {"paths": list(DEFAULT_CODE_PATHS), "exclude": []},
        "evidence": {
            "path": None,
            "prefix": "E",
            "allow_needs_source": False,
            "daily_limit": 5,
            "minor_paths": list(DEFAULT_MINOR_PATHS),
            "files": [".delivery/artifacts/**"],
        },
        "baseline": {"enabled": False, "path": None, "pattern": None, "ref": "HEAD"},
        "exemptions": {"path": ".delivery/preflight-exemptions.md"},
        "identity": {"name": None, "email": None, "check_committer": False},
        "limits": {"record_max_lines": 80, "record_max_line_length": 0},
        "secrets": {
            "patterns": [dict(item) for item in DEFAULT_SECRET_PATTERNS],
            "exclude": [],
            "max_bytes": 2 * 1024 * 1024,
        },
        "message": {
            "banned_links": list(DEFAULT_BANNED_LINKS),
            "banned_trailers": list(DEFAULT_BANNED_TRAILERS),
        },
        "state": {
            "id_pattern": DEFAULT_ID_PATTERN,
            "banned_tokens": list(DEFAULT_BANNED_TOKENS),
        },
        "decisions": {"path": ".delivery/decisions.md", "executors": ["AGENTS.md", "CLAUDE.md"]},
        "branches": {"allowed": ["main", "master"]},
        "checks": dict({key: "block" for key in CHECK_TITLES}, l="warn"),
        "readback": {"ref": "HEAD"},
        "hook": {"python": None},
    }


def _merge_config(base: dict, override: dict, location: str, notes: list) -> None:
    if not isinstance(override, dict):
        raise ConfigError(f"{location.rstrip('.')} must be a JSON object")
    for key, value in override.items():
        if key not in base:
            notes.append(f"unknown config key ignored: {location}{key}")
            continue
        current = base[key]
        if isinstance(current, dict):
            _merge_config(current, value, f"{location}{key}.", notes)
        else:
            base[key] = value


def _expect(value, kinds, label: str) -> None:
    if not isinstance(value, kinds):
        expected = " or ".join(kind.__name__ for kind in kinds) if isinstance(kinds, tuple) else kinds.__name__
        raise ConfigError(f"{label} must be {expected}")


def _list_of_strings(value, label: str) -> None:
    _expect(value, list, label)
    for item in value:
        if not isinstance(item, str) or not item:
            raise ConfigError(f"{label} entries must be non-empty strings")


def _compile(pattern: str, label: str) -> "re.Pattern":
    try:
        return re.compile(pattern)
    except re.error as error:
        raise ConfigError(f"{label} is not a valid regular expression: {error}") from None


def validate_config(cfg: dict) -> list:
    notes = []
    _expect(cfg.get("schema"), int, "schema")
    if cfg["schema"] != SCHEMA:
        raise ConfigError(f"unsupported config schema {cfg['schema']!r}; expected {SCHEMA}")

    record = cfg["record"]
    _expect(record, dict, "record")
    _expect(record.get("path"), str, "record.path")
    if not record["path"].strip():
        raise ConfigError("record.path must not be empty")
    _expect(record.get("tracked"), (bool, str), "record.tracked")
    if isinstance(record["tracked"], str) and record["tracked"] != "auto":
        raise ConfigError("record.tracked must be true, false or \"auto\"")
    _list_of_strings(record.get("related_readable"), "record.related_readable")
    _expect(record.get("mtime_tolerance_seconds"), (int, float), "record.mtime_tolerance_seconds")
    if record["mtime_tolerance_seconds"] < 0:
        raise ConfigError("record.mtime_tolerance_seconds must be >= 0")

    code = cfg["code"]
    _expect(code, dict, "code")
    _list_of_strings(code.get("paths"), "code.paths")
    _list_of_strings(code.get("exclude"), "code.exclude")

    evidence = cfg["evidence"]
    _expect(evidence, dict, "evidence")
    if evidence.get("path") is not None:
        _expect(evidence["path"], str, "evidence.path")
        if not evidence["path"].strip():
            raise ConfigError("evidence.path must not be empty when set")
    _expect(evidence.get("prefix"), str, "evidence.prefix")
    if not evidence["prefix"].strip():
        raise ConfigError("evidence.prefix must not be empty")
    _expect(evidence.get("allow_needs_source"), bool, "evidence.allow_needs_source")
    _expect(evidence.get("daily_limit"), int, "evidence.daily_limit")
    if evidence["daily_limit"] < 1:
        raise ConfigError("evidence.daily_limit must be >= 1")
    _list_of_strings(evidence.get("minor_paths"), "evidence.minor_paths")
    _list_of_strings(evidence.get("files"), "evidence.files")

    state = cfg["state"]
    _expect(state, dict, "state")
    _expect(state.get("id_pattern"), str, "state.id_pattern")
    _compile(state["id_pattern"], "state.id_pattern")
    _list_of_strings(state.get("banned_tokens"), "state.banned_tokens")

    decisions = cfg["decisions"]
    _expect(decisions, dict, "decisions")
    _expect(decisions.get("path"), str, "decisions.path")
    _list_of_strings(decisions.get("executors"), "decisions.executors")

    branches = cfg["branches"]
    _expect(branches, dict, "branches")
    _list_of_strings(branches.get("allowed"), "branches.allowed")
    if not branches["allowed"]:
        raise ConfigError("branches.allowed must name at least the main line")

    baseline = cfg["baseline"]
    _expect(baseline, dict, "baseline")
    _expect(baseline.get("enabled"), bool, "baseline.enabled")
    if baseline.get("enabled"):
        if not isinstance(baseline.get("path"), str) or not baseline["path"].strip():
            raise ConfigError("baseline.path is required when baseline.enabled is true")
        if not isinstance(baseline.get("pattern"), str) or not baseline["pattern"]:
            raise ConfigError("baseline.pattern is required when baseline.enabled is true")
        _compile(baseline["pattern"], "baseline.pattern")
    _expect(baseline.get("ref"), str, "baseline.ref")

    _expect(cfg["exemptions"], dict, "exemptions")
    _expect(cfg["exemptions"].get("path"), str, "exemptions.path")

    identity = cfg["identity"]
    _expect(identity, dict, "identity")
    for field in ("name", "email"):
        if identity.get(field) is not None:
            _expect(identity[field], str, f"identity.{field}")
            if not identity[field].strip():
                raise ConfigError(f"identity.{field} must not be empty when set")
    if (identity.get("name") is None) != (identity.get("email") is None):
        raise ConfigError("identity.name and identity.email must be set together")
    _expect(identity.get("check_committer"), bool, "identity.check_committer")

    limits = cfg["limits"]
    _expect(limits, dict, "limits")
    for field in ("record_max_lines", "record_max_line_length"):
        _expect(limits.get(field), int, f"limits.{field}")
        if limits[field] < 0:
            raise ConfigError(f"limits.{field} must be >= 0")

    secrets = cfg["secrets"]
    _expect(secrets, dict, "secrets")
    _expect(secrets.get("patterns"), list, "secrets.patterns")
    for index, item in enumerate(secrets["patterns"]):
        _expect(item, dict, f"secrets.patterns[{index}]")
        _expect(item.get("type"), str, f"secrets.patterns[{index}].type")
        _expect(item.get("regex"), str, f"secrets.patterns[{index}].regex")
        _compile(item["regex"], f"secrets.patterns[{index}].regex")
        if set(item) - {"type", "regex"}:
            notes.append(f"unknown key ignored in secrets.patterns[{index}]")
    _list_of_strings(secrets.get("exclude"), "secrets.exclude")
    _expect(secrets.get("max_bytes"), int, "secrets.max_bytes")
    if secrets["max_bytes"] <= 0:
        raise ConfigError("secrets.max_bytes must be > 0")

    message = cfg["message"]
    _expect(message, dict, "message")
    for field in ("banned_links", "banned_trailers"):
        _list_of_strings(message.get(field), f"message.{field}")
        for index, pattern in enumerate(message[field]):
            _compile(pattern, f"message.{field}[{index}]")

    checks = cfg["checks"]
    _expect(checks, dict, "checks")
    for key, severity in checks.items():
        if key not in CHECK_TITLES:
            notes.append(f"unknown check id ignored: {key}")
            continue
        if severity not in ("block", "warn"):
            raise ConfigError(f"checks.{key} must be \"block\" or \"warn\"")

    _expect(cfg["readback"], dict, "readback")
    _expect(cfg["readback"].get("ref"), str, "readback.ref")
    _expect(cfg["hook"], dict, "hook")
    if cfg["hook"].get("python") is not None:
        _expect(cfg["hook"]["python"], str, "hook.python")
    return notes


def _overlay_config_block(text: str):
    lines = text.splitlines()
    start = None
    fence = None
    for index, line in enumerate(lines):
        if start is None:
            opened = re.match(r"^\s*(`{3,})\s*preflight\s*$", line, re.I)
            if opened:
                start = index + 1
                fence = len(opened.group(1))
            continue
        closed = re.match(r"^\s*(`{3,})\s*$", line)
        if closed and len(closed.group(1)) >= fence:
            return "\n".join(lines[start:index]), start
    if start is not None:
        raise ConfigError("unterminated ```preflight block in .delivery/overlay.md")
    return None


def discover_config(root: Path):
    """Return (config, source, notes). JSON file wins over an overlay block."""
    notes = []
    cfg = default_config()
    json_path = root / ".delivery" / "preflight.json"
    overlay_path = root / ".delivery" / "overlay.md"
    source = "defaults"
    raw_text = None
    if json_path.is_file():
        try:
            raw_text = json_path.read_text(encoding="utf-8")
        except OSError as error:
            raise ConfigError(f"cannot read .delivery/preflight.json: {error}") from None
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as error:
            raise ConfigError(
                f".delivery/preflight.json is not valid JSON (line {error.lineno}, column {error.colno})"
            ) from None
        source = ".delivery/preflight.json"
        if overlay_path.is_file():
            try:
                if _overlay_config_block(overlay_path.read_text(encoding="utf-8")) is not None:
                    notes.append(
                        "an overlay ```preflight block exists but .delivery/preflight.json takes precedence"
                    )
            except ConfigError:
                notes.append("overlay ```preflight block is invalid and was ignored because the JSON file wins")
    elif overlay_path.is_file():
        try:
            overlay_text = overlay_path.read_text(encoding="utf-8")
        except OSError as error:
            raise ConfigError(f"cannot read .delivery/overlay.md: {error}") from None
        block = _overlay_config_block(overlay_text)
        if block is not None:
            block_text, line = block
            try:
                data = json.loads(block_text)
            except json.JSONDecodeError as error:
                raise ConfigError(
                    "the ```preflight block in .delivery/overlay.md is not valid JSON "
                    f"(block line {line + error.lineno}, column {error.colno})"
                ) from None
            source = f".delivery/overlay.md#L{line + 1}"
    if source == "defaults":
        notes.append("no preflight config found; built-in defaults are in use")
        data = {}
    _merge_config(cfg, data, "", notes)
    notes.extend(validate_config(cfg))
    return cfg, source, notes


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def tool_version() -> str:
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    try:
        text = skill.read_text(encoding="utf-8")
    except OSError:
        return "unknown"
    for line in text.splitlines():
        if line.startswith("Version:"):
            return line.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def norm_rel(value: str) -> str:
    text = str(value).replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text


def path_key(value: str) -> str:
    text = norm_rel(value)
    return text.lower() if os.name == "nt" else text


def within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_text_file(path: Path) -> str:
    with open(path, "rb") as handle:
        raw = handle.read()
    return raw.decode("utf-8")


def decode_name(raw: bytes) -> str:
    return raw.decode("utf-8", "surrogateescape")


# ---------------------------------------------------------------------------
# Git plumbing
# ---------------------------------------------------------------------------


class Git:
    def __init__(self, root: Path):
        self.root = root

    def run(self, *args, input_bytes=None):
        return subprocess.run(
            ["git", *args],
            cwd=str(self.root),
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
        )

    def text(self, *args):
        proc = self.run(*args)
        if proc.returncode != 0:
            return None
        return proc.stdout.decode("utf-8", "replace")

    def ok(self, *args) -> bool:
        return self.run(*args).returncode == 0

    def is_work_tree(self) -> bool:
        proc = self.run("rev-parse", "--is-inside-work-tree")
        return proc.returncode == 0 and proc.stdout.strip() == b"true"

    def head_exists(self) -> bool:
        return self.ok("rev-parse", "--verify", "-q", "HEAD")

    def head_sha(self) -> str:
        value = self.text("rev-parse", "HEAD")
        if value is None:
            raise GitError("cannot resolve HEAD")
        return value.strip()

    def head_time(self):
        value = self.text("log", "-1", "--format=%ct")
        try:
            return int(value.strip()) if value else None
        except ValueError:
            return None

    def in_index(self, relative: str) -> bool:
        return self.ok("ls-files", "--error-unmatch", "--", relative)

    def blob(self, ref: str, relative: str) -> bytes:
        proc = self.run("show", f"{ref}:{relative}")
        return proc.stdout if proc.returncode == 0 else None

    def changed(self, staged: bool):
        if staged:
            proc = self.run("diff", "--cached", "--name-status", "-z", "--")
            if proc.returncode != 0:
                raise GitError("git diff --cached failed")
            return parse_name_status(proc.stdout)
        proc = self.run("status", "--porcelain", "-z")
        if proc.returncode != 0:
            raise GitError("git status failed")
        return parse_status(proc.stdout)

    def resolve(self, ref: str) -> str:
        proc = self.run("rev-parse", "--verify", f"{ref}^{{commit}}")
        if proc.returncode != 0:
            return None
        return proc.stdout.decode("utf-8", "replace").strip()

    def parents(self, sha: str):
        value = self.text("show", "-s", "--format=%P", sha)
        return value.split() if value else []

    def changed_between(self, parent: str, child: str):
        proc = self.run("diff", "--name-status", "-z", parent, child)
        if proc.returncode != 0:
            raise GitError("git diff failed for readback")
        return parse_name_status(proc.stdout)

    def commit_files(self, sha: str):
        proc = self.run("ls-tree", "-r", "--name-only", "-z", sha)
        if proc.returncode != 0:
            raise GitError("git ls-tree failed for readback")
        return [(b"A", decode_name(item), None) for item in proc.stdout.split(b"\0") if item]

    def file_mtime(self, relative: str):
        try:
            return (self.root / relative).stat().st_mtime
        except OSError:
            return None


def parse_name_status(raw: bytes):
    parts = raw.split(b"\0")
    if parts and parts[-1] == b"":
        parts.pop()
    entries, index = [], 0
    while index < len(parts):
        status = decode_name(parts[index])
        index += 1
        if not status:
            continue
        kind = status[0]
        if kind in "RC":
            if index + 1 >= len(parts):
                break
            old, new = decode_name(parts[index]), decode_name(parts[index + 1])
            index += 2
            entries.append((kind, new, old))
        else:
            if index >= len(parts):
                break
            entries.append((kind, decode_name(parts[index]), None))
            index += 1
    return entries


def parse_status(raw: bytes):
    parts = raw.split(b"\0")
    if parts and parts[-1] == b"":
        parts.pop()
    entries, index = [], 0
    while index < len(parts):
        token = decode_name(parts[index])
        index += 1
        if len(token) < 3:
            continue
        x, y, path = token[0], token[1], token[3:]
        original = None
        if x in "RC" or y in "RC":
            if index < len(parts):
                original = decode_name(parts[index])
                index += 1
        entries.append((x + y, path, original))
    return entries


# ---------------------------------------------------------------------------
# Check result plumbing
# ---------------------------------------------------------------------------


def finding(level: str, kind: str, message: str, path=None, line=None, fix=None) -> dict:
    return {
        "level": level,
        "type": kind,
        "message": message,
        "path": None if path is None else str(path),
        "line": line,
        "fix": fix,
    }


def result(check_id: str, severity: str, findings=None, status=None, note=None) -> dict:
    findings = findings or []
    if severity == "warn":
        findings = [
            dict(item, level="warn") if item["level"] == "block" else item for item in findings
        ]
    if status is None:
        if any(item["level"] == "block" for item in findings):
            status = "fail"
        elif findings:
            status = "warn"
        else:
            status = "pass"
    return {
        "id": check_id,
        "title": CHECK_TITLES[check_id],
        "severity": severity,
        "status": status,
        "note": note,
        "findings": findings,
    }


def skip(check_id: str, severity: str, note: str) -> dict:
    return result(check_id, severity, status="skip", note=note)


# ---------------------------------------------------------------------------
# Checks a-i: record, batch, evidence, size, secrets, message, identity, readback
# ---------------------------------------------------------------------------


def check_record(root: Path, cfg: dict) -> dict:
    record = root / norm_rel(cfg["record"]["path"])
    findings = []
    if not record.exists():
        findings.append(
            finding(
                "block",
                "record-missing",
                "the declared record file does not exist",
                path=display_path(record, root),
                fix="create the record at record.path (or correct the configured path); do not create a substitute record surface",
            )
        )
        return result("a", cfg["checks"]["a"], findings)
    if not record.is_file():
        findings.append(
            finding(
                "block",
                "record-not-file",
                "the declared record path is not a regular file",
                path=display_path(record, root),
                fix="point record.path at the project's sole active state",
            )
        )
        return result("a", cfg["checks"]["a"], findings)
    try:
        read_text_file(record)
    except (OSError, UnicodeDecodeError) as error:
        findings.append(
            finding(
                "block",
                "record-unreadable",
                f"the record cannot be read as UTF-8 text ({type(error).__name__})",
                path=display_path(record, root),
                fix="repair the file or its permissions; never move the record path without authorization",
            )
        )
    try:
        with open(record, "r+b"):
            pass
    except OSError:
        findings.append(
            finding(
                "block",
                "record-not-writable",
                "the record cannot be opened for writing",
                path=display_path(record, root),
                fix="restore write permission or make the record path writable for the delivery role",
            )
        )
    for related in cfg["record"]["related_readable"]:
        candidate = root / norm_rel(related)
        try:
            with open(candidate, "rb"):
                pass
        except OSError:
            findings.append(
                finding(
                    "block",
                    "related-record-unreadable",
                    "a declared related record is not readable",
                    path=display_path(candidate, root),
                    fix="repair the path or the record availability before staging",
                )
            )
    return result("a", cfg["checks"]["a"], findings)


def _record_tracked(git: Git, cfg: dict, record_rel: str) -> bool:
    configured = cfg["record"]["tracked"]
    if configured == "auto":
        if not git.is_work_tree():
            return False
        if git.in_index(record_rel):
            return True
        return git.head_exists() and git.run("cat-file", "-e", f"HEAD:{record_rel}").returncode == 0
    return bool(configured)


def _matches_any(relative: str, patterns, cache: dict) -> bool:
    key = path_key(relative)
    for pattern in patterns:
        compiled = cache.get(pattern)
        if compiled is None:
            compiled = glob_regex(pattern)
            cache[pattern] = compiled
        if compiled.match(key):
            return True
    return False


def glob_regex(pattern: str) -> "re.Pattern":
    pat = str(pattern).replace("\\", "/")
    while pat.startswith("./"):
        pat = pat[2:]
    if pat.startswith("/"):
        pat = pat[1:]
    out, index = [], 0
    while index < len(pat):
        char = pat[index]
        if char == "*":
            if index + 1 < len(pat) and pat[index + 1] == "*":
                index += 2
                if index < len(pat) and pat[index] == "/":
                    out.append("(?:.*/)?")
                    index += 1
                else:
                    out.append(".*")
            else:
                out.append("[^/]*")
                index += 1
        elif char == "?":
            out.append("[^/]")
            index += 1
        elif char == "[":
            closing = pat.find("]", index + 1)
            if closing == -1:
                out.append(re.escape(char))
                index += 1
            else:
                inner = pat[index + 1 : closing]
                if inner.startswith("!"):
                    inner = "^" + inner[1:]
                out.append("[" + inner + "]")
                index = closing + 1
        else:
            out.append(re.escape(char))
            index += 1
    try:
        return re.compile("^" + "".join(out) + "$", re.IGNORECASE if os.name == "nt" else 0)
    except re.error as error:
        raise ConfigError(f"invalid path pattern {pattern!r}: {error}") from None


def _code_paths(changed, cfg: dict, cache: dict):
    paths = cfg["code"]["paths"]
    excludes = cfg["code"]["exclude"]
    selected = []
    for kind, path, original in changed:
        if kind == "D":
            candidates = [path]
        else:
            candidates = [path] + ([original] if original else [])
        for candidate in candidates:
            if _matches_any(candidate, paths, cache) and not _matches_any(candidate, excludes, cache):
                selected.append(path)
                break
    return sorted(set(selected), key=lambda item: item)


EXEMPTION_LINE = re.compile(r"^[-*+]\s+(?:`([^`]+)`|(\S+))\s*(?:—|–|-{1,2}|:)\s*(.+)$")


def parse_exemptions(text: str):
    entries = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = EXEMPTION_LINE.match(stripped)
        if not match:
            continue
        pattern = match.group(1) or match.group(2)
        reason = match.group(3).strip()
        if pattern and reason:
            entries.append((pattern, reason))
    return entries


def check_same_batch(root: Path, cfg: dict, git: Git, staged: bool) -> dict:
    severity = cfg["checks"]["b"]
    record_rel = norm_rel(cfg["record"]["path"])
    record = root / record_rel
    changed = git.changed(staged)
    cache = {}
    code_paths = _code_paths(changed, cfg, cache)
    if not code_paths:
        return result("b", severity, note="no code-path changes in this batch")
    if not record.exists():
        return skip("b", severity, "record file is missing; see check a")

    tracked = _record_tracked(git, cfg, record_rel)
    record_changed = False
    if tracked:
        record_key = path_key(record_rel)
        record_changed = any(path_key(path) == record_key for _, path, _ in changed)
    findings = []
    if not record_changed and tracked:
        findings.append(
            finding(
                "block",
                "record-not-in-batch",
                "code paths changed but the record is not in the same batch",
                path=record_rel,
                fix="update the record and include it in this batch, or add a matching reason to the exemptions file",
            )
        )
    elif not tracked:
        tolerance = float(cfg["record"]["mtime_tolerance_seconds"])
        mtimes = [git.file_mtime(path) for path in code_paths]
        mtimes = [value for value in mtimes if value is not None]
        newest = max(mtimes) if mtimes else (git.head_time() or 0)
        try:
            record_mtime = record.stat().st_mtime
        except OSError:
            return skip("b", severity, "record file cannot be inspected; see check a")
        if record_mtime + tolerance < newest:
            findings.append(
                finding(
                    "block",
                    "record-stale",
                    "the local (untracked) record was not written after the newest code change in this batch",
                    path=record_rel,
                    fix="write/update the record after the code changes, then re-run preflight; the untracked-record check uses file modification time and only covers this machine",
                )
            )
    if findings:
        exemptions_path = root / norm_rel(cfg["exemptions"]["path"])
        if exemptions_path.is_file():
            try:
                entries = parse_exemptions(exemptions_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                entries = []
            if entries:
                uncovered = []
                for path in code_paths:
                    hit = None
                    for pattern, reason in entries:
                        try:
                            if glob_regex(pattern).match(path_key(path)):
                                hit = pattern
                                break
                        except ConfigError:
                            continue
                    if hit is None:
                        uncovered.append(path)
                if not uncovered:
                    note = "code changes covered by exemption file: " + " ".join(sorted({pattern for pattern, _ in entries}))[:300]
                    if tracked:
                        findings = [
                            finding(
                                "warn",
                                "record-exempt",
                                "the record gap is exempted by the configuration's exemptions file; the reason must also be in the batch receipt",
                                path=record_rel,
                                fix="keep the exemption scoped to this batch and record the reason",
                            )
                        ]
                    else:
                        findings = []
                    return result("b", severity, findings, note=note)
                findings.append(
                    finding(
                        "block",
                        "record-not-in-batch",
                        f"{len(uncovered)} code path(s) are not covered by the exemptions file",
                        path=record_rel,
                        fix="add a `- <glob> — <reason>` line for each uncovered path, or include the record in this batch",
                    )
                )
    note = None
    if not tracked:
        note = "untracked record: freshness checked by modification time (same-machine batch only)"
    return result("b", severity, findings, note=note)


def _evidence_prefix(cfg: dict):
    return re.compile(
        EVIDENCE_LINE.pattern.format(prefix=re.escape(cfg["evidence"]["prefix"])),
        re.MULTILINE,
    )


def parse_evidence_lines(text: str, cfg: dict):
    regex = _evidence_prefix(cfg)
    lines = []
    for number, line in enumerate(text.splitlines(), 1):
        match = regex.match(line)
        if match:
            lines.append((number, int(match.group(1)), line.strip()))
    return lines


def analyse_evidence(cfg: dict, content: str, old_content, root: Path, evidence_path: Path):
    """Return findings, added numbers and a note for checks c and d."""
    prefix = cfg["evidence"]["prefix"]
    evidence = parse_evidence_lines(content, cfg)
    old = parse_evidence_lines(old_content, cfg) if old_content is not None else []
    old_map = {number: line for _, number, line in old}
    old_numbers = set(old_map)
    changed_lines, added_numbers = [], []
    for source_line, number, line in evidence:
        if old_content is None or number not in old_map:
            changed_lines.append((source_line, number, line))
            added_numbers.append(number)
        elif line != old_map[number]:
            changed_lines.append((source_line, number, line))
    counts = {}
    for _, number, _ in evidence:
        counts[number] = counts.get(number, 0) + 1
    changed_numbers = {number for _, number, _ in changed_lines}
    duplicated = {
        number
        for number, count in counts.items()
        if count > 1 and number in changed_numbers
    }
    findings = []
    downgrade = old_content is None
    level = "warn" if downgrade else "block"
    if duplicated:
        for number in sorted(duplicated):
            findings.append(
                finding(
                    level,
                    "evidence-duplicate-number",
                    f"evidence number {prefix}{number} appears more than once",
                    line=None,
                    fix="give each evidence line a unique increasing number",
                )
            )
    for source_line, number, line in changed_lines:
        link = INLINE_LINK.search(line)
        if link is None:
            if cfg["evidence"]["allow_needs_source"] and "needs-source" in line:
                findings.append(
                    finding(
                        "warn",
                        "evidence-needs-source",
                        f"evidence line {prefix}{number} has no resolvable link and is marked needs-source",
                        line=source_line,
                        fix="replace needs-source with a resolvable link before the evidence gate closes",
                    )
                )
            else:
                findings.append(
                    finding(
                        level,
                        "evidence-missing-link",
                        f"evidence line {prefix}{number} has no Markdown link",
                        line=source_line,
                        fix="add a relative Markdown link to the evidence file",
                    )
                )
            continue
        target = link.group(1).strip()
        problem = evaluate_link(target, root, evidence_path)
        if problem is not None:
            findings.append(
                finding(
                    level,
                    "evidence-broken-link",
                    f"evidence line {prefix}{number}: {problem}",
                    line=source_line,
                    fix="link an existing evidence file relative to the evidence index or the project root",
                )
            )
    if added_numbers:
        expected = max(old_numbers) if old_numbers else 0
        ordered = added_numbers
        if ordered != sorted(ordered) or len(set(ordered)) != len(ordered):
            findings.append(
                finding(
                    level,
                    "evidence-number-order",
                    "new evidence numbers are not strictly increasing in file order",
                    fix="append new evidence with the next unused, strictly increasing number",
                )
            )
        elif ordered and ordered[0] <= expected:
            findings.append(
                finding(
                    level,
                    "evidence-number-order",
                    f"new evidence number {prefix}{ordered[0]} does not follow the baseline maximum {expected}",
                    fix="use a number greater than the largest existing evidence number",
                )
            )
    note = None
    if downgrade:
        note = "no Git baseline for the evidence index: all lines checked and failures downgraded to warnings"
    return findings, added_numbers, note


def evaluate_link(target: str, root: Path, evidence_path: Path) -> str:
    """Return a problem description for an evidence link, or None when it resolves."""
    if not target:
        return "empty link target"
    decoded = urllib.parse.unquote(target)
    if WINDOWS_DRIVE.match(decoded) or decoded.startswith("/"):
        return "absolute link targets are not portable and cannot be verified"
    parsed = urllib.parse.urlsplit(decoded)
    if parsed.scheme or parsed.netloc:
        return "external links cannot be verified as existing targets"
    path = urllib.parse.unquote(parsed.path).strip()
    if not path:
        return None  # same-file anchor
    resolved = None
    for candidate in (evidence_path.parent / path, root / path):
        if candidate.exists():
            resolved = candidate
            break
    if resolved is None:
        return "link target does not exist"
    if resolved.is_file() and not within(resolved, root):
        return "link target is outside the project root"
    return None


def _evidence_file(root: Path, cfg: dict) -> Path:
    configured = cfg["evidence"]["path"]
    relative = norm_rel(configured) if configured else norm_rel(cfg["record"]["path"])
    return root / relative


def check_evidence_links(root: Path, cfg: dict, git: Git, staged: bool) -> dict:
    severity = cfg["checks"]["c"]
    evidence = _evidence_file(root, cfg)
    if not evidence.is_file():
        if evidence != root / norm_rel(cfg["record"]["path"]):
            findings = [
                finding(
                    "block",
                    "evidence-index-missing",
                    "the configured evidence index file does not exist",
                    path=display_path(evidence, root),
                    fix="point evidence.path at the existing evidence index",
                )
            ]
            return result("c", severity, findings)
        return skip("c", severity, "evidence index is the record, which is missing; see check a")
    try:
        if staged and git.is_work_tree():
            raw = git.run("show", f":{norm_rel(evidence.relative_to(root))}")
            content = raw.stdout.decode("utf-8", "replace") if raw.returncode == 0 else None
        else:
            content = read_text_file(evidence)
    except (OSError, UnicodeDecodeError):
        return skip("c", severity, "evidence index cannot be read; see check a")
    if content is None:
        return skip("c", severity, "evidence index is not staged")
    old_content = None
    if git.is_work_tree() and git.head_exists():
        blob = git.blob("HEAD", norm_rel(evidence.relative_to(root)))
        if blob is not None:
            old_content = blob.decode("utf-8", "replace")
    findings, _, note = analyse_evidence(cfg, content, old_content, root, evidence)
    return result("c", severity, findings, note=note)


def check_baseline(root: Path, cfg: dict, git: Git, staged: bool) -> dict:
    severity = cfg["checks"]["d"]
    baseline = cfg["baseline"]
    if not baseline["enabled"]:
        return skip("d", severity, "baseline check is disabled (baseline.enabled=false)")
    evidence = _evidence_file(root, cfg)
    if not evidence.is_file():
        return skip("d", severity, "evidence index is missing")
    content = read_text_file(evidence)
    old_content = None
    old_available = False
    if git.is_work_tree() and git.head_exists():
        blob = git.blob("HEAD", norm_rel(evidence.relative_to(root)))
        if blob is not None:
            old_content = blob.decode("utf-8", "replace")
            old_available = True
    if not old_available:
        return skip("d", severity, "evidence index has no Git baseline; new evidence lines cannot be identified")
    _, added_numbers, _ = analyse_evidence(cfg, content, old_content, root, evidence)
    if not added_numbers:
        return result("d", severity, note="no new evidence lines in this batch")
    baseline_path = root / norm_rel(baseline["path"])
    pattern = _compile(baseline["pattern"], "baseline.pattern")
    try:
        current_text = read_text_file(baseline_path)
    except (OSError, UnicodeDecodeError):
        findings = [
            finding(
                "block",
                "baseline-unreadable",
                "the configured baseline file cannot be read",
                path=display_path(baseline_path, root),
                fix="fix baseline.path or restore the baseline file",
            )
        ]
        return result("d", severity, findings)
    current_match = pattern.search(current_text)
    if current_match is None:
        findings = [
            finding(
                "block",
                "baseline-unparsable",
                "the configured baseline pattern does not match the baseline file",
                path=display_path(baseline_path, root),
                fix="fix baseline.pattern so it captures the version",
            )
        ]
        return result("d", severity, findings)
    old_match = git.blob(baseline["ref"], norm_rel(baseline_path.relative_to(root)))
    old_value = None
    if old_match is not None:
        match = pattern.search(old_match.decode("utf-8", "replace"))
        if match:
            old_value = match.group(1) if match.groups() else match.group(0)
    if old_value is None:
        return skip("d", severity, "baseline file has no Git baseline; version increase cannot be compared")
    current_value = current_match.group(1) if current_match.groups() else current_match.group(0)
    if old_value is not None and not version_greater(current_value, old_value):
        findings = [
            finding(
                "block",
                "baseline-not-incremented",
                f"evidence lines were added but the baseline version did not increase ({old_value} -> {current_value})",
                path=display_path(baseline_path, root),
                fix="increment the declared baseline version in the configured file",
            )
        ]
        return result("d", severity, findings)
    return result("d", severity, note=f"baseline advanced ({old_value} -> {current_value})")


def version_greater(current: str, previous: str) -> bool:
    def parts(value: str):
        return [int(item) if item.isdigit() else item for item in re.split(r"[._-]", value)]

    try:
        return parts(current) > parts(previous)
    except TypeError:
        return current > previous


def check_limits(root: Path, cfg: dict) -> dict:
    severity = cfg["checks"]["e"]
    record = root / norm_rel(cfg["record"]["path"])
    if not record.is_file():
        return skip("e", severity, "record file is missing; see check a")
    try:
        content = read_text_file(record)
    except (OSError, UnicodeDecodeError):
        return skip("e", severity, "record cannot be read; see check a")
    lines = content.splitlines()
    findings = []
    max_lines = cfg["limits"]["record_max_lines"]
    max_length = cfg["limits"]["record_max_line_length"]
    if max_lines and len(lines) > max_lines:
        findings.append(
            finding(
                "block",
                "record-too-long",
                f"record has {len(lines)} lines; the configured limit is {max_lines}",
                path=display_path(record, root),
                fix="keep only the current node, authority, gates and recovery; move history to batch records",
            )
        )
    if max_length:
        for number, line in enumerate(lines, 1):
            if len(line) > max_length:
                findings.append(
                    finding(
                        "block",
                        "record-line-too-long",
                        f"record line {number} has {len(line)} characters; the configured limit is {max_length}",
                        path=display_path(record, root),
                        line=number,
                        fix="split or shorten the long line",
                    )
                )
                if len([item for item in findings if item["type"] == "record-line-too-long"]) >= 10:
                    break
    return result("e", severity, findings)


def _scan_candidates(git: Git, staged: bool):
    if staged:
        entries = git.changed(staged=True)
    else:
        entries = git.changed(staged=False)
    seen, paths = set(), []
    for kind, path, original in entries:
        if kind and kind[-1] == "D":
            continue
        if path not in seen:
            seen.add(path)
            paths.append(path)
    return paths


def check_secrets(root: Path, cfg: dict, git: Git, staged: bool) -> dict:
    severity = cfg["checks"]["f"]
    if not git.is_work_tree():
        return skip("f", severity, "not a Git work tree; pending content cannot be enumerated")
    patterns = [
        (item["type"], _compile(item["regex"], f"secrets.patterns[{index}].regex"))
        for index, item in enumerate(cfg["secrets"]["patterns"])
    ]
    if not patterns:
        return result("f", severity, note="no secret patterns configured")
    files = _scan_candidates(git, staged)
    if not files:
        return result("f", severity, note="no pending file changes")
    cache = {}
    excludes = cfg["secrets"]["exclude"]
    max_bytes = cfg["secrets"]["max_bytes"]
    findings, scanned, skipped = [], 0, []
    for relative in files:
        if _matches_any(relative, excludes, cache):
            continue
        if staged:
            proc = git.run("show", f":{relative}")
            data = proc.stdout if proc.returncode == 0 else None
        else:
            try:
                data = (root / relative).read_bytes()
            except OSError:
                data = None
        if data is None:
            continue
        if len(data) > max_bytes:
            skipped.append(relative)
            continue
        if b"\0" in data[:8192]:
            skipped.append(relative)
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            skipped.append(relative)
            continue
        scanned += 1
        reported = set()
        for number, line in enumerate(text.splitlines(), 1):
            for secret_type, regex in patterns:
                if secret_type in reported:
                    continue
                if regex.search(line):
                    reported.add(secret_type)
                    findings.append(
                        finding(
                            "block" if severity == "block" else "warn",
                            secret_type,
                            "secret-like content detected; the value is never printed",
                            path=relative,
                            line=number,
                            fix="remove or replace the value; rotate it if it was real; do not commit; full coverage needs a dedicated secret scanner",
                        )
                    )
                    break
    note = f"scanned {scanned} pending file(s)"
    if skipped:
        note += f"; skipped {len(skipped)} binary/oversized file(s)"
    return result("f", severity, findings, note=note)


def check_message(root: Path, cfg: dict, message_file) -> dict:
    severity = cfg["checks"]["g"]
    if message_file is None:
        return skip("g", severity, "no --message-file provided")
    path = Path(message_file)
    if not path.is_file():
        raise UsageError(f"--message-file does not exist: {message_file}")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise UsageError(f"cannot read --message-file: {error}") from None
    links = [
        _compile(pattern, f"message.banned_links[{index}]")
        for index, pattern in enumerate(cfg["message"]["banned_links"])
    ]
    trailers = [
        _compile(pattern, f"message.banned_trailers[{index}]")
        for index, pattern in enumerate(cfg["message"]["banned_trailers"])
    ]
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        if any(regex.search(line) for regex in links):
            findings.append(
                finding(
                    "block" if severity == "block" else "warn",
                    "message-link",
                    "the candidate message contains a session/share/chat link; the value is not printed",
                    path=str(path),
                    line=number,
                    fix="rewrite the message with a domain-neutral reason; keep opaque collaboration links out of commit metadata",
                )
            )
        if any(regex.search(line) for regex in trailers):
            findings.append(
                finding(
                    "block" if severity == "block" else "warn",
                    "message-trailer",
                    "the candidate message contains an agent session trailer",
                    path=str(path),
                    line=number,
                    fix="remove the trailer; keep only trailers required by project policy",
                )
            )
    return result("g", severity, findings, note="candidate message checked")


def check_identity(root: Path, cfg: dict, git: Git) -> dict:
    severity = cfg["checks"]["h"]
    identity = cfg["identity"]
    if identity["name"] is None:
        return skip(
            "h",
            severity,
            "identity policy is not configured; check h skipped and the identity gate is not passed",
        )
    if not git.is_work_tree():
        return skip("h", severity, "not a Git work tree; identity cannot be read")
    checks = [("author", "GIT_AUTHOR_IDENT")]
    if identity["check_committer"]:
        checks.append(("committer", "GIT_COMMITTER_IDENT"))
    findings = []
    for role, variable in checks:
        proc = git.run("var", variable)
        if proc.returncode != 0:
            findings.append(
                finding(
                    "block",
                    "identity-unavailable",
                    f"Git {role} identity is unknown",
                    fix=f"configure {role} identity for this commit (for example with single-commit -c overrides); do not edit global configuration",
                )
            )
            continue
        value = proc.stdout.decode("utf-8", "replace").strip()
        match = IDENTITY_LINE.match(value)
        if match is None:
            findings.append(
                finding(
                    "block",
                    "identity-unparsable",
                    f"Git {role} identity has an unexpected shape",
                    fix="inspect the effective identity and align it with the project policy",
                )
            )
            continue
        name_ok = match.group("name") == identity["name"]
        email_ok = match.group("email").lower() == identity["email"].lower()
        if not (name_ok and email_ok):
            findings.append(
                finding(
                    "block",
                    "identity-mismatch",
                    f"effective Git {role} identity differs from the configured policy",
                    fix="use a single-commit override (git -c user.name=... -c user.email=... commit) after verifying the policy; never change global configuration",
                )
            )
    return result("h", severity, findings, note="identity policy compared")


def check_readback(root: Path, cfg: dict, git: Git) -> dict:
    severity = cfg["checks"]["i"]
    ref = cfg["readback"]["ref"]
    sha = git.resolve(ref)
    if sha is None:
        raise UsageError(f"cannot resolve readback ref {ref!r} to a commit")
    short = sha[:12]
    record_rel = norm_rel(cfg["record"]["path"])
    if git.run("cat-file", "-e", f"{sha}:{record_rel}").returncode != 0:
        return skip(
            "i",
            severity,
            f"record is not version-controlled at {ref}; commit-diff readback is not applicable (documented limit)",
        )
    parents = git.parents(sha)
    if parents:
        changed = []
        for parent in parents:
            changed.extend(git.changed_between(parent, sha))
    else:
        changed = git.commit_files(sha)
    cache = {}
    code_paths = _code_paths(changed, cfg, cache)
    record_key = path_key(record_rel)
    record_changed = any(
        path_key(path) == record_key and kind != "D" for kind, path, _ in changed
    )
    findings = []
    if code_paths and not record_changed:
        findings.append(
            finding(
                "block",
                "readback-record-missing",
                f"commit {short} changes {len(code_paths)} code path(s) but not the record",
                path=record_rel,
                fix="reconcile the record within authorized scope and re-check; do not claim completion from a staged-only record",
            )
        )
    note = f"commit {short} inspected ({len(changed)} changed path(s))"
    return result("i", severity, findings, note=note)


# ---------------------------------------------------------------------------
# Checks j-o: hard constraints H1-H6 (references/hard-constraints.md)
# ---------------------------------------------------------------------------

THREE = {
    "zh": ("三句话", ("现在在", "下一步", "在等")),
    "en": ("Three sentences", ("Now at", "Next", "Waiting on")),
}
AUTH_HEADING = {"zh": "授权与作用域", "en": "Authorizations and scope"}
AUTH_SCOPE = {"zh": "适用", "en": "Applies to"}
AUTH_NOT_COVERED = {"zh": "不在该授权内", "en": "Not covered"}
REVIEW_HEADING = {"zh": "复审轮次", "en": "Review rounds"}
NAMED = re.compile(r"(?:点名|named by)\s*[：:]\s*([^；;。]*)", re.I)
EMPTY_VALUES = {"", "无", "none", "n/a", "-", "—"}
SENTENCE_END = re.compile(r"[。！？.!?][)）\"'”’」』\]*]*\s*$")
CODE_SPAN = re.compile(r"(`+).*?\1")
FIELD = re.compile(r"^\s*[-*+]\s*([^：:]+?)\s*[：:]\s*(.*)$")
DECISION_HEADING = re.compile(r"^##\s+(D\d+)\b(.*)$")
DECISION_FIELDS = {
    "type": ("类型", "type"),
    "rule": ("规则", "rule"),
    "relation": ("补充或取代", "relation"),
    "basis": ("依据", "basis"),
    "check": ("检查", "check"),
    "violations": ("违反", "violations"),
}


def _is_empty(value: str) -> bool:
    value = value.strip().rstrip("。.").strip()
    return value.lower() in EMPTY_VALUES or bool(re.fullmatch(r"<.*>", value))


def _prose_lines(text: str):
    """Yield (number, line) outside fenced blocks and HTML comments."""
    fence = None
    comment = False
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
            continue
        if marker:
            fence = marker.group(1)
            continue
        if comment or line.lstrip().startswith("<!--"):
            comment = "-->" not in line
            continue
        yield number, line


def _sections(text: str):
    """Map each level-2 heading title to its (number, line) prose lines."""
    sections, current, order = {}, None, []
    for number, line in _prose_lines(text):
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1)
            order.append(current)
            sections[current] = []
        elif current is not None and line.strip():
            sections[current].append((number, line))
    return sections, order


def _state_language(order):
    for language, (heading, _) in THREE.items():
        if order and order[0] == heading:
            return language
    return None


def _record_text(root: Path, cfg: dict):
    record = root / norm_rel(cfg["record"]["path"])
    if not record.is_file():
        return None, record
    try:
        return read_text_file(record), record
    except (OSError, UnicodeDecodeError):
        return None, record


def check_state_format(root: Path, cfg: dict) -> dict:
    severity = cfg["checks"]["j"]
    text, record = _record_text(root, cfg)
    if text is None:
        return skip("j", severity, "record is missing or unreadable; see check a")
    where = display_path(record, root)
    findings = []

    def add(kind, message, line=None, fix=None):
        if len(findings) < 25:
            findings.append(finding("block", kind, message, path=where, line=line, fix=fix))

    sections, order = _sections(text)
    language = _state_language(order)
    if language is None:
        add("state-three-sentences-missing",
            "the first level-2 section must be '## 三句话' or '## Three sentences'",
            fix="start the state with the fixed three-sentence section from the state template")
        language = "en" if re.search(r"(?m)^## [A-Za-z]", text) else "zh"
    else:
        labels = THREE[language][1]
        items = sections[THREE[language][0]]
        found = []
        for number, line in items:
            field = FIELD.match(line)
            if field is None:
                add("state-three-sentences-shape", "the three-sentence section holds only its three labelled bullets", line=number)
                continue
            found.append(field.group(1))
            if _is_empty(field.group(2)):
                add("state-three-sentences-empty", f"'{field.group(1)}' has no content", line=number)
        if found != list(labels):
            add("state-three-sentences-labels",
                "the three sentences must be, in order: " + " / ".join(labels),
                fix="answer where the work is, what happens next and who or what it waits on")

    id_pattern = _compile(cfg["state"]["id_pattern"], "state.id_pattern")
    banned = cfg["state"]["banned_tokens"]
    for number, line in _prose_lines(text):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("|"):
            continue
        plain = CODE_SPAN.sub("", stripped)
        if not SENTENCE_END.search(stripped):
            add("state-incomplete-sentence", "state prose must be complete sentences ending with a full stop",
                line=number, fix="rewrite the line as a full sentence; no shorthand fragments")
        for token in banned:
            if token in plain:
                add("state-shorthand", f"shorthand token '{token}' is not allowed in the state", line=number,
                    fix="spell the relation out in words")
        definition = re.match(r"^\s*(?:[-*+]\s+)?\[?(" + id_pattern.pattern + r")\]?(?=\s|[:：])", plain)
        for match in id_pattern.finditer(plain):
            if definition and match.start() == definition.start(1):
                continue
            if not re.match(r"\s?[（(]", plain[match.end():]):
                add("state-id-without-meaning", f"identifier {match.group(0)} is used without its meaning",
                    line=number, fix=f"write it as {match.group(0)}（meaning） / {match.group(0)} (meaning)")

    auth = sections.get(AUTH_HEADING[language])
    if auth is None:
        add("state-authorization-missing", f"the state needs a '## {AUTH_HEADING[language]}' section")
    else:
        scope, not_covered = AUTH_SCOPE[language], AUTH_NOT_COVERED[language]
        has_not_covered = False
        for number, line in auth:
            if not re.match(r"^[-*+]\s", line):
                continue
            label = FIELD.match(line)
            if label and label.group(1) == not_covered:
                has_not_covered = not _is_empty(label.group(2))
                continue
            if not re.search(re.escape(scope) + r"\s*[：:]\s*\S", line):
                add("state-authorization-scope", f"each authorization must state '{scope}:' (the rounds or tasks it covers)",
                    line=number, fix="name the task or round; a new task never inherits an older authorization")
        if not has_not_covered:
            add("state-not-covered-missing", f"the authorization section must say '{not_covered}:' explicitly",
                fix="list what the current task may not do under these authorizations")
    return result("j", severity, findings)


def _evidence_contents(root: Path, cfg: dict, git: Git, staged: bool):
    evidence = _evidence_file(root, cfg)
    if not evidence.is_file():
        return None, None, evidence
    relative = norm_rel(evidence.relative_to(root))
    content = None
    if staged and git.is_work_tree():
        raw = git.run("show", f":{relative}")
        content = raw.stdout.decode("utf-8", "replace") if raw.returncode == 0 else None
    if content is None:
        content = read_text_file(evidence)
    old = None
    if git.is_work_tree() and git.head_exists():
        blob = git.blob("HEAD", relative)
        old = None if blob is None else blob.decode("utf-8", "replace")
    return content, old, evidence


def changed_evidence(cfg: dict, content: str, old_content):
    """Evidence lines that are new or edited relative to old_content, plus new numbers."""
    old = {number: line for _, number, line in parse_evidence_lines(old_content, cfg)} if old_content is not None else {}
    changed, added = [], []
    for source_line, number, line in parse_evidence_lines(content, cfg):
        if old_content is None or number not in old:
            changed.append((source_line, number, line))
            added.append(number)
        elif line != old[number]:
            changed.append((source_line, number, line))
    return changed, added


def _baseline_values(root: Path, cfg: dict, git: Git):
    baseline = cfg["baseline"]
    if not baseline["enabled"] or not git.is_work_tree():
        return None, None
    pattern = _compile(baseline["pattern"], "baseline.pattern")
    path = norm_rel(baseline["path"])
    try:
        current = pattern.search(read_text_file(root / path))
    except (OSError, UnicodeDecodeError):
        return None, None
    blob = git.blob(baseline["ref"], path)
    old = pattern.search(blob.decode("utf-8", "replace")) if blob is not None else None
    value = lambda match: None if match is None else (match.group(1) if match.groups() else match.group(0))
    return value(current), value(old)


def _decision_numbers(text):
    return {match.group(1) for match in re.finditer(r"(?m)^##\s+(D\d+)\b", text or "")}


def check_evidence_kinds(root: Path, cfg: dict, git: Git, staged: bool) -> dict:
    severity = cfg["checks"]["k"]
    content, old, evidence = _evidence_contents(root, cfg, git, staged)
    if content is None:
        return skip("k", severity, "evidence index is missing; see checks a and c")
    where = display_path(evidence, root)
    prefix = cfg["evidence"]["prefix"]
    changed, added = changed_evidence(cfg, content, old)
    findings = []
    for line_no, number, line in changed:
        if not EVIDENCE_KIND.search(line):
            findings.append(finding("block", "evidence-kind-missing",
                                    f"{prefix}{number} is not tagged [门结论]/[变更]/[根因] ([gate]/[change]/[root-cause])",
                                    path=where, line=line_no,
                                    fix="register only gate conclusions, production/field changes and failure root causes; put the rest in the commit message"))
        if not DATE.search(line):
            findings.append(finding("block", "evidence-date-missing", f"{prefix}{number} has no YYYY-MM-DD date",
                                    path=where, line=line_no, fix="add the date the entry was registered"))
        if REVIEW_WORD.search(line) and not ROUND.search(line):
            findings.append(finding("block", "evidence-review-round-missing",
                                    f"{prefix}{number} records a review without its round number",
                                    path=where, line=line_no, fix="write 第N轮 / round N in the entry"))
    if not git.is_work_tree():
        return result("k", severity, findings, note="not a Git work tree; minor-batch and baseline rules skipped")
    cache = {}
    changes = git.changed(staged)
    records = {path_key(norm_rel(item)) for item in (cfg["record"]["path"], cfg["decisions"]["path"])}
    records.add(path_key(norm_rel(evidence.relative_to(root))))
    work = [path for _, path, _ in changes
            if path_key(path) not in records and not _matches_any(path, cfg["evidence"]["files"], cache)]
    current_version, old_version = _baseline_values(root, cfg, git)
    bumped = current_version is not None and old_version is not None and current_version != old_version
    if bumped and cfg["baseline"]["path"]:
        work = [path for path in work if path_key(path) != path_key(norm_rel(cfg["baseline"]["path"]))]
    minor = bool(work) and all(_matches_any(path, cfg["evidence"]["minor_paths"], cache) for path in work)
    if minor:
        if added:
            findings.append(finding("block", "minor-batch-evidence",
                                    "this batch only touches UI/copy/style paths but adds evidence entries",
                                    path=where, fix="drop the entries; describe the change in the commit message"))
        if bumped:
            findings.append(finding("block", "minor-batch-baseline",
                                    f"this batch only touches UI/copy/style paths but bumps the baseline ({old_version} -> {current_version})",
                                    fix="keep the baseline version; wording and style changes never bump it"))
        new_files = [path for kind, path, _ in changes
                     if (kind.startswith("A") or kind == "??") and _matches_any(path, cfg["evidence"]["files"], cache)]
        for path in new_files:
            findings.append(finding("block", "minor-batch-evidence-file",
                                    "this batch only touches UI/copy/style paths but creates an evidence file",
                                    path=path, fix="remove the new evidence file; the commit message is the record"))
    elif bumped and not added:
        decisions = root / norm_rel(cfg["decisions"]["path"])
        blob = git.blob("HEAD", norm_rel(cfg["decisions"]["path"]))
        new_decisions = _decision_numbers(read_text_file(decisions) if decisions.is_file() else "") - _decision_numbers(
            None if blob is None else blob.decode("utf-8", "replace"))
        if not new_decisions:
            findings.append(finding("block", "baseline-bump-without-basis",
                                    f"the baseline moved ({old_version} -> {current_version}) without a new evidence entry or decision",
                                    fix="bump only for a gate conclusion, field change, root cause or a registered decision"))
    return result("k", severity, findings)


def check_daily_evidence(root: Path, cfg: dict, git: Git, staged: bool) -> dict:
    severity = cfg["checks"]["l"]
    content, old, evidence = _evidence_contents(root, cfg, git, staged)
    if content is None:
        return skip("l", severity, "evidence index is missing; see checks a and c")
    limit = cfg["evidence"]["daily_limit"]
    counts = {}
    for _, _, line in parse_evidence_lines(content, cfg):
        date = DATE.search(line)
        if date:
            counts[date.group(1)] = counts.get(date.group(1), 0) + 1
    changed, _ = changed_evidence(cfg, content, old)
    dates = {DATE.search(line).group(1) for _, _, line in changed if DATE.search(line)}
    findings = [
        finding("block", "evidence-daily-threshold",
                f"{counts[date]} evidence entries are dated {date}; the threshold is {limit}",
                path=display_path(evidence, root),
                fix="check each entry is a gate conclusion, field change or root cause; fold the rest into commit messages")
        for date in sorted(dates) if counts.get(date, 0) > limit
    ]
    return result("l", severity, findings, note=f"threshold {limit} entries per day")


def check_review_rounds(root: Path, cfg: dict) -> dict:
    severity = cfg["checks"]["m"]
    text, record = _record_text(root, cfg)
    if text is None:
        return skip("m", severity, "record is missing or unreadable; see check a")
    sections, order = _sections(text)
    language = _state_language(order) or "zh"
    where = display_path(record, root)
    ledger = sections.get(REVIEW_HEADING[language])
    if ledger is None:
        return result("m", severity, [finding("block", "review-ledger-missing",
                                              f"the state needs a '## {REVIEW_HEADING[language]}' section (write '- 无。' / '- None.' when empty)",
                                              path=where)])
    findings = []
    for number, line in ledger:
        found = ROUND.search(line) if re.match(r"^[-*+]\s", line) else None
        if found is None:
            continue
        rounds = int(found.group(1) or found.group(2))
        named = NAMED.search(line)
        if rounds > 2 and (named is None or _is_empty(named.group(1))):
            findings.append(finding("block", "review-round-cap",
                                    f"review round {rounds} needs the owner to name it; stop here",
                                    path=where, line=number,
                                    fix="ask the owner; record 点名：<owner, source> / named by: <owner, source> before starting the round"))
    return result("m", severity, findings)


def parse_decisions(text: str):
    entries = []
    for number, line in _prose_lines(text):
        heading = DECISION_HEADING.match(line)
        if heading:
            entries.append({"id": heading.group(1), "title": heading.group(2).strip(), "line": number, "fields": {}})
            continue
        field = FIELD.match(line)
        if field and entries:
            label = field.group(1).strip().lower()
            for key, names in DECISION_FIELDS.items():
                if label in names:
                    entries[-1]["fields"][key] = field.group(2).strip()
    return entries


def check_decisions(root: Path, cfg: dict) -> dict:
    severity = cfg["checks"]["n"]
    path = root / norm_rel(cfg["decisions"]["path"])
    defaults = default_config()["checks"]
    relaxed = [key for key in "jklmno" if cfg["checks"][key] != defaults[key]]
    if not path.is_file():
        if relaxed:
            return result("n", severity, [finding("block", "severity-change-without-decision",
                                                  f"checks.{key} differs from the default but no decision register exists",
                                                  fix="register a decision whose rule names checks." + key)
                                          for key in relaxed])
        return skip("n", severity, "no decision register yet; create it from assets/decisions.template.md at the first rule change")
    try:
        text = read_text_file(path)
    except (OSError, UnicodeDecodeError):
        return result("n", severity, [finding("block", "decisions-unreadable", "the decision register cannot be read",
                                              path=display_path(path, root))])
    where = display_path(path, root)
    entries = parse_decisions(text)
    known = [entry["id"] for entry in entries]
    findings = []

    def add(kind, message, line, fix=None):
        findings.append(finding("block", kind, message, path=where, line=line, fix=fix))

    for duplicate in sorted({item for item in known if known.count(item) > 1}):
        add("decision-duplicate", f"{duplicate} is registered twice", None)
    for entry in entries:
        fields, ident, line = entry["fields"], entry["id"], entry["line"]
        if _is_empty(entry["title"].strip("（）() ")):
            add("decision-meaning-missing", f"{ident} heading has no meaning", line, f"write ## {ident}（meaning）")
        for key in ("type", "rule", "relation", "basis"):
            if _is_empty(fields.get(key, "")):
                add("decision-field-missing", f"{ident} lacks '{DECISION_FIELDS[key][0]} / {DECISION_FIELDS[key][1]}'", line)
        rule = fields.get("rule", "").lower()
        for word in VAGUE_WORDS:
            if word in rule:
                add("decision-vague-word", f"{ident} rule uses the undecidable word '{word}'", line,
                    "replace it with a threshold, a list or an observable event")
        hard = re.search(r"硬约束|hard", fields.get("type", ""), re.I)
        no_check = _is_empty(fields.get("check", ""))
        if hard and no_check:
            add("decision-check-missing", f"{ident} is a hard constraint without a mechanical check", line)
        violations = re.search(r"\d+", fields.get("violations", ""))
        if violations and int(violations.group(0)) >= 2 and no_check:
            add("decision-escalation-required",
                f"{ident} was violated {violations.group(0)} times and still has no check", line,
                "upgrade it to a hard constraint with a mechanical check; adding more text is not allowed")
        for ref in re.findall(r"\bD\d+\b", fields.get("relation", "")):
            if ref not in known:
                add("decision-unknown-reference", f"{ident} supersedes or supplements unknown {ref}", line)
    for key in relaxed:
        if not any(f"checks.{key}" in entry["fields"].get("rule", "") for entry in entries):
            add("severity-change-without-decision", f"checks.{key} differs from the default without a decision naming it", None,
                f"register a decision whose rule names checks.{key} and its reason")
    for name in cfg["decisions"]["executors"]:
        executor = root / norm_rel(name)
        if not executor.is_file():
            continue
        try:
            body = read_text_file(executor)
        except (OSError, UnicodeDecodeError):
            continue
        for number, line in enumerate(body.splitlines(), 1):
            for ref in re.findall(r"\bD\d+\b", line):
                if ref not in known:
                    findings.append(finding("block", "executor-unknown-decision",
                                            f"{name} points at {ref}, which is not in the register",
                                            path=name, line=number))
    return result("n", severity, findings, note=f"{len(entries)} decisions registered")


def check_branches(cfg: dict, git: Git) -> dict:
    severity = cfg["checks"]["o"]
    allowed = set(cfg["branches"]["allowed"])
    names = (git.text("for-each-ref", "--format=%(refname:short)", "refs/heads/") or "").splitlines()
    findings = [
        finding("block", "new-branch", f"local branch '{name}' is not on the allowed main-line list",
                fix="unless the owner asked for a branch: git worktree add --detach <path> <main>, then fast-forward main; "
                    "if asked, register the decision and add the branch to branches.allowed")
        for name in names if name and name not in allowed
    ]
    return result("o", severity, findings, note="allowed: " + ", ".join(sorted(allowed)))


# ---------------------------------------------------------------------------
# Hook installation (the only write this tool performs, and only on request)
# ---------------------------------------------------------------------------

HOOK_MARKER = "# delivery-harness preflight hook"


def install_hook(root: Path, cfg: dict, git: Git) -> dict:
    output = git.text("rev-parse", "--git-path", "hooks")
    if not output:
        raise UsageError("cannot resolve the repository hooks directory")
    hooks = Path(output.strip())
    hooks_dir = hooks.resolve() if hooks.is_absolute() else (root / hooks).resolve()
    if not within(hooks_dir, root):
        raise UsageError(
            f"refusing to install a hook outside the repository: {hooks_dir}"
        )
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook = hooks_dir / "commit-msg"
    if hook.exists():
        try:
            existing = hook.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            raise UsageError(f"cannot read the existing commit-msg hook: {error}") from None
        if HOOK_MARKER not in existing:
            raise UsageError(
                f"refusing to overwrite an unrelated commit-msg hook at {hook}; remove it or install manually"
            )
    python = cfg["hook"]["python"] or sys.executable
    script = Path(__file__).resolve().as_posix()
    python_display = Path(python).as_posix() if os.path.isabs(python) else python
    lines = [
        "#!/bin/sh",
        HOOK_MARKER + " (installed by references/preflight.py --install-hook)",
        "# Uninstall: delete this file. Reinstall after moving or updating the skill directory.",
        "root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0",
        f'exec "{python_display}" -B "{script}" --root "$root" --staged --message-file "$1"',
        "",
    ]
    try:
        with open(hook, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(lines))
        try:
            os.chmod(hook, 0o755)
        except OSError:
            pass
    except OSError as error:
        raise UsageError(f"cannot write the commit-msg hook: {error}") from None
    return {
        "hook": str(hook),
        "python": python_display,
        "script": script,
        "uninstall": f"delete {hook}",
    }


# ---------------------------------------------------------------------------
# Command line and output
# ---------------------------------------------------------------------------


class PreflightParser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def build_parser():
    parser = PreflightParser(
        prog="preflight.py",
        description="Mechanical preflight for Delivery Harness records and commits.",
    )
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="emit one machine-readable JSON object")
    parser.add_argument("--staged", action="store_true", help="check only the Git index (pre-commit)")
    parser.add_argument("--readback", action="store_true", help="verify the HEAD commit really contains the record change")
    parser.add_argument("--message-file", help="candidate commit message file to check")
    parser.add_argument("--install-hook", action="store_true", help="install the optional commit-msg hook, then exit")
    return parser


def parse_args(argv):
    args = build_parser().parse_args(argv)
    if args.install_hook and (args.readback or args.staged or args.message_file):
        raise UsageError("--install-hook cannot be combined with --staged, --readback or --message-file")
    if args.readback and args.staged:
        raise UsageError("--readback and --staged are mutually exclusive")
    if args.readback and args.message_file:
        raise UsageError("--readback checks an existing commit; --message-file is for candidate checks")
    return args


def resolve_mode(args) -> str:
    if args.install_hook:
        return "install-hook"
    if args.readback:
        return "readback"
    if args.staged:
        return "staged"
    return "default"


def run_checks(root: Path, cfg: dict, git: Git, mode: str, args):
    staged = mode == "staged"
    results = []
    if mode == "readback":
        results.append(check_readback(root, cfg, git))
        return results
    results.append(check_record(root, cfg))
    if git.is_work_tree():
        results.append(check_same_batch(root, cfg, git, staged))
        results.append(check_evidence_links(root, cfg, git, staged))
        results.append(check_baseline(root, cfg, git, staged))
    else:
        results.append(skip("b", cfg["checks"]["b"], "not a Git work tree; batch comparison unavailable"))
        results.append(skip("c", cfg["checks"]["c"], "not a Git work tree; evidence baseline unavailable"))
        results.append(skip("d", cfg["checks"]["d"], "not a Git work tree; evidence baseline unavailable"))
    results.append(check_limits(root, cfg))
    results.append(check_secrets(root, cfg, git, staged))
    results.append(check_message(root, cfg, args.message_file))
    results.append(check_identity(root, cfg, git))
    results.append(skip("i", cfg["checks"]["i"], "readback runs only with --readback"))
    results.append(check_state_format(root, cfg))
    results.append(check_evidence_kinds(root, cfg, git, staged))
    results.append(check_daily_evidence(root, cfg, git, staged))
    results.append(check_review_rounds(root, cfg))
    results.append(check_decisions(root, cfg))
    if git.is_work_tree():
        results.append(check_branches(cfg, git))
    else:
        results.append(skip("o", cfg["checks"]["o"], "not a Git work tree; branches unavailable"))
    return results


def summarise(results):
    return {
        "blocked": sum(1 for item in results if item["status"] == "fail"),
        "warned": sum(1 for item in results if item["status"] == "warn"),
        "skipped": sum(1 for item in results if item["status"] == "skip"),
        "passed": sum(1 for item in results if item["status"] == "pass"),
    }


def emit_human(version: str, mode: str, root: Path, source: str, results, notes):
    print(f"preflight {version} | mode={mode} | root={root} | config={source}")
    for item in results:
        label = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "skip": "SKIP"}[item["status"]]
        print(f"{label} {item['id']}  {item['title']}")
        if item.get("note"):
            print(f"     note: {item['note']}")
        for entry in item["findings"]:
            location = entry["path"] or ""
            if entry["line"]:
                location += f":{entry['line']}"
            print(f"       - {entry['type']}{' ' + location if location else ''}: {entry['message']}")
            if entry["fix"]:
                print(f"         fix: {entry['fix']}")
    for note in notes:
        print(f"note: {note}")
    summary = summarise(results)
    state = "FAIL" if summary["blocked"] else "PASS"
    print(
        f"RESULT: {state} ({summary['blocked']} blocked, {summary['warned']} warned, "
        f"{summary['skipped']} skipped, {summary['passed']} passed)"
    )


def emit_json(payload):
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def error_payload(message: str) -> dict:
    return {"schema": SCHEMA, "tool": TOOL, "status": "error", "error": message}


def main(argv) -> int:
    args = None
    try:
        args = parse_args(argv)
        root = Path(args.root).expanduser().resolve()
        if not root.is_dir():
            raise UsageError(f"--root is not a directory: {args.root}")
        mode = resolve_mode(args)
        cfg, source, notes = discover_config(root)
        git = Git(root)
        if mode in ("staged", "readback", "install-hook") and not git.is_work_tree():
            raise UsageError(f"not inside a Git work tree: {root}")
        version = tool_version()
        if mode == "install-hook":
            installed = install_hook(root, cfg, git)
            if args.json:
                emit_json(
                    {
                        "schema": SCHEMA,
                        "tool": TOOL,
                        "tool_version": version,
                        "mode": mode,
                        "root": str(root),
                        "config_source": source,
                        "status": "pass",
                        "install": installed,
                        "notes": notes,
                    }
                )
            else:
                print(f"INSTALLED {installed['hook']}")
                print(f"python: {installed['python']}")
                print(f"script: {installed['script']}")
                print(f"uninstall: {installed['uninstall']}")
            return EXIT_PASS
        results = run_checks(root, cfg, git, mode, args)
        summary = summarise(results)
        payload = {
            "schema": SCHEMA,
            "tool": TOOL,
            "tool_version": version,
            "mode": mode,
            "root": str(root),
            "config_source": source,
            "status": "fail" if summary["blocked"] else "pass",
            "summary": summary,
            "checks": results,
            "notes": notes,
        }
        if args.json:
            emit_json(payload)
        else:
            emit_human(version, mode, root, source, results, notes)
        return EXIT_FAIL if summary["blocked"] else EXIT_PASS
    except UsageError as error:
        message = f"usage error: {error}"
    except ConfigError as error:
        message = f"configuration error: {error}"
    except (GitError, OSError, subprocess.SubprocessError) as error:
        message = f"environment error: {error}"
    except Exception as error:  # pragma: no cover - defensive, value-free message
        message = f"internal error: {type(error).__name__}: {error}"
    if getattr(args, "json", False):
        emit_json(error_payload(message))
    else:
        print(f"preflight: {message}", file=sys.stderr)
    return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
