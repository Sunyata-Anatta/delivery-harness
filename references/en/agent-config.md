# Agent Configuration

`SKILL.md` is the single execution specification. Runtimes and projects reference it; they do not copy the workflow.

## Runtime configuration

Install the complete tree using [runtime-installation.md](runtime-installation.md). Keep one source repository and deploy complete copies. `agents/openai.yaml` must quote interface strings, include `$delivery-harness` in `default_prompt`, and declare optional tools only when the core workflow cannot operate without them.

For runtimes without automatic Agent Skills discovery, add the matching short entry block from `assets/en/` to a project instruction file the runtime actually reads.

## Single and multiple agents

A single agent owns reality audit, active node, documents, tests, evidence, and VCS. Delegate only when tasks are independent, parallel work is worthwhile, and user/project rules permit it.

The primary agent owns shared state, gates, global rules, integration, commits, pushes, and phase changes. A delegated task must specify inputs, allowed files, acceptance command, prohibitions, and required evidence. Delegated reports are not acceptance evidence; the primary agent reviews the actual diff and reruns verification.

## Project overlay

Copy the English [project overlay template](../../assets/en/project-overlay.template.md) for project facts, commands, authority, integrations, evidence gates, experience, and Resolver routes. Priority remains system/safety/user instructions, then repository rules and overlay, then general Harness rules. An overlay may tighten or specialize rules; it cannot bypass higher authority.

After updates, validate frontmatter, OpenAI metadata, links, templates, repository tests, official skill validation, and explicit discovery in a fresh runtime session.
