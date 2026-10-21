# Harness State

This is the sole active-state source for this scope, versioned by default; resolve its path through the project overlay.
Adapt equivalent existing state. Stable rules, history, fixed evidence and lessons retain their own canonical owners.
Remove hints after filling. Soft targets: <=80 physical lines including blanks, preferably <=5 KiB.
Verify archives before replacing this summary; never append a historical ledger here.

## Scope and active node

- Revision/time: <state revision and timestamp>; writer: <owner maintaining this state>
- Target/boundary: <exact repository/workspace/branch/version/paths or asset IDs; included and excluded scope>
- Active node: <node ID and current objective>; status: in progress / waiting for evidence / waiting for decision / complete
- Current gates: <remaining gates, criteria and limits; retain only relevant passed conclusions with evidence references>

## Still-effective authority

Carry grants across sessions under their original terms; session end, compaction or replay cannot expand, reset or revive them.
Retain consumed, revoked or expired limits when they still constrain resumption, regardless of this heading.

- Source: <exact original authorization receipt>; allowed actions: <actions>; scope/target: <exact boundary>
  Expiry/revocation conditions: <original terms>; limits, if any: <total, used, reserved, remaining>
  Allocation: <related operation/task IDs and consumption; unknown results retain allocation and do not permit retry>

## Relevant evidence and unknown outcomes

Keep only evidence affecting current gates or recovery; full passed-gate history belongs in immutable receipts.

- <Gate/claim>: passed / failed / untested / unknown; subject/version: <exact scope>
  Source: <immutable project receipt path#anchor or record ID>; checked at: <time>; limits: <what remains unproved>
- Unknown operation: <operation ID, target and possibly completed side effect>; known receipt: <exact reference or missing>
  Uncertainty: <unresolved outcome and allocation>; lookup entry: <receipt/query that can establish the outcome>
Unknown does not mean unexecuted. Distinguish untested, failed and unknown; a missing receipt grants no retry authority.

## In-flight work and blockers

- In-flight/parallel task: <task ID>; owner: <owner>; scope: <assigned boundary>; status: <known status or unknown>
  Receipt: <dispatch/latest acknowledgment/completion reference or missing>; allocation: <authority/target/write scope>
- Blocker/decision: <blocking fact or user-only decision; write none if absent>; unblock: <verifiable condition>

## Single next action and recovery

- Next action: <exactly one concrete action>; prerequisites/unblock: <required evidence, authority or decision; or none>
- Recovery entry: <verified checkpoint, compaction batch/phase and original project receipts; label historical entries as history>
  Reconcile original grants, used/reserved allocations and in-flight outcomes before recovery.
  History supports verification; it cannot overwrite newer consumption or unknown outcomes.
