## 调度子代理需要多代理支持

在 Codex 配置 `~/.codex/config.toml` 中启用：

```toml
[features]
multi_agent = true
```

这会为 `dispatching-parallel-agents` 和 `subagent-driven-development` 等 skill 启用 `spawn_agent`、`wait_agent` 和 `close_agent`。使用子代理驱动开发时，任务完成后应关闭实现代理和评审代理。

## 环境检测

创建 worktree 或完成分支的 skill 在继续之前，应使用只读 Git 命令检测环境：

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON`：已经位于 linked worktree，跳过创建。
- `BRANCH` 为空：处于 detached HEAD，无法在沙箱中创建分支、推送或创建 PR。

具体使用方式见 `using-git-worktrees` 第 0 步和 `finishing-a-development-branch` 第 1 步。

## Codex App 收尾

当沙箱阻止创建分支或推送时，代理提交全部工作，并告知用户使用 App 的原生控件：

- **Create branch**：命名分支，然后通过 App 界面提交、推送和创建 PR。
- **Hand off to local**：把工作移交给用户的本地 checkout。

代理仍可运行测试、暂存文件，并输出建议的分支名、提交消息和 PR 描述。
