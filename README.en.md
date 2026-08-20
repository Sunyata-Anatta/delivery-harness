# Delivery Harness

`delivery-harness` is an Agent Skill for complex software delivery. It keeps work moving within accepted authority while using project state, evidence gates, and explicit stop conditions to control stage changes.

It is not a project template, task tracker, or deployment script. It does not contain project-specific business facts, credentials, runtime logs, or development records.

English guide; 中文说明：[README.md](README.md). When using the Skill, English readers should start with the [English routing index](references/index.en.md).

## When to use it

Use the Skill when an agent owns a multi-stage project and must keep analysis, design, implementation, debugging, validation, and handoff aligned. Typical cases include:

- continuing an existing project from live repository and runtime evidence;
- taking an accepted goal through a verifiable real-world evidence gate;
- coordinating agents, tools, external services, or runtimes without exceeding authority; and
- diagnosing, recovering, retesting, and recording a failed node instead of only reporting failure.

## Published contents

The repository root is the installable Skill. The release contains only these four items:

```text
SKILL.md       execution contract and entry point
agents/        Codex interface metadata
assets/        project-overlay and auto-load block templates
references/    task-routed rules and runtime contracts
```

Do not ship `.git/`, project state, test output, review material, transcripts, or machine-specific configuration. Keep project facts in the project's ignored local state location, not in this general Skill.

## Install

Copy all four items into the target runtime's skill directory named `delivery-harness`. Do not copy only `SKILL.md`, and do not leave a second `SKILL.md` inside the target.

Common user-level locations:

| Runtime | Target directory |
|---|---|
| Codex | `$HOME/.agents/skills/delivery-harness` |
| Claude Code | `$HOME/.claude/skills/delivery-harness` |
| OpenClaw | Use its Git or local-directory installation flow |
| Hermes Agent | `$HOME/.hermes/skills/delivery-harness` |

For runtime-specific discovery, updating, removal, and verification, read [Runtime installation and arrival verification (Chinese)](references/runtime-installation.md) and follow its runtime link.

## Invoke and auto-load

Installation makes a Skill discoverable; it does not make every project load it automatically.

- Codex: invoke `$delivery-harness`.
- Claude Code: invoke `/delivery-harness`.
- For automatic loading in a new project session, add the complete marked block from the [AGENTS template](assets/AGENTS.block.template.md) or [CLAUDE template](assets/CLAUDE.block.template.md) to the project's effective `AGENTS.md` or `CLAUDE.md` file.
- For a restricted or other runtime, use the [generic entry template](assets/restricted-runtime-entry.block.template.md) only in an instruction surface that runtime actually reads.

The same Skill name may be available from more than one location. Do not assume the runtime merges sources or selects the newest copy. Record the selected path and validate again in a new session after updating.

## Verify and update

After every installation or update:

1. Compare the source and target four-item manifests and per-file hashes.
2. Confirm that the runtime lists or explicitly invokes `delivery-harness`.
3. Open a fresh context-free session and confirm that the startup receipt appears before the first tool call.

The complete four-level evidence model plus update and rollback rules are in [Runtime installation and arrival verification (Chinese)](references/runtime-installation.md). A present file does not prove runtime loading; a listed Skill does not prove timely automatic loading.

## Boundaries

[SKILL.md](SKILL.md) is the authoritative rule entry point. Read `references/` progressively by task, rather than loading every reference. Use the [project overlay template](assets/project-overlay.template.md) for project-local state and persistence boundaries; the entry point routes phase gates, diagnosis, capability selection, and external integrations to their corresponding references.

Do not write personal data, host names, tokens, private addresses, or raw diagnostic values into the general Skill or archived material. Diagnostics are non-persistent by default; redact before archival.
