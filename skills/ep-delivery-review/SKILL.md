---
name: ep-delivery-review
description: Use when the user or another Easypower skill explicitly asks to review a completed or high-risk business slice, branch, pull request, or delivery against an approved business contract and engineering risks
---

# 评审业务交付

## 不要进入本 Skill

- 低风险切片 + 已有直接业务证据 → 由 `ep-execution` 完成局部检查
- 还未实现完成的代码 → 不评审空壳
- 只是为了通过合并而走流程 → 不进入
- 与业务契约无关的纯代码风格讨论 → 留给 Code Review 工具

## 入口检查

- [ ] 已有可评审的实际代码差异、产物和证据
- [ ] Spec 已被批准或明确为"无法评估"
- [ ] 切片属于核心闭环、高风险、公共契约变化或最终交付
- [ ] 没有更好的入口（请求/缺陷验证走 `$ep-request-intake`,失败诊断走 `$ep-diagnosis`）

## 输出契约

- 业务契约检查：`Pass` / `Fail` / `Not assessable`
- 工程风险检查：`Pass` / `Fail` / `Pass with follow-ups`
- Findings 按 Blocker / Important / Minor / Question 排序
- 最终决定：`Approved` / `Approved with follow-ups` / `Not approved`
- 详细协议见 [business-contract-axis.md](references/business-contract-axis.md)、[engineering-risk-axis.md](references/engineering-risk-axis.md)、[feedback-and-gate.md](references/feedback-and-gate.md)

## 核心原则

评审分别回答两个问题：交付是否满足已批准的业务契约；实现是否带来不可接受的工程风险。测试通过、代码整洁或性能达标都不能抵消业务结果错误，业务路径通过也不能掩盖越权、数据丢失或不可恢复迁移。

本 Skill 不作为每个小改动的固定步骤。用户显式要求、核心闭环完成、高风险切片、公共契约变化或最终交付前才调用；低风险切片已有直接证据时，由执行流程完成局部检查即可。

## 1. 明确评审范围

读取 [review-scope.md](references/review-scope.md)。明确基线和当前版本、实际代码差异（diff）、产物、批准的 Spec（业务规格）与 Plan（执行计划）、证据目录、相关 ADR（架构决策记录）和仓库规范。不要只评审实现者摘要，也不要让未提交或范围外修改悄悄进入结论。

Spec 缺失或未批准时仍可检查工程风险，但 Contract Review（业务契约检查）只能标为 `Not assessable（无法评估）`，不能宣称交付完整。

## 2. 选择评审强度

按业务风险和影响范围决定方式：

- 文案、文档、低风险配置：单次针对性检查；
- 独立普通切片：Agent（协调代理）依次完成两类检查；
- 金额、权限、状态、一致性、迁移或公共接口：使用独立审查上下文，必要时并行完成两类检查；
- 跨模块、影响未知或最终发布：扩大调用方、兼容性、恢复和集成证据。

不要固定要求两个子代理、全量测试、多轮评审或三次重复运行。独立上下文用于降低确认偏差，不是工作量指标。

## 3. 检查业务契约

读取 [business-contract-axis.md](references/business-contract-axis.md)。逐项对照业务目标、核心闭环、规则、不变量、验收、增强范围和明确不做，检查：

- 要求是否完整实现，而非只有代码入口；
- 业务证据是否使用正确输入、版本、口径和环境；
- 实际结果是否满足期望、误差和失败语义；
- 是否存在遗漏、部分实现、范围漂移或未经批准的行为；
- 核心闭环在增强后是否持续成立。

证据不存在、过期或无法复现时，标记 Evidence Gap（证据缺口）。不要用测试数量代替业务结果。

## 4. 检查工程风险

读取 [engineering-risk-axis.md](references/engineering-risk-axis.md)。从实际代码差异、调用方和数据流出发，优先检查可能改变业务结果或恢复能力的问题：正确性、安全与权限、数据生命周期、并发与幂等、接口兼容、性能成本、失败恢复和可观测性。

仓库规范优先于通用偏好。工具已可靠执行的格式或静态规则不重复人工报告。代码气味只有在造成当前风险、修改扩散或验证困难时才成为 Finding（评审发现），不要为尚未出现的需求推动抽象。

## 5. 按业务影响定级

每个评审发现必须包含位置或证据、触发场景、业务影响和可验证的修复方向：

- **Blocker**：核心业务契约失败、安全/越权、资金或数据损失、不可恢复操作、证据链失真；
- **Important**：已批准增强缺失、可信回归风险、兼容/恢复/运维缺口，交付前应处理；
- **Minor**：范围内、低风险且值得当前成本的改进；
- **Question**：缺少事实，不能假装成缺陷。

不要把风格偏好定为 Blocker，也不要因改动看起来专业而降低真实业务失败的严重度。

## 6. 核验并处理反馈

读取 [feedback-and-gate.md](references/feedback-and-gate.md)。收到评审意见后，对照代码、契约、调用方和证据逐项判断 Accept、Reject、Defer 或 Need clarification。评审意见是待验证的技术主张，不是自动扩展范围的命令。

接受的评审发现按 Blocker、Important、Minor 顺序返回执行流程；实际业务故障明确调用 `$ep-diagnosis`。在后续记录和交付更新中写出 Skill 名称，不要只写“进入诊断流程”。评审发现必须改变 Spec、公共接口、Schema 或关键架构时升级用户审批。

## 7. 给出交付结论

先列 Findings（评审发现），按严重度排序并标明属于业务契约还是工程风险；没有评审发现时明确说没有发现问题。随后报告：

- Contract Review（业务契约检查）：`Pass（通过）`、`Fail（不通过）` 或 `Not assessable（无法评估）`；
- Engineering Risk Review（工程风险检查）：`Pass（通过）`、`Fail（不通过）` 或 `Pass with follow-ups（通过但需跟进）`；
- 证据缺口和剩余风险；
- 最终决定：`Approved（批准）`、`Approved with follow-ups（批准但需跟进）`、`Not approved（不批准）` 或 `Not assessable（无法评估）`；
- 修复后需要重验的业务场景和工程边界。

修复完成后只重验受影响的评审发现、原业务证据和必要回归；根因或影响范围扩大时再扩大审查。不要让评审形成无限循环。

需要完整示例时读取 [delivery-review-example.md](references/delivery-review-example.md)。

## 常见错误

- 只读测试摘要，不检查实际代码差异、产物和证据。
- 把业务契约检查与代码风格混成一个总分。
- 每个切片固定派两个评审代理或运行全量测试。
- 先列优点，把阻断问题埋在后面。
- 接受未来可能需要的抽象并扩大已批准范围。
- 没有 Spec 或可复现证据仍宣布可以交付。
- 修复评审意见后不重验原始业务闭环。
