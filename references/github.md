# GitHub 能力检查与完整 CLI 流程

涉及 GitHub 仓库创建、远端绑定、推送、PR 或发布时读取本文件。

## 目录

- [分开检查三种能力](#分开检查三种能力)
- [阻塞前必须报告尝试](#阻塞前必须报告尝试)
- [Git 环节脱敏硬规则](#git-环节脱敏硬规则)
- [完整 gh CLI 流程](#完整-gh-cli-流程powershell)
- [常见失败判断](#常见失败判断)

## 分开检查三种能力

- **GitHub 连接器或插件**：连接状态只证明它能访问已授权资源。能否创建仓库、文件、分支或 PR，以当前暴露的工具为准。
- **`gh` CLI**：使用独立的本机凭据。插件已连接不能证明 `gh` 已登录。
- **浏览器**：使用用户浏览器的登录态。CLI 失败后不能自动切换，必须先得到用户明确允许。

优先使用能完成任务的专用连接器。连接器缺少目标动作时，报告能力缺口，再进入 CLI 流程。

## 阻塞前必须报告尝试

至少给出：

```text
已尝试：<连接器/API/CLI 与具体动作>
结果：<成功、错误码或未暴露该动作>
已确认：<连接状态、能力边界、认证状态分别是什么>
阻塞：<唯一剩余阻塞>
下一步：<完整恢复路径及需要用户完成的动作>
```

示例：

```text
已尝试：检查 GitHub 连接器的仓库写工具。
结果：插件已连接，可操作已有仓库，但未暴露 create-repository 动作。
已尝试：gh auth status。
结果：本机账号存在，但令牌失效，HTTP 401。
结论：插件连接正常；建库能力缺失；CLI 需独立重新认证。
下一步：完成 gh 登录，然后创建仓库、绑定 origin、推送并验证。
```

不得只说 `GitHub 未登录` 或 `插件不可用`。

## Git 环节脱敏硬规则

任何 `git commit`、建库、推送、PR 或发布之前，先按 [gates.md](gates.md) 扫描工作树、暂存区和完整 Git 历史。至少检查私钥、令牌、密码、云凭据、连接串、认证文件、会话信息、真实个人信息和机器专属路径。

硬规则：

1. 脱敏扫描未通过，不得执行 git commit，也不得创建远端或推送。
2. 不在命令输出、报告、提交信息或修复补丁中回显秘密值。
3. 发现可能有效的秘密，先撤销或轮换，再清理文件。
4. 普通修复提交不能清除历史中的秘密。历史已污染时，选择历史重写、干净的新根提交或新仓库。
5. 历史重写、删除远端引用和强制推送必须单独授权。先说明备份、协作者影响、重新克隆要求和验证方式。
6. 清理后重新扫描当前内容、全部本地分支与标签。只有复扫通过，才创建全新提交。

扫描器不可用时，不得跳过。用只读仓库搜索和 Git 对象检查降级，并报告覆盖限制。公开用户名和公开仓库地址不是凭据；是否匿名化由项目发布范围决定。

## 完整 `gh` CLI 流程（PowerShell）

### 1. 检查工具、本地仓库和认证

```powershell
gh --version
git status --short
git branch --show-current
git remote -v
gh auth status
```

记录账号、当前分支、脏工作区和现有远端。不要覆盖用户已有远端。

### 2. 重新认证

令牌无效或未登录时：

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh auth status
gh api user --jq .login
```

如果无界面执行环境卡在 `按 Enter` 或设备码步骤，立即报告等待状态。经用户允许后改在可见交互终端执行；不得悄悄换用浏览器登录态。

只有 `gh auth login` 无法修复且用户明确同意清除旧凭据时，才执行：

```powershell
gh auth logout --hostname github.com --user <owner>
gh auth login --hostname github.com --git-protocol https --web
```

### 3. 确认目标与可见性

```powershell
$owner = gh api user --jq .login
$repo = "your-repository"
gh repo view "$owner/$repo"
```

`gh repo view` 返回不存在后才能创建。默认使用 `--private`；改为 `--public` 或添加开源许可证前必须确认公开和授权意图。

### 4A. 当前仓库没有 `origin`：创建、绑定并推送

```powershell
$branch = git branch --show-current
gh repo create "$owner/$repo" --private --source . --remote origin --push
git push -u origin $branch
```

`gh repo create --push` 已成功设置上游时，第二条 `git push` 是幂等验证；若输出确认已设置，可省略。

### 4B. 先创建远端，再手动绑定

适用于需要分开观察每个状态转换的场景：

```powershell
$branch = git branch --show-current
gh repo create "$owner/$repo" --private
git remote add origin "https://github.com/$owner/$repo.git"
git push -u origin $branch
```

### 4C. 已存在 `origin`

先检查目标：

```powershell
git remote get-url origin
```

如果 `origin` 是必须保留的其他远端，不要覆盖：

```powershell
git remote rename origin previous-origin
git remote add origin "https://github.com/$owner/$repo.git"
git push -u origin (git branch --show-current)
```

只有用户明确要求替换现有 `origin` 时才使用：

```powershell
git remote set-url origin "https://github.com/$owner/$repo.git"
git push -u origin (git branch --show-current)
```

### 5. 验证远端结果

```powershell
gh repo view "$owner/$repo" --json nameWithOwner,visibility,url,defaultBranchRef
git remote -v
git status --short
git log -1 --oneline
```

只有远端元数据、默认分支、远端 URL 和提交均符合预期后，才能声称建库与推送完成。

## 常见失败判断

- **插件连接、无建库工具**：插件正常但能力不足；使用 CLI 或让用户先建立空仓库。
- **插件对新建私有仓库返回 404**：先用已认证 CLI 验证仓库是否真实存在；若存在，说明 GitHub App 尚未获该私有仓库的访问范围，不得误报建库失败。提示用户在 GitHub App 设置中授权该仓库后再复核。
- **`gh auth status` 返回 401**：CLI 凭据失效；按认证流程恢复，不能引用插件连接状态作为反证。
- **仓库名已存在**：先确认是否为目标仓库；不要自动改名或覆盖。
- **`origin` 已存在**：保留并改名，或取得用户明确同意后替换。
- **推送被拒绝**：检查权限、分支保护、远端是否已有不相关历史；不要强推。
- **浏览器可能已登录**：这只是可选回退；先取得用户明确允许。
