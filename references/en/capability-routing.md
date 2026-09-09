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
| Primary sources/versions | research |
| Code/implementation/debugging | engineering |
| Tests/real evidence/review | verification |
| Documents/sheets/slides/images | documents |
| Install/deploy/publish | operations |
| Domain formats/workflows | domain |

Groups narrow candidates; they grant no authority and never load the whole group. Profiles replace neither process nor authority. At startup assess current signals only; say none when absent. Reassess on node, directory, configuration, version, failure or task-type changes. Explain only on selection change/failure or user request: `capability -> provider(type/source); basis; fallback/limits`.

## Configuration and providers

The [configuration contract](routing-configuration.md) defines profiles, directory overrides, candidate order and new Skill adoption. Reuse the overlay Resolver; move long detail to one `routing.md` only when needed. No additional executor.

| Capability | Type and installation source | Fallback |
|---|---|---|
| Ponytail | Plugin/Skill; DietrichGebert/ponytail | Manual minimal-change review |
| Caveman | Skill/plugin; JuliusBrussee/caveman | Concise communication |
| Humanizer | Skill; blader/humanizer | Manual non-Chinese editing |
| Humanizer-ZH | Skill; op7418/humanizer-zh | Manual Chinese editing |
| Context7 | MCP/CLI; upstash/context7 | Official documentation |
| Document parsing / book-to-skill | Tool/Skill; catalog maintainers | Key-page verification |
| codebase-memory | MCP companion Skill; DeusData/codebase-memory-mcp | rg + focused source |

Chinese prose -> humanizer-zh; non-Chinese prose -> humanizer; split mixed-language text by paragraph. Edit only fact-checked prose; preserve code, logs, evidence and quotations verbatim. Missing Chinese provider means manual editing, never silent generic Humanizer fallback.

Read only the selected [provider catalog](capability-catalog.md) section when installation or invocation detail is needed; request installation authority first (reuse explicit existing scope); must not install silently. Unknown sources stay uninstalled; never invent commands. Changed capability scope, data, persistence or cost uses a gate; configuration grants no authority.
