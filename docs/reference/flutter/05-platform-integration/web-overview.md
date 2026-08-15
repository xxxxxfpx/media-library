> 原文链接: [https://docs.flutter.dev/platform-integration/web](https://docs.flutter.dev/platform-integration/web)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter delivers the same experiences on the web as on mobile.

Building on the portability of Dart, the power of the web platform,
                  the flexibility of the Flutter framework, and the performance of WebAssembly,
                  you can build apps for iOS, Android, and the browser from the same codebase.
                  The web is just another device target for your app.

To get started, visit[Building a web application with Flutter](https://docs.flutter.dev/platform-integration/web/building).

## Powered by WebAssembly

Dart and Flutter can compile to WebAssembly,
                  a binary instruction format that enables fast apps on all major browsers.

For a glimpse into the benefits of using WebAssembly,
                  check out the following video.

## How it works

Adding web support to Flutter involved implementing Flutter's
                  core drawing layer on top of standard browser APIs,
                  in addition to compiling Dart to JavaScript,
                  instead of the ARM machine code that
                  is used for mobile applications.
                  Using a combination of DOM, Canvas, and WebAssembly,
                  Flutter can provide a portable, high-quality,
                  and performant user experience across modern browsers.
                  We implemented the core drawing layer completely in Dart
                  and used Dart's optimized JavaScript compiler to compile the
                  Flutter core and framework along with your application into a single,
                  minified source file that can be deployed to any web server.

![Flutter architecture for web](https://docs.flutter.dev/assets/images/docs/arch-overview/web-framework-diagram.png)

## What types of apps can I build?

While you can do a lot on the web,
                  Flutter's web support is most valuable in the
                  following scenarios:

Flutter's web support enables complex standalone web apps that are rich with
                      graphics and interactive content to reach end users on a wide variety of
                      devices.

Web support for Flutter provides a browser-based delivery model for existing
                      Flutter mobile apps.

Not every HTML scenario is ideally suited for Flutter at this time.
                  For example, text-rich, flow-based, static content such as blog articles
                  benefit from the document-centric model that the web is built around,
                  rather than the app-centric services that a UI framework like Flutter
                  can deliver. However, you*can*use Flutter to embed interactive
                  experiences into these websites.

However, if you want to use Dart and wish to implement a traditional
                  DOM-based website, a community-released Dart package,[Jaspr](https://jaspr.site/), supports static websites; in fact,
                  the[Dart documentation](https://dart.dev)and[Flutter documentation](https://flutter.dev)and[marketing](https://flutter.dev)websites were migrated to use the Jaspr package.
                  Note that Jaspr uses Dart (but not Flutter), and makes SEO work in the same
                  way a traditional website would.

## Get started

The following resources can help you get started:

- To add web support to an existing app, or to create a
                    new app that includes web support,
                    visit[Building a web application with Flutter](https://docs.flutter.dev/platform-integration/web/building).
- To configure web development server settings in a centralized file,
                    check out[Set up a web development configuration file](https://docs.flutter.dev/platform-integration/web/web-dev-config-file).
- To learn about Flutter's different web renderers (CanvasKit and Skwasm),
                    check out[Web renderers](https://docs.flutter.dev/platform-integration/web/renderers).
- To learn how to create a responsive Flutter
                    app, check out[Creating responsive apps](https://docs.flutter.dev/ui/adaptive-responsive).
- To view commonly asked questions and answers,
                    visit the[web FAQ](https://docs.flutter.dev/platform-integration/web/faq).
- For code examples,
                    check out the[web samples for Flutter](https://github.com/flutter/samples/#?platform=web).
- For a Flutter web app demo, check out the[Wonderous app](https://wonderous.app//web).
- To learn about deploying a web app,
                    visit[Preparing an app for web release](https://docs.flutter.dev/deployment/web).
- [File an issue](https://goo.gle/flutter_web_issue)on the main Flutter repo.
- You can chat and ask web-related questions on the**#help**channel on[Discord](https://discordapp.com/invite/yeZ6s7k).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/index.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/index.md).
