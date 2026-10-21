# {{PROJECT_NAME}} Delivery Overlay

本文件只保存稳定规则、定义与唯一入口。它可以收紧或具体化 Delivery Harness，但不能覆盖系统、安全或用户指令。
当前状态只写唯一状态；固定观察写证据入口，历史写过程/历史入口，经验写经验入口。删除不适用条目，不保留空洞占位说明。

## 项目标识

- 目标：{{ACCEPTED_OUTCOME}}
- 非目标：{{NON_GOALS}}
- 主要用户：{{USERS}}
- 锁定语言：{{LANGUAGE_AUTO_ZH_EN}}

## 事实源

- 仓库规则：{{REPOSITORY_INSTRUCTIONS}}
- 已接受规格：{{ACCEPTED_SPEC}}
- 执行计划：{{EXECUTION_PLAN}}
- 活动状态：`{{ACTIVE_STATE_PATH}}`（唯一指针；默认布局填 `.delivery/state.md`）
- 导航：`{{PROJECT_MAP_PATH}}`（默认 `PROJECTMAP.md`；骨架与按需导引，不递归展开）
- 规约入口：{{RULE_CLAUSE_ENTRIES}}（来源路径及适用范围/章节；已有规则只引用，不复制正文）
- 正式记录契约（适用时）：{{FORMAL_RECORD_CONTRACT_ENTRY}}（唯一入口；来源/作用域、语义角色、写入方与时机、阶段判据、回读及恢复，不存当前结果）
- 过程索引：`{{PROCESS_RECORD_PATH}}`（默认 `.delivery/process.md`；只存重要历史检查点与最近压缩回执，按主题/编号读取）
- 原始历史入口：`{{HISTORY_ENTRY_PATH}}`（既有归档入口或按需创建的历史清单；原文不可变，不在启动时展开）
- 证据入口：`{{EVIDENCE_ENTRY_PATH}}`（既有报告/章节或按需摘要；固定对象、版本、结果、限制与原始回执）
- 经验入口：`{{LESSONS_ENTRY_PATH}}`（复用既有文件或章节；仅按当前任务/复发条件读取，不另建副本）
- 既有状态适配：{{STATE_FIELD_MAPPING_WRITER_AUTHORITY_VERIFY_RECOVERY}}（节点/授权/证据/待决断字段、写入方与权限、验证及恢复方法；不另建活动状态）

上述路径只在此定义；摘要与其他章节引用字段名。路径字段默认相对项目根（仓库使用工作树根），Markdown 相对链接仍以所在文档为基准。
已有治理沿用其明确声明的路径基准；不同基准或跨工作面须在此说明，不能静默重解释已有路径。
接入与规约检查、提交发现、错误细节、方案选择及支撑数据先留不可变回执，过程索引只保留必要导航。

## 目录约定

存放根：`.delivery/`（默认名，改名后在此写明）
- 活动状态：使用上方唯一指针，默认进版本控制；隐私偏离需登记可恢复位置和验证方法
- `uploads/`：获准留存的短期用户输入，只入不改
- `artifacts/<task>/tmp/`：可丢弃/可重建中间物、一次性测试资源；登记清理条件
- `artifacts/<task>/retained/`：需交付或长期保留的 demo、图文音视频与人工测试材料；不自动清理
- `debug/`：临时排错输出与复现材料
复用既有资源登记；否则任务 README 只保存用途、最新不可变批次、保留/恢复与批次清单入口。
明细写批次清单，旧摘要先归档核验再替换，不在 README 无限逐项追加。任务子目录有内容才建；state/地图只留入口。
旧材料未分类先保留。沙盒成果交付前复制并验证项目内副本；失败保留源，恢复动作写唯一状态。
保留项仍默认 Git 忽略，不代表已备份或获准外发。
默认布局按已安装 Skill 的初始化参考复制状态/资源槽骨架；已适配既有状态时跳过默认状态创建。
过程索引、证据摘要、资源 README 有内容才按需建立，已有同职责文件直接适配，不为启动创建空文件。
长期规格、正式证据报告和回归/构建依赖沿用项目语义目录；敏感原件留在获准受限位置。
偏离默认的存放位置写在这里并说明原因：{{STORAGE_DEVIATIONS}}
历史跟踪/隐私/恢复策略：{{HISTORY_TRACKING_PRIVACY_RECOVERY_POLICY}}（访问范围、保留期、恢复入口与验证方法）。
状态进版本控制不使历史原文自动被跟踪或发布；历史按自身已批准策略保存。

## 项目独有规则

### 必须

- {{PROJECT_MUST_RULE}}

### 禁止

- {{PROJECT_MUST_NOT_RULE}}

### 约定

- 代码与文档风格：{{PROJECT_CONVENTIONS}}
- 数据与隐私：{{DATA_RULES}}

## 启动摘要

常规启动只读本页事实源的指针定义、适用硬约束与本节，再读指针解析出的唯一状态；不默认全文载入覆盖层。
本节只保留目标、事实源字段引用、profile 与硬约束，软目标 ≤450 tokens。长详情按当前动作读取，不展开所有入口。
必要安全与验收条款不因预算省略；首次适配或映射不清时读取相关完整定义。
- profile：`auto`（research/develop/review/document/operate 只调整候选）
- 路由事实源：本页 Resolver；过长才移到 `.delivery/routing.md` 并删除本页重复表
- 规约检查：动作前核对适用条款；节点转换、规则/路径变化或验证失败时按 Harness 执行合同检查。
  当前结论/阻塞写唯一状态，固定结果写证据入口，过程索引只留详细回执入口。

## 项目 Resolver

