"""Repository-only structural checks; these do not prove semantic/runtime safety.

Run: python -m unittest discover -s tests -v
Report soft template sizes separately: python tests/test_document_contract.py --sizes
No installed dependency beyond Python's standard library; inventory uses local Git.
"""

import html
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = (Path(), Path("en"))
SECTIONS = {"ownership", "reading", "triggers", "procedure", "recovery", "verification"}
DESTINATION = r'(<[^>\n]+>|(?:\\.|[^\s()]|\([^()\n]*\))+)'
INLINE_LINK = re.compile(r'\[[^\]\n]*\]\(\s*' + DESTINATION + r'(?:\s+[\'\"][^\n]*?[\'\"])?\s*\)')
REFERENCE = re.compile(r'^ {0,3}\[[^\]\n]+\]:\s*' + DESTINATION, re.M)
EXPLICIT_ANCHOR = re.compile(r'<a\b[^>]*\b(?:id|name)\s*=\s*[\'\"]([^\'\"]+)[\'\"]', re.I)


def prose(markdown):
    """Remove comments and fenced examples, preserving headings/line boundaries."""
    lines, fence = [], None
    for line in re.sub(r"<!--.*?-->", "", markdown, flags=re.S).splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            lines.append("")
        elif marker:
            fence = marker[1]
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def anchors(markdown):
    """Explicit anchors and GitHub-style ATX/setext heading slugs, with duplicates."""
    text = prose(markdown)
    found, used = set(EXPLICIT_ANCHOR.findall(text)), set()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        title = heading[1] if heading else None
        if title is None and line.strip() and i + 1 < len(lines) and re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[i + 1]):
            title = line.strip()
        if title is None:
            continue
        title = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", title)
        title = html.unescape(re.sub(r"<[^>]*>", "", title))
        base = re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-")
        slug, suffix = base, 0
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        found.add(slug)
    return found


def local_links(source, markdown):
    text = re.sub(r"(`+).*?\1(?!`)", "", prose(markdown), flags=re.S)
    for pattern in (INLINE_LINK, REFERENCE):
        for match in pattern.finditer(text):
            destination = html.unescape(match[1].strip("<>"))
            if re.search(r"\{\{|\}\}|\$\{|<[^>]+>", destination):
                continue  # Downstream paths are filled when a template is adopted.
            destination = re.sub(r"\\([^\w\s])", r"\1", destination)
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path)
            target = (source.parent / path).resolve() if path else source
            yield target, unquote(parsed.fragment), destination


def public_markdown():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "*.md"],
        cwd=ROOT, check=True, stdout=subprocess.PIPE,
    )
    paths = {Path(name.decode("utf-8")) for name in result.stdout.split(b"\0") if name}
    return sorted(ROOT / p for p in paths if not {".delivery", ".git"}.intersection(p.parts) and (ROOT / p).is_file())


class DocumentContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = {p: p.read_text(encoding="utf-8") for p in public_markdown()}
        cls.links = {p: list(local_links(p, text)) for p, text in cls.documents.items()}

    def test_local_files_and_fragments(self):
        self.assertTrue(self.documents, "No public Markdown discovered")
        for source, links in self.links.items():
            for target, fragment, destination in links:
                with self.subTest(source=str(source.relative_to(ROOT)), link=destination):
                    self.assertTrue(target.exists(), f"Missing target: {target}")
                    if fragment and target.suffix.lower() == ".md" and target.is_file():
                        self.assertIn(fragment, anchors(target.read_text(encoding="utf-8")),
                                      f"Missing anchor: {destination}")

    def test_bilingual_counterparts(self):
        for directory, templates_only in (("references", False), ("assets", True)):
            root = ROOT / directory
            counterparts = []
            for language in LANGUAGES:
                base = root / language
                files = {p.relative_to(base) for p in self.documents if p.is_relative_to(base)}
                files = {p for p in files if p.parts[0] != "en"
                         and (not templates_only or p.name.endswith(".template.md"))}
                counterparts.append(files)
            chinese, english = counterparts
            allowed = {Path("index.md")} if directory == "references" else set()
            with self.subTest(directory=directory):
                self.assertEqual(chinese - english, set(), "Missing English counterpart")
                self.assertEqual(english - chinese - allowed, set(), "Missing Chinese counterpart")

    def test_state_template_matches_distributed_skeleton(self):
        for language in LANGUAGES:
            base = ROOT / "assets" / language
            template = base / "harness-state.template.md"
            skeleton = base / "delivery-skeleton/.delivery/state.md"
            with self.subTest(language=str(language)):
                self.assertTrue(template.is_file(), f"Missing template: {template}")
                self.assertTrue(skeleton.is_file(), f"Missing skeleton: {skeleton}")
                self.assertEqual(template.read_bytes(), skeleton.read_bytes(), "State copy drift")

    def test_lifecycle_navigation_and_compatibility(self):
        for language in LANGUAGES:
            base = ROOT / "references" / language
            lifecycle, core, execution = (base / name for name in ("context-lifecycle.md", "core.md", "execution.md"))
            with self.subTest(language=str(language)):
                for path in (lifecycle, core, execution):
                    self.assertIn(path, self.documents, f"Missing public document: {path}")
                self.assertFalse(SECTIONS - anchors(self.documents[lifecycle]), "Missing lifecycle section anchors")
                self.assertIn(lifecycle, {target for target, _, _ in self.links[core]},
                              "Core must expose the lifecycle entry")
                self.assertIn("state-size", anchors(self.documents[execution]), "Legacy fragment must remain valid")
                self.assertIn(lifecycle, {target for target, _, _ in self.links[execution]},
                              "Legacy execution reference must route to lifecycle")

    def test_install_payload_has_one_skill_entry(self):
        entries = []
        for name in ("SKILL.md", "agents", "assets", "references"):
            root = ROOT / name
            self.assertTrue(root.exists(), f"Missing install root: {name}")
            paths = [root] if root.is_file() else root.rglob("SKILL.md")
            entries.extend(p.relative_to(ROOT).as_posix() for p in paths if p.is_file() and p.name == "SKILL.md")
        self.assertEqual(sorted(entries), ["SKILL.md"], "Nested Skill entry in the four-root payload")


def report_sizes():
    print("Soft template targets only; exceeding them does not fail a check. Tokens are not measured.")
    budgets = {"harness-state": 80, "process-index": 30, "evidence-summary": 50, "artifact-readme": 30}
    for language in LANGUAGES:
        for name, target in budgets.items():
            path = ROOT / "assets" / language / f"{name}.template.md"
            if path.is_file():
                data = path.read_bytes()
                lines = len(data.splitlines())
                print(f"{path.relative_to(ROOT)}: {lines} physical lines, {len(data)} bytes; "
                      f"soft line target {target}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--sizes"]:
        report_sizes()
    else:
        unittest.main()
