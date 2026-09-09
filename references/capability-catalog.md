# 能力提供者目录

只读已选提供者的小节。安装与更新命令使用前查当前一手文档；既有授权按范围复用。

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

用途：完成事实核对后，清理 README、交接文档和对外说明中的机械表达。通用 Humanizer 官方源为 `blader/humanizer`；中文专用 Humanizer-ZH 来源为 `op7418/humanizer-zh`。

文本语言路由是硬规则：

```text
中文正文 -> humanizer-zh
非中文正文 -> humanizer
混合文本按段落拆分后分别路由
```

先查看当前运行时能发现的名称。目标 Skill 缺失时，给出上表对应的安装来源和方法，安装前请求授权；不静默安装。`humanizer-zh` 不可用或未获授权时，中文正文只能人工编辑，不得回退到通用 `humanizer`。代码、命令、结构化数据、日志、法律原文、证据和引用始终不进入 Humanizer。

跨 Agent Skills CLI 安装示例：

```bash
npx skills add blader/humanizer --global
npx skills add op7418/humanizer-zh --global
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
