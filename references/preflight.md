# 机械预检（preflight）

本页定义交付记录与提交的机械校验：把“记录可用、记录与代码同批、证据可追溯、身份一致、提交真实回读”做成可执行、可失败、可读回的检查。规范性判断仍由[门控](gates.md)承担；预检是门的机械投影，不替代审阅、真实证据与用户决断。工具是随载荷分发的单文件标准库脚本 [preflight.py](preflight.py)，语言中立只此一份，本页与英文版同步维护。

## 用途与边界

- 只读运行：不修改记录、不创建替代记录、不写项目文件；唯一写操作是显式请求的可选 `--install-hook`。
- 覆盖十五项检查：a–i 守记录与提交，j–o 是[硬约束](hard-constraints.md) H1–H6 的机械检查；严重级别可配为 block 或 warn；失败输出修复建议，由执行者修复后重跑。
- 不联网；秘密扫描只报告“文件+类型”，绝不回显匹配值；不读取证据槽之外的敏感来源。
- 退出码可被 CI 消费，`--json` 是稳定的机器接口。
- 不替代：独立审阅、真实证据门、提交对象回读的人工判断、专用秘密扫描器与历史覆盖检查。

## 运行时机

| 事件 | 命令 | 说明 |
|---|---|---|
| 本次交付首次 `git add` 前 | `python -B -X utf8 <skill>/references/preflight.py --root . --json` | 默认模式查看工作区与暂存区待提交变更；有 block 失败不得暂存 |
| `git add` 后、提交前 | 同上加 `--staged` | 只检查索引；提交 hook 也运行此模式 |
| 候选提交消息定稿后 | 加 `--message-file <文件>` | 检查会话/分享链接与 agent trailer |
| 提交创建后 | 加 `--readback` | 检查该提交的 diff 真的包含记录变更，而不只是暂存过 |
| 完成、交接或发布声明前 | 默认模式或 `--staged` | 未通过不得宣告完成 |
| 需要自动拦截时 | `--install-hook` | 显式同意后安装仓库内 commit-msg hook |
| CI | `--json` | 按退出码与 `status`、`checks` 消费 |

`<skill>` 指安装后的 delivery-harness 目录；脚本位于 `references/` 内，随运行时四项载荷分发，不新增顶层分发目录。

## 配置

发现顺序：先读 `<root>/.delivery/preflight.json`；不存在时读 `.delivery/overlay.md` 中名为 `preflight` 的围栏块内的同构 JSON；都没有则使用内置默认值，并在输出里标记 `config_source: "defaults"`。JSON 文件优先；overlay 块存在但被遮蔽时在 `notes` 中说明。配置只接受 JSON，不引入第二种语法；类型错误、未知枚举、不可编译的正则都按配置错误处理（退出码 2）。

