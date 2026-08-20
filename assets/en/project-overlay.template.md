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
- Active state: `.delivery/state.md` (single source of truth)

## Storage
Root: `.delivery/`
- `.delivery/state.md`: active node, session authority, passed evidence gates, and pending decisions; version controlled
- `uploads/`: immutable user inputs
- `artifacts/`: generated and evidence artifacts
- `debug/`: essential reproduction/debug files
On first setup, follow the installed Skill's project-initialization reference and copy the complete `.delivery` skeleton; do not create empty directories that Git cannot record.
Deviations: {{STORAGE_DEVIATIONS}}

## Project rules
- Required: {{PROJECT_MUST_RULE}}
- Forbidden: {{PROJECT_MUST_NOT_RULE}}
- Conventions: {{PROJECT_CONVENTIONS}}
- Data/privacy: {{DATA_RULES}}

## Resolver
| Condition | Skill/tool/process | Evidence | Fallback | Verification | Revisit when | Last verified |
|---|---|---|---|---|---|---|
| {{CONDITION}} | {{ROUTE}} | {{EVIDENCE}} | {{FALLBACK}} | `{{VERIFY_COMMAND}}` | {{REVISIT_WHEN}} | {{DATE}} |

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
