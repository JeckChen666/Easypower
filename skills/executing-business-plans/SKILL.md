---
name: executing-business-plans
description: Use when the user or another Easypower skill explicitly asks to execute an approved business Spec and main Plan across multiple tasks, contexts, or subagents
---

# 执行业务计划

## 核心原则

只执行已经批准的业务契约。以磁盘中的 Spec、主 Plan、子 Plan、代码和证据为事实来源；不要依赖上一段对话或 Agent 记忆。业务切片只有完成验收并留下证据后才算完成。

## 1. 启动检查

读取 Spec 和主 Plan 的完整文件，确认：

- 两者状态均为“已批准”或“执行中”；
- 核心业务闭环、切片依赖、验收摘要和自治边界存在；
- 当前仓库、环境、权限和基线可用；
- 没有需要用户先决定的阻塞问题。

任何前提不成立时不要开始实现。报告缺口并停在规划阶段。

## 2. 恢复执行状态

读取 [execution-state.md](references/execution-state.md)。以主 Plan 的状态表为执行账本，结合 Git 状态、子 Plan 和 `evidence/` 目录恢复真实进度。不要因为进程中断就重跑已验证任务，也不要把“代码存在”推断为“业务已经通过”。

重新计算执行前沿。优先领取核心业务闭环；它通过前不推进纯增强切片。

## 3. 按需展开子 Plan

一个切片即将进入 Ready 时，根据最新代码展开或刷新对应子 Plan。细化实现步骤不需要重新审批；改变业务范围、验收、不变量、公共接口、数据模型或关键架构时，将切片标为 Blocked 并升级审批。

## 4. 调度任务

读取 [agent-brief.md](references/agent-brief.md)。由协调 Agent 独占主 Plan、Spec 和跨切片公共契约的写权限。执行 Agent 只接收当前切片所需的事实链接、依赖产物、所有权、完成定义和升级条件。

只有任务之间不存在顺序依赖、公共契约争用、共享状态冲突和文件所有权重叠时才并行。存在共享接口或 Schema 时，先建立并完成契约冻结切片，或将相关任务串行化。

环境不支持子代理时，保持同一切片和状态协议顺序执行，不伪造独立代理或并行结果。

## 5. 完成切片循环

对每个已领取切片：

1. 确认基线和依赖证据仍然有效；
2. 实现最小完整业务路径；
3. 保存实现摘要和局部检查结果，将状态改为 Implemented；
4. 按 [validation-and-recovery.md](references/validation-and-recovery.md) 选择最少但充分的业务验证；
5. 回归已经成立的核心业务证据；
6. 验证通过后保存证据并依次改为 Verified、Completed；
7. 重新计算执行前沿并调度下一批任务。

不要为每个切片固定运行全量测试、双阶段评审或独立审查代理。验证和评审强度由业务风险、影响范围和证据可信度决定。

## 6. 处理失败和阻塞

局部实现或业务证据失败时，明确调用 `$diagnosing-business-failures`，传递 Spec、主 Plan、当前子 Plan、失败记录和证据路径。在任务 Brief 和执行更新中写出 Skill 名称，不要只写“交给诊断执行者”。诊断 Skill 建立业务反馈环、定位根因并在授权范围内修复；证据表明需要改变已批准契约时停止相关切片，不用临时绕过继续推进。

诊断返回后，由协调 Agent 核对原业务场景、回归证据和剩余风险，再恢复切片状态。止损措施、代码已修改或局部测试通过都不能直接把切片推进为 Completed。

一个切片 Blocked 时继续执行与它在依赖、契约、状态和所有权上独立的前沿任务。记录阻塞事实、影响、候选方案和恢复入口，等待用户决定。

## 7. 交付

所有可执行切片结束后，按 Spec 输出业务交付报告：

- 核心业务闭环及证据；
- 每个增强切片的状态和价值；
- Blocked、未开始和范围外项目；
- 计划偏差及审批情况；
- 实际运行的验证和产物位置；
- 用户回来后可以直接继续的恢复入口。

需要完整例子时读取 [bi-execution-example.md](references/bi-execution-example.md)。

## 常见错误

- 未检查 Spec/Plan 批准状态就开始编码。
- 把所有 Ready 标签当成并行安全，忽略共享 Schema 和文件所有权。
- 让执行 Agent 修改主 Plan 或公共契约。
- 把 Implemented 当成 Completed。
- 单个切片阻塞后停止所有独立工作。
- 中断恢复时依赖聊天摘要而不是磁盘事实。
- 用全量测试或代理数量代替业务验收证据。
