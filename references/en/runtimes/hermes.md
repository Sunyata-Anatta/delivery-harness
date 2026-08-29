# Hermes Agent Runtime Contract

Based on the Hermes Agent [Skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/); facts last verified on 2026-08-20.

## Installation

The stable user-level path is `$HOME/.hermes/skills/delivery-harness`. Copy the four items `SKILL.md`, `agents/`, `assets/`, and `references/` from this Skill root.

A project-level copy can be placed at `<project>/.agents/skills/delivery-harness`; then trust the entire project from its root:

```bash
hermes skills trust
```

Hermes supports Hub and direct-URL sources, but the default tap convention discovers multiple Skills below a repository's `skills/` path. This repository deliberately uses one Skill at its root, so do not present the default tap as a zero-configuration installation route for this root repository.

## Discovery and Invocation

```bash
hermes skills list
hermes skills inspect delivery-harness
```

Explicitly invoke it in a new session:

```text
/delivery-harness Start from current reality and continue until the accepted evidence gates pass.
```

The project instruction entry depends on the instruction surface currently reachable by Hermes. When one exists, use [restricted-runtime-entry.block.template.md](../../../assets/restricted-runtime-entry.block.template.md); otherwise record the explicit-invocation boundary.

## Arrival Verification

1. Per-file hashes prove all four items were copied completely.
2. `skills list` and `skills inspect` return the actual source and trust state.
3. Explicit invocation produces this Skill's fixed startup block.
4. Any automatic-loading claim requires fresh-session ordering evidence, repeated at least twice.

A readable but untrusted project Skill is not an executable installation.

## Update

For a local-copy source, completely overwrite all four items. For a Hub source, use the check/update flow offered by the installed Hermes version. Inspect again after the update and confirm another same-name copy in an external directory has not shadowed the resolved source.

## Uninstall and Rollback

For a local copy, remove only the exact target directory. For a Hub installation, use the Hermes uninstall command. Roll back by restoring the complete old copy or version. Revoke project-level trust and entry blocks according to the actual configuration; deleting only the user-level copy is insufficient.

## Known Boundaries

- A project Skill requires explicit trust; directory presence does not make it executable.
- External directories can create same-name shadowing and writable-source risk; record the source actually resolved.
- The default tap's `skills/` layout differs from this repository's single-Skill root. Without a custom tap path, compatibility is not promised.
- Direct-URL installation must prove every relatively referenced resource was fetched; fetching only `SKILL.md` is incomplete.
