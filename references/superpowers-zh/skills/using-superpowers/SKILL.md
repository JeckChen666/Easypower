---
name: using-superpowers
description: 每次对话开始时使用；要求先发现并调用适用的 skill，再回答问题或执行任何动作
---

<SUBAGENT-STOP>
如果你是被调度来执行明确子任务的子代理，忽略本 skill 的启动规则，直接执行父代理交代的任务。
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
只要存在哪怕 1% 的可能某个 skill 适用，就必须先检查并调用它。不要等到写代码时才考虑 skill。
</EXTREMELY-IMPORTANT>

# 使用 Skill 系统

## 规则

每次新请求先扫描可用 skill 的名称和 description，识别所有可能适用的 skill。先读取最相关的 `SKILL.md`，再回答澄清问题、提出计划或执行命令。若多个 skill 适用，按工作流依赖顺序调用。

用户明确要求使用某 skill 时，优先满足该要求；用户明确要求跳过时，遵循用户要求，但仍需保留必要的安全和验证步骤。

## 优先级

1. 系统和用户指令。
2. 处理当前请求所需的强制流程 skill。
3. 用户明确点名的 skill。
4. 其他帮助完成任务的 skill。

常见顺序是：`brainstorming` -> `using-git-worktrees` -> `writing-plans` -> `subagent-driven-development` 或 `executing-plans` -> `test-driven-development` -> `requesting-code-review` -> `verification-before-completion` -> `finishing-a-development-branch`。

## 平台适配

先识别当前 agent 是否支持子代理、任务列表、工作区和浏览器工具。不要调用不存在的工具；读取相应参考文件了解平台映射：

- `references/codex-tools.md`
- `references/antigravity-tools.md`
- `references/pi-tools.md`

当没有子代理能力时，使用顺序计划执行并明确记录降级；不要假装任务已并行或已由评审代理检查。

## 触发后的行为

Skill 的 `description` 负责触发，正文负责执行。不要只引用 skill 名称而不阅读正文，也不要把一个 skill 的职责替换成另一个 skill。完成前必须使用 `verification-before-completion`。
