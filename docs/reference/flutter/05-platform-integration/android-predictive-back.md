> 原文链接: [https://docs.flutter.dev/platform-integration/android/predictive-back](https://docs.flutter.dev/platform-integration/android/predictive-back)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This feature has landed in Flutter,
                  but it's not enabled by default in Android itself yet.
                  You can try it out using the following instructions.

## Configure your app

Make sure your app supports Android API 33 or higher,
                  as predictive back won't work on older versions of Android.
                  Then, set the flag`android:enableOnBackInvokedCallback="true"`in`android/app/src/main/AndroidManifest.xml`.

`android:enableOnBackInvokedCallback="true"`
`android/app/src/main/AndroidManifest.xml`
## Configure your device

You need to enable Developer Mode and set a flag on your device,
                  so you can't yet expect predictive back to work on most users'
                  Android devices. If you want to try it out on your own device though,
                  make sure it's running API 33 or higher, and then in**Settings => System => Developer**options,
                  make sure the switch is enabled next to**Predictive back animations**.

## Set up your app

The predictive back route transitions are currently
                  not enabled by default, so for now you'll need to enable them
                  manually in your app.
                  Typically, you do this by setting them in your theme:

`MaterialApp(
  theme: ThemeData(
    pageTransitionsTheme: const PageTransitionsTheme(
      builders: <TargetPlatform, PageTransitionsBuilder>{
        // Set the predictive back transitions for Android.
        TargetPlatform.android: PredictiveBackPageTransitionsBuilder(),
      },
    ),
  ),
  ...
),`
## Run your app

Lastly, just make sure you're using at least
                  Flutter version 3.22.2 to run your app,
                  which is the latest stable release at the time of this writing.

## For more information

You can find more information at the following link:

- [Android predictive back](https://docs.flutter.dev/release/breaking-changes/android-predictive-back)breaking change

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/android/predictive-back.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/android/predictive-back&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/android/predictive-back.md).
