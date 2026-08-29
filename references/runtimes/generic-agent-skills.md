# 通用 Agent Skills 运行时契约

适用于声明兼容 Agent Skills 目录结构、但没有本 Skill 专用适配文件的主机。先读主机的一手文档和本机帮助；以下是最低互操作契约，不猜测产品命令。

## 安装

确认主机支持以目录为单位加载含 YAML frontmatter 的 `SKILL.md`。把本仓库根的四项复制到主机声明的用户级或项目级目录下，并保持目标目录名为 `delivery-harness`：

```text
delivery-harness/
  SKILL.md
  agents/
  assets/
  references/
```

主机若只接收单文件、会丢弃相对引用或要求执行脚本，本 Skill 不满足其安装契约；不要用部分复制冒充兼容。

## 发现与调用

使用主机的技能列表、检查或解析命令确认 `name: delivery-harness`。显式调用语法以本机帮助为准；调用内容使用“从当前现实开始，推进到已接受证据门通过”。

项目自动载入只写入主机明确会读的项目指令文件。目标文件不属于 `AGENTS.md` 或 `CLAUDE.md` 时，用 [restricted-runtime-entry.block.template.md](../../assets/restricted-runtime-entry.block.template.md) 替换占位符。

## 到达验证

1. 字节清单和逐文件哈希一致。
2. frontmatter 可解析，内部相对链接可达。
3. 主机列出并能显式调用本 Skill。
4. 若声称自动载入，全新会话中启动回执先于第一次工具调用；至少重复两次。

无法获得第三级证据时，只能写“文件已部署，运行时未验证”。

## 更新

保存旧版本或哈希，完整覆盖四项，清理主机明确声明的技能缓存，再重复发现与到达验证。不要只改入口文件而保留旧 references。

## 卸载与回滚

按主机文档只删除或注销 `delivery-harness`。同步处理项目入口块。回滚恢复完整四项并重启主机要求的新会话或进程。

## 已知边界

- “兼容 Markdown”不等于“兼容 Agent Skills”。
- 主机可能忽略 `agents/openai.yaml`，这不影响核心规则，但会失去 OpenAI 元数据。
- 目录优先级、热重载、调用前缀和信任模型没有跨主机统一保证。
- 没有一手文档或真实运行时证据时，不在支持矩阵中标成已验证。
