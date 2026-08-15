> 原文链接: [https://docs.flutter.dev/testing/code-debugging](https://docs.flutter.dev/testing/code-debugging)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This guide describes which debugging features you can enable in your code.
                  For a full list of debugging and profiling tools, check out the[Debugging](https://docs.flutter.dev/testing/debugging)page.

## Add logging to your application

The following list contains a few statements that you can use to log the
                  behavior of your application. You can view your logs in DevTools'[Logging view](https://docs.flutter.dev/tools/devtools/logging)or in your system console.

- code-excerpt "lib/main.dart (stderr)"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

[print()](https://api.flutter.dev/flutter/dart-core/print.html): Prints a`stdout`(standard output) message. Part of the`dart:io`library.

`print()`
`stdout`
`dart:io`
[stderr.method_to_invoke()](https://api.flutter.dev/flutter/dart-io/stderr.html): Prints a`stderr`(standard error) message.
                      Replace`method_to_invoke()`with a method supported by the`stderr`property, such as`writeln()`or`write()`. Often used in a`try...catch`block. Part of the`dart:io`library.

`stderr.method_to_invoke()`
`stderr`
`method_to_invoke()`
`stderr`
`writeln()`
`write()`
`try...catch`
`dart:io`
`stderr.writeln('print me');`
[log()](https://api.flutter.dev/flutter/dart-developer/log.html): Includes greater granularity and more information in the
                      logging output. Part of the`dart:developer`library.

`log()`
`dart:developer`
[debugPrint()](https://api.flutter.dev/flutter/widgets/debugPrint.html): If too much output results in discarded log lines, use
                      this to keep those lines. Will print messages in release mode unless part
                      of a debug mode check or an assert. Part of the`foundations`library.

`debugPrint()`
`foundations`
### Example 1

`import 'dart:developer' as developer;
​
void main() {
  developer.log('log me', name: 'my.app.category');
​
  developer.log('log me 1', name: 'my.other.category');
  developer.log('log me 2', name: 'my.other.category');
}`
You can also pass app data to the log call.
                  The convention for this is to use the`error:`named
                  parameter on the`log()`call, JSON encode the object
                  you want to send, and pass the encoded string to the
                  error parameter.

`error:`
`log()`
### Example 2

`import 'dart:convert';
import 'dart:developer' as developer;
​
void main() {
  var myCustomObject = MyCustomObject();
​
  developer.log(
    'log me',
    name: 'my.app.category',
    error: jsonEncode(myCustomObject),
  );
}`
DevTool's logging view interprets the JSON encoded error parameter
                  as a data object.
                  DevTool renders in the details view for that log entry.

## Set breakpoints

You can set breakpoints in DevTools'[Debugger](https://docs.flutter.dev/tools/devtools/debugger)or
                  in the built-in debugger of your IDE.

To set programmatic breakpoints:


Import the`dart:developer`package into the relevant file.

`dart:developer`
Insert programmatic breakpoints using the`debugger()`statement.
                      This statement takes an optional`when`argument.
                      This boolean argument sets a break when the given condition resolves to true.

`debugger()`
`when`
**Example 3**illustrates this.

### Example 3

`import 'dart:developer';
​
void someFunction(double offset) {
  debugger(when: offset > 30);
  // ...
}`
## Debug app layers using flags

Each layer of the Flutter framework provides a function to dump its
                  current state or events to the console using the`debugPrint`property.

`debugPrint`
### Print the widget tree

To dump the state of the Widgets library,
                  call the[debugDumpApp()](https://api.flutter.dev/flutter/widgets/debugDumpApp.html)function.

`debugDumpApp()`
1. Open your source file.
1. Import`package:flutter/rendering.dart`.
1. Call the[debugDumpApp()](https://api.flutter.dev/flutter/widgets/debugDumpApp.html)function from within the`runApp()`function.
                    You need your app in debug mode.
                    You cannot call this function inside a`build()`method
                    when the app is building.
1. If you haven't started your app, debug it using your IDE.
1. If you have started your app, save your source file.
                    Hot reload re-renders your app.

`package:flutter/rendering.dart`
`debugDumpApp()`
`runApp()`
`build()`
#### Example 4: CalldebugDumpApp()

`debugDumpApp()`
`import 'package:flutter/material.dart';
​
void main() {
  runApp(const MaterialApp(home: AppHome()));
}
​
class AppHome extends StatelessWidget {
  const AppHome({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Material(
      child: Center(
        child: TextButton(
          onPressed: () {
            debugDumpApp();
          },
          child: const Text('Dump Widget Tree'),
        ),
      ),
    );
  }
}`
This function recursively calls the`toStringDeep()`method starting with
                  the root of the widget tree. It returns a "flattened" tree.

`toStringDeep()`
**Example 4**produces the following widget tree. It includes:


All the widgets projected through their various build functions.

Many widgets that don't appear in your app's source.
                      The framework's widgets' build functions insert them during the build.

The following tree, for example, shows[_InkFeatures](https://api.flutter.dev/flutter/material/InkFeature-class.html).
                      That class implements part of the[Material](https://api.flutter.dev/flutter/material/Material-class.html)widget.
                      It doesn't appear anywhere in the code in**Example 4**.

`_InkFeatures`
`Material`
`flutter: WidgetsFlutterBinding - DEBUG MODE
flutter: [root](renderObject: RenderView#06beb)
flutter: └View-[GlobalObjectKey FlutterView#7971c]
flutter:  └_ViewScope
flutter:   └_MediaQueryFromView(state: _MediaQueryFromViewState#d790c)
flutter:    └MediaQuery(MediaQueryData(size: Size(800.0, 600.0), devicePixelRatio: 1.0, textScaleFactor: 1.0, platformBrightness: Brightness.dark, padding: EdgeInsets.zero, viewPadding: EdgeInsets.zero, viewInsets: EdgeInsets.zero, systemGestureInsets: EdgeInsets.zero, alwaysUse24HourFormat: false, accessibleNavigation: false, highContrast: false, disableAnimations: false, invertColors: false, boldText: false, navigationMode: traditional, gestureSettings: DeviceGestureSettings(touchSlop: null), displayFeatures: []))
flutter:     └MaterialApp(state: _MaterialAppState#27fa9)
flutter:      └ScrollConfiguration(behavior: MaterialScrollBehavior)
flutter:       └HeroControllerScope
flutter:        └Focus(state: _FocusState#d7f97)
flutter:         └_FocusInheritedScope
flutter:          └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#a6464)
flutter:           └WidgetsApp-[GlobalObjectKey _MaterialAppState#27fa9](state: _WidgetsAppState#b5b17)
flutter:            └RootRestorationScope(state: _RootRestorationScopeState#6b028)
flutter:             └UnmanagedRestorationScope
flutter:              └RestorationScope(dependencies: [UnmanagedRestorationScope], state: _RestorationScopeState#d1369)
flutter:               └UnmanagedRestorationScope
flutter:                └SharedAppData(state: _SharedAppDataState#95e82)
flutter:                 └_SharedAppModel
flutter:                  └Shortcuts(shortcuts: <Default WidgetsApp Shortcuts>, state: _ShortcutsState#272dc)
flutter:                   └Focus(debugLabel: "Shortcuts", dependencies: [_FocusInheritedScope], state: _FocusState#a3300)
flutter:                    └_FocusInheritedScope
flutter:                     └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#db110)
flutter:                      └DefaultTextEditingShortcuts
flutter:                       └Shortcuts(shortcuts: <Default Text Editing Shortcuts>, state: _ShortcutsState#1d796)
flutter:                        └Focus(debugLabel: "Shortcuts", dependencies: [_FocusInheritedScope], state: _FocusState#0081b)
flutter:                         └_FocusInheritedScope
flutter:                          └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#0d70e)
flutter:                           └Shortcuts(shortcuts: <Web Disabling Text Editing Shortcuts>, state: _ShortcutsState#56bac)
flutter:                            └Focus(debugLabel: "Shortcuts", dependencies: [_FocusInheritedScope], state: _FocusState#3152e)
flutter:                             └_FocusInheritedScope
flutter:                              └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#b7eaf)
flutter:                               └Actions(dispatcher: null, actions: {DoNothingIntent: DoNothingAction#0fda1, DoNothingAndStopPropagationIntent: DoNothingAction#17f30, RequestFocusIntent: RequestFocusAction#10bd0, NextFocusIntent: NextFocusAction#60317, PreviousFocusIntent: PreviousFocusAction#2a933, DirectionalFocusIntent: DirectionalFocusAction#a6922, ScrollIntent: _OverridableContextAction<ScrollIntent>#964fe(defaultAction: ScrollAction#ffb50), PrioritizedIntents: PrioritizedAction#be0e2, VoidCallbackIntent: VoidCallbackAction#805fa}, state: _ActionsState#bbd25)
flutter:                                └_ActionsScope
flutter:                                 └FocusTraversalGroup(policy: ReadingOrderTraversalPolicy#f1e76, state: _FocusTraversalGroupState#0c200)
flutter:                                  └Focus(debugLabel: "FocusTraversalGroup", focusNode: _FocusTraversalGroupNode#ffcad(FocusTraversalGroup [IN FOCUS PATH]), dependencies: [_FocusInheritedScope], state: _FocusState#c7dc2)
flutter:                                   └_FocusInheritedScope
flutter:                                    └TapRegionSurface(renderObject: RenderTapRegionSurface#17aba)
flutter:                                     └ShortcutRegistrar(state: _ShortcutRegistrarState#44954)
flutter:                                      └_ShortcutRegistrarScope
flutter:                                       └Shortcuts(manager: ShortcutManager#eb38c(shortcuts: {}), shortcuts: {}, state: _ShortcutsState#f85ac)
flutter:                                        └Focus(debugLabel: "Shortcuts", dependencies: [_FocusInheritedScope], state: _FocusState#8c1a7)
flutter:                                         └_FocusInheritedScope
flutter:                                          └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#1fc98)
flutter:                                           └Localizations(locale: en_US, delegates: [DefaultMaterialLocalizations.delegate(en_US), DefaultCupertinoLocalizations.delegate(en_US), DefaultWidgetsLocalizations.delegate(en_US)], state: _LocalizationsState#ae3a0)
flutter:                                            └Semantics(container: false, properties: SemanticsProperties, tooltip: null, textDirection: ltr, renderObject: RenderSemanticsAnnotations#8776e)
flutter:                                             └_LocalizationsScope-[GlobalKey#61ca6]
flutter:                                              └Directionality(textDirection: ltr)
flutter:                                               └Title(color: Color(0xff2196f3))
flutter:                                                └CheckedModeBanner("DEBUG")
flutter:                                                 └Banner("DEBUG", textDirection: ltr, location: topEnd, Color(0xa0b71c1c), text inherit: true, text color: Color(0xffffffff), text size: 10.2, text weight: 900, text height: 1.0x, dependencies: [Directionality])
flutter:                                                  └CustomPaint(renderObject: RenderCustomPaint#c014d)
flutter:                                                   └DefaultTextStyle(debugLabel: fallback style; consider putting your text in a Material, inherit: true, color: Color(0xd0ff0000), family: monospace, size: 48.0, weight: 900, decoration: double Color(0xffffff00) TextDecoration.underline, softWrap: wrapping at box width, overflow: clip)
flutter:                                                    └Builder(dependencies: [MediaQuery])
flutter:                                                     └ScaffoldMessenger(dependencies: [MediaQuery], state: ScaffoldMessengerState#5b36e)
flutter:                                                      └_ScaffoldMessengerScope
flutter:                                                       └DefaultSelectionStyle
flutter:                                                        └AnimatedTheme(duration: 200ms, state: _AnimatedThemeState#cd149(ticker inactive, ThemeDataTween(ThemeData#ef3b2 → ThemeData#ef3b2)))
flutter:                                                         └Theme(ThemeData#ef3b2, dependencies: [DefaultSelectionStyle])
flutter:                                                          └_InheritedTheme
flutter:                                                           └CupertinoTheme(brightness: light, primaryColor: MaterialColor(primary value: Color(0xff2196f3)), primaryContrastingColor: Color(0xffffffff), scaffoldBackgroundColor: Color(0xfffafafa), actionTextStyle: TextStyle(inherit: false, color: MaterialColor(primary value: Color(0xff2196f3)), family: .SF Pro Text, size: 17.0, letterSpacing: -0.4, decoration: TextDecoration.none), navActionTextStyle: TextStyle(inherit: false, color: MaterialColor(primary value: Color(0xff2196f3)), family: .SF Pro Text, size: 17.0, letterSpacing: -0.4, decoration: TextDecoration.none))
flutter:                                                            └_InheritedCupertinoTheme
flutter:                                                             └IconTheme(color: MaterialColor(primary value: Color(0xff2196f3)))
flutter:                                                              └IconTheme(color: Color(0xdd000000))
flutter:                                                               └DefaultSelectionStyle
flutter:                                                                └FocusScope(debugLabel: "Navigator Scope", AUTOFOCUS, dependencies: [_FocusInheritedScope], state: _FocusScopeState#acbd8)
flutter:                                                                 └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#ab3f0)
flutter:                                                                  └_FocusInheritedScope
flutter:                                                                   └Navigator-[GlobalObjectKey<NavigatorState> _WidgetsAppState#b5b17](dependencies: [HeroControllerScope, UnmanagedRestorationScope], state: NavigatorState#1395a(tickers: tracking 1 ticker))
flutter:                                                                    └HeroControllerScope
flutter:                                                                     └Listener(listeners: [down, up, cancel], behavior: deferToChild, renderObject: RenderPointerListener#34172)
flutter:                                                                      └AbsorbPointer(absorbing: false, renderObject: RenderAbsorbPointer#f8711)
flutter:                                                                       └FocusTraversalGroup(policy: ReadingOrderTraversalPolicy#f1e76, state: _FocusTraversalGroupState#8d61a)
flutter:                                                                        └Focus(debugLabel: "FocusTraversalGroup", focusNode: _FocusTraversalGroupNode#dd2b1(FocusTraversalGroup [IN FOCUS PATH]), dependencies: [_FocusInheritedScope], state: _FocusState#0bb03)
flutter:                                                                         └_FocusInheritedScope
flutter:                                                                          └Focus(debugLabel: "Navigator", AUTOFOCUS, focusNode: FocusNode#a3309(Navigator [IN FOCUS PATH]), dependencies: [_FocusInheritedScope], state: _FocusState#d3d07)
flutter:                                                                           └_FocusInheritedScope
flutter:                                                                            └UnmanagedRestorationScope
flutter:                                                                             └Overlay-[LabeledGlobalKey<OverlayState>#5485a](state: OverlayState#5bd52(entries: [OverlayEntry#fc947(opaque: true; maintainState: false), OverlayEntry#05a32(opaque: false; maintainState: true)]))
flutter:                                                                              └_Theater(skipCount: 0, dependencies: [Directionality], renderObject: _RenderTheater#e86c3)
flutter:                                                                               ├_OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#1b37e](state: _OverlayEntryWidgetState#06ab0)
flutter:                                                                               │└TickerMode(state: _TickerModeState#0b4ac(requested mode: enabled))
flutter:                                                                               │ └_EffectiveTickerMode(effective mode: enabled)
flutter:                                                                               │  └_RenderTheaterMarker
flutter:                                                                               │   └IgnorePointer(ignoring: false, renderObject: RenderIgnorePointer#34c66)
flutter:                                                                               │    └ModalBarrier
flutter:                                                                               │     └BlockSemantics(blocking: true, renderObject: RenderBlockSemantics#97799)
flutter:                                                                               │      └ExcludeSemantics(excluding: true, renderObject: RenderExcludeSemantics#8c4ce)
flutter:                                                                               │       └_ModalBarrierGestureDetector
flutter:                                                                               │        └RawGestureDetector(state: RawGestureDetectorState#556f6(gestures: [any tap], behavior: opaque))
flutter:                                                                               │         └_GestureSemantics(renderObject: RenderSemanticsGestureHandler#616f1)
flutter:                                                                               │          └Listener(listeners: [down, panZoomStart], behavior: opaque, renderObject: RenderPointerListener#c2b89)
flutter:                                                                               │           └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#c3b31)
flutter:                                                                               │            └MouseRegion(listeners: <none>, cursor: SystemMouseCursor(basic), renderObject: RenderMouseRegion#53cdb)
flutter:                                                                               │             └ConstrainedBox(BoxConstraints(biggest), renderObject: RenderConstrainedBox#faa51)
flutter:                                                                               └_OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#bc0aa](state: _OverlayEntryWidgetState#cbf35)
flutter:                                                                                └TickerMode(state: _TickerModeState#23e73(requested mode: enabled))
flutter:                                                                                 └_EffectiveTickerMode(effective mode: enabled)
flutter:                                                                                  └_RenderTheaterMarker
flutter:                                                                                   └Semantics(container: false, properties: SemanticsProperties, tooltip: null, sortKey: OrdinalSortKey#135f4(order: 0.0), renderObject: RenderSemanticsAnnotations#5565e)
flutter:                                                                                    └_ModalScope<dynamic>-[LabeledGlobalKey<_ModalScopeState<dynamic>>#4fe82](state: _ModalScopeState<dynamic>#4da7d)
flutter:                                                                                     └AnimatedBuilder(listenable: ValueNotifier<String?>#d87c6(null), state: _AnimatedState#dde81)
flutter:                                                                                      └RestorationScope(dependencies: [UnmanagedRestorationScope], state: _RestorationScopeState#78c51)
flutter:                                                                                       └UnmanagedRestorationScope
flutter:                                                                                        └_ModalScopeStatus(active)
flutter:                                                                                         └Offstage(offstage: false, renderObject: RenderOffstage#5e498)
flutter:                                                                                          └PageStorage
flutter:                                                                                           └Builder
flutter:                                                                                            └Actions(dispatcher: null, actions: {DismissIntent: _DismissModalAction#6279e}, state: _ActionsState#48019)
flutter:                                                                                             └_ActionsScope
flutter:                                                                                              └PrimaryScrollController(ScrollController#6a546(no clients))
flutter:                                                                                               └FocusScope(debugLabel: "_ModalScopeState<dynamic> Focus Scope", focusNode: FocusScopeNode#0e2af(_ModalScopeState<dynamic> Focus Scope [PRIMARY FOCUS]), dependencies: [_FocusInheritedScope], state: _FocusScopeState#0bac4)
flutter:                                                                                                └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#44b4e)
flutter:                                                                                                 └_FocusInheritedScope
flutter:                                                                                                  └RepaintBoundary(renderObject: RenderRepaintBoundary#38f41)
flutter:                                                                                                   └AnimatedBuilder(listenable: Listenable.merge([AnimationController#9d623(⏭ 1.000; paused; for MaterialPageRoute<dynamic>(/))➩ProxyAnimation, kAlwaysDismissedAnimation➩ProxyAnimation➩ProxyAnimation]), dependencies: [_InheritedTheme, _LocalizationsScope-[GlobalKey#61ca6]], state: _AnimatedState#47725)
flutter:                                                                                                    └CupertinoPageTransition(dependencies: [Directionality])
flutter:                                                                                                     └SlideTransition(listenable: kAlwaysDismissedAnimation➩ProxyAnimation➩ProxyAnimation➩Cubic(0.35, 0.91, 0.33, 0.97)ₒₙ/Cubic(0.67, 0.03, 0.65, 0.09)➩Tween<Offset>(Offset(0.0, 0.0) → Offset(-0.3, 0.0))➩Offset(0.0, 0.0), state: _AnimatedState#b6162)
flutter:                                                                                                      └FractionalTranslation(renderObject: RenderFractionalTranslation#fb461)
flutter:                                                                                                       └SlideTransition(listenable: AnimationController#9d623(⏭ 1.000; paused; for MaterialPageRoute<dynamic>(/))➩ProxyAnimation➩ThreePointCubic ₒₙ/FlippedCurve(ThreePointCubic )➩Tween<Offset>(Offset(1.0, 0.0) → Offset(0.0, 0.0))➩Offset(0.0, 0.0), state: _AnimatedState#834bf)
flutter:                                                                                                        └FractionalTranslation(renderObject: RenderFractionalTranslation#73ea4)
flutter:                                                                                                         └DecoratedBoxTransition(listenable: AnimationController#9d623(⏭ 1.000; paused; for MaterialPageRoute<dynamic>(/))➩ProxyAnimation➩Cubic(0.35, 0.91, 0.33, 0.97)➩DecorationTween(_CupertinoEdgeShadowDecoration(colors: null) → _CupertinoEdgeShadowDecoration(colors: [Color(0x04000000), Color(0x00000000)]))➩_CupertinoEdgeShadowDecoration(colors: [Color(0x04000000), Color(0x00000000)]), state: _AnimatedState#a7fca)
flutter:                                                                                                          └DecoratedBox(bg: _CupertinoEdgeShadowDecoration(colors: [Color(0x04000000), Color(0x00000000)]), dependencies: [Directionality, MediaQuery, _LocalizationsScope-[GlobalKey#61ca6]], renderObject: RenderDecoratedBox#9965c)
flutter:                                                                                                           └_CupertinoBackGestureDetector<dynamic>(dependencies: [Directionality, MediaQuery], state: _CupertinoBackGestureDetectorState<dynamic>#ab8cd)
flutter:                                                                                                            └Stack(alignment: AlignmentDirectional.topStart, fit: passthrough, dependencies: [Directionality], renderObject: RenderStack#b2b7c)
flutter:                                                                                                             ├AnimatedBuilder(listenable: ValueNotifier<bool>#1a88e(false), state: _AnimatedState#6e33c)
flutter:                                                                                                             │└IgnorePointer(ignoring: false, renderObject: RenderIgnorePointer#2b763)
flutter:                                                                                                             │ └RepaintBoundary-[GlobalKey#628f4](renderObject: RenderRepaintBoundary#5a53b)
flutter:                                                                                                             │  └Builder
flutter:                                                                                                             │   └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#f8795)
flutter:                                                                                                             │    └AppHome
flutter:                                                                                                             │     └Material(type: canvas, dependencies: [_InheritedTheme, _LocalizationsScope-[GlobalKey#61ca6]], state: _MaterialState#7d183)
flutter:                                                                                                             │      └AnimatedPhysicalModel(duration: 200ms, shape: rectangle, borderRadius: BorderRadius.zero, elevation: 0.0, color: Color(0xfffafafa), animateColor: false, shadowColor: Color(0xff000000), animateShadowColor: true, state: _AnimatedPhysicalModelState#d479e(ticker inactive))
flutter:                                                                                                             │       └PhysicalModel(shape: rectangle, borderRadius: BorderRadius.zero, elevation: 0.0, color: Color(0xfffafafa), shadowColor: Color(0xff000000), renderObject: RenderPhysicalModel#c60b5)
flutter:                                                                                                             │        └NotificationListener<LayoutChangedNotification>
flutter:                                                                                                             │         └_InkFeatures-[GlobalKey#e9da0 ink renderer](renderObject: _RenderInkFeatures#d8e6d)
flutter:                                                                                                             │          └AnimatedDefaultTextStyle(duration: 200ms, debugLabel: (englishLike bodyMedium 2014).merge(blackRedwoodCity bodyMedium), inherit: false, color: Color(0xdd000000), family: .AppleSystemUIFont, size: 14.0, weight: 400, baseline: alphabetic, decoration: TextDecoration.none, softWrap: wrapping at box width, overflow: clip, state: _AnimatedDefaultTextStyleState#12f43(ticker inactive))
flutter:                                                                                                             │           └DefaultTextStyle(debugLabel: (englishLike bodyMedium 2014).merge(blackRedwoodCity bodyMedium), inherit: false, color: Color(0xdd000000), family: .AppleSystemUIFont, size: 14.0, weight: 400, baseline: alphabetic, decoration: TextDecoration.none, softWrap: wrapping at box width, overflow: clip)
flutter:                                                                                                             │            └Center(alignment: Alignment.center, dependencies: [Directionality], renderObject: RenderPositionedBox#b088f)
flutter:                                                                                                             │             └TextButton(dirty, dependencies: [MediaQuery, _InheritedTheme, _LocalizationsScope-[GlobalKey#61ca6]], state: _ButtonStyleState#687c9)
flutter:                                                                                                             │              └Semantics(container: true, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#ca411 relayoutBoundary=up1)
flutter:                                                                                                             │               └_InputPadding(renderObject: _RenderInputPadding#60ede relayoutBoundary=up2)
flutter:                                                                                                             │                └ConstrainedBox(BoxConstraints(56.0<=w<=Infinity, 28.0<=h<=Infinity), renderObject: RenderConstrainedBox#34800 relayoutBoundary=up3)
flutter:                                                                                                             │                 └Material(type: button, color: Color(0x00000000), shadowColor: Color(0xff000000), textStyle.debugLabel: ((englishLike labelLarge 2014).merge(blackRedwoodCity labelLarge)).copyWith, textStyle.inherit: false, textStyle.color: MaterialColor(primary value: Color(0xff2196f3)), textStyle.family: .AppleSystemUIFont, textStyle.size: 14.0, textStyle.weight: 500, textStyle.baseline: alphabetic, textStyle.decoration: TextDecoration.none, shape: RoundedRectangleBorder(BorderSide(width: 0.0, style: none), BorderRadius.circular(4.0)), dependencies: [_InheritedTheme, _LocalizationsScope-[GlobalKey#61ca6]], state: _MaterialState#50a4d(tickers: tracking 5 tickers))
flutter:                                                                                                             │                  └_MaterialInterior(duration: 200ms, shape: RoundedRectangleBorder(BorderSide(width: 0.0, style: none), BorderRadius.circular(4.0)), elevation: 0.0, color: Color(0x00000000), shadowColor: Color(0xff000000), dependencies: [Directionality, _InheritedTheme, _LocalizationsScope-[GlobalKey#61ca6]], state: _MaterialInteriorState#d296d(ticker inactive))
flutter:                                                                                                             │                   └PhysicalShape(clipper: ShapeBorderClipper, elevation: 0.0, color: Color(0x00000000), shadowColor: Color(0xff000000), renderObject: RenderPhysicalShape#43df6 relayoutBoundary=up4)
flutter:                                                                                                             │                    └_ShapeBorderPaint(dependencies: [Directionality])
flutter:                                                                                                             │                     └CustomPaint(renderObject: RenderCustomPaint#c1a3c relayoutBoundary=up5)
flutter:                                                                                                             │                      └NotificationListener<LayoutChangedNotification>
flutter:                                                                                                             │                       └_InkFeatures-[GlobalKey#625bc ink renderer](renderObject: _RenderInkFeatures#54439 relayoutBoundary=up6)
flutter:                                                                                                             │                        └AnimatedDefaultTextStyle(duration: 200ms, debugLabel: ((englishLike labelLarge 2014).merge(blackRedwoodCity labelLarge)).copyWith, inherit: false, color: MaterialColor(primary value: Color(0xff2196f3)), family: .AppleSystemUIFont, size: 14.0, weight: 500, baseline: alphabetic, decoration: TextDecoration.none, softWrap: wrapping at box width, overflow: clip, state: _AnimatedDefaultTextStyleState#2f29d(ticker inactive))
flutter:                                                                                                             │                         └DefaultTextStyle(debugLabel: ((englishLike labelLarge 2014).merge(blackRedwoodCity labelLarge)).copyWith, inherit: false, color: MaterialColor(primary value: Color(0xff2196f3)), family: .AppleSystemUIFont, size: 14.0, weight: 500, baseline: alphabetic, decoration: TextDecoration.none, softWrap: wrapping at box width, overflow: clip)
flutter:                                                                                                             │                          └InkWell
flutter:                                                                                                             │                           └_InkResponseStateWidget(gestures: [tap], mouseCursor: ButtonStyleButton_MouseCursor, clipped to BoxShape.rectangle, dirty, dependencies: [Directionality, MediaQuery, _InheritedTheme, _LocalizationsScope-[GlobalKey#61ca6]], state: _InkResponseState#0b11d)
flutter:                                                                                                             │                            └_ParentInkResponseProvider
flutter:                                                                                                             │                             └Actions(dispatcher: null, actions: {ActivateIntent: CallbackAction<ActivateIntent>#018db, ButtonActivateIntent: CallbackAction<ButtonActivateIntent>#ef87a}, state: _ActionsState#a5eab)
flutter:                                                                                                             │                              └_ActionsScope
flutter:                                                                                                             │                               └Focus(dependencies: [_FocusInheritedScope], state: _FocusState#5a9de)
flutter:                                                                                                             │                                └_FocusInheritedScope
flutter:                                                                                                             │                                 └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#8ac3e relayoutBoundary=up7)
flutter:                                                                                                             │                                  └MouseRegion(listeners: [enter, exit], cursor: SystemMouseCursor(click), renderObject: RenderMouseRegion#13d4e relayoutBoundary=up8)
flutter:                                                                                                             │                                   └Builder(dependencies: [DefaultSelectionStyle])
flutter:                                                                                                             │                                    └DefaultSelectionStyle
flutter:                                                                                                             │                                     └Semantics(container: false, properties: SemanticsProperties, tooltip: null, renderObject: RenderSemanticsAnnotations#d99cc relayoutBoundary=up9)
flutter:                                                                                                             │                                      └GestureDetector(startBehavior: start, dependencies: [MediaQuery])
flutter:                                                                                                             │                                       └RawGestureDetector(state: RawGestureDetectorState#b8d93(gestures: [tap], excludeFromSemantics: true, behavior: opaque))
flutter:                                                                                                             │                                        └Listener(listeners: [down, panZoomStart], behavior: opaque, renderObject: RenderPointerListener#a4c3b relayoutBoundary=up10)
flutter:                                                                                                             │                                         └Builder(dependencies: [IconTheme])
flutter:                                                                                                             │                                          └IconTheme(color: MaterialColor(primary value: Color(0xff2196f3)))
flutter:                                                                                                             │                                           └Padding(padding: EdgeInsets(8.0, 0.0, 8.0, 0.0), dependencies: [Directionality], renderObject: RenderPadding#18a87 relayoutBoundary=up11)
flutter:                                                                                                             │                                            └Align(alignment: Alignment.center, widthFactor: 1.0, heightFactor: 1.0, dependencies: [Directionality], renderObject: RenderPositionedBox#fb8a8 relayoutBoundary=up12)
flutter:                                                                                                             │                                             └Text("Dump Widget Tree", dependencies: [DefaultSelectionStyle, DefaultTextStyle, MediaQuery])
flutter:                                                                                                             │                                              └RichText(softWrap: wrapping at box width, maxLines: unlimited, text: "Dump Widget Tree", dependencies: [Directionality, _LocalizationsScope-[GlobalKey#61ca6]], renderObject: RenderParagraph#d15aa relayoutBoundary=up13)
flutter:                                                                                                             └PositionedDirectional(dependencies: [Directionality])
flutter:                                                                                                              └Positioned(left: 0.0, top: 0.0, bottom: 0.0, width: 20.0)
flutter:                                                                                                               └Listener(listeners: [down], behavior: translucent, renderObject: RenderPointerListener#d884c)
flutter:
flutter:`
When the button changes from being pressed to being released,
                  this invokes the`debugDumpApp()`function.
                  It also coincides with the[TextButton](https://api.flutter.dev/flutter/material/TextButton-class.html)object calling[setState()](https://api.flutter.dev/flutter/widgets/State/setState.html)and thus marking itself dirty.
                  This explains why a Flutter marks a specific object as "dirty".
                  When you review the widget tree, look for a line that resembles the following:

`debugDumpApp()`
`TextButton`
`setState()`
`└TextButton(dirty, dependencies: [MediaQuery, _InheritedTheme, _LocalizationsScope-[GlobalKey#5880d]], state: _ButtonStyleState#ab76e)`
If you write your own widgets, override the[debugFillProperties()](https://api.flutter.dev/flutter/widgets/Widget/debugFillProperties.html)method to add information.
                  Add[DiagnosticsProperty](https://api.flutter.dev/flutter/foundation/DiagnosticsProperty-class.html)objects to the method's argument
                  and call the superclass method.
                  The`toString`method uses this function to fill in the widget's description.

`debugFillProperties()`
`toString`
### Print the render tree

When debugging a layout issue, the Widgets layer's tree might lack detail.
                  The next level of debugging might require a render tree.
                  To dump the render tree:

1. Open your source file.
1. Call the[debugDumpRenderTree()](https://api.flutter.dev/flutter/rendering/debugDumpRenderTree.html)function.
                    You can call this any time except during a layout or paint phase.
                    Consider calling it from a[frame callback](https://api.flutter.dev/flutter/scheduler/SchedulerBinding/addPersistentFrameCallback.html)or an event handler.
1. If you haven't started your app, debug it using your IDE.
1. If you have started your app, save your source file.
                    Hot reload re-renders your app.

`debugDumpRenderTree()`
#### Example 5: CalldebugDumpRenderTree()

`debugDumpRenderTree()`
`import 'package:flutter/material.dart';
​
void main() {
  runApp(const MaterialApp(home: AppHome()));
}
​
class AppHome extends StatelessWidget {
  const AppHome({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Material(
      child: Center(
        child: TextButton(
          onPressed: () {
            debugDumpRenderTree();
          },
          child: const Text('Dump Render Tree'),
        ),
      ),
    );
  }
}`
When debugging layout issues, look at the`size`and`constraints`fields.
                  The constraints flow down the tree and the sizes flow back up.

`size`
`constraints`
`flutter: RenderView#02c80
flutter:  │ debug mode enabled - macos
flutter:  │ view size: Size(800.0, 600.0) (in physical pixels)
flutter:  │ device pixel ratio: 1.0 (physical pixels per logical pixel)
flutter:  │ configuration: Size(800.0, 600.0) at 1.0x (in logical pixels)
flutter:  │
flutter:  └─child: RenderSemanticsAnnotations#fe6b5
flutter:    │ needs compositing
flutter:    │ creator: Semantics ← _FocusInheritedScope ← Focus ←
flutter:    │   HeroControllerScope ← ScrollConfiguration ← MaterialApp ←
flutter:    │   MediaQuery ← _MediaQueryFromView ← _ViewScope ←
flutter:    │   View-[GlobalObjectKey FlutterView#6cffa] ← [root]
flutter:    │ parentData: <none>
flutter:    │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:    │ size: Size(800.0, 600.0)
flutter:    │
flutter:    └─child: RenderSemanticsAnnotations#6edef
flutter:      │ needs compositing
flutter:      │ creator: Semantics ← _FocusInheritedScope ← Focus ← Shortcuts ←
flutter:      │   _SharedAppModel ← SharedAppData ← UnmanagedRestorationScope ←
flutter:      │   RestorationScope ← UnmanagedRestorationScope ←
flutter:      │   RootRestorationScope ← WidgetsApp-[GlobalObjectKey
flutter:      │   _MaterialAppState#5c303] ← Semantics ← ⋯
flutter:      │ parentData: <none> (can use size)
flutter:      │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:      │ size: Size(800.0, 600.0)
flutter:      │
flutter:      └─child: RenderSemanticsAnnotations#e8ce8
flutter:        │ needs compositing
flutter:        │ creator: Semantics ← _FocusInheritedScope ← Focus ← Shortcuts ←
flutter:        │   DefaultTextEditingShortcuts ← Semantics ← _FocusInheritedScope
flutter:        │   ← Focus ← Shortcuts ← _SharedAppModel ← SharedAppData ←
flutter:        │   UnmanagedRestorationScope ← ⋯
flutter:        │ parentData: <none> (can use size)
flutter:        │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:        │ size: Size(800.0, 600.0)
flutter:        │
flutter:        └─child: RenderSemanticsAnnotations#fc545
flutter:          │ needs compositing
flutter:          │ creator: Semantics ← _FocusInheritedScope ← Focus ← Shortcuts ←
flutter:          │   Semantics ← _FocusInheritedScope ← Focus ← Shortcuts ←
flutter:          │   DefaultTextEditingShortcuts ← Semantics ← _FocusInheritedScope
flutter:          │   ← Focus ← ⋯
flutter:          │ parentData: <none> (can use size)
flutter:          │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:          │ size: Size(800.0, 600.0)
flutter:          │
flutter:          └─child: RenderTapRegionSurface#ff857
flutter:            │ needs compositing
flutter:            │ creator: TapRegionSurface ← _FocusInheritedScope ← Focus ←
flutter:            │   FocusTraversalGroup ← _ActionsScope ← Actions ← Semantics ←
flutter:            │   _FocusInheritedScope ← Focus ← Shortcuts ← Semantics ←
flutter:            │   _FocusInheritedScope ← ⋯
flutter:            │ parentData: <none> (can use size)
flutter:            │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:            │ size: Size(800.0, 600.0)
flutter:            │ behavior: deferToChild
flutter:            │
flutter:            └─child: RenderSemanticsAnnotations#fe316
flutter:              │ needs compositing
flutter:              │ creator: Semantics ← _FocusInheritedScope ← Focus ← Shortcuts ←
flutter:              │   _ShortcutRegistrarScope ← ShortcutRegistrar ← TapRegionSurface
flutter:              │   ← _FocusInheritedScope ← Focus ← FocusTraversalGroup ←
flutter:              │   _ActionsScope ← Actions ← ⋯
flutter:              │ parentData: <none> (can use size)
flutter:              │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:              │ size: Size(800.0, 600.0)
flutter:              │
flutter:              └─child: RenderSemanticsAnnotations#fa55c
flutter:                │ needs compositing
flutter:                │ creator: Semantics ← Localizations ← Semantics ←
flutter:                │   _FocusInheritedScope ← Focus ← Shortcuts ←
flutter:                │   _ShortcutRegistrarScope ← ShortcutRegistrar ← TapRegionSurface
flutter:                │   ← _FocusInheritedScope ← Focus ← FocusTraversalGroup ← ⋯
flutter:                │ parentData: <none> (can use size)
flutter:                │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                │ size: Size(800.0, 600.0)
flutter:                │
flutter:                └─child: RenderCustomPaint#4b256
flutter:                  │ needs compositing
flutter:                  │ creator: CustomPaint ← Banner ← CheckedModeBanner ← Title ←
flutter:                  │   Directionality ← _LocalizationsScope-[GlobalKey#4a3aa] ←
flutter:                  │   Semantics ← Localizations ← Semantics ← _FocusInheritedScope ←
flutter:                  │   Focus ← Shortcuts ← ⋯
flutter:                  │ parentData: <none> (can use size)
flutter:                  │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                  │ size: Size(800.0, 600.0)
flutter:                  │ painter: null
flutter:                  │ foregroundPainter: BannerPainter#1bfd7(Instance of
flutter:                  │   '_SystemFontsNotifier')
flutter:                  │
flutter:                  └─child: RenderSemanticsAnnotations#f470f
flutter:                    │ needs compositing
flutter:                    │ creator: Semantics ← FocusScope ← DefaultSelectionStyle ←
flutter:                    │   IconTheme ← IconTheme ← _InheritedCupertinoTheme ←
flutter:                    │   CupertinoTheme ← _InheritedTheme ← Theme ← AnimatedTheme ←
flutter:                    │   DefaultSelectionStyle ← _ScaffoldMessengerScope ← ⋯
flutter:                    │ parentData: <none> (can use size)
flutter:                    │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                    │ size: Size(800.0, 600.0)
flutter:                    │
flutter:                    └─child: RenderPointerListener#f59c8
flutter:                      │ needs compositing
flutter:                      │ creator: Listener ← HeroControllerScope ←
flutter:                      │   Navigator-[GlobalObjectKey<NavigatorState>
flutter:                      │   _WidgetsAppState#0d73a] ← _FocusInheritedScope ← Semantics ←
flutter:                      │   FocusScope ← DefaultSelectionStyle ← IconTheme ← IconTheme ←
flutter:                      │   _InheritedCupertinoTheme ← CupertinoTheme ← _InheritedTheme ← ⋯
flutter:                      │ parentData: <none> (can use size)
flutter:                      │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                      │ size: Size(800.0, 600.0)
flutter:                      │ behavior: deferToChild
flutter:                      │ listeners: down, up, cancel
flutter:                      │
flutter:                      └─child: RenderAbsorbPointer#c91bd
flutter:                        │ needs compositing
flutter:                        │ creator: AbsorbPointer ← Listener ← HeroControllerScope ←
flutter:                        │   Navigator-[GlobalObjectKey<NavigatorState>
flutter:                        │   _WidgetsAppState#0d73a] ← _FocusInheritedScope ← Semantics ←
flutter:                        │   FocusScope ← DefaultSelectionStyle ← IconTheme ← IconTheme ←
flutter:                        │   _InheritedCupertinoTheme ← CupertinoTheme ← ⋯
flutter:                        │ parentData: <none> (can use size)
flutter:                        │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                        │ size: Size(800.0, 600.0)
flutter:                        │ absorbing: false
flutter:                        │ ignoringSemantics: null
flutter:                        │
flutter:                        └─child: _RenderTheater#07897
flutter:                          │ needs compositing
flutter:                          │ creator: _Theater ←
flutter:                          │   Overlay-[LabeledGlobalKey<OverlayState>#49a93] ←
flutter:                          │   UnmanagedRestorationScope ← _FocusInheritedScope ← Focus ←
flutter:                          │   _FocusInheritedScope ← Focus ← FocusTraversalGroup ←
flutter:                          │   AbsorbPointer ← Listener ← HeroControllerScope ←
flutter:                          │   Navigator-[GlobalObjectKey<NavigatorState>
flutter:                          │   _WidgetsAppState#0d73a] ← ⋯
flutter:                          │ parentData: <none> (can use size)
flutter:                          │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │ size: Size(800.0, 600.0)
flutter:                          │ skipCount: 0
flutter:                          │ textDirection: ltr
flutter:                          │
flutter:                          ├─onstage 1: RenderIgnorePointer#3b659
flutter:                          │ │ creator: IgnorePointer ← _RenderTheaterMarker ←
flutter:                          │ │   _EffectiveTickerMode ← TickerMode ←
flutter:                          │ │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#a47f4]
flutter:                          │ │   ← _Theater ← Overlay-[LabeledGlobalKey<OverlayState>#49a93] ←
flutter:                          │ │   UnmanagedRestorationScope ← _FocusInheritedScope ← Focus ←
flutter:                          │ │   _FocusInheritedScope ← Focus ← ⋯
flutter:                          │ │ parentData: not positioned; offset=Offset(0.0, 0.0) (can use
flutter:                          │ │   size)
flutter:                          │ │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │ │ size: Size(800.0, 600.0)
flutter:                          │ │ ignoring: false
flutter:                          │ │ ignoringSemantics: null
flutter:                          │ │
flutter:                          │ └─child: RenderBlockSemantics#7586c
flutter:                          │   │ creator: BlockSemantics ← ModalBarrier ← IgnorePointer ←
flutter:                          │   │   _RenderTheaterMarker ← _EffectiveTickerMode ← TickerMode ←
flutter:                          │   │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#a47f4]
flutter:                          │   │   ← _Theater ← Overlay-[LabeledGlobalKey<OverlayState>#49a93] ←
flutter:                          │   │   UnmanagedRestorationScope ← _FocusInheritedScope ← Focus ← ⋯
flutter:                          │   │ parentData: <none> (can use size)
flutter:                          │   │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │   │ blocks semantics of earlier render objects below the common
flutter:                          │   │ boundary
flutter:                          │   │ size: Size(800.0, 600.0)
flutter:                          │   │ blocking: true
flutter:                          │   │
flutter:                          │   └─child: RenderExcludeSemantics#c1d3f
flutter:                          │     │ creator: ExcludeSemantics ← BlockSemantics ← ModalBarrier ←
flutter:                          │     │   IgnorePointer ← _RenderTheaterMarker ← _EffectiveTickerMode ←
flutter:                          │     │   TickerMode ←
flutter:                          │     │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#a47f4]
flutter:                          │     │   ← _Theater ← Overlay-[LabeledGlobalKey<OverlayState>#49a93] ←
flutter:                          │     │   UnmanagedRestorationScope ← _FocusInheritedScope ← ⋯
flutter:                          │     │ parentData: <none> (can use size)
flutter:                          │     │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │     │ size: Size(800.0, 600.0)
flutter:                          │     │ excluding: true
flutter:                          │     │
flutter:                          │     └─child: RenderSemanticsGestureHandler#70b16
flutter:                          │       │ creator: _GestureSemantics ← RawGestureDetector ←
flutter:                          │       │   _ModalBarrierGestureDetector ← ExcludeSemantics ←
flutter:                          │       │   BlockSemantics ← ModalBarrier ← IgnorePointer ←
flutter:                          │       │   _RenderTheaterMarker ← _EffectiveTickerMode ← TickerMode ←
flutter:                          │       │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#a47f4]
flutter:                          │       │   ← _Theater ← ⋯
flutter:                          │       │ parentData: <none> (can use size)
flutter:                          │       │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │       │ size: Size(800.0, 600.0)
flutter:                          │       │ behavior: opaque
flutter:                          │       │ gestures: <none>
flutter:                          │       │
flutter:                          │       └─child: RenderPointerListener#1f34a
flutter:                          │         │ creator: Listener ← _GestureSemantics ← RawGestureDetector ←
flutter:                          │         │   _ModalBarrierGestureDetector ← ExcludeSemantics ←
flutter:                          │         │   BlockSemantics ← ModalBarrier ← IgnorePointer ←
flutter:                          │         │   _RenderTheaterMarker ← _EffectiveTickerMode ← TickerMode ←
flutter:                          │         │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#a47f4]
flutter:                          │         │   ← ⋯
flutter:                          │         │ parentData: <none> (can use size)
flutter:                          │         │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │         │ size: Size(800.0, 600.0)
flutter:                          │         │ behavior: opaque
flutter:                          │         │ listeners: down, panZoomStart
flutter:                          │         │
flutter:                          │         └─child: RenderSemanticsAnnotations#73467
flutter:                          │           │ creator: Semantics ← Listener ← _GestureSemantics ←
flutter:                          │           │   RawGestureDetector ← _ModalBarrierGestureDetector ←
flutter:                          │           │   ExcludeSemantics ← BlockSemantics ← ModalBarrier ←
flutter:                          │           │   IgnorePointer ← _RenderTheaterMarker ← _EffectiveTickerMode ←
flutter:                          │           │   TickerMode ← ⋯
flutter:                          │           │ parentData: <none> (can use size)
flutter:                          │           │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │           │ size: Size(800.0, 600.0)
flutter:                          │           │
flutter:                          │           └─child: RenderMouseRegion#560dc
flutter:                          │             │ creator: MouseRegion ← Semantics ← Listener ← _GestureSemantics ←
flutter:                          │             │   RawGestureDetector ← _ModalBarrierGestureDetector ←
flutter:                          │             │   ExcludeSemantics ← BlockSemantics ← ModalBarrier ←
flutter:                          │             │   IgnorePointer ← _RenderTheaterMarker ← _EffectiveTickerMode ← ⋯
flutter:                          │             │ parentData: <none> (can use size)
flutter:                          │             │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │             │ size: Size(800.0, 600.0)
flutter:                          │             │ behavior: opaque
flutter:                          │             │ listeners: <none>
flutter:                          │             │ cursor: SystemMouseCursor(basic)
flutter:                          │             │
flutter:                          │             └─child: RenderConstrainedBox#01e8c
flutter:                          │                 creator: ConstrainedBox ← MouseRegion ← Semantics ← Listener ←
flutter:                          │                   _GestureSemantics ← RawGestureDetector ←
flutter:                          │                   _ModalBarrierGestureDetector ← ExcludeSemantics ←
flutter:                          │                   BlockSemantics ← ModalBarrier ← IgnorePointer ←
flutter:                          │                   _RenderTheaterMarker ← ⋯
flutter:                          │                 parentData: <none> (can use size)
flutter:                          │                 constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          │                 size: Size(800.0, 600.0)
flutter:                          │                 additionalConstraints: BoxConstraints(biggest)
flutter:                          │
flutter:                          ├─onstage 2: RenderSemanticsAnnotations#8187b
flutter:                          ╎ │ needs compositing
flutter:                          ╎ │ creator: Semantics ← _RenderTheaterMarker ← _EffectiveTickerMode
flutter:                          ╎ │   ← TickerMode ←
flutter:                          ╎ │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#8cd54]
flutter:                          ╎ │   ← _Theater ← Overlay-[LabeledGlobalKey<OverlayState>#49a93] ←
flutter:                          ╎ │   UnmanagedRestorationScope ← _FocusInheritedScope ← Focus ←
flutter:                          ╎ │   _FocusInheritedScope ← Focus ← ⋯
flutter:                          ╎ │ parentData: not positioned; offset=Offset(0.0, 0.0) (can use
flutter:                          ╎ │   size)
flutter:                          ╎ │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎ │ size: Size(800.0, 600.0)
flutter:                          ╎ │
flutter:                          ╎ └─child: RenderOffstage#f211d
flutter:                          ╎   │ needs compositing
flutter:                          ╎   │ creator: Offstage ← _ModalScopeStatus ← UnmanagedRestorationScope
flutter:                          ╎   │   ← RestorationScope ← AnimatedBuilder ←
flutter:                          ╎   │   _ModalScope<dynamic>-[LabeledGlobalKey<_ModalScopeState<dynamic>>#db401]
flutter:                          ╎   │   ← Semantics ← _RenderTheaterMarker ← _EffectiveTickerMode ←
flutter:                          ╎   │   TickerMode ←
flutter:                          ╎   │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#8cd54]
flutter:                          ╎   │   ← _Theater ← ⋯
flutter:                          ╎   │ parentData: <none> (can use size)
flutter:                          ╎   │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎   │ size: Size(800.0, 600.0)
flutter:                          ╎   │ offstage: false
flutter:                          ╎   │
flutter:                          ╎   └─child: RenderSemanticsAnnotations#9436c
flutter:                          ╎     │ needs compositing
flutter:                          ╎     │ creator: Semantics ← FocusScope ← PrimaryScrollController ←
flutter:                          ╎     │   _ActionsScope ← Actions ← Builder ← PageStorage ← Offstage ←
flutter:                          ╎     │   _ModalScopeStatus ← UnmanagedRestorationScope ←
flutter:                          ╎     │   RestorationScope ← AnimatedBuilder ← ⋯
flutter:                          ╎     │ parentData: <none> (can use size)
flutter:                          ╎     │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎     │ size: Size(800.0, 600.0)
flutter:                          ╎     │
flutter:                          ╎     └─child: RenderRepaintBoundary#f8f28
flutter:                          ╎       │ needs compositing
flutter:                          ╎       │ creator: RepaintBoundary ← _FocusInheritedScope ← Semantics ←
flutter:                          ╎       │   FocusScope ← PrimaryScrollController ← _ActionsScope ← Actions
flutter:                          ╎       │   ← Builder ← PageStorage ← Offstage ← _ModalScopeStatus ←
flutter:                          ╎       │   UnmanagedRestorationScope ← ⋯
flutter:                          ╎       │ parentData: <none> (can use size)
flutter:                          ╎       │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎       │ layer: OffsetLayer#e73b7
flutter:                          ╎       │ size: Size(800.0, 600.0)
flutter:                          ╎       │ metrics: 66.7% useful (1 bad vs 2 good)
flutter:                          ╎       │ diagnosis: insufficient data to draw conclusion (less than five
flutter:                          ╎       │   repaints)
flutter:                          ╎       │
flutter:                          ╎       └─child: RenderFractionalTranslation#c3a54
flutter:                          ╎         │ needs compositing
flutter:                          ╎         │ creator: FractionalTranslation ← SlideTransition ←
flutter:                          ╎         │   CupertinoPageTransition ← AnimatedBuilder ← RepaintBoundary ←
flutter:                          ╎         │   _FocusInheritedScope ← Semantics ← FocusScope ←
flutter:                          ╎         │   PrimaryScrollController ← _ActionsScope ← Actions ← Builder ← ⋯
flutter:                          ╎         │ parentData: <none> (can use size)
flutter:                          ╎         │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎         │ size: Size(800.0, 600.0)
flutter:                          ╎         │ translation: Offset(0.0, 0.0)
flutter:                          ╎         │ transformHitTests: false
flutter:                          ╎         │
flutter:                          ╎         └─child: RenderFractionalTranslation#7fcf2
flutter:                          ╎           │ needs compositing
flutter:                          ╎           │ creator: FractionalTranslation ← SlideTransition ←
flutter:                          ╎           │   FractionalTranslation ← SlideTransition ←
flutter:                          ╎           │   CupertinoPageTransition ← AnimatedBuilder ← RepaintBoundary ←
flutter:                          ╎           │   _FocusInheritedScope ← Semantics ← FocusScope ←
flutter:                          ╎           │   PrimaryScrollController ← _ActionsScope ← ⋯
flutter:                          ╎           │ parentData: <none> (can use size)
flutter:                          ╎           │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎           │ size: Size(800.0, 600.0)
flutter:                          ╎           │ translation: Offset(0.0, 0.0)
flutter:                          ╎           │ transformHitTests: true
flutter:                          ╎           │
flutter:                          ╎           └─child: RenderDecoratedBox#713ec
flutter:                          ╎             │ needs compositing
flutter:                          ╎             │ creator: DecoratedBox ← DecoratedBoxTransition ←
flutter:                          ╎             │   FractionalTranslation ← SlideTransition ← FractionalTranslation
flutter:                          ╎             │   ← SlideTransition ← CupertinoPageTransition ← AnimatedBuilder ←
flutter:                          ╎             │   RepaintBoundary ← _FocusInheritedScope ← Semantics ← FocusScope
flutter:                          ╎             │   ← ⋯
flutter:                          ╎             │ parentData: <none> (can use size)
flutter:                          ╎             │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎             │ size: Size(800.0, 600.0)
flutter:                          ╎             │ ├─decoration: _CupertinoEdgeShadowDecoration
flutter:                          ╎             │     colors: Color(0x04000000), Color(0x00000000)
flutter:                          ╎             │
flutter:                          ╎             │ configuration: ImageConfiguration(bundle:
flutter:                          ╎             │   PlatformAssetBundle#164ca(), devicePixelRatio: 1.0, locale:
flutter:                          ╎             │   en_US, textDirection: TextDirection.ltr, platform: macOS)
flutter:                          ╎             │
flutter:                          ╎             └─child: RenderStack#83b13
flutter:                          ╎               │ needs compositing
flutter:                          ╎               │ creator: Stack ← _CupertinoBackGestureDetector<dynamic> ←
flutter:                          ╎               │   DecoratedBox ← DecoratedBoxTransition ← FractionalTranslation ←
flutter:                          ╎               │   SlideTransition ← FractionalTranslation ← SlideTransition ←
flutter:                          ╎               │   CupertinoPageTransition ← AnimatedBuilder ← RepaintBoundary ←
flutter:                          ╎               │   _FocusInheritedScope ← ⋯
flutter:                          ╎               │ parentData: <none> (can use size)
flutter:                          ╎               │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎               │ size: Size(800.0, 600.0)
flutter:                          ╎               │ alignment: AlignmentDirectional.topStart
flutter:                          ╎               │ textDirection: ltr
flutter:                          ╎               │ fit: passthrough
flutter:                          ╎               │
flutter:                          ╎               ├─child 1: RenderIgnorePointer#ad50f
flutter:                          ╎               │ │ needs compositing
flutter:                          ╎               │ │ creator: IgnorePointer ← AnimatedBuilder ← Stack ←
flutter:                          ╎               │ │   _CupertinoBackGestureDetector<dynamic> ← DecoratedBox ←
flutter:                          ╎               │ │   DecoratedBoxTransition ← FractionalTranslation ←
flutter:                          ╎               │ │   SlideTransition ← FractionalTranslation ← SlideTransition ←
flutter:                          ╎               │ │   CupertinoPageTransition ← AnimatedBuilder ← ⋯
flutter:                          ╎               │ │ parentData: not positioned; offset=Offset(0.0, 0.0) (can use
flutter:                          ╎               │ │   size)
flutter:                          ╎               │ │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎               │ │ size: Size(800.0, 600.0)
flutter:                          ╎               │ │ ignoring: false
flutter:                          ╎               │ │ ignoringSemantics: null
flutter:                          ╎               │ │
flutter:                          ╎               │ └─child: RenderRepaintBoundary#29754
flutter:                          ╎               │   │ needs compositing
flutter:                          ╎               │   │ creator: RepaintBoundary-[GlobalKey#75409] ← IgnorePointer ←
flutter:                          ╎               │   │   AnimatedBuilder ← Stack ←
flutter:                          ╎               │   │   _CupertinoBackGestureDetector<dynamic> ← DecoratedBox ←
flutter:                          ╎               │   │   DecoratedBoxTransition ← FractionalTranslation ←
flutter:                          ╎               │   │   SlideTransition ← FractionalTranslation ← SlideTransition ←
flutter:                          ╎               │   │   CupertinoPageTransition ← ⋯
flutter:                          ╎               │   │ parentData: <none> (can use size)
flutter:                          ╎               │   │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎               │   │ layer: OffsetLayer#fa835
flutter:                          ╎               │   │ size: Size(800.0, 600.0)
flutter:                          ╎               │   │ metrics: 90.9% useful (1 bad vs 10 good)
flutter:                          ╎               │   │ diagnosis: this is an outstandingly useful repaint boundary and
flutter:                          ╎               │   │   should definitely be kept
flutter:                          ╎               │   │
flutter:                          ╎               │   └─child: RenderSemanticsAnnotations#95566
flutter:                          ╎               │     │ creator: Semantics ← Builder ← RepaintBoundary-[GlobalKey#75409]
flutter:                          ╎               │     │   ← IgnorePointer ← AnimatedBuilder ← Stack ←
flutter:                          ╎               │     │   _CupertinoBackGestureDetector<dynamic> ← DecoratedBox ←
flutter:                          ╎               │     │   DecoratedBoxTransition ← FractionalTranslation ←
flutter:                          ╎               │     │   SlideTransition ← FractionalTranslation ← ⋯
flutter:                          ╎               │     │ parentData: <none> (can use size)
flutter:                          ╎               │     │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎               │     │ size: Size(800.0, 600.0)
flutter:                          ╎               │     │
flutter:                          ╎               │     └─child: RenderPhysicalModel#bc9d7
flutter:                          ╎               │       │ creator: PhysicalModel ← AnimatedPhysicalModel ← Material ←
flutter:                          ╎               │       │   AppHome ← Semantics ← Builder ←
flutter:                          ╎               │       │   RepaintBoundary-[GlobalKey#75409] ← IgnorePointer ←
flutter:                          ╎               │       │   AnimatedBuilder ← Stack ←
flutter:                          ╎               │       │   _CupertinoBackGestureDetector<dynamic> ← DecoratedBox ← ⋯
flutter:                          ╎               │       │ parentData: <none> (can use size)
flutter:                          ╎               │       │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎               │       │ size: Size(800.0, 600.0)
flutter:                          ╎               │       │ elevation: 0.0
flutter:                          ╎               │       │ color: Color(0xfffafafa)
flutter:                          ╎               │       │ shadowColor: Color(0xfffafafa)
flutter:                          ╎               │       │ shape: BoxShape.rectangle
flutter:                          ╎               │       │ borderRadius: BorderRadius.zero
flutter:                          ╎               │       │
flutter:                          ╎               │       └─child: _RenderInkFeatures#ac819
flutter:                          ╎               │         │ creator: _InkFeatures-[GlobalKey#d721e ink renderer] ←
flutter:                          ╎               │         │   NotificationListener<LayoutChangedNotification> ← PhysicalModel
flutter:                          ╎               │         │   ← AnimatedPhysicalModel ← Material ← AppHome ← Semantics ←
flutter:                          ╎               │         │   Builder ← RepaintBoundary-[GlobalKey#75409] ← IgnorePointer ←
flutter:                          ╎               │         │   AnimatedBuilder ← Stack ← ⋯
flutter:                          ╎               │         │ parentData: <none> (can use size)
flutter:                          ╎               │         │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎               │         │ size: Size(800.0, 600.0)
flutter:                          ╎               │         │
flutter:                          ╎               │         └─child: RenderPositionedBox#dc1df
flutter:                          ╎               │           │ creator: Center ← DefaultTextStyle ← AnimatedDefaultTextStyle ←
flutter:                          ╎               │           │   _InkFeatures-[GlobalKey#d721e ink renderer] ←
flutter:                          ╎               │           │   NotificationListener<LayoutChangedNotification> ← PhysicalModel
flutter:                          ╎               │           │   ← AnimatedPhysicalModel ← Material ← AppHome ← Semantics ←
flutter:                          ╎               │           │   Builder ← RepaintBoundary-[GlobalKey#75409] ← ⋯
flutter:                          ╎               │           │ parentData: <none> (can use size)
flutter:                          ╎               │           │ constraints: BoxConstraints(w=800.0, h=600.0)
flutter:                          ╎               │           │ size: Size(800.0, 600.0)
flutter:                          ╎               │           │ alignment: Alignment.center
flutter:                          ╎               │           │ textDirection: ltr
flutter:                          ╎               │           │ widthFactor: expand
flutter:                          ╎               │           │ heightFactor: expand
flutter:                          ╎               │           │
flutter:                          ╎               │           └─child: RenderSemanticsAnnotations#a0a4b relayoutBoundary=up1
flutter:                          ╎               │             │ creator: Semantics ← TextButton ← Center ← DefaultTextStyle ←
flutter:                          ╎               │             │   AnimatedDefaultTextStyle ← _InkFeatures-[GlobalKey#d721e ink
flutter:                          ╎               │             │   renderer] ← NotificationListener<LayoutChangedNotification> ←
flutter:                          ╎               │             │   PhysicalModel ← AnimatedPhysicalModel ← Material ← AppHome ←
flutter:                          ╎               │             │   Semantics ← ⋯
flutter:                          ╎               │             │ parentData: offset=Offset(329.0, 286.0) (can use size)
flutter:                          ╎               │             │ constraints: BoxConstraints(0.0<=w<=800.0, 0.0<=h<=600.0)
flutter:                          ╎               │             │ semantic boundary
flutter:                          ╎               │             │ size: Size(142.0, 28.0)
flutter:                          ╎               │             │
flutter:                          ╎               │             └─child: _RenderInputPadding#4672f relayoutBoundary=up2
flutter:                          ╎               │               │ creator: _InputPadding ← Semantics ← TextButton ← Center ←
flutter:                          ╎               │               │   DefaultTextStyle ← AnimatedDefaultTextStyle ←
flutter:                          ╎               │               │   _InkFeatures-[GlobalKey#d721e ink renderer] ←
flutter:                          ╎               │               │   NotificationListener<LayoutChangedNotification> ← PhysicalModel
flutter:                          ╎               │               │   ← AnimatedPhysicalModel ← Material ← AppHome ← ⋯
flutter:                          ╎               │               │ parentData: <none> (can use size)
flutter:                          ╎               │               │ constraints: BoxConstraints(0.0<=w<=800.0, 0.0<=h<=600.0)
flutter:                          ╎               │               │ size: Size(142.0, 28.0)
flutter:                          ╎               │               │
flutter:                          ╎               │               └─child: RenderConstrainedBox#425d6 relayoutBoundary=up3
flutter:                          ╎               │                 │ creator: ConstrainedBox ← _InputPadding ← Semantics ← TextButton
flutter:                          ╎               │                 │   ← Center ← DefaultTextStyle ← AnimatedDefaultTextStyle ←
flutter:                          ╎               │                 │   _InkFeatures-[GlobalKey#d721e ink renderer] ←
flutter:                          ╎               │                 │   NotificationListener<LayoutChangedNotification> ← PhysicalModel
flutter:                          ╎               │                 │   ← AnimatedPhysicalModel ← Material ← ⋯
flutter:                          ╎               │                 │ parentData: offset=Offset(0.0, 0.0) (can use size)
flutter:                          ╎               │                 │ constraints: BoxConstraints(0.0<=w<=800.0, 0.0<=h<=600.0)
flutter:                          ╎               │                 │ size: Size(142.0, 28.0)
flutter:                          ╎               │                 │ additionalConstraints: BoxConstraints(56.0<=w<=Infinity,
flutter:                          ╎               │                 │   28.0<=h<=Infinity)
flutter:                          ╎               │                 │
flutter:                          ╎               │                 └─child: RenderPhysicalShape#8e171 relayoutBoundary=up4
flutter:                          ╎               │                   │ creator: PhysicalShape ← _MaterialInterior ← Material ←
flutter:                          ╎               │                   │   ConstrainedBox ← _InputPadding ← Semantics ← TextButton ←
flutter:                          ╎               │                   │   Center ← DefaultTextStyle ← AnimatedDefaultTextStyle ←
flutter:                          ╎               │                   │   _InkFeatures-[GlobalKey#d721e ink renderer] ←
flutter:                          ╎               │                   │   NotificationListener<LayoutChangedNotification> ← ⋯
flutter:                          ╎               │                   │ parentData: <none> (can use size)
flutter:                          ╎               │                   │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                   │ size: Size(142.0, 28.0)
flutter:                          ╎               │                   │ elevation: 0.0
flutter:                          ╎               │                   │ color: Color(0x00000000)
flutter:                          ╎               │                   │ shadowColor: Color(0x00000000)
flutter:                          ╎               │                   │ clipper: ShapeBorderClipper
flutter:                          ╎               │                   │
flutter:                          ╎               │                   └─child: RenderCustomPaint#eea46 relayoutBoundary=up5
flutter:                          ╎               │                     │ creator: CustomPaint ← _ShapeBorderPaint ← PhysicalShape ←
flutter:                          ╎               │                     │   _MaterialInterior ← Material ← ConstrainedBox ← _InputPadding ←
flutter:                          ╎               │                     │   Semantics ← TextButton ← Center ← DefaultTextStyle ←
flutter:                          ╎               │                     │   AnimatedDefaultTextStyle ← ⋯
flutter:                          ╎               │                     │ parentData: <none> (can use size)
flutter:                          ╎               │                     │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                     │ size: Size(142.0, 28.0)
flutter:                          ╎               │                     │ painter: null
flutter:                          ╎               │                     │ foregroundPainter: _ShapeBorderPainter#ac724()
flutter:                          ╎               │                     │
flutter:                          ╎               │                     └─child: _RenderInkFeatures#b19a7 relayoutBoundary=up6
flutter:                          ╎               │                       │ creator: _InkFeatures-[GlobalKey#87971 ink renderer] ←
flutter:                          ╎               │                       │   NotificationListener<LayoutChangedNotification> ← CustomPaint ←
flutter:                          ╎               │                       │   _ShapeBorderPaint ← PhysicalShape ← _MaterialInterior ←
flutter:                          ╎               │                       │   Material ← ConstrainedBox ← _InputPadding ← Semantics ←
flutter:                          ╎               │                       │   TextButton ← Center ← ⋯
flutter:                          ╎               │                       │ parentData: <none> (can use size)
flutter:                          ╎               │                       │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                       │ size: Size(142.0, 28.0)
flutter:                          ╎               │                       │
flutter:                          ╎               │                       └─child: RenderSemanticsAnnotations#4d1b3 relayoutBoundary=up7
flutter:                          ╎               │                         │ creator: Semantics ← _FocusInheritedScope ← Focus ← _ActionsScope
flutter:                          ╎               │                         │   ← Actions ← _ParentInkResponseProvider ←
flutter:                          ╎               │                         │   _InkResponseStateWidget ← InkWell ← DefaultTextStyle ←
flutter:                          ╎               │                         │   AnimatedDefaultTextStyle ← _InkFeatures-[GlobalKey#87971 ink
flutter:                          ╎               │                         │   renderer] ← NotificationListener<LayoutChangedNotification> ← ⋯
flutter:                          ╎               │                         │ parentData: <none> (can use size)
flutter:                          ╎               │                         │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                         │ size: Size(142.0, 28.0)
flutter:                          ╎               │                         │
flutter:                          ╎               │                         └─child: RenderMouseRegion#e5b3f relayoutBoundary=up8
flutter:                          ╎               │                           │ creator: MouseRegion ← Semantics ← _FocusInheritedScope ← Focus ←
flutter:                          ╎               │                           │   _ActionsScope ← Actions ← _ParentInkResponseProvider ←
flutter:                          ╎               │                           │   _InkResponseStateWidget ← InkWell ← DefaultTextStyle ←
flutter:                          ╎               │                           │   AnimatedDefaultTextStyle ← _InkFeatures-[GlobalKey#87971 ink
flutter:                          ╎               │                           │   renderer] ← ⋯
flutter:                          ╎               │                           │ parentData: <none> (can use size)
flutter:                          ╎               │                           │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                           │ size: Size(142.0, 28.0)
flutter:                          ╎               │                           │ behavior: opaque
flutter:                          ╎               │                           │ listeners: enter, exit
flutter:                          ╎               │                           │ cursor: SystemMouseCursor(click)
flutter:                          ╎               │                           │
flutter:                          ╎               │                           └─child: RenderSemanticsAnnotations#deb9b relayoutBoundary=up9
flutter:                          ╎               │                             │ creator: Semantics ← DefaultSelectionStyle ← Builder ←
flutter:                          ╎               │                             │   MouseRegion ← Semantics ← _FocusInheritedScope ← Focus ←
flutter:                          ╎               │                             │   _ActionsScope ← Actions ← _ParentInkResponseProvider ←
flutter:                          ╎               │                             │   _InkResponseStateWidget ← InkWell ← ⋯
flutter:                          ╎               │                             │ parentData: <none> (can use size)
flutter:                          ╎               │                             │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                             │ size: Size(142.0, 28.0)
flutter:                          ╎               │                             │
flutter:                          ╎               │                             └─child: RenderPointerListener#2017a relayoutBoundary=up10
flutter:                          ╎               │                               │ creator: Listener ← RawGestureDetector ← GestureDetector ←
flutter:                          ╎               │                               │   Semantics ← DefaultSelectionStyle ← Builder ← MouseRegion ←
flutter:                          ╎               │                               │   Semantics ← _FocusInheritedScope ← Focus ← _ActionsScope ←
flutter:                          ╎               │                               │   Actions ← ⋯
flutter:                          ╎               │                               │ parentData: <none> (can use size)
flutter:                          ╎               │                               │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                               │ size: Size(142.0, 28.0)
flutter:                          ╎               │                               │ behavior: opaque
flutter:                          ╎               │                               │ listeners: down, panZoomStart
flutter:                          ╎               │                               │
flutter:                          ╎               │                               └─child: RenderPadding#8455f relayoutBoundary=up11
flutter:                          ╎               │                                 │ creator: Padding ← IconTheme ← Builder ← Listener ←
flutter:                          ╎               │                                 │   RawGestureDetector ← GestureDetector ← Semantics ←
flutter:                          ╎               │                                 │   DefaultSelectionStyle ← Builder ← MouseRegion ← Semantics ←
flutter:                          ╎               │                                 │   _FocusInheritedScope ← ⋯
flutter:                          ╎               │                                 │ parentData: <none> (can use size)
flutter:                          ╎               │                                 │ constraints: BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0)
flutter:                          ╎               │                                 │ size: Size(142.0, 28.0)
flutter:                          ╎               │                                 │ padding: EdgeInsets(8.0, 0.0, 8.0, 0.0)
flutter:                          ╎               │                                 │ textDirection: ltr
flutter:                          ╎               │                                 │
flutter:                          ╎               │                                 └─child: RenderPositionedBox#80b8d relayoutBoundary=up12
flutter:                          ╎               │                                   │ creator: Align ← Padding ← IconTheme ← Builder ← Listener ←
flutter:                          ╎               │                                   │   RawGestureDetector ← GestureDetector ← Semantics ←
flutter:                          ╎               │                                   │   DefaultSelectionStyle ← Builder ← MouseRegion ← Semantics ← ⋯
flutter:                          ╎               │                                   │ parentData: offset=Offset(8.0, 0.0) (can use size)
flutter:                          ╎               │                                   │ constraints: BoxConstraints(40.0<=w<=784.0, 28.0<=h<=600.0)
flutter:                          ╎               │                                   │ size: Size(126.0, 28.0)
flutter:                          ╎               │                                   │ alignment: Alignment.center
flutter:                          ╎               │                                   │ textDirection: ltr
flutter:                          ╎               │                                   │ widthFactor: 1.0
flutter:                          ╎               │                                   │ heightFactor: 1.0
flutter:                          ╎               │                                   │
flutter:                          ╎               │                                   └─child: RenderParagraph#59bc2 relayoutBoundary=up13
flutter:                          ╎               │                                     │ creator: RichText ← Text ← Align ← Padding ← IconTheme ← Builder
flutter:                          ╎               │                                     │   ← Listener ← RawGestureDetector ← GestureDetector ← Semantics ←
flutter:                          ╎               │                                     │   DefaultSelectionStyle ← Builder ← ⋯
flutter:                          ╎               │                                     │ parentData: offset=Offset(0.0, 6.0) (can use size)
flutter:                          ╎               │                                     │ constraints: BoxConstraints(0.0<=w<=784.0, 0.0<=h<=600.0)
flutter:                          ╎               │                                     │ size: Size(126.0, 16.0)
flutter:                          ╎               │                                     │ textAlign: start
flutter:                          ╎               │                                     │ textDirection: ltr
flutter:                          ╎               │                                     │ softWrap: wrapping at box width
flutter:                          ╎               │                                     │ overflow: clip
flutter:                          ╎               │                                     │ locale: en_US
flutter:                          ╎               │                                     │ maxLines: unlimited
flutter:                          ╎               │                                     ╘═╦══ text ═══
flutter:                          ╎               │                                       ║ TextSpan:
flutter:                          ╎               │                                       ║   debugLabel: ((englishLike labelLarge 2014).merge(blackRedwoodCity
flutter:                          ╎               │                                       ║     labelLarge)).copyWith
flutter:                          ╎               │                                       ║   inherit: false
flutter:                          ╎               │                                       ║   color: MaterialColor(primary value: Color(0xff2196f3))
flutter:                          ╎               │                                       ║   family: .AppleSystemUIFont
flutter:                          ╎               │                                       ║   size: 14.0
flutter:                          ╎               │                                       ║   weight: 500
flutter:                          ╎               │                                       ║   baseline: alphabetic
flutter:                          ╎               │                                       ║   decoration: TextDecoration.none
flutter:                          ╎               │                                       ║   "Dump Render Tree"
flutter:                          ╎               │                                       ╚═══════════
flutter:                          ╎               └─child 2: RenderPointerListener#db4b5
flutter:                          ╎                   creator: Listener ← Positioned ← PositionedDirectional ← Stack ←
flutter:                          ╎                     _CupertinoBackGestureDetector<dynamic> ← DecoratedBox ←
flutter:                          ╎                     DecoratedBoxTransition ← FractionalTranslation ←
flutter:                          ╎                     SlideTransition ← FractionalTranslation ← SlideTransition ←
flutter:                          ╎                     CupertinoPageTransition ← ⋯
flutter:                          ╎                   parentData: top=0.0; bottom=0.0; left=0.0; width=20.0;
flutter:                          ╎                     offset=Offset(0.0, 0.0) (can use size)
flutter:                          ╎                   constraints: BoxConstraints(w=20.0, h=600.0)
flutter:                          ╎                   size: Size(20.0, 600.0)
flutter:                          ╎                   behavior: translucent
flutter:                          ╎                   listeners: down
flutter:                          ╎
flutter:                          └╌no offstage children
flutter:`
In the render tree for**Example 5**:


The`RenderView`, or window size, limits all render objects up to and
                      including[RenderPositionedBox](https://api.flutter.dev/flutter/rendering/RenderPositionedBox-class.html)`#dc1df`render object
                      to the size of the screen.
                      This example sets the size to`Size(800.0, 600.0)`

`RenderView`
`RenderPositionedBox`
`#dc1df`
`Size(800.0, 600.0)`
The`constraints`property of each render object limits the size
                      of each child. This property takes the[BoxConstraints](https://api.flutter.dev/flutter/rendering/BoxConstraints-class.html)render object as a value.
                      Starting with the`RenderSemanticsAnnotations#fe6b5`, the constraint equals`BoxConstraints(w=800.0, h=600.0)`.

`constraints`
`BoxConstraints`
`RenderSemanticsAnnotations#fe6b5`
`BoxConstraints(w=800.0, h=600.0)`
The[Center](https://api.flutter.dev/flutter/widgets/Center-class.html)widget created the`RenderPositionedBox#dc1df`render object
                      under the`RenderSemanticsAnnotations#8187b`subtree.

`Center`
`RenderPositionedBox#dc1df`
`RenderSemanticsAnnotations#8187b`
Each child under this render object has`BoxConstraints`with both
                      minimum and maximum values. For example,`RenderSemanticsAnnotations#a0a4b`uses`BoxConstraints(0.0<=w<=800.0, 0.0<=h<=600.0)`.

`BoxConstraints`
`RenderSemanticsAnnotations#a0a4b`
`BoxConstraints(0.0<=w<=800.0, 0.0<=h<=600.0)`
All children of the`RenderPhysicalShape#8e171`render object use`BoxConstraints(BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0))`.

`RenderPhysicalShape#8e171`
`BoxConstraints(BoxConstraints(56.0<=w<=800.0, 28.0<=h<=600.0))`
The child`RenderPadding#8455f`sets a`padding`value of`EdgeInsets(8.0, 0.0, 8.0, 0.0)`.
                      This sets a left and right padding of 8 to all subsequent children of
                      this render object.
                      They now have new constraints:`BoxConstraints(40.0<=w<=784.0, 28.0<=h<=600.0)`.

`RenderPadding#8455f`
`padding`
`EdgeInsets(8.0, 0.0, 8.0, 0.0)`
`BoxConstraints(40.0<=w<=784.0, 28.0<=h<=600.0)`
This object, which the`creator`field tells us is
                  probably part of the[TextButton](https://api.flutter.dev/flutter/material/TextButton-class.html)'s definition,
                  sets a minimum width of 88 pixels on its contents and a
                  specific height of 36.0. This is the`TextButton`class implementing
                  the Material Design guidelines regarding button dimensions.

`creator`
`TextButton`
`TextButton`
`RenderPositionedBox#80b8d`render object loosens the constraints again
                  to center the text within the button.
                  The[RenderParagraph](https://api.flutter.dev/flutter/rendering/RenderParagraph-class.html)#59bc2 render object picks its size based on
                  its contents.
                  If you follow the sizes back up the tree,
                  you see how the size of the text influences the width of all the boxes
                  that form the button.
                  All parents take their child's dimensions to size themselves.

`RenderPositionedBox#80b8d`
`RenderParagraph`
Another way to notice this is by looking at the`relayoutBoundary`attribute of in the descriptions of each box.
                  This tells you how many ancestors depend on this element's size.

`relayoutBoundary`
For example, the innermost`RenderPositionedBox`line has a`relayoutBoundary=up13`.
                  This means that when Flutter marks the`RenderConstrainedBox`as dirty,
                  it also marks box's 13 ancestors as dirty because the new dimensions
                  might affect those ancestors.

`RenderPositionedBox`
`relayoutBoundary=up13`
`RenderConstrainedBox`
To add information to the dump if you write your own render objects,
                  override[debugFillProperties()](https://api.flutter.dev/flutter/rendering/Layer/debugFillProperties.html).
                  Add[DiagnosticsProperty](https://api.flutter.dev/flutter/foundation/DiagnosticsProperty-class.html)objects to the method's argument
                  then call the superclass method.

`debugFillProperties()`
### Print the layer tree

To debug a compositing issue, use[debugDumpLayerTree()](https://api.flutter.dev/flutter/rendering/debugDumpLayerTree.html).

`debugDumpLayerTree()`
#### Example 6: CalldebugDumpLayerTree()

`debugDumpLayerTree()`
`import 'package:flutter/material.dart';
​
void main() {
  runApp(const MaterialApp(home: AppHome()));
}
​
class AppHome extends StatelessWidget {
  const AppHome({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Material(
      child: Center(
        child: TextButton(
          onPressed: () {
            debugDumpLayerTree();
          },
          child: const Text('Dump Layer Tree'),
        ),
      ),
    );
  }
}`
`flutter: TransformLayer#214da
flutter:  │ owner: RenderView#ebaaf
flutter:  │ creator: [root]
flutter:  │ engine layer: TransformEngineLayer#535de
flutter:  │ handles: 1
flutter:  │ offset: Offset(0.0, 0.0)
flutter:  │ transform:
flutter:  │   [0] 1.0,0.0,0.0,0.0
flutter:  │   [1] 0.0,1.0,0.0,0.0
flutter:  │   [2] 0.0,0.0,1.0,0.0
flutter:  │   [3] 0.0,0.0,0.0,1.0
flutter:  │
flutter:  ├─child 1: OffsetLayer#0f766
flutter:  │ │ creator: RepaintBoundary ← _FocusInheritedScope ← Semantics ←
flutter:  │ │   FocusScope ← PrimaryScrollController ← _ActionsScope ← Actions
flutter:  │ │   ← Builder ← PageStorage ← Offstage ← _ModalScopeStatus ←
flutter:  │ │   UnmanagedRestorationScope ← ⋯
flutter:  │ │ engine layer: OffsetEngineLayer#1768d
flutter:  │ │ handles: 2
flutter:  │ │ offset: Offset(0.0, 0.0)
flutter:  │ │
flutter:  │ ├─child 1: PictureLayer#dd023
flutter:  │ │   handles: 1
flutter:  │ │   paint bounds: Rect.fromLTRB(0.0, 0.0, 800.0, 600.0)
flutter:  │ │   picture: _NativePicture#36f94
flutter:  │ │   raster cache hints: isComplex = false, willChange = false
flutter:  │ │
flutter:  │ └─child 2: OffsetLayer#4cfc8
flutter:  │   │ creator: RepaintBoundary-[GlobalKey#bd5d9] ← IgnorePointer ←
flutter:  │   │   AnimatedBuilder ← Stack ←
flutter:  │   │   _CupertinoBackGestureDetector<dynamic> ← DecoratedBox ←
flutter:  │   │   DecoratedBoxTransition ← FractionalTranslation ←
flutter:  │   │   SlideTransition ← FractionalTranslation ← SlideTransition ←
flutter:  │   │   CupertinoPageTransition ← ⋯
flutter:  │   │ engine layer: OffsetEngineLayer#a1676
flutter:  │   │ handles: 2
flutter:  │   │ offset: Offset(0.0, 0.0)
flutter:  │   │
flutter:  │   └─child 1: PictureLayer#aee55
flutter:  │       handles: 1
flutter:  │       paint bounds: Rect.fromLTRB(0.0, 0.0, 800.0, 600.0)
flutter:  │       picture: _NativePicture#e732d
flutter:  │       raster cache hints: isComplex = false, willChange = false
flutter:  │
flutter:  └─child 2: PictureLayer#b16e5
flutter:      handles: 1
flutter:      paint bounds: Rect.fromLTRB(0.0, 0.0, 800.0, 600.0)
flutter:      picture: _NativePicture#eef0a
flutter:      raster cache hints: isComplex = false, willChange = false
flutter:`
The`RepaintBoundary`widget creates:

`RepaintBoundary`
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

A`RenderRepaintBoundary`RenderObject in the render tree
                      as shown in the**Example 5**results.

`RenderRepaintBoundary`
`╎     └─child: RenderRepaintBoundary#f8f28
╎       │ needs compositing
╎       │ creator: RepaintBoundary ← _FocusInheritedScope ← Semantics ←
╎       │   FocusScope ← PrimaryScrollController ← _ActionsScope ← Actions
╎       │   ← Builder ← PageStorage ← Offstage ← _ModalScopeStatus ←
╎       │   UnmanagedRestorationScope ← ⋯
╎       │ parentData: <none> (can use size)
╎       │ constraints: BoxConstraints(w=800.0, h=600.0)
╎       │ layer: OffsetLayer#e73b7
╎       │ size: Size(800.0, 600.0)
╎       │ metrics: 66.7% useful (1 bad vs 2 good)
╎       │ diagnosis: insufficient data to draw conclusion (less than five
╎       │   repaints)`
A new layer in the layer tree as shown in the**Example 6**results.

`├─child 1: OffsetLayer#0f766
│ │ creator: RepaintBoundary ← _FocusInheritedScope ← Semantics ←
│ │   FocusScope ← PrimaryScrollController ← _ActionsScope ← Actions
│ │   ← Builder ← PageStorage ← Offstage ← _ModalScopeStatus ←
│ │   UnmanagedRestorationScope ← ⋯
│ │ engine layer: OffsetEngineLayer#1768d
│ │ handles: 2
│ │ offset: Offset(0.0, 0.0)`
This reduces how much needs to be repainted.

### Print the focus tree

To debug a focus or shortcut issue, dump the focus tree
                  using the[debugDumpFocusTree()](https://api.flutter.dev/flutter/widgets/debugDumpFocusTree.html)function.

`debugDumpFocusTree()`
The`debugDumpFocusTree()`method returns the focus tree for the app.

`debugDumpFocusTree()`
The focus tree labels nodes in the following way:

- The focused node is labeled`PRIMARY FOCUS`.
- Ancestors of the focus nodes are labeled`IN FOCUS PATH`.

`PRIMARY FOCUS`
`IN FOCUS PATH`
If your app uses the[Focus](https://api.flutter.dev/flutter/widgets/Focus-class.html)widget, use the[debugLabel](https://api.flutter.dev/flutter/widgets/Focus/debugLabel.html)property to simplify finding its focus node in the tree.

`Focus`
`debugLabel`
You can also use the[debugFocusChanges](https://api.flutter.dev/flutter/widgets/debugFocusChanges.html)boolean property to enable
                  extensive logging when the focus changes.

`debugFocusChanges`
#### Example 7: CalldebugDumpFocusTree()

`debugDumpFocusTree()`
`import 'package:flutter/material.dart';
​
void main() {
  runApp(const MaterialApp(home: AppHome()));
}
​
class AppHome extends StatelessWidget {
  const AppHome({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Material(
      child: Center(
        child: TextButton(
          onPressed: () {
            debugDumpFocusTree();
          },
          child: const Text('Dump Focus Tree'),
        ),
      ),
    );
  }
}`
`flutter: FocusManager#9d096
flutter:  │ primaryFocus: FocusScopeNode#926dc(_ModalScopeState<dynamic>
flutter:  │   Focus Scope [PRIMARY FOCUS])
flutter:  │ primaryFocusCreator: FocusScope ← PrimaryScrollController ←
flutter:  │   _ActionsScope ← Actions ← Builder ← PageStorage ← Offstage ←
flutter:  │   _ModalScopeStatus ← UnmanagedRestorationScope ←
flutter:  │   RestorationScope ← AnimatedBuilder ←
flutter:  │   _ModalScope<dynamic>-[LabeledGlobalKey<_ModalScopeState<dynamic>>#bd53e]
flutter:  │   ← Semantics ← _RenderTheaterMarker ← _EffectiveTickerMode ←
flutter:  │   TickerMode ←
flutter:  │   _OverlayEntryWidget-[LabeledGlobalKey<_OverlayEntryWidgetState>#89dd7]
flutter:  │   ← _Theater ← Overlay-[LabeledGlobalKey<OverlayState>#52f82] ←
flutter:  │   UnmanagedRestorationScope ← ⋯
flutter:  │
flutter:  └─rootScope: FocusScopeNode#f4205(Root Focus Scope [IN FOCUS PATH])
flutter:    │ IN FOCUS PATH
flutter:    │ focusedChildren: FocusScopeNode#a0d10(Navigator Scope [IN FOCUS
flutter:    │   PATH])
flutter:    │
flutter:    └─Child 1: FocusNode#088ec([IN FOCUS PATH])
flutter:      │ context: Focus
flutter:      │ NOT FOCUSABLE
flutter:      │ IN FOCUS PATH
flutter:      │
flutter:      └─Child 1: FocusNode#85f70(Shortcuts [IN FOCUS PATH])
flutter:        │ context: Focus
flutter:        │ NOT FOCUSABLE
flutter:        │ IN FOCUS PATH
flutter:        │
flutter:        └─Child 1: FocusNode#f0c18(Shortcuts [IN FOCUS PATH])
flutter:          │ context: Focus
flutter:          │ NOT FOCUSABLE
flutter:          │ IN FOCUS PATH
flutter:          │
flutter:          └─Child 1: FocusNode#0749f(Shortcuts [IN FOCUS PATH])
flutter:            │ context: Focus
flutter:            │ NOT FOCUSABLE
flutter:            │ IN FOCUS PATH
flutter:            │
flutter:            └─Child 1: _FocusTraversalGroupNode#28990(FocusTraversalGroup [IN FOCUS PATH])
flutter:              │ context: Focus
flutter:              │ NOT FOCUSABLE
flutter:              │ IN FOCUS PATH
flutter:              │
flutter:              └─Child 1: FocusNode#5b515(Shortcuts [IN FOCUS PATH])
flutter:                │ context: Focus
flutter:                │ NOT FOCUSABLE
flutter:                │ IN FOCUS PATH
flutter:                │
flutter:                └─Child 1: FocusScopeNode#a0d10(Navigator Scope [IN FOCUS PATH])
flutter:                  │ context: FocusScope
flutter:                  │ IN FOCUS PATH
flutter:                  │ focusedChildren: FocusScopeNode#926dc(_ModalScopeState<dynamic>
flutter:                  │   Focus Scope [PRIMARY FOCUS])
flutter:                  │
flutter:                  └─Child 1: _FocusTraversalGroupNode#72c8a(FocusTraversalGroup [IN FOCUS PATH])
flutter:                    │ context: Focus
flutter:                    │ NOT FOCUSABLE
flutter:                    │ IN FOCUS PATH
flutter:                    │
flutter:                    └─Child 1: FocusNode#eb709(Navigator [IN FOCUS PATH])
flutter:                      │ context: Focus
flutter:                      │ IN FOCUS PATH
flutter:                      │
flutter:                      └─Child 1: FocusScopeNode#926dc(_ModalScopeState<dynamic> Focus Scope [PRIMARY FOCUS])
flutter:                        │ context: FocusScope
flutter:                        │ PRIMARY FOCUS
flutter:                        │
flutter:                        └─Child 1: FocusNode#a6b74
flutter:                            context: Focus
flutter:`
### Print the semantics tree

The`debugDumpSemanticsTree()`function prints the semantic tree for the app.

`debugDumpSemanticsTree()`
The Semantics tree is presented to the system accessibility APIs.
                  To obtain a dump of the Semantics tree:

1. Enable accessibility using a system accessibility tool
                    or the`SemanticsDebugger`
1. Use the[debugDumpSemanticsTree()](https://api.flutter.dev/flutter/rendering/debugDumpSemanticsTree.html)function.

`SemanticsDebugger`
`debugDumpSemanticsTree()`
#### Example 8: CalldebugDumpSemanticsTree()

`debugDumpSemanticsTree()`
`import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
​
void main() {
  runApp(const MaterialApp(home: AppHome()));
}
​
class AppHome extends StatelessWidget {
  const AppHome({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Material(
      child: Center(
        child: Semantics(
          button: true,
          enabled: true,
          label: 'Clickable text here!',
          child: GestureDetector(
            onTap: () {
              debugDumpSemanticsTree();
              if (kDebugMode) {
                print('Clicked!');
              }
            },
            child: const Text('Click Me!', style: TextStyle(fontSize: 56)),
          ),
        ),
      ),
    );
  }
}`
`flutter: SemanticsNode#0
flutter:  │ Rect.fromLTRB(0.0, 0.0, 800.0, 600.0)
flutter:  │
flutter:  └─SemanticsNode#1
flutter:    │ Rect.fromLTRB(0.0, 0.0, 800.0, 600.0)
flutter:    │ textDirection: ltr
flutter:    │
flutter:    └─SemanticsNode#2
flutter:      │ Rect.fromLTRB(0.0, 0.0, 800.0, 600.0)
flutter:      │ sortKey: OrdinalSortKey#824a2(order: 0.0)
flutter:      │
flutter:      └─SemanticsNode#3
flutter:        │ Rect.fromLTRB(0.0, 0.0, 800.0, 600.0)
flutter:        │ flags: scopesRoute
flutter:        │
flutter:        └─SemanticsNode#4
flutter:            Rect.fromLTRB(278.0, 267.0, 522.0, 333.0)
flutter:            actions: tap
flutter:            flags: isButton, hasEnabledState, isEnabled
flutter:            label:
flutter:              "Clickable text here!
flutter:              Click Me!"
flutter:            textDirection: ltr
flutter:
flutter: Clicked!`
### Print event timings

If you want to find out where your events happen relative to the frame's
                  begin and end, you can set prints to log these events.
                  To print the beginning and end of the frames to the console,
                  toggle the[debugPrintBeginFrameBanner](https://api.flutter.dev/flutter/scheduler/debugPrintBeginFrameBanner.html)and the[debugPrintEndFrameBanner](https://api.flutter.dev/flutter/scheduler/debugPrintEndFrameBanner.html).

`debugPrintBeginFrameBanner`
`debugPrintEndFrameBanner`
**The print frame banner log for Example 1**

`I/flutter : ▄▄▄▄▄▄▄▄ Frame 12         30s 437.086ms ▄▄▄▄▄▄▄▄
I/flutter : Debug print: Am I performing this work more than once per frame?
I/flutter : Debug print: Am I performing this work more than once per frame?
I/flutter : ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀`
To print the call stack causing the current frame to be scheduled,
                  use the[debugPrintScheduleFrameStacks](https://api.flutter.dev/flutter/scheduler/debugPrintScheduleFrameStacks.html)flag.

`debugPrintScheduleFrameStacks`
## Debug layout issues

To debug a layout problem using a GUI, set[debugPaintSizeEnabled](https://api.flutter.dev/flutter/rendering/debugPaintSizeEnabled.html)to`true`.
                  This flag can be found in the`rendering`library.
                  You can enable it at any time and affects all painting while`true`.
                  Consider adding it to the top of your`void main()`entry point.

`debugPaintSizeEnabled`
`true`
`rendering`
`true`
`void main()`
#### Example 9

See an example in the following code:

`// Add import to the Flutter rendering library.
import 'package:flutter/rendering.dart';
​
void main() {
  debugPaintSizeEnabled = true;
  runApp(const MyApp());
}`
When enabled, Flutter displays the following changes to your app:

- Displays all boxes in a bright teal border.
- Displays all padding as a box with a faded blue fill and blue border
                    around the child widget.
- Displays all alignment positioning with yellow arrows.
- Displays all spacers in gray, when they have no child.

The[debugPaintBaselinesEnabled](https://api.flutter.dev/flutter/rendering/debugPaintBaselinesEnabled.html)flag
                  does something similar but for objects with baselines.
                  The app displays the baseline for alphabetic characters in bright green
                  and the baseline for ideographic characters in orange.
                  Alphabetic characters "sit" on the alphabetic baseline,
                  but that baseline "cuts" through the bottom of[CJK characters](https://en.wikipedia.org/wiki/CJK_characters).
                  Flutter positions the ideographic baseline at the very bottom of the text line.

`debugPaintBaselinesEnabled`
The[debugPaintPointersEnabled](https://api.flutter.dev/flutter/rendering/debugPaintPointersEnabled.html)flag turns on a special mode that
                  highlights any objects that you tap in teal.
                  This can help you determine if an object fails to hit test.
                  This might happen if the object falls outside the bounds of its parent
                  and thus not considered for hit testing in the first place.

`debugPaintPointersEnabled`
If you're trying to debug compositor layers, consider using the following flags.


Use the[debugPaintLayerBordersEnabled](https://api.flutter.dev/flutter/rendering/debugPaintLayerBordersEnabled.html)flag to find the boundaries
                      of each layer. This flag results in outlining each layer's bounds in orange.

`debugPaintLayerBordersEnabled`
Use the[debugRepaintRainbowEnabled](https://api.flutter.dev/flutter/rendering/debugRepaintRainbowEnabled.html)flag to display a repainted layer.
                      Whenever a layer repaints, it overlays with a rotating set of colors.

`debugRepaintRainbowEnabled`
Any function or method in the Flutter framework that starts with`debug...`only works in[debug mode](https://docs.flutter.dev/testing/build-modes#debug).

`debug...`
## Debug animation issues

Set the[timeDilation](https://api.flutter.dev/flutter/scheduler/timeDilation.html)variable (from the`scheduler`library) to a number greater than 1.0, for instance, 50.0.
                  It's best to only set this once on app startup. If you
                  change it on the fly, especially if you reduce it while
                  animations are running, it's possible that the framework
                  will observe time going backwards, which will probably
                  result in asserts and generally interfere with your efforts.

`timeDilation`
`scheduler`
## Debug performance issues

Flutter provides a wide variety of top-level properties and functions
                  to help you debug your app at various points along the
                  development cycle.
                  To use these features, compile your app in debug mode.

The following list highlights some flags and one function from the[rendering library](https://api.flutter.dev/flutter/rendering/rendering-library.html)for debugging performance issues.

`debugDumpRenderTree()`
To dump the rendering tree to the console,
                      call this function when not in a layout or repaint phase.

To set these flags either:

- Edit the framework code.
- Import the module, set the value in your`main()`function,
                        then hot restart.

`main()`
`debugPaintLayerBordersEnabled`
To display the boundaries of each layer, set this property to`true`.
                      When set, each layer paints a box around its boundary.

`true`
`debugRepaintRainbowEnabled`
To display a colored border around each widget, set this property to`true`.
                      These borders change color as the app user scrolls in the app.
                      To set this flag, add`debugRepaintRainbowEnabled = true;`as a top-level
                      property in your app.
                      If any static widgets rotate through colors after setting this flag,
                      consider adding repaint boundaries to those areas.

`true`
`debugRepaintRainbowEnabled = true;`
`debugPrintMarkNeedsLayoutStacks`
To determine if your app creates more layouts than expected,
                      set this property to`true`.
                      This layout issue could happen on the timeline, on a profile,
                      or from a`print`statement inside a layout method.
                      When set, the framework outputs stack traces to the console
                      to explain why your app marks each render object to be laid out.

`true`
`print`
`debugPrintMarkNeedsPaintStacks`
To determine if your app paints more layouts than expected,
                      set this property to`true`.

`true`
You can generate stack traces on demand as well.
                  To print your own stack traces, add the`debugPrintStack()`function to your app.

`debugPrintStack()`
### Trace Dart code performance

To perform custom performance traces and measure wall or CPU time of arbitrary
                  segments of Dart code, use`dart:developer`[Timeline](https://api.dart.dev/dart-developer/Timeline-class.html)utilities.

`dart:developer`
1. code-excerpt "lib/perf_trace.dart"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Open your source code.

Wrap the code you want to measure in`Timeline`methods.

`Timeline`
`import 'dart:developer';
​
void main() {
  Timeline.startSync('interesting function');
  // iWonderHowLongThisTakes();
  Timeline.finishSync();
}`
While connected to your app, open DevTools'[Timeline events tab](https://docs.flutter.dev/tools/devtools/performance#timeline-events-tab).

Select the**Dart**recording option in the**Performance settings**.

Perform the function you want to measure.

To ensure that the runtime performance characteristics closely match that
                  of your final product, run your app in[profile mode](https://docs.flutter.dev/testing/build-modes#profile).

### Add performance overlay

To enable the`PerformanceOverlay`widget in your code,
                  set the`showPerformanceOverlay`property to`true`on the[MaterialApp](https://api.flutter.dev/flutter/material/MaterialApp/MaterialApp.html),[CupertinoApp](https://api.flutter.dev/flutter/cupertino/CupertinoApp-class.html), or[WidgetsApp](https://api.flutter.dev/flutter/widgets/WidgetsApp-class.html)constructor:

`PerformanceOverlay`
`showPerformanceOverlay`
`true`
`MaterialApp`
`CupertinoApp`
`WidgetsApp`
#### Example 10

`import 'package:flutter/material.dart';
​
class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      showPerformanceOverlay: true,
      title: 'My Awesome App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'My Awesome App'),
    );
  }
}`
(If you're not using`MaterialApp`,`CupertinoApp`,
                  or`WidgetsApp`, you can get the same effect by wrapping your
                  application in a stack and putting a widget on your stack that was
                  created by calling[PerformanceOverlay.allEnabled()](https://api.flutter.dev/flutter/widgets/PerformanceOverlay/PerformanceOverlay.allEnabled.html).)

`MaterialApp`
`CupertinoApp`
`WidgetsApp`
`PerformanceOverlay.allEnabled()`
To learn how to interpret the graphs in the overlay,
                  check out[The performance overlay](https://docs.flutter.dev/perf/ui-performance#the-performance-overlay)in[Profiling Flutter performance](https://docs.flutter.dev/perf/ui-performance).

## Add widget alignment grid

To add an overlay to a[Material Design baseline grid](https://m3.material.io/foundations/layout/understanding-layout/spacing)on your app to
                  help verify alignments, add the`debugShowMaterialGrid`argument in the[MaterialAppconstructor](https://api.flutter.dev/flutter/material/MaterialApp/MaterialApp.html).

`debugShowMaterialGrid`
`MaterialApp`
To add an overlay to non-Material applications, add a[GridPaper](https://api.flutter.dev/flutter/widgets/GridPaper-class.html)widget.

`GridPaper`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/code-debugging.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/testing/code-debugging&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/code-debugging.md).
