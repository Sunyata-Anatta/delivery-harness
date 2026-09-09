# Routing Configuration Contract

Configuration is Agent-readable Markdown, not an executable parser. Without configuration use currently reachable capabilities from the routing table. Core and action gates do not depend on candidate groups or third-party Skills.

## Configuration source

Default to the project overlay Resolver. Move a long table only to the declared `.delivery/routing.md`; keep profile, constraint summary and one pointer in the overlay, never duplicate bindings. Apply durable user preferences only within native instruction authority. Native shortcuts adapt accepted configuration; they are not a second source.

`profile=auto|research|develop|review|document|operate`. Auto follows the current action; the other profiles prioritize research, engineering, verification, documents and operations respectively. Domain requires an actual domain task. Presets affect candidate order only; core gates always apply.

## Resolver fields

Keep existing condition, selection, evidence, fallback, verification and revisit fields. Extend the same row for multiple candidates; omit unused fields.

| Condition/directory | Capability and requirement | Ordered candidates (type/unique source) | Constraints | Verification and fallback | Revisit |
|---|---|---|---|---|---|
| Code review in packages/api/** | review, required | Verified local reviewer Skill > local manual review | Offline; no outbound data | Review a known defect; block review gate if neither meets it | Source/version changes |
| Other repository code queries | code-discovery, optional | Current graph MCP > rg CLI | Local source | Known symbol/call chain; invalid index falls back to rg | Index/Agent changes |

Directories are project-relative; exact/deeper bindings win. Normalize separators and compare using platform case semantics; a same-name prefix is not a child directory. Resolve cross-directory actions separately; restart at project boundaries. Candidates use actual native names and source/version; exclude `disabled`. Never load declared mutually exclusive candidates together. Requirement belongs to the capability goal, not one provider.

## Selection and changes

Apply hard constraints first, then routing-page precedence. Temporary user choices affect only the current action and never become global defaults. If a choice violates authority or acceptance, explain the conflict and continue independent safe work. Re-resolve after configuration/version changes, Agent switch, compaction recovery or action changes. Restore only current bindings and needed evidence pointers, not whole groups or history. Explain the actual source and selection basis; no successful-invocation claim without verification.

## New Skill adoption

Read name/description/source metadata -> check compatibility, data and authority -> verify a small task -> add a Resolver candidate or binding. No Harness core edit is required. Newly installed Skills never automatically replace verified defaults. Unknown source, unresolved name shadowing, missing or disabled candidates yield explicit reasons and ordered fallback. If no provider meets a required capability, its gate remains failed.

Native bundles that skip missing members do not prove required capabilities complete; verify each capability. Across Agents keep goals and constraints, but recheck reachable tools and authentication instead of sharing success assertions.

## Adoption scenarios

- Temporary task: keep session state; create no directories.
- New project: initialize minimal skeleton/overlay; empty configuration works.
- Existing governance: select one active state using the initialization contract and preserve original rules.
- Restricted runtime: use explicit invocation when injection is unavailable and record the timing boundary.
- Self-bootstrap: separate the installed governing baseline from candidate source; new sessions use new rules after candidate tests and synchronization.
- Companion task: independent goals keep distinct state pointers; link the relationship, do not merge because they share a directory.
