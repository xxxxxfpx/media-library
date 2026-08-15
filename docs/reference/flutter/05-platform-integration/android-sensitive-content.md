> 原文链接: [https://docs.flutter.dev/platform-integration/android/sensitive-content](https://docs.flutter.dev/platform-integration/android/sensitive-content)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The[SensitiveContent](https://api.flutter.dev/flutter/widgets/SensitiveContent-class.html)widget allows you to prevent
                  screens that contain sensitive content (such as passwords)
                  from being projected. To learn more,
                  check out the following two-minute Widget of the Week video:

`SensitiveContent`
## About theSensitiveContentwidget

`SensitiveContent`
You can use the`SensitiveContent`widget in your app to set the content
                  sensitivity of a child`Widget`to one of the following[ContentSensitivity](https://api.flutter.dev/flutter/services/ContentSensitivity.html)values:`notSensitive`,`sensitive`, or`autoSensitive`.
                  Your chosen mode determines if the device screen should be obscured
                  (blacked out) during media projection to protect sensitive data.

`SensitiveContent`
`Widget`
`ContentSensitivity`
`notSensitive`
`sensitive`
`autoSensitive`
You can have as many`SensitiveContent`widgets in your app as you wish,
                  but if*any*one of those widgets has a`sensitive`content value, then the
                  entire screen is obscured during media projection. Thus, for most use cases,
                  using multiple`SensitiveContent`widgets provides no advantage over having
                  one`SensitiveContent`widget in your app’s widget tree.

`SensitiveContent`
`sensitive`
`SensitiveContent`
`SensitiveContent`
This feature is available on Android API 35+
                  and has no effect on lower API versions or other platforms.

## Using theSensitiveContentwidget

`SensitiveContent`
Given some content that you want to protect from media screen share
                  (for example, a`MySensitiveContent()`widget), you can wrap it with the`SensitiveContent`widget as shown in the following example:

`MySensitiveContent()`
`SensitiveContent`
`class MyWidget extends StatelessWidget {
  ...
  Widget build(BuildContext context) {
    return SensitiveContent(
      sensitivity: ContentSensitivity.sensitive,
      child: MySensitiveContent(),
    );
  }
}`
When running on Android API 34 and below, the screen won't be obscured
                  during media projection. The widget will exist in the tree but has no other
                  effect, and you don't need to avoid usages of`SensitiveContent`on platforms
                  that don't support this feature.

`SensitiveContent`
## For more information

For more information, visit the[SensitiveContent](https://api.flutter.dev/flutter/widgets/SensitiveContent-class.html)and[ContentSensitivity](https://api.flutter.dev/flutter/services/ContentSensitivity.html)API docs.

`SensitiveContent`
`ContentSensitivity`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/android/sensitive-content.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/android/sensitive-content&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/android/sensitive-content.md).
