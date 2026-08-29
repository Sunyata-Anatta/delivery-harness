# Complete `.delivery` Skeleton

Copy the sibling `delivery-skeleton/.delivery/` directory into the governed project root. If `.delivery/` already exists, merge file by file without overwriting current state or evidence.

For existing-directory checks, parent-ignore handling, the merge matrix, and verification, read [Project Initialization and Safe Merge](../../references/en/project-initialization.md).

The skeleton contains:

- [`state.md`](delivery-skeleton/.delivery/state.md): a project-tracked active-state placeholder to fill and maintain;
- [`.gitignore`](delivery-skeleton/.delivery/.gitignore): ignores evidence-slot contents while retaining directory placeholders;
- [`uploads/.gitkeep`](delivery-skeleton/.delivery/uploads/.gitkeep): placeholder for immutable user inputs;
- [`artifacts/.gitkeep`](delivery-skeleton/.delivery/artifacts/.gitkeep): placeholder for generated and evidence artifacts;
- [`debug/.gitkeep`](delivery-skeleton/.delivery/debug/.gitkeep): placeholder for diagnostic material.

Commit `state.md`, `.gitignore`, and the three `.gitkeep` files. Do not commit real slot contents unless project rules require it and the material has passed sensitive-data checks.
