#!/usr/bin/env python3
"""Delivery Harness formatting flow helpers (standard library, Python 3.9+).

Subcommands (contract: references/formatting.md and references/en/formatting.md):

  style    measure the existing JavaScript style and print a minimal-diff
           Prettier config (majority quotes, semicolons, indentation,
           embedded-language formatting off).
  markers  list the source-text markers that tests look for (indexOf,
           includes, startsWith, endsWith, regex .test/.match) and report the
           ones present in the old source but missing from the new source.
  tree     print the tree hash of a ref or of the working tree, and compare it
           with --expect.

Exit codes: 0 = pass, 1 = check failed, 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

SOURCE_EXT = (".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".vue")
TEST_HINT = re.compile(r"(^|/)(tests?|__tests__)/|\.(test|spec)\.[cm]?[jt]sx?$")
READS_SOURCE = re.compile(r"readFileSync|readFile\(|fs\.promises")
STRING_CALL = re.compile(r"\.(?:indexOf|includes|startsWith|endsWith|lastIndexOf)\(\s*(['\"`])((?:\\.|(?!\1).)*)\1")
REGEX_CALL = re.compile(r"(?<![\w)\]])/((?:\\.|\[(?:\\.|[^\]])*\]|[^/\\\n\[])+)/([a-z]*)\s*\.(?:test|exec)\(")
MATCH_CALL = re.compile(r"\.(?:match|search|matchAll|replace)\(\s*/((?:\\.|\[(?:\\.|[^\]])*\]|[^/\\\n\[])+)/([a-z]*)")


def git(root: Path, *args, env=None, check=True) -> str:
    proc = subprocess.run(["git", "-c", "core.autocrlf=true", *args], cwd=root, capture_output=True, env=env)
    if check and proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout.decode("utf-8", "replace")


def tracked(root: Path, ref: str = None):
    if ref:
        return [p for p in git(root, "ls-tree", "-r", "--name-only", ref).splitlines() if p]
    return [p for p in git(root, "ls-files", "--cached", "--others", "--exclude-standard").splitlines() if p]


def read(root: Path, path: str, ref: str = None) -> str:
    if ref:
        return git(root, "show", f"{ref}:{path}", check=False)
    try:
        return (root / path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


# --------------------------------------------------------------------------- style


def cmd_style(args) -> int:
    root = Path(args.root).resolve()
    sources = [p for p in tracked(root) if p.endswith(SOURCE_EXT) and not TEST_HINT.search(p)]
    quotes, semi, indent, crlf = Counter(), Counter(), Counter(), 0
    for path in sources:
        text = read(root, path)
        crlf += text.count("\r\n")
        for line in text.splitlines():
            code = re.sub(r"//.*$", "", line).rstrip()
            quotes["single"] += len(re.findall(r"(?<![\w\\])'", code)) // 2
            quotes["double"] += len(re.findall(r"(?<![\w\\])\"", code)) // 2
            if re.search(r"[\w)\]'\"`]$", code) and not re.match(r"\s*(if|for|while|else|function|class|\}|//|\*)", code):
                semi["without"] += 1
            elif code.endswith(";"):
                semi["with"] += 1
            lead = re.match(r"^(\s+)\S", line)
            if lead:
                indent["tab" if lead.group(1).startswith("\t") else len(lead.group(1))] += 1
    widths = Counter({k: v for k, v in indent.items() if k != "tab"})
    tab_width = 2 if not widths else min((2, 4), key=lambda w: -sum(v for k, v in widths.items() if k % w == 0))
    config = {
        "singleQuote": quotes["single"] >= quotes["double"],
        "semi": semi["with"] >= semi["without"],
        "useTabs": indent["tab"] > sum(widths.values()),
        "tabWidth": tab_width,
        "printWidth": args.print_width,
        "trailingComma": "es5",
        "endOfLine": "auto",
        "embeddedLanguageFormatting": "off",
    }
    print(json.dumps(config, indent=2))
    print(json.dumps({"files": len(sources), "quotes": quotes, "semicolons": semi,
                      "indent": {str(k): v for k, v in indent.items()}, "crlf_lines": crlf}), file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- markers


def test_markers(root: Path, ref: str, globs):
    """Yield (path, line, kind, marker, flags) for tests that read source text."""
    for path in tracked(root, ref):
        if not TEST_HINT.search(path) or not path.endswith(SOURCE_EXT):
            continue
        if globs and not any(Path(path).match(g) for g in globs):
            continue
        text = read(root, path, ref)
        if not READS_SOURCE.search(text):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for match in STRING_CALL.finditer(line):
                if "${" not in match.group(2):
                    yield path, number, "string", unescape(match.group(2)), ""
            for pattern in (REGEX_CALL, MATCH_CALL):
                for match in pattern.finditer(line):
                    yield path, number, "regex", match.group(1), match.group(2)


def unescape(value: str) -> str:
    return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t", "r": "\r"}.get(m.group(1), m.group(1)), value)


def present(marker: str, kind: str, flags: str, text: str):
    if kind == "string":
        return marker in text
    py = (re.I if "i" in flags else 0) | (re.M if "m" in flags else 0) | (re.S if "s" in flags else 0)
    try:
        return re.search(marker, text, py) is not None
    except re.error:
        return None


def cmd_markers(args) -> int:
    root = Path(args.root).resolve()
    sources = lambda ref: "\n".join(read(root, p, ref) for p in tracked(root, ref)
                                    if p.endswith(SOURCE_EXT) and not TEST_HINT.search(p))
    new_ref = None if args.new == "WORKTREE" else args.new
    old_text, new_text = sources(args.old), sources(new_ref)
    rows = list(test_markers(root, new_ref, args.tests))
    lost, unparsed = [], []
    for path, number, kind, marker, flags in rows:
        before, after = present(marker, kind, flags, old_text), present(marker, kind, flags, new_text)
        if before is None or after is None:
            unparsed.append((path, number, marker))
        elif before and not after:
            lost.append((path, number, kind, marker))
    print(f"source-reading markers scanned: {len(rows)}")
    if args.list:
        for path, number, kind, marker, _ in rows:
            print(f"MARKER {path}:{number} {kind} {marker!r}")
    for path, number, kind, marker in lost:
        print(f"LOST {path}:{number} {kind} {marker!r}")
    for path, number, marker in unparsed:
        print(f"REVIEW {path}:{number} regex not portable to Python: {marker!r}")
    print(f"RESULT: {'FAIL' if lost else 'PASS'} ({len(lost)} lost, {len(unparsed)} to review by hand)")
    return 1 if lost else 0


# --------------------------------------------------------------------------- tree


def worktree_tree(root: Path) -> str:
    """Tree hash of the working tree (tracked + untracked, ignore rules applied) via a temp index."""
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(tmp) / "index"))
        git(root, "read-tree", "HEAD", env=env, check=False)
        git(root, "add", "-A", env=env)
        return git(root, "write-tree", env=env).strip()


def cmd_tree(args) -> int:
    root = Path(args.root).resolve()
    value = worktree_tree(root) if args.ref == "WORKTREE" else git(root, "rev-parse", f"{args.ref}^{{tree}}").strip()
    print(value)
    if args.expect is None:
        return 0
    same = value == args.expect.strip()
    print(f"RESULT: {'PASS' if same else 'FAIL'} (expected {args.expect.strip()})")
    return 0 if same else 1


def main(argv) -> int:
    parser = argparse.ArgumentParser(prog="format_flow.py", description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    style = sub.add_parser("style", help="print a minimal-diff Prettier config")
    style.add_argument("--print-width", type=int, default=100)
    markers = sub.add_parser("markers", help="report test markers lost by formatting")
    markers.add_argument("--old", required=True, help="ref before formatting")
    markers.add_argument("--new", default="HEAD", help="ref after formatting, or WORKTREE (default HEAD)")
    markers.add_argument("--tests", nargs="*", default=[], help="optional test path globs")
    markers.add_argument("--list", action="store_true", help="also print every scanned marker (pre-format inventory)")
    tree = sub.add_parser("tree", help="print or compare a tree hash")
    tree.add_argument("--ref", default="HEAD", help="ref, or WORKTREE for the working tree")
    tree.add_argument("--expect", help="tree hash that must match")
    args = parser.parse_args(argv)
    return {"style": cmd_style, "markers": cmd_markers, "tree": cmd_tree}[args.command](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
