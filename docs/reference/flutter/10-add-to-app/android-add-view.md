> 原文链接: [https://docs.flutter.dev/add-to-app/android/add-flutter-view](https://docs.flutter.dev/add-to-app/android/add-flutter-view)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Integrating via a[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)requires a bit more work than via FlutterActivity and FlutterFragment previously
                  described.

Fundamentally, the Flutter framework on the Dart side requires access to various
                  activity-level events and lifecycles to function. Since the FlutterView (which
                  is an[android.view.View](https://developer.android.com/reference/android/view/View.html))
                  can be added to any activity which is owned by the developer's application
                  and since the FlutterView doesn't have access to activity level events, the
                  developer must bridge those connections manually to the[FlutterEngine](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/FlutterEngine.html).

How you choose to feed your application's activities' events to the FlutterView
                  will be specific to your application.

## A sample

Unlike the guides for FlutterActivity and FlutterFragment, the FlutterView
                  integration could be better demonstrated with a sample project.

A sample project is at[https://github.com/flutter/samples/tree/main/add_to_app/android_view](https://github.com/flutter/samples/tree/main/add_to_app/android_view)to document a simple FlutterView integration where FlutterViews are used
                  for some of the cells in a RecycleView list of cards as seen in the gif above.

## General approach

The general gist of the FlutterView-level integration is that you
                  must recreate the various interactions between your Activity, the[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)and the[FlutterEngine](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/FlutterEngine.html)present in the[FlutterActivityAndFragmentDelegate](https://cs.opensource.google/flutter/engine/+/main:shell/platform/android/io/flutter/embedding/android/FlutterActivityAndFragmentDelegate.java)in your own application's code.
                  The connections made in the[FlutterActivityAndFragmentDelegate](https://cs.opensource.google/flutter/engine/+/main:shell/platform/android/io/flutter/embedding/android/FlutterActivityAndFragmentDelegate.java)are done automatically when using a[FlutterActivity](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterActivity.html)or a[FlutterFragment](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterFragment.html),
                  but since the[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)in this case is being added to an`Activity`or`Fragment`in your application,
                  you must recreate the connections manually.
                  Otherwise, the[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)won't render anything or have other missing functionalities.

`FlutterView`
`FlutterEngine`
`FlutterActivityAndFragmentDelegate`
`FlutterActivityAndFragmentDelegate`
`FlutterActivity`
`FlutterFragment`
`FlutterView`
`Activity`
`Fragment`
`FlutterView`
A sample[FlutterViewEngine](https://github.com/flutter/samples/blob/main/add_to_app/android_view/android_view/app/src/main/java/dev/flutter/example/androidView/FlutterViewEngine.kt)class shows one such possible implementation of an application-specific
                  connection between an`Activity`, a[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)and a[FlutterEngine](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/FlutterEngine.html).

`FlutterViewEngine`
`Activity`
`FlutterView`
### APIs to implement

The absolute minimum implementation needed for Flutter
                  to draw anything at all is to:

- Call[attachToFlutterEngine](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html#attachToFlutterEngine-io.flutter.embedding.engine.FlutterEngine-)when the[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)is added to a resumed`Activity`'s view hierarchy and is visible; and
- Call[appIsResumed](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/systemchannels/LifecycleChannel.html#appIsResumed--)on the[FlutterEngine](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/FlutterEngine.html)'s`lifecycleChannel`field when the`Activity`hosting the[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)is visible.

`attachToFlutterEngine`
`FlutterView`
`Activity`
`appIsResumed`
`FlutterEngine`
`lifecycleChannel`
`Activity`
`FlutterView`
The reverse[detachFromFlutterEngine](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html#detachFromFlutterEngine--)and other lifecycle methods on the[LifecycleChannel](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/systemchannels/LifecycleChannel.html)class must also be called to not leak resources when the`FlutterView`or`Activity`is no longer visible.

`detachFromFlutterEngine`
`LifecycleChannel`
`FlutterView`
`Activity`
In addition, see the remaining implementation in the[FlutterViewEngine](https://github.com/flutter/samples/blob/main/add_to_app/android_view/android_view/app/src/main/java/dev/flutter/example/androidView/FlutterViewEngine.kt)demo class or in the[FlutterActivityAndFragmentDelegate](https://cs.opensource.google/flutter/engine/+/main:shell/platform/android/io/flutter/embedding/android/FlutterActivityAndFragmentDelegate.java)to ensure a correct functioning of other features such as clipboards,
                  system UI overlay, plugins, and so on.

`FlutterViewEngine`
`FlutterActivityAndFragmentDelegate`
## Content-sized views

Usually, a[FlutterView](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterView.html)needs fixed dimensions either through it's own dimensions or by matching a
                  parent's dimensions.  This can be seen in the[sample project](https://github.com/flutter/samples/tree/main/add_to_app/android_view/android_view).
                  However, it's now possible to allow`FlutterView`to size itself
                  based on its content. By using,`content_wrap`for either the height
                  or the width a`FlutterView`can size itself, as shown in the[content sized sample project](https://github.com/flutter/samples/tree/main/add_to_app/android_view/content_sizing_android_view).

`FlutterView`
`FlutterView`
`content_wrap`
`FlutterView`
- To*enable*Content-sized view when deploying your app,
                    add the following setting to your project's`AndroidManifest.xml`file under the`<application>`tag:

`AndroidManifest.xml`
`<application>`
`<meta-data
  android:name="io.flutter.embedding.android.EnableContentSizing"
  android:value="true" />`
### Restrictions

Since content-sized Flutter views require your Flutter app to be able to size itself,
                  some widgets are not supported.

- A widget with unbounded size, like a`ListView`.
- A widget that defers to its child for the size, like`LayoutBuilder`.

`ListView`
`LayoutBuilder`
In practice, this means that quite a few common widgets are not supported,
                  such as`ScaffoldBuilder`,`CupertinoTimerPicker`,
                  or any widget that internally relies on a`LayoutBuilder`.
                  When in doubt, you can use an`UnconstrainedBox`to test the usability of
                  a widget for a content-sized view, as shown in the following example:

`ScaffoldBuilder`
`CupertinoTimerPicker`
`LayoutBuilder`
`UnconstrainedBox`
`import 'package:flutter/material.dart';
​
void main() => runApp(MyApp());
​
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context)
  => MaterialApp(home: MyPage());
}
​
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: UnconstrainedBox(
          // TODO: Edit this line to check if a widget
          // can cause problems with content-sized views.
          child: Text('This works!'),
          // child: Column(children: [Column(children: [Expanded(child: Text('This blows up!'))])]),
          // child: ListView(children: [Text('This blows up!')]),
        )
    );
  }
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/add-flutter-view.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/add-to-app/android/add-flutter-view&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/add-flutter-view.md).
