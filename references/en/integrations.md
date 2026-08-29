# External Integrations

Delivery Harness can guide GitHub, database, deployment platform, knowledge base, and other external setup only when the active node needs it. It discovers, explains, verifies, and resumes; it never silently expands authority.

## Default decision

GitHub is not a hard dependency, and no optional service belongs in generic Agent metadata. The same Skill must work for local, offline, and differently hosted projects.

Declare a connector as hard dependency only when the core flow cannot work without it. When a project merely chooses a service, record configuration and authority in the project overlay.

## Scope of automatic guidance

Harness may automatically:

- inspect exposed connectors, CLIs, project configuration, and read-only state;
- check whether an action exists and whether that client is authenticated;
- use official sources to provide installation, login, scope, and verification steps;
- perform reversible project-level configuration within existing authority; and
- reverify capability after setup and resume from the failed node.

Harness must not silently install a global plugin, Skill, Hook, or trusted program, and must not silently authenticate an account. It must not request or echo secrets, enable paid services, expand scopes, use browser login state, alter organization settings, or change persistent machine configuration unless the user explicitly authorized that action.

## Select a capability

Choose the smallest sufficient capability in this order:

1. Existing local project capability.
2. Installed and authorized dedicated connector.
3. Installed and independently authenticated CLI.
4. Browser interaction after explicit user permission.

Connector connected, CLI logged in, and browser logged in are three separate facts. One cannot prove another.

## Output when blocked

Attempt allowed checks before reporting:

```text
Attempted: <capability and exact action>
Result: <success, error code, missing action, or missing authority>
Confirmed: <connection, capability, and authentication state separately>
Block: <only remaining block>
Next: <complete setup or recovery path and the user's required action>
```

When the user must install or authenticate, provide the path from installation through final verification. Do not give one isolated command, and do not describe an untried route as unavailable.

## Project record

Record in the project overlay:

- integration name and purpose;
- connector, CLI, or browser entry;
- account or resource owner without secrets;
- granted capability and scope;
- configuration source, version, and verification command;
- whether data leaves the machine or organization boundary;
- cost, rollback, and revisit condition.

For GitHub authentication, repository creation, remote binding, push, and private-repository authority, read [github.md](github.md).
