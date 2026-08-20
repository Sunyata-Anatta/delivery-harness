# Claude Code Runtime Contract

Primary sources: [Skills](https://code.claude.com/docs/en/slash-commands) and [plugins](https://code.claude.com/docs/en/plugins-reference); checked 2026-08-20.

## Installation
Copy the complete tree to `$HOME/.claude/skills/delivery-harness` or `<project>/.claude/skills/delivery-harness`. A current single-skill plugin may also use a root `SKILL.md`; use standalone copy when version support is uncertain.

## Discovery and invocation
Open a new session and invoke `/delivery-harness`. For auto-load, add the English [CLAUDE block](../../../assets/en/CLAUDE.block.template.md) to the effective `CLAUDE.md`.

## Arrival verification
Compare manifest/hashes; verify command discovery and invocation; verify startup receipt before first tool call in a fresh session; repeat twice and record version/success/failure. Invocation alone does not prove CLAUDE auto-load.

## Update
Replace all four items for standalone installs or use plugin-source update, then retest in a fresh session. Check actual personal/project/plugin precedence.

## Uninstall and rollback
Remove the exact standalone directory or use plugin uninstall; remove stale entry block. Restore the complete prior source to roll back.

## Known boundaries
Claude.ai uploads and Claude Code local skills are separate. OpenAI metadata does not configure Claude. Auto-load requires sequence evidence.
