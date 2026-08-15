> 原文链接: [https://docs.flutter.dev/platform-integration/web/faq](https://docs.flutter.dev/platform-integration/web/faq)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Questions

### What scenarios are ideal for Flutter on the web?

Not every web page makes sense in Flutter,
                  but we think Flutter is particularly suited for app-centric experiences:

- Progressive Web Apps
- Single Page Apps
- Existing Flutter mobile apps

At this time, Flutter is not suitable for static websites with text-rich
                  flow-based content. For example, blog articles benefit from the document-centric
                  model that the web is built around, rather than the app-centric services that a
                  UI framework like Flutter can deliver. However, you*can*use Flutter to embed
                  interactive experiences into these websites.

For more information on how you can use Flutter on the web,
                  see[Web support for Flutter](https://docs.flutter.dev/platform-integration/web).

### Search Engine Optimization (SEO)

In general, Flutter is geared towards dynamic application experiences.
                  Flutter's web support is no exception.
                  Flutter web prioritizes performance, fidelity, and consistency.
                  This means application output doesn't align with what search
                  engines need to properly index.

However, a community-released Dart package,[Jaspr](https://jaspr.site/)*does*support static websites.
                  In fact, the[Dart documentation](https://dart.dev),[Flutter documentation](https://docs.flutter.dev/), and[Flutter marketing](https://flutter.dev)websites were migrated to using the Jaspr package.

To summarize, for web content that is static or document-like,
                  we recommend*either*using:

1. [Jaspr](https://jaspr.site/), if you want to use Dart but want a more traditional
                    DOM-based website. Also note that Jaspr makes SEO work in the
                    same way a traditional website would.
1. HTML—in this case, consider separating your primary application
                    experience (created in Flutter), from your landing page,
                    marketing content, and help content (created using
                    search engine optimized HTML).

### Does hot reload work with a web app?

Yes! For more information,
                  check out[hot reload on the web](https://docs.flutter.dev/platform-integration/web/building#hot-reload-web).

### Which web browsers are supported by Flutter?

Flutter web apps can run on the following browsers:

- Chrome (mobile & desktop)
- Safari (mobile & desktop)
- Edge (mobile & desktop)
- Firefox (mobile & desktop)

During development, Chrome (on macOS, Windows, and Linux),
                  and Edge (on Windows) are supported as the default browsers
                  for debugging your app.

### Can I build, run, and deploy web apps in any of the IDEs?

You can select**Chrome**or**Edge**as the target device in
                  Android Studio/IntelliJ and VS Code.

The device pulldown should now include the**Chrome (web)**option for all channels.

### How do I build a responsive app for the web?

See[Creating responsive apps](https://docs.flutter.dev/ui/adaptive-responsive).

### Can I usedart:iowith a web app?

`dart:io`
No. The file system is not accessible from the browser.
                  For network functionality, use the[http](https://pub.dev/packages/http)package. Note that security works somewhat
                  differently because the browser (and not the app)
                  controls the headers on an HTTP request.

`http`
### How do I handle web-specific imports?

Some plugins require platform-specific imports, particularly if they use the
                  file system, which is not accessible from the browser. To use these plugins
                  in your app, see the[documentation for conditional imports](https://dart.dev/guides/libraries/create-library-packages#conditionally-importing-and-exporting-library-files)on[dart.dev](https://dart.dev).

### Does Flutter web support concurrency?

Dart's concurrency support that uses[isolates](https://dart.dev/guides/language/concurrency)is not currently supported in Flutter web.

Flutter web apps can potentially work around this
                  by using[web workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers),
                  although such support isn't built in.

### How do I deploy a web app?

See[Preparing a web app for release](https://docs.flutter.dev/deployment/web).

### DoesPlatform.iswork on the web?

`Platform.is`
No. While you can technically import`dart:io`when compiling for the web,
                  calling any`Platform.isXYZ`method throws an`UnsupportedError`.
                  Furthermore, importing`dart:io`in a package
                  (except through conditional imports) causes pub.dev
                  to score the package as not supporting the web.

`dart:io`
`Platform.isXYZ`
`UnsupportedError`
`dart:io`
- If you are developing a Flutter app, consider using[kIsWeb](https://api.flutter.dev/flutter/foundation/kIsWeb-constant.html).
- If you are developing a package
                    (especially one without a Flutter dependency),
                    consider using the[os_detect](https://pub.dev/packages/os_detect)package.

`kIsWeb`
`os_detect`
### Why doesn't my app update immediately after it's deployed?

You might need to configure the`Cache-Control`header
                  returned by your web server.
                  For example, if this header is set to 3600,
                  then the browser and CDN will cache the asset for 1 hour,
                  and your users might see an out-of-date
                  version of your app up to 1 hour after you deploy a new version.
                  For more information about caching on the web, check out[Prevent unnecessary network requests with the HTTP Cache](https://web.dev/articles/http-cache).

`Cache-Control`
It's a good idea to be aware of this behavior to avoid an
                  undesirable user experience.
                  After you deploy your app, users might use a
                  cached version of your app (cached by the browser or CDN)
                  for the duration defined by your cache headers.
                  This can lead to using a version of your app that
                  is incompatible with changes that have been deployed
                  to backend services.

### How do I clear the web cache after a deployment and force an app download?

If you wish to defeat these cache headers after each deployment,
                  a common technique is to append a build ID of some sort to the links
                  of your static resources, or update the filenames themselves.
                  For example,`logo.png`might become`logo.v123.png`.

`logo.png`
`logo.v123.png`
`<!-- Option 1, append build ID as a query parameter in your links -->
<script src="flutter_bootstrap.js?v=123" async></script>
​
<!-- Option 2, update the filename and update your links -->
<script src="flutter_bootstrap.v123.js" async></script>`
Flutter doesn't currently support appending build IDs to resources
                  automatically.

### How do I configure my cache headers?

If you are using Firebase Hosting,
                  the shared cache (CDN) is invalidated when you deploy a
                  new version of your app.
                  However, to make sure that the browser doesn't
                  cache application scripts but the shared cache does,
                  you can configure your cache headers as follows,

`{
  "hosting": {
    "headers": [
      {
        "source":
          "**/*.@(jpg|jpeg|gif|png|svg|webp|css|eot|otf|ttf|ttc|woff|woff2|font.css)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=3600,s-maxage=604800"
          }
        ]
      },
      {
        "source":
          "**/*.@(mjs|js|wasm|json)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=0,s-maxage=604800"
          }
        ]
      }
    ]
  }
}`
### How do I configure a service worker?

The service worker generated by`flutter build web`is deprecated,
                  and you can disable it by setting the`--pwa-strategy`flag to`none`when running the`flutter build web`command.

`flutter build web`
`--pwa-strategy`
`none`
`flutter build web`
`flutter build web --pwa-strategy=none`
If you would like to continue to use a service worker, you can[build your own](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers)or try third-party tools
                  such as[Workbox](https://github.com/GoogleChrome/workbox).

If your service worker is not refreshing,
                  configure your CDN and browser cache by setting
                  the`Cache-Control`header to a small value such as 0 or 60 seconds.

`Cache-Control`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/faq.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web/faq&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/faq.md).
