# Decision, Authority, and Evidence Gates

Before any gate here, read and execute the [common contract](execution.md#common-contract), including the runway check before independent review or gate actions; then read the complete rule unit for the current event.

## Continue directly

Within accepted scope, Harness may:

- inspect repository, environment, dependencies, licenses, and runtime state read-only;
- query current primary sources;
- complete reversible local edits, tests, debugging, and documentation;
- choose ordinary implementation details that do not change behavior or risk;
- install approved project dependencies with clear rollback;
- fix defects required by accepted tests and gates;
- update node state and activate the next node; and
- make verified, scoped local commits.

## Stop for a material decision

Request a user choice when:

- outcome, users, scope, or acceptance materially changes;
- architecture changes persistent data, isolation, privacy, authority, interoperability, or long-term operation;
- a tool adds recurring cost, restrictive or unclear licensing, telemetry, cloud transfer, or lock-in;
- requirements conflict without a safe reversible default; or
- new real evidence invalidates the accepted design.

Present evidence, options, trade-offs, recommendation, and one explicit question.

## Stop for an authority boundary

- Installing or modifying global plugins, Skills, Hooks, trusted software, or persistent machine configuration.
- Requesting credentials, tokens, account changes, paid services, or data transfer beyond the accepted boundary.
- Unapproved remote push, PR, release, production deployment, external message, or third-party coordination.
- Switching to a user's browser login state because a connector or CLI lacks capability without prior permission.
- Destructive or hard-to-recover file, database, migration, history, or infrastructure action.

Request the smallest authority possible and state action, target, persistence, external effect, and rollback. Never bypass denied authority.

<a id="authorization-reuse"></a>
## Reuse authorization within the same node

Do not re-ask for the same explicitly approved action class inside one active node when target, action class, data class, cost range, persistence, and external effect are unchanged.

Never extend one approval to a new data class or cost range. A new data class, new or broader cost, different external recipient, changed persistence or broader authority requires new approval. At a new node, recheck existing authority; approval of the full plan remains valid for covered actions. Ambiguous authority means not authorized. Every authorization states the rounds or tasks it applies to, and a new task never inherits an older one; see [H4](hard-constraints.md#h4).

## Evidence receipt, conditional authority, and side effects

Trigger: a user screenshot, original source, human decision, or external result arrives. Action: record a minimal evidence receipt in the sole active state resolved from the overlay (default `.delivery/state.md`) before analysis, design, or side effects. Method: record `received_at`, `source_ref` (or `needs-source` when it cannot be preserved), scope, direct observations, limits, and open questions; copy the original into an evidence slot only when authorized. Criterion: later claims trace to a source and distinguish fact from inference. Failure: mark `needs-source`; do not present inference as confirmed fact. Evidence: the receipt and any authorized evidence-slot reference.

Register new evidence minimally first; evidence entries are only gate conclusions, production or field changes and failure root causes, see [H1](hard-constraints.md#h1). Once its full receipt is in the sole evidence source, state keeps only conclusions, limits and exact entries still affecting the current action, under [document lifecycle](context-lifecycle.md).

Reusing older user or external evidence in a new session or active node also triggers this gate. When its old receipt lacks `source_ref` or `needs-source`, backfill it before using the evidence to support implementation, deployment, or an external write.

Keep authority classes separate: evidence recording, reversible local experiment, remote deployment or service restart, external persistent write, and import/activation/release. One class never authorizes the next. “Check first and report” or “continue after checking” authorizes only the check and report; do not implement, deploy, or write external state until the user receives the report and explicitly accepts the next action.

A preliminary experiment is not completion, even when deployed. Record its purpose, changed version, unproven acceptance conditions, rollback, and prohibited inferences. Until it satisfies the approved design, do not call it live, implementation-complete, or evidence for later import or activation.

## Stop at an evidence gate

- Required real sample, device, browser state, user behavior, dataset, account, service, or production-like environment is unavailable.
- Full verification fails.
- Only weaker acceptance can make tests pass.
- Accuracy, latency, privacy, security, or reliability cannot be measured.

Do not mark the stage complete. Record available evidence, missing evidence, exhausted safe work, and the exact unblock condition.

<a id="stop-reason"></a>
## Write one visible stop line

Every stopping response contains exactly one reason from this closed list:

```text
Stopping here because: <waiting for user decision / waiting for result on user's machine / waiting for necessary evidence or an in-flight result / new authority required / multiple reasonable interpretations require clarification>
```

If you cannot write that line, do not stop, including after announcing an action. The line is a visibility mechanism, not a gate: it turns a zero-output turn from apparently normal into an obvious missing reason. Acceptance is not “never stop early”; it is “every stop can be judged immediately.”

A user's preferred cadence constrains handoff size, not turn boundaries. Confusing them creates a stable failure mode where “I am starting now” becomes the whole handoff.

<a id="formal-record-consistency"></a>
## Formal-record consistency and completion gate

Trigger: before a persistent change, deployment, publication or reconciliation that must maintain formal records,
and before accepting or declaring completion of that batch.
Resolve authoritative sources, scope, record meaning, writers/timing, pre/post checks and recovery from the project contract.
If unmapped, use [initialization](project-initialization.md#formal-records) to locate native mechanisms; undeclared does not mean inapplicable.

| Record meaning | Precondition | Completion criterion |
|---|---|---|
| Past facts or current-state record | Claims about the baseline needed for this action match reality, without relevant omissions, conflicts or unknown outcomes | Batch effects and required records agree; identity, outcome and authoritative readback are complete |
| Target declaration | An accepted target is bound to exact artifacts and permits moving from the baseline; baseline and target may differ now | Actual results reach the target; do not revise the target to accept unfinished work |
| Event record | Check required predecessors and in-flight status by operation ID, not the table's last row | Required events and results for this operation satisfy its protocol; acceptance, start or another operation's success is not completion |

Method: fix the subject, environment, artifacts and batch scope; use native execution, registration and readback entries.
Custom, restricted and manual paths carry the same obligations.
Check relevant record identity, content, dependencies, effective state and actual effects under the project's model,
not just the last row, maximum identifier or newest repository file.
For concurrent writers, use native locking, version conditions or a final pre-execution check; do not silently accept a drifted baseline.
Passing preconditions permits starting only; close completion only after batch effects, required records and readback satisfy postconditions.
Batch closure does not require one database transaction; handle partial or pending results in non-atomic/asynchronous protocols under project phase gates, never directly as success.

Failure: relevant omissions, conflicts or unknown outcomes keep affected writes and dependent gates closed;
state retains the current conclusion, one recovery action and the evidence entry.
“Debt retained,” exit code zero or encoding residual values as expected values does not permit continuation.
Read-only investigation, recovery within existing authority and independent safe work may continue.
Reconciliation needs both authority for that write and sufficient factual evidence; record only proven scope and read it back.
Never substitute reconciliation time for an unknown original execution time.
Use the [recovery contract](context-lifecycle.md#recovery) to inspect the original operation first;
do not blindly replay, alter executed artifacts or history to conceal discrepancies, or record success without evidence.
Reuse covered authority; ask only for a necessary decision, permission or evidence. Approval to repair does not itself resolve the discrepancy.

Evidence: use existing batch receipts for contract sources, subject/version, pre/post criteria, relevant record IDs, method, result, limits and recovery entries.
Process stores pointers; active state does not copy the ledger. Create no parallel record system or per-action full scan.
Deterministic blocking belongs in the project's actual execution entry.

<a id="write-back-check"></a>
### Write-back check

Trigger: after writing or updating the sole active state, an evidence receipt, the process record, the overlay, or any formal record used as delivery evidence; before claiming completion, handing off, or committing.

Action: immediately read back the actual content just written instead of trusting the writing command's exit code, an editor save prompt, or a remembered draft.

Criterion: the read-back matches the writing intent: fields, paths, identifiers, links, authority scope, and conclusions are present; nothing is missing, truncated, garbled, mis-encoded, or written to another path or record surface.

Failure: treat the record as unfinished: do not claim completion, do not commit, and do not continue using the unread record as evidence. After fixing, read back again until it matches; when the write target cannot be confirmed, record the exact path, symptom, and unblock condition, then stop.

Evidence: read-back time, path and location read, and the matched or mismatched conclusion; never copy sensitive values.

## Commit, remote publication, and redaction gate

### Record and identity availability gate

Trigger: before the first `git add` for a delivery change. Action: confirm that the sole active state, the project overlay, and the process record are readable, that the existing record system can save necessary receipts and update its index before commit, and that an author-identity policy is available. Method: run the smallest read/write preflight at the paths declared by the project overlay without reading evidence-slot contents, then compare `git var GIT_AUTHOR_IDENT` with the author policy. Criterion: the record is updated, the identity policy is available, and the candidate identity matches. Failure: **do not stage, commit, or push**; never infer policy from the current Git identity, old commits, or remote authors. Make a record-path failure the active diagnostic node: run one time-bounded minimal read, one equivalent read-only retry, and one write preflight that cannot overwrite original records. Never relocate records, create a substitute record surface, or call a timeout a successful record. After three safe checks still fail, preserve unstaged changes and report the exact path, operation, timeout/error, and unblock condition before stopping. Evidence: paths, preflight time, write result, identity-policy source, and comparison result; never record sensitive values.

<a id="mechanical-preflight"></a>
### Mechanical preflight gate

Trigger: before the first `git add` of this delivery change; before any completion, handoff, or release claim; on every commit once the optional commit hook is installed (`--staged --message-file`).

Action: at the project root run the [mechanical preflight](preflight.md) (`python -B -X utf8 <skill>/references/preflight.py --root . --json`; add `--staged` before commit, `--message-file` for the candidate message, and `--readback` after commit) and check record availability, record-code batching, evidence links and numbers, baseline, record size, secrets, candidate message, and identity against the project configuration, plus the [hard constraints](hard-constraints.md) H1-H6 (checks j-o).

Criterion: exit code 0 with no block-level failure. Register every warn and skip; skips such as a missing identity policy or a record outside version control do not pass their gates.

Method: run preflight before staging and repair per the printed suggestions. Preflight never edits records, and no substitute record surface may be created to pass it. The hook is optional and needs explicit consent; without it the executor runs the same commands at the same action point.

Failure: exit code 1 equals the corresponding gate failing: no `git add`, commit, push, or completion claim; repair records, evidence, message, or identity first, or record a matching exemption reason and recheck. Exit code 2 is a usage or configuration error and equally forbids continuing; never guess a configuration to bypass it.

Exception: `--no-verify` is limited to an unavailable hook environment or emergency recovery, must state the reason in the process record, and requires a manual `--readback` plus other evidence after the commit; never bypass a failed check. Repeated bypass is a gate failure.

Evidence: preflight command, exit code, `--json` summary, `config_source`, exemption basis, and readback result; never record secret values or session links.

<a id="commit-history-coverage"></a>
### Check scope and historical coverage

Before commit, inspect the current worktree, staged set, candidate message and historical coverage for private keys, tokens, passwords, cloud credentials, connection strings, authentication files, session cookies, real personal information, machine-specific paths, and output containing identity or authority data.

On first adoption or without a trusted baseline, inspect the full history required by project scope.
Bind the receipt to a verifiable object set/boundary, ref scope, rule/tool versions, results and limits.
Subsequently check all new, rewritten or introduced objects not covered by a valid baseline; reuse results only for unchanged covered objects, not periodic rescans solely because time passed.
Rule changes, wider scope, history import/rewrite or an unverifiable baseline require checking affected scope; expand to the necessary full scan when coverage boundaries cannot be proved.
Before push or publication, prove that the complete outgoing object scope is covered by current effective rules.
A baseline never replaces current worktree, staged-set or candidate-message checks.

Commit metadata is part of that coverage. File-content scans cannot inspect messages or author/committer identities; verify them separately. Checking an old HEAD does not prove full coverage.

Trigger: before `git commit` or another entry that creates/rewrites commits. Action: inspect the candidate commit message title, body, and trailers, not only existing history. Treat text from `-m`, `-F`, an editor, or an Agent-generated message the same way. Session, share, chat, or other opaque collaboration links must not enter commit metadata; a `Claude-Session`-style trailer must not enter commit metadata either.

Method: review the exact draft before committing, with special attention to URLs and combinations of `session`, `share`, and platform names. Keep only domain-neutral text needed to explain the change. Criterion: the candidate message contains no session/share link or trailer and remains understandable without one. Failure: abort the commit, remove the link or rewrite the reason neutrally, then recheck; when already pushed, record the historical exposure and request explicit authority for a cleanup plan. Evidence: record check time, message source, finding type, and disposition, never the link value.

<a id="commit-object-readback"></a>
### Commit-object readback

Trigger: after commits are created, rewritten or introduced, before relying on them to continue, hand off, push or publish.
Read messages, author/committer identities and other policy-bound metadata by actual SHA; compare with candidate content, identity policy and the delivery object.
For a normal commit check that object; for amend, rebase, cherry-pick, merge, squash or import, check every affected new object not already covered, not only the final HEAD.
Bind receipts to the object set and rule version; changed objects cannot inherit old-SHA results.
A reviewed draft or tool success message alone does not verify the final message.
On failure, pause affected follow-on actions, repair within existing authority and history-rewrite boundaries, then recheck.
Record object identifiers, finding types and disposition without copying prohibited values.

Before every commit, read the effective identity instead of assuming it matches project policy. Repository config may be absent, global config may serve another purpose, and a runtime may inject environment identity. Across projects, runtimes, or machines, the effective values can change silently.

Compare the effective values with the author policy in the project overlay. `git var GIT_AUTHOR_IDENT` evaluates config and injected environment together and fails when identity is unknown. When values differ, override only that commit with `git -c user.name=... -c user.email=... commit`; never change global configuration for this purpose.

Check identity changes against applicable policy and receipts; multiple authorized contributors do not themselves prove a missed check.

Never commit a real secret as a test fixture. Use obviously invalid placeholders and avoid complete shapes that resemble usable credentials. Prefer a dedicated secret scanner. When unavailable, use repository search and Git-object inspection as a documented degraded check.

When a secret is found:

1. Stop commit and push immediately; never repeat the value in replies, logs, or a fix commit.
2. Revoke or rotate any value that may still work, then clean current files.
3. A normal follow-up commit cannot remove history. Choose history rewrite, a clean root commit, or a new repository.
4. History rewrite, deleting old remote refs, and force-push affect collaborators. Explain backup, impact, reclone requirement, and verification, then obtain explicit authority.
5. For public hosting, rewrite plus force-push may leave old objects reachable through SHA, clones, forks, and PR references. Verify current platform primary documentation; real removal may require platform intervention or repository deletion and recreation.
6. Rescan worktree, staged set, every branch, and every tag before a new commit.

Public usernames, public repository addresses, and documentation examples are not secrets. Whether to anonymize account identifiers depends on the publication boundary. Reports record file, commit, secret type, and disposition, never the value.

<a id="review-failure-recovery"></a>
## Independent-review recovery gate

Trigger: independent review reports a Critical or Important finding. Action: make it the sole active node, reproduce it, apply the smallest fix, and repeat independent review; continue to block the deployment, external write, import, activation, or release protected by the failed gate. Method: record the finding, affected scope, reproduction command, fix, and re-review evidence; before a long verification or re-review, confirm execution runway, or first record a resumable handoff (active finding/evidence, completed verification, frozen side effects, single resume action, unblock condition). Criterion: the finding is reproduced and fixed, with relevant tests and re-review passing. Failure: pause only for a new decision, authority, or missing real evidence, and write the visible stop line plus the unblock condition; exhaustion is not completion. Evidence: the review report and reproduction, fix, and re-review records.

An unresolved Critical or Important finding cannot be the final activity of an active node or a completed session; the finding alone is not a reason to pause. One change gets at most two re-review rounds; a third needs the owner to name it, see [H2](hard-constraints.md#h2). When findings remain after two rounds, the stop line is "waiting for user decision".

## Final-review freshness gate

Trigger: code, runtime configuration, or delivery artifact changes after an independent review. Action: independently review the final artifact before deployment, release, or completion. Criterion: the reviewed object exactly matches the version to be deployed, released, or declared complete. Failure: an old review, tests, scans, self-review, or old-version live verification does not pass this gate; when an old version is already deployed, record the version divergence and do not use its live conclusion for the changed version. Evidence: the final version identifier and new independent-review record.

### Output redaction for diagnostics, probes, and status commands

Tool output enters conversation and persistent records verbatim. Before any command that may expose credentials, verify its masking strategy: values are redacted before context; key names and structure may remain. Success means no real credential value appears. Diagnostics are non-persistent by default. Before approved archival, redact, write only to an approved appropriately protected location, and register retention. A project evidence slot is not a secret vault; synchronization does not waive redaction.

If output contains a real value despite claimed masking, treat it as exposure:

1. Do not repeat the value in any response, log, or record.
2. Add the exposed key or token to the rotation list; rotation itself needs authority.
3. Remove residual copies from temporary or server files and verify removal.
4. Record exposure surfaces, disposition, and remaining risk.

### Portability review

Portability is separate from secret scanning; neither substitutes for the other. “Do not misreport as a secret” does not waive this review.

This is reuse quality, not security. A generic Skill carrying one project's world pollutes every other project. Criterion: **would a completely unrelated project find this repository inexplicably specific?**

Scope includes user infrastructure names, synchronization tools, server hostnames, product names, repository names, and project-only domain vocabulary.

Use three layers:

1. Test generic shapes automatically: private network addresses, user-directory paths, and email addresses. Put the patterns in tests, not in a published list that becomes an exposure surface.
2. Keep named forbidden terms in the project overlay because those terms are project facts, not generic content.
3. Manually read every new or rewritten lesson, example, and trigger for domain neutrality. Preserve failure mode and criterion, not the business where it occurred. Secret scanners and regular expressions cannot catch this layer.

For portability findings, do not rotate or stop all work. Rewrite to domain-neutral language or placeholders, rerun tests, and commit normally. History rewrite remains a separate authority gate. Before rewriting, find documentation that cites commit SHAs because those references will break.
