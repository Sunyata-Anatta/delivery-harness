"""Demo repository for the hard constraints and the formatting flow.

Each test builds a throwaway Git repository, shows a check failing on the
anti-pattern, applies the fix and shows the same check passing:

  state lint (j), daily evidence count (l), review round cap (m), formatting
  flow (format_flow.py markers/tree + line-length guard template), plus the
  other hard-constraint checks (k, n, o) and the skill's own rule table.

Run: python -m unittest discover -s tests -v
Needs git; the formatting test also needs node and `npx prettier@3.3.3` (skipped otherwise).
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "references" / "preflight.py"
FORMAT_FLOW = ROOT / "references" / "format_flow.py"
GUARD = ROOT / "assets" / "line-length-guard.test.template.mjs"
PRETTIER = "prettier@3.3.3"

GOOD_STATE = """# Harness 状态

## 三句话

- 现在在：登录页修复已经实现，正在等第一轮复审的结论。
- 下一步：根据复审结论决定是否合并到主线。
- 在等：负责人对第一轮复审的结论。

## 范围与活动节点

- 目标与边界：示例仓库的主线，只包含登录页。
- 活动节点：登录页修复；状态：等证据。

## 授权与作用域

- 来源：负责人 2026-10-25 的会话指令；获准动作：本地提交；范围：登录页；适用：登录页修复这一个任务。
- 不在该授权内：推送、发布和任何新任务。

## 证据与未知结果

{evidence}
## 复审轮次

- 登录页修复：第 {round} 轮；点名：{named}。

## 恢复入口

- 恢复入口：本文件与提交历史。
"""

BAD_STATE = """# 状态

## 当前

