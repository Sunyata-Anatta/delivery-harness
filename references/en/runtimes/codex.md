# Codex Runtime Contract

Based on OpenAI's [Agent Skills documentation](https://developers.openai.com/codex/skills); facts last verified on 2026-08-20.

## Installation

The user-level target is `$HOME/.agents/skills/delivery-harness`. The project-level target is `.agents/skills/delivery-harness`, discoverable while walking from the working directory to the repository root.

PowerShell, run from this Skill repository root:

```powershell
$target = Join-Path $HOME ".agents\skills\delivery-harness"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -LiteralPath ".\SKILL.md" -Destination $target -Force
foreach ($name in "agents", "assets", "references") {
  Copy-Item -LiteralPath ".\$name" -Destination $target -Recurse -Force
}
```

POSIX shell:

```bash
target="$HOME/.agents/skills/delivery-harness"
mkdir -p "$target"
cp SKILL.md "$target/"
cp -R agents assets references "$target/"
```

Do not copy this repository to `$CODEX_HOME/skills` as a new default. The current general discovery path is `.agents/skills`.

## Discovery and Invocation

Start a new Codex session, inspect the Skill list, or enter:

```text
$delivery-harness Start from current reality and continue until the accepted evidence gates pass.
```

When a project needs automatic loading, append the fixed block from [AGENTS.block.template.md](../../../assets/AGENTS.block.template.md) to the `AGENTS.md` that the project actually loads. Codex does not merge same-name Skills; multiple sources can appear in the selector at once. Verification must record the path actually selected. Open a fresh session after changes.

## Arrival Verification

1. Verify the target directory's four-item manifest and per-file hashes.
2. Confirm Codex can list or explicitly invoke `delivery-harness`.
3. Start a context-free session and check for `【Startup Receipt】` and `【Capability Signal Assessment】` before the first tool call.
4. Repeat at least five times and record successes, failures, and the Codex version.

A directory that exists without runtime discovery evidence is not a successful installation.

## Update

First save the target-directory hashes or a backup, then completely overwrite all four items with the installation command. Restart the session and repeat arrival verification. If a same-name project copy exists, update it too or verify the path actually selected; do not assume the runtime merges copies or automatically chooses the newest one.

## Uninstall and Rollback

Remove the exact target directory; do not recursively operate on its `.agents/skills` parent. For rollback, restore the complete backup, reopen the session, and verify again. If the project's `AGENTS.md` still contains an automatic-loading block, remove or rewrite that block as well.

## Known Boundaries

- A running session can cache Skills; verify updates in a fresh session.
- `agents/openai.yaml` is OpenAI interface metadata, not an entry file for other runtimes.
- Same-name Skills can coexist without merging; results from one project do not prove another.
- Skill availability in ChatGPT and Codex local discovery paths are separate deployment surfaces and must be verified separately.

Pre-injection may use a marked block in global `$CODEX_HOME/AGENTS.md` or the effective project `AGENTS.md`. `allow_implicit_invocation` affects Skill selection, not delivery of the startup contract. Check that project-instruction size limits do not truncate the block.

Native entry addendum checked 2026-09-08: [official documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
