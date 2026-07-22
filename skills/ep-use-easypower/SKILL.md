---
name: ep-use-easypower
description: Use when the user explicitly invokes ep-use-easypower or clearly asks to use Easypower, and the current context must be routed to the smallest suitable Easypower workflow
---

# 使用 Easypower

## 核心原则

只做一次 Route（路由）判断，然后进入最小且足够的下游 Skill。不要一次加载全部 Skill，不要因为用户提到 Easypower 就强制编写 Spec、Plan 或测试。

## 选择路径

先检查当前上下文、已有文档和用户目标，再选择一个主路径：

| 当前任务 | 主路径 |
|---|---|
| 清楚、局部、可逆的代码修改 | `$ep-code-change` |
| 清晰且需要正式规划的业务功能 | `$ep-planning` |
| 跨上下文且仍有多个重大未知项 | `$ep-large-project` |
| 已有批准的 Spec 和 Plan | `$ep-execution` |
| 外部需求、缺陷或 PR 尚未验证 | `$ep-request-intake` |
| 已出现业务结果错误或不稳定故障 | `$ep-diagnosis` |
| 产品形态、用户路径或操作效率不清楚 | `$ep-product-design` |
| 架构、领域、外部事实或运行原型是主要问题 | `$ep-architecture`、`$ep-domain-modeling`、`$ep-research` 或 `$ep-prototyping` |
| 已批准的多角色工作流需要执行 | `$ep-orchestration` |
| 已有交付需要独立检查 | `$ep-delivery-review` |

同时存在多个问题时，选择当前最先阻止业务推进的路径；下游 Skill 再按自身规则调用决策分支。只有缺少一个会改变主路径的关键信息时才提问。

## 交接

说明选择了哪个 Skill 及原因，然后只加载并遵循该 Skill。环境支持显式 Skill 调用时使用 `$skill-name`；否则读取同级目录中对应的 `SKILL.md`。不要复制下游工作流，也不要在下游已经运行后重新路由。

用户已经明确指定某个 Easypower Skill 时，尊重该选择；只有输入明显不满足其启动条件时说明缺口，不自行换成更重流程。

## 边界

- 普通问答、解释或状态查询不转成开发流程；
- 文件数量、代码行数和“权限”“金额”等词语不能单独决定任务大小；
- 清晰小改动保持快速，重要未决业务选择才升级；
- 本 Skill 不代替用户批准 Spec、Plan、生产操作或不可恢复动作。
