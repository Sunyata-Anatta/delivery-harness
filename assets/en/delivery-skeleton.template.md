# Complete `.delivery` Skeleton

Copy the sibling `delivery-skeleton/.delivery/` directory into the governed project root only for the default state layout. If `.delivery/` already exists, merge file by file without overwriting current state or evidence. With an existing-state adapter, skip default `state.md` creation rather than copying the full tree.

For existing-directory checks, parent-ignore handling, the merge matrix, and verification, read [Project Initialization and Safe Merge](../../references/en/project-initialization.md).

The skeleton contains:

- [`state.md`](delivery-skeleton/.delivery/state.md): a project-tracked active-state placeholder to fill and maintain;
- [`.gitignore`](delivery-skeleton/.delivery/.gitignore): ignores evidence-slot contents while retaining directory placeholders;
- [`uploads/.gitkeep`](delivery-skeleton/.delivery/uploads/.gitkeep): placeholder for immutable user inputs;
- [`artifacts/.gitkeep`](delivery-skeleton/.delivery/artifacts/.gitkeep): placeholder for generated and evidence artifacts;
- [`debug/.gitkeep`](delivery-skeleton/.delivery/debug/.gitkeep): placeholder for diagnostic material.

This is only the state/temporary-slot skeleton. Full adoption also follows the initialization reference to fill the [overlay](project-overlay.template.md), [project map](project-map.template.md) and rules/README entries, and reuse or create a process record. Adapt equivalent existing files rather than creating duplicates.

When commit is authorized, include state, ignore rules, placeholders and approved navigation/rules under their tracking/privacy policy. Do not commit real slot contents unless project rules require it and the material has passed sensitive-data checks.
