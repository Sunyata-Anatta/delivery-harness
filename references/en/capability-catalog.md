# Provider Catalog

Read only the selected provider section. Recheck primary documentation before installation/update commands; reuse existing authority within scope.

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
