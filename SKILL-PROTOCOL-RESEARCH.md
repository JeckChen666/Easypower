# Codex Skill 协议研究

> 研究时间：2026-08-07
> 研究目的：验证 Easypower 是否可以通过目录分层（tier-light / tier-heavy）实现渐进式披露。

## 一、问题

Easypower 当前有 15 个 Skill，每个 SKILL.md 完整内容约 60-150 行。理论上默认上下文里全部加载会消耗相当多的 token。是否可以通过目录拆分让 harness 只加载其中一部分？

## 二、研究结论

**协议不支持目录拆分。** Codex Plugin 的 `plugin.json` 中 `skills` 字段是**单个字符串路径**，skill 文件夹必须**平铺**在该目录下。

但实际上**这个限制无关紧要**，因为 Agent Skills 标准已经实现了"渐进式披露"——harness 默认只加载每个 Skill 的元数据（`name` + `description`），完整 body 仅在被触发时加载。

## 三、官方规范

### 3.1 plugin.json 的 schema

来源：[developers.openai.com/plugins/build/plugins](https://developers.openai.com/plugins/build/plugins)

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Bundle reusable skills and MCP servers.",
  "skills": "./skills/",
  "mcpServers": "./.mcp.json",
  "apps": "./.app.json",
  "hooks": "./hooks/hooks.json"
}
```

**关键约束：**

1. `skills` 字段是**单个字符串路径**（必须以 `./` 开头，相对插件根目录）
2. **不支持数组、不支持多个路径、不支持 inline skill 对象**
3. skill 文件夹必须**平铺**在 `skills/` 下
4. 文档示例固定为 `skills/<skill-name>/SKILL.md` 形式
5. 文档未提及 `skills/core/` 或 `skills/heavy/` 这类嵌套结构

### 3.2 Agent Skills 的渐进式披露

来源：[learn.chatgpt.com/docs/build-skills](https://learn.chatgpt.com/docs/build-skills)

> **YAML metadata** at the top with `name` and `description` fields (~100 tokens, **always in context for matching**)
> **Markdown body** with detailed instructions, workflows, and notes (typically <5000 tokens, **loaded on trigger**)

每个 Skill 默认只把 metadata 加载到上下文，body 只在该 Skill 被显式触发时才加载。

**这意味着**：即使 15 个 Skill 都装在 harness 上，默认上下文只有 15 × ~100 = ~1500 token 的 metadata。一旦某个 Skill 被触发，再加载该 Skill 的 ~5000 token body。

### 3.3 Skills CLI

来源：[skills.sh](https://skills.sh)、[skills.sh/docs/cli](https://skills.sh/docs/cli)

Skills CLI 使用 URL 平铺路由（如 `/mattpocock/skills/tdd`），没有显式的目录嵌套支持。

## 四、Easypower 自身的检查

`scripts/validate_repo.py` 第 47-53 行强制 `skills` 字段值为 `"./skills/"`：

```python
required = {
    "name": "easypower",
    "skills": "./skills/",
    "license": "MIT",
}
```

任何偏离该值都会导致校验失败。

## 五、为什么目录拆分对 Easypower 没必要

按 metadata-only 加载机制：

| 维度 | 数值 |
|---|---|
| 15 个 Skill 的元数据总开销 | ~1500 token |
| 单个 Skill body（未触发） | 0 |
| 单个 Skill body（已触发） | ~5000 token |

如果改成"目录分层"，能减少的也只有那 ~1500 token 的元数据开销。**代价**是破坏路径兼容性、需要重装 Plugin、迁移 `git mv`。

**结论：现有 P3 改造（标准化前导 + references/ 按需读）已经走在了协议支持的渐进式披露正确路径上。**

## 六、合法的渐进披露手段

既然协议约束清晰，可以走的优化路径只有这几种：

### 6.1 缩短 description（推荐）

**做法：** 把每个 Skill 的 `description` 压到 ~100 字符以内，只保留触发关键词。

**效果：** 默认上下文的 metadata 开销从 ~1500 token 降到 ~1000 token。

**代价：** 几乎没有。

### 6.2 添加 weight 元数据（推荐）

**做法：** 在 SKILL.md frontmatter 增加 `weight: light | heavy`：

- `weight: light`：高频低风险，可自动调用（如 `ep-code-change`、`ep-chinese-writing`）
- `weight: heavy`：重型业务流，应显式调用

**效果：** harness 可以按 weight 优先用 light Skill（避免误触发），或在元数据中标注建议调用方式。

**代价：** harness 需要支持 `weight` 字段才能生效，但即使 harness 不支持，元数据也只是描述。

### 6.3 合并相似 Skill（不推荐）

**做法：** 把 `ep-research` `ep-prototyping` `ep-domain-modeling` 合并成一个 `ep-investigate`。

**效果：** Skill 数量减少到 13。

**代价：** 职责清晰度下降，路由粒度变粗。

### 6.4 Skill 数量硬控制（推荐）

**做法：** 在 SKILL-MAP 中明确"达到 20 个 Skill 触发准入条件重新审视"。

**效果：** 从制度上防止 Skill 膨胀。

**代价：** 没有。

## 七、本次采用的方案

1. **方案 6.1**：把 15 个 SKILL.md 的 `description` 压到 ~80-100 字符。
2. **方案 6.2**：在 SKILL.md frontmatter 增加 `weight: light | heavy` 字段，并在 validator 中强制要求该字段。

不做 6.3、6.4 中没列的方案（合并 Skill），因为当前 15 个 Skill 的职责已经清晰，强行合并会损害设计完整性。

## 八、对未来 Plugin 升级的提示

如果 Codex Plugin 协议将来支持：

- `skills` 接受数组（多路径）
- 或支持嵌套子目录
- 或支持 weight 优先级

Easypower 应该立即：

1. 在 `plugin.json` 的 `skills` 字段支持多路径时，把 2 个 light Skill 与 13 个 heavy Skill 分目录
2. 在协议支持 weight 优先级时，light Skill 的 description 进入"首选路由"

但在那之前，**不要试图用协议外的方式实现目录拆分**。

## 九、参考资料

| 来源 | 链接 |
|---|---|
| Codex Plugin 文档 | https://developers.openai.com/plugins/build/plugins |
| Agent Skills 构建指南 | https://learn.chatgpt.com/docs/build-skills |
| Codex CLI 仓库 | https://github.com/openai/codex |
| Codex Skills 文档（重定向） | https://developers.openai.com/codex/skills → https://learn.chatgpt.com/docs/build-skills |
| Skills CLI | https://skills.sh, https://skills.sh/docs/cli |