# Node Execution Reference

Read the common contract at the end first, then the active-node section; ordinary startup reads only the [core](core.md).

## reality_audit: start from reality

Read repository rules, the overlay startup summary and its resolved sole active state, and Git state. Use the project map to locate the specifications, plans, implementation, tests and runtime evidence needed by the active node, reading by section or identifier rather than treating links as a full-reading list. Distinguish designed, implemented, tested, deployed, and accepted; identify the outcome, non-goals, success evidence, constraints, risks, authority boundary, active node, and next gate. Old messages, checked roadmap boxes, and simulated results cannot independently prove current implementation.

When a screenshot, original source, human decision, or external result arrives, write a minimal evidence receipt before analysis or a design request: received time, reviewable source (or `needs-source`), scope, direct observations, limits, and open questions. The receipt freezes facts only; it neither approves a design nor authorizes a side effect.

Before a new session or active node reuses older evidence, check that its receipt contains `source_ref` or `needs-source`; backfill it first when absent. Do not use an untraceable old receipt for implementation, deployment, or an external write.

Use the [English project overlay template](../../assets/en/project-overlay.template.md) when the project needs local rules, durable lessons, or a Resolver. The overlay stores stable project facts; the sole active state stores mutable content. For first adoption or governance gaps, map and align existing work through [initialization](project-initialization.md); do not restart completed phases.

## requirements: clarify the need

Confirm the user outcome, roles, sensitive data, privacy and authority, input/output, scale, latency, accuracy, reliability, offline needs, representative samples, compatibility, deployment, rollback, and reversible MVP boundary. Ask one genuinely blocking question at a time. Record safe assumptions that do not change behavior or risk, then continue.

## tool_research: research current tools

When a library, model, service, Skill, protocol, license, or deployment option may have changed, inspect prior project decisions first, then use primary sources to verify version, platform, license, security, telemetry, maintenance, and deployment requirements. Compare at least the no-new-component baseline, current capability, and the strongest alternative justified by the need.

Date the evidence and distinguish fact from inference. Before inventing classification, matching, scoring, similarity, or threshold methods, research mature options and public benchmarks. Test existing and custom options on the same real samples. Read-only online research may continue directly; installation, payment, outbound data, and broader authority use separate gates.

## solution_decision / design_and_plan: decide and plan

Request a user decision only when an option materially changes behavior, architecture, persistent data, privacy, cost, license, deployment risk, or long-term operation. For ordinary reversible detail, choose the simplest option that satisfies acceptance.

Record the choice, reason, rejected options, assumptions, risks, rollback, and revisit condition. An implementation node names files, RED test, target, verification command, dependencies, estimate, and stop gate. A strong rule is anchored to an externally observable event and states trigger, action, reproducible method, criterion, failure handling, and evidence; escalation uses observable event counts.

List evidence recording, reversible local experiments, remote deployment, external persistent writes, and import/activation as separate action classes. When the user says “check first and report,” deliver that report first; the conditional authority does not cover implementation or side effects. A preliminary experiment states its purpose, untested acceptance conditions, rollback, and prohibited inferences; “deployed” never substitutes for implementation evidence of an approved design.

## environment_and_authority: verify environment and authority

Start with read-only checks. Record OS, runtime, dependencies, network, storage, services, credential boundary, repository shape, unrelated edits, and verification commands. Reuse existing components first. Before third-party software, inspect source, license, telemetry, installer, and security impact.

An authority request states action, target, persistence, external effect, and rollback. A preauthorized tool set removes repeated prompts only for items inside that set; it does not remove compatibility checks, post-install verification, or registration.

Local RED/GREEN evidence or a written plan never authorizes remote copying, service restart, external persistent writes, import, or activation. Check explicit authority for each such side effect; ambiguous or conditional wording is not authority.

## repository_integration: integrate surgically

