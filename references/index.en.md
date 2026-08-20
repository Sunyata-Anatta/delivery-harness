# Delivery Harness: English Routing Index

Chinese is the source of truth for the rule text. This index lets an English session navigate without loading the Chinese body into context. Read only the file the current task needs.

## Language rule

- Chinese session: read SKILL.md directly.
- English session: read this index, then open only the referenced Chinese file for the current task. Do not load both languages for the same project.
- Decision signal is external: the session UI language or the user message language; when unsure, use the user message language.

## Task -> reference

| Task | Read |
|---|---|
| Change state, install, deploy, enter a new phase | [gates.md](gates.md) |
| Session bootstrap or a failed node | [principles.md](principles.md) |
| Diagnose, recover, retry a failed node | [debugging.md](debugging.md) |
| Install to Codex, Claude Code, OpenClaw, Hermes, another Agent Skills host | [runtime-installation.md](runtime-installation.md), then its linked runtime guide |
| Pick Ponytail, Caveman, Humanizer, Context7, document parsing, code graph | [capability-routing.md](capability-routing.md) |
| Configure agents or split tasks | [agent-config.md](agent-config.md) |
| Use connectors, CLIs, accounts, external services | [integrations.md](integrations.md) |
| Use GitHub | [github.md](github.md) |

## Non-negotiables (summary only, the Chinese files are authoritative)

1. One active node at a time. Document updates are checkpoints, not stop points.
2. Before ending a turn, write a visible stop reason from the closed list of four.
3. Commit gate: read the actual staged list, confirm the effective identity, run desensitization and generality scans.
4. State and evidence live under the project storage root `.delivery/`; look there before searching anywhere else.
5. Optional capabilities are routed, not hard dependencies; evaluate signals at node events.
