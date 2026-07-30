# Easypower

[![skills.sh](https://skills.sh/b/JeckChen666/Easypower)](https://skills.sh/JeckChen666/Easypower)
[![License](https://img.shields.io/github/license/JeckChen666/Easypower)](LICENSE)

Easypower 是一个以业务结果为核心的 Code Agent Skill 仓库。它将复杂开发任务组织为可审核的业务 Spec（业务规格）、渐进式 Plan（执行计划）和可验证的业务闭环，再由 Agent 或子代理持续推进交付。

它适合需要保留人类决策权、又希望将已批准范围交给 Agent 自主执行的团队：小修改快速完成；较大功能先澄清业务、用户体验和架构取舍；大型模糊目标先建立决策地图，而不急于编写实现清单。

## 正式 Skill

Easypower 目前有十五个正式 Skill：

- [ep-use-easypower](skills/ep-use-easypower/SKILL.md)：在用户明确要求使用 Easypower 时，根据上下文选择最小且足够的正式流程。
- [ep-code-change](skills/ep-code-change/SKILL.md)：自动区分快速代码或开发操作和需要正式规划的复杂任务，避免为小改动机械新增测试。
- [ep-planning](skills/ep-planning/SKILL.md)：与用户形成并批准业务 Spec 和渐进式 Plan；
- [ep-execution](skills/ep-execution/SKILL.md)：在全新上下文中消费已批准的 Spec 和 Plan，持续执行并留下业务证据。
- [ep-architecture](skills/ep-architecture/SKILL.md)：围绕业务负载比较计算、存储、接口和迁移方案，形成可批准的架构决定。
- [ep-diagnosis](skills/ep-diagnosis/SKILL.md)：从错误业务结果、间歇故障或性能退化建立 Feedback Loop（反馈闭环），定位根因并证明恢复。
- [ep-delivery-review](skills/ep-delivery-review/SKILL.md)：分别审查业务契约符合度、工程风险和交付证据可信度。
- [ep-prototyping](skills/ep-prototyping/SKILL.md)：用一次性逻辑、UI 或技术原型回答一个必须运行后才能判断的问题。
- [ep-research](skills/ep-research/SKILL.md)：基于第一方来源调查外部事实，形成可引用的业务决策证据。
- [ep-domain-modeling](skills/ep-domain-modeling/SKILL.md)：用具体场景统一业务语言、边界和不变量，并限制 ADR 膨胀。
- [ep-large-project](skills/ep-large-project/SKILL.md)：为跨上下文且尚无法形成 Spec 的大型目标维护决策地图和未知前沿。
- [ep-request-intake](skills/ep-request-intake/SKILL.md)：验证外部需求、缺陷和 PR 的业务主张，并形成可交给规划流程的 Business Brief。
- [ep-product-design](skills/ep-product-design/SKILL.md)：基于用户证据、多角色评审和任务走查确定可批准的产品形态。
- [ep-orchestration](skills/ep-orchestration/SKILL.md)：用持久化 DAG、真实子代理和 Decision Gate 运行多角色工作流。
- [ep-chinese-writing](skills/ep-chinese-writing/SKILL.md)：约束面向用户的中文解释和工程文档，保留专业英文并在首次出现时补充中文意译。

需求分流、Wayfinding、规划与执行 Skill 组成外部请求或大型模糊目标到业务交付的完整链路；架构、研究、原型、领域建模、诊断和评审 Skill 只在相应的重要决策、业务结果异常或交付判断中进入。后续能力只根据真实使用反馈扩展。

新 Skill 不直接复制 Superpowers 或 mattpocock-skill。每个能力都需要结合实际工作方式重新定义触发边界、业务价值和验证方式，并通过独立场景测试后才进入 `skills/`。

完整候选能力、来源映射和建设顺序见 [Easypower Skill 能力地图](SKILL-MAP.md)。

它解决以下问题：

- 日常对话不应自动进入重型开发流程；
- 清晰、局部且可逆的代码修改应快速完成，不机械新增测试；
- Spec 应先明确业务目标、规则和验收依据；
- 重要用户路径和产品形态应在 Spec 批准前完成走查；
- Plan 应按端到端业务切片组织，而不是按技术层拆分；
- 大型 Plan 应使用主 Plan 和按需子 Plan 渐进展开；
- 核心业务闭环应先完成并验证，再推进增强能力；
- 测试强度应由业务风险和影响范围决定；
- 用户批准范围内可以由子代理持续执行，重大变化必须升级审批。

## 安装

### Codex Plugin（推荐）

Easypower 以一个包含十五个 Skill 的 Codex Plugin（插件）发布。推荐从 GitHub Marketplace Source（插件源）整体安装：

```powershell
codex plugin marketplace add JeckChen666/Easypower --ref main
codex plugin add easypower@easypower
```

本地开发时，可以把第一条命令中的仓库地址换成 Easypower 的绝对路径。修改 Plugin 后，运行以下命令刷新来源并重新安装：

```powershell
codex plugin marketplace upgrade easypower
codex plugin add easypower@easypower
```

安装或更新后开启新对话，使 Codex 重新加载 Skill。使用 `$ep-use-easypower` 作为统一入口；也可以用 `$` 直接选择任意 `ep-*` Skill。

### Skills CLI

需要在 Skills CLI 支持的其他 Agent 中安装时，使用：

```powershell
npx skills add JeckChen666/Easypower
```

在交互界面选择需要的 `ep-*` Skill。该安装方式与 Codex Plugin 分发相互独立；前者使用通用 Agent Skills 目录，后者提供 Codex 的 Plugin 安装与 UI 元数据。

本仓库在 [skills.sh](https://skills.sh/JeckChen666/Easypower) 上的搜索和安装统计由 Skills CLI 的匿名安装 telemetry（安装遥测）自动建立。完整机制、排查步骤和本地扫描命令见 [skills.sh 收录说明](SKILLS-SH.md)。

### 兼容性

| 环境 | 支持情况 |
|---|---|
| Codex CLI、IDE Extension（IDE 扩展） | 支持显式和隐式 Skill 调用 |
| ChatGPT Desktop / Codex App | 支持 Plugin 安装和 Skill UI 元数据 |
| 不支持子代理的环境 | 规划和普通执行仍可使用；`ep-execution` 按顺序执行，不伪造并行 |
| MCP 或外部服务 | Easypower 本身无强制依赖；具体项目权限仍由用户和运行环境提供 |

## 调用方式

安装 Plugin 后，可以显式调用：

```text
$ep-use-easypower
$ep-code-change
$ep-planning
$ep-execution
$ep-architecture
$ep-diagnosis
$ep-delivery-review
$ep-prototyping
$ep-research
$ep-domain-modeling
$ep-large-project
$ep-request-intake
$ep-product-design
$ep-orchestration
$ep-chinese-writing
```

示例：

```text
使用 $ep-use-easypower 判断这个任务应该进入哪个 Easypower 流程。

使用 $ep-code-change 快速完成这个局部代码修改，并按现有测试情况选择验证。

使用 $ep-planning 和我梳理这个功能的业务 Spec 与渐进式 Plan，批准后再组织子代理执行。

使用 $ep-execution 执行 docs/easypower/sales-report/ 中已经批准的 Spec 和主 Plan。

使用 $ep-architecture 比较这个报表功能的计算、查询和存储架构，并形成可批准的决定。

使用 $ep-diagnosis 从这份错误业务结果建立反馈闭环，定位根因并验证修复。

使用 $ep-delivery-review 对照批准的业务契约和工程风险评审这次交付。

使用 $ep-prototyping 构建最小原型来回答这个业务决策问题。

使用 $ep-research 调查这个决定依赖的外部事实，并区分事实、推论和未知项。

使用 $ep-domain-modeling 通过具体场景澄清这个功能的业务术语、边界和不变量。

使用 $ep-large-project 为这个跨上下文且仍然模糊的业务目标建立决策地图。

使用 $ep-request-intake 验证这个外部请求并形成可交给规划流程的 Business Brief。

使用 $ep-product-design 和我确定这个功能的用户路径与产品形态。

使用 $ep-orchestration 运行这个已批准的多角色 YAML 工作流。

使用 $ep-chinese-writing 检查这段技术中文的术语和表达。
```

除 `ep-code-change` 和 `ep-chinese-writing` 外，其余十三个 Skill 都设置了：

```yaml
policy:
  allow_implicit_invocation: false
```

因此不会因为普通问答或简单代码请求自动进入完整工作流。`ep-use-easypower` 只在用户显式调用或明确要求使用 Easypower 时进行智能路由。

`ep-code-change` 和 `ep-chinese-writing` 设置 `allow_implicit_invocation: true`。前者只为代码修改选择 Quick Change（快速修改）或升级路径，后者只调整表达；两者都保持简短，不自动启动完整业务工作流。

## 语言约定

Easypower 保留工程团队常用的英文术语，第一次出现时使用 `English（中文）`，后文固定使用英文或已约定的中文简称。例如：`Spec（业务规格）`、`Plan（执行计划）`、`Business Brief（业务简报）`、`Wayfinding（大型工作导航）`。API、JSON、HTML 等通用缩写只在含义可能不清楚时解释，不逐处机械翻译。

具体约束见 [自然技术中文 Skill](skills/ep-chinese-writing/SKILL.md)。

状态名保持英文原值，避免文档与状态机不一致，并在状态定义处补充中文，例如 `Ready（可领取）`、`Blocked（受阻）`、`Completed（已完成）`。普通动作和判断使用自然中文，避免逐字翻译英文流程名。

## 工作方式

```text
业务调查
  -> 产品体验塑造（按需）
  -> Spec 审批
  -> 主 Plan 审批
  -> 核心业务闭环
  -> 增强切片
  -> 业务证据报告
```

完整说明见 [Easypower 工作流](SKILL-WORKFLOW.md)。

按需参考协议：

- [Spec 协议](skills/ep-planning/references/spec-protocol.md)
- [Plan 协议](skills/ep-planning/references/plan-protocol.md)
- [BI 报表规划示例](skills/ep-planning/references/bi-report-example.md)
- [执行状态协议](skills/ep-execution/references/execution-state.md)
- [风险验证与恢复](skills/ep-execution/references/validation-and-recovery.md)
- [业务架构决策框架](skills/ep-architecture/references/decision-framework.md)
- [Feedback Loop（业务反馈闭环）](skills/ep-diagnosis/references/feedback-loops.md)
- [业务契约评审轴](skills/ep-delivery-review/references/business-contract-axis.md)
- [逻辑原型协议](skills/ep-prototyping/references/logic-prototype.md)
- [研究来源与证据等级](skills/ep-research/references/source-evidence.md)
- [Product Experience Contract（产品体验契约）](skills/ep-product-design/references/experience-protocol.md)

## 仓库结构

```text
.codex-plugin/plugin.json       # Plugin 清单与版本
.agents/plugins/marketplace.json # GitHub 与本地安装入口
skills/                         # 十五个正式 Skill
tests/                          # 场景与路由 Eval
scripts/validate_repo.py        # 跨平台仓库校验
```

`skills/` 是 Easypower 正式 Skill 的唯一发布目录。根目录的 Plugin 清单只分发该目录；本地 `references/` 已由 `.gitignore` 排除，不参与 Git、安装或 Skill 发现。

## 参考来源

- [obra/superpowers](https://github.com/obra/superpowers) (基于 2026-07-23 前的提交 `d884ae04edebef577e82ff7c4e143debd0bbec99`)：提供规划、执行、调试和评审机制的对比基线；
- [mattpocock/skills](https://github.com/mattpocock/skills) (基于 2026-07-23 前的提交 `ed37663cc5fbef691ddfecd080dff42f7e7e350d`)：提供领域建模、研究、原型和大型工作导航等行为参考；
- [jnMetaCode workflow-runner](https://github.com/jnMetaCode/superpowers-zh/blob/main/skills/workflow-runner/SKILL.md)：提供 YAML 多角色工作流的参考实现。
- [agency-orchestrator](https://github.com/jnMetaCode/agency-orchestrator)：提供角色库、工作流和编排引擎分离的参考设计。

参考来源用于提取可复用思想，不决定 Easypower 的 Skill 数量、触发方式或工作流结构。完整归属说明见 [Third-party notices](THIRD_PARTY_NOTICES.md)。

## 验证

每次提交先运行结构校验：

```powershell
python scripts/validate_repo.py
```

该命令检查 Plugin、Marketplace、Skill 元数据、触发策略、交叉引用、本地链接和路由 Eval 的结构。CI 会运行同一命令。`tests/routing-evals.json` 保存两个入口的最小可移植评估语料，不在 CI 中调用付费模型或把非确定性模型输出伪装成单元测试。

[规划场景测试](tests/ep-planning/scenarios.md) 覆盖三类核心用法：

- 有基准目标数据的 BI 报表；
- 没有现成目标产物的权限功能；
- 需要多个子代理持续执行的大型功能。

[执行场景测试](tests/ep-execution/scenarios.md) 覆盖：

- 核心闭环完成后再推进增强；
- Ready 任务之间存在公共 Schema 冲突；
- 中断恢复、局部业务阻塞和独立任务继续执行。

`ep-execution` 已通过上述三个隔离前向场景，以及一次从规划批准到执行交接的组合测试。

[架构场景测试](tests/ep-architecture/scenarios.md) 覆盖 BI 计算与查询负载、订单定价模块边界，以及大 JSON 的渐进存储演进。该 Skill 已通过三个隔离前向场景。

[诊断场景测试](tests/ep-diagnosis/scenarios.md) 覆盖基准报表差异、低概率重复扣款和 Schema 迁移后的性能退化。该 Skill 已通过三个隔离前向场景。

[评审场景测试](tests/ep-delivery-review/scenarios.md) 覆盖业务结果失败、工程风险阻断和低风险外部反馈核验。该 Skill 已通过三个隔离前向场景。

[原型场景测试](tests/ep-prototyping/scenarios.md) 覆盖业务逻辑口径、现有页面 UI 方案和应先调查的供应商能力。该 Skill 已通过三个隔离前向场景。

[研究场景测试](tests/ep-research/scenarios.md) 覆盖供应商能力、未指定框架的版本升级，以及必须运行验证的 Excel 算法等价问题。该 Skill 已通过三个隔离前向场景。

[领域建模场景测试](tests/ep-domain-modeling/scenarios.md) 覆盖 SaaS “账号”歧义、报表定义/计算/发布混用，以及 ADR 过度记录。该 Skill 已通过三个隔离前向场景。

[大型工作导航场景测试](tests/ep-large-project/scenarios.md) 覆盖 ERP 替换、模糊 BI 平台统一和不应建图的清晰小功能。该 Skill 已通过三个前向场景，小功能入口经一次修订后复测通过。

[业务请求分流场景测试](tests/ep-request-intake/scenarios.md) 覆盖证据不足的退款报表缺陷、方案先行的 Kafka 请求，以及完整但尚未批准规划的合同批量操作。该 Skill 已通过三个前向场景。

[自然技术中文场景](tests/ep-chinese-writing/scenarios.md) 覆盖用户解释、Spec/Plan 文档和代码评审，检查首次释义、术语一致性和自然中文句法。

[多角色工作流编排场景](tests/ep-orchestration/scenarios.md) 覆盖并行角色评审、共享 Schema 冲突，以及失败后的跨会话恢复。

[产品体验塑造场景](tests/ep-product-design/scenarios.md) 覆盖 BI 高频筛选、权限配置流程，以及不应进入体验设计的纯后端任务。

[Easypower 路由场景](tests/ep-use-easypower/scenarios.md) 覆盖明确小改动、已批准 Plan 和大型模糊目标。[代码修改场景](tests/ep-code-change/scenarios.md) 覆盖无需新增测试的小修改、需要同步既有测试的行为修改，以及可以快速处理的指定用户赋权。

新增或修改正式 Skill 时，应先观察无 Skill 的基线行为，再使用相同场景进行前向验证。

## 版本与贡献

Plugin 使用 Semantic Versioning（语义化版本），当前版本记录在 [.codex-plugin/plugin.json](.codex-plugin/plugin.json)。触发边界、审批协议或路由行为发生兼容性变化时必须提升版本。

贡献前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，安全问题按 [SECURITY.md](SECURITY.md) 私下报告。Easypower 使用 [MIT License](LICENSE)。
