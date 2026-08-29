# GitHub Capability Checks and Complete CLI Flow

Read this file for GitHub repository creation, remote binding, push, PR, or release.

## Contents

- [Check three capabilities separately](#check-three-capabilities-separately)
- [Report attempts before declaring a block](#report-attempts-before-declaring-a-block)
- [Hard redaction rules for Git actions](#hard-redaction-rules-for-git-actions)
- [Complete gh CLI flow](#complete-gh-cli-flow-powershell)
- [Common failure decisions](#common-failure-decisions)

## Check three capabilities separately

- **GitHub connector or plugin:** connection proves only access to authorized resources. Repository, file, branch, or PR creation depends on exposed tools.
- **`gh` CLI:** uses an independent local credential. A connected plugin does not prove `gh` is authenticated.
- **Browser:** uses the user's browser login state. CLI failure never authorizes an automatic switch; obtain explicit permission first.

Prefer a dedicated connector that exposes the required action. When it lacks the action, report the capability gap and then enter the CLI flow.

## Report attempts before declaring a block

Include at least:

```text
Attempted: <connector/API/CLI and exact action>
Result: <success, error code, or action not exposed>
Confirmed: <connection, capability, and authentication state separately>
Block: <only remaining block>
Next: <complete recovery path and the user's required action>
```

Example:

```text
Attempted: inspect the GitHub connector for repository-write tools.
Result: plugin connected and can operate existing repositories, but exposes no create-repository action.
Attempted: gh auth status.
Result: a local account exists, but its token is invalid with HTTP 401.
Conclusion: plugin connection works; repository creation is unavailable; CLI needs independent reauthentication.
Next: complete gh login, then create the repository, bind origin, push, and verify.
```

Never report only “GitHub is not logged in” or “plugin unavailable.”

## Hard redaction rules for Git actions

Before `git commit`, repository creation, push, PR, or release, follow [gates.md](gates.md) and scan worktree, staged set, and full Git history. Include private keys, tokens, passwords, cloud credentials, connection strings, authentication files, session information, real personal data, and machine-specific paths.

Hard rules:

1. No commit, remote creation, or push before redaction checks pass.
2. Never echo secret values in command output, reports, commit messages, or patches.
3. When a potentially live secret is found, revoke or rotate it before cleaning files.
4. A normal fix commit cannot remove historical secrets. Choose history rewrite, a clean root, or a new repository.
5. History rewrite, deleting remote refs, and force-push need separate authority, after backup, collaborator impact, reclone requirement, and verification are explained.
6. Rescan current content, every local branch, and every tag after cleanup. Only then create a new commit.

When no scanner is available, do not skip. Degrade to read-only repository search and Git-object inspection and report coverage limits. Public usernames and repository URLs are not credentials; anonymization depends on the publication boundary.

## Complete `gh` CLI flow (PowerShell)

### 1. Check tool, local repository, and authentication

```powershell
gh --version
git status --short
git branch --show-current
git remote -v
gh auth status
```

Record account, branch, dirty worktree, and existing remote. Never overwrite an existing remote silently.

### 2. Reauthenticate

For an invalid token or signed-out CLI:

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh auth status
gh api user --jq .login
```

When a headless environment stalls at Enter or device-code interaction, report the waiting state immediately. Switch to a visible interactive terminal only after user permission; never silently use browser login state.

Only when `gh auth login` cannot recover and the user explicitly authorizes forgetting the old credential:

```powershell
gh auth logout --hostname github.com --user <owner>
gh auth login --hostname github.com --git-protocol https --web
```

### 3. Confirm target and visibility

```powershell
$owner = gh api user --jq .login
$repo = "your-repository"
gh repo view "$owner/$repo"
```

Create only after `gh repo view` proves absence. Default to `--private`; public visibility or an open-source license requires explicit intent.

### 4A. No `origin`: create, bind, and push

```powershell
$branch = git branch --show-current
gh repo create "$owner/$repo" --private --source . --remote origin --push
git push -u origin $branch
```

When `gh repo create --push` already confirms upstream, the second push is an idempotent verification and may be omitted.

### 4B. Create remote, then bind manually

Use this when each state transition needs separate observation:

```powershell
$branch = git branch --show-current
gh repo create "$owner/$repo" --private
git remote add origin "https://github.com/$owner/$repo.git"
git push -u origin $branch
```

### 4C. Existing `origin`

Inspect first:

```powershell
git remote get-url origin
```

When the existing remote must remain:

```powershell
git remote rename origin previous-origin
git remote add origin "https://github.com/$owner/$repo.git"
git push -u origin (git branch --show-current)
```

Replace only with explicit user permission:

```powershell
git remote set-url origin "https://github.com/$owner/$repo.git"
git push -u origin (git branch --show-current)
```

### 5. Verify remote result

```powershell
gh repo view "$owner/$repo" --json nameWithOwner,visibility,url,defaultBranchRef
git remote -v
git status --short
git log -1 --oneline
```

Claim completion only after remote metadata, default branch, remote URL, and commit match the accepted target.

## Common failure decisions

- **Plugin connected, no repository-creation tool:** plugin works but capability is insufficient; use CLI or ask the user to create an empty repository.
- **Plugin returns 404 for a newly created private repository:** use authenticated CLI to prove the repository exists. If it does, the GitHub App lacks that repository scope; ask the user to authorize the repository and reverify.
- **`gh auth status` returns 401:** CLI credential is invalid. Follow authentication recovery; plugin connection is not counter-evidence.
- **Repository name exists:** confirm it is the target. Never rename or overwrite automatically.
- **`origin` exists:** preserve and rename it, or replace only after explicit approval.
- **Push rejected:** inspect authority, branch protection, and unrelated remote history; never force-push.
- **Browser may be logged in:** optional fallback only after explicit permission.
