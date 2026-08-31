# Node Execution Reference

Read only the section for the active node. General stages, state transitions, and stop rules remain in `SKILL.md`.

## reality_audit: start from reality

Read repository rules, the project overlay, `.delivery/state.md`, accepted specifications and plans, relevant implementation and tests, Git state, and available runtime evidence. Distinguish designed, implemented, tested, deployed, and accepted; identify the outcome, non-goals, success evidence, constraints, risks, authority boundary, active node, and next gate. Old messages, checked roadmap boxes, and simulated results cannot independently prove current implementation.

When a screenshot, original source, human decision, or external result arrives, write a minimal evidence receipt before analysis or a design request: received time, reviewable source (or `needs-source`), scope, direct observations, limits, and open questions. The receipt freezes facts only; it neither approves a design nor authorizes a side effect.

Before a new session or active node reuses older evidence, check that its receipt contains `source_ref` or `needs-source`; backfill it first when absent. Do not use an untraceable old receipt for implementation, deployment, or an external write.

Use the [English project overlay template](../../assets/en/project-overlay.template.md) when the project needs local rules, durable lessons, or a Resolver. The overlay stores stable project facts; `state.md` stores mutable active state.

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

Register each evidence artifact's location and access route, processing, conclusion, boundary, and review date. Default slots are `.delivery/uploads/`, `artifacts/`, and `debug/`. Before calling evidence absent, state the current machine, directory, network, and authority reachability boundary.

Branch, HEAD, worktree, remote, identity, and installation inventory are checkable facts, not timeless prose. Store them only as a dated receipt with `verified_at`, the probe command or resolver, scope, and limits. A later session must re-probe before reuse; if reality changed, update active state instead of repeating the old receipt.
