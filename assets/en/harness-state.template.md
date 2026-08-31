# Harness State

This version-controlled file is the single source for mutable project state. Keep stable rules, Resolver routes, and progress metrics in the overlay or plan.

## Active node
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
