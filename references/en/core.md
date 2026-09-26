# Execution Core

Keep one active node per declared scope. Simple questions need no project state. Follow the injected startup block first. An explicit cold invocation may read only the Skill and this core before emitting a receipt, then use business tools; it is not a pre-injection pass. Receipt: rules, version control, node, boundary, current capability signals. Mark unknowns pending probe, then verify read-only.

Cold invocations use this fixed block too. Fill known facts without renaming fields. Mark irrelevant probes not applicable with a reason.

```text
【Startup Receipt】
Rules: pending probe
Version control: pending probe
Node: pending probe
Boundary: pending probe
【Capability Signal Assessment】Current triggers or none, with reason.
```

At project startup read only project rules, overlay (default `.delivery/overlay.md`), unique active state (default `.delivery/state.md`), and current Git/environment facts. Re-probe old receipts before reuse. Reuse the overlay's sole pointer for existing governance; never dual-write. Use the project map (default `PROJECTMAP.md`) to locate needed material without recursively opening its links; read [initialization](project-initialization.md) only for adoption or governance changes. Record new evidence first: time, source or `needs-source`, observations and limits. Facts are not authority.

Before each action check applicable rules, scope, authority and evidence gates. At node transitions or rule/path changes run the [conformance check](execution.md#project-conformance). Reuse fully read, unchanged content; expand or reread when sources are unclear, conflicting, truncated or changed. Stop expanding once the action has enough information.

Replace the current state summary on every update; target <=80 lines. If exceeded, [archive history before writing](execution.md#state-size), never truncate necessary authority or unresolved risks.

Before each action, load the relevant rule units for its triggers:

| Event | Required reading |
|---|---|
| New node, state transition, TDD, long test, project completion | [Execution](execution.md) |
| Decision, authority, new evidence, staging/commit, deploy/publish, final review | [Gates](gates.md) |
| Professional capability selection or change | [Routing](capability-routing.md) |
| Installation, pre-injection, update or rollback | [Runtime](runtime-installation.md) |
| Failure/retry | [Debugging](debugging.md), [principles](principles.md) when needed |
| Delegation; external service; GitHub | [Agent](agent-config.md); [integrations](integrations.md); [GitHub](github.md) |

Check authority by action class; continue under existing approval. Conditional inspection does not authorize implementation. Receipts do not replace source evidence. Verify explicit authority for global changes, outbound data, payment and publishing. Redact values before context; diagnostics are non-persistent by default, redacted before archival. Tests cannot replace real evidence, old reviews cannot cover new artifacts, and failure or exhausted runway is not completion. Do not delegate without authority. After passing a gate, update state and affected documents and continue. Pause necessary work only for an actual decision, authority or evidence blocker and give its unblock condition.
