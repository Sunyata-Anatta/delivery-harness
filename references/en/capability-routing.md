# Optional Capability Routing

Optional capabilities are routes, not dependencies. Missing capability must produce benefit/risk/fallback analysis, never silent installation.

## Common lifecycle

```text
discover -> assess fit -> authorize -> install -> invoke -> verify -> degrade
```

Discover installed skills, plugins, MCP tools, CLIs, and repository rules first. Assess trigger, benefit, data boundary, license, maintenance, and alternative at an observable node event. Reversible project configuration may proceed within authority; global installation, hooks, MCP, persistent configuration, and authentication require explicit authority. Prefer native installers and actual runtime names. Verify discovery plus a small read-only task. If unavailable, degrade to repository tools, normal search/writing, or manual rules.

Do not install duplicate names. Record source, version, scope, precedence, verification, and uninstall path.

## Trigger table

| Observable event | Evaluate |
|---|---|
| `reality_audit` starts repository discovery | code graph for unfamiliar/large repositories or call-chain impact |
| `tool_research` starts | primary/current documentation capability |
| PDF or project image appears | local extraction/OCR, then selected excerpts |
| external README or public prose is finalized | Humanizer after factual verification |
| dependency, abstraction, file, or code is about to be added | Ponytail/minimality |
| domain format or platform-specific behavior appears | project-specific capability |

## Selection matrix

| Capability | Use when | Avoid when |
|---|---|---|
| Ponytail | implementation may add unnecessary code, files, abstractions, or dependencies | it would weaken safety, integrity, accessibility, or accepted behavior |
| Caveman | user requests compressed communication or frequent machine coordination | security warnings or ordered irreversible steps would become ambiguous |
| Humanizer | final public prose sounds mechanical | code, logs, evidence, quotes, structured or legal text requires fidelity |
| Current-doc lookup | library/framework version or API may have changed | platform specifications require direct official sources |
| Document parsing | large PDF/image material would waste context | short documents or verbatim evidence can be read directly |
| Code graph | unfamiliar/large codebase, call paths, cross-module impact | literal/config/non-code search or a small file is enough |
| Project capability | present evidence shows a domain gap | benefit is speculative |

Ponytail changes implementation size; Caveman changes communication size. Neither replaces analysis, TDD, safety, or evidence. Humanizer runs only after facts, numbers, commands, links, and scope are fixed. For documents: extraction uses OCR/parser, reasoning uses the model; visually inferred text is not acceptable for verbatim evidence. For code graphs: search symbol, trace path, read snippet, then use text search for literals/config; source and tests override stale graph data.

For project-specific tools, record purpose, trigger, source/version/license, runtime/scope, data/network/telemetry/credential boundary, invocation, verification, fallback, removal, and revisit condition. Stop for global/persistent installation, external data/account/cost, material security/privacy/license change, unresolved duplicate source, uninspectable remote installer, or verification that would require weaker acceptance.
