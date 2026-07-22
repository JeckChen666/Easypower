---
name: requesting-code-review
description: 当任务完成、实现了重要功能或准备合并前使用，以验证成果符合需求并尽早发现问题
---

# 发起代码评审

通过独立的代码评审代理检查实现，防止问题累积。评审者只接收必要的需求和 diff 上下文，不继承当前会话历史。

**核心原则：尽早评审，持续评审。**

## 何时必须评审

- 子代理驱动开发的每个任务完成后。
- 重要功能完成后。
- 合并到主分支前。

遇到卡点、重构前或修复复杂缺陷后也适合主动评审。

## 如何发起

1. 获取起止提交：

   ```bash
   BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
   HEAD_SHA=$(git rev-parse HEAD)
   ```

2. 使用 [code-reviewer.md](code-reviewer.md) 模板，调用 `general-purpose` 评审代理。
3. 填入实现摘要、需求或计划、`BASE_SHA` 和 `HEAD_SHA`。
4. 评审返回后，立即修复 Critical，继续前修复 Important，Minor 可以记录后安排。
5. 若意见错误，引用代码和测试给出技术理由，不要沉默忽略。

## 评审输入模板

```text
DESCRIPTION: <实现了什么>
PLAN_OR_REQUIREMENTS: <必须满足的需求或计划任务>
BASE_SHA: <起始提交>
HEAD_SHA: <结束提交>
```

评审者应检查规格符合性、正确性、回归、测试覆盖、错误处理、可维护性和范围控制。评审输入不应包含你的结论或希望评审者找到的具体问题。

## 红线

不要因为改动简单就跳过评审；不要忽略 Critical；不要带着未处理的 Important 继续推进；不要把评审当作形式流程。评审结论必须和实际 diff、测试输出相互印证。
