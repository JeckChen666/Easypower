# 评审反馈与交付判断

## 核验反馈

对每条 Finding（评审发现）记录：

| Finding | 契约或代码依据 | 实际影响 | 决定 | 后续 |
|---|---|---|---|---|
| ... | ... | ... | Accept / Reject / Defer / Need clarification | ... |

- **Accept（接受）**：证据成立且在批准范围内，返回执行并重验；
- **Reject（拒绝）**：与当前代码、契约或仓库约定不符，引用证据说明；
- **Defer（延期处理）**：存在价值但不属于当前交付要求，不阻断且另行记录；
- **Need clarification（需要澄清）**：事实不足或涉及业务、架构选择，停止相关修改。

不要在理解一半时先处理部分含糊意见。能独立核验的明确 Blocker 可以先止损，但范围变化仍需批准。

## 最终放行条件

| 契约轴 | 工程轴 | 最终决定 |
|---|---|---|
| Pass（通过） | Pass（通过） | Approved（批准） |
| Pass（通过） | Pass with follow-ups（通过但需跟进） | Approved with follow-ups（批准但需跟进） |
| Fail（不通过） | 任意 | Not approved（不批准） |
| 任意 | Fail（不通过） | Not approved（不批准） |
| Not assessable（无法评估） | 任意 | Not assessable；用户明确只请求工程风险评审时除外 |

Minor 或已接受的非阻断跟进必须有所有者和范围，不能成为无限期评审循环。Blocker 和 Important 修复后，重验其触发场景、相关契约项和必要工程边界；不默认重跑所有审查。

实际业务失败交给 `$diagnosing-business-failures`。普通实现修复交回 `$executing-business-plans`。需要改变业务契约或关键架构时交由用户批准，并按需调用 `$designing-business-architecture`。
