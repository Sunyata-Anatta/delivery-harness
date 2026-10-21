#!/usr/bin/env python3
"""Delivery Harness preflight: mechanical checks for records and commits.

A single-file, standard-library tool for Python 3.9+. It reads the project
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
        "evidence": {"path": None, "prefix": "E", "allow_needs_source": False},
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
        "checks": {key: "block" for key in "abcdefghi"},
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
# Checks a-i
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
