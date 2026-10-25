# 代码格式化流程

在项目第一次引入格式化工具，或代码里出现超长单行、需要一次性整理排版时读取。目标是让格式化成为一个可重放、可核对的机械动作：diff 最小、和逻辑改动分开、测试不因排版变化失效，并且以后不会再长出超长行。工具是随载荷分发的 [format_flow.py](format_flow.py)（标准库）与[行长守卫模板](../assets/line-length-guard.test.template.mjs)（Node 内置测试，无依赖）。

下文 `<skill>` 指安装后的 delivery-harness 目录，`<pre>` 指格式化前的提交。

## 1. 配置：固定版本、按现有风格取参数

1. 只读测量现有风格：`python -B -X utf8 <skill>/references/format_flow.py --root . style > .prettierrc.json`。标准错误输出给出引号、分号、缩进和 CRLF 的计数，核对后再用。
2. 生成的配置按多数派取引号、分号和缩进，并固定三项：`embeddedLanguageFormatting: "off"`（不格式化 HTML、CSS、SQL 等内嵌模板）、`endOfLine: "auto"`（不改动既有换行符）、`printWidth` 与守卫的行长上限相同（默认 100）。
3. 用 npx 调用固定版本，不写进 `package.json`、不新增依赖：`npx --yes prettier@3.3.3 --write <路径>`。版本号写进决策；升级版本等于重做本流程。
4. 生成文件、第三方代码和快照写进 `.prettierignore`。

## 2. 单独提交，并登记决策

1. 格式化前工作区必须干净；只运行上面的 npx 命令，不夹带任何手工修改。
2. 提交只含配置文件与格式化结果，提交信息写明工具与版本，例如 `style: mechanical formatting (prettier 3.3.3)`。逻辑改动、测试修正都放在后续提交。
3. 在[决策登记](../assets/decisions.template.md)新增一条，类型为「基线」，写明：格式化提交的编号、工具版本与配置、格式化之后所有发行包与文件的哈希都会变化，依赖旧哈希的引用自此失效。基线因这条决策改版。

## 3. 依赖源码排版的测试：先扫描，再逐一改写

1. 格式化前列出测试里读取源码文本的写法（`indexOf`、`includes`、`startsWith`、`endsWith`、正则 `.test`/`.match`）：`format_flow.py --root . markers --old HEAD --list`。只扫描读取了源码文件（`readFileSync` 等）的测试。
2. 格式化提交之后，找出「旧源码里有、新源码里没有」的标记：`format_flow.py --root . markers --old <pre>`。每一行 `LOST 文件:行号` 都要改。无法换算成 Python 正则的标记标为 `REVIEW`，逐个人工核对。
3. 改写为不依赖排版的写法：优先改成断言运行行为；必须读源码时，用允许空白变化的正则（例如 `/a:\s*1,\s*b:\s*2/`）。改完重跑第 2 步，直到 `RESULT: PASS`。
4. 之后不再新写依赖源码排版的测试；新测试断言行为。

## 4. 行长守卫测试

1. 把[守卫模板](../assets/line-length-guard.test.template.mjs)复制进项目测试目录，设置 `GUARD_ROOTS`（源码目录，逗号分隔）与 `GUARD_MAX`（等于 `printWidth`）。
2. 守卫先去掉字符串、模板字符串（含 `${...}` 内的表达式）、正则字面量和注释，再计算每行代码长度；所以长文案不会误报，真正的超长代码行一定报出。模板自带自测用例，覆盖这五种剥离与除号不被误认为正则。
3. 证明它会失败：在格式化前的提交上运行，必须红。按 [H6](hard-constraints.md#h6) 用分离工作树：`git worktree add --detach ../pre-format <pre>`，把守卫复制进去，运行 `node --test <守卫文件>`，确认退出码非 0，再 `git worktree remove ../pre-format`。这次结果作为一条 `[门结论]` 证据登记。
4. 在格式化后的提交上运行，必须绿。

## 5. 全量回归：把环境失败和真实失败分开

跑项目的全量测试，把失败分成两张清单报告：

| 类别 | 典型信号 | 处理 |
|---|---|---|
| 环境原因 | Docker 不可用；`EACCES`、`EPERM` 等权限错误；成片 `ECONNREFUSED`（本地数据库未运行）；浅克隆缺历史（`bad object`、`unknown revision`、`shallow`） | 修复环境后重跑同一批测试；修复前不能计为通过，也不能计为回归 |
| 真实失败 | 其余所有失败 | 按排错流程定位；格式化提交本身不得引入真实失败 |

两张清单都写进同一条证据，注明每条的判断依据。

## 6. 跨机器交付：重放格式化 + 小补丁

格式化结果是确定的，目标机不需要接收整个格式化后的代码包：

1. 在源机导出格式化之后的逻辑改动：`git format-patch <格式化提交>..HEAD -o <补丁目录>`。
2. 在目标机（已有 `<pre>`）建立分离工作树：`git worktree add --detach <临时路径> <pre>`；写入同一份配置，运行同一版本的 npx 命令。
3. 核对 tree 哈希：`format_flow.py --root <临时路径> tree --ref WORKTREE --expect <源机格式化提交的 tree 哈希>`；源机用 `git rev-parse <格式化提交>^{tree}` 取得期望值。不相等就停下，先查配置、版本或换行符差异。
4. 提交重放结果，`git am <补丁目录>/*.patch` 应用小补丁，再用 `tree --ref HEAD --expect <源机 HEAD 的 tree 哈希>` 核对最终结果。
5. 目标机的提交编号会和源机不同（作者时间不同），验收标准是 tree 哈希相等；确实需要相同提交编号时改用 `git bundle` 传输。
6. 在主工作树 `git merge --ff-only <提交>` 快进主线，`git worktree remove <临时路径>`。

## 注意事项

- Windows 检出的仓库在 Linux 挂载里做只读 git 操作时，带 `-c core.autocrlf=true`，否则会看到成百个假修改。`format_flow.py` 调用 git 时已经带上这个参数。
- 容器重启后本地 PostgreSQL 可能已经停掉；测试出现成片 `ECONNREFUSED` 时，先检查数据库是否在运行，再判断是不是回归。
- 目标工作区里有同名的未跟踪文件时，快进合并会被阻止。内容相同（哈希一致）就先删除该文件再合并；内容不同就停下询问，不覆盖。
- 浅克隆缺历史对象时，依赖历史的测试会报错。先 `git fetch --deepen=<有限深度>` 补取历史再判定，不要直接把这些失败记为回归。
