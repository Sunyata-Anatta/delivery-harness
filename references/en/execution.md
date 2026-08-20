# Node Execution Reference

Read only the section for the active node. Stage order, state transitions, and stop rules remain in `SKILL.md`.

## reality_audit
Read repository rules, overlay, `.delivery/state.md`, accepted specification and plan, relevant implementation/tests, Git state, and runtime evidence. Separate designed, implemented, tested, deployed, and accepted. State goal, non-goals, evidence, constraints, risks, authority, active node, and next gate. Use the English [project overlay template](../../assets/en/project-overlay.template.md) for stable project facts; keep mutable state in `state.md`.

## requirements
Confirm outcome, roles, sensitive data, privacy/authority, input/output, scale, latency, accuracy, reliability, offline needs, representative samples, compatibility, deployment, rollback, and reversible MVP boundary. Ask one genuinely blocking question at a time; record safe non-behavior-changing assumptions and continue.

## tool_research
When tools or facts may change, inspect prior project decisions, then verify primary sources for version, platform, license, security, telemetry, maintenance, and deployment. Compare no-new-component baseline, current capability, and the strongest justified alternative. Date evidence and separate fact from inference. Research mature methods and public benchmarks before inventing classifiers, matching, scoring, similarity, or thresholds; test all candidates on the same real samples.

## solution_decision / design_and_plan
Request a decision only for material behavior, architecture, persistent data, privacy, cost, license, deployment risk, or long-term operation. Use the simplest accepted reversible detail otherwise. Record choice, reason, rejected options, assumptions, risks, rollback, and revisit condition. Each implementation node names files, RED test, target, verification, dependencies, estimate, and stop gate. A strong rule defines observable trigger, action, reproducible method, criterion, failure handling, and evidence.

## environment_and_authority
Start read-only. Record OS, runtime, dependencies, network, storage, services, credential boundary, repository shape, unrelated edits, and verification commands. Reuse existing components. Check third-party source, license, telemetry, installer, and security. Authority requests state action, target, persistence, external effect, and rollback.

## repository_integration
- Preserve unrelated edits; add only goal-required content; verify installation and rollback.
- Never commit secrets, personal data, or machine paths. Redact credential values before context; diagnostics are non-persistent by default and redacted before archival.
- Derive paths from project root/evidence slots or inject and register absolute-path deviations.
- Before commit, inspect staged files, identities, secrets, and portability; the commit message must cover the whole staged set.
- Separate deliverable and development-only paths. Judge dependencies at the delivery boundary. Keep caches rebuildable.

## tdd_nodes
Write the smallest behavior test; observe expected RED; make the minimal implementation; observe focused GREEN; refactor only under GREEN; run risk-proportionate regression and real artifacts; fix root causes without weakening tests; synchronize state and counterpart documents; commit when authorized; activate the next node.

## real_evidence
Before completion run `IDENTIFY -> RUN -> READ -> VERIFY -> THEN`; record command, exit code, test count, artifact/observation, and limitations. Unit tests do not replace required real samples, devices, browsers, datasets, accounts, services, production-like loads, or user acceptance. Register every evidence artifact's location/access, processing, conclusion, limits, and review date. Use `.delivery/uploads/`, `artifacts/`, and `debug/`; describe access boundaries before calling evidence absent.
