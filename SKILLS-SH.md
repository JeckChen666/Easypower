# Easypower 的 skills.sh 收录说明

本文说明如何让 Easypower 及其 `ep-*` Skill 被 [skills.sh](https://skills.sh) 自动收录和搜索。

## 收录机制

skills.sh 没有人工提交入口。公开 GitHub 仓库中的 Skill 被用户通过 Skills CLI 安装后，CLI 会发送匿名 install telemetry（安装遥测）；skills.sh 据此自动建立索引，并按累计安装量参与排行。

遥测只会记录被安装的 Skill、对应文件和时间等聚合信息，不包含个人或设备信息。设置 `DISABLE_TELEMETRY=1` 或 `DO_NOT_TRACK=1` 会关闭上报，也就无法通过该次安装触发收录。

## 收录前提

仓库需要满足以下条件：

- GitHub 仓库公开可访问；
- 待发布内容已经推送到远端；
- 每个 Skill 位于 CLI 支持的发现目录中；
- `SKILL.md` 包含有效的 YAML frontmatter，至少有 `name` 和 `description`；
- Skill 没有设置 `metadata.internal: true`。

Easypower 使用标准的多 Skill 布局：

```text
skills/
  ep-use-easypower/
    SKILL.md
  ep-code-change/
    SKILL.md
  ...
```

## 发布前检查

先运行仓库自身的结构校验：

```powershell
python scripts/validate_repo.py
```

再让 Skills CLI 扫描本地仓库：

```powershell
npx skills add . --list
```

该命令应列出全部正式 `ep-*` Skill。它只验证发现结果，不会产生远端安装 telemetry，因此不能单独触发 skills.sh 收录。

## 首次触发收录

确保最新提交已经推送到公开 GitHub 仓库，然后从远端执行一次真实安装：

```powershell
npx skills add JeckChen666/Easypower
```

在交互界面中选择需要安装的 Skill。至少可以选择统一入口 `ep-use-easypower`；若希望全部 Skill 都进入索引，则选择全部正式 Skill。

安装时不要禁用 telemetry，也不要只使用本地路径。以下操作不会触发首次收录：

```powershell
npx skills add . --list
npx skills find easypower
```

## 验证收录结果

skills.sh 没有承诺固定的索引完成时间。等待索引更新后，使用以下命令检查：

```powershell
npx skills find easypower
npx skills find ep-use-easypower
npx skills find easypower --owner JeckChen666
```

也可以访问预期的仓库页面：

```text
https://skills.sh/JeckChen666/Easypower
```

如果仍然搜索不到，依次确认：

1. GitHub 仓库是否为 public（公开）；
2. 远端默认分支是否包含最新的 `skills/ep-*/SKILL.md`；
3. `npx skills add JeckChen666/Easypower` 是否真的完成了安装，而不只是 `--list`；
4. 当前环境是否设置了 `DISABLE_TELEMETRY`、`DO_NOT_TRACK` 或 CI 环境变量；
5. 安装时是否选择了希望被收录的具体 Skill；
6. 是否为索引延迟，稍后再重新查询。

## 后续更新

已收录后，继续正常向 GitHub 推送新版 Skill。用户再次从远端安装或更新时，skills.sh 会收到新的匿名使用数据。Skill 的 `name` 应保持稳定；修改名称通常会被视为新的 Skill，并会影响原有搜索入口和安装统计。

skills.sh 的分发和 Easypower 的 Codex Plugin（插件）分发彼此独立：Plugin 清单负责 Codex 安装体验，skills.sh 根据 Skills CLI 的远端安装记录建立目录索引。

## README 徽章

收录后可在 README 中加入安装量徽章：

```markdown
[![skills.sh](https://skills.sh/b/JeckChen666/Easypower)](https://skills.sh/JeckChen666/Easypower)
```

## 当前验证记录

截至 2026-07-22：

- `main` 已推送到 GitHub；
- Skills CLI 能从本地仓库发现 15 个正式 Skill；
- `easypower` 和 owner `JeckChen666` 尚未出现在 skills.sh 搜索结果中；
- 下一步是从 GitHub 远端完成一次未禁用 telemetry 的真实安装。

## 官方参考

- [skills.sh Documentation](https://skills.sh/docs)
- [skills.sh FAQ](https://skills.sh/docs/faq)
- [Skills CLI](https://github.com/vercel-labs/skills)
