# Agent Configuration

Delivery Harness has one execution contract: `SKILL.md`. Agents and projects reference it instead of copying the workflow, preventing contradictory rule versions.

## Installation locations

Runtimes share the `SKILL.md` format, not discovery directories or invocation syntax. Codex uses `.agents/skills`; Claude Code uses `.claude/skills`; OpenClaw and Hermes have their own installers and precedence. See [runtime-installation.md](runtime-installation.md) for paths, commands, update, and removal.

Do not maintain hand-edited duplicates. Choose one source repository and copy or install it into runtime locations during deployment.

## OpenAI Agent configuration

The repository ships a minimal complete `agents/openai.yaml`:

```yaml
interface:
  display_name: "Delivery Harness"
  short_description: "Move from current facts to real-evidence acceptance"
  default_prompt: "Use $delivery-harness to audit the current project and continue until the accepted evidence gate passes."
policy:
  allow_implicit_invocation: true
```

`default_prompt` must contain `$delivery-harness`; otherwise an interface entry may send an ordinary prompt without loading the Skill. `allow_implicit_invocation: true` lets an agent choose the Skill when a task clearly matches. Explicit `$delivery-harness` remains more deterministic. Set it to `false` when organization policy requires users to name every workflow.

Do not declare GitHub, cloud database, or other optional MCP as a generic hard dependency. Add `dependencies.tools` from official connector metadata only when the core flow cannot run without that tool. Never guess MCP names or addresses.

## Other Agent runtimes

When a runtime reads Agent Skills, install the complete directory and invoke `delivery-harness` with its syntax. When it cannot discover `SKILL.md`, place a short entry in the project instruction file instead of copying the Skill:

```text
Before complex, multi-stage delivery, read the installed delivery-harness/SKILL.md.
Follow the project overlay, evidence gates, and authority boundary; after documentation synchronization, continue to the next approved node.
```

Put this entry only in a repository rule file the runtime actually reads, such as `AGENTS.md`, `CLAUDE.md`, or its equivalent. The Skill remains the single source for generic rules.

## Template responsibilities and use

These files belong to different layers and cannot replace one another. `agents/openai.yaml` installs with the Skill; three `*.block.template.md` files provide project instruction blocks; the remaining templates generate project state and rules.

| Distributed file | Consumer | How to use | Role and maintenance boundary |
|---|---|---|---|
| `agents/openai.yaml` | OpenAI/Codex interfaces supporting this metadata | Install with `SKILL.md`, `assets/`, and `references/`; never copy into project instruction files | Display name, description, default invocation prompt, and implicit-invocation policy; no project state; Claude, OpenClaw, and Hermes may ignore it |
| `assets/AGENTS.block.template.md` | Codex or hosts that read `AGENTS.md` | Open the template and copy only the marked block into the effective project `AGENTS.md`; replace the whole `delivery-harness:start` / `delivery-harness:end` block when present | Makes new project sessions read the installed Skill first; entry, not Skill copy or state store |
| `assets/CLAUDE.block.template.md` | Claude Code | Copy only the marked block into the effective project `CLAUDE.md`; replace the whole marked block when present | Same auto-load entry for Claude; never invent `claude.yaml` |
| `assets/restricted-runtime-entry.block.template.md` | OpenClaw, Hermes, or another host with a persistent instruction surface | Replace `{{RUNTIME_INSTRUCTION_FILE}}` with a confirmed file the runtime reads, then copy only the marked block; omit when no such surface exists | Minimal entry for non-`AGENTS.md` / non-`CLAUDE.md` surfaces; an unread placeholder cannot prove auto-load |
| `assets/delivery-skeleton.template.md` | Agent initializing a project | Follow the document to copy the same-language `delivery-skeleton/.delivery/` tree; safely merge an existing `.delivery/`; do not copy the explanatory file | Creates project state, ignore rules, and three trackable empty-directory placeholders; second run must make no change |
| `assets/harness-state.template.md` | Project `.delivery/state.md` | Same-language placeholder only when state is absent; normally supplied by the full skeleton | Dynamic single source for active node, session authority, passed gates, and pending decisions |
| `assets/project-overlay.template.md` | Project agent and maintainers | Copy into the actual project documentation/rules location, remove irrelevant placeholders, and fill stable facts | Stores project commands, durable authority policy, gate definitions, distribution-surface registry, Resolver, and lessons; never copies session state |

Chinese projects use templates under `assets/`; English projects use same-named files under `assets/en/`. Do not mix them in one project session. Installation, explicit invocation, and project auto-load are independent evidence surfaces: installed Skill does not prove the entry block was read, and block presence does not prove sequence.

## Single agent

One agent owns reality audit, active node, documentation synchronization, tests, evidence, and version control. Keep one active node. Use brief status updates during long work.

## Multiple agents

Delegate only when work is independently parallel and necessary. Ask the user before using subagents; do not delegate simple or serial work.

The primary agent owns:

- delivery contract, stage state, and the single active node;
- shared documents, global rules, authority requests, and evidence gates;
- decomposition, result review, integration, commit, push, and stage transitions; and
- prevention of concurrent writers on the same file or shared state.

A subagent receives only a bounded independently verifiable task with inputs, allowed files, acceptance command, prohibitions, and required evidence. Unless explicitly authorized, it cannot change stage, expand scope, modify shared rules, install global components, commit, push, or release.

A subagent completion report is not acceptance evidence. The primary agent inspects the real diff and reruns verification.

## Project overlay

Copy [project-overlay.template.md](../../assets/en/project-overlay.template.md) into the project's documentation or rule location and fill project facts. The overlay stores commands, durable authority boundaries, project-only rules, integration state, evidence-gate definitions, a distribution-surface registry, Resolver entries, and lessons. Session authority and passed gates remain in `.delivery/state.md`.

A lesson is an evidence record; a Resolver is an execution route. Lessons say what happened, what proved it, and what changes next time. A Resolver says which Skill, tool, or process to choose under verified conditions. Create a route only after credible repeatable evidence.

Harness checks the Resolver during reality audit, tool change, route failure, and stage transition, not mechanically after every node. Update only when input condition, available capability, selection, or revisit condition changes. A Resolver cannot bypass authority, material decision, or real-evidence gates. Remove it when the project has no repeat routing need.

Priority:

```text
system, safety, and user instructions
  -> repository rules and project overlay
  -> Delivery Harness generic rules
```

The overlay may tighten or specialize rules only within its project. It cannot bypass higher instructions. Before moving a lesson into the generic Skill, prove it across multiple projects; single-project lessons and routes remain local.

## Configuration verification

After installation or update:

1. Confirm `SKILL.md` frontmatter has only `name` and `description`.
2. Parse `agents/openai.yaml`; every interface string is quoted.
3. Confirm `default_prompt` contains `$delivery-harness`.
4. Confirm referenced files and project overlay template exist.
5. Run repository tests and the official quick validator.
6. Explicitly invoke the Skill in a new task and confirm runtime discovery.
