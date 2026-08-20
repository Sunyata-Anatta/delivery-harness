# Codex Runtime Contract

Primary source: [OpenAI Agent Skills](https://developers.openai.com/codex/skills); checked 2026-08-20.

## Installation
Copy the complete tree to user `$HOME/.agents/skills/delivery-harness` or a project `.agents/skills/delivery-harness`. Do not create a new default under `$CODEX_HOME/skills`.

## Discovery and invocation
Open a new session and invoke `$delivery-harness`. For project auto-load, install the English [AGENTS block](../../../assets/en/AGENTS.block.template.md). Duplicate names are not merged; record selected source.

## Arrival verification
Compare manifest/hashes; verify listing or explicit invocation; in a context-free session verify `【Startup Receipt】` and `【Capability Signal Assessment】` before the first tool call; repeat twice and record version, successes, and failures.

## Update
Back up, replace the complete tree, open a new session, and repeat verification. Synchronize or explicitly select duplicate project/user sources.

## Uninstall and rollback
Remove only the exact skill directory and stale AGENTS block. Restore a complete backup for rollback.

## Known boundaries
Running sessions may cache skills. `agents/openai.yaml` is OpenAI metadata. ChatGPT and local Codex are separate deployment surfaces.
