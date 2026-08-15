> 原文链接: [https://docs.flutter.dev/add-to-app/android/plugin-setup](https://docs.flutter.dev/add-to-app/android/plugin-setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This guide describes how to set up your project to consume
                  plugins and how to manage your Gradle library dependencies
                  between your existing Android app and your Flutter module's plugins.

## A. Simple scenario

In the simple cases:

- Your Flutter module uses a plugin that has no additional
                    Android Gradle dependency because it only uses Android OS
                    APIs, such as the camera plugin.
- Your Flutter module uses a plugin that has an Android
                    Gradle dependency, such as[ExoPlayer from the video_player plugin](https://github.com/flutter/packages/blob/main/packages/video_player/video_player_android/android/build.gradle),
                    but your existing Android app didn't depend on ExoPlayer.

There are no additional steps needed. Your add-to-app
                  module will work the same way as a full-Flutter app.
                  Whether you integrate using Android Studio,
                  Gradle subproject or AARs,
                  transitive Android Gradle libraries are automatically
                  bundled as needed into your outer existing app.

## B. Plugins needing project edits

Some plugins require you to make some edits to the
                  Android side of your project.

For example, the integration instructions for the[firebase_crashlytics](https://pub.dev/packages/firebase_crashlytics)plugin require manual
                  edits to your Android wrapper project's`build.gradle`file.

`build.gradle`
For full-Flutter apps, these edits are done in your
                  Flutter project's`/android/`directory.

`/android/`
In the case of a Flutter module, there are only Dart
                  files in your module project. Perform those Android
                  Gradle file edits on your outer, existing Android
                  app rather than in your Flutter module.

## C. Merging libraries

The scenario that requires slightly more attention is if
                  your existing Android application already depends on the
                  same Android library that your Flutter module
                  does (transitively via a plugin).

For instance, your existing app's Gradle might already have:

- [Kotlin](#73-tab-panel)
- [Groovy](#74-tab-panel)

`…
dependencies {
    …
    implementation("com.crashlytics.sdk.android:crashlytics:2.10.1")
    …
}
…`
`…
dependencies {
    …
    implementation "com.crashlytics.sdk.android:crashlytics:2.10.1"
    …
}
…`
And your Flutter module also depends on[firebase_crashlytics](https://pub.dev/packages/firebase_crashlytics)via`pubspec.yaml`:

`pubspec.yaml`
`…
dependencies:
  …
  firebase_crashlytics: ^0.1.3
  …
…`
This plugin usage transitively adds a Gradle dependency again via
                  firebase_crashlytics v0.1.3's own[Gradle file](https://github.com/firebase/flutterfire/blob/bdb95fcacf7cf077d162d2f267eee54a8b0be3bc/packages/firebase_crashlytics/android/build.gradle#L40):

`…
dependencies {
    …
    implementation "com.crashlytics.sdk.android:crashlytics:2.9.9"
    …
}
…`
The two`com.crashlytics.sdk.android:crashlytics`dependencies
                  might not be the same version. In this example,
                  the host app requested v2.10.1 and the Flutter
                  module plugin requested v2.9.9.

`com.crashlytics.sdk.android:crashlytics`
By default, Gradle v5[resolves dependency version conflicts](https://docs.gradle.org/current/userguide/dependency_resolution.html#sub:resolution-strategy)by using the newest version of the library.

This is generally ok as long as there are no API
                  or implementation breaking changes between the versions.
                  For example, you might use the new Crashlytics library
                  in your existing app as follows:

- [Kotlin](#75-tab-panel)
- [Groovy](#76-tab-panel)

`…
dependencies {
    …
    implementation("com.crashlytics.sdk.android:crashlytics:2.10.1")
    …
}
…`
`…
dependencies {
    …
    implementation "com.google.firebase:firebase-crashlytics:17.0.0-beta03"
    …
}
…`
This approach won't work since there are major API differences
                  between the Crashlytics' Gradle library version
                  v17.0.0-beta03 and v2.9.9.

For Gradle libraries that follow semantic versioning,
                  you can generally avoid compilation and runtime errors
                  by using the same major semantic version in your
                  existing app and Flutter module plugin.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/plugin-setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/add-to-app/android/plugin-setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/plugin-setup.md).
