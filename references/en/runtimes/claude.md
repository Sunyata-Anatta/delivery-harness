# Claude Runtime Contract

Based on Anthropic's [Skills documentation](https://code.claude.com/docs/en/slash-commands) and [plugin reference](https://code.claude.com/docs/en/plugins-reference); facts last verified on 2026-08-20.

## Installation

Claude Code's user-level directory is `$HOME/.claude/skills/delivery-harness`; its project-level directory is `<project>/.claude/skills/delivery-harness`. From this Skill repository root, copy the same four items used for Codex, changing only the target root to `.claude/skills/delivery-harness`.

PowerShell:

```powershell
$target = Join-Path $HOME ".claude\skills\delivery-harness"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -LiteralPath ".\SKILL.md" -Destination $target -Force
foreach ($name in "agents", "assets", "references") {
  Copy-Item -LiteralPath ".\$name" -Destination $target -Recurse -Force
}
```

The current Claude Code plugin format also supports a single-Skill plugin whose root contains only one `SKILL.md`; it does not require an additional `skills/` wrapper. This repository shape can be the content source for such a plugin, but actual distribution still follows Claude Code's plugin installation and trust flow. When support in the installed version cannot be confirmed, use the standalone copy path above.

## Discovery and Invocation

Start a new Claude Code session and enter:

```text
/delivery-harness Start from current reality and continue until the accepted evidence gates pass.
```

When a project needs automatic loading, put the fixed block from [CLAUDE.block.template.md](../../../assets/CLAUDE.block.template.md) in the `CLAUDE.md` that the project actually loads. Claude Code can discover a new Skill during a session, but version updates and automatic-loading verification still require a fresh session.

## Arrival Verification

1. Verify the four-item target manifest and per-file hashes.
2. Confirm `/delivery-harness` appears among available commands and can be invoked explicitly.
3. Start a context-free session and confirm the fixed startup block appears before the first tool call.
4. Repeat at least five times and record the Claude Code version, successes, and failures.

Proving only that `/delivery-harness` can be invoked does not prove that automatic loading through `CLAUDE.md` is active.

## Update

For a standalone installation, completely overwrite all four items; for a plugin installation, update through its plugin source. Save the old copy or version, then restart the session and rerun arrival verification. A personal Claude Code Skill takes precedence over a project Skill, while plugin Skills are namespaced. Check each actual source during update; do not guess precedence.

## Uninstall and Rollback

For a standalone installation, remove only the exact `delivery-harness` target directory; for a plugin installation, use Claude Code's plugin uninstall path. If `CLAUDE.md` still contains the entry block, remove or rewrite it as well. Roll back by restoring the complete old copy or old plugin version.

## Known Boundaries

- A single-Skill root plugin is a current format capability; current documentation does not prove support in an unverified older runtime.
- A Skill uploaded to Claude.ai and a local Claude Code Skill are separate deployment surfaces and must be verified separately.
- `agents/openai.yaml` does not configure Claude; do not invent a `claude.yaml`.
- Only fresh-session ordering evidence can prove that automatic loading is active.

Pre-inject a marked block through the effective user or project `CLAUDE.md`. Native `paths` conditions are runtime-specific adapters, not portable frontmatter. Reinvoking the same Skill does not guarantee removal of prior body text.

Native entry addendum checked 2026-09-08: [official documentation](https://code.claude.com/docs/en/skills).