| 键 | 默认值 | 含义 |
|---|---|---|
| `schema` | `1` | 配置版本；目前只接受 1 |
| `record.path` | `.delivery/state.md` | 唯一活动状态或正式记录路径（相对项目根） |
| `record.tracked` | `"auto"` | 记录是否在版本控制；`auto` 依据索引与 HEAD 自动判断 |
| `record.related_readable` | `[]` | 只需可读的相关记录或覆盖层路径 |
| `record.mtime_tolerance_seconds` | `0` | untracked 记录修改时间比较的容差 |
| `code.paths` | 常见源码路径 | 视为“代码变更”的 glob；`*` 不跨目录，`**` 跨目录 |
| `code.exclude` | `[]` | 从代码路径中排除的 glob |
| `evidence.path` | 记录路径 | 证据索引文件 |
| `evidence.prefix` | `"E"` | 证据编号前缀 |
| `evidence.allow_needs_source` | `false` | 允许无链接的 `needs-source` 行降级为告警 |
| `baseline.enabled` | `false` | 检查 d 的开关 |
| `baseline.path` / `pattern` / `ref` | 无 | 版本文件、提取版本号的捕获正则、基线提交 |
| `exemptions.path` | `.delivery/preflight-exemptions.md` | 豁免文件 |
| `identity.name` / `email` / `check_committer` | 无 | 身份策略；未配置时检查 h 跳过并告警 |
| `limits.record_max_lines` / `record_max_line_length` | `80` / `0` | 记录行数与单行字符上限；行长 0 表示关闭 |
| `secrets.patterns` / `exclude` / `max_bytes` | 高置信内置模式 | 秘密扫描；只报文件+类型 |
| `message.banned_links` / `banned_trailers` | 内置规则 | 候选消息中禁用的链接与 trailer 正则 |
| `evidence.daily_limit` | `5` | 检查 l：同一日期的证据条目上限 |
| `evidence.minor_paths` | 样式表、`**/locales/**`、`**/i18n/**` | 检查 k：只改这些路径的批次视为界面、文案或样式微调 |
| `evidence.files` | `[".delivery/artifacts/**"]` | 检查 k：视为证据文件的路径 |
| `state.id_pattern` | `\b[A-Z]{1,2}\d+[a-z]?\b` | 检查 j：需要写含义的编号形态 |
| `state.banned_tokens` | `→`、`=>`、`->`、`TBD`、`w/`、`&&` | 检查 j：状态正文禁用的速记（代码片段除外） |
| `decisions.path` / `executors` | `.delivery/decisions.md` / `AGENTS.md`、`CLAUDE.md` | 检查 n：决策登记与需核对引用的执行文件 |
| `branches.allowed` | `main`、`master` | 检查 o：允许存在的本地分支 |
| `checks.a` … `checks.o` | `block`（`l` 为 `warn`） | 每项检查的严重级别，可取 `block` 或 `warn`；调整须有决策登记 |
| `readback.ref` | `HEAD` | 检查 i 要回读的提交 |
| `hook.python` | 安装时的解释器 | 提交 hook 使用的 Python 命令 |

独立配置示例：

```json
{
  "schema": 1,
  "record": {
    "path": ".delivery/state.md",
    "related_readable": [".delivery/overlay.md"]
  },
  "code": {"paths": ["src/**", "**/*.py"], "exclude": ["docs/**"]},
  "evidence": {"path": ".delivery/state.md", "prefix": "E"},
  "identity": {
    "name": "Example Author",
    "email": "author@example.invalid",
    "check_committer": false
  },
  "limits": {"record_max_lines": 80, "record_max_line_length": 0},
  "checks": {"d": "warn"}
}
```

同一份配置也可作为覆盖层中的围栏块存在（初始化或不愿意维护独立文件时）：

```preflight
{"record": {"path": ".delivery/state.md"}, "checks": {"d": "warn"}}
```

证据行约定：行首允许列表符号或方括号，随后是“前缀+数字”和空格，行内必须有一个 Markdown 链接、一个类别标签（`[门结论]`、`[变更]`、`[根因]` 或英文 `[gate]`、`[change]`、`[root-cause]`）和登记日期 `YYYY-MM-DD`，复审条目再写 `第 N 轮`；链接按“证据索引所在目录、项目根”的顺序解析，目标必须存在。编号在新增行内严格递增，且大于基线中的最大编号。示意：

```text
- E12 [门结论] 2026-10-21 批量运行通过；[batch run](artifacts/batch/run.log)。
- E13 [根因] 2026-10-21 复审第 2 轮确认缓存未失效；[receipt](.delivery/artifacts/2026-10-21-preflight/README.md)。
```

豁免文件用于“本批确实不该改记录”的例外；每行一个 glob 和理由，理由不能为空：

```text
- src/generated/** — generated files; record updated in batch 2026-10-21-preflight
```

## 检查项

