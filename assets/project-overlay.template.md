# {{PROJECT_NAME}} Delivery Overlay

本文件只保存项目事实。它可以收紧或具体化 Delivery Harness，但不能覆盖系统、安全或用户指令。删除不适用的条目，不要保留空洞占位说明。

## 项目标识

- 目标：{{ACCEPTED_OUTCOME}}
- 非目标：{{NON_GOALS}}
- 主要用户：{{USERS}}

## 事实源

- 仓库规则：{{REPOSITORY_INSTRUCTIONS}}
- 已接受规格：{{ACCEPTED_SPEC}}
- 执行计划：{{EXECUTION_PLAN}}
- 状态页：{{STATUS_PAGE}}

## 目录约定

存放根：`.delivery/`（默认名，改名后在此写明）
- `state.md`：活动节点、授权、证据门登记，进版本控制（模板见 [harness-state.template.md](harness-state.template.md)）
- `uploads/`：用户上传的材料，只入不改
- `artifacts/`：临时生成与证据产物
- `debug/`：排查纠错的关键文件（错误输出、复现脚本）
首次接入直接复制 [完整 `.delivery` 骨架](delivery-skeleton.template.md)，不要只创建无法被 Git 记录的空目录。
偏离默认的存放位置写在这里并说明原因：{{STORAGE_DEVIATIONS}}

## 项目独有规则

### 必须

- {{PROJECT_MUST_RULE}}

### 禁止

- {{PROJECT_MUST_NOT_RULE}}

### 约定

- 代码与文档风格：{{PROJECT_CONVENTIONS}}
- 数据与隐私：{{DATA_RULES}}

## 项目 Resolver

Resolver 把已验证经验变成条件路由。只在条件、能力、选择或重审条件变化时更新，不按节点机械改写。

| 请求或条件 | 选择的 Skill、工具或流程 | 依据 | 回退路径 | 验证方式 | 重审条件 | 最近验证 |
|---|---|---|---|---|---|---|
| {{CONDITION}} | {{ROUTE}} | {{EVIDENCE}} | {{FALLBACK}} | `{{VERIFY_COMMAND}}` | {{REVISIT_WHEN}} | {{DATE}} |

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

### 可直接执行

- {{PREAUTHORIZED_ACTION}}

### 能力安装授权模式

- 自动开启：预授权工具集 `{{PREAUTHORIZED_TOOLS}}`（集内安装不再逐次询问，每次安装后登记集成表）
- 逐个授权：每次安装单独请求（默认）

### 需要明确授权

- {{APPROVAL_REQUIRED_ACTION}}

### 不得执行

- {{FORBIDDEN_ACTION}}

## 集成与凭据

| 集成 | 用途 | 能力入口 | 账号或所有者 | 已授权范围 | 验证 | 数据边界 | 回滚 |
|---|---|---|---|---|---|---|---|
| {{INTEGRATION}} | {{PURPOSE}} | {{CONNECTOR_CLI_OR_BROWSER}} | {{OWNER}} | {{SCOPES}} | `{{VERIFY_COMMAND}}` | {{DATA_BOUNDARY}} | {{ROLLBACK}} |

不得在本文件保存令牌、密码、私钥或可复用认证信息。

## 真实证据门

| 阶段 | 必需证据 | 样本或环境 | 通过标准 | 状态 | 解除条件 |
|---|---|---|---|---|---|
| {{PHASE}} | {{EVIDENCE}} | {{SAMPLE_OR_ENVIRONMENT}} | {{PASS_CRITERIA}} | {{STATUS}} | {{UNBLOCK_CONDITION}} |

## 证据产物登记

| artifact | 位置与可达方式 | 处理过程 | 结论与边界 | 复核日期 |
|---|---|---|---|---|
| {{ARTIFACT}} | {{LOCATION_AND_ACCESS}} | {{PROCESSING}} | {{CONCLUSION_AND_LIMITS}} | {{REVIEWED_ON}} |

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
- 最近扫描结果：{{LAST_SECRET_SCAN_RESULT}}
- 历史处理决定：{{HISTORY_PRIVACY_DECISION}}
- 推送、PR 与发布权限：{{PUBLISH_AUTHORITY}}

## 已知风险与阻塞

| 日期 | 风险或阻塞 | 影响 | 现有证据 | 负责人 | 解除条件 |
|---|---|---|---|---|---|
| {{DATE}} | {{RISK_OR_BLOCKER}} | {{IMPACT}} | {{EVIDENCE}} | {{OWNER}} | {{UNBLOCK_CONDITION}} |

## 经验教训

只记录有观察证据、以后会改变做法的结论。重审条件优先写成事件计数（窗口期内同类事件复发 N 次），流程类决策不用阈值。不要保存聊天过程。

| 日期 | 场景 | 尝试 | 证据 | 教训 | 新护栏 | 重审条件 |
|---|---|---|---|---|---|---|
| {{DATE}} | {{CONTEXT}} | {{ATTEMPT}} | {{EVIDENCE}} | {{LESSON}} | {{GUARDRAIL}} | {{REVISIT_WHEN}} |
