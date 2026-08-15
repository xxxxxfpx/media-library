> 原文链接: [https://docs.flutter.dev/perf/web-performance](https://docs.flutter.dev/perf/web-performance)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The Flutter framework emits timeline events as it works to build frames,
                  draw scenes, and track other activity such as garbage collections.
                  These events are exposed in the[Chrome DevTools performance panel](https://developer.chrome.com/docs/devtools/performance)for debugging.

You can also emit your own timeline events using the`dart:developer`[Timeline](https://api.flutter.dev/flutter/dart-developer/Timeline-class.html)and[TimelineTask](https://api.flutter.dev/flutter/dart-developer/TimelineTask-class.html)APIs for further performance analysis.

`dart:developer`
![Screenshot of the Chrome DevTools performance panel](https://docs.flutter.dev/assets/images/docs/tools/devtools/chrome-devtools-performance-panel.png)

## Optional flags to enhance tracing

To configure which timeline events are tracked, set any of the following top-level properties to`true`in your app's`main`method.

`true`
`main`
- [debugProfileBuildsEnabled](https://api.flutter.dev/flutter/widgets/debugProfileBuildsEnabled.html): Adds`Timeline`events for every`Widget`built.
- [debugProfileBuildsEnabledUserWidgets](https://api.flutter.dev/flutter/widgets/debugProfileBuildsEnabledUserWidgets.html): Adds`Timeline`events for every user-created`Widget`built.
- [debugProfileLayoutsEnabled](https://api.flutter.dev/flutter/rendering/debugProfileLayoutsEnabled.html): Adds`Timeline`events for every`RenderObject`layout.
- [debugProfilePaintsEnabled](https://api.flutter.dev/flutter/rendering/debugProfilePaintsEnabled.html): Adds`Timeline`events for every`RenderObject`painted.

`Timeline`
`Widget`
`Timeline`
`Widget`
`Timeline`
`RenderObject`
`Timeline`
`RenderObject`
## Instructions

1. *[Optional]*Set any desired tracing flags to true from your app's main method.
1. Run your Flutter web app in[profile mode](https://docs.flutter.dev/testing/build-modes#profile).
1. Open up the[Chrome DevTools Performance panel](https://developer.chrome.com/docs/devtools/performance)for your application,
                     and[start recording](https://developer.chrome.com/docs/devtools/performance/#record)to capture timeline events.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/web-performance.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/perf/web-performance&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/web-performance.md).
