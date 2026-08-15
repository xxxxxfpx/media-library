> 原文链接: [https://docs.flutter.dev/platform-integration/web/setup](https://docs.flutter.dev/platform-integration/web/setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Learn how to set up your development environment
                  to run, build, and deploy Flutter apps for the web platform.

## Install a web browser

To run and debug your Flutter app on the web,[download and install Google Chrome](https://www.google.com/chrome/)or[install and use Microsoft Edge](https://www.microsoft.com/edge).

If you want to debug your app in other web browsers,
you can use the`flutter run -d web-server`command,
and manually navigate to the specified URL in your preferred browser.

`flutter run -d web-server`
Note that debugging support in the`web-server`mode is limited.

`web-server`
## Validate your setup

To ensure that you installed the browser successfully,
                  and that Flutter can find it,
                  run`flutter devices`in your preferred terminal.

`flutter devices`
You should at least see one connected device labeled**Chrome (web)**or**Edge (web)**, similar to the following:

`$ flutter devices

Found 1 connected devices:
  Chrome (web)    • chrome • web-javascript • Google Chrome`
If the command isn't found, or you don't see Chrome listed,
                  check out[Set up troubleshooting](https://docs.flutter.dev/install/troubleshoot).

## Start developing for the web

Now that you've set up web development for Flutter,
                  you can continue your Flutter learning journey while testing on the web
                  or begin expanding integration with the web.

- [Learn the fundamentals](https://docs.flutter.dev/learn/pathway)
- [Explore Flutter widgets](https://www.youtube.com/watch?v=b_sQ9bMltGU&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)
- [Check out samples](https://docs.flutter.dev/reference/learning-resources)

- [Build a web app with Flutter](https://docs.flutter.dev/platform-integration/web/building)
- [Customize app initialization](https://docs.flutter.dev/platform-integration/web/initialization)
- [Compile to Wasm](https://docs.flutter.dev/platform-integration/web/wasm)
- [Integrate web content](https://docs.flutter.dev/platform-integration/web/web-content-in-flutter)
- [Embed in another web app](https://docs.flutter.dev/platform-integration/web/embedding-flutter-web)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web/setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/setup.md).
