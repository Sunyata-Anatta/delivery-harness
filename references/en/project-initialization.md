# Project Initialization and Safe Merge

Read this when a project first adopts Delivery Harness or an existing `.delivery/` needs repair. The outcome is idempotent and lossless: copy a new layout as a unit, but never replace the directory wholesale when it already exists.

## Lightweight and existing governance adoption

Temporary questions create no directories. Inspect existing rules and state first; preserve original governance. The overlay may declare one active-state path, mappings for node/authority/evidence/decisions, writer and authority, verification and recovery. Adoption passes only when these fields can be verified for reading and writing. Do not maintain a second state in `.delivery/state.md`; a compatibility entry is a pointer only. Preserve history before migration and read it on demand. Companion tasks remain independent.

Default skeleton and Git criteria below apply only to projects using that layout. For an external-state adapter, validate declared fields, writes and recovery; do not require a second `.delivery/` or tracking private material. Use a decision gate only when changing existing governance exceeds authority. Adoption remains incomplete if controlled actions cannot keep the sole state current.

## Select the delivery surface

- English projects use the [English skeleton](../../assets/en/delivery-skeleton.template.md), [state template](../../assets/en/harness-state.template.md), [overlay](../../assets/en/project-overlay.template.md), and matching auto-load block under `assets/en/`.
- Chinese projects use the Chinese surface and its [Chinese initialization reference](../project-initialization.md).
- The project-locked language binds all project placeholders and entry blocks.

## Preflight

1. Confirm the project root, repository rules, Git state, and any storage deviation recorded by the overlay.
2. Inspect only path existence, type, and names under `.delivery/`; do not read or transmit slot contents.
3. If `.delivery` is a symbolic link or reparse point, do not follow it for writes. Record the resolved target and enter the authority or project-decision gate.
4. If `.delivery`, `uploads`, `artifacts`, or `debug` has the same name but is not a directory, stop that path. Do not rename, delete, or replace the existing object.

## Merge matrix

| Observation | Action |
|---|---|
| `.delivery/` is absent | Copy the complete English skeleton. |
| `.delivery/` exists | Preserve the directory and every existing item; never replace the directory wholesale. |
| `state.md` is absent | Copy the English state placeholder. |
| `state.md` exists | Preserve the original text. Append a missing heading only when its meaning is unambiguous; route conflicting facts to a decision gate. |
| `.gitignore` is absent | Copy the skeleton rules. |
| `.gitignore` exists | Merge is additive only: preserve order and existing rules, append missing slot rules, and add no duplicate line. |
| A slot is absent | Create the directory and its `.gitkeep`. |
| A slot is a directory | Preserve all contents; add only a missing `.gitkeep`. |
| An expected directory path is another object | Stop that path and report its type and required decision. |

An explicit project deviation controls slot layout or tracking. Explicit approval of local-private state requires a recovery location, unique writer and verification method; do not claim that state is version controlled.

## Parent ignore rules

The nested `.delivery/.gitignore` works only when an ancestor does not ignore the whole directory. Before initialization run:

```text
git check-ignore -v .delivery/state.md
```

No output with exit code 1 means the untracked state file can enter Git. For an existing path, use `git check-ignore -v --no-index .delivery/state.md`. If a parent `.delivery/` rule matches, locate its controlling file from the output. When the project has no explicit deviation, append the narrow unignore block below to the version-controlled project ignore surface after the broad rule:

```gitignore
!.delivery/
!.delivery/.gitignore
!.delivery/state.md
!.delivery/uploads/
!.delivery/uploads/.gitkeep
!.delivery/artifacts/
!.delivery/artifacts/.gitkeep
!.delivery/debug/
!.delivery/debug/.gitkeep
```

Then run `git check-ignore -v --no-index .delivery/uploads/__delivery_probe__`, `git check-ignore -v --no-index .delivery/artifacts/__delivery_probe__`, and `git check-ignore -v --no-index .delivery/debug/__delivery_probe__`. Each ordinary slot probe must still match the nested skeleton rules; no probe file needs to be created.

## Related project files

Copy the English overlay into a project-declared documentation or rule path. If none is declared, use `.delivery/overlay.md`; do not ask the user merely to choose a path. The overlay belongs in the governed project, never global memory or the Skill source repository. When project privacy rules require it to be ignored, record only its path, scope, and limits in `state.md`, never sensitive values. Remove unused placeholders and fill stable facts. A copied overlay has no dependency on relative links inside the installed Skill. Append the matching marked `AGENTS.md`, `CLAUDE.md`, or restricted-runtime block to an instruction file the runtime actually reads; replace an existing marked block as a unit.

## Completion evidence

1. `.delivery/state.md`, `.delivery/.gitignore`, and all three `.gitkeep` files exist; no prior file or slot content was deleted or overwritten.
2. `git diff -- .delivery` contains only approved additions; `git status --short -- .delivery` is explainable.
3. `state.md` is not ignored unless an explicit private-state deviation was verified; ordinary slot contents are ignored.
4. Repeat the same procedure. The second run produces no new diff.
5. Before commit, inspect the actual staged set. Commit state, ignore rules, and placeholders only; handle real slot contents under project policy and the sensitive-data gate.
