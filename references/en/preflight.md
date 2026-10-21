# Mechanical Preflight (preflight)

This page defines the mechanical checks for delivery records and commits: record availability, records travelling with code, traceable evidence, identity consistency, and a genuine commit readback become executable, failing, and readable checks. Normative judgment remains with the [gates](../gates.md); preflight is the mechanical projection of a gate, never a substitute for review, real evidence, or user decisions. The tool is the single-file standard-library script [preflight.py](../preflight.py) shipped inside the payload; it is language-neutral and exists only once, with this page synchronized with the Chinese counterpart.

## Purpose and boundaries

- Read-only: it does not modify records, create substitute records, or write project files. The only write is the explicitly requested optional `--install-hook`.
- Nine checks with severity configurable as block or warn. Failures print repair suggestions; the executor fixes and re-runs.
- No network access. Secret scanning reports only file and type, never the matched value, and does not read sensitive sources outside the evidence slot.
- Exit codes are CI-consumable; `--json` is the stable machine interface.
- Not a substitute for independent review, real-evidence gates, human commit-object readback, a dedicated secret scanner, or historical coverage checks.

## When to run

| Event | Command | Notes |
|---|---|---|
| Before the first `git add` of this delivery | `python -B -X utf8 <skill>/references/preflight.py --root . --json` | Default mode inspects worktree and staged pending changes; block failures forbid staging |
| After `git add`, before commit | Same command plus `--staged` | Checks only the index; the commit hook runs this mode too |
| After the candidate message is final | Add `--message-file <file>` | Checks session/share links and agent trailers |
| After the commit is created | Add `--readback` | Verifies the commit diff really contains the record change, not just a staged one |
| Before completion, handoff, or release claims | Default mode or `--staged` | A failure forbids claiming completion |
| When automatic interception is wanted | `--install-hook` | Installs the in-repository commit-msg hook after explicit consent |
| CI | `--json` | Consume exit codes together with `status` and `checks` |

`<skill>` is the installed delivery-harness directory. The script lives inside `references/` and ships with the four-root runtime payload; no new top-level distribution directory is added.

## Configuration

Discovery order: read `<root>/.delivery/preflight.json` first; when absent, read the structurally identical JSON inside the `preflight` fenced block of `.delivery/overlay.md`; when neither exists, use built-in defaults and report `config_source: "defaults"`. The JSON file wins; if an overlay block is shadowed, `notes` says so. Configuration is JSON only (no second syntax). Type errors, unknown enum values, and non-compilable regular expressions are configuration errors (exit code 2).

| Key | Default | Meaning |
|---|---|---|
| `schema` | `1` | Configuration version; only 1 is accepted |
| `record.path` | `.delivery/state.md` | Sole active state or formal-record path, relative to the project root |
| `record.tracked` | `"auto"` | Whether the record is version-controlled; `auto` inspects the index and HEAD |
| `record.related_readable` | `[]` | Related record or overlay paths that only need to be readable |
| `record.mtime_tolerance_seconds` | `0` | Tolerance for modification-time comparison of untracked records |
| `code.paths` | common source paths | Globs treated as code changes; `*` stays within a directory, `**` crosses directories |
| `code.exclude` | `[]` | Globs excluded from code paths |
| `evidence.path` | record path | Evidence index file |
| `evidence.prefix` | `"E"` | Evidence number prefix |
| `evidence.allow_needs_source` | `false` | Allows link-less `needs-source` lines to degrade to a warning |
| `baseline.enabled` | `false` | Switch for check d |
| `baseline.path` / `pattern` / `ref` | none | Version file, capture regex for the version, baseline commit |
| `exemptions.path` | `.delivery/preflight-exemptions.md` | Exemptions file |
| `identity.name` / `email` / `check_committer` | none | Identity policy; when absent, check h skips with a warning |
| `limits.record_max_lines` / `record_max_line_length` | `80` / `0` | Record line and single-line character limits; 0 disables the line-length limit |
| `secrets.patterns` / `exclude` / `max_bytes` | high-signal built-ins | Secret scan; reports file and type only |
| `message.banned_links` / `banned_trailers` | built-in rules | Patterns banned from the candidate message |
| `checks.a` ... `checks.i` | `block` | Severity per check, `block` or `warn` |
| `readback.ref` | `HEAD` | Commit inspected by check i |
| `hook.python` | interpreter at install time | Python command used by the commit hook |

