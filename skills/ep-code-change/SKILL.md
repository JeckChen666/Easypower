---
name: ep-code-change
description: Use automatically whenever the user asks to create, modify, fix, refactor, or delete source code, or make a bounded configuration, data, or developer operation, unless a specific Easypower workflow already governs the request; keeps bounded changes fast and routes unresolved business or architecture decisions to ep-use-easypower
---

# 轻量代码修改

## 先判断规模

满足以下条件时按 Quick Change（快速修改）直接完成：

- 目标和正确结果清楚；
- 检查代码后确认影响范围局部；
- 沿用现有业务规则、接口和架构；
- 没有需要用户选择的新业务口径；
- 修改可恢复，且能在当前上下文完成。

不要按敏感词机械升级。为指定用户赋予明确权限、修正一个确定数值、调整已确认公式或纠正明确状态，都可以是 Quick Change，前提是对象、结果、授权和影响范围清楚。该判断不扩大生产写入、不可恢复操作或外部权限的授权。

目标不清、需要定义或改变业务规则、影响公共接口或 Schema、涉及跨模块迁移、影响范围无法确认，或者需要跨上下文和多个 Agent 时，停止直接修改并明确调用 `$ep-use-easypower`。说明已知事实和升级原因，只交接一次。

## 快速完成

1. 读取相关代码和项目约定；
2. 做满足目标的最小完整修改，不顺带重构；
3. 默认不新增测试用例；
4. 已有测试覆盖被修改行为时，同步修改必要用例并运行最相关的测试，不删除、弱化或绕过原有保护；
5. 使用成本最低的直接证据检查结果，例如 diff、类型检查、局部运行或页面观察；
6. 简要报告修改、验证和未检查内容。

测试期望只有在用户要求的行为确实改变时才能更新，不要为了让测试通过而接受错误结果。用户明确要求新增测试或更广验证时，按用户要求执行。

## 优先级

用户已经明确调用 `$ep-use-easypower` 或其他具体 Easypower Skill 时，让该流程拥有控制权，不降低它的验证要求。由 `$ep-use-easypower` 选择本 Skill 时直接执行 Quick Change，不再路由回去。
