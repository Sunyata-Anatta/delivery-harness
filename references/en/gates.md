# Decision, Authority, and Evidence Gates

## Continue directly

Within accepted scope, perform read-only inspection and current research; reversible local edits, tests, debugging, and documentation; ordinary implementation choices that do not change behavior or risk; approved project dependency installation; required fixes; node updates; and verified, scoped local commits.

## Stop for a material decision

Request a decision when goals, users, scope, or acceptance materially change; architecture changes persistent data, isolation, privacy, authority, interoperability, or long-term operation; a tool adds recurring cost, restrictive/unclear licensing, telemetry, cloud transfer, or lock-in; requirements conflict without a safe reversible default; or real evidence invalidates the accepted design.

## Stop for new authority

Request exact authority before global plugins/skills/hooks/trusted software/persistent machine configuration; credentials, account changes, paid service, or broader data transfer; unapproved push, PR, release, production deployment, external message, or coordination; browser session use; and destructive or hard-to-recover file, data, history, migration, or infrastructure actions. State action, target, persistence, external effect, and rollback.

Reuse approval only inside the same active node when target, action class, data class, cost, persistence, and external effect are unchanged. Ambiguous approval means not authorized.

## Stop at an evidence gate

Do not complete a phase when required samples, device/browser state, user behavior, dataset, account, service, or production-like environment is unavailable; full verification fails; only weaker acceptance would pass; or quality/privacy/security/reliability cannot be measured. Record existing evidence, missing evidence, exhausted safe work, and the exact unblock condition.

Visible stop line:

```text
Stopping here because: <waiting for user decision / waiting for result on user's machine / new authority required / multiple reasonable interpretations require clarification>
```

## Commit, publication, and redaction

Before commit, inspect worktree, staged set, full history, and effective author/committer identity. Scan private keys, tokens, passwords, cloud credentials, connection strings, auth files, cookies, personal data, machine paths, and identity-bearing output. Use invalid placeholders only. If a live secret appears, stop commit/push, do not repeat its value, rotate with authority, clean current and historical copies, and rescan all refs. History rewrite and force-push need separate authority and may not remove already public objects.

Credential-bearing diagnostic values must be redacted before entering context. Diagnostics are non-persistent by default; redact before approved archival. If a value leaked, do not repeat it; register rotation, remove residual copies, and record exposure surface and disposition.

Run a separate portability review: reject user infrastructure names, sync tools, hostnames, product/repository names, and project-only domain vocabulary. Automate generic shapes, keep named forbidden terms in the project overlay, and manually review domain language.
