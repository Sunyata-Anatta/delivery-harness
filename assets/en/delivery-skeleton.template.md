# Complete `.delivery` Skeleton

Copy the sibling `delivery-skeleton/.delivery/` directory into the governed project root only for the default state layout. If `.delivery/` already exists, merge file by file without overwriting current state or evidence. With an existing-state adapter, skip default `state.md` creation rather than copying the full tree.

For existing-directory checks, parent-ignore handling, the merge matrix, and verification, read [Project Initialization and Safe Merge](../../references/en/project-initialization.md).

The skeleton contains:

- [`state.md`](delivery-skeleton/.delivery/state.md): a project-tracked active-state placeholder to fill and maintain;
- [`.gitignore`](delivery-skeleton/.delivery/.gitignore): ignores evidence-slot contents while retaining directory placeholders;
- [`uploads/.gitkeep`](delivery-skeleton/.delivery/uploads/.gitkeep): placeholder for immutable user inputs;
- [`artifacts/.gitkeep`](delivery-skeleton/.delivery/artifacts/.gitkeep): placeholder for generated artifacts, test materials and evidence;
- [`debug/.gitkeep`](delivery-skeleton/.delivery/debug/.gitkeep): placeholder for diagnostic material.

This is only the state/resource-slot skeleton. Follow [resource storage](../../references/en/execution.md#resource-storage) to create `tmp/` and `retained/` under `artifacts/<task>/` only with content.
Both inherit existing ignore rules; retained items are not automatically cleaned. Follow initialization to fill the [overlay](project-overlay.template.md), [project map](project-map.template.md) and rules/README entries.
Adapt equivalent existing files or sections and register their canonical entries; do not create duplicates.

## On-demand output templates

These are optional outputs, not mandatory skeleton files. Use them only with content or a compaction need; do not copy empty process, evidence or README documents at startup:

- [Process index](process-index.template.md): important historical checkpoints, latest compaction receipt and lazy history entry;
- [Evidence summary](evidence-summary.template.md): fixed version, scope, conclusion, limits and original receipts;
- [Artifact README](artifact-readme.template.md): purpose, latest immutable batch, retention/recovery and batch-manifest entries.

Reuse canonical entries under [content ownership](../../references/en/context-lifecycle.md#ownership); follow the [compaction procedure](../../references/en/context-lifecycle.md#procedure) before replacement.
Resolve project paths relative to each output file or an explicit workspace and verify reachability; outputs must not depend on relative links into the Skill source tree.
The template/contract links in this instruction document belong to the installed Skill and are not copied as project-document dependencies.

When commit is authorized, include state, ignore rules, placeholders and approved navigation/rules under their tracking/privacy policy. Do not commit real slot contents unless project rules require it and the material has passed sensitive-data checks.
