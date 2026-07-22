# Easypower

Easypower 是一个以业务结果为核心的 Code Agent Skill 仓库。它面向需要先审核业务 Spec 和渐进式 Plan，再交给 Agent 或子代理持续执行的开发任务。

## 当前进度

Easypower 目前有九个正式 Skill：

- [business-driven-development](skills/business-driven-development/SKILL.md)：与用户形成并批准业务 Spec 和渐进式 Plan；
- [executing-business-plans](skills/executing-business-plans/SKILL.md)：在全新上下文中消费已批准的 Spec 和 Plan，持续执行并留下业务证据。
- [designing-business-architecture](skills/designing-business-architecture/SKILL.md)：围绕业务负载比较计算、存储、接口和迁移方案，形成可批准的架构决定。
- [diagnosing-business-failures](skills/diagnosing-business-failures/SKILL.md)：从错误业务结果、间歇故障或性能退化建立反馈环，定位根因并证明恢复。
- [reviewing-business-delivery](skills/reviewing-business-delivery/SKILL.md)：分别审查业务契约符合度、工程风险和交付证据可信度。
- [prototyping-decisions](skills/prototyping-decisions/SKILL.md)：用一次性逻辑、UI 或技术原型回答一个必须运行后才能判断的问题。
- [researching-decisions](skills/researching-decisions/SKILL.md)：基于第一方来源调查外部事实，形成可引用的业务决策证据。
- [modeling-business-domain](skills/modeling-business-domain/SKILL.md)：用具体场景统一业务语言、边界和不变量，并限制 ADR 膨胀。
- [wayfinding-large-work](skills/wayfinding-large-work/SKILL.md)：为跨上下文且尚无法形成 Spec 的大型目标维护决策地图和未知前沿。

Wayfinding、规划与执行 Skill 组成大型模糊目标到业务交付的完整链路；架构、研究、原型、领域建模、诊断和评审 Skill 只在相应的重要决策、业务失败或交付门出现时进入。后续还会继续加入其他实际工作场景的独立 Skill。

新 Skill 不直接复制 Superpowers 或 mattpocock-skill。每个能力都需要结合实际工作方式重新定义触发边界、业务价值和验证方式，并通过独立场景测试后才进入 `skills/`。

完整候选能力、来源映射和建设顺序见 [Easypower Skill 能力地图](SKILL-MAP.md)。

它解决以下问题：

- 日常对话不应自动进入重型开发流程；
- Spec 应先固定业务目标、规则和验收依据；
- Plan 应按端到端业务切片组织，而不是按技术层拆分；
- 大型 Plan 应使用主 Plan 和按需子 Plan 渐进展开；
- 核心业务闭环应先完成并验证，再推进增强能力；
- 测试强度应由业务风险和影响范围决定；
- 用户批准范围内可以由子代理持续执行，重大变化必须升级审批。

## 调用方式

安装或加载需要的 Skill 目录，然后显式调用：

```text
$business-driven-development
$executing-business-plans
$designing-business-architecture
$diagnosing-business-failures
$reviewing-business-delivery
$prototyping-decisions
$researching-decisions
$modeling-business-domain
$wayfinding-large-work
```

示例：

```text
使用 $business-driven-development 和我梳理这个功能的业务 Spec 与渐进式 Plan，批准后再组织子代理执行。

使用 $executing-business-plans 执行 docs/easypower/sales-report/ 中已经批准的 Spec 和主 Plan。

使用 $designing-business-architecture 比较这个报表功能的计算、查询和存储架构，并形成可批准的决定。

使用 $diagnosing-business-failures 从这份错误业务结果建立反馈环，定位根因并验证修复。

使用 $reviewing-business-delivery 对照批准的业务契约和工程风险评审这次交付。

使用 $prototyping-decisions 构建最小原型来回答这个业务决策问题。

使用 $researching-decisions 调查这个决定依赖的外部事实，并区分事实、推论和未知项。

使用 $modeling-business-domain 通过具体场景澄清这个功能的业务术语、边界和不变量。

使用 $wayfinding-large-work 为这个跨上下文且仍然模糊的业务目标建立决策地图。
```

九个 Skill 都在各自的 OpenAI 元数据中设置了：

```yaml
policy:
  allow_implicit_invocation: false
```

因此不会因为普通问答或简单代码请求自动进入完整工作流。

## 工作方式

```text
业务调查
  -> Spec 审批
  -> 主 Plan 审批
  -> 核心业务闭环
  -> 增强切片
  -> 业务证据报告
```

完整说明见 [Easypower 工作流](SKILL-WORKFLOW.md)。

按需参考协议：