| 检查 | 触发与做法 | 判据 | 失败处理 |
|---|---|---|---|
| a | 记录文件存在、可按 UTF-8 读取、`r+b` 可写；`record.related_readable` 逐个只读预检 | 全部通过 | block 失败；不自动创建或迁移记录 |
| b | 暂存区（默认模式含工作区未暂存变更）有代码路径变更时，要求记录同批变更；tracked 记录按变更集合严格比对；untracked 记录要求修改时间不早于本批最新代码改动；或由豁免文件覆盖 | 同批或全部豁免 | block 失败并列出未覆盖路径；豁免命中记告警 |
| c | 相对 `HEAD` 取证据索引新增/修改行；无基线时整文件检查并降级告警 | 每行有可解析且目标存在的链接；新增编号严格递增 | block 失败，只报行号与编号 |
| d | 新增证据行时，`baseline.path` 中由 `baseline.pattern` 捕获的版本号必须递增；`baseline.enabled=false` 时跳过 | 版本按数字段严格增大 | block 失败；开关关闭时显式 skip |
| e | 记录行数与单行字符数不超过 `limits` | 均不超 | block 失败；0 表示该项关闭 |
| f | 扫描暂存（`--staged`）或待提交文件内容，二进制与超大文件跳过 | 无命中 | block 失败；只报文件与类型，绝不回显值 |
| g | `--message-file` 的候选提交消息 | 无会话/分享/聊天链接，无 `Claude-*` 类 trailer | block 失败；只报类型与行号，不回显链接 |
| h | `git var GIT_AUTHOR_IDENT`，配置 `check_committer` 时另查提交者身份 | name 精确、email 大小写不敏感一致 | block 失败；未配置身份策略时 skip 并告警，不构成身份门通过 |
| i | `--readback` 读取 `readback.ref` 提交的 diff 与记录 blob | 提交含代码变更时记录路径必须在提交 diff 中真实变更 | block 失败；untracked 记录无法回读时 skip 并写明局限 |
| j | [H3](hard-constraints.md#h3)、[H4](hard-constraints.md#h4)：读状态文件 | 三句话段、完整句子、无速记、编号带含义；授权段每条有「适用」，并有「不在该授权内」 | block 失败；未填写的模板占位符按空值处理 |
| k | [H1](hard-constraints.md#h1)：相对 `HEAD` 的新增或改动证据行与本批改动 | 每行有类别标签与日期，复审行有轮次；纯微调批次不加条目、不升基线、不建证据文件；基线改版须有新条目或新决策 | block 失败 |
| l | [H1](hard-constraints.md#h1)：按日期统计证据条目 | 本批涉及的日期都不超过 `evidence.daily_limit` | 默认 warn，作为逐条复核提示 |
| m | [H2](hard-constraints.md#h2)：状态的「复审轮次」段 | 段落存在；轮次大于 2 的行写明负责人点名 | block 失败并提示停下 |
| n | [H5](hard-constraints.md#h5)：决策登记与执行文件 | 字段齐全、无不可判定词、硬约束有检查、第二次违反已升级、引用的编号存在 | block 失败；登记文件不存在时 skip |
| o | [H6](hard-constraints.md#h6)：本地分支 | 全部在 `branches.allowed` 中 | block 失败 |

## 退出码与 --json

| 退出码 | 含义 | 后续动作 |
|---|---|---|
| `0` | PASS：没有 block 级失败；warn 与 skip 允许出现 | 按门继续；skip 逐项登记，不得写成门已通过 |
| `1` | FAIL：至少一项 block 级失败 | 等同对应门失败：不得暂存、提交、推送或宣告完成 |
| `2` | 用法或配置错误 | 修复命令、配置或 Git 环境后重跑；不得用猜测配置绕过 |

`--json` 输出单个对象，字段固定：`schema`、`tool`、`tool_version`、`mode`、`root`、`config_source`、`status`（`pass`/`fail`/`error`）、`summary`（blocked/warned/skipped/passed）、`checks`（按 a–o 排列，含 `severity`、`status`、`note`、`findings`）、`notes`。`findings` 只含 `level`、`type`、`message`、`path`、`line`、`fix`，不包含任何被扫描到的值。用法或配置错误时同样输出 JSON，`status` 为 `error`，退出码 2。

```json
{
  "schema": 1,
  "tool": "delivery-harness-preflight",
  "mode": "staged",
  "status": "fail",
  "summary": {"blocked": 1, "warned": 0, "skipped": 4, "passed": 4},
  "checks": [
    {
      "id": "b",
      "severity": "block",
      "status": "fail",
      "findings": [
        {"level": "block", "type": "record-not-in-batch", "path": ".delivery/state.md", "line": null, "message": "code paths changed but the record is not in the same batch", "fix": "update the record and include it in this batch"}
      ]
    }
  ]
}
```

## 与门的关系

- [机械预检门](gates.md#mechanical-preflight)：首次 `git add` 前与任何完成声明前必须运行；退出码 1 或 2 都不得继续，检查失败等同对应门失败。
- “记录与身份可用性门”由 a、h 机械化；h 跳过表示身份策略或身份事实不可核对，不表示该门通过。
- [正式记录一致性](gates.md#formal-record-consistency)要求记录回读：写入后按[落笔自检](gates.md#write-back-check)读回实际内容，预检不替代这一步。
- [提交对象回读](gates.md#commit-object-readback)：`--readback` 只验证 commit diff 含记录变更；消息、作者、提交者仍需按门读回。
- 证据门与秘密门：c 是链接与编号的降级检查，f 是高置信模式扫描；专用扫描器、真实样本与独立审阅仍是更高层证据。
- 预检通过不使其他门自动通过；预检失败也不因其他门通过而放行。

## --no-verify 例外规则

1. 仅限 hook 环境不可用（例如解释器缺失、宿主禁用 hook）或紧急恢复；必须在过程记录写明原因、范围和替代验证。
2. 记录缺失、记录未同批、证据链接失败、秘密命中、身份不符、候选消息含会话链接等检查失败时，禁止用 `--no-verify` 或任何环境变量绕过；先修复再提交。
3. 绕过 hook 后仍必须在提交前后手动运行默认模式与 `--readback`，并在过程记录登记命令、退出码与结果。
4. 未安装 hook 不等于通过；未安装时由执行者在同一执行点运行同样的命令。
5. 重复或系统性绕过视为门失败：在唯一活动状态保留未闭合项与解除条件，直到补跑通过。

## 提交 hook（可选）

- 安装：`python -B -X utf8 <skill>/references/preflight.py --root . --install-hook`。只有显式给出该参数才执行；hook 安装不是默认行为，也不是分布面同步。
- 位置：只写仓库 hooks 目录内的 `commit-msg`，遵守 `core.hooksPath`；解析到仓库外时拒绝（退出码 2）。
- 保护：已存在无本工具标记的 hook 时拒绝覆盖，需人工先处理。
- 内容：调用同一脚本的 `--staged --message-file "$1"`；解释器与脚本路径在安装时写入，只存在于本地 hook 文件，不进入仓库。
- 卸载：删除该 hook 文件；移动或更新 skill 目录后重新安装。
- 不修改全局 Git 配置；全局与项目安装面的同步和验证属于发布动作，需另行授权。

## 限制与降级

- untracked 或被忽略的记录：b 使用修改时间启发，只覆盖同机同批；i 无法回读时 skip 并告警，不得声称提交回读通过。
- c、d 需要证据索引在 Git 中存在基线；无基线时整文件检查并降级告警，或直接跳过。
- f 只覆盖配置的高置信模式，不是完整秘密扫描；二进制、超大文件与历史提交不在默认范围。
- merge、rebase、amend 之后应按门的对象范围重新回读；`--readback` 只检查所选提交与其父提交的 diff。
- Windows 路径按 `/` 归一化匹配，配置可写反斜杠；文件系统大小写不敏感。
- 预检不判断记录内容是否真实、证据是否充分、授权是否覆盖；这些仍由门与人工判断。
