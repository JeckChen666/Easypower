# ep-use-easypower 场景

## 场景一：明确的小修改

用户明确要求使用 Easypower，把一个现有页面按钮文案改为“重新计算”。应选择 `$ep-code-change`，不创建 Spec、Plan 或新测试。

## 场景二：已有批准计划

用户要求使用 Easypower，继续执行磁盘中已批准的 Spec 和 Plan。应选择 `$ep-execution`，不重新规划。

## 场景三：大型模糊目标

用户要求使用 Easypower 统一多个业务系统，但目标边界和迁移顺序仍不清楚。应选择 `$ep-large-project`，不直接进入实现。

## 失败信号

- 一次加载全部 Easypower Skill；
- 所有代码任务都进入 Spec 和 Plan；
- 已经选定下游 Skill 后重新路由；
- 用户已明确指定可用 Skill 时无理由替换。
