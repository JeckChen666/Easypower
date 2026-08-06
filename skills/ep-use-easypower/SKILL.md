---
name: ep-use-easypower
description: Use when the user explicitly invokes ep-use-easypower or clearly asks to use Easypower, and the current context must be routed to the smallest suitable Easypower workflow
---

# 使用 Easypower

> 任务形态（阶段/规模/模式）的概念框架见 [Easypower 任务形态](../../TASK-SHAPE.md)。本 Skill 负责按当前上下文选择最小且足够的下游 Skill。

## 核心原则

只做一次 Route（路由）判断，然后进入最小且足够的下游 Skill。不要一次加载全部 Skill，不要因为用户提到 Easypower 就强制编写 Spec、Plan 或测试。

**默认倾向"轻量",不要因为流程更"安全"就升级到重型 Skill。**

## 信号路由

优先按可观察信号路由,而不是按抽象原则。每条信号独立判断,命中多个时按"最先阻止业务推进的"选择。

| 信号 | 主路径 |
|---|---|
| 用户一句话能描述目标 + 改动局部 + 可恢复 + 不改变业务规则 | `$ep-code-change` |
| 磁盘中存在 `docs/easypower/*/spec.md` 且状态为"已批准",同时主 Plan 已批准 | `$ep-execution` |
| 输入含 issue / PR / 缺陷报告 / 外部需求,业务主张尚未验证 | `$ep-request-intake` |
| 已有业务结果错误、间歇故障、性能退化或回归证据 | `$ep-diagnosis` |
| 单一业务功能,边界基本清晰,可在一次规划内形成可批准 Spec | `$ep-planning` |
| 跨上下文、边界和迁移顺序仍模糊,无法写可批准 Spec | `$ep-large-project` |
| 多角色评审 / 研究 / 决策需要 YAML DAG 协调 | `$ep-orchestration` |
| 已完成切片或 PR 需要独立审查业务契约和工程风险 | `$ep-delivery-review` |
| 用户路径、信息层级、交互形态存在多种合理方案 | `$ep-product-design` |
| 决策依赖外部事实(官方能力、版本兼容、协议、SDK) | `$ep-research` |
| 必须运行、操作或观看后才能判断的状态/计算/交互 | `$ep-prototyping` |
| 业务术语、场景、边界或不变量存在多种合理解释 | `$ep-domain-modeling` |
| 公共接口、计算、存储、迁移、系统结构难以逆转 | `$ep-architecture` |
| 其他 | `$ep-code-change`(默认)+ 用户澄清 |

## 反例库(误路由陷阱)

以下输入看起来像 A,但实际应该走 B。命中反例时优先走实际路径。

| 输入特征 | 看起来像 | 实际应走 | 原因 |
|---|---|---|---|
| "为指定用户 X 赋予 Y 角色,授权已确认" | 权限修改 → 重型流程 | `$ep-code-change` | 对象/结果/授权/影响范围都清楚,无歧义 |
| "把按钮文案从 X 改为 Y" | 文案修改 → 走规划 | `$ep-code-change` | 局部、可逆、无业务规则变化 |
| "修一个生产 bug,有日志和错误截图" | Bug 修复 → 走规划 | `$ep-diagnosis` | 已有失败证据,根因未知 |
| "查清楚这个 API 的限制" | 研究 → 重型流程 | `$ep-research` | 单纯事实调查,无需规划/评审 |
| "做一个原型看下哪个方案好" | 原型 → 走规划 | `$ep-prototyping` | 一次性验证,不写生产代码 |
| "已经批准了 Plan,接着干" | 执行 → 走规划 | `$ep-execution` | Plan 已批准,不要再规划 |
| "统一多个系统" | 大目标 → 走规划 | `$ep-large-project` | 跨上下文且仍模糊 |
| "评审一下这个 PR" | 评审 → 走规划 | `$ep-delivery-review` | 不需要先做 Spec |
| "看看用 Redis 还是 Postgres" | 选型 → 走研究 | `$ep-architecture` | 涉及计算/存储取舍 |
| "这个术语到底指什么" | 术语 → 走研究 | `$ep-domain-modeling` | 业务语言歧义 |

**反例库会随真实使用持续扩充,新增反例需通过 `tests/routing-evals.json` 验证。**

## 路由决策流程

1. **检查输入文件**:磁盘中是否有 Spec / Plan / issue / 证据?
2. **匹配可观察信号**:按上表从上到下匹配,第一个命中即采用
3. **检查反例库**:命中反例则改走实际路径
4. **遇到歧义**:只在缺少一个会改变主路径的关键信息时提问,否则按默认(轻量)选择
5. **不要重复路由**:下游 Skill 已经在运行时不再重新路由

## 交接

说明选择了哪个 Skill 及原因,然后只加载并遵循该 Skill。环境支持显式 Skill 调用时使用 `$skill-name`;否则读取同级目录中对应的 `SKILL.md`。不要复制下游工作流,也不要在下游已经运行后重新路由。

用户已经明确指定某个 Easypower Skill 时,尊重该选择;只有输入明显不满足其启动条件时说明缺口,不自行换成更重流程。

## 边界

- 普通问答、解释或状态查询不转成开发流程
- 文件数量、代码行数和"权限""金额"等词语不能单独决定任务大小
- 清晰小改动保持快速,重要未决业务选择才升级
- 本 Skill 不代替用户批准 Spec、Plan、生产操作或不可恢复动作
- 默认倾向"轻量",避免为了显得"安全"而升级流程