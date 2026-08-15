> 原文链接: [https://docs.flutter.dev/testing/errors](https://docs.flutter.dev/testing/errors)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The Flutter framework catches errors that occur during callbacks
                  triggered by the framework itself, including errors encountered
                  during the build, layout, and paint phases. Errors that don't occur
                  within Flutter's callbacks can't be caught by the framework,
                  but you can handle them by setting up an error handler on the[PlatformDispatcher](https://api.flutter.dev/flutter/dart-ui/PlatformDispatcher-class.html).

`PlatformDispatcher`
All errors caught by Flutter are routed to the[FlutterError.onError](https://api.flutter.dev/flutter/foundation/FlutterError/onError.html)handler. By default,
                  this calls[FlutterError.presentError](https://api.flutter.dev/flutter/foundation/FlutterError/presentError.html),
                  which dumps the error to the device logs.
                  When running from an IDE, the inspector overrides this
                  behavior so that errors can also be routed to the IDE's
                  console, allowing you to inspect the
                  objects mentioned in the message.

`FlutterError.onError`
`FlutterError.presentError`
When an error occurs during the build phase,
                  the[ErrorWidget.builder](https://api.flutter.dev/flutter/widgets/ErrorWidget/builder.html)callback is
                  invoked to build the widget that is used
                  instead of the one that failed. By default,
                  in debug mode this shows an error message in red,
                  and in release mode this shows a gray background.

`ErrorWidget.builder`
When errors occur without a Flutter callback on the call stack,
                  they are handled by the`PlatformDispatcher`'s error callback. By default,
                  this only prints errors and does nothing else.

`PlatformDispatcher`
You can customize these behaviors,
                  typically by setting them to values in
                  your`void main()`function.

`void main()`
Below each error type handling is explained. At the bottom
                  there's a code snippet which handles all types of errors. Even
                  though you can just copy-paste the snippet, we recommend you
                  to first get acquainted with each of the error types.

## Errors caught by Flutter

For example, to make your application quit immediately any time an
                  error is caught by Flutter in release mode, you could use the
                  following handler:

`import 'dart:io';
​
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
​
void main() {
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    if (kReleaseMode) exit(1);
  };
  runApp(const MyApp());
}
​
// The rest of the `flutter create` code...`
This handler can also be used to report errors to a logging service.
                  For more details, see our cookbook chapter for[reporting errors to a service](https://docs.flutter.dev/cookbook/maintenance/error-reporting).

## Define a custom error widget for build phase errors

To define a customized error widget that displays whenever
                  the builder fails to build a widget, use[MaterialApp.builder](https://api.flutter.dev/flutter/material/MaterialApp/builder.html).

`MaterialApp.builder`
`class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      builder: (context, widget) {
        Widget error = const Text('...rendering error...');
        if (widget is Scaffold || widget is Navigator) {
          error = Scaffold(body: Center(child: error));
        }
        ErrorWidget.builder = (errorDetails) => error;
        if (widget != null) return widget;
        throw StateError('widget is null');
      },
    );
  }
}`
## Errors not caught by Flutter

Consider an`onPressed`callback that invokes an asynchronous function,
                  such as`MethodChannel.invokeMethod`(or pretty much any plugin).
                  For example:

`onPressed`
`MethodChannel.invokeMethod`
`OutlinedButton(
  child: const Text('Click me!'),
  onPressed: () async {
    const channel = MethodChannel('crashy-custom-channel');
    await channel.invokeMethod('blah');
  },
)`
If`invokeMethod`throws an error, it won't be forwarded to`FlutterError.onError`.
                  Instead, it's forwarded to the`PlatformDispatcher`.

`invokeMethod`
`FlutterError.onError`
`PlatformDispatcher`
To catch such an error, use[PlatformDispatcher.instance.onError](https://api.flutter.dev/flutter/dart-ui/PlatformDispatcher/onError.html).

`PlatformDispatcher.instance.onError`
`import 'package:flutter/material.dart';
import 'dart:ui';
​
void main() {
  MyBackend myBackend = MyBackend();
  PlatformDispatcher.instance.onError = (error, stack) {
    myBackend.sendError(error, stack);
    return true;
  };
  runApp(const MyApp());
}`
## Handling all types of errors

Say you want to exit application on any exception and to display
                  a custom error widget whenever a widget building fails - you can base
                  your errors handling on next code snippet:

`import 'package:flutter/material.dart';
import 'dart:ui';
​
Future<void> main() async {
  await myErrorsHandler.initialize();
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    myErrorsHandler.onErrorDetails(details);
  };
  PlatformDispatcher.instance.onError = (error, stack) {
    myErrorsHandler.onError(error, stack);
    return true;
  };
  runApp(const MyApp());
}
​
class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      builder: (context, widget) {
        Widget error = const Text('...rendering error...');
        if (widget is Scaffold || widget is Navigator) {
          error = Scaffold(body: Center(child: error));
        }
        ErrorWidget.builder = (errorDetails) => error;
        if (widget != null) return widget;
        throw StateError('widget is null');
      },
    );
  }
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/errors.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/testing/errors&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/errors.md).
