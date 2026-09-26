# Project Initialization and Safe Merge

Read this for first adoption or governance/navigation repair, not as mandatory full startup reading. The outcome is correct continuation under current rules, idempotent and lossless: copy a new layout as a unit, but never replace the directory wholesale when it already exists. A user-supplied specification informs alignment; its templates and commands do not automatically authorize execution.

## Lightweight and existing governance adoption

Temporary questions create no directories. Inspect existing rules and state first; preserve original governance. The overlay may declare one active-state path, mappings for node/authority/evidence/decisions, writer and authority, verification and recovery. Adoption passes only when these fields can be verified for reading and writing. Do not maintain a second state in `.delivery/state.md`; a compatibility entry is a pointer only. Preserve history before migration and read it on demand. Companion tasks remain independent.

Default skeleton and Git criteria below apply only to projects using that layout. For an external-state adapter, validate declared fields, writes and recovery; do not require a second `.delivery/` or tracking private material. Use a decision gate only when changing existing governance exceeds authority. Adoption remains incomplete if controlled actions cannot keep the sole state current.

With multiple worktrees, locate the current checkout through Git rather than assuming the root is mainline. Independent workflows exist only when declared by the project: the overlay identifies each scope, sole state, writer and mainline handoff. Keep one active node per scope; merging must not overwrite mainline state with branch state. Historical facts retain check dates and source refs/commits; do not renumber existing facts or extend old authority to new actions.

## Select the delivery surface

- English projects use the [English skeleton](../../assets/en/delivery-skeleton.template.md), [state template](../../assets/en/harness-state.template.md), [overlay](../../assets/en/project-overlay.template.md), [project map](../../assets/en/project-map.template.md), and matching auto-load block under `assets/en/`.
- Chinese projects use the Chinese surface and its [Chinese initialization reference](../project-initialization.md).
- The project-locked language binds all project placeholders and entry blocks.

<a id="project-map"></a>
## Project map and content ownership

Full default adoption uses README, the instruction file actually read by the host, and `PROJECTMAP.md` as root entries. `.delivery/` holds overlay, sole state, process record and temporary slots. Reuse equivalent existing files and map them in the overlay instead of recreating the diagram. README links to the map; the map holds only the skeleton and "trigger + one entry + section/identifier range", never progress, SHA, test results or authority copies.

| Content responsibility | Default location and creation condition |
|---|---|
| Current node, authority, evidence gates, pending decisions | The overlay-resolved sole active state; never duplicate in map, specification or plan |
| Stable facts, rules, decisions | Existing baseline/rule registry; use `docs/baseline.md` when needed; process logs do not automatically become rules |
| Phase scope and acceptance gates | Existing roadmap or `docs/roadmaps/` for distinct phases; implementation completion is not phase acceptance |
| Research, requirements, design and execution steps | Existing specification/plan locations, or `docs/specs/` and `docs/plans/` when content exists; create `docs/contracts/` or `docs/adr/` only for reusable contracts/decisions |
| Durable validation findings and evidence | Existing evidence index/reports, or `docs/evidence.md` and `docs/evidence/` when results exist; sensitive originals stay in approved restricted storage, with safe index references only |
| Runtime code, deployment and reproducible inputs | Keep component, `ops/`, `deploy/`, test/fixture conventions; create deployment/recovery guidance when actual steps exist |
| Attempts, errors and handoff history | Existing append-only process record, default `.delivery/process.md`; read by date/topic, not in full at startup |
| Short-term inputs, one-off outputs, temporary diagnostics | `.delivery/uploads/`, `artifacts/`, `debug/`; not storage for durable specifications, test inputs or secrets |

File by purpose rather than extension, Skill or branch name. Create directories only for actual content and responsibilities; no phase-by-purpose matrix or copied source trees named after branches. Tidying directories is not an adoption prerequisite. For necessary moves, separately map old to new paths and impacts on callers/test discovery, fixture identity, packaging, deployment and recovery; execute only with covered authority. Never renumber or rewrite applied database migrations.

## On-demand reading

Always applicable: user/host/project rules and the Harness startup contract; overlay startup summary, hard constraints and unique pointers; active node, action-specific authority/evidence gates/pending decisions; and applicable safety, data and acceptance clauses. Read full relevant definitions for first adaptation or unclear mappings; summaries do not replace required source material.

