# Antigravity CLI（`agy`）工具映射

Skill 使用“调度子代理”“创建待办”“读取文件”等动作描述；在 Antigravity CLI（`agy`）上对应以下工具：

| Skill 请求的动作 | Antigravity CLI 对应项 |
|---|---|
| 调度子代理（`Subagent (general-purpose):` 模板） | 使用内置 `TypeName` 调用 `invoke_subagent`：完整能力使用 `self`，只读调查使用 `research`。 |
| 任务跟踪（“创建待办”“标记完成”） | 使用 `write_to_file` 创建任务 artifact，设置 `IsArtifact: true` 和 `ArtifactType: "task"`。不要使用管理后台进程的 `manage_task`。 |

## 任务跟踪

Antigravity 没有待办工具；`manage_task` 管理的是后台进程的 `list`、`kill`、`status`、`send_input`，不是清单。

当 skill 要求创建或跟踪任务时，使用 `write_to_file` 写入 Markdown 清单，并设置 `IsArtifact: true`、`ArtifactMetadata.ArtifactType: "task"`。执行过程中用 `replace_file_content` 或 `multi_replace_file_content` 将完成项改为 `- [x]`。

多步骤任务开始时列出全部步骤，完成一步就更新一步；计划变化时同步修改清单。对话变长后，在开始下一步前重新读取清单。
