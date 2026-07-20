# 测试反模式

**在以下情况读取：**编写或修改测试、增加 mock，或想在生产代码中添加仅供测试使用的方法。

## 概述

测试必须验证真实行为，而不是 mock 行为。Mock 是隔离手段，不是被测试的对象。

**核心原则：测试代码做了什么，不要测试 mock 做了什么。**

严格遵循 TDD 可以避免以下反模式。

## 铁律

```text
1. 永远不要测试 mock 行为
2. 永远不要给生产类添加只供测试使用的方法
3. 不理解依赖时永远不要 mock
```

## 反模式 1：测试 mock 行为

**错误示例：**

```typescript
// ❌ 错误：测试 mock 是否存在
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**为什么错误：**你验证的是 mock 存在，而不是组件工作；mock 一存在测试就通过，无法说明真实行为。

**修复：**测试真实组件或不要 mock：

```typescript
// ✅ 正确：测试真实组件
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});
```

如果必须为隔离而 mock，不要断言 mock 本身，而应测试 Page 在 sidebar 存在时的行为。

### 门禁

在断言任何 mock 元素前问：“我是在测试真实组件行为，还是仅在测试 mock 存在？”如果是后者，停止，删除断言或取消 mock，改测真实行为。

## 反模式 2：生产代码中的测试专用方法

**错误示例：**生产类污染了只在测试中调用的 `destroy()`，测试在 `afterEach` 中调用它清理。

**为什么错误：**生产 API 混入测试代码，可能被误调用；违反 YAGNI 和职责分离；混淆对象生命周期与实体生命周期。

**修复：**把清理放入测试工具：

```typescript
// ✅ 正确：测试工具负责测试清理
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}
```

在给生产类加方法前问：“这是否只被测试使用？”如果是，停止并放入测试工具；再问：“这个类是否拥有该资源的生命周期？”如果不是，说明方法放错了类。

## 反模式 3：不理解依赖就 mock

mock 可能屏蔽测试真正依赖的副作用，例如配置写入，导致重复服务器检测测试失效。不要为了“安全”而过度 mock。

**正确做法：**在较低层 mock 慢速或外部操作，保留测试需要的高层行为：

```typescript
// ✅ 正确：只 mock 慢的服务器启动，保留配置写入
vi.mock('MCPServerManager');

await addServer(config);
await addServer(config); // 正确检测重复
```

mock 方法前：

1. 查明真实方法的所有副作用；
2. 确认测试是否依赖这些副作用；
3. 先用真实实现运行测试，观察实际需要；
4. 在正确的较低层加入最小 mock。

“我先 mock 以防万一”“它可能很慢”“先 mock 总没错”都是停止并调查的信号。

## 反模式 4：不完整的 mock

只写测试当前用到的字段会隐藏真实结构假设。下游代码可能依赖被遗漏的字段，导致单测通过、集成失败。

**铁律：**mock 必须镜像真实数据结构的完整程度，而不是只包含当前断言需要的字段。

```typescript
// ✅ 正确：匹配真实 API 的完整响应
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
};
```

创建响应 mock 前查看真实 API 文档和示例，包含系统下游可能消费的全部字段，并核对 schema。不确定时包含所有已记录字段。

## 反模式 5：把集成测试当作事后补充

“实现完成，之后再测试”不是完成状态。测试属于实现的一部分，TDD 会在实现过程中暴露问题。

```text
1. 写失败测试
2. 实现到通过
3. 重构
4. 然后才能声称完成
```

## Mock 变得过于复杂时

以下信号说明应该考虑真实集成测试：mock setup 比测试逻辑更长、几乎所有东西都被 mock、mock 缺少真实组件的方法、mock 变化就导致测试崩溃。问：“这里真的需要 mock 吗？”真实组件的集成测试有时反而更简单。

## TDD 如何避免这些反模式

1. 先写测试，迫使你明确测什么；
2. 观察测试失败，确认它测的是行为；
3. 最小实现，避免测试专用方法混入生产代码；
4. 先看到真实依赖，再决定是否需要 mock。

如果你在测试 mock 行为，就说明没有先对真实代码观察到 RED 阶段的失败。

## 快速参考

| 反模式 | 修复 |
|---|---|
| 断言 mock 元素 | 测真实组件或取消 mock |
| 生产类中的测试专用方法 | 移到测试工具 |
| 不理解依赖就 mock | 先理解依赖，最小化 mock |
| 不完整 mock | 完整镜像真实 API |
| 测试事后补充 | 测试优先，遵循 TDD |
| 复杂 mock | 考虑集成测试 |

## 红旗

- 断言 `*-mock` test id；
- 方法只在测试文件中调用；
- mock setup 占测试一半以上；
- 删除 mock 后测试失败；
- 说不清 mock 为什么必要；
- “只是为了安全”而 mock。

## 底线

**Mock 是隔离工具，不是测试对象。**如果 TDD 暴露出你正在测试 mock 行为，说明方向错误：测试真实行为，或重新质疑为什么需要 mock。
