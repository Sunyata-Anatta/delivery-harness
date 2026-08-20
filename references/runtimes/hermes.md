# Hermes Agent 运行时契约

依据 Hermes Agent 的 [Skills 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)；事实复核日期：2026-08-20。

## 安装

稳定的用户级路径是 `$HOME/.hermes/skills/delivery-harness`。从本 Skill 根复制 `SKILL.md`、`agents/`、`assets/`、`references/` 四项。

项目级可放在 `<project>/.agents/skills/delivery-harness`，然后从该项目根信任整个项目：

```bash
hermes skills trust
```

Hermes 支持 Hub 和直接 URL 等来源，但默认 tap 约定从仓库的 `skills/` 路径发现多 Skill。这个仓库故意采用根目录单 Skill，因此不要把默认 tap 当作根仓库的零配置安装方案。

## 发现与调用

```bash
hermes skills list
hermes skills inspect delivery-harness
```

新会话显式调用：

```text
/delivery-harness 从当前现实开始，推进到已接受证据门通过。
```

项目指令入口取决于 Hermes 当前可达的指令面；存在时使用 [restricted-runtime-entry.block.template.md](../../assets/restricted-runtime-entry.block.template.md)，不存在时登记显式调用边界。

## 到达验证

1. 逐文件哈希证明四项复制完整。
2. `skills list` 与 `skills inspect` 返回实际来源及信任状态。
3. 显式调用出现本 Skill 的启动固定块。
4. 自动载入声明必须用全新会话顺序证据，并至少重复两次。

目录可读但未 trust 的项目 Skill，不算可执行安装。

## 更新

本地复制来源用完整四项覆盖；Hub 来源用当前 Hermes 版本提供的 check/update 流程。更新后再次 inspect，并核对实际解析来源没有被另一个 external directory 同名副本遮蔽。

## 卸载与回滚

本地复制只移除准确目标目录；Hub 安装使用 Hermes 的卸载命令。回滚恢复完整旧副本或旧版本。项目级信任和入口块按实际配置撤销，不能只删除用户级副本。

## 已知边界

- 项目级 Skill 需要显式 trust；目录存在不代表可执行。
- external directories 可能引入同名遮蔽和可写来源风险，必须记录实际来源。
- 默认 tap 的 `skills/` 布局与本仓库根目录单 Skill 不同；若未自定义 tap 路径，不作兼容承诺。
- 直接 URL 安装需要验证所有相对引用资源都被获取；只取 `SKILL.md` 会造成不完整安装。
