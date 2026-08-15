> 原文链接: [https://docs.flutter.dev/data-and-backend/networking](https://docs.flutter.dev/data-and-backend/networking)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Cross-platform http networking

The[http](https://pub.dev/packages/http)package provides the simplest way to issue http requests. This
                  package is supported on Android, iOS, macOS, Windows, Linux and the web.

`http`
## Platform notes

Some platforms require additional steps, as detailed below.

### Android

Android apps must[declare their use of the internet](https://developer.android.com/training/basics/network-ops/connecting)in the Android
                  manifest (`AndroidManifest.xml`):

`AndroidManifest.xml`
`<manifest xmlns:android...>
 ...
 <uses-permission android:name="android.permission.INTERNET" />
 <application ...
</manifest>`
### macOS

macOS apps must allow network access in the relevant`*.entitlements`files.

`*.entitlements`
`<key>com.apple.security.network.client</key>
<true/>`
Learn more about[setting up entitlements](https://docs.flutter.dev/platform-integration/macos/building#setting-up-entitlements).

## Samples

For a practical sample of various networking tasks (incl. fetching data,
                  WebSockets, and parsing data in the background) see the[networking cookbook recipes](https://docs.flutter.dev/cookbook/networking).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/data-and-backend/networking.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/data-and-backend/networking&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/data-and-backend/networking.md).
