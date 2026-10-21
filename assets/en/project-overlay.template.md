# {{PROJECT_NAME}} Delivery Overlay

Store stable rules, definitions and canonical pointers only. This overlay may tighten Delivery Harness but cannot override system, safety or user instructions.
Keep active state in sole state, fixed observations in evidence, history in process/history and lessons in their own entry. Remove unused entries.

## Project identity
- Outcome: {{ACCEPTED_OUTCOME}}
- Non-goals: {{NON_GOALS}}
- Users: {{USERS}}
- Locked language: {{LANGUAGE_AUTO_ZH_EN}}

## Sources of truth
- Repository rules: {{REPOSITORY_INSTRUCTIONS}}
- Accepted specification: {{ACCEPTED_SPEC}}
- Execution plan: {{EXECUTION_PLAN}}
- Active state: `{{ACTIVE_STATE_PATH}}` (sole pointer; use `.delivery/state.md` for the default layout)
- Navigation: `{{PROJECT_MAP_PATH}}` (default `PROJECTMAP.md`; skeleton and on-demand entries, never recursively expanded)
- Rule entries: {{RULE_CLAUSE_ENTRIES}} (source paths and scope/sections; reference existing clauses instead of copying them)
- Process index: `{{PROCESS_RECORD_PATH}}` (default `.delivery/process.md`; important historical checkpoints and latest compaction receipt, read by topic/ID)
- Original history entry: `{{HISTORY_ENTRY_PATH}}` (existing archive entry or on-demand manifest; immutable originals, never expanded at startup)
- Evidence entry: `{{EVIDENCE_ENTRY_PATH}}` (existing report/section or on-demand summary; fixed subject, version, result, limits and original receipts)
- Lessons entry: `{{LESSONS_ENTRY_PATH}}` (reuse an existing file/section; read for the current task or recurrence condition, never duplicate)
- Existing-state adapter: {{STATE_FIELD_MAPPING_WRITER_AUTHORITY_VERIFY_RECOVERY}} (node/authority/evidence/decision fields, writer and authority, verification and recovery; no additional active state)

Define these paths here only; summaries and other sections refer to the field names. Path fields default to the project root (the worktree root for a repository); relative Markdown links resolve from their containing document.
Preserve an existing governance system's declared path base. State different or cross-workspace bases here; never silently reinterpret existing paths.
Keep adoption/conformance, commit findings, errors, options/choice and supporting data in immutable receipts; the process index holds necessary navigation only.

## Storage
Root: `.delivery/`
- Active state: use the sole pointer above; version by default, with recovery location and verification for privacy deviations
- `uploads/`: approved short-term user inputs, unchanged
- `artifacts/<task>/tmp/`: disposable/rebuildable intermediates and one-off test resources; register cleanup conditions
- `artifacts/<task>/retained/`: demos, images/documents/audio/video and manual-test materials needed for delivery or retention; no automatic cleanup
- `debug/`: temporary debugging output and reproduction material
Reuse resource registration; otherwise a task README holds purpose, latest immutable batch, retention/recovery and batch-manifest entries.
Keep details in batch manifests; archive and verify old summaries before replacement, never append endless item lists. Create task subdirectories only with content.
State/map hold entries only. Preserve unclassified older materials. Copy sandbox outputs to the project and verify before delivery.
On failure retain sources and put recovery actions in sole state. Git-ignore or retention status proves neither backup nor outbound authority.
For the default layout, follow the installed Skill's initialization reference and copy the state/resource-slot skeleton; skip state creation with an existing-state adapter.
Create process indexes, evidence summaries and artifact READMEs on demand with content; adapt equivalent files and never create empty startup documents.
Durable specifications, formal evidence reports and regression/build dependencies use project-semantic locations; sensitive originals stay in approved restricted storage.
Deviations: {{STORAGE_DEVIATIONS}}
History tracking/privacy/recovery policy: {{HISTORY_TRACKING_PRIVACY_RECOVERY_POLICY}} (access, retention, recovery entry and verification).
Versioning state does not automatically track or publish historical originals; preserve history under its own approved policy.

## Project rules
- Required: {{PROJECT_MUST_RULE}}
- Forbidden: {{PROJECT_MUST_NOT_RULE}}
- Conventions: {{PROJECT_CONVENTIONS}}
- Data/privacy: {{DATA_RULES}}

## Startup summary

At ordinary startup read only this page's source-pointer definitions, applicable hard constraints and this section, then the resolved sole state.
Do not load the whole overlay by default. Keep outcome, source-field references, profile and hard constraints here; soft target <=450 tokens.
Read long details for the current action without expanding every entry. Budgets never remove necessary safety or acceptance clauses.
Read the relevant full definitions on first adaptation or when mappings are unclear.
- profile: `auto` (research/develop/review/document/operate adjust candidates only)
- Routing source: this Resolver; move long detail to `.delivery/routing.md` and remove duplicate tables
- Conformance: check applicable clauses before actions; at transitions, rule/path changes or validation failures follow the Harness execution contract.
  Current conclusions/blockers go to sole state, fixed results to evidence and detailed-receipt entries to the process index.

