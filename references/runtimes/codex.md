# Codex 运行时契约

依据 OpenAI 的 [Agent Skills 文档](https://developers.openai.com/codex/skills)；事实复核日期：2026-08-20。

## 安装

用户级目标是 `$HOME/.agents/skills/delivery-harness`。项目级目标是从工作目录向仓库根可发现的 `.agents/skills/delivery-harness`。

PowerShell（在本 Skill 仓库根执行）：

```powershell
$target = Join-Path $HOME ".agents\skills\delivery-harness"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -LiteralPath ".\SKILL.md" -Destination $target -Force
foreach ($name in "agents", "assets", "references") {
  Copy-Item -LiteralPath ".\$name" -Destination $target -Recurse -Force
}
```

POSIX shell：

```bash
target="$HOME/.agents/skills/delivery-harness"
mkdir -p "$target"
cp SKILL.md "$target/"
cp -R agents assets references "$target/"
```

不要把本仓库复制到 `$CODEX_HOME/skills` 作为新的默认方案；当前通用发现路径是 `.agents/skills`。

## 发现与调用

启动一个新 Codex 会话，查看技能列表或输入：

```text
$delivery-harness 从当前现实开始，推进到已接受证据门通过。
```

项目需要自动载入时，把 [AGENTS.block.template.md](../../assets/AGENTS.block.template.md) 的固定块追加到项目实际生效的 `AGENTS.md`。Codex 不合并同名 Skill，多个来源可以同时出现在选择器中；验证时必须记录实际选择的路径。修改后开新会话复验。

## 到达验证

1. 核对目标目录四项清单和逐文件哈希。
2. 确认 Codex 能列出或显式调用 `delivery-harness`。
3. 新建无上下文会话，在第一次工具调用前检查 `【启动回执】` 和 `【能力信号评估】`。
4. 至少重复两次，并记录成功数、失败数和 Codex 版本。

只有目录存在，没有运行时发现结果，不算安装成功。

## 更新

先保存目标目录哈希或副本，再用安装命令完整覆盖四项。重新启动会话，重复到达验证。项目级同名副本存在时，也要同步或在选择器中核对实际路径，不能假设运行时会合并或自动选中较新的副本。

## 卸载与回滚

移除准确目标目录；不要递归操作 `.agents/skills` 上级目录。回滚时恢复完整副本，重开会话并复验。若项目 `AGENTS.md` 仍含自动载入块，同时移除或改写该块。

## 已知边界

- 运行中的会话可能缓存技能；更新后以新会话为准。
- `agents/openai.yaml` 是 OpenAI 界面元数据，不是其他运行时的入口文件。
- 同名 Skill 可能同时出现且不会合并；跨项目结果不能相互代替。
- ChatGPT 中 Skill 的可用面与 Codex 本地发现路径不是同一个部署面，分别验证。
