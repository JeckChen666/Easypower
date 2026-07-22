---
name: ep-product-design
description: Use when the user or another Easypower skill explicitly asks to shape a software product before approving its Spec because important user journeys, information hierarchy, interaction states, or tradeoffs between user value, business scope, and architecture remain unclear
---

# 塑造产品体验

## 核心原则

先确定用户如何顺畅完成重要任务，再确定页面和实现。用真实用户证据约束角色判断；没有证据的内容标为 Assumption（待验证假设）。Agent（智能体）可以提出和比较产品方向，但最终产品形态由用户批准。

本 Skill 处理 Product Experience（产品体验）方法，`$ep-orchestration` 只处理角色调度。普通文案、视觉微调、已有明确交互的小改动和没有用户操作的后端任务不进入本流程。

## 1. 建立体验问题

读取 [experience-protocol.md](references/experience-protocol.md)。调查现有产品、用户反馈和项目约束，先明确：

- 主要用户、工作环境和高频任务；
- 当前路径、可观察阻力和业务影响；
- 必须决定的产品形态；
- 已知事实、用户证据、约束和待验证假设；
- 什么结果足以批准或否决一个方案。

不要把 Persona（用户画像）或角色 Prompt（提示词）当成用户证据。缺少关键证据时，明确调用 `$ep-research`、请求用户补充，或将问题保留为待验证假设。

## 2. 选择评审深度

单一、低风险且可逆的问题由主 Agent 直接分析。用户价值、交互和架构之间存在重要冲突时，读取 [role-contracts.md](references/role-contracts.md)，明确调用 `$ep-orchestration`，并让用户先批准角色、轮次、输入和产物。

默认使用 Product Lead（产品负责人）、User Advocate（用户代表）、Interaction Designer（交互设计师）和 Architect（架构师）。根据问题删减角色，不为凑人数建立工作流。User Advocate 只能依据提供的证据模拟任务，不能自称真实用户。

## 3. 有限轮次形成方案

按以下顺序推进，不进行开放式无限讨论：

1. 各角色独立分析相同事实，分别提交发现和依据；
2. 汇总冲突，区分用户阻力、业务取舍、交互问题和技术约束；
3. 形成 2–3 个结构明显不同的候选产品形态；
4. 使用相同高频任务走查每个方案，覆盖正常、空、加载、错误、权限和恢复状态；
5. Product Lead 汇总推荐、代价、假设和未解决分歧；
6. 用户在 Decision Gate（决策关口）批准、拒绝或要求验证。

默认最多进行两轮角色复审。两轮后仍无法区分方案时，补充用户证据或明确调用 `$ep-prototyping` 制作可操作原型，不继续消耗讨论轮次。

## 4. 形成体验契约

按 [experience-protocol.md](references/experience-protocol.md) 记录批准结论。简单功能直接写入 Spec（业务规格）的产品体验部分；复杂功能可暂存为 `docs/easypower/<feature>/experience.md`，批准后将稳定结论压缩回 Spec，避免形成第二份长期业务规格。

体验契约至少固定主要用户、关键任务、目标路径、信息优先级、关键状态、效率要求、被否决方案、待验证假设和原型结论。不要提前写普通组件、接口、数据库或生产代码。

## 5. 交还主流程

用户批准后，将业务可见的体验规则和验收方式回写 Spec；架构约束交给 `$ep-architecture`；必须运行后判断的问题交给 `$ep-prototyping`。然后返回 `$ep-planning` 继续 Spec 和 Plan，不在本 Skill 中接管实现。

## 完成条件

- 关键用户任务和当前阻力有事实或明确假设；
- 候选方案使用相同任务和状态比较；
- 推荐同时说明用户价值、业务代价和技术约束；
- 真实用户未知项没有被 Agent 角色掩盖；
- 用户批准产品方向，结论已回写 Spec。

## 常见错误

- 让“真实用户 Agent”凭空代表真实用户。
- 角色互相附和，没有独立首轮和证据引用。
- 只比较颜色和装饰，不比较信息层级与操作顺序。
- 架构成本直接否决用户需求，或用户愿望完全忽略系统约束。
- 角色不断讨论，却没有原型、用户证据或 Decision Gate。
