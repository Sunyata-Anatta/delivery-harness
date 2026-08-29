# Generic Agent Skills Runtime Contract

Use this contract for hosts that claim compatibility with the Agent Skills directory structure but have no adapter specific to this Skill. Read the host's primary documentation and local help first. The rules below are a minimum interoperability contract, not guessed product commands.

## Installation

Confirm that the host loads a directory containing a `SKILL.md` with YAML frontmatter. Copy the four items from this repository root into the host's declared user-level or project-level directory, preserving `delivery-harness` as the target directory name:

```text
delivery-harness/
  SKILL.md
  agents/
  assets/
  references/
```

If the host accepts only one file, discards relative references, or requires executable scripts, this Skill does not satisfy its installation contract. Do not present a partial copy as compatibility.

## Discovery and Invocation

Use the host's Skill list, inspection, or parsing command to confirm `name: delivery-harness`. Take explicit invocation syntax from local help; invoke it with “Start from current reality and continue until the accepted evidence gates pass.”

Write an automatic-loading entry only into a project instruction file the host explicitly reads. If the target is neither `AGENTS.md` nor `CLAUDE.md`, replace the placeholders in [restricted-runtime-entry.block.template.md](../../../assets/restricted-runtime-entry.block.template.md).

## Arrival Verification

1. Byte manifest and per-file hashes match.
2. Frontmatter parses and internal relative links resolve.
3. The host lists and can explicitly invoke this Skill.
4. If automatic loading is claimed, the startup receipt precedes the first tool call in a fresh session; repeat at least twice.

Without level-three evidence, report only “files deployed; runtime not verified.”

## Update

Save the old version or hashes, completely overwrite all four items, clear only the Skill cache explicitly documented by the host, then repeat discovery and arrival verification. Do not update only the entry file while leaving stale references.

## Uninstall and Rollback

Delete or unregister only `delivery-harness`, following the host documentation. Update the project entry block too. For rollback, restore all four items and restart the session or process required by the host.

## Known Boundaries

- “Markdown compatible” does not mean “Agent Skills compatible.”
- A host can ignore `agents/openai.yaml`; this does not disable the core rules, but OpenAI metadata is lost.
- Directory precedence, hot reload, invocation prefix, and trust model have no cross-host guarantee.
- Without primary documentation or real runtime evidence, do not mark the host verified in the support matrix.
