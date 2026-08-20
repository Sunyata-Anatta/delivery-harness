# Agent 配置

Delivery Harness 只有一份执行规范，就是 `SKILL.md`。不同 Agent 或项目只引用它，不复制整套流程。这样修改规则时不会出现多个互相矛盾的版本。

## 安装位置

不同运行时共享 `SKILL.md` 格式，但不共享发现目录和调用语法。Codex 使用 `.agents/skills`，Claude Code 使用 `.claude/skills`，OpenClaw 和 Hermes 还有自己的安装器与优先级。完整路径、命令、更新和卸载流程见 [runtime-installation.md](runtime-installation.md)。

不要维护多个手工编辑副本。选一个源仓库，在部署时复制或安装到运行时目录。

## OpenAI Agent 配置

仓库自带的 `agents/openai.yaml` 是最小完整配置：

```yaml
interface:
  display_name: "Delivery Harness"
  short_description: "从当前事实持续推进到真实证据验收"
  default_prompt: "Use $delivery-harness to audit the current project and continue until the accepted evidence gate passes."
policy:
  allow_implicit_invocation: true
```

`default_prompt` 必须出现 `$delivery-harness`，否则界面入口可能只发送普通提示而不加载技能。`allow_implicit_invocation: true` 允许 Agent 在任务明显匹配时自动选择技能；显式写 `$delivery-harness` 始终更确定。若组织要求所有工作流都由用户点名，把该值改为 `false`。

不要在通用配置中声明 GitHub、云数据库或其他可选 MCP 为硬依赖。只有当核心流程在缺少该工具时完全不能运行，才从该连接器的官方元数据添加 `dependencies.tools`。不要猜测 MCP 名称或地址。

## 其他 Agent 运行时

如果运行时能读取 Agent Skills，安装完整目录并按其语法调用 `delivery-harness`。如果运行时不能自动发现 `SKILL.md`，在项目说明文件中放一个短入口，不要粘贴整份技能：

```text
复杂、多阶段交付任务开始前，读取已安装的 delivery-harness/SKILL.md。
遵守项目覆盖层、证据门和授权边界；文档同步后继续下一个已批准节点。
```

可把这段入口放进该运行时实际读取的仓库规则文件，例如 `AGENTS.md`、`CLAUDE.md` 或同类文件。具体文件名由运行时决定。技能本身仍是通用规则的唯一事实源。

## 单 Agent

同一个 Agent 负责现实审计、当前节点、文档同步、测试、证据和版本控制。任何时候只保留一个活动节点。长任务用简短状态更新维持可见性。

## 多 Agent

只有任务可独立并行且确有必要时才考虑委派。先请求用户允许使用子代理；不得为简单或串行任务委派。获得允许后才启用子代理。

主代理负责：

- 交付契约、阶段状态和唯一活动节点；
- 共享文档、全局规则、权限请求和证据门；
- 任务拆分、结果复核、集成、提交、推送和阶段转换；
- 避免两个写入者同时修改同一文件或共享状态。

子代理只接收边界清楚、可独立验证的任务。任务说明应包含输入、允许修改的文件、验收命令、禁止事项和返回证据。除非主代理明确授权，子代理不得改变阶段、扩大范围、修改共享规则、安装全局组件、提交、推送或发布。

子代理的完成报告不是验收证据。主代理必须查看实际差异并重新运行相应验证。

## 项目覆盖层

把 [project-overlay.template.md](../assets/project-overlay.template.md) 复制到项目的文档或规则目录，填写项目事实。覆盖层适合存放命令、授权边界、项目独有规则、集成状态、真实证据门、Resolver 和经验教训。

经验是证据记录，Resolver 是执行路由。经验回答之前发生了什么、证据是什么、以后要改变什么；Resolver 回答在已知条件下应该选择哪个 Skill、工具或流程。先有可信经验，再把稳定且会重复使用的结论写进 Resolver。

Harness 在现实审计、工具变化、路由失败和阶段转换时检查 Resolver，但不按节点机械改写。只有输入条件、可用能力、选择结果或重审条件发生变化时才更新路由。Resolver 不能跳过授权边界、重大决策或真实证据门。项目没有重复路由需求时，删除该节即可。

优先级如下：

```text
系统、安全与用户指令
  -> 仓库规则和项目覆盖层
  -> Delivery Harness 通用规则
```

项目覆盖层只能在本项目内收紧或具体化规则，不能绕过更高层指令。通用经验回写技能前，先确认它已在多个项目中成立；单个项目的经验和 Resolver 留在覆盖层。

## 配置验证

安装或更新后检查：

1. `SKILL.md` 前置元数据只有 `name` 和 `description`。
2. `agents/openai.yaml` 能被 YAML 解析，所有界面字符串都有引号。
3. `default_prompt` 包含 `$delivery-harness`。
4. 引用文件和项目覆盖层模板都存在。
5. 运行技能仓库的测试和官方快速校验脚本。
6. 在一个新任务中显式调用技能，确认运行时能发现它。
