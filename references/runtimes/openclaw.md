# OpenClaw 运行时契约

依据 OpenClaw 的 [Skills CLI 文档](https://docs.openclaw.ai/cli/skills)；事实复核日期：2026-08-20。

## 安装

本仓库根有 `SKILL.md`，可作为 Git 源直接安装：

```bash
openclaw skills install git:<owner>/<repo>@<ref> --global
```

安装当前本地检出：

```bash
openclaw skills install . --global
```

省略 `--global` 时按 OpenClaw 当前工作区或 Agent 范围安装；需要指定 Agent 时使用该版本帮助中声明的 Agent 选项。先运行 `openclaw skills install --help` 核对本机版本，不把帮助输出中的凭据值带入记录。

## 发现与调用

```bash
openclaw skills info delivery-harness --json
openclaw skills check --json
```

然后在新会话用可组合的显式引用调用：

```text
$delivery-harness 从当前现实开始，推进到已接受证据门通过。
```

独立命令形式 `/delivery-harness ...` 也可用；需要在一条提示中组合多个 Skill 时优先 `$delivery-harness`。

若 OpenClaw 工作区有可持久读取的项目指令文件，使用 [restricted-runtime-entry.block.template.md](../../assets/restricted-runtime-entry.block.template.md)；没有就登记为显式调用模式。

## 到达验证

1. `skills info` 返回准确名称、来源和可用状态。
2. `skills check` 无缺失依赖。
3. 显式调用能读到本 Skill 的启动固定块。
4. 声称自动载入时，用全新会话证明回执先于第一次工具调用，并重复至少两次。

安装命令退出零但 `skills info` 找不到目标，仍判失败。

## 更新

Git 或本地安装不假设具备 ClawHub 的跟踪更新语义。用同一来源重新安装，必要时按当前 CLI 帮助使用覆盖选项；更新前记录旧来源与版本，更新后重新执行 `info`、`check` 和显式调用。

## 卸载与回滚

先用 `openclaw skills --help` 或版本对应文档确认卸载子命令和范围，再只卸载 `delivery-harness`。回滚时从旧 Git ref 或完整副本重新安装。全局与 Agent 级安装分别清理，避免旧副本遮蔽结果。

## 已知边界

- OpenClaw CLI 选项会随版本变化，执行前以本机 `--help` 为判据。
- ClawHub 更新语义不能自动套到 Git 或本地来源。
- 工作区、Agent 和全局可同时存在同名 Skill；验证时记录实际解析来源。
- 远端 Git 安装涉及网络与外部来源，按授权门执行。
