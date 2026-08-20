# Delivery Harness

[中文](README.md) | [English](README.en.md)

`delivery-harness` 是一个面向复杂软件交付的 Agent Skill。它让 Agent 在已有授权内持续推进工作，并用项目状态、证据门和明确的停止条件约束每一次阶段转换。

它不是项目模板、任务管理系统或部署脚本。它不保存具体项目的业务事实、凭据、运行日志或开发记录。

英文读者使用 Skill 时，从 [英文路由索引](references/en/index.md) 进入。

## 适用场景

在 Agent 需要负责多阶段项目，并且需要把分析、设计、实施、排错、验证和交接保持一致时使用。典型触发包括：

- 继续一个已有项目，先以当前仓库和运行证据确认真实状态；
- 将已接受的目标推进至可验证的真实证据门；
- 协调多个 Agent、工具、外部服务或运行时，并保持权限边界；
- 对失败节点进行诊断、恢复、复验和记录，而不是仅报告失败。

## 仓库与运行时载荷

repo 保留两份仓库说明文件：`README.md`（中文）和 `README.en.md`（English）。它们属于仓库发布面，必须随远端保留，但不是 Agent 执行 Skill 所需的运行时文件。

运行时 Skill 载荷由以下四项构成：

```text
SKILL.md       执行规范和入口
agents/        Codex 界面元数据
assets/        项目覆盖层、状态骨架和自动载入块模板
references/    按任务读取的规则与运行时契约
```

因此 repo 顶层是两份 README 加四项 Skill 载荷；安装到 Agent 时复制四项载荷即可。不要把 `.git/`、项目状态实例、测试输出、评审材料、聊天记录或机器配置加入 repo 或运行时载荷。项目特有事实不写回此通用 Skill。

## 项目状态契约

下游项目默认使用 `.delivery/`：

- `.delivery/state.md` 是活动状态唯一事实源，进入版本控制；记录活动节点、当次授权、已过证据门和待决断。
- `.delivery/uploads/`、`artifacts/`、`debug/` 默认忽略，不随交付分发。
- 稳定规则、命令、Resolver 和经验写入 [项目覆盖层模板](assets/project-overlay.template.md) 生成的项目覆盖层。

首次接入时复制 [`.delivery` 完整骨架](assets/delivery-skeleton.template.md)。其中 `state.md` 是随项目提交、随后持续填写的占位；骨架还包含忽略规则和三个空目录的可追踪占位。

本 Skill 源仓库是公开交付面：它自身的 `.delivery/` 只含开发测试、状态、评审和 case study，因此按项目特例留在本机、不进入发布历史。该特例不改变下游项目对 `state.md` 的默认版本控制规则。

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

语言控制使用 `language=auto|zh|en`。`auto` 首次按用户明确要求、项目会话锁定、用户消息主要语言、界面语言的顺序选择，并同时约束回复、参考文件和自动载入模板；代码、路径、命令、日志和引文不触发切换。

- Codex：显式输入 `$delivery-harness`。
- Claude Code：显式输入 `/delivery-harness`。
- 项目希望在新会话自动载入时，将与项目锁定语言一致的 [AGENTS 模板](assets/AGENTS.block.template.md) 或 [CLAUDE 模板](assets/CLAUDE.block.template.md) 的完整标记块写入实际生效的 `AGENTS.md` 或 `CLAUDE.md`；英文项目使用 `assets/en/` 中的同名模板。
- 受限或其他运行时使用 [通用入口模板](assets/restricted-runtime-entry.block.template.md)，并只写入该运行时确认会读取的指令面。

同名 Skill 可能来自多个位置。不要推测运行时会合并它们或优先选择最新副本；记录实际选择的路径，并在更新后新开会话验证。

## 验证与更新

每次安装或更新后，至少完成：

1. 对比源和目标的四项清单与逐文件哈希。
2. 确认运行时能列出或显式调用 `delivery-harness`。
3. 新开无上下文会话，确认启动回执先于首次工具调用。

完整的四级证据模型、更新和回滚规则在 [运行时安装与到达验证](references/runtime-installation.md)。文件存在不等于运行时读取；运行时可列出也不等于自动载入按时生效。

## 使用边界

Skill 规则的权威入口是 [SKILL.md](SKILL.md)。按任务渐进读取 `references/`，不要把所有参考文件无差别载入上下文。节点执行细节见 [节点执行参考](references/execution.md)；阶段门、诊断、能力路由和外部集成由入口链接到相应参考文件。

不要把个人信息、主机名、令牌、私有地址或原始诊断值写入通用 Skill 或归档材料。诊断默认不落盘；需要归档时先脱敏。