Standalone configuration example:

```json
{
  "schema": 1,
  "record": {
    "path": ".delivery/state.md",
    "related_readable": [".delivery/overlay.md"]
  },
  "code": {"paths": ["src/**", "**/*.py"], "exclude": ["docs/**"]},
  "evidence": {"path": ".delivery/state.md", "prefix": "E"},
  "identity": {
    "name": "Example Author",
    "email": "author@example.invalid",
    "check_committer": false
  },
  "limits": {"record_max_lines": 80, "record_max_line_length": 0},
  "checks": {"d": "warn"}
}
```

The same configuration may live as an overlay fenced block (during adoption, or when an extra file is not wanted):

```preflight
{"record": {"path": ".delivery/state.md"}, "checks": {"d": "warn"}}
```

Evidence line convention: start with an optional list marker or bracket, then the prefix plus a number, and the line must contain one Markdown link. Links resolve against the evidence index directory first and the project root second; the target must exist. Added numbers increase strictly and are greater than the largest baseline number. Example:

```text
- E12 | [batch run](artifacts/batch/run.log) | note
E13: [receipt](.delivery/artifacts/2026-10-21-preflight/README.md)
```

The exemptions file records exceptions where the record legitimately should not change in this batch; one glob and one non-empty reason per line:

```text
- src/generated/** — generated files; record updated in batch 2026-10-21-preflight
```

## Checks

| Check | Trigger and method | Criterion | Failure handling |
|---|---|---|---|
| a | Record exists, reads as UTF-8, and opens with `r+b`; every `record.related_readable` path gets a read-only probe | All pass | Block failure; never create or migrate the record automatically |
| b | When staged changes (pending worktree changes in default mode) touch code paths, the record must change in the same batch. Tracked records use strict set comparison; untracked records must not be older than the newest code change; the exemptions file may cover the gap | Same batch, or all paths exempted | Block failure listing uncovered paths; a matched exemption warns |
| c | Added or modified evidence lines relative to `HEAD`; without a baseline the whole file is checked and downgraded to warnings | Every line has a resolvable existing link; added numbers increase strictly | Block failure; reports line and number only |
| d | When evidence lines are added, the version captured by `baseline.pattern` from `baseline.path` must increase; `baseline.enabled=false` skips | Version increases numerically | Block failure; explicit skip when disabled |
| e | Record line count and single-line character count stay within `limits` | Both within limits | Block failure; 0 disables that limit |
| f | Scans staged (`--staged`) or pending file content; binary and oversized files are skipped | No match | Block failure; reports file and type only, never the value |
| g | The candidate commit message from `--message-file` | No session/share/chat link and no `Claude-*`-style trailer | Block failure; reports type and line only, never the link |
| h | `git var GIT_AUTHOR_IDENT`; the committer identity too when `check_committer` is set | Name exact, email equal case-insensitively | Block failure; when no identity policy is configured the check skips with a warning and the identity gate is not passed |
| i | `--readback` reads the diff of `readback.ref` and the record blob | When the commit changes code paths, the record path must really change in that commit diff | Block failure; an untracked record skips with the documented limit |

## Exit codes and --json

| Exit code | Meaning | Next action |
|---|---|---|
| `0` | PASS: no block-level failure; warnings and skips may exist | Continue through the gate; register each skip and never present it as a passed gate |
| `1` | FAIL: at least one block-level failure | Equal to gate failure: do not stage, commit, push, or claim completion |
| `2` | Usage or configuration error | Fix command, configuration, or Git environment and re-run; never guess a configuration to bypass |

