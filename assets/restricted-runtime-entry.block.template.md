# 受限运行时自动载入块

把下面固定块追加到 `{{RUNTIME_INSTRUCTION_FILE}}`；已有同名块时整块替换。**追加或整块替换**，不要保留两份。若运行时没有可持久读取的项目指令文件，只保留手动调用路径，并把此项记为已知边界。

```markdown
<!-- delivery-harness:start -->
本项目在 delivery-harness 下运行。首次触碰项目时，先读取已安装的 delivery-harness/SKILL.md，并按其要求输出启动回执。
活动节点、当次授权、已过证据门和待决断只写 `.delivery/state.md`；稳定规则、命令和 Resolver 写项目覆盖层。提交前同步两者涉及的事实。引用旧的外部状态前先用判据命令复验。
<!-- delivery-harness:end -->
```
