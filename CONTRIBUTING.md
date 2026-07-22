# Contributing

Easypower 只接收能够解决重复、真实工作问题的 Skill 变化。新增能力前，请先说明触发场景、现有失败方式、与已有 Skill 的边界，以及为什么不能作为现有 Skill 的内部协议。

## 修改要求

1. 保持 `SKILL.md` 简短，将按需细节放入同级 `references/`；
2. 目录名、frontmatter `name` 和 `$ep-*` 调用名称必须一致；
3. 更新 `agents/openai.yaml`，明确是否允许隐式调用；
4. 在 `tests/<skill-name>/scenarios.md` 增加或调整真实场景；
5. 只验证业务风险，不为覆盖率或测试数量增加无价值步骤；
6. 运行 `python scripts/validate_repo.py`。

Pull Request 应说明行为变化、触发边界、验证结果和兼容性影响。改变业务审批、路由或安全边界时，请单独标出。
