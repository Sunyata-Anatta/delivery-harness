# Decision, Authority, and Evidence Gates

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

## Reuse authorization within the same node

Do not re-ask for the same explicitly approved action class inside one active node when target, action class, data class, cost range, persistence, and external effect are unchanged.

Never extend one approval to a new data class or cost range. New or broader cost, different external recipient, changed persistence, broader authority, or a new node requires new approval. Ambiguous authority means not authorized.

## Evidence receipt, conditional authority, and side effects

Trigger: a user screenshot, original source, human decision, or external result arrives. Action: record a minimal evidence receipt in `.delivery/state.md` before analysis, design, or side effects. Method: record `received_at`, `source_ref` (or `needs-source` when it cannot be preserved), scope, direct observations, limits, and open questions; copy the original into an evidence slot only when authorized. Criterion: later claims trace to a source and distinguish fact from inference. Failure: mark `needs-source`; do not present inference as confirmed fact. Evidence: the receipt and any authorized evidence-slot reference.

Reusing older user or external evidence in a new session or active node also triggers this gate. When its old receipt lacks `source_ref` or `needs-source`, backfill it before using the evidence to support implementation, deployment, or an external write.

Keep authority classes separate: evidence recording, reversible local experiment, remote deployment or service restart, external persistent write, and import/activation/release. One class never authorizes the next. “Check first and report” or “continue after checking” authorizes only the check and report; do not implement, deploy, or write external state until the user receives the report and explicitly accepts the next action.

A preliminary experiment is not completion, even when deployed. Record its purpose, changed version, unproven acceptance conditions, rollback, and prohibited inferences. Until it satisfies the approved design, do not call it live, implementation-complete, or evidence for later import or activation.

## Stop at an evidence gate

- Required real sample, device, browser state, user behavior, dataset, account, service, or production-like environment is unavailable.
- Full verification fails.
- Only weaker acceptance can make tests pass.
- Accuracy, latency, privacy, security, or reliability cannot be measured.

Do not mark the stage complete. Record available evidence, missing evidence, exhausted safe work, and the exact unblock condition.

## Write one visible stop line

Every stopping response contains exactly one reason from this closed list:

```text
Stopping here because: <waiting for user decision / waiting for result on user's machine / new authority required / multiple reasonable interpretations require clarification>
```

If you cannot write that line, do not stop, including after announcing an action. The line is a visibility mechanism, not a gate: it turns a zero-output turn from apparently normal into an obvious missing reason. Acceptance is not “never stop early”; it is “every stop can be judged immediately.”

A user's preferred cadence constrains handoff size, not turn boundaries. Confusing them creates a stable failure mode where “I am starting now” becomes the whole handoff.

## Commit, remote publication, and redaction gate

Before commit, inspect worktree, staged set, and full Git history for private keys, tokens, passwords, cloud credentials, connection strings, authentication files, session cookies, real personal information, machine-specific paths, and output containing identity or authority data.

Commit metadata is also in scope. Author and committer identities travel with a push and cannot be found by scanning file contents alone; inspect author and committer addresses across all commits separately.

Trigger: before running `git commit`. Action: inspect the candidate commit message title, body, and trailers, not only existing history. Treat text from `-m`, `-F`, an editor, or an Agent-generated message the same way. Session, share, chat, or other opaque collaboration links must not enter commit metadata; a `Claude-Session`-style trailer must not enter commit metadata either.

Method: review the exact draft before committing, with special attention to URLs and combinations of `session`, `share`, and platform names. Keep only domain-neutral text needed to explain the change. Criterion: the candidate message contains no session/share link or trailer and remains understandable without one. Failure: abort the commit, remove the link or rewrite the reason neutrally, then recheck; when already pushed, record the historical exposure and request explicit authority for a cleanup plan. Evidence: record check time, message source, finding type, and disposition, never the link value.

Before every commit, read the effective identity instead of assuming it matches project policy. Repository config may be absent, global config may serve another purpose, and a runtime may inject environment identity. Across projects, runtimes, or machines, the effective values can change silently.

Compare the effective values with the author policy in the project overlay. `git var GIT_AUTHOR_IDENT` evaluates config and injected environment together and fails when identity is unknown. When values differ, override only that commit with `git -c user.name=... -c user.email=... commit`; never change global configuration for this purpose.

Multiple identities in the same repository history are direct evidence that this gate was not consistently executed.

Never commit a real secret as a test fixture. Use obviously invalid placeholders and avoid complete shapes that resemble usable credentials. Prefer a dedicated secret scanner. When unavailable, use repository search and Git-object inspection as a documented degraded check.

When a secret is found:

1. Stop commit and push immediately; never repeat the value in replies, logs, or a fix commit.
2. Revoke or rotate any value that may still work, then clean current files.
3. A normal follow-up commit cannot remove history. Choose history rewrite, a clean root commit, or a new repository.
4. History rewrite, deleting old remote refs, and force-push affect collaborators. Explain backup, impact, reclone requirement, and verification, then obtain explicit authority.
5. For public hosting, rewrite plus force-push may leave old objects reachable through SHA, clones, forks, and PR references. Verify current platform primary documentation; real removal may require platform intervention or repository deletion and recreation.
6. Rescan worktree, staged set, every branch, and every tag before a new commit.

Public usernames, public repository addresses, and documentation examples are not secrets. Whether to anonymize account identifiers depends on the publication boundary. Reports record file, commit, secret type, and disposition, never the value.

## Independent-review recovery gate

Trigger: independent review reports a Critical or Important finding. Action: make it the sole active node, reproduce it, apply the smallest fix, and repeat independent review; continue to block the deployment, external write, import, activation, or release protected by the failed gate. Method: record the finding, affected scope, reproduction command, fix, and re-review evidence; before a long verification or re-review, confirm execution runway, or first record a resumable handoff (active finding/evidence, completed verification, frozen side effects, single resume action, unblock condition). Criterion: the finding is reproduced and fixed, with relevant tests and re-review passing. Failure: pause only for a new decision, authority, or missing real evidence, and write the visible stop line plus the unblock condition; exhaustion is not completion. Evidence: the review report and reproduction, fix, and re-review records.

An unresolved Critical or Important finding cannot be the final activity of an active node or a completed session; the finding alone is not a reason to pause.

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
