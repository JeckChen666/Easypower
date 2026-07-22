# 根因追踪

## 概述

缺陷经常在调用栈深处暴露，例如在错误目录执行 `git init`、在错误位置创建文件，或用错误路径打开数据库。直觉会让人直接修复报错位置，但那只是处理症状。

**核心原则：沿调用链反向追踪，直到找到最初触发点，再在源头修复。**

## 何时使用

- 错误发生在执行深处而非入口。
- 堆栈包含较长调用链。
- 不清楚无效数据从哪里产生。
- 需要找出哪个测试或代码触发了问题。

## 追踪流程

### 1. 观察症状

```text
Error: git init failed in ~/project/packages/core
```

### 2. 找到直接原因

```typescript
await execFileAsync('git', ['init'], { cwd: projectDir });
```

问：哪段代码直接造成了这个结果？

### 3. 追问是谁调用它

```text
WorktreeManager.createSessionWorktree(projectDir, sessionId)
  -> Session.initializeWorkspace()
  -> Session.create()
  -> Project.create() 中的测试
```

### 4. 继续向上追踪

确认传入的值和每次转换：

- `projectDir = ''`（空字符串）；
- 空字符串作为 `cwd` 时解析为 `process.cwd()`；
- 因而操作落在源码目录。

### 5. 找到最初触发点

```typescript
const context = setupCoreTest(); // 返回 { tempDir: '' }
Project.create('name', context.tempDir); // 在 beforeEach 前访问
```

不要把第一个发现的错误值当作根因，继续查明它为什么会出现。

## 添加堆栈追踪

无法手动追踪时，临时增加调试 instrumentation：

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  console.error('DEBUG git init:', {
    directory,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack,
  });

  await execFileAsync('git', ['init'], { cwd: directory });
}
```

测试中使用 `console.error()`，不要只使用可能被隐藏的 logger：

```bash
npm test 2>&1 | grep 'DEBUG git init'
```

阅读堆栈时寻找测试文件名、触发调用的行号，以及重复出现的测试或参数模式。危险操作前记录上下文，不要等失败后再记录。

## 找出污染环境的测试

如果测试期间出现了额外文件或状态，却不知道是哪一个测试产生的，使用本目录的 `find-polluter.sh`：

```bash
./find-polluter.sh '.git' 'src/**/*.test.ts'
```

脚本逐个运行测试，在第一个污染者出现时停止；具体参数见脚本帮助。

## 示例：空的 projectDir

**症状：**`.git` 被创建在源码目录 `packages/core/`。

**追踪链：**

1. `git init` 因空 `cwd` 参数在 `process.cwd()` 执行；
2. WorktreeManager 收到空的 projectDir；
3. Session.create() 传入空字符串；
4. 测试在 beforeEach 前访问 `context.tempDir`；
5. setupCoreTest() 初始返回 `{ tempDir: '' }`。

**根因：**顶层变量初始化时访问了空值。

**修复：**将 tempDir 改为在 beforeEach 前访问就抛错的 getter。

**纵深防御：**Project.create() 校验目录、WorkspaceManager 校验非空、测试环境禁止在临时目录外执行 git init，并在操作前记录堆栈。

## 关键原则

```text
找到直接原因后，继续向上追踪；找到源头后修复，并在各层添加必要校验。
```

永远不要只修复错误出现的位置。只有找到原始触发点，才知道修复没有把问题留在其他调用路径中。

## 堆栈技巧

- 测试中使用 `console.error()`，logger 可能被抑制。
- 在危险操作前记录，而不是失败后记录。
- 至少包含目录、cwd、环境变量和时间戳。
- 用 `new Error().stack` 获取完整调用链。