| Current event | Reading entry and expansion condition |
|---|---|
| Adoption or governance repair | This reference, relevant templates and existing adapter definitions; expand inventory for conflicts, path-type or authority problems |
| Continue work or design | Current scope, specification/plan item and dependency contracts pointed to by state; trace further for phase changes, conflicts or missing dependencies |
| Code or repair | Current plan item, related implementation/callers and tests; expand for cross-module root causes, insufficient graph results or validation failure |
| Verify evidence | Current acceptance, specific results and necessary originals; expand for version mismatch, conflict or missing samples |
| Deploy, publish or write data | Specific authority, final version, deploy/rollback and evidence gates; new side effects or missing recovery conditions enter the relevant gate |
| Trace history | Index-selected date, identifier or passage; expand for broken sources, conflicts or an explicit full-audit request |

Locate first, then fully read relevant passages and necessary references; never recursively open every map link. Reuse fully read unchanged content; reread changed sources/versions, truncated or garbled output. Stop expansion when the action has enough information. No hard word limit may block safety review, call-chain tracing or complete validation. Use a code graph only when available and data access/transmission is authorized; otherwise search locally.

## Align an existing project

After the preflight below, add an adoption receipt to the existing process record: `item -> existing source -> Harness requirement -> gap/reason to preserve -> repair or adaptation -> verification evidence`. This is a dated adoption result, not another task-state file. Cover rule priority, state fields/writer, authority classes, phase acceptance, storage/privacy, reading entries and continuation node. Reuse what satisfies the contract; minimally repair gaps. When repeat adoption finds no material change and the old receipt remains valid, reuse it; do not add timestamps, duplicate receipts or state writes merely for rechecking.

Order: inventory/preflight -> resolve sole sources -> incremental merge -> populate navigation -> verify storage and reading scenarios -> repeat for idempotence -> record adoption result -> continue from the verified current node. Verify state writes with the actual adoption receipt or a system-supported non-mutating check, never by overwriting the active node as a probe. Read access without lawful update or recovery does not complete adoption.

