---
name: wayfinding-large-work
description: Use when the user explicitly asks to organize and progressively clarify a business initiative that is too large for one agent context and still too ambiguous for an approvable Spec or Plan, by maintaining a durable decision map, current frontier, dependencies, unresolved fog, and cross-session handoff
---

# 大型工作导航

## 核心原则

Wayfinding（大型工作导航）用于逐步找清通往可批准 Spec（业务规格）的路线，不提前执行整项工作。Decision Map（决策地图）保存 Destination（探索终点）、已决事项、Frontier（决策前沿）和 Fog（待澄清区域）；每次会话只展开并关闭一个重要决策，直到可以可靠进入业务规划。

本 Skill 只在用户显式调用时运行。它不是给普通功能增加仪式，也不是长期项目管理器。

## 1. 判断是否需要地图

同时满足以下条件才使用 Wayfinding：

- 目标或影响范围超过一个 Agent（智能体）上下文能够可靠容纳；
- 关键业务边界、口径、方案或依赖仍然模糊，当前无法写出可批准 Spec；
- 多个后续决策需要共享前序结论并跨会话恢复。

如果需求已经清楚但尚无已批准主 Plan，直接交给 `$business-driven-development`；只有磁盘中的 Spec 和主 Plan 都明确标记为已批准或执行中时，才交给 `$executing-business-plans`。用户说“需求已批准”不等于主 Plan 已批准，不要在拒绝建图后临时生成实现清单绕过规划审批。如果只是一个独立未知项，直接使用对应的研究、原型、领域或架构 Skill。不要为了保险创建大型地图。

## 2. 确认 Destination（探索终点）

先与用户确定 Destination：这轮探索结束时，哪些问题必须明确，才能开始编写 Spec。写明业务目标、成功边界、本轮不解决的内容和完成条件。Destination 不包含半年排期、完整架构或实现清单。

一次只推进一个会改变地图范围的问题，并给出推荐。用户批准 Destination 前不创建大量票据；以后改变 Destination、重要范围或完成信号必须重新取得批准。

## 3. 绘制概览地图

读取 [decision-map.md](references/decision-map.md)。广度优先扫描业务价值、领域语言、用户场景、外部事实、架构约束、迁移与运行风险，识别会阻止 Destination 的未知项，但不深入替它们作答。

将未知项分成：

- **Decision Ticket（决策票据）**：现在已经能精确写成一个问题，即使暂时受阻；
- **Fog（待澄清区域）**：知道方向存在，但还不能准确提出问题；
- **范围外**：不属于已批准 Destination，不会自动转为 Decision Ticket。

只创建当前能准确描述的 Decision Ticket，再建立真实依赖并根据依赖关系更新 Frontier。不要把半年工作一次性拆成实施任务，也不要用任意周数和阶段制造精确感。

默认保存到：

```text
docs/easypower/<initiative>/
├─ wayfinding.md
└─ decisions/
   ├─ D001-<decision>.md
   └─ D002-<decision>.md
```

项目已有合适的本地约定时沿用。只有用户明确要求且仓库已经配置 issue tracker 时才将地图写入外部系统；不要为使用本 Skill 先搭建追踪器。

## 4. 分类并分派决策

读取 [decision-ticket.md](references/decision-ticket.md)。每张票据只回答一个会改变后续路线的问题，并注明业务影响、输入、依赖、决策者、解决方法和完成证据：

- 业务范围或取舍：与用户逐项讨论；
- 术语、场景、边界和不变量：调用 `$modeling-business-domain`；
- 外部事实：调用 `$researching-decisions`；
- 必须运行或展示才可判断：调用 `$prototyping-decisions`；
- 重要系统取舍：调用 `$designing-business-architecture`；
- 取得访问、样本或事实的前置动作：最小 prerequisite，不交付 Destination 本身。

用户决策票据必须由用户确认，Agent 不得自问自答。互不依赖的研究票据可以由子代理并行处理；需要用户参与的讨论、原型和业务取舍保持可见，不伪装成后台自治。

## 5. 每次推进一个决策

读取 [frontier-and-recovery.md](references/frontier-and-recovery.md)。每个工作会话：

1. 先读取主地图，不加载所有票据；
2. 选择用户指定的票据，否则领取前沿中最高价值且未被占用的一张；
3. 在工作前记录 `Claimed（已领取）`、执行者和时间；
4. 只加载该票据依赖的已决结论和证据；
5. 使用指定方法取得事实、比较选项并推动决策；
6. 将完整结论留在票据，主地图只增加一行摘要与链接；
7. 重新计算依赖、Frontier 和 Fog，删除或降级已失效票据；
8. 留下下一会话可直接领取的入口。

默认一个会话只关闭一个决策。独立研究可以并行，但协调者仍负责合并冲突、更新地图和保护唯一权威来源。

## 6. 完成并交接

当所有阻止 Destination 的问题都已解决，Fog 不再包含会改变 Spec 的事项，并且用户确认路线已经清楚时，将地图标为 `Ready for Spec（可以编写业务规格）`。

明确调用 `$business-driven-development`，传递主地图和相关已决票据的路径。业务规划 Skill 重新组织并请求批准 Spec；不要把决策地图直接当成 Spec，也不要在 Wayfinding 中提前写完整 Plan 或开始生产实现。

## 完成条件

- Destination、范围和完成信号已由用户批准；
- 主地图是索引，不复制各票据的完整讨论；
- 当前 Decision Ticket、Fog 和范围外内容互不重叠；
- 每张票据是一个可决定的问题，而非实施切片；
- 依赖和 Frontier 由真实阻塞关系决定；
- 用户决策没有被 Agent 或子代理代替；
- 跨会话可从磁盘恢复已决结论、当前领取和下一入口；
- 进入 Spec 前不存在会改变业务边界的重要迷雾。

## 常见错误

- 对清晰的小功能建立跨会话地图。
- Destination 未批准就生成完整路线图和半年排期。
- 把数据库、后端、前端和测试拆成 Wayfinding 票据。
- 把尚不能准确提问的 Fog 伪装成详细任务。
- 在主地图复制所有票据正文，导致每次会话加载全部上下文。
- 一次解决多个人类决策，或让 Agent 替用户批准业务取舍。
- 为每轮会话创建 handoff、summary 和 progress 等重复文档。
- 地图仍有关键迷雾时就开始实施，或把地图直接当成已批准 Spec。
