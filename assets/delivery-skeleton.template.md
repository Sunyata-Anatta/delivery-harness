# `.delivery` 完整骨架

只有采用默认状态布局时，将同目录的 `delivery-skeleton/.delivery/` 复制到被治理项目根目录。若项目已有 `.delivery/`，逐文件合并，不覆盖现有状态或证据；已适配既有状态时跳过默认 `state.md` 创建，不整份复制。

完整的既有目录判定、父级忽略处理、合并矩阵和复验见 [项目初始化与安全合并](../references/project-initialization.md)。

骨架包含：

- [`state.md`](delivery-skeleton/.delivery/state.md)：随项目提交并持续填写的活动状态占位；
- [`.gitignore`](delivery-skeleton/.delivery/.gitignore)：忽略三个证据槽的实际内容，但保留目录占位；
- [`uploads/.gitkeep`](delivery-skeleton/.delivery/uploads/.gitkeep)：用户原始输入槽占位；
- [`artifacts/.gitkeep`](delivery-skeleton/.delivery/artifacts/.gitkeep)：生成物与证据槽占位；
- [`debug/.gitkeep`](delivery-skeleton/.delivery/debug/.gitkeep)：诊断材料槽占位。

这只是状态与临时槽骨架；完整接入还需按初始化参考填写 [覆盖层](project-overlay.template.md)、[项目地图](project-map.template.md) 与规则/README 入口，并复用或建立过程记录。已有同职责文件直接适配，不新建第二套。

提交获授权时，按跟踪/隐私策略纳入状态、忽略规则、占位及批准的导航/规则文件。不要提交槽内真实内容，除非项目规则明确要求且已完成敏感信息检查。
