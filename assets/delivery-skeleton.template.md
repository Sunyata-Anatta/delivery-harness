# `.delivery` 完整骨架

只有采用默认状态布局时，将同目录的 `delivery-skeleton/.delivery/` 复制到被治理项目根目录。若项目已有 `.delivery/`，逐文件合并，不覆盖现有状态或证据；已适配既有状态时跳过默认 `state.md` 创建，不整份复制。

完整的既有目录判定、父级忽略处理、合并矩阵和复验见 [项目初始化与安全合并](../references/project-initialization.md)。

骨架包含：

- [`state.md`](delivery-skeleton/.delivery/state.md)：随项目提交并持续填写的活动状态占位；
- [`.gitignore`](delivery-skeleton/.delivery/.gitignore)：忽略三个证据槽的实际内容，但保留目录占位；
- [`uploads/.gitkeep`](delivery-skeleton/.delivery/uploads/.gitkeep)：用户原始输入槽占位；
- [`artifacts/.gitkeep`](delivery-skeleton/.delivery/artifacts/.gitkeep)：生成物、测试材料与证据槽占位；
- [`debug/.gitkeep`](delivery-skeleton/.delivery/debug/.gitkeep)：诊断材料槽占位。

这只是状态与资源槽骨架；按 [资源归档](../references/execution.md#resource-storage) 在 `artifacts/<task>/` 有内容时才建 `tmp/` 与 `retained/`。
二者均受既有忽略规则保护，保留项不自动清理。完整接入按初始化参考填写 [覆盖层](project-overlay.template.md)、[项目地图](project-map.template.md) 与规则/README 入口。
已有同职责文件或章节直接适配，登记唯一入口，不新建第二套。

## 按需输出模板

以下模板不是骨架必装文件；有对应内容或压缩需要才使用，不在启动时批量复制空的 process、证据摘要或 README：

- [过程索引](process-index.template.md)：重要历史检查点、最近压缩回执与按需历史入口；
- [证据摘要](evidence-summary.template.md)：固定版本、范围、结论、限制与原始回执；
- [资源 README](artifact-readme.template.md)：用途、最新不可变批次、保留/恢复与批次清单入口。

按 [内容归属](../references/context-lifecycle.md#ownership) 复用既有入口；替换摘要前执行 [压缩与核验](../references/context-lifecycle.md#procedure)。
填入相对输出文件或明确工作面的已解析项目路径，并核对引用可达；输出不得依赖 Skill 源仓库的相对链接。
本说明的模板/合同链接属于已安装 Skill 的使用说明，不复制为项目文档依赖。

提交获授权时，按跟踪/隐私策略纳入状态、忽略规则、占位及批准的导航/规则文件。不要提交槽内真实内容，除非项目规则明确要求且已完成敏感信息检查。
