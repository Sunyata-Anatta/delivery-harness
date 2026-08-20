# Delivery Harness

[中文](README.md) | [English](README.en.md)

`delivery-harness` is an Agent Skill for complex software delivery. It keeps work moving within accepted authority while using project state, evidence gates, and explicit stop conditions to control stage changes.

It is not a project template, task tracker, or deployment script. It does not contain project-specific business facts, credentials, runtime logs, or development records.

English readers start with the [English routing index](references/en/index.md).

## When to use it

Use the Skill when an agent owns a multi-stage project and must keep analysis, design, implementation, debugging, validation, and handoff aligned. Typical cases include:

- continuing an existing project from live repository and runtime evidence;
- taking an accepted goal through a verifiable real-world evidence gate;
- coordinating agents, tools, external services, or runtimes without exceeding authority; and
- diagnosing, recovering, retesting, and recording a failed node instead of only reporting failure.

## Repository and runtime payload

The repo retains two repository guide files: `README.md` (Chinese) and `README.en.md` (English). They are required parts of the published repository, but agents do not need them to execute the Skill.

The runtime Skill payload consists of these four items:

```text
SKILL.md       execution contract and entry point
agents/        Codex interface metadata
assets/        project overlay, state skeleton, and auto-load block templates
references/    task-routed rules and runtime contracts
```

The repo root therefore contains two READMEs plus the four-part runtime payload; install only the four payload items into an Agent. Do not add `.git/`, project-state instances, test output, review material, transcripts, or machine-specific configuration to either surface. Do not write project-specific facts back into this general Skill.

## Project state contract

Downstream projects use `.delivery/` by default:

- `.delivery/state.md` is the single source for active state and stays in version control; it records the active node, session authority, passed evidence gates, and pending decisions.
- `.delivery/uploads/`, `artifacts/`, and `debug/` are ignored by default and are not distributed.
- Stable rules, commands, Resolver routes, and evidence-based lessons live in the project overlay created from the [English project overlay template](assets/en/project-overlay.template.md).

For first-time setup, follow [Project Initialization and Safe Merge](references/en/project-initialization.md) and copy the [complete `.delivery` skeleton](assets/en/delivery-skeleton.template.md). Its `state.md` is a project-tracked placeholder that is filled and maintained with the project; the skeleton also includes ignore rules and trackable placeholders for all three empty directories.

This Skill source repository is a public delivery surface. Its own `.delivery/` contains development tests, state, reviews, and the companion case study, so a project-specific exception keeps it local and outside published history. That exception does not change the downstream default for version-controlled `state.md`.

## Install

Copy all four items into the target runtime's skill directory named `delivery-harness`. Do not copy only `SKILL.md`, and do not leave a second `SKILL.md` inside the target.

Common user-level locations:

| Runtime | Target directory |
|---|---|
| Codex | `$HOME/.agents/skills/delivery-harness` |
| Claude Code | `$HOME/.claude/skills/delivery-harness` |
| OpenClaw | Use its Git or local-directory installation flow |
| Hermes Agent | `$HOME/.hermes/skills/delivery-harness` |

For runtime-specific discovery, updating, removal, and verification, read [Runtime installation and arrival verification](references/en/runtime-installation.md) and follow its runtime link.

## Invoke and auto-load

Installation makes a Skill discoverable; it does not make every project load it automatically.

Language control is `language=auto|zh|en`. `auto` selects once per project using explicit user choice, locked project-session language, dominant user-message language, then interface language. The selection binds replies, references, and auto-load templates; code, paths, commands, logs, and quotations do not trigger switching.

- Codex: invoke `$delivery-harness`.
- Claude Code: invoke `/delivery-harness`.
- For automatic loading in a new project session, add the complete marked block from the [AGENTS template](assets/en/AGENTS.block.template.md) or [CLAUDE template](assets/en/CLAUDE.block.template.md) to the project's effective `AGENTS.md` or `CLAUDE.md` file.
- For a restricted or other runtime, use the [generic entry template](assets/en/restricted-runtime-entry.block.template.md) only in an instruction surface that runtime actually reads.

For the exact role of `agents/openai.yaml`, the three entry blocks, the `.delivery` skeleton, the state template, and the project overlay, read [Template responsibilities and use](references/en/agent-config.md#template-responsibilities-and-use).

The same Skill name may be available from more than one location. Do not assume the runtime merges sources or selects the newest copy. Record the selected path and validate again in a new session after updating.

## Verify and update

After every installation or update:

1. Compare the source and target four-item manifests and per-file hashes.
2. Confirm that the runtime lists or explicitly invokes `delivery-harness`.
3. Open a fresh context-free session and confirm that the startup receipt appears before the first tool call.

The complete four-level evidence model plus update and rollback rules are in [Runtime installation and arrival verification](references/en/runtime-installation.md). A present file does not prove runtime loading; a listed Skill does not prove timely automatic loading.

## Boundaries

[SKILL.md](SKILL.md) is the authoritative rule entry point. Read `references/en/` progressively by task, rather than loading every reference. Use the [node execution reference](references/en/execution.md) for phase details; the entry point routes gates, diagnosis, capability selection, and integrations to their corresponding English references.

Do not write personal data, host names, tokens, private addresses, or raw diagnostic values into the general Skill or archived material. Diagnostics are non-persistent by default; redact before archival.