Preserve valid past phases and original safety rules; do not restart the lifecycle for adoption. Resolve conflicts under host instruction priority; ask only when the outcome, governance responsibility or required authority changes. After acceptance, use the [project conformance check](execution.md#project-conformance) for ongoing actions, transitions and changes.

Check active-summary size during first adoption too. Above roughly 80 lines, follow [state compaction](execution.md#state-size): archive and verify history before retaining the current summary. Adoption must neither delete history nor add writable state.

## Preflight

1. Confirm project root, repository rules, Git/worktrees, existing edits and overlay storage deviations. If Git is absent, record it; do not initialize or commit automatically.
2. Inspect only path existence, type, and names under `.delivery/`; do not read or transmit slot contents.
3. If `.delivery` is a symbolic link or reparse point, do not follow it for writes. Record the resolved target and enter the authority or project-decision gate.
4. If `.delivery`, `uploads`, `artifacts`, or `debug` has the same name but is not a directory, stop that path. Do not rename, delete, or replace the existing object.
5. Inspect every write target and its ancestors, including rules, map, overlay and external state, for type, permission and link/reparse targets. If the authorized boundary cannot be proved, stop that path without forced deletion or out-of-scope writes; independent document preparation may continue.

## Merge matrix

| Observation | Action |
|---|---|
| `.delivery/` is absent | Copy the complete English skeleton. |
| `.delivery/` exists | Preserve the directory and every existing item; never replace the directory wholesale. |
| `state.md` is absent | Copy the English state placeholder. |
| `state.md` exists | Preserve the original text. Append a missing heading only when its meaning is unambiguous; route conflicting facts to a decision gate. |
| `.gitignore` is absent | Copy the skeleton rules. |
| `.gitignore` exists | Merge is additive only: preserve order and existing rules, append missing slot rules, and add no duplicate line. |
| A slot is absent | Create the directory and its `.gitkeep`. |
| A slot is a directory | Preserve all contents; add only a missing `.gitkeep`. |
| An expected directory path is another object | Stop that path and report its type and required decision. |

Resolve the sole state before applying the matrix. With an external-state adapter, skip default `state.md` creation and do not copy the full skeleton containing it.

An explicit project deviation controls slot layout or tracking. Explicit approval of local-private state requires a recovery location, unique writer and verification method; do not claim that state is version controlled.

## Parent ignore rules

The nested `.delivery/.gitignore` works only when an ancestor does not ignore the whole directory. Before initialization run:

```text
git check-ignore -v .delivery/state.md
```

No output with exit code 1 means the untracked state file can enter Git. For an existing path, use `git check-ignore -v --no-index .delivery/state.md`. If a parent `.delivery/` rule matches, locate its controlling file from the output. When the project has no explicit deviation, append the narrow unignore block below to the version-controlled project ignore surface after the broad rule:

```gitignore
!.delivery/
!.delivery/.gitignore
!.delivery/state.md
!.delivery/uploads/
!.delivery/uploads/.gitkeep
!.delivery/artifacts/
!.delivery/artifacts/.gitkeep
!.delivery/debug/
!.delivery/debug/.gitkeep
```

Then run `git check-ignore -v --no-index .delivery/uploads/__delivery_probe__`, `git check-ignore -v --no-index .delivery/artifacts/__delivery_probe__`, and `git check-ignore -v --no-index .delivery/debug/__delivery_probe__`. Each ordinary slot probe must still match the nested skeleton rules; no probe file needs to be created.

Verify README, map, rules, overlay and process record against their declared tracking/privacy policy. Add the narrowest unignore rules for newly versioned paths as needed; do not unignore all governance content. Without Git, mark this section not applicable and record storage/recovery instead. Ignore rules are not access control for sensitive data.

## Related project files

Copy the English overlay into a project-declared documentation or rule path. If none is declared, use `.delivery/overlay.md`; do not ask the user merely to choose a path. The overlay belongs in the governed project, never global memory or the Skill source repository. When project privacy rules require it to be ignored, record only its path, scope and limits in the resolved sole state, never sensitive values. Remove unused placeholders and fill stable facts. A copied overlay has no dependency on relative links inside the installed Skill. Append the matching marked `AGENTS.md`, `CLAUDE.md`, or restricted-runtime block to an instruction file the runtime actually reads; replace an existing marked block as a unit.

Merge existing overlay fields individually. Define the state pointer once and reference that field from summaries; never leave competing default and adapted values. Register navigation, rule-clause entries and process-record reading method; long specifications remain pointers. Fill the selected-language map template with existing components and task entries only. Paths are relative to the map file, at project root by default; cross-worktree material first points to a local worktree guide, never dangling links. Aim for one or two screens; move detail out rather than generating full file lists or meaningless length tests.

Map variables: `PROJECT_NAME` names the project; `PROJECT_MAP_PATH`, `RULES_PATH`, `OVERLAY_PATH`, `ACTIVE_STATE_PATH` are verified paths, and `GOVERNANCE_ROOT` is the existing governance root. Fill `EXISTING_COMPONENT_ROWS` and `TASK_ROUTE_ROWS` only with existing entries needing navigation; remove unused rows/directories and empty variables. Preserve the structure and relative-path base of an existing map.

Merge the block below into the project's actual host-read instruction file, replacing its placeholder with the verified path. Replace only an existing same-name block, retaining Harness startup markers and all other rules. Add one map entry to README, without copying state.

```markdown
<!-- project-navigation:start -->
Follow Harness startup and project rules. Use {{PROJECT_MAP_PATH}} only to select entries, never recursively load links; resolve sole state through the project overlay. Read current node, action-specific authority/evidence gates, pending decisions and applicable rules, then full necessary passages by heading/identifier. Expand or reread unclear, conflicting, truncated or changed sources. Check rules before actions; at node transitions or rule/path changes run Harness project conformance checks. Repair and recheck drift within authority; pause affected actions only for missing decisions, authority or evidence. Map and plans hold no active state; verify links when entries change. Context savings never bypass safety, authority or real-evidence gates.
<!-- project-navigation:end -->
```

## Completion evidence

1. Default layout has `.delivery/state.md`, `.delivery/.gitignore` and all three `.gitkeep` files; validate adapted layouts against their declarations. Preserve prior files, edits and slot contents; no out-of-scope writes, outbound data or secret output.
2. The current scope has one writable state source with checkable fields, writer and recovery. The alignment receipt covers gaps and their resolution; unresolved governance gaps cannot pass adoption.
3. README, rules, overlay and map entries work without conflicting full-reading requirements; no unresolved template variables, broken links/anchors or copied state/SHA/results/authority. Necessary safety clauses are reachable and actually read.
4. `git diff -- .delivery`, `git status --short -- .delivery` and all changed entry paths are explainable. Verify state tracking/privacy deviations and slot ignores; without Git, record not applicable and recovery method.
5. Walk through "continue work, change code, verify evidence", locating and reading necessary rules and evidence without opening unrelated history; repair missing entries first.
6. Repeat the same procedure. The second run produces no new diff, duplicate marker or overwritten original. Record inspected files/versions, methods, results and limits.
7. When commit is authorized, inspect the actual staged set and include only approved navigation/rules, state, ignore rules and placeholders. Handle real slot contents under project policy and the sensitive-data gate. Technical adoption is not business acceptance, effective installation or production completion.
