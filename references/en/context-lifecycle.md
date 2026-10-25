# Document compaction and safe continuation

Read when adopting long existing records, closing a node, handing off, exceeding a candidate-summary budget, or finding duplicated facts. Ordinary startup follows [core](core.md), without loading this page or history. Acceptance means the next executor can continue safely while default reading stays bounded as history grows.

On-demand entries: [ownership](#ownership), [reading](#reading), [triggers](#triggers), [procedure](#procedure), [recovery](#recovery), [verification](#verification).

<a id="ownership"></a>
## One maintenance location per fact

Use the sole sources already resolved by the overlay. Names below describe default responsibilities; they do not require renaming or empty files.

| Document | Keep | Update method and soft budget |
|---|---|---|
| `state.md` | Target assets/scope, active node, action authority, open gates, necessary limits, unknown outcomes/in-flight work, one next action and recovery | Replace current summaries; format and <=80 physical lines per [H3](hard-constraints.md#h3), preferably <=5 KiB; measure tokens separately |
| `process.md` | Process index, historical checkpoints needed for continuation, latest compaction receipt entry | About 30 lines; replace the index and archive old detail/indexes |
| Evidence summary | Verified results, object version/batch, scope, limits and exact original receipt entries | About 50 lines; replace outdated summaries, retain original receipts by batch |
| Artifact README | Directory purpose, last registered batch, retention rules, batch manifests and recovery entries | About 30 lines; move old batch detail out instead of accumulating per-file history |
| Baseline, overlay, map and navigation | Stable rules, sole-source paths, document responsibilities and read triggers | Update on change; link to results, active blockers and authority |
| Lessons | Evidence-based lessons that change future work, applicability and revisit conditions | Replace/merge by topic; archive invalidated lessons and read by task |

Specifications and plans own approved scope, steps and acceptance, not live progress. Consumed/revoked/expired authority is historical; any resulting restriction on the next action remains in state. Once a lesson becomes a baseline rule, keep only its rationale and rule entry in lessons rather than another maintained copy.

If an existing append-only system cannot become an index, use its verifiable section/query/pagination entry and define default reading scope and archival in the overlay. Preserve original identifiers and meaning; do not add writable state or silently rewrite that system.

<a id="reading"></a>
## Default reads and stopping expansion

Read only effective project rules, the overlay startup summary/hard constraints/sole-source fields, the sole state, and the clauses required by the current action. `process.md`, evidence summaries, artifact READMEs, lessons and history are not a mandatory startup bundle. An overlay pointer makes content locatable; it does not recursively load it.

| Current need | Additional read and stopping condition |
|---|---|
| Decide whether the next action can proceed | State's target, authority, gates, unknown outcomes and in-flight work; expand the relevant original only for unclear, conflicting or changed sources |
| Verify a conclusion | That evidence-summary item, then its version/batch receipt; stop once the evidence scope is sufficient |
| Retrieve or clean artifacts | That task's README and matching batch manifest, retention decision and recovery entry |
| Explain an earlier decision or error | The historical identifier/section selected by the process index; do not replay all batches |
| Apply a lesson | Its matching topic and necessary evidence; resolve authority through state and original approval |
| Recover interrupted compaction | State's batch/stage/recovery entry, then that batch's manifest; follow recovery below, never execute historical commands directly |

Keep stable record identifiers/explicit anchors; line numbers are locating aids only. When a passage cannot be read reliably in isolation, read the complete rule unit. Expand conflicting, truncated or unverifiable sources rather than skipping necessary conditions for a budget. Reuse unchanged content already read; a smaller file does not unload its old text from the current conversation.

<a id="triggers"></a>
## When to compact

Replace current fields on every state update. Add durable records only for new facts affecting scope, authority, gates, limits, recovery or future practice. Routine successful commands, repeated test narration and "no new findings" create no new history entries; evidence entries are only the three kinds in [H1](hard-constraints.md#h1).

At node closure, handoff, project adoption, any over-budget candidate summary or duplicated fact, check whether the related documents need compaction. Process only materially changed files or actual historical burden. With no change, reuse the receipt without new timestamps, snapshots or maintenance logs. Total history may grow; the default reading set does not grow with batch count.

All size targets are soft. Move duplicates and completed history first; if necessary safety information still exceeds a target, retain it with the reason and next action. Never truncate authority/risks, pack long lines, hide content or report an over-budget result as a budget pass.

<a id="procedure"></a>
## Protect originals before replacing summaries

1. **Confirm scope and writers.** Resolve existing paths, storage/privacy policy and recovery location through the overlay. Check target/parent types, permissions and symlink/reparse boundaries. Inventory in-flight work and other writers; when shared writes cannot be coordinated, prepare candidates without replacing active files.
2. **Save immutable originals.** Reuse project history storage; otherwise create `.delivery/history/<batch>/` only as needed. Preserve original bytes and relative directory structure. A manifest records original path, snapshot path, source version, bytes and SHA-256; reread and compare each copy. Preserve relative-link dependencies or record their original resolution base and verifiable recovery mapping. Unresolved necessary dependencies cannot count as recoverable.
3. **Label history without modifying originals.** Mark the batch README/manifest "Historical record, not current authority", and label every navigation link to its snapshots as historical. Do not insert a warning into already-hashed source bytes. The batch must identify itself independently as historical; read its notice before opening a raw original. Sensitive materials retain authorized restricted storage; ignore rules are neither access control nor backup.
4. **Extract continuation essentials.** Check originals for target assets; valid authority's source/action/scope/conditions; used/reserved/remaining amounts when limited; open gates/unblock conditions; failure limits; unknown outcomes; parallel task identifier/owner/scope/receipt; and recovery. One next action is the successor's next action, not a claim that no other work is running.
5. **Prepare replacement and interruption recovery.** Keep candidates outside active reading paths. After checking links and required fields, register the batch's incomplete compaction, stage and recovery entry in the sole state. Without an atomic multi-file switch, write other documents first and the verified new state last, closing the compaction gate. Track expected versions/hashes, including this operation's state marker. Check before every replacement for other writers' changes; reconcile and revalidate drift instead of overwriting concurrent facts.
6. **Replace and record a minimal receipt.** Recheck original hashes, links/anchors, field continuity and document diffs before completing the switch. The receipt records only batch, source version, archive/check entry, changed files, before/after reading measurements, necessary exceptions and recovery. Keep detail in its batch record and only the latest receipt link in process. Normal compaction neither deletes originals/history nor requests already-covered authority again.

Segment historical detail by phase/task/batch. The history index also serves on-demand routing; do not copy every batch summary into the active index. Keep exact original evidence and authority sources; a summary is an entry, not a substitute for the original approval.

<a id="recovery"></a>
## Authority continuity and failure recovery

Before a quota-limited or unsafe-to-repeat side effect, persist the operation identifier and reserved/in-flight status in the sole state, using the original authority's consumption rules. When a sent operation has an unknown outcome, timeout or a missing receipt neither returns its quota nor permits an automatic retry. Check that operation and in-flight work first. Reuse an operation identifier only under a verified platform idempotency contract; do not assume idempotency.

If archive write/readback, hashes, references or required fields fail, preserve originals. Until the switch completes, keep the compaction gate open; the next action checks actual persisted versions and completes or recovers that batch. Pause only actions depending on this uncertainty; independent authorized work may continue.

Restoring an old snapshot restores material, not its former authority. Reconcile the latest approval with subsequent consumption, revocation, expiry and operation receipts before rebuilding valid state. Never replay an already executed action because an old snapshot says "one use remaining". If this cannot be determined, record unknown and block the affected side effect rather than assuming success, failure or renewed authority.

<a id="verification"></a>
## Verify only what this change requires

For document-only compaction, check original/manifest SHA-256, retained paths and anchors, continuity of required fields and unknown/in-flight work, unchanged authority scope, no second active state, and a diff containing only intended documents. With no application artifact/behavior change, do not rerun the full application suite. Skill rule changes still need the relevant behavioral scenarios.

Compare the same reading task's default files/sections, actual read bytes and physical lines. Measure tokens using the same known tokenizer; explicitly report unavailable measurement. Report baseline and result separately, counting host injection, tool output and historical rereads separately. Byte reduction is not proportional token reduction; neither fixed savings claims nor shorter files replace acceptance.

From default entries, a successor must identify the target, permitted action, open gates, unknown/in-flight work, one next action and recovery; verify evidence by opening its selected source. Check long history, an unknown single-use operation, old-snapshot recovery, concurrent updates and interrupted compaction. Simulations do not constitute production or actual host-runtime evidence.

For new projects, select [process index](../../assets/en/process-index.template.md), [evidence summary](../../assets/en/evidence-summary.template.md) and [artifact README](../../assets/en/artifact-readme.template.md) templates by actual responsibility. Migrate existing projects in place in the order above rather than creating a parallel system.
