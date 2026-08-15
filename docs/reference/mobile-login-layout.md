# Flutter 响应式布局详解

## 一、核心 API 介绍

### 1. MediaQuery.orientation

获取设备物理方向，返回 `Orientation` 枚举：

```dart
enum Orientation {
  portrait,   // 竖屏
  landscape,  // 横屏
}
```

**使用方式：**

```dart
// 获取当前方向
final orientation = MediaQuery.of(context).orientation;
final isLandscape = orientation == Orientation.landscape;

// 或者一行搞定
final isLandscape = MediaQuery.of(context).orientation == Orientation.landscape;
```

**注意：** 桌面和电视平台始终返回 `landscape`，不会随窗口大小变化。

---

### 2. LayoutBuilder

根据父级约束条件动态构建 UI，比 `MediaQuery` 更灵活：

```dart
LayoutBuilder(
  builder: (context, constraints) {
    // constraints.maxWidth  最大宽度
    // constraints.maxHeight 最大高度
    // constraints.minWidth  最小宽度
    // constraints.minHeight 最小高度

    if (constraints.maxWidth > 600) {
      return WideLayout();
    } else {
      return NarrowLayout();
    }
  },
)
```

**使用场景：**
- 需要根据可用空间而非屏幕方向来决定布局
- 同一个 widget 在不同父级容器中有不同表现
- 响应式 Web/桌面应用

---

### 3. Flex

`Row` 和 `Column` 的基类，支持动态切换主轴方向：

```dart
// Row 等同于
Flex(
  direction: Axis.horizontal,
  children: [...],
)

// Column 等同于
Flex(
  direction: Axis.vertical,
  children: [...],
)
```

**核心特点：**
- `direction` 可动态切换（这是与 Row/Column 的本质区别）
- 配合 `Expanded` 实现自适应布局

---

### 4. Expanded

让子组件填充 Flex 容器中的剩余空间：

```dart
Flex(
  direction: Axis.horizontal,
  children: [
    // 固定宽度
    Container(width: 100, child: ...),

    // 占据剩余空间的 2/3
    Expanded(
      flex: 2,
      child: ...,
    ),

    // 占据剩余空间的 1/3
    Expanded(
      flex: 1,
      child: ...,
    ),
  ],
)
```

**注意：** `Expanded` 必须放在 `Flex`（或 `Row`/`Column`）内部。

---

## 二、login.dart 布局原理解析

### 整体结构

```dart
Widget build(BuildContext context) {
  final isLandscape = MediaQuery.of(context).orientation == Orientation.landscape;

  return Flex(
    direction: isLandscape ? Axis.horizontal : Axis.vertical,  // 动态切换主轴
    children: [
      Expanded(
        flex: isLandscape ? 3 : 0,   // 横屏占 3 份，竖屏不占空间
        child: _MediaIcon(),
      ),
      Expanded(
        flex: isLandscape ? 2 : 1,   // 横屏占 2 份，竖屏占全部
        child: _buildForm(),
      ),
    ],
  );
}
```

### 横屏布局（Flex direction: horizontal）

```
┌──────────────────────────────────────────────────────┐
│  ┌──────────────────┐  ┌──────────────────────────┐  │
│  │                  │  │         媒体库            │  │
│  │                  │  │      登录到您的账户        │  │
│  │    MediaIcon     │  │                          │  │
│  │     (3/5)        │  │    [ 用户名输入框 ]       │  │
│  │                  │  │    [ 密码输入框   ]       │  │
│  │                  │  │    [    登录     ]       │  │
│  │                  │  │                          │  │
│  └──────────────────┘  └──────────────────────────┘  │
│           3 份                      2 份              │
└──────────────────────────────────────────────────────┘
```

### 竖屏布局（Flex direction: vertical）

```
┌───────────────────────┐
│  ┌─────────────────┐  │
│  │                 │  │
│  │    MediaIcon    │  │
│  │                 │  │
│  └─────────────────┘  │
│                       │
│       媒体库          │
│    登录到您的账户      │
│                       │
│  ┌─────────────────┐  │
│  │   用户名输入框   │  │
│  └─────────────────┘  │
│  ┌─────────────────┐  │
│  │   密码输入框     │  │
│  └─────────────────┘  │
│  ┌─────────────────┐  │
│  │      登录       │  │
│  └─────────────────┘  │
│                       │
└───────────────────────┘
```

---

## 三、条件渲染

通过 `if` 关键字在 children 列表中实现条件显示：

```dart
Flex(
  direction: isLandscape ? Axis.horizontal : Axis.vertical,
  children: [
    // 始终显示
    IconWidget(),

    // 仅横屏显示
    if (isLandscape) LandscapeOnlyWidget(),

    // 仅竖屏显示
    if (!isLandscape) PortraitOnlyWidget(),

    // 动态内容
    Expanded(child: isLandscape ? WideForm() : NarrowForm()),
  ],
)
```

---

## 四、完整示例代码

### 示例 1：简单的响应式布局

```dart
class ResponsiveExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final isLandscape =
        MediaQuery.of(context).orientation == Orientation.landscape;

    return Scaffold(
      body: Flex(
        direction: isLandscape ? Axis.horizontal : Axis.vertical,
        children: [
          Expanded(
            flex: isLandscape ? 1 : 0,
            child: Container(
              color: Colors.blue,
              child: Center(child: Text('侧边栏')),
            ),
          ),
          Expanded(
            flex: isLandscape ? 3 : 1,
            child: Container(
              color: Colors.white,
              child: Center(child: Text('主内容')),
            ),
          ),
        ],
      ),
    );
  }
}
```

### 示例 2：使用 LayoutBuilder 根据宽度切换

```dart
class AdaptiveExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // 手机：单列 | 平板/桌面：双列
        final isWide = constraints.maxWidth > 600;

        return Scaffold(
          body: isWide
              ? Row(children: [ListView(), GridView()])
              : ListView(),
        );
      },
    );
  }
}
```

### 示例 3：横竖屏差异化 padding

```dart
Widget build(BuildContext context) {
  final isLandscape =
      MediaQuery.of(context).orientation == Orientation.landscape;

  return Padding(
    padding: EdgeInsets.symmetric(
      horizontal: isLandscape ? 24 : 32,  // 横屏左右 24，竖屏左右 32
      vertical: isLandscape ? 16 : 24,   // 横屏上下 16，竖屏上下 24
    ),
    child: Content(),
  );
}
```

---

## 五、注意事项

| 问题 | 解决方案 |
|------|---------|
| 竖屏时 icon 占据空间导致表单被挤压 | `flex: 0` 让 icon 不参与 Flex 空间分配 |
| 键盘弹出后布局异常 | 用 `SingleChildScrollView` 包裹表单 |
| 桌面端无法切换横竖屏 | 使用 `LayoutBuilder` + 宽度判断替代 orientation |
| 快速旋转时布局抖动 | 使用 `FittedBox` 或 `Flexible` 预留弹性空间 |

---

## 六、相关资料

- [Flutter 官方文档 - LayoutBuilder](https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html)
- [Flutter 官方文档 - Flex](https://api.flutter.dev/flutter/widgets/Flex-class.html)
- [Flutter 官方文档 - MediaQuery](https://api.flutter.dev/flutter/widgets/MediaQuery-class.html)
- [Flutter 官方文档 - Orientation](https://api.flutter.dev/flutter/dart-ui/Orientation.html)