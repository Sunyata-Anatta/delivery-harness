# 能力路由

按当前动作选择能力；先读运行时已暴露的名称、描述与来源，不预载技能正文。Skill、插件、MCP、CLI 是不同类型。默认零配置，已有能力能满足就复用；可选提供者缺失可降级，必需能力缺失则停在对应证据门。

## 选择顺序

1. 先筛任务、目录、语言、离线/数据边界、授权与兼容性；冲突约束不得被偏好覆盖。
2. 合格候选按当前用户选择 > 最具体目录绑定 > 项目 Resolver > 用户偏好 > profile 默认 > 新发现候选选择；同级不明确时只阻塞该选择。原生指令权限层级不变。
3. 只读取选中提供者的正文，验证真实调用。重名须解析来源与版本；disabled/冲突/未验证候选不自动提升默认。
4. 失败按已配置候选顺序回退，逐项重做约束与验证；不能降低必需能力验收。跨 Agent/主机重新解析工具与认证，旧主机成功不继承。

## 触发与分组

| 当前动作 | 能力候选组 |
|---|---|
| 查一手资料/版本 | research |
| 读代码/实现/排错 | engineering |
| 测试/真实证据/审阅 | verification |
| 文档/表格/幻灯片/图片 | documents |
| 安装/部署/发布 | operations |
| 领域格式/专有工作流 | domain |

组只缩小候选集，不授权、不整组加载；profile 也不是流程或权限替代。启动只评估当前相关信号；无信号写无，节点、目录、配置、版本、失败或任务类型变化时重评。只有选择变化/失败/用户要求解释时输出一行：`能力 -> 提供者(类型/来源)；依据；回退/限制`。

## 配置与提供者

[配置合同](routing-configuration.md) 定义 profile、目录覆盖、候选顺序和新技能接入；沿用覆盖层 Resolver，详情过长才移到唯一 `routing.md`，不另造执行器。

| 能力 | 类型与安装来源 | 降级 |
|---|---|---|
| Ponytail | 插件/Skill；DietrichGebert/ponytail | 最小实现人工审查 |
| Caveman | Skill/插件；JuliusBrussee/caveman | 简洁沟通 |
| Humanizer | Skill；blader/humanizer | 人工编辑非中文正文 |
| Humanizer-ZH | Skill；op7418/humanizer-zh | 人工编辑中文正文 |
| Context7 | MCP/CLI；upstash/context7 | 官方文档 |
| 文档解析 / book-to-skill | 工具/Skill；维护者见目录 | 关键页核对 |
| codebase-memory | MCP 配套 Skill；DeusData/codebase-memory-mcp | rg + 定点源码 |

中文正文 -> humanizer-zh；非中文正文 -> humanizer；混合文本按段落分别路由。只处理事实核对后的正文，代码、日志、证据、引用保真；中文目标缺失只人工编辑，不静默转通用 Humanizer。

仅在确需安装或调用细节时读[提供者目录](capability-catalog.md)相应小节。安装前请求授权（已有明确授权覆盖则复用），不静默安装。未知来源保持未安装，不编造命令。能力范围、数据、持久性或费用变化过门；配置变更不扩大授权。
