# AGENTS.md 自动载入块

把下面固定块追加到项目实际读取的 `AGENTS.md`；已有同名块时整块替换。**追加或整块替换**，不要保留两份。

```markdown
<!-- delivery-harness:start -->
本项目在 delivery-harness 下运行。首次触碰项目时，先读取已安装的 delivery-harness/SKILL.md，并按其要求输出启动回执。
活动节点、当次授权、已过证据门和待决断只写 `.delivery/state.md`；稳定规则、命令和 Resolver 写项目覆盖层。提交前同步两者涉及的事实。引用旧的外部状态前先用判据命令复验。
<!-- delivery-harness:end -->
```
