# {{PROJECT_NAME}} Delivery Overlay

Store project facts only. This overlay may tighten Delivery Harness but cannot override system, safety, or user instructions. Remove unused entries.

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
- Process record: {{PROCESS_RECORD_PATH}} (default `.delivery/process.md`; read by date/topic. Keep adoption and conformance receipts; append findings, error details, improvement intent, options/choice and supporting data at the commit gate. State its location when outside the delivery surface)
- Existing-state adapter: {{STATE_FIELD_MAPPING_WRITER_AUTHORITY_VERIFY_RECOVERY}} (node/authority/evidence/decision fields, writer and authority, verification and recovery; no additional active state)

## Storage
Root: `.delivery/`
- Active state: use the sole pointer above; version by default, with recovery location and verification for privacy deviations
- `uploads/`: approved short-term user inputs, unchanged
- `artifacts/`: one-off outputs and temporary evidence
- `debug/`: temporary debugging output and reproduction material
For the default layout, follow the installed Skill's initialization reference and copy the full `.delivery` skeleton. With an existing-state adapter, skip default state creation. Durable specifications, evidence reports and fixtures use project-semantic locations, created only when content exists; sensitive originals stay in approved restricted storage.
Deviations: {{STORAGE_DEVIATIONS}}

## Project rules
- Required: {{PROJECT_MUST_RULE}}
- Forbidden: {{PROJECT_MUST_NOT_RULE}}
- Conventions: {{PROJECT_CONVENTIONS}}
- Data/privacy: {{DATA_RULES}}

## Startup summary

Keep only outcome, references to source fields, profile and hard constraints; target <=450 tokens. Define rule/state/navigation/process paths above only. Read long details for the current action; budgets never remove necessary safety or acceptance clauses.
- profile: `auto` (research/develop/review/document/operate adjust candidates only)
- Routing source: this Resolver; move long detail to `.delivery/routing.md` and remove duplicate tables
- Conformance: check applicable clauses before actions; at transitions, rule/path changes or validation failures follow the Harness execution contract. Current conclusions go to sole state, detailed receipts to the process record

## Resolver
| Condition | Skill/tool/process | Evidence | Fallback | Verification | Revisit when | Last verified |
|---|---|---|---|---|---|---|
| {{CONDITION}} | {{ROUTE}} | {{EVIDENCE}} | {{FALLBACK}} | `{{VERIFY_COMMAND}}` | {{REVISIT_WHEN}} | {{DATE}} |

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
- Preauthorized: {{PREAUTHORIZED_ACTION}}
- Tool mode: preauthorized set `{{PREAUTHORIZED_TOOLS}}` / individual approval
- Explicit approval required: {{APPROVAL_REQUIRED_ACTION}}
- Forbidden: {{FORBIDDEN_ACTION}}

## Integrations and credentials
| Integration | Purpose | Entry | Owner | Scope | Verification | Data boundary | Rollback |
|---|---|---|---|---|---|---|---|
| {{INTEGRATION}} | {{PURPOSE}} | {{CONNECTOR_CLI_OR_BROWSER}} | {{OWNER}} | {{SCOPES}} | `{{VERIFY_COMMAND}}` | {{DATA_BOUNDARY}} | {{ROLLBACK}} |

Never store tokens, passwords, private keys, or reusable authentication here.

## Distribution surface registry

Register every path, installer, account-synchronized surface, or hosted entry that receives the project artifact. Keep unknown or unreachable surfaces explicitly unverified; success on one surface cannot prove another is updated.

| Surface | Resolver or address | Update method | Canonical source | Evidence level | Last verified | Status and limits | Rollback |
|---|---|---|---|---|---|---|---|
| {{DISTRIBUTION_SURFACES}} | {{SURFACE_RESOLVER_OR_ADDRESS}} | {{SURFACE_UPDATE_METHOD}} | {{CANONICAL_SOURCE}} | {{EVIDENCE_LEVEL}} | {{DATE}} | {{STATUS_AND_LIMITS}} | {{ROLLBACK}} |

## Real-evidence gate definitions
| Phase | Evidence | Sample/environment | Pass criteria | Unblock condition |
|---|---|---|---|---|
| {{PHASE}} | {{EVIDENCE}} | {{SAMPLE_OR_ENVIRONMENT}} | {{PASS_CRITERIA}} | {{UNBLOCK_CONDITION}} |

## Evidence artifacts
| Artifact | Location/access | Processing | Conclusion/limits | Reviewed on |
|---|---|---|---|---|
| {{ARTIFACT}} | {{LOCATION_AND_ACCESS}} | {{PROCESSING}} | {{CONCLUSION_AND_LIMITS}} | {{REVIEWED_ON}} |

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
- Last scan / history decision: {{LAST_SECRET_SCAN_RESULT}} / {{HISTORY_PRIVACY_DECISION}}
- Push, PR, release authority: {{PUBLISH_AUTHORITY}}

## Risks and blocks
| Date | Risk/block | Impact | Evidence | Owner | Unblock condition |
|---|---|---|---|---|---|
| {{DATE}} | {{RISK_OR_BLOCKER}} | {{IMPACT}} | {{EVIDENCE}} | {{OWNER}} | {{UNBLOCK_CONDITION}} |

## Evidence-based lessons
| Date | Context | Attempt | Evidence | Lesson | Guardrail | Revisit when |
|---|---|---|---|---|---|---|
| {{DATE}} | {{CONTEXT}} | {{ATTEMPT}} | {{EVIDENCE}} | {{LESSON}} | {{GUARDRAIL}} | {{REVISIT_WHEN}} |
