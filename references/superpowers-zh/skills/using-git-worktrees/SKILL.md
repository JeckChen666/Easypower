---
name: using-git-worktrees
description: 开始需要隔离的功能开发或执行实现计划前使用；确保通过宿主原生能力或 git worktree 创建隔离工作区
---

# 使用 Git Worktree

在开始修改前确认工作区隔离方式，优先使用平台原生工作区能力；没有原生能力时再使用 Git worktree。不要和宿主环境争抢工作区管理权。

## 第 0 步：检查现有隔离

先检查当前是否已经处于 worktree、临时工作区、子模块或宿主分配的隔离目录。若已隔离，记录路径和分支，直接复用；若只是子模块，按普通仓库处理。

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
git branch --show-current
```

## 第 1 步：创建隔离工作区

1. 读取仓库状态，确保用户已有修改不被覆盖。
2. 选择清晰的功能分支名，例如 `feat/<topic>` 或 `fix/<topic>`。
3. 优先调用当前平台的原生 worktree/工作区工具。
4. 否则从主仓库根目录创建：

   ```bash
   git worktree add .worktrees/<topic> -b <branch-name>
   ```

5. 进入新目录后再次确认根目录、分支和干净状态。

不要在已有用户改动的目录上强行创建或清理 worktree，也不要复用另一个功能分支的 worktree。

## 第 2 步：安装项目依赖

只执行项目实际需要的初始化命令：

```bash
# Node.js
npm install

# Rust
cargo build

# Python
python -m venv .venv && python -m pip install -r requirements.txt

# Go
go mod download
```

优先遵循项目 README、锁文件和现有 CI，不要擅自升级依赖。

## 第 3 步：验证干净基线

运行项目对应的测试、构建或 lint 命令，并记录结果。基线失败必须报告给用户；不要把基线失败归因于新工作。

```bash
git status --short
<项目测试命令>
```

## 快速参考

```bash
git worktree list
git worktree add .worktrees/<topic> -b <branch-name>
git -C .worktrees/<topic> status
git worktree remove .worktrees/<topic>
git worktree prune
```

## 红线

不得删除不属于当前任务的 worktree；不得在未确认用户改动的情况下切换、重置或覆盖分支；不得把 `.worktrees/` 下的目录提交进项目；不得在 worktree 内删除它自己。完成任务后的清理遵循 `finishing-a-development-branch`。
