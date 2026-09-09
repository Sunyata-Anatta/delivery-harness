# Execution Core

Keep one active node. Simple questions need no project state. Follow the injected startup block first. An explicit cold invocation may read only the Skill and this core before emitting a receipt, then use business tools; it is not a pre-injection pass. Receipt: rules, version control, node, boundary, current capability signals. Mark unknowns pending probe, then verify read-only.

Cold invocations use this fixed block too. Fill known facts without renaming fields. Mark irrelevant probes not applicable with a reason.

```text
【Startup Receipt】
Rules: pending probe
Version control: pending probe
Node: pending probe
Boundary: pending probe
【Capability Signal Assessment】Current triggers or none, with reason.
```

At project startup read only project rules, overlay (default `.delivery/overlay.md`), unique active state (default `.delivery/state.md`), and current Git/environment facts. Re-probe old receipts before reuse. An overlay may point to existing governed state as the sole source; never dual-write. See [initialization](project-initialization.md). Record new evidence first: time, source or `needs-source`, observations and limits. Facts are not authority.

Before each action, load its triggered reference:

| Event | Required reading |
|---|---|
| New node, state transition, TDD, long test, project completion | [Execution](execution.md) |
| Decision, authority, new evidence, staging/commit, deploy/publish, final review | [Gates](gates.md) |
| Professional capability selection or change | [Routing](capability-routing.md) |
| Installation, pre-injection, update or rollback | [Runtime](runtime-installation.md) |
| Failure/retry | [Debugging](debugging.md), [principles](principles.md) when needed |
| Delegation; external service; GitHub | [Agent](agent-config.md); [integrations](integrations.md); [GitHub](github.md) |

Check authority by action class; continue under existing approval. Conditional inspection does not authorize implementation. Receipts do not replace source evidence. Verify explicit authority for global changes, outbound data, payment and publishing. Redact values before context; diagnostics are non-persistent by default, redacted before archival. Tests cannot replace real evidence, old reviews cannot cover new artifacts, and failure or exhausted runway is not completion. Do not delegate without authority. After passing a gate, update state and affected documents and continue. Pause necessary work only for an actual decision, authority or evidence blocker and give its unblock condition.
