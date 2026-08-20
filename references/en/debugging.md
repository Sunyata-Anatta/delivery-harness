# Autonomous Debugging and Recovery

Read this when a node, command, result, or verification fails.

```text
failure -> reproduce -> classify -> diagnose safely -> recover -> retest -> continue
```

1. Repeat the original action. Preserve command, exit code, error class, and minimal context.
2. Classify: implementation, test/data, environment, execution-context isolation, network, permission/credential, tool capability, missing real evidence, or missing decision.
3. Start with non-mutating diagnostics. Identify the actual account, credential store, network, service, client, and execution context.
4. Use the smallest recovery already authorized: fix implementation, use a reliable equivalent command or authorized context, use an installed alternative client, or revert a reversible project change.
5. Repeat the original failing action, then run risk-proportionate verification. Continue only after it passes.

Sandbox, desktop, CI, container, connector, CLI, and browser contexts can have different files, networks, and credentials. A failure in one does not prove the account or service is invalid. Never bypass failure through silent login, installation, broader permissions, paid service, destructive action, or speculative mutation.

Stop only for a material decision, new authentication/authority/persistent configuration, irreversible action, unavailable required real evidence, or exhaustion of all safe authorized recovery paths. Report attempts, evidence, confirmed cause, excluded paths, sole remaining block, and exact unblock condition.