- Preserve unrelated edits; add only content required by the accepted goal; verify installation and rollback.
- Do not commit secrets, personal data, or machine-specific paths. Redact credential values before context; diagnostics are non-persistent by default and redacted before archival. If a value leaked, do not repeat it; register rotation, residual cleanup, and exposure surface.
- Derive input/output directories from project root or evidence slots. Inject absolute paths as parameters and register deviations in the overlay.
- Before commit, read the actual staged file list; the commit message covers every staged file. Run secret, portability, and identity checks.
- Separate deliverable and development-only paths. Judge dependencies at the delivery boundary. Caches and indexes remain rebuildable by default.

## tdd_nodes: execute each node with TDD

For every behavior: write the smallest test; observe expected RED; implement the minimum; observe focused GREEN; refactor only under GREEN; run risk-proportionate regression and inspect the real artifact; fix the root cause without weakening tests; synchronize state and counterpart documents before commit; commit when authorized; activate the next node.

## real_evidence: verify real evidence

Before completion run `IDENTIFY -> RUN -> READ -> VERIFY -> THEN`. Record command, exit code, test count, artifact or observation, and limitations. Unit tests cannot replace required real samples, devices, browsers, datasets, accounts, external services, production-like loads, or user acceptance.

When independent review finds a Critical or Important issue, make it the active node, reproduce it, apply the smallest fix, and re-review. Do not end the turn at that finding unless a new decision, authority, or real-evidence blocker exists; then use the gates stop line and unblock condition.

Any code, runtime-configuration, or delivery-artifact change after the last independent review invalidates that review. Before deployment, release, or completion, independently review the final artifact; tests, scans, self-review, and old-version live verification do not substitute.

Register each evidence artifact's location and access route, processing, conclusion, boundary, and review date. Default slots are `.delivery/uploads/`, `artifacts/`, and `debug/`. Before calling evidence absent, state the current machine, directory, network, and authority reachability boundary.

Branch, HEAD, worktree, remote, identity, and installation inventory are checkable facts, not timeless prose. Store them only as a dated receipt with `verified_at`, the probe command or resolver, scope, and limits. A later session must re-probe before reuse; if reality changed, update active state instead of repeating the old receipt.

## Common contract: state and transitions

Default storage is `.delivery/`. `state.md` is the sole active-state source; with existing governance, resolve the overlay's unique pointer before every read or write instead of writing to the default path. Version state by default; explicit privacy deviations or an existing-governance adapter follow the initialization contract. Keep only the active node, authority, passed gates and pending decisions. Stable facts, commands, rules and Resolver belong in the project overlay, default `.delivery/overlay.md`; neither global memory nor the Skill source repository substitutes. Record private-overlay path, scope and limits in the sole state without sensitive values. `uploads/`, `artifacts/`, `debug/` are ignored temporary slots, excluded from distribution; store durable specifications, evidence and reproducible inputs by [content purpose](project-initialization.md#project-map). Use the [full skeleton](../../assets/en/delivery-skeleton.template.md) only for first adoption of the default layout; record storage-root deviations in the overlay.

Checkable facts need verification time, probe/resolver, scope and limits; re-probe before reuse. Historical receipts retain their as-of meaning. New source evidence must receive `received_at`, `source_ref` or `needs-source`, scope, observations, limits and open questions before analysis, design requests or side effects. Copy originals only when authorized. A receipt is not design approval. Before reusing evidence at a new session/node, backfill missing source references.

<a id="state-size"></a>
### State compaction: around 80 lines

`state.md` is the recovery entry for current work, not an append-only log. Target **<=80 physical lines, including headings and blanks**, while retaining the <=600-token active-summary budget. Do not pack long lines to evade limits. With existing governance, use its mapped active-summary fields rather than adding writable state.

- **Before every update**, replace summaries by topic. At transitions, move out finished nodes, resolved blockers, expired authority and evidence no longer supporting the current action. Record new evidence minimally first, then archive detail if needed. Never keep appending full command output, past test scores, conversations or specifications.
- **Retain what current work needs**: one active node and completion gate, effective authority with action/boundary/source, relevant latest evidence conclusions and exact references, unresolved risks/decisions and unblock conditions, and one next action. Stable rules/commands/Resolver stay in existing rule sources or overlay; specifications, plans and PROJECTMAP never take over live state.
- **Compact an over-budget candidate**: append history by date/topic to the existing process record or evidence report named by the overlay, retaining sources, check times and conclusion limits. Keep current summaries with `path#anchor` or record identifiers in state. Write and reread the archive before replacing state; then verify references, required fields and line count. Never split current state into `state-2.md`.
- **Preserve data on failure**: if archival is unwritable, sources cannot be traced or another writer changed the original state, retain the original and recover the recording/write conditions first. If necessary authority or risks still exceed the budget, retain them and state the reason and recovery action; never truncate or claim the size check passed. Pause dependent work only for new authority, decision or evidence obstacles.

