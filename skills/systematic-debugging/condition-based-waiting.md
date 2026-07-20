# 基于条件的等待

## 概述

不稳定测试经常用任意延迟猜测时序。在快机器上可能通过，在 CI 或高负载下却失败。

**核心原则：等待真正关心的条件，不要等待对耗时的猜测。**

## 何时使用

- 测试包含任意 `setTimeout`、`sleep` 或 `time.sleep()`；
- 测试偶尔通过、负载上升时失败；
- 并行运行时超时；
- 等待异步操作完成。

测试 debounce、throttle 等真实时间行为时，固定延迟可能是正确的，但必须说明原因。

## 核心模式

```typescript
// ❌ 之前：猜测耗时
await new Promise(r => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// ✅ 之后：等待条件
await waitFor(() => getResult() !== undefined);
const result = getResult();
expect(result).toBeDefined();
```

## 常用模式

| 场景 | 写法 |
|---|---|
| 等待事件 | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| 等待状态 | `waitFor(() => machine.state === 'ready')` |
| 等待数量 | `waitFor(() => items.length >= 5)` |
| 等待文件 | `waitFor(() => fs.existsSync(path))` |
| 复杂条件 | `waitFor(() => obj.ready && obj.value > 10)` |

## 实现

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise(r => setTimeout(r, 10));
  }
}
```

完整实现和 `waitForEvent`、`waitForEventCount`、`waitForEventMatch` 等领域辅助函数见本目录的 `condition-based-waiting-example.ts`。

## 常见错误

- **轮询过快：**`setTimeout(check, 1)` 浪费 CPU；通常每 10ms 检查一次。
- **没有超时：**条件永远不满足时无限循环；始终提供上限和清晰错误。
- **读取旧数据：**在循环外缓存状态；应在循环内重新调用 getter。

## 何时固定延迟是正确的

```typescript
// 工具每 100ms tick；需要 2 次 tick 验证部分输出
await waitForEvent(manager, 'TOOL_STARTED');
await new Promise(r => setTimeout(r, 200));
// 200ms = 100ms 间隔的 2 次 tick，原因已记录
```

要求：先等待触发条件；延迟必须来自已知时序而不是猜测；注释说明为什么使用。
