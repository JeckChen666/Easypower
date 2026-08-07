---
name: ep-request-intake
description: Use when evaluating external requests, bugs, issues, or PRs into durable business briefs for planning
weight: heavy
---

# 业务请求分流

## 不要进入本 Skill

- 没有外部请求（issue/PR/缺陷/支持升级）→ 不要凭空分流
- 提交者建议的技术方案被直接当需求 → 不要照单全收
- 已有批准 Spec/主 Plan → 走 `$ep-execution`,不需要再分流
- 已经活跃生产故障 → 走 `$ep-diagnosis`,不放在请求队列

## 入口检查

- [ ] 有外部请求或缺陷输入（issue、PR、邮件、缺陷报告）
- [ ] 尚未验证业务主张（事实依据、价值、范围）
- [ ] 用户明确要求评估或分流
- [ ] 没有更好的入口（活跃故障走 `$ep-diagnosis`,清晰需求走 `$ep-planning`,模糊大目标走 `$ep-large-project`）

## 输出契约

- 单一状态：`Needs Evidence` / `Needs Business Decision` / `Ready for Planning` / `Route to Existing Capability` / `Duplicate` / `Active Incident` / `Deferred` / `Rejected`
- 优先级理由（影响、范围、频率、时效性、替代路径）
- `Ready for Planning` 项：Business Brief（业务问题 + 已验证事实 + 期望结果 + 验收契约 + 范围外 + 风险）
- 不修改外部系统状态除非用户明确授权
- 详细协议见 [intake-and-verification.md](references/intake-and-verification.md)、[routing-states.md](references/routing-states.md)、[business-brief.md](references/business-brief.md)

## 核心原则

Triage（需求分流）用于判断外部请求的类型、事实依据、业务价值、信息缺口和下一步负责人。先验证业务主张，再给出分流结论；不要把提交者建议的技术方案直接当成需求，也不要把信息完整的 Business Brief（业务简报）当成已批准的 Spec（业务规格）或 Plan（执行计划）。

本 Skill 只在用户显式调用时运行。默认执行只读调查和本地输出；修改外部标签、评论、状态、关闭请求或改动 PR 必须在用户明确授权后执行。

## 1. 读取完整请求

读取原始描述、附件、评论、状态、作者、时间、关联条目和已有处理记录；PR 还要读取实际代码差异（diff）与评审。记录请求来源和当前状态，避免把转述摘要当成完整事实。

从请求中分开：

- 受影响的业务参与者和工作流；
- 提交者观察到的现象；
- 提交者期望的业务结果；
- 提交者建议的解决方案；
- 声称的影响、范围和紧迫性；
- 已有证据与仍属推测的内容。

先给出候选类别：Defect（缺陷）、Enhancement（增强需求）、Operational/Support（运营或支持）或 External Change（外部变更）。类别用于选择验证方法，不强迫所有请求落入缺陷或增强需求两类。

## 2. 调查项目事实

读取 [intake-and-verification.md](references/intake-and-verification.md)。在向提交者提问前，先从代码、配置、运行证据、业务文档、领域词汇、已有 Spec/ADR、历史请求和产品现状中查明能查的事实。

至少检查：

- 同一业务能力是否已经存在，只是入口、权限或文档不清楚；
- 是否与已有请求、已批准计划或历史拒绝决定重复；
- 当前系统实际行为是否与报告一致；
- 期望行为是否已有业务契约支持；
- 建议方案是否只是众多实现选择之一。

按业务概念搜索，不只匹配提交者用词。不要因为没找到关键词就断言功能不存在。

## 3. 验证主张

缺陷优先在最高且稳定的业务接口，用最小代表数据复现“输入、期望、实际、差异”。无法稳定复现的间歇问题可以用日志、关联 ID、时间窗和不变量建立证据，不要求先变成确定性单元测试。

增强请求先验证业务问题和价值，不验证提交者预选的架构。明确哪个用户在什么场景受阻、当前替代方案、发生频率、损失或收益，以及什么结果足以解决问题。

外部 PR 同时验证业务意图与 diff：它是否解决声称的问题、是否违反权限/数据/兼容边界、相关验证是否足够。测试通过不能替代业务授权。

