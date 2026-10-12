# Capability Routing

Select by current action. Read exposed names, descriptions and sources first, without preloading Skill bodies. Skill, plugin, MCP and CLI are distinct types. Zero configuration is valid; reuse adequate capabilities. Optional provider failure may fall back; missing required capability blocks its evidence gate.

## Selection order

1. Filter task, directory, language, offline/data boundary, authority and compatibility first; preferences cannot override constraints.
2. Rank eligible candidates: current user choice > most-specific directory binding > project Resolver > user preference > profile default > newly discovered candidate. Unresolved same-level ambiguity blocks only that choice. Native instruction authority is unchanged.
3. Read only the selected provider body and verify actual invocation. Resolve duplicate names by source/version; disabled, conflicting or unverified candidates never become defaults automatically.
4. On failure, try configured candidates in order, checking constraints and verification for each. Never lower required acceptance. Across Agents/hosts, resolve tools and authentication again; another host's success is not inherited.

## Triggers and groups

| Current action | Candidate group |
|---|---|
| External specs, service boundaries/features/usage, primary sources/versions | research |
| Code/implementation/debugging | engineering |
| Tests/real evidence/review | verification |
| Documents/sheets/slides/images | documents |
| Install/deploy/publish | operations |
| Domain formats/workflows | domain |

Groups narrow candidates; they grant no authority and never load the whole group. Profiles replace neither process nor authority. At startup assess current signals only; say none when absent. Reassess on node, directory, configuration, version, failure or task-type changes. Explain only on selection change/failure or user request: `capability -> provider(type/source); basis; fallback/limits`.

## Documentation queries: Context7

Trigger: questions about external library, framework, protocol or service specs/API contracts, capability boundaries, features or usage. Platform- or host-level specifications such as Agent Skills and Hooks go to official pages directly, not through this route. Installing and configuring Context7 itself follows the [provider catalog](capability-catalog.md#context7). Within authorized network and data boundaries, invoke available Context7 first without waiting for another “use context7” request. Read project-owned specs locally first; query external facts they depend on without uploading private specifications.

Method: discover existing Context7 Skills, plugins, MCP tools or CLIs and reuse a working provider. A missing same-name SKILL.md does not mean Context7 is absent. Follow [Context7 invocation and installation](capability-catalog.md#context7) to resolve the product/library and version before querying docs. For a service category, identify concrete products first; clarify only ambiguity that materially changes the answer.

Acceptance and evidence: the query succeeds only when this invocation actually returns relevant documentation; a failed call, no matching documentation or a version mismatch counts as not passed. Record product/library ID, version scope, query date, actual invocation result and supporting official documentation links. A name match or successful installation is not an answer. Verify limits, quotas and supported scope against the relevant official pages.

Missing or failed: **missing** means no callable Context7 provider was found (Skill/plugin, MCP/connector or CLI); only then check installation options at the [official repository](https://github.com/upstash/context7). A failed invocation, no matching documentation, a version gap, or an offline/data boundary that prevents the query is **failure**: state the reason and use permitted primary sources instead, without installing; must not install silently. Both follow [gates](gates.md) for authority: new global configuration, a global CLI install or persistent MCP registration always needs its own authority, and nothing installs silently. If the user explicitly requires a successful Context7 query for acceptance, keep that evidence gate open.

## Configuration and providers

The [configuration contract](routing-configuration.md) defines profiles, directory overrides, candidate order and new Skill adoption. Reuse the overlay Resolver; move long detail to one `routing.md` only when needed. No additional executor.

| Capability | Type and installation source | Fallback |
|---|---|---|
| Ponytail | Plugin/Skill; DietrichGebert/ponytail | Manual minimal-change review |
| Caveman | Skill/plugin; JuliusBrussee/caveman | Concise communication |
| Humanizer | Skill; blader/humanizer | Manual non-Chinese editing |
| Humanizer-ZH | Skill; op7418/humanizer-zh | Manual Chinese editing |
| Context7 | Skill/plugin/MCP/CLI; upstash/context7 | Explain the gap under the query rule above, then verify official docs |
| Document parsing / book-to-skill | Tool/Skill; catalog maintainers | Key-page verification |
| codebase-memory | MCP companion Skill; DeusData/codebase-memory-mcp | rg + focused source |

Chinese prose -> humanizer-zh; non-Chinese prose -> humanizer; split mixed-language text by paragraph. Edit only fact-checked prose; preserve code, logs, evidence and quotations verbatim. Missing Chinese provider means manual editing, never silent generic Humanizer fallback.

Read only the selected [provider catalog](capability-catalog.md) section when installation or invocation detail is needed; request installation authority first: reuse only when authority covers target, action category and configuration scope together, always authorize new global configuration or persistent registration separately, and never install silently. Unknown sources stay uninstalled; never invent commands. Changed capability scope, data, persistence or cost uses a gate; configuration grants no authority.
