# Standalone Goal Prompt（独立目标 Prompt）

当用户选择"其他窗口执行"模式时，`ep-execution` 生成一个自包含的目标 Prompt 包，让用户复制到另一个窗口/会话/Agent 中运行整个 Plan。

## 双层结构

| 层 | 位置 | 内容 | 用途 |
|---|---|---|---|
| 简版 | 聊天消息框 | 一句话 + 文档路径 | 用户复制粘贴到目标 Agent |
| 详版 | `docs/easypower/<feature>/execution-goal.md` | 完整执行包 | 目标 Agent 读取并执行 |

## 简版 Prompt 模板

直接输出到聊天窗口：

```text
执行 `<feature>` 的 Phase 2 任务,详见 `docs/easypower/<feature>/execution-goal.md`。
```

或带更多上下文版本：

```text
执行 `<feature>` 的完整业务计划。本 Spec 和主 Plan 已批准,核心闭环切片清单和验收契约见上述文档。按 $ep-execution 协议从 Frontier 开始,使用 Agent 工具 spawn 子代理执行,每个切片留下 evidence。
```

**原则：** 简版 Prompt **不重复**详版内容,只**指向**文档。

## 详版 Prompt 模板（execution-goal.md）

保存路径：`docs/easypower/<feature>/execution-goal.md`

```markdown
# Execution Goal: <feature>

## 上下文来源

- **Spec：** `docs/easypower/<feature>/spec.md`（已批准）
- **主 Plan：** `docs/easypower/<feature>/plan.md`（已批准）
- **入口检查清单：** 见 [execution-state.md](execution-state.md)

## 执行目标

<一句话描述本阶段要让什么业务闭环完成>

## 切片清单

按主 Plan 顺序列出本次要执行的切片（每个切片一行）：

| ID | 业务结果 | 依赖 | 预期状态 |
|---|---|---|---|
| P01 | <一句话> | 无 | Ready |
| P02 | <一句话> | P01 | Planned |
| ... | ... | ... | ... |

只展开 Frontier 中的切片（Ready 状态），其他切片留作 Planned。

## 子 Plan 展开指南

对每个即将进入 Ready 的切片，按以下结构展开 `plans/<ID>.md`：

- 切片背景（引用 Spec 相关章节）
- 实现步骤（具体到文件级别）
- 验收依据（引用 Spec 中的业务验收）
- 依赖产物（上游完成的接口、数据）
- 所有权（允许修改 / 只读 / 禁止修改）
- 升级条件（参见 agent-brief.md 标准模板）

**不要在子 Plan 中重复 Spec 章节**，只引用路径。

## 子代理调用模板

每个切片使用 Agent 工具 spawn 子代理，prompt 模板见 [agent-brief.md](agent-brief.md)。

**关键参数：**
- `subagent_type`: `general-purpose`
- `isolation`: `worktree`（大型项目）或不传（小切片）
- `prompt`: 必须包含切片 ID、Spec/Plan 路径、所有权、升级条件、返回契约

## 状态恢复点

执行过程中断后，从以下位置恢复：

1. 读取主 Plan 的状态表（执行账本）
2. 检查 Git diff / worktree 状态
3. 检查 `evidence/<ID>/` 目录
4. 重新计算 Frontier

不要依赖聊天摘要，按 [execution-state.md](execution-state.md) 的恢复协议操作。

## 升级条件

以下任一情况立即停下，回报主 Agent 或用户：

- 业务规则 / 不变量 / 验收标准与已批准 Spec 不一致
- 需要改变公共接口、Schema、迁移路径或关键架构
- 缺少凭据、外部权限或不可恢复操作授权
- 业务口径存在多种合理解释，无法用现有证据区分
- 发现系统性风险，超出主 Plan 授权

## 验收标准

每个切片必须满足：

- 业务验收：Spec 中定义的业务场景通过
- 代码层验证：运行指定命令，输出符合预期
- 核心业务回归：已通过的核心闭环切片仍成立
- 证据：保存到 `evidence/<ID>/`：
  - 输入 / 数据版本
  - 期望业务结果
  - 实际结果
  - 执行命令和输出
  - 核心闭环回归结果
  - 已知限制和未覆盖风险

## 不要做

- 不要修改 Spec 或主 Plan（除非授权范围内更新业务决策）
- 不要跳过证据保存
- 不要用全量测试或代理数量替代业务证据
- 不要在遇到歧义时自行选择一种业务解释继续推进
- 不要把"已实现"等同于"已完成"

## 完成时

所有切片 Completed 后：

1. 输出业务交付报告（核心闭环 + 增强项 + 证据 + 偏差 + 剩余风险 + 产物位置）
2. 回到主对话，调用 `$ep-delivery-review` 做最终评审
3. 用户决定 Approved / Approved with follow-ups / Not approved

## 跨会话提示

- 本文档是**自包含**的：目标 Agent 不需要读主对话历史
- 所有真实信息都在磁盘文件里：Spec、Plan、execution-state.md、agent-brief.md
- 如果 Spec 或主 Plan 有更新，需要重新生成 execution-goal.md
```

## 生成时机

**只在用户选择"其他窗口执行"模式时生成。** 默认执行模式（当前窗口派子代理）不需要这个文件——因为执行 Agent 在当前上下文,可以直接读取 Plan。

## 更新规则

每次执行前重新生成：

- 主 Plan 变更后,execution-goal.md 必须同步
- 新增切片或调整依赖后,切片清单表必须更新
- 跨会话执行时,execution-goal.md 是唯一入口,不需要聊天记录

## 与 Goal Prompt 相关的常见错误

- 把完整 Spec 内容复制到 execution-goal.md（膨胀且不一致）
- 在聊天里输出完整 Goal Prompt（应该只输出一句话 + 路径）
- 生成后不更新，主 Plan 改了但 execution-goal.md 还是旧的
- 让目标 Agent 不读 execution-goal.md 就开始执行（失去自包含意义）
- 在 execution-goal.md 里写未来计划或猜测（只写当前已批准内容）