涉及正在发生的金额、权限、数据损坏、安全或大面积可用性风险时，不等待普通队列补齐信息；将状态设为 `Active Incident（正在发生的生产事故）`，明确调用 `$ep-diagnosis` 建立止损措施和反馈闭环。

## 4. 给出一个分流状态

读取 [routing-states.md](references/routing-states.md)。每个请求只给一个当前状态和推荐理由：

- `Needs Evidence（需要证据）`：关键主张无法验证；
- `Needs Business Decision（需要业务决策）`：事实足够，但价值、范围或口径需要用户决定；
- `Ready for Planning（可以进入规划）`：业务问题、边界和验收依据足以进入 Easypower 规划；
- `Route to Existing Capability（转用现有能力）`：产品已支持，问题出在发现、权限、配置或使用；
- `Duplicate（重复请求）`：已有活动请求或已批准工作覆盖；
- `Active Incident（正在发生的生产事故）`：需要立即止损和诊断；
- `Deferred（延期）`：有价值，但当前时机、依赖或容量不满足；
- `Rejected（拒绝）`：明确不符合业务方向、风险边界或已有长期决定。

不要用虚假的数值评分掩盖业务判断。优先级至少说明受影响业务、严重度、范围、频率、时间敏感性、替代路径和不处理的后果；缺证据时降低置信度，不把嗓门当优先级。

先向用户推荐类别、状态、理由和下一动作。除非用户已经明确要求应用某项外部变更，否则等待确认后再改标签、评论、关闭或合并。

## 5. 只追问阻塞信息

Agent（智能体）能从仓库、附件或只读工具查到的事实直接调查。必须由业务方确认时，每次只问一个会改变状态、优先级或 Brief 内容的问题，并给出推荐选项。

`Needs Evidence` 问题必须具体可执行，例如租户/环境、关联 ID、时间窗、脱敏样本、操作步骤、期望公式或用户可见差异。不要丢给提交者一份通用二十项问卷，也不要重复询问已有评论已经回答的内容。

## 6. 编写 Business Brief

只有达到 `Ready for Planning` 才读取 [business-brief.md](references/business-brief.md) 并写 Brief。Brief 记录业务问题、已验证事实、期望结果、场景、验收契约、范围外和风险，不预写普通实现步骤。

阻塞性业务决定必须在 Brief 前解决；无法阻止规划的未知项可以明确保留，并写出谁在何时用什么证据关闭。Brief 应能跨几天或代码移动后继续使用，优先引用稳定业务接口与权威产物，避免依赖行号或聊天记忆。

## 7. 交给下游

Business Brief 是规划输入，不是开发授权：

- 范围清楚且可在正常规划上下文处理：调用 `$ep-planning` 形成并批准 Spec 与 Plan；
- 超过一个上下文且仍有多个相互依赖的重大未知项：调用 `$ep-large-project`；
- 已存在明确批准的 Spec 和主 Plan：调用 `$ep-execution`；
- 活跃业务故障：调用 `$ep-diagnosis`；
- 已有能力、重复、延期或拒绝：记录依据和恢复条件，不创建实施 Plan。

不要仅凭外部 issue、PR、需求邮件或 Business Brief 直接编码。

## 完成条件

- 原始请求、观察、期望和建议方案已经分离；
- Agent 先查明可从项目获得的事实，再向人提问；
- 当前行为、业务影响和证据强度有明确结论；
- 重复、已有能力和历史决定已经检查；
- 请求只有一个当前状态，且优先级理由可解释；
- `Ready for Planning` 项有可验收、非程序化的 Business Brief；
- 外部系统没有未经确认的状态变更；
- 下游不会绕过 Spec 和 Plan 审批。

## 常见错误

- 看到“Kafka”“重写”“加缓存”等词就按指定方案建任务。
- 未复现缺陷或核对业务契约就标记可开发。
- 要求提交者提供代码库中本可直接查明的信息。
- 为低风险请求固定跑全量测试，或为截图不足的报告猜根因。
- 把已有功能误判为新需求，重复实现。
- 用优先级分数代替影响、范围和时效判断。
- Brief 写成文件和行号清单，或包含大量未批准实现代码。
- 自动评论、改标签、关单或合并外部 PR。