## Resolver
| Condition | Skill/tool/process | Evidence reference | Fallback | Verification definition | Revisit when |
|---|---|---|---|---|---|
| {{CONDITION}} | {{ROUTE}} | {{ROUTE_EVIDENCE_REF}} | {{FALLBACK}} | `{{VERIFY_COMMAND}}` | {{REVISIT_WHEN}} |

## Capability installation catalog

Use this table only when the current Agent does not discover a needed capability. Give a verified installation source and method before requesting its authority; when either is unknown, leave it uninstalled and use the fallback.

| Capability | Type | Installation source and version | Current-runtime installation method | Authority impact | Discovery and behavior verification | Fallback |
|---|---|---|---|---|---|---|
| {{CAPABILITY}} | {{SKILL_PLUGIN_MCP_CLI}} | {{SOURCE_AND_VERSION}} | `{{INSTALL_COMMAND_OR_METHOD}}` | {{AUTHORITY_REQUIRED}} | `{{VERIFY_COMMAND}}` | {{FALLBACK}} |

## Commands
- Bootstrap: `{{SESSION_BOOTSTRAP_COMMAND}}`
- Setup: `{{SETUP_COMMAND}}`
- Focused test: `{{FOCUSED_TEST_COMMAND}}`
- Full test: `{{FULL_TEST_COMMAND}}`
- Lint: `{{LINT_COMMAND}}`
- Build: `{{BUILD_COMMAND}}`
- Run: `{{RUN_COMMAND}}`
- Deployment verification: `{{DEPLOY_VERIFY_COMMAND}}`

## Authority
Define standing rules and boundaries here; maintain effective grants, source/actions, allocations and expiry only in sole state.
- Preauthorized: {{PREAUTHORIZED_ACTION}}
- Tool mode: preauthorized set `{{PREAUTHORIZED_TOOLS}}` / individual approval
- Installation receipts go to evidence; stable configuration belongs in the integration registry.
- Explicit approval required: {{APPROVAL_REQUIRED_ACTION}}
- Forbidden: {{FORBIDDEN_ACTION}}

## Integrations and credentials
| Integration | Purpose | Entry | Owner | Configured permission boundary | Verification definition | Data boundary | Rollback |
|---|---|---|---|---|---|---|---|
| {{INTEGRATION}} | {{PURPOSE}} | {{CONNECTOR_CLI_OR_BROWSER}} | {{OWNER}} | {{SCOPES}} | `{{VERIFY_COMMAND}}` | {{DATA_BOUNDARY}} | {{ROLLBACK}} |

Never store tokens, passwords, private keys, or reusable authentication here.

## Distribution surface registry

Register stable paths, installers, owners, account-synchronized surfaces and hosted entries that receive the artifact.
Keep checked versions/times, evidence levels, results and limits only in referenced evidence. Unknown/unreachable remains unverified.
Success on one surface cannot prove another is updated. Current blockers belong only in sole state; this is not another distribution-progress record.

| Surface | Resolver or address | Owner | Update method | Canonical source | Verification definition | Evidence reference | Rollback |
|---|---|---|---|---|---|---|---|
| {{DISTRIBUTION_SURFACES}} | {{SURFACE_RESOLVER_OR_ADDRESS}} | {{SURFACE_OWNER}} | {{SURFACE_UPDATE_METHOD}} | {{CANONICAL_SOURCE}} | {{SURFACE_VERIFY_METHOD}} | {{SURFACE_EVIDENCE_REF}} | {{ROLLBACK}} |

## Real-evidence gate definitions
| Phase | Evidence | Sample/environment | Pass criteria | Unblock condition |
|---|---|---|---|---|
| {{PHASE}} | {{EVIDENCE}} | {{SAMPLE_OR_ENVIRONMENT}} | {{PASS_CRITERIA}} | {{UNBLOCK_CONDITION}} |

## Version control
- Deliverable paths: {{DELIVERABLE_PATHS}}
- Development-only paths: {{DEV_ONLY_PATHS}}
- Deliverable dependency policy: {{DELIVERABLE_DEPENDENCY_POLICY}}
- Default branch / branch rule: {{DEFAULT_BRANCH}} / {{BRANCH_RULE}}
- Commit rule: {{COMMIT_RULE}}
- Author identity policy: {{AUTHOR_IDENTITY_POLICY}}
- Secret scan: {{SECRET_SCAN_COMMAND_AND_SCOPE}}
- Project-only forbidden terms: {{FORBIDDEN_TERMS}}
- Staged-file list command: {{STAGED_FILE_LIST_COMMAND}}
- Scan evidence: use the evidence source field, selecting subject version and scan scope; do not copy the latest result here
- History privacy policy: {{HISTORY_PRIVACY_DECISION}}
- Push, PR, release authority rules: {{PUBLISH_AUTHORITY}} (effective grants and consumption belong in sole state)