`--json` emits one object with fixed fields: `schema`, `tool`, `tool_version`, `mode`, `root`, `config_source`, `status` (`pass`/`fail`/`error`), `summary` (blocked/warned/skipped/passed), `checks` (ordered a-i, each with `severity`, `status`, `note`, `findings`), and `notes`. `findings` contains only `level`, `type`, `message`, `path`, `line`, `fix` and never any scanned value. Usage and configuration errors also emit JSON with `status` set to `error` and exit code 2.

```json
{
  "schema": 1,
  "tool": "delivery-harness-preflight",
  "mode": "staged",
  "status": "fail",
  "summary": {"blocked": 1, "warned": 0, "skipped": 4, "passed": 4},
  "checks": [
    {
      "id": "b",
      "severity": "block",
      "status": "fail",
      "findings": [
        {"level": "block", "type": "record-not-in-batch", "path": ".delivery/state.md", "line": null, "message": "code paths changed but the record is not in the same batch", "fix": "update the record and include it in this batch"}
      ]
    }
  ]
}
```

## Relationship to the gates

- [Mechanical preflight gate](../gates.md#mechanical-preflight): run before the first `git add` and before any completion claim. Exit code 1 or 2 forbids continuing; a failed check equals the corresponding gate failing.
- The record and identity availability gate is mechanized by a and h. A skipped h means the identity policy or identity facts cannot be checked, not that the gate passed.
- [Formal-record consistency](../gates.md#formal-record-consistency) requires readback: after writing, perform the [write-back check](../gates.md#write-back-check) against actual content; preflight does not replace it.
- [Commit-object readback](../gates.md#commit-object-readback): `--readback` only proves the commit diff contains the record change; the message, author, and committer still need gate readback.
- Evidence and secret gates: c is a degraded link/number check and f is a high-signal pattern scan; dedicated scanners, real samples, and independent review remain higher evidence.
- Passing preflight never auto-passes another gate, and a failed preflight is not excused by another gate passing.

## --no-verify exception rules

1. Only for an unavailable hook environment (for example a missing interpreter or a host that disables hooks) or an emergency recovery; record the reason, scope, and substitute verification in the process record.
2. When a check failed (missing record, record not in the batch, broken evidence link, secret hit, identity mismatch, session link in the candidate message), `--no-verify` and any environment variable may not bypass it; fix it first.
3. After bypassing the hook, still run default mode and `--readback` manually before and after the commit, and register command, exit code, and result in the process record.
4. Not installing the hook is not a pass; without the hook the executor runs the same commands at the same action point.
5. Repeated or systematic bypass is a gate failure: keep the open item and unblock condition in the sole active state until the re-run passes.

## Commit hook (optional)

- Install: `python -B -X utf8 <skill>/references/preflight.py --root . --install-hook`. Only an explicit request performs it; hook installation is neither default behavior nor distribution-surface synchronization.
- Location: writes only `commit-msg` inside the repository hooks directory and respects `core.hooksPath`; refuses (exit code 2) when it resolves outside the repository.
- Protection: refuses to overwrite an existing hook without this tool's marker; a human must handle that first.
- Content: invokes the same script with `--staged --message-file "$1"`; interpreter and script paths are written at install time and live only in the local hook file, never in the repository.
- Uninstall: delete the hook file. Reinstall after moving or updating the skill directory.
- Never edits global Git configuration; synchronizing and verifying global or project installation surfaces is a release action that needs separate authority.

## Limits and degradation

- Untracked or ignored records: b uses a modification-time heuristic that only covers the same machine and batch; when i cannot read back it skips with a warning and must not be reported as a passed commit readback.
- c and d need a Git baseline for the evidence index; without one the whole file is checked with downgraded warnings, or the check skips.
- f covers only the configured high-signal patterns, not a full secret scan; binary files, oversized files, and history are outside the default scope.
- After merge, rebase, or amend, re-read the object scope under the gates; `--readback` inspects only the selected commit and its parent diffs.
- Windows paths are normalized to `/` for matching and configuration may use backslashes; the filesystem is case-insensitive.
- Preflight does not judge whether record content is true, evidence sufficient, or authority covering; the gates and humans still decide that.
