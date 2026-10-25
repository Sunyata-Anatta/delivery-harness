# Hard Constraints

This page is the only full text of H1-H6. The core, the gates and the startup blocks cite the IDs and never copy the rule text. Every hard constraint has a [mechanical preflight](preflight.md) check; a failed check equals the matching gate failing: no staging, commit, push or completion claim until it is fixed and rerun. A rule without a check does not belong on this page.

| ID | Rule | Mechanical check |
|---|---|---|
| [H1](#h1) | Evidence granularity: register only gate conclusions, production or field changes and failure root causes | k, l |
| [H2](#h2) | Review cap: at most 2 rounds per change; a third needs the owner to name it | m |
| [H3](#h3) | State file format: three sentences first, complete sentences, identifiers with meanings, <=80 lines | j, e |
| [H4](#h4) | Authorization scope: every authorization states what it applies to; new tasks inherit nothing | j |
| [H5](#h5) | Rules need checks: a second violation upgrades the rule to a checked hard constraint | n |
| [H6](#h6) | Main-line work: unless explicitly asked, parallel tasks use worktrees, no new branches | o |

Run: `python -B -X utf8 <skill>/references/preflight.py --root . --json` before the first `git add`, before every commit (`--staged`) and before any completion claim. Check l only warns by default; the others block by default. A project may change a severity only through a registered decision that gives the reason.

<a id="h1"></a>
## H1 Evidence granularity

Rule: fact or evidence entries are registered for three kinds only, tagged `[gate]` (gate conclusion), `[change]` (production or field change) and `[root-cause]` (failure root cause); the equivalent Chinese tags on the Chinese page are accepted too. Each entry carries its registration date `YYYY-MM-DD`; review conclusions state `round N`. UI, copy and style tweaks and single-page fixes live only in the commit message: no new entry, no baseline bump and no new evidence file.

Check: k checks that new or edited evidence lines carry a tag, a date and, for reviews, the round; when every change in the batch matches `evidence.minor_paths` (by default style sheets, `locales/` and `i18n/`; projects add their UI copy paths), a new entry, a baseline bump or a new file under `evidence.files` blocks; a baseline change with no new entry or decision also blocks. l counts entries per date and warns when one date exceeds `evidence.daily_limit` (default 5), prompting an entry-by-entry review.

On failure: delete entries outside the three kinds and move their content into the commit message; relabelling a tag to pass is not a fix.

<a id="h2"></a>
## H2 Review cap

Rule: one change gets at most 2 independent review rounds. Before each round, record `- <change name>: round N; named by: none.` in the state's "Review rounds" section, and evidence entries state the round number too. When a third round is needed, stop, write the [stop line](gates.md#stop-reason) "waiting for user decision", and hand the findings and evidence of both rounds to the owner; after the owner names the round, change the line to `named by: <owner and original receipt>` and only then start round 3. Every further round needs a new naming.

Check: m reads the "Review rounds" section of the state; it blocks with "stop here" when the section is missing or any line has a round above 2 with an empty or "none" naming.

On failure: stop reviewing; never open a third round on your own to fix small issues. This rule bounds the re-review loop of the [independent-review recovery gate](gates.md#review-failure-recovery).

<a id="h3"></a>
## H3 State file format

Rule: the first level-2 heading of the state file is always `## Three sentences`, holding exactly three items in this order: `Now at:` (the current node), `Next:` (the next action) and `Waiting on:` (who or what it waits for). The body is complete sentences, each line ending with a full stop, question mark or exclamation mark; internal shorthand is banned, by default `→`, `=>`, `->`, `TBD`, `w/` and `&&` (inside code spans excepted). Every identifier is written with its meaning: "ID (meaning)", or defined at the start of a line as "- ID meaning". The whole file stays at 80 lines or fewer. See the [state template](../../assets/en/harness-state.template.md).

Check: j checks the three-sentence section, complete sentences, shorthand tokens, identifier meanings and the authorization section; e checks the line count (`limits.record_max_lines`, default 80). Unfilled template placeholders count as empty, so a template copied unchanged cannot pass.

On failure: rewrite line by line as prompted; above 80 lines move history and evidence detail to their single homes instead of splitting a second state file.

<a id="h4"></a>
## H4 Authorization scope

Rule: in the state's "Authorizations and scope" section every authorization states `Applies to: <rounds or tasks>`. A new task never inherits an older authorization: the section must contain a `Not covered:` line listing the actions the current task may not take. When moving to a new task, only authorizations whose `Applies to` names that task stay valid; the rest are history.

Check: j checks that the authorization section exists, that every authorization has `Applies to:`, and that `Not covered:` has content.

On failure: add the scope; when the scope is unclear, treat it as unauthorized and ask for new authority. This rule supplements [reuse authorization within the same node](gates.md#authorization-reuse).

<a id="h5"></a>
## H5 Rules need checks

Rule: every hard constraint has a mechanical check. A rule without a check that is violated a second time must be upgraded to a hard constraint with a check; adding more text is not allowed. Rule changes are registered as decisions per the next section.

Check: n checks the decision register: every decision has a meaning, type, rule, relation and basis; a hard constraint cannot have an empty check; a violation count of 2 or more without a check blocks; rule text with undecidable words blocks; decision IDs cited by executor files must exist. The skill's own rule table is checked by a repository test: every row of the table above must name checks that preflight already has.

On failure: write the check first, then register the rule; a rule nobody can check stays guidance and is never called a hard constraint.

<a id="h6"></a>
## H6 Main-line work

Rule: unless the owner explicitly asks for a branch, parallel tasks use worktrees on the main line and create no new local branch:

1. `git worktree add --detach <path> <main line>` creates a detached-HEAD worktree.
2. Commit inside that worktree; when done, run `git merge --ff-only <commit>` in the main worktree to fast-forward the main line.
3. When a fast-forward is impossible, run `git rebase <main line>` inside that worktree and fast-forward afterwards; stop and report on conflicts.
4. `git worktree remove <path>` cleans up the worktree.

When the owner asks for a branch, register the decision first, then add the branch name to `branches.allowed`. When adopting an existing project, list each existing branch in `branches.allowed` and note that it predates adoption.

Check: o lists local branches and blocks any branch not in `branches.allowed` (default `main`, `master`).

On failure: fast-forward or rebase the commits of the new branch onto the main line, then delete the branch; when deleting needs authority, ask through the gates.

## Rule revision mechanism

- Registration: new, supplementing and superseding rules are registered as owner decisions with D numbers, by default in `.delivery/decisions.md`, using the [decision template](../../assets/en/decisions.template.md). Rule tables cite the decision number and never copy the full text into several files; executor files (AGENTS.md and the like) hold only executable items and point at the decision number.
- Relation and basis: every decision states which older rule it supplements or supersedes and its basis (a review report or fact number).
- Decidable: rule text avoids undecidable words such as "appropriate", "as needed", "if necessary", "when necessary", "reasonable" and "where possible", and uses thresholds, lists or observable events instead; check n blocks these words.
- Version: the baseline changes only for a gate conclusion, a production or field change, a failure root cause or a new decision; wording changes never bump it, and check k blocks an unsupported bump.
- When this skill revises its own rules, the revision log below states what was supplemented or superseded and the basis, and both languages change together.

The standard code formatting flow is not a hard constraint; see [formatting](formatting.md).

## Revision log

| Version | Change | Supplements or supersedes | Basis |
|---|---|---|---|
| 2026.10.25.1 | Added H1-H6 and checks j-o | H1 supplements the evidence receipt gate and the compaction triggers; H2 bounds the re-review loop of the independent-review recovery gate; H3 supersedes the old sectioned state template; H4 supplements authorization reuse within a node; H5 and H6 are new | Review of a real project: 222 fact entries in 14 days, 9 review rounds for one change, a state file turned into shorthand only agents could read, a front-end line of almost 3000 characters, and an existing written "no over-review" rule that never took effect; owner revision instruction of 2026-10-25 |
