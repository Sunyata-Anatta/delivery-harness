# Delivery Harness

`delivery-harness` 是一个面向复杂软件交付的 Agent Skill。它让 Agent 在已有授权内持续推进工作，并用项目状态、证据门和明确的停止条件约束每一次阶段转换。

它不是项目模板、任务管理系统或部署脚本。它不保存具体项目的业务事实、凭据、运行日志或开发记录。

中文说明；English guide: [README.en.md](README.en.md)。英文读者使用 Skill 时，应从 [英文路由索引](references/index.en.md) 进入。

## 适用场景

在 Agent 需要负责多阶段项目，并且需要把分析、设计、实施、排错、验证和交接保持一致时使用。典型触发包括：

- 继续一个已有项目，先以当前仓库和运行证据确认真实状态；
- 将已接受的目标推进至可验证的真实证据门；
- 协调多个 Agent、工具、外部服务或运行时，并保持权限边界；
- 对失败节点进行诊断、恢复、复验和记录，而不是仅报告失败。

## 发布内容

仓库根目录本身就是可安装的 Skill。发布包只包含以下四项：

```text
SKILL.md       执行规范和入口
agents/        Codex 界面元数据
assets/        项目覆盖层和自动载入块模板
references/    按任务读取的规则与运行时契约
```

不要把 `.git/`、项目状态、测试输出、评审材料、聊天记录或机器配置加入发布包。项目特有事实应放在被项目忽略的本地状态目录，而不是写回此通用 Skill。

## 安装

将上述四项完整复制到目标运行时名为 `delivery-harness` 的技能目录。不要只复制 `SKILL.md`，也不要在目标中保留第二份 `SKILL.md`。

常见用户级位置：

| 运行时 | 目标目录 |
|---|---|
| Codex | `$HOME/.agents/skills/delivery-harness` |
| Claude Code | `$HOME/.claude/skills/delivery-harness` |
| OpenClaw | 使用其 Git 或本地目录安装方式 |
| Hermes Agent | `$HOME/.hermes/skills/delivery-harness` |

不同运行时的发现、更新、卸载和验证方式见 [运行时安装与到达验证](references/runtime-installation.md)，再按其中的运行时链接操作。

## 调用与自动载入

安装只让运行时能够发现技能；它不保证每个项目自动载入。

- Codex：显式输入 `$delivery-harness`。
- Claude Code：显式输入 `/delivery-harness`。
- 项目希望在新会话自动载入时，将 [AGENTS 模板](assets/AGENTS.block.template.md) 或 [CLAUDE 模板](assets/CLAUDE.block.template.md) 的完整标记块写入实际生效的 `AGENTS.md` 或 `CLAUDE.md`。
- 受限或其他运行时使用 [通用入口模板](assets/restricted-runtime-entry.block.template.md)，并只写入该运行时确认会读取的指令面。

同名 Skill 可能来自多个位置。不要推测运行时会合并它们或优先选择最新副本；记录实际选择的路径，并在更新后新开会话验证。

## 验证与更新

每次安装或更新后，至少完成：

1. 对比源和目标的四项清单与逐文件哈希。
2. 确认运行时能列出或显式调用 `delivery-harness`。
3. 新开无上下文会话，确认启动回执先于首次工具调用。

完整的四级证据模型、更新和回滚规则在 [运行时安装与到达验证](references/runtime-installation.md)。文件存在不等于运行时读取；运行时可列出也不等于自动载入按时生效。

## 使用边界

Skill 规则的权威入口是 [SKILL.md](SKILL.md)。按任务渐进读取 `references/`，不要把所有参考文件无差别载入上下文。项目级状态和持久化边界使用 [项目覆盖层模板](assets/project-overlay.template.md)；阶段门、诊断、能力路由和外部集成由入口链接到相应参考文件。

不要把个人信息、主机名、令牌、私有地址或原始诊断值写入通用 Skill 或归档材料。诊断默认不落盘；需要归档时先脱敏。
