> 原文链接: [https://docs.flutter.dev/tools/devtools](https://docs.flutter.dev/tools/devtools)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## What is DevTools?

DevTools is a suite of performance and debugging tools
                  for Dart and Flutter.*Flutter DevTools*and*Dart DevTools*refer to the
                  same set of tools.

![Dart DevTools Screens](https://docs.flutter.dev/assets/images/docs/tools/devtools/dart-devtools.webp)

For a video introduction to DevTools, check out
                  the following deep dive and use-case walkthrough:

## What can I do with DevTools?

Here are some of the things you can do with DevTools:

- Inspect the UI layout and state of a Flutter app.
- Diagnose UI jank performance issues in a Flutter app.
- CPU profiling for a Flutter or Dart app.
- Network profiling for a Flutter app.
- Source-level debugging of a Flutter or Dart app.
- Debug memory issues in a Flutter or Dart
                    command-line app.
- View general log and diagnostics information
                    about a running Flutter or Dart
                    command-line app.
- Analyze code and app size.
- Validate deep links in your Android or iOS app.

We expect you to use DevTools in conjunction with
                  your existing IDE or command-line based development workflow.

## How to launch DevTools

You can launch DevTools with the following tools:

- [VS Code](https://docs.flutter.dev/tools/devtools/vscode)
- [Android Studio/IntelliJ](https://docs.flutter.dev/tools/devtools/android-studio)
- [command line](https://docs.flutter.dev/tools/devtools/cli)

## Troubleshooting some standard issues

**Question**: My app looks janky or stutters.
                    How do I fix it?

**Answer**: Performance issues can cause[UI frames](https://docs.flutter.dev/perf/ui-performance)to be janky and/or slow down some operations.

1. To detect which code impacts concrete late frames,
                    start at[Performance > Timeline](https://docs.flutter.dev/tools/devtools/performance#timeline-events-tab).
1. To learn which code takes the most CPU time in
                    the background, use the[CPU profiler](https://docs.flutter.dev/tools/devtools/cpu-profiler).

For more information, check out the[Performance](https://docs.flutter.dev/perf)page.

**Question**: I see a lot of garbage collection (GC) events occurring.
                    Is this a problem?

**Answer**: Frequent GC events might display on
                    the DevTools > Memory > Memory chart. In most cases,
                    it's not a problem.

If your app has frequent background activity with some idle time,
                  Flutter might use that opportunity to collect the created objects
                  without performance impact.

## Providing feedback

Please give DevTools a try, provide feedback, and file issues
                  in the[DevTools issue tracker](https://github.com/flutter/devtools/issues). Thanks!

## DevTools versioning

DevTools is distributed as part of the Flutter SDK. To get access to the latest
                  DevTools functionality, run`flutter upgrade`to get the most up-to-date version
                  of Flutter. To access DevTools features before they hit the Flutter`stable`channel, consider switching to the`beta`or`main`channels.

`flutter upgrade`
`stable`
`beta`
`main`
## Other resources

For more information on debugging and profiling
                  Flutter apps, see the[Debugging](https://docs.flutter.dev/testing/debugging)page and,
                  in particular, its list of[other resources](https://docs.flutter.dev/testing/debugging#other-resources).

For more information on using DevTools with
                  Dart command-line apps, see the[DevTools documentation on dart.dev](https://dart.dev/tools/dart-devtools).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/index.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/devtools&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/index.md).
