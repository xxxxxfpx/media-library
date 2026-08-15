> 原文链接: [https://docs.flutter.dev/platform-integration/macos/platform-views](https://docs.flutter.dev/platform-integration/macos/platform-views)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Platform views allow you to embed native views in a Flutter app, so you can
                  apply transforms, clips, and opacity to the native view from Dart.

This allows you, for example, to use the native web views directly inside your
                  Flutter app.

macOS uses Hybrid composition, which means that the
                  native`NSView`is appended to the view hierarchy.

`NSView`
To create a platform view on macOS, use the following instructions:

## On the Dart side

On the Dart side, create a`Widget`and add the build implementation,
                  as shown in the following steps:

`Widget`
In the Dart widget file, make changes similar to those
                  shown in`native_view_example.dart`:

`native_view_example.dart`
1. code-excerpt "lib/native_view_example_4.dart (import)"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. code-excerpt "lib/native_view_example_4.dart (macos-composition)"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Add the following imports:

`import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';`
Implement a`build()`method:

`build()`
`Widget build(BuildContext context) {
  // This is used in the platform side to register the view.
  const String viewType = '<platform-view-type>';
  // Pass parameters to the platform side.
  final Map<String, dynamic> creationParams = <String, dynamic>{};
​
  return AppKitView(
    viewType: viewType,
    layoutDirection: TextDirection.ltr,
    creationParams: creationParams,
    creationParamsCodec: const StandardMessageCodec(),
  );
}`
For more information, check out the[AppKitView](https://api.flutter.dev/flutter/widgets/AppKitView-class.html)API docs.

`AppKitView`
## On the platform side

Implement the factory and the platform view.
                  The`NativeViewFactory`creates the platform view, and
                  the platform view provides a reference to the`NSView`.
                  For example,`NativeView.swift`:

`NativeViewFactory`
`NSView`
`NativeView.swift`
`import Cocoa
import FlutterMacOS
​
class NativeViewFactory: NSObject, FlutterPlatformViewFactory {
  private var messenger: FlutterBinaryMessenger
​
  init(messenger: FlutterBinaryMessenger) {
    self.messenger = messenger
    super.init()
  }
​
  func create(
    withViewIdentifier viewId: Int64,
    arguments args: Any?
  ) -> NSView {
    return NativeView(
      viewIdentifier: viewId,
      arguments: args,
      binaryMessenger: messenger)
  }
​
  /// Implementing this method is only necessary when
  /// the `arguments` in `createWithFrame` is not `nil`.
  public func createArgsCodec() -> (FlutterMessageCodec & NSObjectProtocol)? {
    return FlutterStandardMessageCodec.sharedInstance()
  }
}
​
class NativeView: NSView {
​
  init(
    viewIdentifier viewId: Int64,
    arguments args: Any?,
    binaryMessenger messenger: FlutterBinaryMessenger?
  ) {
    super.init(frame: CGRect(x: 0, y: 0, width: 200, height: 200))
    wantsLayer = true
    layer?.backgroundColor = NSColor.systemBlue.cgColor
    // macOS views can be created here
    createNativeView(view: self)
  }
​
    required init?(coder nsCoder: NSCoder) {
        super.init(coder: nsCoder)
    }
​
  func createNativeView(view _view: NSView) {
    let nativeLabel = NSTextField()
    nativeLabel.frame = CGRect(x: 0, y: 0, width: 180, height: 48.0)
    nativeLabel.stringValue = "Native text from macOS"
    nativeLabel.textColor = NSColor.black
    nativeLabel.font = NSFont.systemFont(ofSize: 14)
    nativeLabel.isBezeled = false
    nativeLabel.focusRingType = .none
    nativeLabel.isEditable = true
    nativeLabel.sizeToFit()
    _view.addSubview(nativeLabel)
  }
}`
Finally, register the platform view.
                  This can be done in an app or a plugin.

For app registration, modify the App's`MainFlutterWindow.swift`:

`MainFlutterWindow.swift`
`import Cocoa
import FlutterMacOS
​
class MainFlutterWindow: NSWindow {
  override func awakeFromNib() {
    // ...
​
    let registrar = flutterViewController.registrar(forPlugin: "plugin-name")
    let factory = NativeViewFactory(messenger: registrar.messenger)
    registrar.register(
      factory,
      withId: "<platform-view-type>")
  }
}`
For plugin registration, modify the plugin's main file:

`import Cocoa
import FlutterMacOS
​
public class Plugin: NSObject, FlutterPlugin {
  public static func register(with registrar: FlutterPluginRegistrar) {
    let factory = NativeViewFactory(messenger: registrar.messenger)
    registrar.register(factory, withId: "<platform-view-type>")
  }
}`
For more information, check out the API docs for:

- [FlutterPlatformViewFactory](https://api.flutter.dev/ios-embedder/protocol_flutter_platform_view_factory-p.html)
- [FlutterPlatformView](https://api.flutter.dev/ios-embedder/protocol_flutter_platform_view-p.html)
- [PlatformView](https://api.flutter.dev/javadoc/io/flutter/plugin/platform/PlatformView.html)

`FlutterPlatformViewFactory`
`FlutterPlatformView`
`PlatformView`
## Putting it together

When implementing the`build()`method in Dart,
                  you can use[defaultTargetPlatform](https://api.flutter.dev/flutter/foundation/defaultTargetPlatform.html)to detect the platform, and decide which widget to use:

`build()`
`defaultTargetPlatform`
`Widget build(BuildContext context) {
  // This is used in the platform side to register the view.
  const String viewType = '<platform-view-type>';
  // Pass parameters to the platform side.
  final Map<String, dynamic> creationParams = <String, dynamic>{};
​
  switch (defaultTargetPlatform) {
    case TargetPlatform.android:
    // return widget on Android.
    case TargetPlatform.iOS:
    // return widget on iOS.
    case TargetPlatform.macOS:
    // return widget on macOS.
    default:
      throw UnsupportedError('Unsupported platform view');
  }
}`
## Performance

Platform views in Flutter come with performance trade-offs.

For example, in a typical Flutter app, the Flutter UI is composed on a dedicated
                  raster thread. This allows Flutter apps to be fast, as this thread is rarely
                  blocked.

When a platform view is rendered with hybrid composition, the Flutter UI
                  continues to be composed from the dedicated raster thread, but the platform view
                  performs graphics operations on the platform thread. To rasterize the combined
                  contents, Flutter performs synchronization between its raster thread and the
                  platform thread. As such, any slow or blocking operations on the platform thread
                  can negatively impact Flutter graphics performance.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/macos/platform-views.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/macos/platform-views&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/macos/platform-views.md).
