# OpenClaw Runtime Contract

Primary source: [OpenClaw Skills CLI](https://docs.openclaw.ai/cli/skills); checked 2026-08-20.

## Installation
Install the root Git source with `openclaw skills install git:<owner>/<repo>@<ref> --global` or the local checkout with `openclaw skills install . --global`. Check local `--help` before relying on version-sensitive options.

## Discovery and invocation
Use `openclaw skills info delivery-harness --json` and `openclaw skills check --json`, then invoke `$delivery-harness` (composable) or `/delivery-harness`. Use the English [generic block](../../../assets/en/restricted-runtime-entry.block.template.md) only on a persistent instruction surface OpenClaw reads.

## Arrival verification
`info` must report name/source/availability; `check` must report no missing dependencies; explicit invocation must show the startup receipt. Auto-load needs two fresh-session sequence trials.

## Update
Git/local installs are unmanaged unless current CLI says otherwise. Reinstall the same source, recording old/new source and version, then rerun info/check/invocation.

## Uninstall and rollback
Confirm current uninstall syntax and scope, then remove only `delivery-harness`. Roll back from an old ref or complete copy and clean each global/agent/workspace duplicate separately.

## Known boundaries
CLI options change; ClawHub update semantics do not imply Git/local behavior. Remote Git installation crosses the network and follows authority gates.
