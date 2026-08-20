# 项目初始化与安全合并

项目首次接入 Delivery Harness，或需要修复已有 `.delivery/` 时读取。目标是可重复执行、零数据损失：新目录可整份复制；已有目录只做类型安全的增量合并，**不得整目录覆盖**。

## 选择交付面

- 中文项目使用 [中文骨架](../assets/delivery-skeleton.template.md)、[中文状态模板](../assets/harness-state.template.md) 和 [中文覆盖层模板](../assets/project-overlay.template.md)。
- 英文项目从 [英文初始化参考](en/project-initialization.md) 进入，只使用 `assets/en/`。
- 项目锁定的语言同时约束状态占位、覆盖层和自动载入块。

## 预检

1. 确认项目根、仓库规则、Git 状态和覆盖层声明的存放偏离。
2. 只检查 `.delivery/` 及预期子路径的存在性、类型和文件名；不读取或外发槽内内容。
3. `.delivery` 是符号链接或重解析点时，不跟随写入；记录解析目标并进入权限或项目决策门。
4. `.delivery`、`uploads`、`artifacts` 或 `debug` 同名但不是目录时，停止该路径的初始化；不得改名、删除或替换现有对象。

## 合并矩阵

| 观察 | 动作 |
|---|---|
| `.delivery/` 不存在 | 复制锁定语言的完整骨架。 |
| `.delivery/` 已存在 | 保留目录及全部内容，逐项执行下列规则；不得整目录覆盖。 |
| `state.md` 不存在 | 复制锁定语言的状态占位。 |
| `state.md` 已存在 | 保留原文；只在语义明确时把缺失标题追加为新节。事实冲突进入决策门，不重写旧内容。 |
| `.gitignore` 不存在 | 复制骨架规则。 |
| `.gitignore` 已存在 | 只增不删：保留顺序和原规则，仅追加缺失的槽位规则，不制造重复行。 |
| 槽位不存在 | 创建目录并加入 `.gitkeep`。 |
| 槽位已是目录 | 保留全部内容；缺 `.gitkeep` 时补入，不移动、不读取、不删除内容。 |
| 预期目录位置是其他对象 | 停止该路径，报告对象类型和需要的项目决策。 |

任何项目明确偏离默认槽位或跟踪策略时，以覆盖层登记的决定为准；该决定若让 `state.md` 无法进入版本控制，就不能声称 Harness 状态契约已经安装。

## 父级忽略规则

`.delivery/.gitignore` 只有在父目录未被整体忽略时才生效。初始化前运行：

```text
git check-ignore -v .delivery/state.md
```

无输出且退出码为 1，表示未跟踪的 `state.md` 可进入 Git。已有文件可用 `git check-ignore -v --no-index .delivery/state.md` 复核。若命中父级 `.delivery/` 规则，先按输出定位控制文件；项目没有明确偏离时，在该项目的版本化忽略面末尾加入最窄的反向规则：

```gitignore
!.delivery/
!.delivery/.gitignore
!.delivery/state.md
!.delivery/uploads/
!.delivery/uploads/.gitkeep
!.delivery/artifacts/
!.delivery/artifacts/.gitkeep
!.delivery/debug/
!.delivery/debug/.gitkeep
```

随后分别用 `git check-ignore -v --no-index .delivery/uploads/__delivery_probe__`、`git check-ignore -v --no-index .delivery/artifacts/__delivery_probe__` 和 `git check-ignore -v --no-index .delivery/debug/__delivery_probe__` 验证槽内普通内容仍被骨架规则忽略。探针路径不需要实际创建文件。

## 相关项目文件

把覆盖层模板复制到项目实际使用的文档或规则目录，删除不适用占位并填写稳定事实；复制后的覆盖层不依赖 Skill 内相对链接。把匹配语言的 `AGENTS.md`、`CLAUDE.md` 或受限运行时标记块追加到运行时真实读取的项目指令文件；已有同名标记块时整块替换。

## 完成判据

1. `.delivery/state.md`、`.delivery/.gitignore` 和三个 `.gitkeep` 存在；原文件和槽内内容零删除、零覆盖。
2. `git diff -- .delivery` 只显示已批准的新增或追加；`git status --short -- .delivery` 可解释。
3. `state.md` 不被忽略，三个槽内普通内容被忽略。
4. 重新执行同一初始化流程；第二次重复执行不产生新差异。
5. 提交前检查实际暂存清单，只提交状态、忽略规则和占位；槽内真实内容按项目规则与敏感信息门处理。
