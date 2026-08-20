# 可选能力路由

Delivery Harness 按项目特征选择 Ponytail、Caveman、Humanizer、Context7、文档解析、代码图谱或项目特有 Skill 或插件。它们不是硬依赖。缺失时说明收益、风险和降级方案，不得静默安装。

## 目录

- [统一流程](#统一流程)
- [信号评估时机](#信号评估时机)
- [选择矩阵](#选择矩阵)
- [Ponytail](#ponytail)
- [Caveman](#caveman)
- [Humanizer](#humanizer)
- [Context7](#context7)
- [文档解析](#文档解析)
- [代码图谱](#代码图谱)
- [项目特有能力](#项目特有能力)
- [Resolver 记录](#resolver-记录)
- [停止条件](#停止条件)

## 统一流程

所有可选能力都执行同一条路径：

```text
发现 -> 适配判断 -> 授权 -> 安装 -> 调用 -> 验证 -> 降级
```

1. 发现：查看当前运行时已经暴露的 Skill、插件、MCP、CLI 和仓库规则。零安装能力优先，安装全局组件是最后手段。常用只读探测：`npx --yes skills list` 列已装独立 Skill；PowerShell 用 `Get-Command`、POSIX 用 `which` 查 CLI 是否可用。
2. 适配判断：按下面的评估时机表在节点事件上评估信号，确认任务触发信号、预期收益、数据边界、许可证、维护状态和替代方案。
3. 授权：项目内可逆配置按既有权限继续。全局安装、Hook、MCP、持久配置和账号认证先请求明确授权。授权分两种模式：自动开启（用户预授权所需工具集，写入覆盖层「预授权工具集」槽，集内安装不再逐次询问）或逐个授权；两种模式都不免除安装后登记到集成表。
4. 安装：优先运行时原生安装器，其次使用 [runtime-installation.md](runtime-installation.md) 的标准 Skill 目录。
5. 调用：使用运行时实际列出的名称。插件命名空间与独立 Skill 名称可能不同。
6. 验证：先确认可发现，再用一个小型只读任务确认行为，不用安装成功提示代替运行验证。
7. 降级：能力缺失或不适配时退回仓库工具、标准搜索、普通写作或人工规则，项目不得因此停摆。

不要同时安装多个同名副本。安装前检查覆盖顺序，安装后记录来源、版本、范围、验证和卸载方式。

## 信号评估时机

harness 自主推进时用户不在场，信号的评估必须锚定在节点事件上：走到那个动作就评估，不靠执行者想起，也不依赖用户开口。触发后走统一流程，只有授权、决策和证据门需要用户。

| 节点事件 | 评估的信号 |
|---|---|
| reality_audit 开始读取仓库结构 | 代码图谱：陌生或大型仓库、调用链、跨模块影响 |
| tool_research 开始 | Context7、联网调研：一手文档、版本与 API 事实 |
| reality_audit、tool_research 或 real_evidence 遇到 PDF 或项目图片材料 | 文档解析：本地提取，片段化送模型 |
| 写入对外文档或 README 前 | Humanizer：事实核对后的最终文稿 |
| 新增依赖、抽象、文件或代码前 | Ponytail：规模控制 |
| 处理领域格式或平台能力 | 项目特有能力 |

## 选择矩阵

| 能力 | 触发信号 | 不应启用 |
|---|---|---|
| Ponytail | 新增依赖、抽象、文件或代码可能过多；用户要求最小实现 | 安全、数据完整性、无障碍或明确需求会被削弱 |
| Caveman | 用户要求低 Token、短进度或机器间高频协作 | 安全警告、不可逆确认、复杂操作顺序会因压缩而含糊 |
| Humanizer | 对外文档、README、说明文需要自然表达 | 代码、结构化数据、日志、法律原文、证据或引用需要逐字保真 |
| Context7 | 需要库或框架的一手文档、版本与 API 事实 | 平台文档、规范页要用官方来源，不用库索引替代 |
| 文档解析 | 遇到 PDF 或项目图片材料，量大会烧 token | 小文档直接读；逐字保真文本不用视觉模型代读 |
| 代码图谱 | 陌生或大型仓库、调用链、跨模块影响、路由和死代码分析 | 小仓库、单文件任务、简单字面搜索已经足够 |
| 项目特有能力 | 领域格式、平台或验收无法由现有能力可靠覆盖 | 只有推测收益，没有当前任务证据 |

## Ponytail

用途：减少不必要的依赖、抽象、文件和代码。它不替代需求分析、TDD、安全和真实证据门。

优先检查是否已安装。官方插件源为 `DietrichGebert/ponytail`。Codex 插件安装示例：

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Claude Code 中分两次执行：

```text
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

OpenClaw 可用 `clawhub install ponytail`。Hermes 可用：

```bash
hermes plugins install DietrichGebert/ponytail --enable
```

安装插件可能同时启用 Hook。先阅读插件清单和 Hook，再信任并重启运行时。若只需要指令层，按运行时安装独立 `ponytail` Skill，接受没有常驻 Hook 的差异。

调用名称以运行时列表为准。常见形式：

```text
$ponytail:ponytail ultra
$ponytail ultra
/ponytail ultra
```

验证：让它审查一个小改动，确认建议减少非必要实现，同时保留验证、安全和错误处理。

## Caveman

用途：压缩沟通和 Token，不负责减少实现范围。官方源为 `JuliusBrussee/caveman`。

Codex 的独立 Skill 安装示例：

```bash
npx skills add JuliusBrussee/caveman -a codex
```

Claude Code 插件安装示例：

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

OpenClaw 的官方项目提供专用安装器。不要直接执行未经查看的远程脚本。先克隆或下载固定版本，阅读 `INSTALL.md` 和安装脚本，运行 `--dry-run`，获全局配置授权后再按其 `--only openclaw` 路径安装。

调用名称以运行时列表为准：

```text
$caveman full
/caveman full
```

验证：同一技术问题的回答明显变短，但命令、错误文本、验收证据和安全警告保持完整。

## Humanizer

用途：完成事实核对后，清理 README、交接文档和对外说明中的机械表达。官方源为 `blader/humanizer`。

跨 Agent Skills CLI 安装示例：

```bash
npx skills add blader/humanizer --global
```

Claude Code 也可使用插件：

```text
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

常见调用形式：

```text
$humanizer:humanizer 优化 README.md，只编辑最终稿，不改变事实和命令。
/humanizer:humanizer 优化 README.md，只编辑最终稿，不改变事实和命令。
```

运行时没有插件命名空间时使用 `$humanizer` 或 `/humanizer`。验证时比较前后事实、数字、链接、命令和范围，任何信息损失都应回退。

## Context7

用途：检索库与框架的一手文档，供工具调研时引用版本、API 和配置事实。官方源为 `upstash/context7`。

零安装调用（语法核实于 2026-08-18）：

```text
npx -y context7 <库名或组织/仓库> <问题>
npx -y context7 search <关键词>
```

实测边界：CLI 语法如上，但本执行环境调用 API 返回 404，可能是环境代理拦截或需要 API key。在项目环境里先跑一次小查询验证可用，再依赖它；验证不通过时直接降级到 web 检索与官方页。

MCP 形式（`npx -y @upstash/context7-mcp`）属于持久配置，高频使用后再评估，且必须单独授权。

边界：它覆盖库文档，对 Agent Skills 规范、hooks 这类平台文档覆盖有限，权威源仍是官方页。引用外部事实时写成判据式（命令 + 日期 + 当时结果），不用检索摘要代替一手核对。

验证：让它回答一个已知版本的事实，与官方发布页逐字核对。降级：web 检索与官方页直接阅读。

## 文档解析

用途：PDF 与项目图片先本地提取再送模型，省下把整页像素和原始布局喂给模型的 token。分工原则：**提取用 OCR，理解用模型**。需要逐字保真的文本（证据、引用、命令、日志）禁用视觉模型代读，因为视觉模型会在难读处猜测改写。

路由按材料类型：

```text
遇到 PDF 或项目图片材料
  -> pdf-inspector 分类：文本型 / 扫描型
     文本型 -> LiteParse 转 Markdown，按需截取相关页与章节送模型
     扫描型 -> PaddleOCR 提取文本，片段化送模型
  项目图片（截图、照片、图表含字）-> PaddleOCR
  整本书要当长期知识 -> book-to-skill 转技能，一次转换长期复用
  小文档（几页）-> 直接读，不解析
```

- 官方源：pdf-inspector（firecrawl/pdf-inspector，Rust 库，无 OCR）、LiteParse（run-llama/LiteParse）、PaddleOCR（PaddlePaddle/PaddleOCR）、book-to-skill（virgiliojr94/book-to-skill）。核实于 2026-08-18。
- 授权边界：pdf-inspector 与 LiteParse 可项目级安装；PaddleOCR 依赖重（框架级），全局安装必须先授权；book-to-skill 是技能安装，按统一流程走。
- 验证：同一 PDF 取一页，对比直接读与解析后送入的 token 量与文本完整性；OCR 用已知文字图片核验逐字准确率。
- 降级：工具缺失时模型直接读关键页；逐字保真场景没有 OCR 时人工核对，不交给视觉模型。
- 重选条件：解析丢失关键信息（表格、公式、版面）或实测 token 节省不显著时回到直接阅读。

## 代码图谱

代码图谱是结构化代码发现能力，不是项目事实源。优先使用运行时已经提供的图谱 MCP。典型调用顺序：

```text
search_graph -> trace_path -> get_code_snippet -> 普通文本搜索补缺
```

`search_graph` 找符号，`trace_path` 查调用方向和影响，`get_code_snippet` 读取目标实现。索引缺失或过期时先重建，再验证关键结果。字面量、错误文本、配置和非代码文件仍用普通搜索。配套指令卡 `codebase-memory` Skill 提供决策矩阵与坑位表，安装 MCP 前先读，确认工具面与项目需要匹配。

如项目决定采用 `DeusData/codebase-memory-mcp`，先检查其当前发布、校验和、许可证、遥测、写入位置和运行时配置。推荐下载固定版本安装包并核对 SHA-256。也可在明确授权后使用：

```bash
npm install -g codebase-memory-mcp
codebase-memory-mcp install
```

该操作会安装全局程序并修改 Agent 的 MCP 或规则配置，必须先授权。安装后重启 Agent，索引目标仓库，再用 `search_graph` 和 `trace_path` 验证。图谱回答与源码冲突时，以当前源码和测试为准。

## 项目特有能力

项目可以在覆盖层加入特有 Skill 或插件。先写能力卡，再决定是否安装：

```text
名称与用途：
触发信号：
来源、版本与许可证：
运行时与安装范围：
数据、网络、遥测和凭据边界：
调用方式：
验证命令或样例：
失败降级：
卸载与回滚：
重审条件：
```

选择规则：

1. 现有能力足够时不新增。
2. 只从维护者资料核对安装和权限，不把搜索摘要当安装说明。
3. 先项目级、临时或只读试用，再考虑全局和持久安装。
4. 含 Hook、MCP、浏览器登录态、远程执行脚本、外发数据或秘密的能力必须单独授权。
5. 安装后必须运行发现测试和一个代表性任务。
6. 无法验证、来源不明或收益不足时保持未安装，并记录降级路径。

## Resolver 记录

把稳定路由写入项目覆盖层，不写回通用 Skill。例如：

| 条件 | 选择 | 验证 | 降级 | 重审条件 |
|---|---|---|---|---|
| 跨模块调用链分析 | 已安装代码图谱 | 找到符号并追踪一条已知调用链 | `rg` 加定点源码阅读 | 索引过期或语言不支持 |
| 对外中文 README 定稿 | Humanizer | 事实、命令和链接无变化 | 人工编辑 | 文档改为法律或审计证据 |

Resolver 只记录有证据、会重复使用的路由。一次性试验留在节点记录，不提升为长期规则。

## 停止条件

遇到以下情况停止并请求用户决定或授权：

- 需要安装全局程序、插件、Hook、MCP 或修改持久机器配置；
- 工具会读取仓库外数据、上传代码、使用账号或产生费用；
- 候选能力改变安全、隐私、许可证或长期维护方式；
- 同名 Skill 来源冲突，无法确定真实生效副本；
- 安装器只有远程脚本且无法先检查内容；
- 能力验证失败，继续需要削弱验收标准。
