# {{PROJECT_NAME}} 项目地图

只保留骨架与按需入口。启动遵循 [项目规则]({{RULES_PATH}})；唯一状态由 [项目覆盖层]({{OVERLAY_PATH}}) 解析。按当前任务选入口，不递归展开全部链接。

## 骨架

```text
项目根/
├── README.md                 简介与地图入口
├── {{PROJECT_MAP_PATH}}      骨架与导引
├── {{RULES_PATH}}            项目规则
└── {{GOVERNANCE_ROOT}}/      状态、过程与指针
{{EXISTING_COMPONENT_ROWS}}
```

## 按需导引

| 当前需要 | 读取入口与范围 |
|---|---|
| 继续工作、核对授权 | [唯一活动状态]({{ACTIVE_STATE_PATH}})：当前节点、本动作授权与证据门 |
{{TASK_ROUTE_ROWS}}

地图不存进度、SHA、测试结果或授权副本。仅在入口、职责或读取触发变化时更新。
