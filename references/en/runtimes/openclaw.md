# OpenClaw Runtime Contract

Based on the OpenClaw [Skills CLI documentation](https://docs.openclaw.ai/cli/skills); facts last verified on 2026-08-20.

## Installation

This repository root contains `SKILL.md` and can be installed directly from a Git source:

```bash
openclaw skills install git:<owner>/<repo>@<ref> --global
```

Install the current local checkout with:

```bash
openclaw skills install . --global
```

Without `--global`, installation follows the current OpenClaw workspace or Agent scope. When a specific Agent is required, use the Agent option declared by that installed version. First run `openclaw skills install --help` to verify local syntax, and do not copy credential values from help output into records.

## Discovery and Invocation

```bash
openclaw skills info delivery-harness --json
openclaw skills check --json
```

Then use a composable explicit reference in a fresh session:

```text
$delivery-harness Start from current reality and continue until the accepted evidence gates pass.
```

The standalone command form `/delivery-harness ...` is also available. Prefer `$delivery-harness` when composing multiple Skills in one prompt.

If the OpenClaw workspace has a persistently loaded project instruction file, use [restricted-runtime-entry.block.template.md](../../../assets/restricted-runtime-entry.block.template.md); otherwise register explicit-invocation mode.

## Arrival Verification

1. `skills info` returns the exact name, source, and availability state.
2. `skills check` reports no missing dependencies.
3. Explicit invocation reads this Skill's fixed startup block.
4. When automatic loading is claimed, a fresh session proves the receipt precedes the first tool call; repeat at least twice.

If installation exits zero but `skills info` cannot find the target, the installation still fails.

## Update

Do not assume Git or local installations have ClawHub's tracked-update semantics. Reinstall from the same source, using an overwrite option only when current CLI help requires it. Record the old source and version before updating, then rerun `info`, `check`, and explicit invocation.

## Uninstall and Rollback

Use `openclaw skills --help` or version-matched documentation to confirm the uninstall subcommand and scope, then uninstall only `delivery-harness`. Roll back by reinstalling from the old Git ref or a complete backup. Clean up global and Agent-level installations separately so an old copy cannot shadow the result.

## Known Boundaries

- OpenClaw CLI options can change by version; local `--help` is the execution criterion.
- ClawHub update semantics cannot be applied automatically to Git or local sources.
- Same-name Skills can coexist at workspace, Agent, and global scope; record the source actually resolved.
- Remote Git installation uses the network and an external source, so it remains subject to the authority gate.
