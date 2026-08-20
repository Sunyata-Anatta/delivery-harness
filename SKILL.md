---
name: delivery-harness
description: Use when an agent is asked to own a complex multi-stage software project, keep plans and implementation aligned, continue without repeated confirmation, research changing tools, or stop only at material decisions, authority boundaries, and real-world evidence gates.
---

# Delivery Harness

> **English readers:** Chinese rules are authoritative. Start with the operational [English routing index](references/en/index.md), then load only English references required by the active task.

在授权、决策和证据边界内，把已接受项目持续推进到可验证完成。Harness 维护一个活动节点、一份项目状态、清晰权限和可核验阶段门；专业 Skill 负责具体设计、调研、实现、测试、排错和部署。

## 语言与载入

控制项是 `language=auto|zh|en`，默认 `auto`：

- 判定优先级：用户显式指定 > 会话已锁定语言 > 当前用户消息主要语言 > 会话界面语言。
- 首次确定后按项目锁定；用户显式切换或首次触碰另一项目时重判。
- 代码、路径、命令、日志或引文不参与语言判定。
- 选定语言同时约束回复、参考路径、README 链接和自动载入模板；同一项目不重复载入两种语言。
- 中文会话读本页与中文参考；英文会话从 [English index](references/en/index.md) 进入，只读英文参考。
- 中文是规范源；冲突时执行中文，并把英文差异作为同一变更必须修补的缺陷。

## 按任务路由

- 节点执行细节：[execution.md](references/execution.md)
- 项目首次接入或合并已有 `.delivery/`：[project-initialization.md](references/project-initialization.md)
- 状态转换、授权、发布和证据门：[gates.md](references/gates.md)
- 启动或节点失败：[principles.md](references/principles.md)
- 诊断、恢复或重试：[debugging.md](references/debugging.md)
- 运行时安装、更新、卸载和到达验证：[runtime-installation.md](references/runtime-installation.md)
- 可选能力选择：[capability-routing.md](references/capability-routing.md)
- Agent 职责与委派：[agent-config.md](references/agent-config.md)
- 连接器、CLI、账号和外部服务：[integrations.md](references/integrations.md)
- GitHub：[github.md](references/github.md)

按活动节点和当前动作点读，不预载无关参考。可选能力不是硬依赖；不可用时可采用其原则，但不得声称已调用。

## 会话启动

载入单位是项目。会话开始且工作目录是已识别项目，或动作首次落到另一项目根时，按顺序载入：

1. 项目规则与项目覆盖层。
2. 分支、HEAD、工作树和本次生效的提交身份。
3. 可达能力、运行环境与权限边界。
4. `.delivery/state.md` 中的上次结论、活动节点、授权和证据门。
5. 文档更新面。
6. 运行时实际读取的自动载入块；缺则嵌入，有则核对，更新则整块替换。

**第一条回复必须是启动产出固定块**，出现在任何工具调用之前。按已锁定语言选择下列等效模板；未输出不得开始工具调用。

```text
【启动回执】
规则：<项目规则与覆盖层，一句话>
版本控制：<分支/HEAD 与生效提交身份>
节点：<活动节点与下一道门>
边界：<沙箱/权限/工具限制，一句话>
【能力信号评估】
<每个能力：触发或未触发+理由>
```

```text
【Startup Receipt】
Rules: <project rules and overlay, one sentence>
Version control: <branch/HEAD and effective commit identity>
Node: <active node and next gate>
Boundary: <sandbox/authority/tool limits, one sentence>
【Capability Signal Assessment】
<every capability: triggered or not triggered plus reason>
```

取不到分支、HEAD 或节点时写“待探测”/“pending probe”，回执后立即用判据命令补报。缺规则则问；缺提交身份可继续但不得提交；缺上次结论则从活文件重建；缺环境事实先只读探测。

回执先于首次工具调用是验收判据。自动载入层超预算时先丢文档更新面，再丢上次结论；不丢规则、版本控制事实和环境边界。

## 项目状态

默认存放根是 `.delivery/`。`state.md` 是活动状态的唯一事实源并进入版本控制；只写活动节点、当次授权、已过证据门和待决断。稳定项目事实、命令、规则、Resolver 和经验写项目覆盖层。`uploads/`、`artifacts/`、`debug/` 默认忽略，不随交付分发。首次接入复制完整的 [`.delivery` 骨架](assets/delivery-skeleton.template.md)；项目可在覆盖层改存放根并登记偏离。

阶段顺序：

```text
reality_audit
  -> requirements
  -> tool_research
  -> solution_decision
  -> design_and_plan
  -> environment_and_authority
  -> repository_integration
  -> tdd_nodes
  -> real_evidence
  -> release_or_handoff
```

每次转换：

1. 用新证据验证当前门。
2. 更新 `state.md`，只保留一个活动节点。
3. 提交前同步本次事实涉及的规格、计划、规则、经验、Resolver、README 和对照语言版本。
4. 本地提交已获授权时，提交最小完整变更。
5. 下一动作仍在范围内且无停止条件时继续。

改变事实后，用旧说法全仓检索并处理每个命中。文档更新是检查点，不是停止点；交接只写一次性上下文，不承载可现查的分支、远端或身份事实。

## 规则与执行纪律

强规则必须以**外部可观测事件**为**触发**，并写明**动作**、可复制方法、成功**判据**、**失败**处理和登记**证据**。内部判断不是稳定触发点。升级条件使用事件计数；普通可逆细节采用满足验收的最简单方案。

失败不是默认停止条件。按 [debugging.md](references/debugging.md) 复现、分类、安全诊断、恢复并复验原动作。只有重大决策、新权限或真实证据缺失才暂停。规模本身不是停止理由；未获用户或项目授权不得委派。

能力信号在启动和节点事件上评估并留下“触发/未触发+理由”。安装全局插件、Skill、Hook、MCP、认证账号、付费服务、浏览器登录态、外发数据、持久配置或扩大权限前过授权门。连接器、CLI 和浏览器的能力与认证分别验证。

提交前读取实际暂存清单，确认有效身份，扫描工作树、暂存区和完整历史中的秘密、个人信息和机器路径，并做独立通用性检查。可能接触凭据的诊断先遮蔽值，**值不进上下文**；结果**默认不落盘**，归档前**脱敏**。发现泄露时不重复值，登记轮换、残留清理和暴露面。

每个已接受行为执行 TDD：最小测试 → 预期 RED → 最小实现 → 聚焦 GREEN → GREEN 后重构 → 风险相称回归与真实产物检查。不得削弱测试掩盖失败。

## 完成条件

声明完成前执行 `IDENTIFY -> RUN -> READ -> VERIFY -> THEN`。只有以下全部满足才能结束：

- 已接受目标和真实证据门通过；
- 聚焦测试和适量回归通过；
- `state.md`、规格、计划、规则、安装和版本控制符合现实；
- 回滚方式与剩余限制已记录；
- 没有未完成的必要工作。

否则继续，或按 [gates.md](references/gates.md) 报告准确的决策、权限或证据阻塞。
