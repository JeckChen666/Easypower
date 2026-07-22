# 可视化助手指南

基于浏览器的视觉头脑风暴助手，用于展示 mockup、图表和方案对比。

## 何时使用

按问题判断，而不是按整个会话判断。标准是：**用户通过看到它，是否会比阅读文字理解得更好？**

**使用浏览器**处理内容本身具有视觉属性的场景：

- UI mockup：线框、布局、导航结构、组件设计；
- 架构图：系统组件、数据流、关系图；
- 并排视觉比较：布局、配色或设计方向对比；
- 视觉润色：外观、间距和视觉层级；
- 空间关系：状态机、流程图和实体关系图。

**使用终端**处理文本或表格内容：

- 需求和范围问题；
- 用文字描述的 A/B/C 概念选择；
- 优缺点和取舍表；
- API、数据建模和架构方案选择；
- 答案本身是文字而非视觉偏好的澄清问题。

“关于 UI 的问题”不一定是视觉问题。“你想要什么类型的向导？”是概念问题，用终端；“这两个向导布局哪个更合适？”才是视觉问题，用浏览器。

## 工作方式

服务器监视 HTML 文件目录，并在浏览器中提供最新文件。你把 HTML 内容写入 `screen_dir`，用户在浏览器中查看并点击选择；选择记录到 `state_dir/events`，下一轮读取。

**内容片段和完整文档：**HTML 文件以 `<!DOCTYPE` 或 `<html` 开头时，服务器按原样提供，只注入辅助脚本。否则服务器自动使用 frame 模板包装内容，加入标题、CSS 主题、连接状态和交互基础设施。默认写内容片段；只有需要完全控制页面时才写完整文档。

## 启动会话

```bash
# 用户批准助手后再启动；--open 会自动打开第一屏，--project-dir 会持久化 mockup。
scripts/start-server.sh --project-dir /path/to/project --open

# 返回：{"type":"server-started","port":52341,
#       "url":"http://localhost:52341/?key=ab12…",
#       "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#       "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

保存响应中的 `screen_dir` 和 `state_dir`。使用 `--open` 时浏览器会在第一屏推送后自动打开；仍要分享完整 URL 作为备用，因为无头或远程环境无法自动打开。

URL 包含会话密钥 `?key=...`。服务器会拒绝没有密钥的请求，因此始终把 `url` 字段返回的完整 URL 给用户，不要删除查询字符串，也不要分享裸的 `http://host:port`。密钥保护 HTTP 和 WebSocket，避免其他标签页或机器读取屏幕、注入事件。首次加载后浏览器通过 cookie 记住密钥。

如果没有捕获启动输出，从 `$STATE_DIR/server-info` 读取启动 JSON。使用 `--project-dir` 时，到 `<project>/.superpowers/brainstorm/` 查找会话目录。

把项目根目录传给 `--project-dir`，这样 mockup 会持久化在 `.superpowers/brainstorm/`，重启服务器后仍可查看；没有该参数时文件会进入 `/tmp` 并被清理。如果项目还没有忽略规则，提醒用户将 `.superpowers/` 加入 `.gitignore`。

## 各平台启动方式

**Claude Code：**

```bash
scripts/start-server.sh --project-dir /path/to/project --open
```

Windows 会自动切换为前台模式并阻塞工具调用。使用 Bash 工具的 `run_in_background: true`，让服务器跨会话保持运行；下一轮从 `$STATE_DIR/server-info` 读取 URL 和端口。

**Codex：**

```bash
scripts/start-server.sh --project-dir /path/to/project --open
```

Codex 会回收后台进程，脚本会自动检测 `CODEX_CI` 并切换前台模式；正常运行即可。

**Copilot CLI：**

