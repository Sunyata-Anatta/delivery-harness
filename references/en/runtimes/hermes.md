# Hermes Agent Runtime Contract

Primary source: [Hermes Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/); checked 2026-08-20.

## Installation
Copy the complete tree to `$HOME/.hermes/skills/delivery-harness`. A project may use `<project>/.agents/skills/delivery-harness`, then run `hermes skills trust` from that project. Default taps expect a multi-skill `skills/` layout and are not zero-config for this root single-skill repository.

## Discovery and invocation
Run `hermes skills list` and `hermes skills inspect delivery-harness`, then invoke `/delivery-harness`. Use the English [generic block](../../../assets/en/restricted-runtime-entry.block.template.md) only on an instruction surface Hermes reads.

## Arrival verification
Verify full hashes, list/inspect source and trust, explicit startup receipt, and two fresh-session sequence trials for auto-load. A readable but untrusted project skill is not executable installation.

## Update
Replace complete local copies or use the current Hub update flow; inspect again and ensure another external directory does not shadow the source.

## Uninstall and rollback
Remove only the exact local directory or use Hub uninstall. Restore a full copy for rollback; revoke project trust/entry only when actually configured.

## Known boundaries
Trust, discovery, and execution are separate. External directories can shadow names. Direct URL install must fetch every relative resource.
