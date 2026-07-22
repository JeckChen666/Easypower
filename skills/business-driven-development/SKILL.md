---
name: business-driven-development
description: Use when the user explicitly asks to turn a substantial business requirement into an approved spec and progressive plan for autonomous or subagent-driven implementation
---

# 业务驱动开发

## 核心原则

以可验收的业务闭环作为规划、实现和验证的基本单位。先与用户确认并批准 Spec（业务规格）和主 Plan（主执行计划），再自主完成授权范围；不要用技术任务、测试数量或代码完成度代替业务结果。

本 Skill 只在用户显式调用时运行。事实可从仓库和工具获取时直接调查；业务决策由用户确认；可逆且不改变业务契约的实现选择交给 Agent（执行代理）。

## 工作流

### 1. 编写 Spec

读取 [spec-protocol.md](references/spec-protocol.md)。探索现有系统后，与用户逐项确定：

- 业务目标、参与者和范围；
- 最小业务闭环；
- 业务规则、不变量和验收依据；
- 已纳入本次交付的增强能力；
- 质量属性和关键技术决策。

每次只讨论一个决策，并给出推荐答案。必须运行、操作或展示后才能判断时，明确调用 `$prototyping-decisions`；依赖外部事实时调用 `$researching-decisions`；业务术语、场景、边界或不变量存在多种解释时调用 `$modeling-business-domain`；涉及公共接口、计算、存储、迁移或系统结构的重要取舍时，明确调用 `$designing-business-architecture`。写入 `docs/easypower/<feature>/spec.md`，等待用户明确批准。

### 2. 编写渐进式 Plan

Spec 批准后读取 [plan-protocol.md](references/plan-protocol.md)。创建短小的 `plan.md` 作为执行地图，定义业务切片、依赖图、核心闭环里程碑、验收证据和自主执行边界。

大型工作只详细展开第一个可执行子 Plan；其他子 Plan 先保留目标、依赖和验收结果。Plan 可包含固定重要决策所必需的最小代码、伪代码、Schema 或接口，不提前书写普通实现。等待用户明确批准主 Plan。

### 3. 自主执行

Plan 批准后，明确调用 `executing-business-plans`，传递 Spec 和主 Plan 的路径。规划会话在此完成；执行 Skill 使用全新上下文恢复磁盘事实、展开子 Plan、调度子代理和交付业务证据。

如果当前环境没有 `executing-business-plans`，停止并说明缺少执行能力，不在本 Skill 中临时重建另一套执行流程。

### 4. 升级审批

以下情况暂停受影响任务并请求用户决定：

- 改变业务范围、验收标准或业务不变量；
- 改变已批准的公共接口、数据模型或关键架构；
- 缺少凭据、外部权限或不可恢复操作授权；
- 现有证据无法区分多个业务解释；
- 失败暴露出主 Plan 未覆盖的系统性风险。

仅细化实现步骤、修正局部缺陷或选择等价实现，不重新请求审批。

### 5. 交付报告

按 Spec 的业务目标报告核心闭环、增强项、证据、偏差、剩余风险和产物位置。使用“哪个业务场景通过了什么证据”，不要只报告测试命令为绿色。

## 快速判断

| 问题 | 归属 |
|---|---|
| 为什么做、做成什么、如何验收 | Spec |
| 按什么业务切片和依赖顺序交付 | 主 Plan |
| 当前切片如何实现和验证 | 子 Plan |
| 普通编码细节 | 执行 Agent |
| 新的业务或关键架构决策 | 升级给用户 |

## 常见错误

- 把数据库、后端、前端、测试拆成互不交付业务价值的水平任务。
- 在 Spec 中替用户决定尚未确认的角色、阈值或业务口径。
- 一开始写完所有子 Plan，导致后续计划依赖过期代码。
- 对同一业务结果在每个代码层重复测试。
- 核心闭环未通过就开始性能、交互或存储增强。
- 子代理发现重大歧义后自行选择一种解释继续执行。

需要完整示例时读取 [bi-report-example.md](references/bi-report-example.md)。
