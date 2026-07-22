# 纵深校验

## 概述

修复无效数据导致的缺陷时，只加一处校验看似足够，但其他调用路径、重构或 mock 都可能绕过它。

**核心原则：数据经过的每一层都校验，让缺陷在结构上无法发生。**

## 为什么需要多层

单层校验只能说明“我们修了问题”；多层校验才能尽量做到“问题无法发生”。不同层捕获不同情况：入口校验捕获大多数错误，业务逻辑捕获领域边界，环境保护阻止危险上下文，调试记录帮助事后调查。

## 四层模型

### 第一层：入口校验

在 API 边界拒绝明显无效输入：

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
}
```

### 第二层：业务逻辑校验

确保数据符合当前操作的领域规则：

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
}
```

### 第三层：环境保护

在特定上下文阻止危险操作：

```typescript
async function gitInit(directory: string) {
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));
    if (!normalized.startsWith(tmpDir)) {
      throw new Error(`Refusing git init outside temp dir during tests: ${directory}`);
    }
  }
}
```

### 第四层：调试记录

为取证保留上下文：

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug('About to git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });
}
```

## 应用步骤

1. 追踪数据流，找到错误值的来源和所有使用点。
2. 列出数据经过的每个检查点。
3. 在入口、业务、环境和调试层分别添加适当保护。
4. 测试绕过第一层时，确认第二层能捕获；依此验证各层。

## 示例

空 `projectDir` 导致 `git init` 在源码目录运行时：

1. 测试 setup 产生空字符串；
2. `Project.create(name, '')` 接收空值；
3. `WorkspaceManager.createWorkspace('')` 继续传递；
4. `git init` 在 `process.cwd()` 执行。

可添加四层保护：Project.create() 校验目录，WorkspaceManager 校验非空，测试环境拒绝临时目录外的 git init，操作前记录堆栈。

不要停在一个校验点。不同调用路径、mock、平台边界和环境差异都可能绕过前一层。
