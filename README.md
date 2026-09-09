# Delivery Harness

[中文](README.md) | [English](README.en.md)

`delivery-harness` 是面向多阶段交付的 Agent Skill：在已有授权内持续推进，以当前项目状态、真实证据和明确门控决定下一步。专业 Skill、MCP 和 CLI 负责具体工作，Harness 负责目标、授权、状态与验证的一致性。

## 如何加载

启动只需要短入口、`SKILL.md` 与选定语言的核心。详细执行、安装、发布和提供者说明，走到对应动作时再读。

| 层 | 内容 | 何时读取 |
|---|---|---|
| 原生启动块 | 回执格式、未知事实待探测、核心入口 | 新会话首次工具前 |
| 单语言核心 | 唯一活动状态、动作路由、始终有效的边界 | Skill 调用时 |
| 动作规则 | 节点、证据、提交、部署、排错 | 对应事件发生前 |
| 提供者与项目详情 | 安装方法、Resolver、历史证据 | 当前选择确实需要时 |

`language=auto|zh|en` 按显式选择、项目会话锁定、消息主语言、界面语言判定；代码和日志不触发切换。只读一种语言的核心和参考。英文使用 [English core](references/en/core.md)。

预算按 `o200k_base` 计 Harness 自身文本：启动块 ≤250 tokens，SKILL + 单语言核心 ≤1000，活动状态 ≤600，覆盖层启动摘要 ≤450，普通启动合计 ≤2300。宿主已注入的技能目录、工具清单与其他全局规则另计；预算不承诺整场对话的节省比例或旧内容自动卸载。详见 [预算与验证合同](references/runtime-installation.md)。

## 接入项目

| 场景 | 做法 |
|---|---|
| 临时问答、小任务 | 会话内执行，不创建状态目录 |
| 新项目 | 默认 `.delivery/state.md`、覆盖层和证据槽 |
| 已有治理项目 | 保留原规则，声明唯一状态指针与字段映射，不双写 |
| 受限运行时 | 使用显式调用，登记缺失的预注入能力 |
| 自举开发 | 当前安装基线治理候选修改；新版本验证后才同步 |

`.delivery/state.md` 默认进入版本控制；明确的隐私偏离需登记恢复与验证方式。`uploads/`、`artifacts/`、`debug/` 默认忽略。首次接入按 [安全初始化](references/project-initialization.md) 使用 [完整骨架](assets/delivery-skeleton.template.md) 和 [覆盖层模板](assets/project-overlay.template.md)，已有内容增量合并。

本仓库自身的 `.delivery/` 保存合法的自举开发状态、计划、测试与审阅，按公开分发边界留在本地。伴随案例研究有独立目标与记录，只通过结论引用关联。

## 能力分组与路由

候选组为 `research`、`engineering`、`verification`、`documents`、`operations`、`domain`；组只缩小选择范围，不整组加载正文。`profile=auto|research|develop|review|document|operate` 调整候选顺序，不扩大权限。

先筛任务、目录、语言、离线、数据和授权约束，再按“当前用户选择 > 最具体目录绑定 > 项目 Resolver > 用户偏好 > profile > 新候选”选择。只读取所选提供者；失败按已配置顺序回退，缺失必需能力保持证据门失败。Skill、插件、MCP、CLI 分别记录来源与验证。

配置沿用项目覆盖层 Resolver；长表可移到唯一 `.delivery/routing.md`，覆盖层保留指针。新技能经过来源/兼容性检查和小任务验证后加入候选，无需修改 Harness 核心。临时选择不自动变成全局默认，同名来源冲突不能静默选择。换 Agent 后重新验证工具与认证。

例如，为某个子目录绑定离线审阅能力：

| 条件 | 必需能力 | 有序候选 | 验证/回退 |
|---|---|---|---|
| packages/api/** | review | 已验证本地 reviewer Skill > 人工审阅 | 找出已知缺陷；均不满足则阻塞审阅门 |

完整字段、接入步骤与限制见 [能力路由](references/capability-routing.md) 和 [配置合同](references/routing-configuration.md)。

## 安装与调用

运行时 Skill 载荷只有四项，完整复制到目标名为 `delivery-harness` 的目录：

```text
SKILL.md       语言选择与核心入口
agents/        Codex 界面元数据
assets/        状态、覆盖层和原生启动块模板
references/    单语言核心、动作规则与运行时说明
```

`README.md`、`README.en.md` 是仓库说明文件；`.gitattributes`、`.gitignore` 是版本化仓库基础设施。这四份随仓库发布，不属于运行时 Skill 载荷。`.git/`、开发状态、测试、原始日志和机器配置不随技能分发。

| 运行时 | 常用用户级安装面 | 显式调用 |
|---|---|---|
| Codex | `$HOME/.agents/skills/delivery-harness` | `$delivery-harness` |
| Claude Code | `$HOME/.claude/skills/delivery-harness` | `/delivery-harness` |
| Hermes Agent | `$HOME/.hermes/skills/delivery-harness` | `/delivery-harness`；CLI 可用 `hermes chat --skills delivery-harness` 预载 |
| OpenClaw / 其他 Agent Skills 主机 | 运行时声明的安装器或目录 | 按原生帮助确认 |

需要预注入时，将 [AGENTS.md 启动块](assets/AGENTS.block.template.md)、[CLAUDE.md 启动块](assets/CLAUDE.block.template.md) 或 [其他入口块](assets/restricted-runtime-entry.block.template.md) 写入实际生效的原生指令面；保留其他用户规则，只替换同名标记块。安装目录存在、隐式调用元数据和完整启动合同是不同条件。

没有预注入时，显式冷调用允许先读 Skill 和核心，再输出回执，再用业务工具；该结果不能计为“回执先于所有工具”的预注入通过。不同运行时的路径、信任、优先级和卸载方式见 [运行时合同](references/runtime-installation.md)。

## 验证、更新与边界

更新前备份完整旧载荷与入口；更新后比较精确文件集合及逐文件哈希，再做结构检查、真实显式调用和全新会话验证。清理废弃文件前核对目标范围，不能只覆盖新文件便宣称集合一致。

每个声称预注入有效的运行时至少验证 5 次全新会话：回执先于首工具、实际加载来源正确、真实任务成功；另测冷调用、缺失能力与规则冲突。结构测试、文件存在、退出码 0 都不能单独证明这些行为。不可达运行时及账号/托管面分别登记未验证。

恢复时只读取当前状态摘要和所需来源。收到新证据先登记回执；提交、全局安装、外发、部署与发布按各自动作类别核对授权。独立审阅发现必须修复重审；审阅后交付物改变使旧审阅失效。Markdown 规则依赖 Agent 遵循，确定性阻断仍应由宿主权限与实际执行入口提供。

执行细则见 [节点合同](references/execution.md)、[门控](references/gates.md) 与 [Agent/模板职责](references/agent-config.md)。通用技能不保存项目秘密或机器事实；诊断默认不落盘，归档前脱敏。
