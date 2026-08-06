---
name: ep-orchestration
description: Use when running or designing a YAML multi-role workflow with subagents, decision gates, and recovery
weight: heavy
---

# 多角色工作流编排

## 不要进入本 Skill

- 已批准业务 Plan 的开发执行 → 走 `$ep-execution`
- 单次评审、简单交接或一个 Agent 直接能完成 → 不创建工作流
- 用同一会话依次模仿角色 → 不是真正的多 Agent 编排
- 业务问题不清、依赖未定义 → 先回到 `$ep-planning` 或 `$ep-large-project`

## 入口检查

- [ ] 任务需要多个独立角色（评审、研究、决策、合成）并行/串行协作
- [ ] 有可表达为 YAML 的 DAG（节点、依赖、Decision Gate、写入范围）
- [ ] 环境支持真实子代理
- [ ] 用户明确希望用本 Skill（不自动触发）

## 输出契约

- 已批准 `workflow.yaml` + 持久化 `state.json`
- 每个 Agent Step 的输出文件（`steps/<step-id>/output.md`）
- `summary.md`：完成、失败、受阻、跳过步骤 + 剩余 Decision Gate + 风险
- 跨会话恢复：磁盘状态 + Frontier 入口
- 详细协议见 [workflow-schema.md](references/workflow-schema.md)

## 核心原则

用声明式 DAG（有向无环图）协调真实子代理。角色是责任、权限和产出契约，不是主 Agent 临时切换的说话风格；协调 Agent 只管理状态、依赖、所有权和升级，不替角色完成任务。

本 Skill 只在用户显式调用时运行。已批准业务 Plan 的开发执行交给 `$ep-execution`；单次评审、简单交接或一个 Agent 能直接完成的任务不创建工作流。

## 1. 读取并批准工作流

读取 [workflow-schema.md](references/workflow-schema.md)。使用结构化 YAML Parser（解析器），验证版本、输入、角色、步骤、模板引用和执行策略。拒绝重复 ID、未知依赖、循环、未定义变量、缺失角色、重叠写入范围和未授权副作用。

用户没有提供 YAML 时，只生成满足当前目标的最小工作流。展示角色责任、DAG 层级、并行组、用户 Decision Gate（决策关口）、写入范围和最终产物，取得用户批准后再运行。普通事实可调查；角色权限、业务选择和外部副作用不得自行补全。

## 2. 建立持久化运行状态

沿用项目已有运行目录；没有约定时使用：

```text
docs/easypower/workflows/<name>/runs/<run-id>/
├─ workflow.yaml
├─ state.json
├─ steps/<step-id>/output.md
└─ summary.md
```

执行前保存已批准工作流和初始状态。`state.json` 记录步骤状态、执行者、attempt（尝试次数）、时间、产物、证据和阻塞原因。协调 Agent 独占该文件；子代理只写自己的输出范围并返回结果包。

## 3. 调度真实角色

根据依赖更新 Ready（可领取）步骤。只有依赖完成、输入可用、所有权无冲突且没有待处理 Decision Gate 时才调度。

每个 Agent Step（代理步骤）使用独立子代理，并接收：完整角色契约、渲染后的任务、直接依赖的产物路径和摘要、读写范围、完成定义、禁止决定的事项和升级条件。不要复制全部历史输出。

同一层步骤只有在文件、Schema（结构定义）、外部资源和决策权不冲突时才并行，并受 `max_parallel` 限制。环境不支持子代理时，停止并请求用户选择；未经允许不得把单模型角色扮演称为多 Agent 编排。

## 4. 验证状态转换

步骤使用 `Pending -> Ready -> Claimed -> In Progress -> Completed`，也可进入 `Blocked`、`Failed` 或 `Skipped`。子代理返回后，协调 Agent 检查产物、完成定义和证据，再写入 Completed；角色口吻正确不代表任务完成。

`user-gate` 步骤必须由用户关闭。多个 Agent 的一致意见不能代替用户批准。最终汇总需要在 YAML 中定义独立 Synthesis Step（汇总步骤），协调 Agent 不私自合并冲突结论。

## 5. 失败与恢复

失败步骤阻塞其后代，其他独立分支继续。只按已批准 retry（重试）策略重新调度，并保留每次失败证据；超时、取消和副作用不明时停止，不盲目重试。

中断后读取 `workflow.yaml`、`state.json` 和实际产物，核对仍在运行的 Agent 与失效的 Claim（任务占用记录），再从最后一个可证明状态继续。不要依赖聊天摘要，也不要因恢复而重跑已完成步骤。

所有步骤进入终态后，报告完成、失败、受阻和跳过的步骤，展示 `summary.md`、运行目录、未解决 Decision Gate 和剩余风险。

## 常见错误

- 用同一会话依次模仿角色，却宣称完成了多 Agent 编排。
- 只按 DAG 判断并行，忽略文件、Schema、外部资源和决策权冲突。
- 把全部上游输出拼进下游 Prompt（提示词），导致上下文持续膨胀。
- 运行结束才保存状态，进程中断后无法恢复。
- 自动生成复杂角色和步骤后不经用户批准就执行。
