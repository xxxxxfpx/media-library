> 原文链接: [https://docs.flutter.dev/platform-integration/web/web-content-in-flutter](https://docs.flutter.dev/platform-integration/web/web-content-in-flutter)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

In some cases, Flutter web applications need to embed web content not
                  rendered by Flutter. For example, embedding a`google_maps_flutter`view
                  (which uses the Google Maps JavaScript SDK) or a`video_player`(which uses a standard`video`element).

`google_maps_flutter`
`video_player`
`video`
Flutter web can render arbitrary web content within the boundaries of a`Widget`,
                  and the primitives used to implement the example packages mentioned previously,
                  are available to all Flutter web applications.

`Widget`
## HtmlElementView

`HtmlElementView`
The`HtmlElementView`Flutter widget reserves a space in the layout to be
                  filled with any HTML Element. It has two constructors:

`HtmlElementView`
- `HtmlElementView.fromTagName`.
- `HtmlElementView`and`registerViewFactory`.

`HtmlElementView.fromTagName`
`HtmlElementView`
`registerViewFactory`
### HtmlElementView.fromTagName

`HtmlElementView.fromTagName`
The[HtmlElementView.fromTagNameconstructor](https://api.flutter.dev/flutter/widgets/HtmlElementView/HtmlElementView.fromTagName.html)creates an HTML Element from
                  its`tagName`, and provides an`onElementCreated`method to configure that
                  element before it's injected into the DOM:

`HtmlElementView.fromTagName`
`tagName`
`onElementCreated`
`// Create a `video` tag, and set its `src` and some `style` properties...
HtmlElementView.fromTag('video', onElementCreated: (Object video) {
  video as web.HTMLVideoElement;
  video.src = 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4';
  video.style.width = '100%';
  video.style.height = '100%';
  // other customizations to the element...
});`
To learn more about the way to interact with DOM APIs,
                  check out the[HTMLVideoElementclass](https://pub.dev/documentation/web/latest/web/HTMLVideoElement-extension-type.html)in[package:web](https://pub.dev/packages/web).

`HTMLVideoElement`
`package:web`
To learn more about the video`Object`that is cast to`web.HTMLVideoElement`,
                  check out Dart's[JS Interoperability](https://dart.dev/interop/js-interop)documentation.

`Object`
`web.HTMLVideoElement`
### HtmlElementViewandregisterViewFactory

`HtmlElementView`
`registerViewFactory`
If you need more control over generating the HTML code you inject, you can use
                  the primitives that Flutter uses to implement the`fromTagName`constructor. In
                  this scenario, register your own HTML Element factory for each type of HTML
                  content that needs to be added to your app.

`fromTagName`
The resulting code is more verbose, and has two steps per platform view type:

1. Register the HTML Element Factory using`platformViewRegistry.registerViewFactory`provided by`dart:ui_web.`
1. Place the widget with the desired`viewType`with`HtmlElementView('viewType')`in your app's widget tree.

`platformViewRegistry.registerViewFactory`
`dart:ui_web.`
`viewType`
`HtmlElementView('viewType')`
For more details about this approach, check out[HtmlElementViewwidget](https://api.flutter.dev/flutter/widgets/HtmlElementView-class.html)docs.

`HtmlElementView`
## package:webview_flutter

`package:webview_flutter`
Embedding a full HTML page inside a Flutter app is such a common feature, that
                  the Flutter team offers a plugin to do so:

- [package:webview_flutter](https://pub.dev/packages/webview_flutter)

`package:webview_flutter`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/web-content-in-flutter.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web/web-content-in-flutter&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/web-content-in-flutter.md).
