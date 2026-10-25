# Delivery Harness

[中文](README.md) | [English](README.en.md)

Current version: **2026.10.25.1**. Calendar versioning; the canonical value ships in [SKILL.md](SKILL.md). Earlier payloads declared no numeric version.

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

Harness soft text budgets use `o200k_base`: startup block <=250 tokens, SKILL + selected core <=1000, active state <=600, overlay startup summary <=450, ordinary startup total <=2300. Count host-injected skill catalogs, tools and other global rules separately. These budgets promise neither whole-conversation savings nor removal of previously loaded content. See the [budget and verification contract](references/en/runtime-installation.md).

## Project adoption

| Scenario | Approach |
|---|---|
| Temporary question or small task | Work in the session without state directories |
| New project | PROJECTMAP navigation, default sole state, overlay and resource slots; create directories for actual content |
| Existing governance | Inventory and record rule gaps; adapt sole state, writer and recovery; resume the current node after adoption passes |
| Restricted runtime | Invoke explicitly and record unavailable pre-injection |
| Self-bootstrap | Installed baseline governs candidate changes; synchronize after verification |

`.delivery/state.md` stays in version control by default. Explicit privacy deviations require recovery and verification records. `uploads/`, `artifacts/` and `debug/` are ignored by default. Follow [safe initialization](references/en/project-initialization.md), the [complete skeleton](assets/en/delivery-skeleton.template.md) and [overlay template](assets/en/project-overlay.template.md); merge existing content incrementally.

The [PROJECTMAP template](assets/en/project-map.template.md) supplies a directory skeleton and "task trigger -> entry -> section" navigation without progress or recursive link loading. Follow [resource storage](references/en/execution.md#resource-storage) for demos, images, documents, audio and video in `artifacts/<task>/tmp/` or `retained/`; copy sandbox outputs into the project and verify, and register recovery for retained items. Durable specifications, formal evidence reports and fixtures stay in project-semantic locations. Incrementally add necessary pointers to rules, overlay and README; repeat initialization must produce no new diff.

During execution, [conformance checks](references/en/execution.md#project-conformance) compare actions, scope, authority and acceptance. Expand relevant source rules at node transitions, rule/path changes or validation failures. Repair and recheck drift, then continue within authority; pause affected actions only for missing necessary decisions, authority or evidence. Reuse fully read unchanged rules instead of repeatedly loading every document.

This repository's own `.delivery/` holds legitimate development state, plans, tests and reviews, kept local under its public-distribution boundary. Companion case studies have independent goals and records, linked through findings only.

Use [document lifecycle](references/en/context-lifecycle.md) to bound downstream growth: state keeps safe-continuation essentials (<=80 physical lines, preferably <=5 KiB); process is an index of about 30 lines; evidence summaries about 50; artifact READMEs about 30. All are soft targets. Replace old summaries after preserving original batches and verifying SHA-256. History is read on demand; compaction preserves unknown outcomes, authority quotas, in-flight work and recovery. Adapt existing projects in place without another active state; no new facts means no added "no new findings" entries.

Use the new templates in `assets/` or `assets/en/` only when content exists. Repository document-contract check: `python3 -m unittest discover -s tests -v`; it checks links/anchors, bilingual resources, state copies and the four-root payload structure. It does not prove installation in an actual runtime or require downstream full application tests for document-only compaction.

## Capability groups and routing

For external library/framework/service specs, features or usage, invoke existing Context7 first under the [query rules](references/en/capability-routing.md); platform-level specifications go to official pages. Check official sources only when no provider is available; a failed call or no match is failure, so use primary sources instead of installing. Authority follows [gates](references/en/gates.md): reuse existing authority only when it covers the target, action and configuration scope together, and always authorize new global configuration, a global CLI install or persistent registration separately. Read project-owned specs locally without uploading private content.

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
assets/        state, overlay, project map and native startup block templates
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

## Hard constraints and formatting

Process rules land as [hard constraints](references/en/hard-constraints.md) H1-H6, each with a [mechanical preflight](references/en/preflight.md) check (j-o) that stops the work on failure: evidence holds only gate conclusions, changes and root causes and is counted per day; one change gets at most 2 review rounds and a third needs the owner to name it; the state file opens with "Three sentences", uses complete sentences, gives every identifier its meaning and stays within 80 lines; authorizations state what they apply to and new tasks inherit nothing; a rule without a check that is violated twice becomes a checked hard constraint; unless explicitly asked, parallel tasks use detached-HEAD worktrees on the main line instead of new branches. Rule revisions are registered under D numbers with the [decision template](assets/en/decisions.template.md), and rule tables cite only the number.

The [formatting flow](references/en/formatting.md) covers the pinned npx call, a separate formatting commit, the test-marker diff scan, the line-length guard template, regression failure triage and cross-machine tree-hash checks; `tests/test_hard_constraints.py` demonstrates every check failing on a sample repository and passing after the fix.

## Verification, updates and limits

Back up the full old payload and entry before updating. Compare exact file sets and per-file hashes, then run structural checks, a real explicit invocation and fresh-session validation. Verify target scope before removing retired files; copying new files alone does not establish set equality.

For each runtime claimed to pre-inject correctly, test at least 5 fresh sessions: receipt before first tool, correct loaded source and successful real task. Test cold invocation, missing capabilities and conflicting rules separately. Structural tests, existing files and exit code 0 do not prove those behaviors. Record unreachable runtimes and account/hosted surfaces as unverified separately.

On recovery, read only current state summaries and needed sources. Record new evidence receipts first. Check authority by action class for commits, global installation, outbound data, deployment and publishing. Repair and re-review independent findings; changes to a reviewed artifact invalidate its old review. Markdown rules depend on Agent adherence; deterministic blocking belongs in host permissions and actual execution entry points.

See [node contracts](references/en/execution.md), [gates](references/en/gates.md) and [Agent/template roles](references/en/agent-config.md). General Skills do not store project secrets or machine facts. Diagnostics are non-persistent by default and redacted before archival.