- N2 done → 等 R1
- 授权：push ok
"""


def evidence_lines(count, date="2026-10-25"):
    return "".join(
        f"- E{n} [门结论] {date} 第 {n} 项门检查通过；[回执](artifacts/r.md)。\n" for n in range(1, count + 1)
    )


class Repo:
    def __init__(self, base: Path):
        self.path = base / "demo"
        self.path.mkdir()
        self.git("init", "-q", "-b", "main")
        for key, value in (("user.name", "Example Author"), ("user.email", "author@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
            self.git("config", key, value)
        self.write(".delivery/artifacts/r.md", "receipt\n")

    def git(self, *args, check=True):
        proc = subprocess.run(["git", *args], cwd=self.path, capture_output=True, text=True, encoding="utf-8")
        if check and proc.returncode != 0:
            raise AssertionError(f"git {args} failed: {proc.stderr}")
        return proc.stdout.strip()

    def write(self, relative, text):
        path = self.path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def config(self, **overrides):
        data = {"schema": 1, "record": {"path": ".delivery/state.md"}}
        data.update(overrides)
        self.write(".delivery/preflight.json", json.dumps(data, ensure_ascii=False))

    def state(self, evidence="", round_=1, named="无"):
        self.write(".delivery/state.md", GOOD_STATE.format(evidence=evidence, round=round_, named=named))

    def commit(self, message="change"):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def preflight(self):
        proc = subprocess.run([sys.executable, "-B", "-X", "utf8", str(PREFLIGHT), "--root", str(self.path), "--json"],
                              capture_output=True, text=True, encoding="utf-8")
        payload = json.loads(proc.stdout)
        return proc.returncode, {item["id"]: item for item in payload["checks"]}

    def run(self, *cmd, env=None):
        return subprocess.run(list(cmd), cwd=self.path, capture_output=True, text=True, encoding="utf-8",
                              env=dict(os.environ, **(env or {})))


def kinds(check):
    return {item["type"] for item in check["findings"]}


@unittest.skipUnless(shutil.which("git"), "git is required")
class HardConstraintDemo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Repo(Path(self.tmp.name))
        self.repo.config()

    def tearDown(self):
        self.tmp.cleanup()

    def test_state_lint_fails_on_shorthand_then_passes(self):
        self.repo.write(".delivery/state.md", BAD_STATE)
        self.repo.commit("bad state")
        code, checks = self.repo.preflight()
        self.assertEqual(code, 1)
        self.assertEqual(checks["j"]["status"], "fail")
        self.assertTrue({"state-three-sentences-missing", "state-shorthand", "state-id-without-meaning",
                         "state-incomplete-sentence", "state-authorization-missing"} <= kinds(checks["j"]))
        self.assertEqual(checks["m"]["status"], "fail")
        self.repo.state()
        self.repo.commit("good state")
        code, checks = self.repo.preflight()
        self.assertEqual((checks["j"]["status"], checks["m"]["status"]), ("pass", "pass"), checks["j"]["findings"])
        self.assertEqual(code, 0)

    def test_state_over_eighty_lines_fails(self):
        self.repo.state(evidence="".join(f"补充说明第 {n} 句。\n" for n in range(60)))
        _, checks = self.repo.preflight()
        self.assertEqual(checks["e"]["status"], "fail")

    def test_daily_evidence_count_prompts_then_passes(self):
        self.repo.state()
        self.repo.commit("baseline")
        self.repo.state(evidence=evidence_lines(6))
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["l"]["status"]), (0, "warn"))  # default: a prompt, not a block
        self.repo.config(checks={"l": "block"})
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["l"]["status"]), (1, "fail"))
        self.assertEqual(kinds(checks["n"]), {"severity-change-without-decision"})  # changing a severity needs a decision
        self.repo.write(".delivery/decisions.md", "## D1（每日计数改为阻断）\n\n- 类型：规则。\n"
                        "- 规则：checks.l 设为 block，超过每日阈值即阻断提交。\n- 补充或取代：补充 H1。\n"
                        "- 依据：示例复盘。\n- 检查：preflight 检查 l。\n- 违反：0 次。\n")
        _, checks = self.repo.preflight()
        self.assertEqual(checks["n"]["status"], "pass", checks["n"]["findings"])
        self.repo.state(evidence=evidence_lines(5))
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["l"]["status"], checks["k"]["status"]), (0, "pass", "pass"))

    def test_evidence_kind_and_minor_batch(self):
        self.repo.write("web/style.css", "a { color: red; }\n")
        self.repo.state()
        self.repo.commit("baseline")
        self.repo.write("web/style.css", "a { color: blue; }\n")
        self.repo.state(evidence="- E1 2026-10-25 按钮颜色调整；[回执](artifacts/r.md)。\n")
        _, checks = self.repo.preflight()
        self.assertTrue({"evidence-kind-missing", "minor-batch-evidence"} <= kinds(checks["k"]))
        self.repo.state()
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["k"]["status"]), (0, "pass"))

    def test_third_review_round_blocks_until_owner_names_it(self):
        self.repo.state(round_=3)
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["m"]["status"]), (1, "fail"))
        self.assertIn("stop here", checks["m"]["findings"][0]["message"])
        self.repo.state(round_=3, named="负责人张三，2026-10-25 会话指令")
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["m"]["status"]), (0, "pass"))

    def test_decision_register_rejects_vague_or_unchecked_rules(self):
        self.repo.state()
        entry = ("## D1（复审上限）\n\n- 类型：硬约束。\n- 规则：{rule}\n- 补充或取代：新规则。\n"
                 "- 依据：示例审阅报告。\n- 检查：{check}\n- 违反：2 次。\n")
        self.repo.write(".delivery/decisions.md", entry.format(rule="必要时限制复审轮次。", check="无。"))
        code, checks = self.repo.preflight()
        self.assertEqual(code, 1)
        self.assertTrue({"decision-vague-word", "decision-check-missing", "decision-escalation-required"}
                        <= kinds(checks["n"]))
        self.repo.write(".delivery/decisions.md",
                        entry.format(rule="同一改动的独立复审超过 2 轮时停止。", check="preflight 检查 m。"))
        self.repo.write("AGENTS.md", "- 复审上限见 D1（复审上限），由 preflight 检查。\n- 另见 D9。\n")
        _, checks = self.repo.preflight()
        self.assertEqual(kinds(checks["n"]), {"executor-unknown-decision"})
        self.repo.write("AGENTS.md", "- 复审上限见 D1（复审上限），由 preflight 检查。\n")
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["n"]["status"]), (0, "pass"))

    def test_new_branch_fails_detached_worktree_passes(self):
        self.repo.state()
        self.repo.commit("baseline")
        self.repo.git("branch", "feature")
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["o"]["status"]), (1, "fail"))
        self.repo.git("branch", "-D", "feature")
        worktree = Path(self.tmp.name) / "parallel"
        self.repo.git("worktree", "add", "--detach", str(worktree), "main")
        (worktree / "notes.txt").write_text("parallel task\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=worktree, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "parallel task"], cwd=worktree, check=True)
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=worktree, capture_output=True, text=True).stdout.strip()
        self.repo.git("merge", "--ff-only", sha)
        self.repo.git("worktree", "remove", str(worktree))
        code, checks = self.repo.preflight()
        self.assertEqual((code, checks["o"]["status"]), (0, "pass"))
        self.assertEqual(self.repo.git("rev-parse", "main"), sha)

    def test_raw_templates_fail_only_on_unfilled_placeholders(self):
        for language in ("", "en"):
            with self.subTest(language=language or "zh"):
                self.repo.write(".delivery/state.md",
                                (ROOT / "assets" / language / "harness-state.template.md").read_text(encoding="utf-8"))
                _, checks = self.repo.preflight()
                self.assertTrue(kinds(checks["j"]) <= {"state-three-sentences-empty", "state-not-covered-missing"},
                                checks["j"]["findings"])
                self.assertEqual(checks["m"]["status"], "pass")


def prettier_available():
    if not (shutil.which("node") and shutil.which("npx")):
        return False
    try:
        return subprocess.run(["npx", "--yes", PRETTIER, "--version"], capture_output=True, timeout=180).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


LONG_SOURCE = "export const table = {" + ",".join(f"k{n}:{n}" for n in range(60)) + "};\n" \
              'export const label = "' + "x" * 200 + '";\n'
SOURCE_TEST = """import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
test('table keeps its first keys', () => {
  const src = readFileSync('src/app.js', 'utf8');
  assert.ok(src.includes('k0:0,k1:1'));
});
"""


@unittest.skipUnless(shutil.which("git"), "git is required")
class FormattingFlowDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not prettier_available():
            raise unittest.SkipTest(f"node/npx with {PRETTIER} unavailable (environment, not a regression)")

    def flow(self, repo, *args):
        return repo.run(sys.executable, "-B", "-X", "utf8", str(FORMAT_FLOW), "--root", str(repo.path), *args)

    def test_format_markers_guard_and_tree_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Repo(Path(tmp))
            repo.write("src/app.js", LONG_SOURCE)
            repo.write("test/app.test.mjs", SOURCE_TEST)
            repo.write("test/guard.test.mjs", GUARD.read_text(encoding="utf-8"))
            pre = repo.commit("before formatting")
            guard_env = {"GUARD_ROOTS": "src", "GUARD_MAX": "100"}
            self.assertNotEqual(repo.run("node", "--test", "test/guard.test.mjs", env=guard_env).returncode, 0,
                                "the guard must fail on the pre-format code")

            style = self.flow(repo, "style")
            self.assertEqual(style.returncode, 0, style.stderr)
            config = json.loads(style.stdout)
            self.assertEqual(config["embeddedLanguageFormatting"], "off")
            repo.write(".prettierrc.json", style.stdout)
            self.assertEqual(repo.run("npx", "--yes", PRETTIER, "--write", "src").returncode, 0)
            formatted = repo.commit("style: mechanical formatting only")

            lost = self.flow(repo, "markers", "--old", pre)
            self.assertEqual(lost.returncode, 1, lost.stdout)
            self.assertIn("LOST test/app.test.mjs:6", lost.stdout)
            repo.write("test/app.test.mjs", SOURCE_TEST.replace("src.includes('k0:0,k1:1')",
                                                                "/k0:\\s*0,\\s*k1:\\s*1/.test(src)"))
            repo.commit("test: read formatted source")
            fixed = self.flow(repo, "markers", "--old", pre)
            self.assertEqual(fixed.returncode, 0, fixed.stdout)
            self.assertEqual(repo.run("node", "--test", "test/guard.test.mjs", env=guard_env).returncode, 0)
            self.assertEqual(repo.run("node", "--test", "test/app.test.mjs").returncode, 0)

            # Target machine: replay the formatting on the old commit in a detached worktree, compare trees.
            replay = Path(tmp) / "replay"
            repo.git("worktree", "add", "--detach", str(replay), pre)
            (replay / ".prettierrc.json").write_text(style.stdout, encoding="utf-8")
            subprocess.run(["npx", "--yes", PRETTIER, "--write", "src"], cwd=replay, capture_output=True, check=True)
            expected = repo.git("rev-parse", f"{formatted}^{{tree}}")
            same = subprocess.run([sys.executable, str(FORMAT_FLOW), "--root", str(replay), "tree", "--ref", "WORKTREE",
                                   "--expect", expected], capture_output=True, text=True)
            self.assertEqual(same.returncode, 0, same.stdout + same.stderr)
            (replay / "src" / "app.js").write_text("drift\n", encoding="utf-8")
            drift = subprocess.run([sys.executable, str(FORMAT_FLOW), "--root", str(replay), "tree", "--ref", "WORKTREE",
                                    "--expect", expected], capture_output=True, text=True)
            self.assertEqual(drift.returncode, 1)
            repo.git("worktree", "remove", "--force", str(replay))


class SkillRuleTable(unittest.TestCase):
    """H5 applied to the skill itself: every hard constraint names an existing mechanical check."""

    def test_every_hard_constraint_has_a_check(self):
        sys.path.insert(0, str(PREFLIGHT.parent))
        try:
            import preflight  # noqa: E402
        finally:
            sys.path.pop(0)
        for language in ("", "en"):
            text = (ROOT / "references" / language / "hard-constraints.md").read_text(encoding="utf-8")
            rows = re.findall(r"(?m)^\| \[?(H\d)\]?.*\|\s*`?([a-o](?:[, ]+[a-o])*)`?\s*\|\s*$", text)
            with self.subTest(language=language or "zh"):
                self.assertEqual([h for h, _ in rows], [f"H{n}" for n in range(1, 7)], "rule table rows")
                for _, checks in rows:
                    for check in re.findall(r"[a-o]", checks):
                        self.assertIn(check, preflight.CHECK_TITLES)


if __name__ == "__main__":
    unittest.main()