- [Spec 协议](skills/business-driven-development/references/spec-protocol.md)
- [Plan 协议](skills/business-driven-development/references/plan-protocol.md)
- [BI 报表规划示例](skills/business-driven-development/references/bi-report-example.md)
- [执行状态协议](skills/executing-business-plans/references/execution-state.md)
- [风险验证与恢复](skills/executing-business-plans/references/validation-and-recovery.md)
- [业务架构决策框架](skills/designing-business-architecture/references/decision-framework.md)
- [业务失败反馈环](skills/diagnosing-business-failures/references/feedback-loops.md)
- [业务契约评审轴](skills/reviewing-business-delivery/references/business-contract-axis.md)
- [逻辑原型协议](skills/prototyping-decisions/references/logic-prototype.md)
- [研究来源与证据等级](skills/researching-decisions/references/source-evidence.md)

## 仓库结构

```text
skills/
├─ business-driven-development/  # 形成业务 Spec 和渐进式 Plan
├─ executing-business-plans/     # 消费已批准 Plan 并持续执行
├─ designing-business-architecture/ # 比较并批准重要架构决定
├─ diagnosing-business-failures/ # 从业务失败证据诊断并恢复
├─ reviewing-business-delivery/  # 审查业务契约和工程风险
├─ prototyping-decisions/        # 用一次性原型回答决策问题
├─ researching-decisions/        # 用一手来源形成决策证据
├─ modeling-business-domain/     # 用场景澄清领域语言与边界
└─ wayfinding-large-work/        # 为大型模糊目标维护决策地图

references/
└─ superpowers-zh/
   └─ skills/                    # 旧 Superpowers 中文译版，仅作参考

tests/
├─ business-driven-development/  # 规划 Skill 的前向测试场景
├─ executing-business-plans/     # 执行 Skill 的前向测试场景
├─ designing-business-architecture/ # 架构 Skill 的前向测试场景
├─ diagnosing-business-failures/ # 诊断 Skill 的前向测试场景
├─ reviewing-business-delivery/  # 评审 Skill 的前向测试场景
├─ prototyping-decisions/        # 原型 Skill 的前向测试场景
├─ researching-decisions/        # 研究 Skill 的前向测试场景
├─ modeling-business-domain/     # 领域建模 Skill 的前向测试场景
└─ wayfinding-large-work/        # 大型工作导航 Skill 的前向测试场景
```

`skills/` 是 Easypower 正式 Skill 的唯一发布目录。`references/` 下的内容不参与安装或 Skill 发现。

## 参考来源

- [Superpowers 中文译版](references/superpowers-zh/README.md)：保留原有中文翻译，供行为比较和机制迁移；
- `superpowers/`：本地原版克隆，由 `.gitignore` 排除；
- `mattpocock-skill/` 与 `mattpocock-skill-zh/`：本地对比仓库，由 `.gitignore` 排除。

参考来源用于提取可复用思想，不决定 Easypower 的 Skill 数量、触发方式或工作流结构。

## 验证

[规划场景测试](tests/business-driven-development/scenarios.md) 覆盖三类核心用法：

- 有黄金目标数据的 BI 报表；
- 没有现成目标产物的权限功能；
- 需要多个子代理持续执行的大型功能。

[执行场景测试](tests/executing-business-plans/scenarios.md) 覆盖：

- 核心闭环完成后再推进增强；
- Ready 任务之间存在公共 Schema 冲突；
- 中断恢复、局部业务阻塞和独立任务继续执行。

`executing-business-plans` 已通过上述三个隔离前向场景，以及一次从规划批准到执行交接的组合测试。

[架构场景测试](tests/designing-business-architecture/scenarios.md) 覆盖 BI 计算与查询负载、订单定价模块边界，以及大 JSON 的渐进存储演进。该 Skill 已通过三个隔离前向场景。

[诊断场景测试](tests/diagnosing-business-failures/scenarios.md) 覆盖黄金报表差异、低概率重复扣款和 Schema 迁移后的性能退化。该 Skill 已通过三个隔离前向场景。

[评审场景测试](tests/reviewing-business-delivery/scenarios.md) 覆盖业务结果失败、工程风险阻断和低风险外部反馈核验。该 Skill 已通过三个隔离前向场景。

[原型场景测试](tests/prototyping-decisions/scenarios.md) 覆盖业务逻辑口径、现有页面 UI 方案和应先调查的供应商能力。该 Skill 已通过三个隔离前向场景。

[研究场景测试](tests/researching-decisions/scenarios.md) 覆盖供应商能力、未指定框架的版本升级，以及必须运行验证的 Excel 算法等价问题。该 Skill 已通过三个隔离前向场景。

[领域建模场景测试](tests/modeling-business-domain/scenarios.md) 覆盖 SaaS “账号”歧义、报表定义/计算/发布混用，以及 ADR 过度记录。该 Skill 已通过三个隔离前向场景。

[大型工作导航场景测试](tests/wayfinding-large-work/scenarios.md) 覆盖 ERP 替换、模糊 BI 平台统一和不应建图的清晰小功能。该 Skill 已通过三个前向场景，小功能入口经一次修订后复测通过。

新增或修改正式 Skill 时，应先观察无 Skill 的基线行为，再使用相同场景进行前向验证。
