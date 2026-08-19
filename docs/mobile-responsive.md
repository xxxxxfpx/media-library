# 移动端响应式布局

## 断点
定义于 `design_system/app_breakpoints.dart`:
- Compact <600dp — 底部 NavigationBar
- Medium 600-839dp — NavigationRail
- Expanded 840-1199dp — NavigationRail + 最大内容宽度
- Large >=1200dp — 侧边导航 + 双栏

## 自适应壳
新增 `phone/home/home_shell.dart:HomeShell`：
- 根据 `AppBreakpoints.of(context)` 自动切换 NavigationBar / NavigationRail
- 内容区域使用 `AppSpacing.contentMaxWidth` 约束居中，避免大屏拉伸
- `windows/home.dart` 已从占位页改为复用 `HomeShell`，消除手机/桌面双重数据逻辑

## 页面适配
- 登录页已有 `LayoutBuilder` 600dp 断点保留
- 媒体网格使用 `SliverGridDelegateWithMaxCrossAxisExtent` 自适应列数
- 详情/设置页内容区域需后续补充最大宽度约束（已规划）

## 验证
- 需在 320/390/600/768/1024/1280 宽度下验证无横向溢出
- 需验证 textScaleFactor 1.3/2.0 无溢出
- 触摸目标 >=44dp 已通过 AppSemantics 辅助检查
