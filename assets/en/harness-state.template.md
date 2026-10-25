# Harness State

## Three sentences

- Now at: <the node name (meaning) and its goal, as one complete sentence>.
- Next: <exactly one concrete action and its precondition or unblock condition>.
- Waiting on: <the person or event this waits on; write "nobody, the agent continues" when nothing>.

## How to write it

This file is the single source of truth for the active state of the current scope; the overlay pointer resolves its path and it is tracked by default.
Write complete sentences only, with no internal shorthand, arrows or abbreviations; every identifier carries its meaning in parentheses, for example E12 (release gate conclusion).
Keep it at 80 lines or fewer; history, evidence detail and lessons each have one home, and this file replaces its summary instead of growing a ledger.
These rules are delivery-harness hard constraints; the mechanical preflight checks each one and a failure stops the work.

## Scope and active node

- Target and boundary: <exact repository, branch, version, path or target asset ID; name what is included and excluded>.
- Active node: <node name (meaning)>; status: one of in progress, waiting for evidence, waiting for a decision or done.
- Current gate: <gates still to meet, with criteria and limits; met gates that still matter keep only the conclusion and evidence reference>.
- Updated: <revision ID and time>; writer: <who maintains this state>.

## Authorizations and scope

Authorizations resume from their original wording across sessions; a new task never inherits an older one, and compaction or replay never widens, resets or revives them.
- Source: <exact receipt of the original authorization>; allowed action: <action>; scope: <exact boundary>; Applies to: <the rounds or tasks it covers>.
  Expiry: <original constraint>; quota: <total, used, reserved and remaining, or not applicable>.
  An operation with an unknown result still holds its quota and is not retryable.
- Not covered: <actions the current task may not take, for example push, release or any new task>.

## Evidence and unknown results

Register only three kinds of entry: gate conclusions, production or field changes, and failure root causes; UI, copy and style tweaks and single-page fixes live only in commit messages.
- Entry format: `E<number> [gate] <YYYY-MM-DD> <conclusion, which is the meaning of this number>; object: <exact version>; [receipt](<receipt path>)`.
- Unknown operation: <operation ID (meaning), target and side effects that may have happened; write none when there is none>.
Unknown is not the same as not executed; keep untested, failed and unknown apart, and a missing receipt grants no retry.

## Review rounds

One change gets at most two independent review rounds; before a third, stop, have the owner name it, record that here, then continue.
- <change name (meaning)>: round <N>; named by: none.

## In-flight work and blockers

- In-flight task: <task ID (meaning)>; owner: <owner>; scope: <claimed boundary>; status: <known status or unknown>.
- Blocker: <blocking fact or decision only the owner can make; write none when there is none>; unblock condition: <verifiable condition>.

## Recovery entry

- Recovery entry: <latest verified checkpoint and original receipt path; mark historical entries as history>.
Before resuming, check the original authorization, used or reserved quota and in-flight results; history is only for checking and never overrides newer use or unknown results.
