> 原文链接: [https://docs.flutter.dev/tools/devtools/network](https://docs.flutter.dev/tools/devtools/network)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## What is it?

The network view allows you to inspect HTTP, HTTPS, and WebSocket traffic from
                  your Dart or Flutter application.

![Screenshot of the network screen](https://docs.flutter.dev/assets/images/docs/tools/devtools/network_screenshot.png)

## What network traffic is recorded?

All network traffic that originates from`dart:io`(like the[HttpClient](https://api.flutter.dev/dart-io/HttpClient-class.html)class) is logged, including the[dio](https://pub.dev/packages/dio)package. Also all network traffic that is logged using the[http_profile](https://pub.dev/packages/http_profile)package is recorded in the network request
                  table. This includes network traffic from the[cupertino_http](https://pub.dev/packages/cupertino_http),[cronet_http](https://pub.dev/packages/cronet_http), and[ok_http](https://pub.dev/packages/ok_http)packages.

`dart:io`
`HttpClient`
`dio`
`http_profile`
`cupertino_http`
`cronet_http`
`ok_http`
For a web app that makes requests using the browser, we recommend using browser
                  tools to inspect network traffic, such as[Chrome DevTools](https://developer.chrome.com/docs/devtools/network).

## How to use it

When you open the Network page, DevTools immediately starts recording network
                  traffic. To pause and resume recording, use the**Pause**and**Resume**buttons (upper left).

When a network request is sent by your app, it appears in the network
                  request table (left). It's listed as "Pending" until a complete response
                  is received.

Select a network request from the table (left) to view details (right). You can
                  inspect general and timing information about the request, as well as the content
                  of response and request headers and bodies. Some data is not available until
                  the response is received.

### Search and filtering

You can use the search and filter controls to find a specific request or filter
                  requests out of the request table.

![Screenshot of the network screen](https://docs.flutter.dev/assets/images/docs/tools/devtools/network_search_and_filter.png)

To apply a filter, press the filter button (right of the search bar). You will
                  see a filter dialog pop up:

![Screenshot of the network screen](https://docs.flutter.dev/assets/images/docs/tools/devtools/network_filter_dialog.png)

The filter query syntax is described in the dialog. You can filter network
                  requests by the following keys:

- `method`,`m`: this filter corresponds to the value in the "Method" column
- `status`,`s`: this filter corresponds to the value in the "Status" column
- `type`,`t`: this filter corresponds to the value in the "Type" column

`method`
`m`
`status`
`s`
`type`
`t`
Any text that is not paired with an available filter key will be queried against
                  all categories (method, URI, status, type).

Example filter queries:

`my-endpoint m:get t:json s:200`
`https s:404`
### Recording network requests on app startup

To record network traffic on app startup, you can start your app in a paused
                  state, and then begin recording network traffic in DevTools
                  before resuming your app.

1. Start your app in a paused state:
1. Open DevTools from the IDE where you started your app, or from the link that
                    was printed to the command line if you started your app from the CLI.
1. Navigate to the Network screen and ensure that recording has started.
1. Resume your app.![Screenshot of the app resumption experience on the Network screen](https://docs.flutter.dev/assets/images/docs/tools/devtools/network_startup_resume.png)
1. The Network profiler will now record all network traffic from your app,
                    including traffic from app startup.

- `flutter run --start-paused ...`
- `dart run --pause-isolates-on-start --observe ...`

`flutter run --start-paused ...`
`dart run --pause-isolates-on-start --observe ...`
## Other resources

HTTP and HTTPS requests are also surfaced in the[Timeline](https://docs.flutter.dev/tools/devtools/performance#timeline-events-tab)as
                  asynchronous timeline events. Viewing network activity in the timeline can be
                  useful if you want to see how HTTP traffic aligns with other events happening
                  in your app or in the Flutter framework.

`Timeline`
To learn how to monitor an app's network traffic and inspect
                  different types of requests using the DevTools,
                  check out a guided[Network View tutorial](https://medium.com/@fluttergems/mastering-dart-flutter-devtools-network-view-part-4-of-8-afce2463687c).
                  The tutorial also uses the view to identify network activity that
                  causes poor app performance.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/network.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/devtools/network&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/network.md).
