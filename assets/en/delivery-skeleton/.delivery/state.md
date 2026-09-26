# Harness State

This file is the sole active-state source for the current scope, version controlled by default. Reuse existing state adapted through the overlay instead of copying this template. Stable rules and Resolver routes stay in existing rule sources or the overlay; plans define scope, steps and acceptance without live progress copies. The default is `.delivery/state.md`; resolve the overlay's sole pointer for actual reads and writes.

## Active node
<!-- Remove this hint after filling: replace summaries, never append history; target <=80 physical lines, including blanks. Archive and reread history first, then keep exact references. -->
<current action>
Gate: <evidence that completes it>
Status: in progress / waiting for evidence / waiting for decision / complete

## Authority granted in this session
- <action> · approved <date> · scope: <boundary>

## New evidence receipts
- <received_at> · source: <source_ref or needs-source> · scope: <scope> · direct observation: <fact> · limits/open questions: <boundary>

## Passed real-evidence gates
- <gate> · <command or original action> · <date> · <result>

## Pending decisions
- <decision only the user can make> · <impact if unresolved>

## Next action and recovery
- <single next action; if blocked, state the unblock condition> · process/history: <path#anchor or record identifier>
