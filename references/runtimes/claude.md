# Claude 运行时契约

依据 Anthropic 的 [Skills 文档](https://code.claude.com/docs/en/slash-commands) 与 [插件参考](https://code.claude.com/docs/en/plugins-reference)；事实复核日期：2026-08-20。

## 安装

Claude Code 用户级目录是 `$HOME/.claude/skills/delivery-harness`；项目级目录是 `<project>/.claude/skills/delivery-harness`。在本 Skill 仓库根执行与 Codex 相同的四项复制，只把目标根改成 `.claude/skills/delivery-harness`。

PowerShell：

```powershell
$target = Join-Path $HOME ".claude\skills\delivery-harness"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -LiteralPath ".\SKILL.md" -Destination $target -Force
foreach ($name in "agents", "assets", "references") {
  Copy-Item -LiteralPath ".\$name" -Destination $target -Recurse -Force
}
```

当前 Claude Code 插件格式也支持根目录只有一个 `SKILL.md` 的单 Skill 插件，不要求额外 `skills/` 包装层。本仓库形态可作为该插件的内容源；实际分发仍按 Claude Code 的插件安装与信任流程。不能确认本机版本支持时，使用上面的 standalone 复制路径。

## 发现与调用

新开 Claude Code 会话，输入：

```text
/delivery-harness 从当前现实开始，推进到已接受证据门通过。
```

项目需要自动载入时，把 [CLAUDE.block.template.md](../../assets/CLAUDE.block.template.md) 的固定块写入项目实际生效的 `CLAUDE.md`。Claude Code 可在会话中发现新 Skill，但版本更新和自动载入验证仍以全新会话为准。

## 到达验证

1. 核对目标四项清单和逐文件哈希。
2. 确认 `/delivery-harness` 出现在可用命令中并能显式执行。
3. 新建无上下文会话，检查启动固定块先于第一次工具调用。
4. 至少重复两次，记录 Claude Code 版本、成功数和失败数。

若只验证 `/delivery-harness` 能调用，不能推导 `CLAUDE.md` 自动载入已经生效。

## 更新

standalone 安装完整覆盖四项；插件安装按插件来源更新。保存旧副本或版本号，随后重开会话并复跑到达验证。Claude Code 的个人级 Skill 优先于项目级 Skill；插件 Skill 使用命名空间。更新时按实际来源逐项核对，不猜优先级。

## 卸载与回滚

standalone 安装只移除准确的 `delivery-harness` 目标目录；插件安装用 Claude Code 的插件卸载路径。若 `CLAUDE.md` 仍有入口块，同步移除或改写。回滚恢复完整旧副本或旧插件版本。

## 已知边界

- 单 Skill 根插件属于当前格式能力；不能拿当前文档替未经验证的旧版运行时作证明。
- Claude.ai 上传 Skill 与 Claude Code 本地 Skill 是不同部署面，分别验证。
- `agents/openai.yaml` 对 Claude 不构成配置；不要另造 `claude.yaml`。
- 自动载入是否生效只能由新会话顺序证据证明。
