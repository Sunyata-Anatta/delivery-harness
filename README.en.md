# Delivery Harness

[中文](README.md) | [English](README.en.md)

`delivery-harness` is an Agent Skill for multi-stage delivery. It continues within existing authority and uses current project state, real evidence and explicit gates to decide the next action. Specialist Skills, MCPs and CLIs do the work; Harness keeps goals, authority, state and verification aligned.

## Loading

Startup needs a short entry, `SKILL.md` and one language core. Read execution, installation, publishing and provider details only when their actions occur.

| Layer | Contents | When to read |
|---|---|---|
| Native startup block | Receipt shape, pending unknowns, core entry | Before the first tool in a new session |
| One language core | Unique active state, action routes, lasting boundaries | When the Skill is invoked |
| Action rules | Nodes, evidence, commits, deployment, debugging | Before the relevant event |
| Provider/project detail | Installation, Resolver, historical evidence | When the current selection needs it |

`language=auto|zh|en` follows explicit choice, project-session lock, dominant message language, then UI language. Code and logs do not switch it. Read one language core and reference tree. English starts at the [core](references/en/core.md).

Harness text budgets use `o200k_base`: startup block <=250 tokens, SKILL + selected core <=1000, active state <=600, overlay startup summary <=450, ordinary startup total <=2300. Count host-injected skill catalogs, tools and other global rules separately. These budgets promise neither whole-conversation savings nor removal of previously loaded content. See the [budget and verification contract](references/en/runtime-installation.md).

## Project adoption

| Scenario | Approach |
|---|---|
| Temporary question or small task | Work in the session without state directories |
| New project | Default `.delivery/state.md`, overlay and evidence slots |
| Existing governance | Preserve rules; map one state pointer and its fields, never dual-write |
| Restricted runtime | Invoke explicitly and record unavailable pre-injection |
| Self-bootstrap | Installed baseline governs candidate changes; synchronize after verification |

`.delivery/state.md` stays in version control by default. Explicit privacy deviations require recovery and verification records. `uploads/`, `artifacts/` and `debug/` are ignored by default. Follow [safe initialization](references/en/project-initialization.md), the [complete skeleton](assets/en/delivery-skeleton.template.md) and [overlay template](assets/en/project-overlay.template.md); merge existing content incrementally.

This repository's own `.delivery/` holds legitimate development state, plans, tests and reviews, kept local under its public-distribution boundary. Companion case studies have independent goals and records, linked through findings only.

## Capability groups and routing

Candidate groups are `research`, `engineering`, `verification`, `documents`, `operations` and `domain`. Groups narrow selection without loading every body. `profile=auto|research|develop|review|document|operate` changes candidate order, never authority.

Filter task, directory, language, offline, data and authority constraints first. Then rank current user choice > most-specific directory binding > project Resolver > user preference > profile > new candidate. Read only the selected provider. Fall back in configured order; missing required capability leaves its evidence gate failed. Record Skill, plugin, MCP and CLI sources and verification separately.

Use the project overlay Resolver. Move long tables to one `.delivery/routing.md`, leaving a pointer in the overlay. After source/compatibility checks and a small-task test, add new Skills as candidates without changing Harness core. Temporary choices never become global defaults automatically. Unresolved same-name sources cannot be silently selected. Recheck tools and authentication when switching Agents.

For example, bind offline review to one directory:

| Condition | Required capability | Ordered candidates | Verification/fallback |
|---|---|---|---|
| packages/api/** | review | Verified local reviewer Skill > manual review | Find a known defect; block the review gate if neither meets it |

See [capability routing](references/en/capability-routing.md) and the [configuration contract](references/en/routing-configuration.md) for fields, adoption and limits.

## Install and invoke

The runtime Skill payload contains four items. Copy them completely into a directory named `delivery-harness`:

```text
SKILL.md       language selection and core entry
agents/        Codex interface metadata
assets/        state, overlay and native startup block templates
references/    language cores, action rules and runtime guidance
```

`README.md` and `README.en.md` are repository guide files; `.gitattributes` and `.gitignore` are versioned repository infrastructure. All four ship with the repository, outside the runtime Skill payload. Do not distribute `.git/`, development state, tests, raw logs or machine configuration as Skill contents.

| Runtime | Common user-level surface | Explicit invocation |
|---|---|---|
| Codex | `$HOME/.agents/skills/delivery-harness` | `$delivery-harness` |
| Claude Code | `$HOME/.claude/skills/delivery-harness` | `/delivery-harness` |
| Hermes Agent | `$HOME/.hermes/skills/delivery-harness` | `/delivery-harness`; CLI preload via `hermes chat --skills delivery-harness` |
| OpenClaw / other Agent Skills hosts | Runtime-declared installer or directory | Check native help |

For pre-injection, put the [AGENTS.md block](assets/en/AGENTS.block.template.md), [CLAUDE.md block](assets/en/CLAUDE.block.template.md) or [other entry block](assets/en/restricted-runtime-entry.block.template.md) in the effective native instruction surface. Preserve other user rules; replace only the matching marked block. An installed directory, implicit-invocation metadata and a complete startup contract are separate conditions.

Without pre-injection, an explicit cold invocation may read the Skill and core before its receipt, then use business tools. This is not a pre-injection pass where the receipt precedes all tools. Runtime paths, trust, precedence and removal are documented in the [runtime contracts](references/en/runtime-installation.md).

## Verification, updates and limits

Back up the full old payload and entry before updating. Compare exact file sets and per-file hashes, then run structural checks, a real explicit invocation and fresh-session validation. Verify target scope before removing retired files; copying new files alone does not establish set equality.

For each runtime claimed to pre-inject correctly, test at least 5 fresh sessions: receipt before first tool, correct loaded source and successful real task. Test cold invocation, missing capabilities and conflicting rules separately. Structural tests, existing files and exit code 0 do not prove those behaviors. Record unreachable runtimes and account/hosted surfaces as unverified separately.

On recovery, read only current state summaries and needed sources. Record new evidence receipts first. Check authority by action class for commits, global installation, outbound data, deployment and publishing. Repair and re-review independent findings; changes to a reviewed artifact invalidate its old review. Markdown rules depend on Agent adherence; deterministic blocking belongs in host permissions and actual execution entry points.

See [node contracts](references/en/execution.md), [gates](references/en/gates.md) and [Agent/template roles](references/en/agent-config.md). General Skills do not store project secrets or machine facts. Diagnostics are non-persistent by default and redacted before archival.
