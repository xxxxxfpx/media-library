> 原文链接: [https://docs.flutter.dev/perf/ui-performance](https://docs.flutter.dev/perf/ui-performance)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Overview

App performance encompasses various aspects, from raw speed and I/O throughput
                  to the smoothness of the user interface. While this page primarily focuses on UI
                  smoothness (lack of stutter or jank), the tools described here can often be used
                  to diagnose other performance issues as well.

Flutter offers several tools for performance analysis. Here are a few of them:


**The Performance Overlay**: Displays a simplified set of metrics directly
                      within your running app. To learn more, see the sections in this topic.

**The Performance View**: A web-based interface that connects to your app and
                      displays detailed performance metrics. Part of the DevTools utility. To learn
                      more, see[Use the Performance View](https://docs.flutter.dev/tools/devtools/performance).

**Performance tracing within Dart**: Add tracing directly into your app's
                      Dart code, using the`dart:developer package`, and then track your app's
                      performance in the DevTools utility. To learn more, see[Tracing Dart code](https://docs.flutter.dev/testing/code-debugging#trace-dart-code-performance).

`dart:developer package`
**Benchmarking**: You can measure and track your app's performance by writing
                      benchmark tests. The Flutter Driver library provides support
                      for benchmarking. Using this integration test framework,
                      you can generate metrics that track jank, download size, battery efficiency,
                      and startup time. For more information, check out[Integration testing](https://docs.flutter.dev/testing/integration-tests).

**Widget rebuild profiler (IntelliJ for Android Studio)**: Jank often arises
                      from unnecessary UI rebuilds. If you are using IntelliJ for Android Studio,
                      the Widget Rebuild Profiler helps pinpoint and fix these issues by showing
                      widget rebuild counts for the current screen and frame. For more information,
                      see[Show performance data](https://docs.flutter.dev/tools/android-studio#show-performance-data).

Flutter aims to provide 60 frames per second (fps) performance,
                  or 120 fps on devices that support it. To achieve the 60fps, each frame must
                  render approximately every 16ms to avoid jank. Jank occurs when frames take
                  significantly longer to render and are dropped, resulting in a visible stutter
                  in animations. For example, if a frame occasionally takes 10 times longer than
                  usual to render, it will likely be dropped, causing the animation to appear
                  jerky.

## Connect to a physical device

Almost all performance debugging for Flutter applications
                  should be conducted on a physical Android or iOS device,
                  with your Flutter application running in[profile mode](https://docs.flutter.dev/testing/build-modes#profile).
                  Using debug mode, or running apps on simulators
                  or emulators, is generally not indicative of the final
                  behavior of release mode builds.*You should consider checking performance
                    on the slowest device that your users might reasonably use.*

## Run in profile mode

Flutter's profile mode compiles and launches your application
                  almost identically to release mode, but with just enough additional
                  functionality to allow debugging performance problems.
                  For example, profile mode provides tracing information to the
                  profiling tools.

Launch the app in profile mode as follows:

- json@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
- @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

In VS Code, open your`launch.json`file, and set the`flutterMode`property to`profile`(when done profiling, change it back to`release`or`debug`):

`launch.json`
`flutterMode`
`profile`
`release`
`debug`
`"configurations": [
  {
    "name": "Flutter",
    "request": "launch",
    "type": "dart",
    "flutterMode": "profile"
  }
]`
In Android Studio and IntelliJ, use the**Run > Flutter Run main.dart in Profile Mode**menu item.

From the command line, use the`--profile`flag:

`--profile`
`$ flutter run --profile`
For more information on the different modes,
                  see[Flutter's build modes](https://docs.flutter.dev/testing/build-modes).

You'll begin by opening DevTools and viewing
                  the performance overlay, as discussed in the next section.

## Launch DevTools

DevTools provides features like profiling, examining the heap,
                  displaying code coverage, enabling the performance overlay,
                  and a step-by-step debugger.
                  DevTools'[Timeline view](https://docs.flutter.dev/tools/devtools/performance)allows you to investigate the
                  UI performance of your application on a frame-by-frame basis.

Once your app is running in profile mode,[launch DevTools](https://docs.flutter.dev/tools/devtools).

## Display the performance overlay

You can toggle the display of the performance overlay as
                  follows:


**DevTools Performance view**: The easiest way to enable the
                      PerformanceOverlay widget is from the[Performance view](https://docs.flutter.dev/tools/devtools/performance)in[DevTools](https://docs.flutter.dev/tools/devtools).
                      Simply click the**Performance Overlay**button to toggle the overlay on your
                      running app.

**command line**: Toggle the performance overlay using the**P**key from
                      the command line.

**programmatically**: To enable the overlay programmatically, see[Performance overlay](https://docs.flutter.dev/testing/code-debugging#add-performance-overlay), a section in the[Debugging Flutter apps programmatically](https://docs.flutter.dev/testing/code-debugging)page.

## Observe the performance overlay

The performance overlay displays statistics in two graphs
                  that show where time is being spent in your app. If the UI
                  is janky (skipping frames), these graphs help you figure out why.
                  The graphs display on top of your running app, but they aren't
                  drawn like a normal widget—the Flutter engine itself
                  paints the overlay and only minimally impacts performance.
                  Each graph represents the last 300 frames for that thread.

This section describes how to enable the performance overlay
                  and use it to diagnose the cause of jank in your application.
                  The following screenshot shows the performance overlay running
                  on the Flutter Gallery example:

![Screenshot of overlay showing zero jank](https://docs.flutter.dev/assets/images/docs/tools/devtools/performance-overlay-green.png)
Performance overlay showing the raster thread (top),
                  and UI thread (bottom).
The vertical green bars
                  represent the current frame.

### Review the graphs

The top graph (marked "GPU") shows the time spent by
                  the raster thread, the bottom one graph shows the time
                  spent by the UI thread.
                  The white lines across the graphs show 16ms increments
                  along the vertical axis; if the graph ever goes over one
                  of these lines then you are running at less than 60Hz.
                  The horizontal axis represents frames. The graph is
                  only updated when your application paints,
                  so if it's idle the graph stops moving.

The overlay should always be viewed in[profile mode](https://docs.flutter.dev/testing/build-modes#profile),
                  since[debug mode](https://docs.flutter.dev/testing/build-modes#debug)performance is intentionally sacrificed
                  in exchange for expensive asserts that are intended to aid
                  development, and thus the results are misleading.

Each frame should be created and displayed within 1/60th of
                  a second (approximately 16ms). A frame exceeding this limit
                  (in either graph) fails to display, resulting in jank,
                  and a vertical red bar appears in one or both of the graphs.
                  If a red bar appears in the UI graph, the Dart code is too
                  expensive. If a red vertical bar appears in the GPU graph,
                  the scene is too complicated to render quickly.

![Screenshot of performance overlay showing jank with red bars](https://docs.flutter.dev/assets/images/docs/tools/devtools/performance-overlay-jank.png)
The vertical red bars indicate that the current frame is
                  expensive to both render and paint.
When both graphs
                  display red, start by diagnosing the UI thread.

### Review the threads

Flutter uses several threads to do its work, though
                  only two of the threads are shown in the overlay.
                  All of your Dart code runs on the UI thread.
                  Although you have no direct access to any other thread,
                  your actions on the UI thread have performance consequences
                  on other threads.

The platform's main thread. Plugin code runs here.
                      For more information, see the[UIKit](https://developer.apple.com/documentation/uikit)documentation for iOS,
                      or the[MainThread](https://developer.android.com/reference/android/support/annotation/MainThread)documentation for Android.*This thread is not shown in the performance overlay.*

The UI thread executes Dart code in the Dart VM.
                      This thread includes code that you wrote, and code executed by
                      Flutter's framework on your app's behalf.
                      When your app creates and displays a scene, the UI thread creates
                      a*layer tree*, a lightweight object containing device-agnostic
                      painting commands, and sends the layer tree to the raster thread to
                      be rendered on the device.*Don't block this thread!*Shown in the bottom row of the performance overlay.

The raster thread takes the layer tree and displays
                      it by talking to the GPU (graphic processing unit).
                      You cannot directly access the raster thread or its data but,
                      if this thread is slow, it's a result of something you've done
                      in the Dart code. Skia and Impeller, the graphics libraries,
                      run on this thread.
                      Shown in the top row of the performance overlay.
                      Note that while the raster thread rasterizes for the GPU,
                      the thread itself runs on the CPU.

Performs expensive tasks (mostly I/O) that would
                      otherwise block either the UI or raster threads.*This thread is not shown in the performance overlay.*

For links to more information and videos,
                  see[The Framework architecture](https://github.com/flutter/flutter/blob/main/docs/about/The-Framework-architecture.md)in the[Flutter wiki](https://github.com/flutter/flutter/tree/main/docs), and the community article,[The Layer Cake](https://medium.com/flutter-community/the-layer-cake-widgets-elements-renderobjects-7644c3142401).

## Identify problems

### Review the UI graph

If the performance overlay shows red in the UI graph,
                  start by profiling the Dart VM, even if the GPU graph
                  also shows red.

### Review the GPU graph

Sometimes a scene results in a layer tree that is easy to construct,
                  but expensive to render on the raster thread. When this happens,
                  the UI graph has no red, but the GPU graph shows red.
                  In this case, you'll need to figure out what your code is doing
                  that is causing rendering code to be slow. Specific kinds of workloads
                  are more difficult for the GPU. They might involve unnecessary calls
                  to[saveLayer](https://api.flutter.dev/flutter/dart-ui/Canvas/saveLayer.html), intersecting opacities with multiple objects,
                  and clips or shadows in specific situations.

`saveLayer`
If you suspect that the source of the slowness is during an animation,
                  click the**Slow Animations**button in the Flutter inspector
                  to slow animations down by 5x.
                  If you want more control on the speed, you can also do this[programmatically](https://docs.flutter.dev/testing/code-debugging#debug-animation-issues).

Is the slowness on the first frame, or on the whole animation?
                  If it's the whole animation, is clipping causing the slow down?
                  Maybe there's an alternative way of drawing the scene that doesn't
                  use clipping. For example, overlay opaque corners onto a square
                  instead of clipping to a rounded rectangle.
                  If it's a static scene that's being faded, rotated, or otherwise
                  manipulated, a[RepaintBoundary](https://api.flutter.dev/flutter/widgets/RepaintBoundary-class.html)might help.

`RepaintBoundary`
#### Checking for offscreen layers

The[saveLayer](https://api.flutter.dev/flutter/dart-ui/Canvas/saveLayer.html)method is one of the most expensive methods in
                  the Flutter framework. It's useful when applying post-processing
                  to the scene, but it can slow your app and should be avoided if
                  you don't need it.  Even if you don't call`saveLayer`explicitly,
                  implicit calls might happen on your behalf, for example when specifying[Clip.antiAliasWithSaveLayer](https://api.flutter.dev/flutter/dart-ui/Clip.html)(typically as a`clipBehavior`).

`saveLayer`
`saveLayer`
`Clip.antiAliasWithSaveLayer`
`clipBehavior`
For example,
                  perhaps you have a group of objects with opacities that are rendered
                  using`saveLayer`. In this case, it's probably more performant to
                  apply an opacity to each individual widget, rather than a parent
                  widget higher up in the widget tree. The same goes for
                  other potentially expensive operations, such as clipping or shadows.

`saveLayer`
When you encounter calls to`saveLayer`,
                  ask yourself these questions:

`saveLayer`
- Does the app need this effect?
- Can any of these calls be eliminated?
- Can I apply the same effect to an individual element instead of a group?

#### Checking for non-cached images

Caching an image with[RepaintBoundary](https://api.flutter.dev/flutter/widgets/RepaintBoundary-class.html)is good,*when it makes sense*.

`RepaintBoundary`
One of the most expensive operations,
                  from a resource perspective,
                  is rendering a texture using an image file.
                  First, the compressed image
                  is fetched from persistent storage.
                  The image is decompressed into host memory (GPU memory),
                  and transferred to device memory (RAM).

In other words, image I/O can be expensive.
                  The cache provides snapshots of complex hierarchies so
                  they are easier to render in subsequent frames.*Because raster cache entries are expensive to
                    construct and take up loads of GPU memory,
                    cache images only where absolutely necessary.*

## Other resources

The following resources provide more information on using
                  Flutter's tools and debugging in Flutter:

- [Debugging](https://docs.flutter.dev/testing/debugging)
- [Performance view](https://docs.flutter.dev/tools/devtools/performance)
- [Flutter inspector](https://docs.flutter.dev/tools/devtools/inspector)
- [Flutter inspector talk](https://www.youtube.com/watch?v=JIcmJNT9DNI), presented at DartConf 2018
- [Why Flutter Uses Dart](https://hackernoon.com/why-flutter-uses-dart-dd635a054ebf), an article on Hackernoon
- [Why Flutter uses Dart](https://www.youtube.com/watch?v=5F-6n_2XWR8), a video on the Flutter channel
- [DevTools](https://docs.flutter.dev/tools/devtools): performance tooling for Dart and Flutter apps
- [Flutter API](https://api.flutter.dev)docs, particularly the[PerformanceOverlay](https://api.flutter.dev/flutter/widgets/PerformanceOverlay-class.html)class,
                    and the[dart:developer](https://api.flutter.dev/flutter/dart-developer/dart-developer-library.html)package

`PerformanceOverlay`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/ui-performance.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/perf/ui-performance&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/ui-performance.md).