Count lines using an available tool, for example PowerShell `@(Get-Content -LiteralPath '<sole-state-path>').Count` or Python `len(text.splitlines())`. Check after every write. Transition receipts record the count and archive location; ordinary updates do not add another stream of size logs. Eighty lines measures size, not token savings or correctness.

Stage order:

```text
reality_audit -> requirements -> tool_research -> solution_decision
  -> design_and_plan -> environment_and_authority -> repository_integration
  -> tdd_nodes -> real_evidence -> release_or_handoff
```

At every transition: run the conformance check below, then verify the current gate with fresh evidence; update the overlay-resolved sole active state, keeping one active node per declared scope; synchronize affected specification, plan, rules, lessons, Resolver, README and counterpart language before commit. Before commit append discoveries, error details, improvement purpose, options/choice and supporting data to the process record named by the overlay; explicitly record no new findings when applicable. Commit the smallest complete change when authorized and continue while in scope. Search for superseded statements after fact changes; documentation is a checkpoint, not a stop. Handoffs carry one-time context, not undated live Git or identity assertions.

Strong rules specify an externally observable trigger, action, reproducible method, success criterion, failure handling and evidence; escalation uses event counts. Before completion run `IDENTIFY -> RUN -> READ -> VERIFY -> THEN`: accepted outcome, real evidence, regression, state/docs, installation/version control, rollback and limits must match reality, with no required work unfinished.

Before a long test, independent review, or gate action, reserve enough model, tool, and time runway to read the result, update state, and start the next gate. If that runway is unavailable or uncertain, first record a resumable handoff: active finding/evidence, completed verification, frozen side effects, single resume action, and unblock condition. Exhaustion is not completion; the next session resumes the handoff and re-reviews.

<a id="project-conformance"></a>
## Project conformance check

This check runs during execution. It creates no background monitor, duplicate checklist or periodic full reread. Reuse loaded rules for ordinary actions; expand source rules and evidence at these events.

| Trigger | Action and method | Pass criterion |
|---|---|---|
| Select an action, enter a node or switch worktrees/workflows | Resolve rules and state through the overlay; use the map to locate current scope, rule clauses, authority and acceptance, then check the plan item and proposed paths | Action matches the outcome, rules and authority; the current scope has one state writer; no phase acceptance gate was bypassed |
| User corrects rules; rules/overlay/map/paths change; a reference breaks | Compare changes and source versions, fully reread affected clauses and verify each item's sole source; check links/anchors when entries change | Conflicts and broken entries are repaired; plans and actions follow effective rules without substituting old receipts for new evidence |
| Validation fails, a node transitions or completion is claimed | Check actual diffs, specific results, state and related documents against current acceptance; for document edits check links and consistency, for executable-path changes check test-name sets, skips and run results | Evidence covers the current version and rules; state is current; specifications, plans and map contain no active-state copies |

On drift, stop the affected action and gated side effects; record the deviation and single recovery action in active state. Repair and recheck within existing scope and authority, then continue; independent safe work may proceed. Ask the user under [gates](gates.md) only for a material decision, new authority or missing necessary evidence. Finding drift is not completion; alignment never authorizes code migration, branch merging or weaker acceptance.

At transitions, rule changes or detected drift, leave a minimal receipt in the existing process record: time, rule source and version/check date, action/scope, method, result, limits and recovery action. Active state retains only the current conclusion and evidence pointer. Unchanged ordinary actions need no repetitive entries. Update the map only when entries, responsibilities or reading triggers change. Agent adherence enforces these rules; deterministic blocking remains with host permissions and actual execution entry points.
