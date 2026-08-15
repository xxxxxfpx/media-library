> 原文链接: [https://docs.flutter.dev/platform-integration/ios/restore-state-ios](https://docs.flutter.dev/platform-integration/ios/restore-state-ios)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

When a user runs a mobile app and then selects another
                  app to run, the first app is moved to the background,
                  or*backgrounded*. The operating system (both iOS and Android)
                  often kills the backgrounded app to release memory or
                  improve performance for the app running in the foreground.

You can use the[RestorationManager](https://api.flutter.dev/flutter/services/RestorationManager-class.html)(and related)
                  classes to handle state restoration.
                  An iOS app requires[a bit of extra setup](https://api.flutter.dev/flutter/services/RestorationManager-class.html#state-restoration-on-ios)in Xcode,
                  but the restoration classes otherwise work the same on
                  both iOS and Android.

`RestorationManager`
For more information, check out[State restoration on Android](https://docs.flutter.dev/platform-integration/android/restore-state-android).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/restore-state-ios.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/ios/restore-state-ios&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/restore-state-ios.md).
