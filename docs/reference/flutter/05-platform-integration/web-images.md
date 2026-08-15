> 原文链接: [https://docs.flutter.dev/platform-integration/web/web-images](https://docs.flutter.dev/platform-integration/web/web-images)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The web supports the standard[Image](https://api.flutter.dev/flutter/widgets/Image-class.html)widget and the more
                  advanced[dart:ui/Image](https://api.flutter.dev/flutter/dart-ui/Image-class.html)class (where more fine-grained control
                  is needed to display images).
                  However, because web browsers are built to run untrusted code safely,
                  there are certain limitations in what you can do with images compared
                  to mobile and desktop platforms. This page explains these limitations
                  and offers ways to work around them.

`Image`
`dart:ui/Image`
## Background

The web offers several methods for displaying images:

- The built-in[<img>](https://developer.mozilla.org/docs/Web/HTML/Element/img)and[<picture>](https://developer.mozilla.org/docs/Web/HTML/Element/picture)HTML elements
- The[drawImage](https://developer.mozilla.org/docs/Web/API/CanvasRenderingContext2D/drawImage)method on the[<canvas>](https://developer.mozilla.org/docs/Web/HTML/Element/canvas)element
- Custom image codec that renders to a WebGL canvas

`<img>`
`<picture>`
`drawImage`
`<canvas>`
Each option has its own benefits and drawbacks.
                  For example, the built-in elements fit nicely among
                  other HTML elements, and they automatically take
                  advantage of browser caching, and built-in image
                  optimization and memory management.
                  They allow you to safely display images from arbitrary sources
                  (more on than in the CORS section below).`drawImage`is great when the image must fit within
                  other content rendered using the`<canvas>`element.
                  You also gain control over image sizing and,
                  when the CORS policy allows it, read the pixels
                  of the image back for further processing.
                  Finally, WebGL gives you the highest degree of
                  control over the image. Not only can you read the pixels and
                  apply custom image algorithms, but you can also use GLSL for
                  hardware-acceleration.

`drawImage`
`<canvas>`
## Cross-Origin Resource Sharing (CORS)

[CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS)is a mechanism that browsers use to control how
                  one site accesses the resources of another site. It is
                  designed such that, by default, one web-site is not
                  allowed to make HTTP requests to another site using[XHR](https://developer.mozilla.org/docs/Web/API/XMLHttpRequest)or[fetch](https://developer.mozilla.org/docs/Web/API/Fetch_API/Using_Fetch).
                  This prevents scripts on another site from acting on
                  behalf of the user and from gaining access to another
                  site's resources without permission.

`fetch`
On the web, Flutter renders apps using the CanvasKit
                  or skwasm (when using Wasm) renderers. These both rely
                  on WebGL. WebGL requires access to the raw image data
                  (bytes) in order to be able to render the image.
                  Therefore, images must only come from servers that
                  have a CORS policy configured to work with the domain
                  that serves your application.

## Solutions

There are multiple solutions to workaround CORS restrictions
                  in Flutter.

### In-memory, asset, and same-origin network images

If the app has the bytes of the encoded image in memory,
                  provided as an[asset](https://docs.flutter.dev/ui/assets/assets-and-images), or stored on the
                  same server that serves the application
                  (also known as*same-origin*), no extra effort is necessary.
                  The image can be displayed using[Image.memory](https://api.flutter.dev/flutter/widgets/Image/Image.memory.html),[Image.asset](https://api.flutter.dev/flutter/widgets/Image/Image.asset.html), or[Image.network](https://api.flutter.dev/flutter/widgets/Image/Image.network.html).

`Image.memory`
`Image.asset`
`Image.network`
### Host images in a CORS-enabled CDN

Typically, content delivery networks (CDN)
                  can be configured to customize what domains
                  are allowed to access your content.
                  For example, Firebase site hosting allows[specifying a custom](https://firebase.google.com/docs/hosting/full-config#headers)`Access-Control-Allow-Origin`header in the`firebase.json`file.

`Access-Control-Allow-Origin`
`firebase.json`
### Use a CORS proxy if you have no control over the origin server

If the image server cannot be configured to allow CORS
                  requests from your application,
                  you might still be able to load images by proxying
                  the requests through another server. This requires that the
                  intermediate server has sufficient access to load the images.

This method can be used in situations when the original
                  image server serves images publicly,
                  but is not configured with the correct CORS headers.

Examples:

- Using[CloudFlare Workers](https://developers.cloudflare.com/workers/examples/cors-header-proxy).
- Using[Firebase Functions](https://github.com/7kfpun/cors-proxy).

### Use a HTML platform view

If none of the other solutions work for your app, Flutter
                  supports embedding raw HTML inside the app using[HtmlElementView](https://api.flutter.dev/flutter/widgets/HtmlElementView-class.html).  Use it to create an`<img>`element to render the image from another domain.

`HtmlElementView`
`<img>`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/web-images.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web/web-images&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/web-images.md).