```bash
scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

通过异步 Bash 工具启动，保存返回的 shellId，必要时使用 `read_bash` 或 `stop_bash`。

其他环境必须让服务器跨会话保持后台运行；如果环境会回收脱离终端的进程，使用 `--foreground` 和平台自己的后台执行机制。

如果浏览器无法访问 URL（远程或容器环境常见），绑定非回环地址：

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

用 `--url-host` 控制返回 JSON 中打印的主机名。

## 交互循环

1. **确认服务器存活，再向用户提供 URL 或推送屏幕。**确认 `$STATE_DIR/server-info` 存在且 `$STATE_DIR/server-stopped` 不存在。若已停止，使用相同 `--project-dir` 重启；它会复用端口，用户打开的标签页会自动重连，服务器停止期间只显示“已暂停”遮罩。服务器默认空闲 4 小时后退出，可用 `--idle-timeout-minutes` 配置。
   - 在 `screen_dir` 写入新文件；使用语义化文件名，如 `platform.html`、`visual-style.html`、`layout.html`。
   - **不要复用文件名**，每一屏都创建新文件。
   - 使用文件创建工具，不要使用 cat 或 heredoc。
   - 服务器自动提供最新文件。
2. **告诉用户要看什么，然后结束本轮：**每一步都提醒完整 URL，简短说明屏幕内容，并提示：“请在浏览器中查看并告诉我想法；如果需要，可以点击选择方案。”
3. **下一轮读取反馈：**如果 `$STATE_DIR/events` 存在，读取其中每行一个 JSON 对象的浏览器交互；与终端文字合并判断。终端消息是主要反馈，事件文件提供结构化信息。
4. **迭代或推进：**反馈改变当前屏幕时写新文件，如 `layout-v2.html`；当前问题确认后才进入下一问题。
5. **回到终端时卸载旧视觉内容：**下一步不需要浏览器时推送等待屏，避免用户继续盯着已经解决的选择：

   ```html
   <!-- 文件名：waiting.html -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">继续在终端中讨论……</p>
   </div>
   ```

6. 重复，直到头脑风暴结束。

## 编写内容片段

只写页面内部的内容。服务器会自动加入 frame 模板、主题 CSS、连接状态和交互基础设施。

```html
<h2>哪个布局更合适？</h2>
<p class="subtitle">请考虑可读性和视觉层级</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>单列</h3>
      <p>整洁、聚焦的阅读体验</p>
    </div>
  </div>
</div>
```

不需要 `<html>`、CSS 或 `<script>` 标签，服务器会提供。

## 可用 CSS 类

### 选项（A/B/C）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content"><h3>标题</h3><p>说明</p></div>
  </div>
</div>
```

容器添加 `data-multiselect` 可启用多选，每次点击切换选中状态。

### 卡片（视觉设计）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup 内容 --></div>
    <div class="card-body"><h3>名称</h3><p>说明</p></div>
  </div>
</div>
```

### Mockup 容器

```html
<div class="mockup">
  <div class="mockup-header">预览：仪表盘布局</div>
  <div class="mockup-body"><!-- mockup HTML --></div>
</div>
```

### 并排视图

```html
<div class="split">
  <div class="mockup"><!-- 左侧 --></div>
  <div class="mockup"><!-- 右侧 --></div>
</div>
```

### 优缺点

```html
<div class="pros-cons">
  <div class="pros"><h4>优点</h4><ul><li>收益</li></ul></div>
  <div class="cons"><h4>缺点</h4><ul><li>代价</li></ul></div>
</div>
```

### Mock 元素（线框积木）

```html
<div class="mock-nav">Logo | 首页 | 关于 | 联系</div>
<div style="display: flex;">
  <div class="mock-sidebar">导航</div>
  <div class="mock-content">主内容区</div>
</div>
<button class="mock-button">操作</button>
<input class="mock-input" placeholder="输入字段">
<div class="placeholder">占位区域</div>
```

### 字体和区块

- `h2`：页面标题；
- `h3`：章节标题；
- `.subtitle`：标题下方的辅助文字；
- `.section`：带下边距的内容块；
- `.label`：小号大写标签。

## 浏览器事件格式

用户点击选项时，交互会记录到 `$STATE_DIR/events`，每行一个 JSON 对象。推送新屏幕时文件会自动清空：

```jsonl
{"type":"click","choice":"a","text":"选项 A - 简洁布局","timestamp":1706000101}
{"type":"click","choice":"c","text":"选项 C - 复杂网格","timestamp":1706000108}
{"type":"click","choice":"b","text":"选项 B - 混合布局","timestamp":1706000115}
```

完整事件流能显示探索路径：用户可能先点击多个选项再决定。最后一个 `choice` 通常是最终选择，但点击模式能暴露犹豫或偏好。如果文件不存在，说明用户没有与浏览器互动，只使用终端文字。

## 设计提示

- 问布局就做线框，问视觉润色才做精细视觉；
- 每一页都说明问题，不要只写“请选择”；
- 当前屏幕反馈变化时先迭代，不要直接进入下一问题；
- 每屏最多 2-4 个选项；
- 设计重要时使用真实内容，避免占位内容掩盖问题；
- 保持 mockup 简单，聚焦布局和结构，不追求像素级还原。

## 文件命名

使用 `platform.html`、`visual-style.html`、`layout.html` 等语义化名称；不要复用文件名；迭代使用 `layout-v2.html`、`layout-v3.html`；服务器按修改时间提供最新文件。

## 清理

```bash
scripts/stop-server.sh $SESSION_DIR
```

使用 `--project-dir` 时 mockup 会保留在 `.superpowers/brainstorm/` 供后续查看，只有 `/tmp` 会话停止时删除。

## 参考

- frame 模板（CSS 参考）：`scripts/frame-template.html`
- 辅助脚本（客户端）：`scripts/helper.js`
