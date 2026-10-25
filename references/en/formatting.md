# Code Formatting Flow

Read this when a project first adopts a formatter, or when code contains overlong single lines and needs a one-time layout pass. The goal is a replayable, verifiable mechanical step: minimal diff, separate from logic changes, no tests broken by layout, and no overlong lines growing back. The tools ship in the payload: [format_flow.py](../format_flow.py) (standard library) and the [line-length guard template](../../assets/line-length-guard.test.template.mjs) (Node built-in test runner, no dependencies).

Below, `<skill>` is the installed delivery-harness directory and `<pre>` is the commit before formatting.

## 1. Configure: pinned version, parameters from the existing style

1. Measure the existing style read-only: `python -B -X utf8 <skill>/references/format_flow.py --root . style > .prettierrc.json`. Standard error reports quote, semicolon, indentation and CRLF counts; check them before use.
2. The generated config follows the majority for quotes, semicolons and indentation, and fixes three settings: `embeddedLanguageFormatting: "off"` (no formatting of embedded HTML, CSS, SQL and similar templates), `endOfLine: "auto"` (existing line endings stay), and `printWidth` equal to the guard limit (default 100).
3. Call the pinned version through npx without touching `package.json` or adding a dependency: `npx --yes prettier@3.3.3 --write <paths>`. Record the version in the decision; upgrading it means repeating this flow.
4. Put generated files, third-party code and snapshots in `.prettierignore`.

## 2. Commit it alone and register a decision

1. The worktree must be clean before formatting; run only the npx command above, with no manual edits mixed in.
2. The commit contains only the config file and the formatting result, and its message names the tool and version, for example `style: mechanical formatting (prettier 3.3.3)`. Logic changes and test fixes go in later commits.
3. Add a decision to the [decision register](../../assets/en/decisions.template.md) of type "baseline" that names the formatting commit, the tool version and config, and states that every release package and file hash changes after formatting, so references to old hashes stop being valid. The baseline moves because of this decision.

## 3. Tests that depend on source layout: scan first, then rewrite each one

1. Before formatting, list how tests read source text (`indexOf`, `includes`, `startsWith`, `endsWith`, regex `.test`/`.match`): `format_flow.py --root . markers --old HEAD --list`. Only tests that read source files (`readFileSync` and similar) are scanned.
2. After the formatting commit, find markers present in the old source and missing from the new source: `format_flow.py --root . markers --old <pre>`. Every `LOST file:line` must be changed. Markers that cannot be translated to a Python regex are listed as `REVIEW` and checked by hand.
3. Rewrite them so layout no longer matters: prefer asserting runtime behavior; when the test must read source, use a regex that tolerates whitespace (for example `/a:\s*1,\s*b:\s*2/`). Rerun step 2 until `RESULT: PASS`.
4. From then on, write no new tests that depend on source layout; new tests assert behavior.

## 4. Line-length guard test

1. Copy the [guard template](../../assets/line-length-guard.test.template.mjs) into the project test directory and set `GUARD_ROOTS` (source directories, comma-separated) and `GUARD_MAX` (equal to `printWidth`).
2. The guard removes strings, template literals (including `${...}` expressions), regex literals and comments before measuring each code line, so long text never trips it while a truly long code line always does. The template carries self-test cases for those five removals and for division not being mistaken for a regex.
3. Prove it fails: run it on the pre-format commit, where it must be red. Use a detached worktree per [H6](hard-constraints.md#h6): `git worktree add --detach ../pre-format <pre>`, copy the guard in, run `node --test <guard file>`, confirm a non-zero exit, then `git worktree remove ../pre-format`. Register that result as a `[gate]` evidence entry.
4. Run it on the formatted commit, where it must be green.

## 5. Full regression: separate environment failures from real ones

Run the full project suite and report failures as two lists:

| Category | Typical signal | Handling |
|---|---|---|
| Environment | Docker unavailable; permission errors such as `EACCES` or `EPERM`; a wave of `ECONNREFUSED` (local database not running); shallow clone missing history (`bad object`, `unknown revision`, `shallow`) | Fix the environment and rerun the same tests; until then the result is neither a pass nor a regression |
| Real | Every other failure | Diagnose through the debugging flow; the formatting commit itself must introduce no real failure |

Write both lists into one evidence entry with the reason for each classification.

## 6. Cross-machine delivery: replay the formatting plus a small patch

Formatting is deterministic, so the target machine does not need the whole formatted code package:

1. On the source machine export the logic changes after formatting: `git format-patch <formatting commit>..HEAD -o <patch dir>`.
2. On the target machine (which has `<pre>`) create a detached worktree: `git worktree add --detach <temp path> <pre>`; write the same config and run the same pinned npx command.
3. Compare tree hashes: `format_flow.py --root <temp path> tree --ref WORKTREE --expect <tree hash of the source formatting commit>`; the source gets the expected value with `git rev-parse <formatting commit>^{tree}`. When they differ, stop and look for config, version or line-ending differences first.
4. Commit the replay, apply the small patch with `git am <patch dir>/*.patch`, and check the final result with `tree --ref HEAD --expect <tree hash of the source HEAD>`.
5. Commit IDs on the target differ from the source (different author times); acceptance is equal tree hashes. When identical commit IDs are required, transfer a `git bundle` instead.
6. In the main worktree run `git merge --ff-only <commit>` to fast-forward the main line, then `git worktree remove <temp path>`.

## Known pitfalls

- For read-only git in a Linux mount of a repository checked out on Windows, pass `-c core.autocrlf=true`; otherwise hundreds of false modifications appear. `format_flow.py` already passes it when it calls git.
- After a container restart the local PostgreSQL may be stopped; when tests fail with a wave of `ECONNREFUSED`, check the database before calling it a regression.
- An untracked file with the same name in the target worktree blocks a fast-forward merge. When the content is identical (same hash), delete it and merge; when it differs, stop and ask instead of overwriting.
- With a shallow clone missing history objects, history-dependent tests fail. Fetch limited history first with `git fetch --deepen=<limited depth>` before judging, instead of recording those failures as regressions.
