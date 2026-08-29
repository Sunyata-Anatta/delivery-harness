# Autonomous Debugging and Recovery

Read this file when a node, command, result, or verification fails. The goal is to recover within existing authority and reduce unnecessary user intervention.

## Fixed flow

```text
failure -> reproduce -> classify -> diagnose safely -> recover -> reverify -> continue
```

1. Reproduce the original action. Preserve command, exit code, error class, and the minimum relevant context. Do not infer root cause from one failure.
2. Classify it as implementation defect, test/data error, environment difference, execution-context isolation, network, authority or credential issue, tool capability gap, missing real evidence, or missing user decision.
3. Diagnose without changing state first. Read machine, project, runtime, and client facts; confirm which account, credential store, network, service, or tool is actually in use.
4. Within existing authority, choose the smallest recovery: fix implementation, rerun the reliable command, use an equivalent authorized execution context, use an installed alternative client, or roll back a reversible project-level change.
5. After recovery, repeat the original failed action and run risk-proportionate full verification. Return to the original node only after reverification passes.

## Execution-context isolation

Sandbox, desktop session, CI, container, CLI, connector, and browser may have different network, filesystem, credential stores, and login state. A 401, missing credential, or inaccessible resource in one context does not independently prove the account, token, or service is invalid.

When a failure concerns authentication, network, or tool visibility:

1. Record the failed context and exact error.
2. Without browser login state, software installation, or persistent configuration changes, inspect an equivalent authorized context.
3. Compare account, authority, target resource, and command result.
4. Declare a real authentication, authority, or service block only after every allowed context fails.

Do not hand a safely diagnosable or recoverable problem to the user early. Do not bypass failure through silent login, installation, broader authority, paid service, destructive action, or speculative change.

## Stop conditions

Pause and report only when:

- outcome, scope, architecture, or acceptance needs a material decision;
- recovery needs new login, credential, authority, persistent configuration, paid service, browser session, or external coordination;
- recovery is irreversible for files, data, history, infrastructure, or production;
- required real sample, account, device, service, or acceptance evidence does not exist; or
- all safe recovery paths inside current authority are exhausted.

The report states attempted actions, evidence, confirmed root cause, excluded paths, the only remaining block, and the exact unblock condition. Do not ask the user to repeat checks already completed by the agent.
