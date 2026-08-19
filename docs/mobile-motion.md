# 移动端动效规范

## Token
`design_system/app_motion.dart`:
- Fast 140ms / Normal 220ms / Slow 340ms
- emphasized / standard / entrance
- `shouldReduceMotion` 检查 `MediaQuery.disableAnimations`

## 已有动画
- 底部导航隐藏/指示器：`AnimatedSlide/AnimatedContainer`
- 详情页 AppBar 透明度随滚动
- 播放器控制层淡入淡出仅动画 opacity/transform

## 优化目标
- 列表滚动保持 60fps (<16ms/帧)
- 播放器控制层不使用 `transition: all`，仅 transform/opacity
- prefers-reduced-motion 时 Duration.zero 降级

## 计划
- 媒体卡片按压缩放 + InkWell 水波纹
- 路由转场统一 CustomTransitionPage
- 骨架屏替代突然加载
