# GitHub Capability and CLI Workflow

Read this for repository creation, remote binding, push, PR, or release.

## Separate capabilities

GitHub connector access, `gh` authentication, and browser login are separate facts. Prefer a purpose-built connected action when exposed; otherwise report the capability gap before using CLI. Never switch to browser state without permission.

Before claiming a block, report every attempted client/action, exact result or code, confirmed connection/capability/authentication state, sole remaining block, and full recovery path.

## Mandatory safety gate

Before commit or any remote action, apply [gates.md](gates.md) to worktree, staged content, all refs, and commit identities. A failed redaction scan blocks commit and publication. Normal commits cannot remove historical secrets; rewrite, ref deletion, and force-push require separate authority, backup, collaborator-impact notice, and post-cleanup rescan.

## CLI sequence

1. Inspect `gh --version`, Git status/branch/remotes, and `gh auth status`.
2. If needed, authenticate with the current official `gh auth login` flow, then verify account separately. Interactive/browser authentication requires user participation.
3. Confirm owner, repository identity, existence, and visibility. Default new repositories to private unless public visibility is explicitly accepted.
4. Preserve an existing `origin`. Do not overwrite or rename it unless the intended target is confirmed; never force-push to solve unrelated history.
5. Push the selected branch only with authority.
6. Verify repository identity/visibility/default branch, remote URLs, local status, and remote commit.

Distinguish missing connector action, expired CLI credential, repository access scope, name collision, protected branch, and unrelated remote history. Report the specific case; do not collapse them into “GitHub unavailable.”