Resolver 把已验证经验变成条件路由。只在条件、能力、选择或重审条件变化时更新，不按节点机械改写。

| 请求或条件 | 选择的 Skill、工具或流程 | 证据引用 | 回退路径 | 验证定义 | 重审条件 |
|---|---|---|---|---|---|
| {{CONDITION}} | {{ROUTE}} | {{ROUTE_EVIDENCE_REF}} | {{FALLBACK}} | `{{VERIFY_COMMAND}}` | {{REVISIT_WHEN}} |

## 能力安装清单

只有当前 Agent 未发现所需能力时才使用此表。先给出已验证的安装来源和命令，再请求对应授权；来源或命令未知时保留未安装并走降级。

| 能力 | 类型 | 安装来源与版本 | 当前运行时安装方法 | 授权影响 | 发现与行为验证 | 降级 |
|---|---|---|---|---|---|---|
| {{CAPABILITY}} | {{SKILL_PLUGIN_MCP_CLI}} | {{SOURCE_AND_VERSION}} | `{{INSTALL_COMMAND_OR_METHOD}}` | {{AUTHORITY_REQUIRED}} | `{{VERIFY_COMMAND}}` | {{FALLBACK}} |

## 命令

- 会话启动采集：`{{SESSION_BOOTSTRAP_COMMAND}}`（输出规则、版本控制、节点、边界四行回执）
- 环境准备：`{{SETUP_COMMAND}}`
- 聚焦测试：`{{FOCUSED_TEST_COMMAND}}`
- 全量测试：`{{FULL_TEST_COMMAND}}`
- 静态检查：`{{LINT_COMMAND}}`
- 构建：`{{BUILD_COMMAND}}`
- 本地运行：`{{RUN_COMMAND}}`
- 部署验证：`{{DEPLOY_VERIFY_COMMAND}}`

## 授权边界

此处定义长期规则与边界；当前动作的有效授权来源、动作、限额占用与失效条件只在唯一状态维护。

### 可直接执行

- {{PREAUTHORIZED_ACTION}}

### 能力安装授权模式

- 自动开启：预授权工具集 `{{PREAUTHORIZED_TOOLS}}`（集内安装不再逐次询问；安装回执写证据入口，稳定配置登记集成表）
- 逐个授权：每次安装单独请求（默认）

### 需要明确授权

- {{APPROVAL_REQUIRED_ACTION}}

### 不得执行

- {{FORBIDDEN_ACTION}}

## 集成与凭据

| 集成 | 用途 | 能力入口 | 账号或所有者 | 配置权限边界 | 验证定义 | 数据边界 | 回滚 |
|---|---|---|---|---|---|---|---|
| {{INTEGRATION}} | {{PURPOSE}} | {{CONNECTOR_CLI_OR_BROWSER}} | {{OWNER}} | {{SCOPES}} | `{{VERIFY_COMMAND}}` | {{DATA_BOUNDARY}} | {{ROLLBACK}} |

不得在本文件保存令牌、密码、私钥或可复用认证信息。

## 分发面登记

登记所有会获得本项目产物的稳定路径、安装器、所有者、账号同步面或托管入口。
核验版本、时间、证据级别、结果与限制只存证据引用所指记录；未知/不可达保持未验证，不能从其他面的成功推导更新。
当前阻塞只写唯一状态；本表不维护第二份分发进度。

| 分发面 | 解析器或地址 | 所有者 | 更新方式 | 规范源 | 验证定义 | 证据引用 | 回滚 |
|---|---|---|---|---|---|---|---|
| {{DISTRIBUTION_SURFACES}} | {{SURFACE_RESOLVER_OR_ADDRESS}} | {{SURFACE_OWNER}} | {{SURFACE_UPDATE_METHOD}} | {{CANONICAL_SOURCE}} | {{SURFACE_VERIFY_METHOD}} | {{SURFACE_EVIDENCE_REF}} | {{ROLLBACK}} |

## 真实证据门定义

| 阶段 | 必需证据 | 样本或环境 | 通过标准 | 解除条件 |
|---|---|---|---|---|
| {{PHASE}} | {{EVIDENCE}} | {{SAMPLE_OR_ENVIRONMENT}} | {{PASS_CRITERIA}} | {{UNBLOCK_CONDITION}} |

## 版本控制

- 交付路径：{{DELIVERABLE_PATHS}}（随交付分发）
- 仅开发路径：{{DEV_ONLY_PATHS}}（不随交付分发。可执行件与一次性产物留在这里）
- 交付物依赖策略：{{DELIVERABLE_DEPENDENCY_POLICY}}
- 默认分支：{{DEFAULT_BRANCH}}
- 工作分支规则：{{BRANCH_RULE}}
- 提交规则：{{COMMIT_RULE}}
- 作者身份与邮箱策略：{{AUTHOR_IDENTITY_POLICY}}
- 脱敏扫描：{{SECRET_SCAN_COMMAND_AND_SCOPE}}
- 脱敏禁用词：{{FORBIDDEN_TERMS}}（本项目的产品名、主机名、同步工具、业务领域词。这些词属于项目事实，只留在本覆盖层，不写进通用 Skill 或它的测试）
- 提交范围核对：{{STAGED_FILE_LIST_COMMAND}}（提交说明必须覆盖这条命令列出的全部文件）
- 扫描证据：使用事实源的证据入口，按对象版本与扫描范围定位，不在此复制最近结果
- 历史隐私处理规则：{{HISTORY_PRIVACY_DECISION}}
- 推送、PR 与发布授权规则：{{PUBLISH_AUTHORITY}}（有效授权及消耗见唯一状态）
