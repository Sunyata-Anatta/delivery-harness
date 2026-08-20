# 运行时安装与到达验证

本仓库根目录就是可安装的 Skill。`SKILL.md`、`agents/`、`assets/`、`references/` 构成唯一规范源；运行时适配层只说明发现路径、调用语法和生命周期，不复制执行规则。

本文中的运行时事实按各产品一手文档于 **2026-08-20** 复核。产品升级后先重查对应运行时文档，再修改命令。

## 运行时路由

| 运行时 | 典型安装入口 | 显式调用 | 详细契约 |
|---|---|---|---|
| Codex App、CLI、IDE | `$HOME/.agents/skills/delivery-harness` | `$delivery-harness` | [codex.md](runtimes/codex.md) |
| Claude Code | `$HOME/.claude/skills/delivery-harness` | `/delivery-harness` | [claude.md](runtimes/claude.md) |
| OpenClaw | `openclaw skills install git:<owner>/<repo>@<ref> --global` | `$delivery-harness`（可组合）或 `/delivery-harness` | [openclaw.md](runtimes/openclaw.md) |
| Hermes Agent | `$HOME/.hermes/skills/delivery-harness` | `/delivery-harness` | [hermes.md](runtimes/hermes.md) |
| 其他 Agent Skills 主机 | 主机声明的用户级或项目级目录 | 以主机帮助为准 | [generic-agent-skills.md](runtimes/generic-agent-skills.md) |

## 一次复制的边界

从干净检出的仓库根复制以下四项到名为 `delivery-harness` 的目标目录：

```text
SKILL.md
agents/
assets/
references/
```

不要复制 `.git/`、项目状态、开发测试、评审记录或本机缓存。仓库里若出现第二份 `SKILL.md`，先停止发布：那意味着规范源已经分叉。

## 项目自动载入

安装证明运行时可以发现 Skill；项目指令块让新会话在触碰项目时主动加载它。两者不能互相替代。

| 指令面 | 模板 |
|---|---|
| `AGENTS.md` | [AGENTS.block.template.md](../assets/AGENTS.block.template.md) |
| `CLAUDE.md` | [CLAUDE.block.template.md](../assets/CLAUDE.block.template.md) |
| 其他可持久读取的项目指令文件 | [restricted-runtime-entry.block.template.md](../assets/restricted-runtime-entry.block.template.md) |

缺块时追加；已有 `delivery-harness:start` / `delivery-harness:end` 时整块替换。不要创建运行时不会读取的占位文件来假装自动载入。运行时没有项目指令面时，保留显式调用并登记边界。

## 四级部署证据

部署验收从便宜、确定的检查开始，按风险逐级上升：

1. **字节级**：目标清单与源清单一致；逐文件哈希一致。证明复制没有缺页或漂移。
2. **内容级**：解析 frontmatter、内部链接和必需资源；专用验证器通过。证明内容结构可读。
3. **运行时级**：让目标运行时列出或解析 `delivery-harness`，再发一次显式调用。证明运行时真正发现了它。
4. **时序与统计级**：用全新会话验证启动回执先于第一次工具调用，并记录样本数、成功数、失败数和重复试验结果。证明强规则到达并稳定执行。

**文件存在不等于运行时读取；运行时列出不等于规则按时到达。** 发布至少做到前三层；声称自动载入有效时必须做到第四层。

每层记录源版本、目标运行时版本、判据、退出码或观察、样本数、时间和已知限制。诊断输出默认不落盘；需要归档时先脱敏。

## 共享更新规则

- 更新前保存旧目录哈希或可恢复副本。
- 用完整四项覆盖，不只替换 `SKILL.md`。
- 覆盖后复跑字节级、内容级和运行时级验证。
- 项目自动载入块若版本变化，按标记整块替换。
- 多个运行时共存时逐个验证，不能用一个运行时的成功代表全部。

## 共享卸载与回滚规则

- 卸载只移除目标运行时里的 `delivery-harness` 目录或注册项，不删除项目数据。
- 如果项目规则仍要求 Harness，先把自动载入块移除或改为新的入口，避免留下失效引用。
- 回滚使用更新前的完整副本，并复跑同级验证。
- 远端仓库重写、全局配置改变和第三方账号操作仍是独立权限门。

## 发布判据

发布前同时满足：根目录直接可安装；只有一个 `SKILL.md`；无执行脚本硬依赖；所有本地链接可达；五个运行时契约都覆盖安装、发现、到达、更新、卸载和边界；至少一个目标运行时完成真实调用；所有声称自动载入的运行时都有新会话时序证据。
