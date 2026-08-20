# Agent Configuration

`SKILL.md` is the single execution specification. Runtimes and projects reference it; they do not copy the workflow.

## Runtime configuration

Install the complete tree using [runtime-installation.md](runtime-installation.md). Keep one source repository and deploy complete copies. `agents/openai.yaml` must quote interface strings, include `$delivery-harness` in `default_prompt`, and declare optional tools only when the core workflow cannot operate without them.

For runtimes without automatic Agent Skills discovery, add the matching short entry block from `assets/en/` to a project instruction file the runtime actually reads.

## Template responsibilities and use

These files operate at different layers and are not interchangeable. `agents/openai.yaml` ships with the installed Skill; the three `*.block.template.md` files provide project instruction blocks; the remaining templates create project-owned state and rules.

| Distributed file | Consumer | How to use it | Effect and maintenance boundary |
|---|---|---|---|
| `agents/openai.yaml` | OpenAI/Codex surfaces that support this metadata | Install it with `SKILL.md`, `assets/`, and `references/`; never paste it into project instructions | Supplies display metadata, the default invocation prompt, and implicit-invocation policy; it stores no project state and may be ignored by Claude, OpenClaw, and Hermes |
| `assets/en/AGENTS.block.template.md` | Codex or another host confirmed to read `AGENTS.md` | Open the template and copy only the marked block into the effective project `AGENTS.md`; replace the whole existing `delivery-harness:start` / `delivery-harness:end` block | Makes a new project session read the installed Skill first; it is an entry, not a Skill copy or state store |
| `assets/en/CLAUDE.block.template.md` | Claude Code | Copy only the marked block into the effective project `CLAUDE.md`; replace the whole matching block when present | Provides the same project auto-load entry for Claude; do not invent `claude.yaml` |
| `assets/en/restricted-runtime-entry.block.template.md` | OpenClaw, Hermes, or another host with a persistent project instruction surface | Replace `{{RUNTIME_INSTRUCTION_FILE}}` with a confirmed instruction filename, then copy only the marked block; omit it when no such surface exists | Supplies a minimal entry outside `AGENTS.md` / `CLAUDE.md`; an unread placeholder file is not auto-load evidence |
| `assets/en/delivery-skeleton.template.md` | The agent initializing a project | Follow it to copy the sibling `delivery-skeleton/.delivery/` directory; safely merge an existing `.delivery/` instead of copying this guide file | Creates project state, ignore rules, and three trackable empty-directory placeholders; a second run must produce no diff |
| `assets/en/harness-state.template.md` | Project `.delivery/state.md` | Use it only when state is absent; the complete skeleton normally provides it | Records the active node, session authority, passed evidence gates, and pending decisions as the single mutable source of truth |
| `assets/en/project-overlay.template.md` | Project agents and maintainers | Copy it into a real project documentation or rule path, remove irrelevant placeholders, and fill stable facts | Stores commands, persistent authority policy, gate definitions, Resolver routes, and lessons; never duplicates current session state |

Use the root `assets/` family for Chinese projects and `assets/en/` for English projects; do not mix families within one project session. Installation, explicit invocation, and project auto-load are separate evidence surfaces: an installed Skill does not prove an entry block was read, and a present block does not prove arrival order.

## Single and multiple agents

A single agent owns reality audit, active node, documents, tests, evidence, and VCS. Delegate only when tasks are independent, parallel work is worthwhile, and user/project rules permit it.

The primary agent owns shared state, gates, global rules, integration, commits, pushes, and phase changes. A delegated task must specify inputs, allowed files, acceptance command, prohibitions, and required evidence. Delegated reports are not acceptance evidence; the primary agent reviews the actual diff and reruns verification.

## Project overlay

Copy the English [project overlay template](../../assets/en/project-overlay.template.md) for project facts, commands, persistent authority policy, integrations, evidence-gate definitions, experience, and Resolver routes. Keep session authority and passed evidence gates only in `.delivery/state.md`. Priority remains system/safety/user instructions, then repository rules and overlay, then general Harness rules. An overlay may tighten or specialize rules; it cannot bypass higher authority.

After updates, validate frontmatter, OpenAI metadata, links, templates, repository tests, official skill validation, and explicit discovery in a fresh runtime session.
