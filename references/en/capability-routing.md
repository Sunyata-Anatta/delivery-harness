# Optional Capability Routing

Delivery Harness selects Ponytail, Caveman, Humanizer, Context7, document parsing, code graph, and project-specific Skills or plugins from project signals. None is a hard dependency. When absent, explain benefit, risk, and fallback; it must not install silently. Give an installation method only for a known installation source; otherwise report the gap and use a manual fallback.

## Contents

- [Common flow](#common-flow)
- [Capability installation inventory](#capability-installation-inventory)
- [Signal evaluation events](#signal-evaluation-events)
- [Selection matrix](#selection-matrix)
- [Ponytail](#ponytail)
- [Caveman](#caveman)
- [Humanizer](#humanizer)
- [Context7](#context7)
- [Document parsing](#document-parsing)
- [Code graph](#code-graph)
- [Project-specific capability](#project-specific-capability)
- [Resolver record](#resolver-record)
- [Stop conditions](#stop-conditions)

## Common flow

Every optional capability follows one path:

```text
discover -> assess fit -> authorize -> install -> invoke -> verify -> degrade
```

1. **Discover:** inspect Skills, plugins, MCPs, CLIs, and repository rules exposed by the current runtime. Prefer zero-install capability; global installation is last. Common read-only probes: `npx --yes skills list` for standalone Skills; `Get-Command` on PowerShell or `which` on POSIX for CLI discovery.
2. **Assess fit:** at the node events below, evaluate task signal, expected benefit, data boundary, license, maintenance, and alternatives.
3. **Authorize:** reversible project configuration continues under existing authority. Global installation, Hook, MCP, persistent configuration, and account authentication need explicit approval. Modes are preauthorized set, recorded in the overlay, or per-item approval; both still require post-install registration.
4. **Install:** prefer the runtime-native installer, then standard Skill directories from [runtime-installation.md](runtime-installation.md).
5. **Invoke:** use the name the runtime actually lists. Plugin namespace and standalone Skill name may differ.
6. **Verify:** prove discovery, then run one small read-only behavior. Installation success text is not runtime evidence.
7. **Degrade:** fall back to repository tools, standard search, ordinary writing, or manual rules. An optional capability cannot stop the project.

Do not install multiple same-name copies together. Inspect precedence before installation; afterward record source, version, scope, verification, and uninstall method.

## Capability installation inventory

Probe the names actually exposed by the current Agent first. If a capability is absent, the Harness gives the installation source and runtime method below, then requests installation authority first. A tool capability is not a disguised Skill dependency: prefer zero-install use or its official installation page and never invent a `skills add` command.

| Capability | Type and installation source | Method when absent | Fallback |
|---|---|---|---|
| Ponytail | Plugin/Skill; `DietrichGebert/ponytail` | Use the runtime-native plugin installer listed below; review Hooks first | Manual minimum-scope review |
| Caveman | Skill/plugin; `JuliusBrussee/caveman` | Use the standalone Skill or plugin installer listed below | Ordinary concise communication |
| Humanizer | Skill/plugin; `blader/humanizer` | `npx skills add blader/humanizer --global`, or the listed Claude plugin route | Manual editing of non-Chinese prose |
| Humanizer-ZH | Skill; `op7418/humanizer-zh` | `npx skills add op7418/humanizer-zh --global` | Manual editing of Chinese prose; never fall back to generic Humanizer |
| Context7 | Tool capability; `upstash/context7` | Try zero-install `npx -y context7`; authorize MCP separately | Official pages and web research |
| Document parsing / book-to-skill | Tools and Skill; maintainer sources listed on this page | Read the maintainer installation page; prefer project-local scope and authorize heavy/global installs | Read key pages directly and require human checking |
| codebase-memory | MCP companion Skill; `DeusData/codebase-memory-mcp` | Use the pinned-install and configuration method below | `rg` plus targeted source reading |

## Signal evaluation events

Autonomous work must evaluate signals at observable node events, not when an executor happens to remember or a user asks. Once triggered, follow the common flow; only authority, material decision, and evidence gates require the user.

| Node event | Signal evaluated |
|---|---|
| `reality_audit` begins reading repository structure | Code graph: unfamiliar or large repository, call paths, cross-module impact |
| `tool_research` begins | Context7 and online research: primary documentation, versions, API facts |
| `reality_audit`, `tool_research`, or `real_evidence` encounters a PDF or project image | Document parsing: local extraction, send only relevant fragments to the model |
| Before external-facing documentation or README | Humanizer after factual verification |
| Before adding dependency, abstraction, file, or code | Ponytail for scale control |
| When processing a domain format or platform capability | Project-specific capability |

## Selection matrix

| Capability | Trigger signal | Do not enable when |
|---|---|---|
| Ponytail | Dependency, abstraction, file, or code growth may be excessive; user requests minimum implementation | It would weaken security, data integrity, accessibility, or an explicit requirement |
| Caveman | User requests low tokens, short progress, or high-frequency machine collaboration | Compression would make a security warning, irreversible confirmation, or complex order ambiguous |
| Humanizer | External documentation, README, or explanatory prose needs natural final wording | Code, structured data, logs, legal text, evidence, or quotations require verbatim fidelity |
| Context7 | Library/framework primary documentation, version, or API facts are needed | Use platform official docs directly for platform rules and specifications |
| Document parsing | PDF or project images would consume excessive tokens | Read small documents directly; never use a vision model for verbatim evidence text |
| Code graph | Unfamiliar/large repository, call path, cross-module impact, routes, or dead-code analysis | Small repository, one file, or literal search is sufficient |
| Project-specific capability | Existing capability cannot reliably cover domain format, platform, or acceptance | Only speculative benefit exists |

## Ponytail

Purpose: reduce unnecessary dependencies, abstractions, files, and code. It does not replace requirements, TDD, security, or real-evidence gates.

Check installation first. Official plugin source is `DietrichGebert/ponytail`. Codex example:

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Claude Code uses two commands:

```text
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

OpenClaw may use `clawhub install ponytail`. Hermes example:

```bash
hermes plugins install DietrichGebert/ponytail --enable
```

A plugin may enable Hooks. Read its manifest and Hooks before trust and runtime restart. When only instruction behavior is needed, install the standalone `ponytail` Skill and accept the missing persistent Hook behavior.

Use the name the runtime lists. Common forms:

```text
$ponytail:ponytail ultra
$ponytail ultra
/ponytail ultra
```

Verify on a small change: recommendations remove unnecessary implementation while preserving validation, security, and error handling.

## Caveman

Purpose: compress communication and token use, not implementation scope. Official source is `JuliusBrussee/caveman`.

Codex standalone Skill example:

```bash
npx skills add JuliusBrussee/caveman -a codex
```

Claude Code plugin example:

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

OpenClaw has a project-specific installer. Never run an uninspected remote script. Clone or download a fixed version, read `INSTALL.md` and the script, run `--dry-run`, then obtain global-configuration authority before its `--only openclaw` path.

Use the runtime-listed name:

```text
$caveman full
/caveman full
```

Verify that the same technical answer becomes shorter while commands, errors, evidence, and security warnings remain intact.

## Humanizer

Purpose: after factual verification, remove mechanical phrasing from README, handoff, and external explanation. The generic Humanizer source is `blader/humanizer`; the Chinese-specific Humanizer-ZH source is `op7418/humanizer-zh`.

Text-language routing is a hard rule:

```text
Chinese prose -> humanizer-zh
non-Chinese prose -> humanizer
split mixed-language text by paragraph, then route each part
```

Inspect the names discoverable by the current runtime first. When the target Skill is absent, give the source and method in the table above and request installation authority first; do not install silently. If `humanizer-zh` is unavailable or not authorized, Chinese prose must be edited manually and must not fall back to generic `humanizer`. Code, commands, structured data, logs, legal text, evidence, and quotations never enter either Humanizer.

Cross-Agent Skills CLI example:

```bash
npx skills add blader/humanizer --global
npx skills add op7418/humanizer-zh --global
```

Claude Code plugin:

```text
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

Common invocation:

```text
$humanizer:humanizer Refine README.md final prose only; preserve facts and commands.
/humanizer:humanizer Refine README.md final prose only; preserve facts and commands.
```

When no plugin namespace exists, use `$humanizer` or `/humanizer`. Verify that facts, numbers, links, commands, and scope are unchanged; revert any information loss.

## Context7

Purpose: retrieve library/framework primary documentation for version, API, and configuration facts during tool research. Official source is `upstash/context7`.

Zero-install syntax, verified 2026-08-18:

```text
npx -y context7 <library-or-org/repo> <question>
npx -y context7 search <keywords>
```

Observed boundary: syntax worked, but this execution environment received API 404, possibly proxy or API-key related. Run a small project-environment query before depending on it; on failure, degrade directly to web search and official pages.

The MCP form, `npx -y @upstash/context7-mcp`, changes persistent configuration. Consider only after repeated use and obtain separate authority.

Boundary: library coverage does not replace platform official pages for Agent Skills specifications or Hooks. Record external facts as criterion receipts with command, date, and observed result; never substitute a search summary for primary verification.

Verify by answering a known version fact and comparing it verbatim with the official release page. Fallback is direct web research and official pages.

## Document parsing

Purpose: extract PDF and project-image content locally before sending selected fragments to the model. Principle: **OCR extracts; the model interprets**. Never let a vision model rewrite verbatim evidence, quotations, commands, or logs because it may guess at unclear text.

Route by material:

```text
PDF or project image
  -> pdf-inspector classifies text / scan
     text PDF -> LiteParse to Markdown, send relevant pages/sections only
     scanned PDF -> PaddleOCR, send fragments
  project image with text -> PaddleOCR
  whole book as durable knowledge -> book-to-skill once, reuse later
  short document -> read directly
```

- Official sources: firecrawl/pdf-inspector (Rust, no OCR), run-llama/LiteParse, PaddlePaddle/PaddleOCR, and virgiliojr94/book-to-skill; checked 2026-08-18.
- Authority: pdf-inspector and LiteParse may install project-local; PaddleOCR is framework-heavy and needs global-install authority; book-to-skill follows Skill installation gates.
- Verification: compare one page before/after for token use and text completeness; test OCR against known text character by character.
- Fallback: let the model read only key pages; when verbatim text lacks OCR, require human checking, not vision inference.
- Revisit when tables, formulas, or layout are lost, or measured token savings are insignificant.

## Code graph

A code graph is structural discovery, not the project fact source. Prefer an already exposed graph MCP. Typical order:

```text
search_graph -> trace_path -> get_code_snippet -> targeted text search for gaps
```

Use `search_graph` for symbols, `trace_path` for callers/callees and impact, and `get_code_snippet` for target implementation. Rebuild a missing or stale index, then verify a known result. Use ordinary search for literals, error text, configuration, and non-code files. The `codebase-memory` Skill contains its decision matrix; read it before installing an MCP.

If the project selects `DeusData/codebase-memory-mcp`, verify current release, checksum, license, telemetry, write locations, and runtime configuration. Prefer a pinned package with SHA-256 verification. With explicit authority:

```bash
npm install -g codebase-memory-mcp
codebase-memory-mcp install
```

This installs a global program and modifies Agent MCP or rule configuration, so authority is mandatory. Restart the Agent, index the target repository, then verify with `search_graph` and `trace_path`. When graph and current source conflict, source and tests win.

## Project-specific capability

A project may add a domain Skill or plugin in its overlay. Write a capability card before installation:

```text
Name and purpose:
Trigger signal:
Source, version, and license:
Runtime and installation scope:
Data, network, telemetry, and credential boundary:
Invocation:
Verification command or sample:
Failure fallback:
Uninstall and rollback:
Revisit condition:
```

Selection rules:

1. Add nothing when existing capability is sufficient.
2. Verify installation and authority only from maintainer sources, not search summaries.
3. Try project-local, temporary, or read-only scope before global persistent installation.
4. Hook, MCP, browser login state, remote script execution, outbound data, or secret access needs separate authority.
5. After installation, run discovery and one representative task.
6. When source, verification, or benefit is insufficient, keep it uninstalled and record the fallback.

## Resolver record

Write stable routes in the project overlay, not the generic Skill:

| Condition | Selection | Verification | Fallback | Revisit condition |
|---|---|---|---|---|
| Cross-module call-path analysis | Installed code graph | Find a symbol and trace one known path | `rg` plus targeted source reading | Index stale or language unsupported |
| Final external Chinese README | humanizer-zh | Facts, commands, and links unchanged | Manual edit | Document becomes legal or audit evidence |

Record only evidence-backed reusable routing. One-off experiments stay in the node record.

## Stop conditions

Stop for a user decision or authority when:

- global software, plugin, Hook, MCP, or persistent machine configuration is required;
- the tool reads data outside the repository, uploads code, uses an account, or creates cost;
- a candidate changes security, privacy, license, or long-term maintenance;
- same-name Skill sources conflict and the effective copy is unknown;
- the only installer is an uninspectable remote script; or
- capability verification fails and continuation would weaken acceptance.
