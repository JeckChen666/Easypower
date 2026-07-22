# Workflow Schema（工作流结构）

- [最小示例](#最小示例)
- [角色契约](#角色契约)
- [校验规则](#校验规则)
- [运行状态](#运行状态)

## 最小示例

```yaml
version: 1
name: product-architecture-review

inputs:
  prd:
    required: true

roles:
  product-reviewer:
    prompt: 独立评审产品目标、用户价值和验收范围，不替用户决定业务取舍。
    responsibility: 检查用户价值、范围和验收
    inputs: [PRD 和项目事实]
    output: 产品评审发现
    may_decide: [评审发现和建议]
    must_escalate: [业务范围选择]
    owns: [steps/product-review/output.md]
  architect:
    prompt: 独立评审系统边界、约束和演进风险，不替用户批准关键架构取舍。
    responsibility: 检查系统边界、风险和演进路径
    inputs: [PRD、现有架构和运行约束]
    output: 架构风险与备选方案
    may_decide: [技术风险判断]
    must_escalate: [关键架构取舍]
    owns: [steps/architecture-review/output.md]
  synthesizer:
    prompt: 只按用户批准的方向合并结论，保留未解决分歧。
    responsibility: 按已批准方向汇总独立结论和剩余分歧
    inputs: [角色评审和用户批准方向]
    output: 最终评审结论
    may_decide: [信息组织和重复项合并]
    must_escalate: [未解决的业务或架构冲突]
    owns: [summary.md]

steps:
  - id: product-review
    type: agent
    role: product-reviewer
    task: 评审 {{ inputs.prd }}
    depends_on: []
    reads: ["{{ inputs.prd }}"]
    owns: [steps/product-review/output.md]
    output: steps/product-review/output.md
    completion: 每条发现包含场景、影响和依据
    escalate_when: 需要选择业务范围或修改 PRD 目标

  - id: architecture-review
    type: agent
    role: architect
    task: 评审 {{ inputs.prd }}
    depends_on: []
    reads: ["{{ inputs.prd }}"]
    owns: [steps/architecture-review/output.md]
    output: steps/architecture-review/output.md
    completion: 给出风险、证据和备选方案
    escalate_when: 需要批准关键架构取舍或外部副作用

  - id: approve-direction
    type: user-gate
    task: 选择需要进入 Spec 的业务与架构方向
    depends_on: [product-review, architecture-review]
    owns: [steps/approve-direction/output.md]
    output: steps/approve-direction/output.md
    completion: 用户明确记录批准、拒绝或要求修改的方向

  - id: synthesis
    type: agent
    role: synthesizer
    task: 根据已批准方向形成最终评审结论
    depends_on: [approve-direction]
    reads:
      - "{{ steps.product-review.output }}"
      - "{{ steps.architecture-review.output }}"
      - "{{ steps.approve-direction.output }}"
    owns: [summary.md]
    output: summary.md
    completion: 明确结论、依据、分歧和下一步
    escalate_when: 角色结论仍存在未批准冲突

execution:
  max_parallel: 2
  retry:
    max_attempts: 2
  timeout_minutes: 30
  continue_independent_on_failure: true
  sequential_fallback: false
```

## 角色契约

角色文件或内联定义至少说明：

- `responsibility`：该角色负责回答什么；
- `inputs`：可以依赖哪些事实；
- `output`：必须返回什么结构；
- `may_decide`：可以自主作出的判断；
- `must_escalate`：必须交给用户或其他角色的决定；
- `owns`：允许写入的文件、模块或资源。

步骤 `owns` 必须是角色 `owns` 的子集；最终权限取角色和步骤声明的交集。`user-gate` 的输出由协调 Agent 代用户记录。角色名称不能代替契约：“架构师”没有自动获得修改架构或批准业务范围的权限。

## 校验规则

运行前必须确认：

1. `version` 受支持，`name` 和所有 ID 唯一且可用于路径；
2. 每个 Agent step 的角色存在，角色 prompt 可读取；
3. 所有依赖存在且 DAG 无循环；
4. 所有 `{{ inputs.* }}` 和 `{{ steps.*.output }}` 引用有定义；
5. 必填输入有值，文件路径在批准范围内；
6. 并行步骤的 `owns`、Schema、端口、数据库和外部副作用不冲突；
7. 每个 Agent Step 都有输出位置、完成定义和升级条件；每个 `user-gate` 都有输出位置和完成定义；
8. 平台不支持的 timeout、retry 或并发选项在批准前明确说明。

使用 YAML parser 后再做结构校验，不用正则或字符串替换解析 YAML。模板只允许显式的输入和步骤输出引用，不执行表达式、命令或任意文件读取。

## 运行状态

`state.json` 至少记录：

```json
{
  "run_id": "2026-07-22T120000Z",
  "workflow_sha256": "...",
  "status": "in_progress",
  "steps": {
    "product-review": {
      "status": "completed",
      "agent": "agent-id",
      "attempt": 1,
      "started_at": "...",
      "finished_at": "...",
      "output": "steps/product-review/output.md",
      "evidence": [],
      "error": null
    }
  }
}
```

更新状态时使用原子写入。恢复时以工作流哈希、实际产物和 Agent 状态交叉确认，不能只相信标签。
