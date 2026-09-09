# Runtime Installation and Arrival Verification

The repository root is the installable Skill. `SKILL.md`, `agents/`, `assets/`, and `references/` form the single canonical source; runtime adapters describe discovery, invocation, and lifecycle without copying execution rules.

Runtime facts here were verified against product primary documentation on **2026-08-20**. Recheck the relevant runtime documentation after product changes before changing commands.

## Runtime routes

| Runtime | Typical installation entry | Explicit invocation | Detailed contract |
|---|---|---|---|
| Codex App, CLI, IDE | `$HOME/.agents/skills/delivery-harness` | `$delivery-harness` | [codex.md](runtimes/codex.md) |
| Claude Code | `$HOME/.claude/skills/delivery-harness` | `/delivery-harness` | [claude.md](runtimes/claude.md) |
| OpenClaw | `openclaw skills install git:<owner>/<repo>@<ref> --global` | composable `$delivery-harness` or `/delivery-harness` | [openclaw.md](runtimes/openclaw.md) |
| Hermes Agent | `$HOME/.hermes/skills/delivery-harness` | `/delivery-harness` | [hermes.md](runtimes/hermes.md) |
| Other Agent Skills hosts | host-declared user or project directory | host help | [generic-agent-skills.md](runtimes/generic-agent-skills.md) |

## One-copy boundary

From a clean checkout root, copy these four items into a target directory named `delivery-harness`:

```text
SKILL.md
agents/
assets/
references/
```

Do not copy `.git/`, project state, development tests, review records, or local caches. A second `SKILL.md` in the repository blocks release because the canonical source has forked.

## Distribution surface registry

Trigger: before first installation, update, release, or when a new runtime/account-sync entry is discovered, register the complete distribution surface inventory in the project overlay. Each entry states runtime, resolver or address, update method, canonical source, required evidence level, last verification, limits, and rollback. Filesystem targets, plugin installation, account synchronization, uploaded Skills, and hosted entries are separate surfaces and cannot substitute evidence for one another.

Method: enumerate project installation records, runtime listings, plugin/account management surfaces, and local targets; then use the runtime's actual resolution result to detect omissions. Success means every known surface has one resolver or address and a current evidence state. Keep an unknown or unreachable surface as `unverified`, record the unblock condition, and **must not claim that every distribution surface is updated**. On drift, stop the release-complete claim, replace that surface completely, and restart verification at the byte level. Register evidence in the overlay and active state.

## Project auto-load

Installation proves runtime discovery; a project instruction block makes a new session actively load the Skill. They cannot substitute for each other.

| Instruction surface | Template |
|---|---|
| `AGENTS.md` | [AGENTS.block.template.md](../../assets/en/AGENTS.block.template.md) |
| `CLAUDE.md` | [CLAUDE.block.template.md](../../assets/en/CLAUDE.block.template.md) |
| Other persistent project instruction file | [restricted-runtime-entry.block.template.md](../../assets/en/restricted-runtime-entry.block.template.md) |

Append when absent; replace the entire `delivery-harness:start` / `delivery-harness:end` block when present. Never create an instruction file the runtime does not read merely to claim auto-load. When no instruction surface exists, retain explicit invocation and register that boundary.

## Four deployment evidence levels

Start with cheap deterministic checks, then increase risk:

1. **Bytes:** identical target/source manifests and per-file hashes prove no missing or drifting content.
2. **Content:** valid frontmatter, links, required resources, and dedicated validator prove readable structure.
3. **Runtime:** the target runtime lists or parses `delivery-harness` and completes one explicit invocation, proving actual discovery.
4. **Sequence and statistics:** a fresh session emits the startup receipt before its first tool call; record samples, successes, failures, repetitions, versions, time, and limits, proving stable strong-rule arrival.

**File presence is not runtime loading; runtime listing is not timely rule delivery.** Release requires levels 1-3. Any auto-load claim requires level 4.

For each level, record source version, target runtime version, criterion, exit code or observation, sample count, time, and known limitations. Diagnostics are non-persistent by default and redacted before archival.

## Shared update rules

- Save the old directory hash or a recoverable copy before update.
- Replace all four items, never only `SKILL.md`.
- Rerun byte, content, and runtime evidence after replacement.
- Replace the entire marked project auto-load block when its version changes.
- Verify every coexisting runtime separately; one runtime's success cannot represent another.
- Read the distribution surface registry before update. Register a newly resolved source first; treat unknown or unreachable surfaces as an evidence-gate failure.

## Shared uninstall and rollback rules

- Remove only the exact `delivery-harness` runtime directory or registration; never delete project data.
- If project rules still require Harness, remove or replace its auto-load entry before uninstall to avoid a stale reference.
- Restore the full prior copy and rerun the same evidence level for rollback.
- Remote history rewrite, global configuration, and third-party account actions remain separate authority gates.

## Release criteria

Before release, all are true: repository root installs directly; only one `SKILL.md`; no hard executable dependency; every local link resolves; all five runtime contracts cover installation, discovery, arrival, update, uninstall, and boundaries; at least one target runtime completes a real invocation; every claimed auto-loaded runtime has fresh-session sequence evidence; and the distribution surface registry contains no silently omitted target.

## Pre-injection, cold invocation and context budgets

Inject only the marked receipt contract, never the full Skill, overlay, history or capability group. It must be visible before the first tool; “read the Skill then emit” cannot satisfy that order. Without pre-injection, an explicit cold invocation may read the Skill and selected core before its receipt, with the first business tool after it. Score the two entries separately; neither proves the other.

Measure newly injected Harness text using `o200k_base`: marked block <=250 tokens; SKILL + selected core <=1000; active state <=600; overlay startup summary <=450; ordinary startup total <=2300. Restore active summaries and pointers only; read history/process/long Resolver on demand. Report host-injected skill catalogs, tool inventory, global rules and cache separately. This is not a host-total context cap or a promise that previously read content unloads.

For each reachable runtime run at least 5 fresh pre-injected sessions, checking the first visible receipt, first tool event, actual read path, selected language and one real task. Separately test explicit cold entry, missing capabilities, unreadable text and source conflicts. No tool event, template echoes or old-session cache do not constitute full behavioral passes. Record every sample and never mark unreachable runtimes passed.
