# Runtime Installation and Arrival Verification

The repository root is the installable Skill. `SKILL.md`, `agents/`, `assets/`, and `references/` form one source. Runtime adapters cover discovery, invocation, and lifecycle only. Runtime facts were checked against primary documentation on **2026-08-20**; recheck after product changes.

| Runtime | Typical target | Invocation | Contract |
|---|---|---|---|
| Codex | `$HOME/.agents/skills/delivery-harness` | `$delivery-harness` | [codex.md](runtimes/codex.md) |
| Claude Code | `$HOME/.claude/skills/delivery-harness` | `/delivery-harness` | [claude.md](runtimes/claude.md) |
| OpenClaw | Git/local installer | `$delivery-harness` or `/delivery-harness` | [openclaw.md](runtimes/openclaw.md) |
| Hermes | `$HOME/.hermes/skills/delivery-harness` | `/delivery-harness` | [hermes.md](runtimes/hermes.md) |
| Other hosts | host-declared directory | host help | [generic-agent-skills.md](runtimes/generic-agent-skills.md) |

Copy the complete four-item tree from a clean checkout. Do not ship `.git/`, project state, development tests, reviews, or caches. A second `SKILL.md` means the source has forked and blocks release.

Installation proves discoverability; an effective project instruction block enables auto-load. Use [AGENTS](../../assets/en/AGENTS.block.template.md), [CLAUDE](../../assets/en/CLAUDE.block.template.md), or [generic runtime](../../assets/en/restricted-runtime-entry.block.template.md) template. Append when absent; replace the full marked block when present. Do not create instruction files the runtime never reads.

## Four evidence levels

1. **Bytes:** identical manifests and per-file hashes.
2. **Content:** valid frontmatter, links, resources, and skill validator.
3. **Runtime:** runtime lists/parses the skill and completes explicit invocation.
4. **Sequence and statistics:** fresh-session startup receipt precedes first tool call; record samples, successes, failures, repetitions, versions, time, and limits.

File presence is not runtime loading; runtime listing is not timely rule delivery. Release requires at least levels 1–3. Auto-load claims require level 4.

Before update, save a hash manifest or recoverable full copy. Replace all four items, update marked project blocks, then rerun evidence per runtime. Uninstall only the exact skill directory/registration and remove stale project entry blocks. Roll back with the full prior copy and same evidence level. Remote rewrite, global configuration, and account actions remain independent gates.
