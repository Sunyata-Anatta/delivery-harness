# AGENTS.md 自动载入块

把下面固定块追加到项目实际读取的 `AGENTS.md`；已有同名块时整块替换。**追加或整块替换**，不要保留两份。

```markdown
<!-- delivery-harness:start -->
本项目在 delivery-harness 下运行。首次触碰项目时，先读取已安装的 delivery-harness/SKILL.md，并按其要求输出启动回执。
活动节点、授权边界和证据门记录在项目覆盖层；提交前同步当前状态。引用旧的外部状态前先用判据命令复验。
<!-- delivery-harness:end -->
```
