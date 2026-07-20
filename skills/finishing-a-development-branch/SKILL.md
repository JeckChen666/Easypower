---
name: finishing-a-development-branch
description: 当实现完成且测试通过，需要决定如何整合工作时使用；提供合并、创建 PR、保留或丢弃分支的结构化流程
---

# 完成开发分支

在完成实现后，用一致的步骤验证、识别工作区环境、呈现整合选项并执行用户选择。

**核心原则：验证测试 -> 识别环境 -> 提供选项 -> 执行选择 -> 清理。**

**开始时声明：**“我正在使用 finishing-a-development-branch skill 来完成这项工作。”

## 1. 验证测试

先运行项目测试：

```bash
npm test / cargo test / pytest / go test ./...
```

测试失败时停止，报告失败数量和关键信息；在测试通过前不要提供合并、PR 或丢弃选项。

## 2. 识别环境

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

判断当前是普通仓库、命名分支 worktree 还是 detached HEAD。普通仓库和命名分支显示 4 个选项；detached HEAD 显示 3 个选项，不提供本地合并。

## 3. 确定基分支

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

若无法确定基分支，询问用户，不要猜测。

## 4. 呈现选项

普通仓库或命名分支 worktree 必须原样提供以下四项：

```text
实现完成。你希望如何处理？

1. 在本地合并回 <基分支>
2. 推送并创建 Pull Request
3. 保留当前分支（稍后处理）
4. 丢弃这项工作

请选择一个选项。
```

detached HEAD 必须提供以下三项：

```text
实现完成。当前处于 detached HEAD（由外部环境管理）。

1. 推送为新分支并创建 Pull Request
2. 保留当前状态（稍后处理）
3. 丢弃这项工作

请选择一个选项。
```

## 5. 执行选择

### 选项 1：本地合并

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <基分支>
git pull
git merge <功能分支>
<合并后再次运行测试>
```

只有合并和测试都成功后，才清理 worktree，再执行 `git branch -d <功能分支>`。

### 选项 2：推送并创建 PR

```bash
git push -u origin <功能分支>
```

保留 worktree，用户需要它继续处理 PR 反馈。

### 选项 3：保留

报告分支名称和 worktree 路径，不做清理。

### 选项 4：丢弃

先明确列出将永久删除的分支、提交和 worktree，并要求用户输入精确的 `discard` 确认。确认后切换到主仓库根目录，清理 worktree，再执行 `git branch -D <功能分支>`。

## 6. 清理工作区

只对选项 1 和 4 清理。若 `GIT_DIR == GIT_COMMON`，说明是普通仓库，无 worktree 可清理。只有位于 `.worktrees/` 或 `worktrees/` 下的 worktree 才视为本 skill 创建并拥有清理权限：

```bash
cd <主仓库根目录>
git worktree remove <WORKTREE_PATH>
git worktree prune
```

其他路径可能由宿主环境管理，绝不删除；如平台有退出工作区工具，使用该工具。

## 快速参考

| 选项 | 合并 | 推送 | 保留 worktree | 清理分支 |
|---|---|---|---|---|
| 1. 本地合并 | 是 | - | 否 | 是 |
| 2. 创建 PR | - | 是 | 是 | 否 |
| 3. 保留 | - | - | 是 | 否 |
| 4. 丢弃 | - | - | 否 | 强制删除 |

## 红线

不得在测试失败时结束；不得在未验证合并结果时合并；不得未经精确确认删除工作；不得无明确请求强制推送；不得删除不属于自己的 worktree；不得从待删除的 worktree 内执行 `git worktree remove`。始终在移除后运行 `git worktree prune`。
