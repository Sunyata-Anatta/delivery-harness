# Operating Principles

These rules select the next action; they do not add ceremony.

## Verify reality first

- Inspect code, runtime, dependencies, tests, and deployment evidence before reporting status.
- Designed, implemented, tested, deployed, and accepted are distinct states.
- An interface does not prove its backend is deployed; a local commit is not a release.
- Synthetic fixtures prove mechanics, not real-world quality.

## Keep progress simple

- Keep one active node. Activate the next only after verifying the current gate.
- Documentation sync is a transition, not the final deliverable.
- Prove behavior with the smallest reversible architecture before adding services.
- Preserve unrelated user changes; commit only files traceable to the active goal.
- Treat failure as a diagnostic node. Recover autonomously within existing authority.

## Be explicit about uncertainty

Record unavailable backends, missing evidence, low-confidence results, and review states. Send ambiguous results to review. Check connector, CLI, browser, sandbox, and desktop contexts separately before declaring a real block. Missing real evidence stops at the evidence gate; speculative implementation cannot replace acceptance.

## Learn only from evidence

An experience record needs context, attempt, evidence, conclusion, new guardrail, and revisit condition. A Resolver maps repeatable conditions to a skill, tool, or process with evidence, fallback, validation, and revisit conditions. Keep single-project rules and experience in the project overlay; strengthen the general Skill only for repeated cross-project failures.
