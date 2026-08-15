> 原文链接: [https://docs.flutter.dev/cookbook/maintenance/error-reporting](https://docs.flutter.dev/cookbook/maintenance/error-reporting)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

While one always tries to create apps that are free of bugs,
                  they're sure to crop up from time to time.
                  Since buggy apps lead to unhappy users and customers,
                  it's important to understand how often your users
                  experience bugs and where those bugs occur.
                  That way, you can prioritize the bugs with the
                  highest impact and work to fix them.

How can you determine how often your users experiences bugs?
                  Whenever an error occurs, create a report containing the
                  error that occurred and the associated stacktrace.
                  You can then send the report to an error tracking
                  service, such as[Bugsnag](https://www.bugsnag.com/platforms/flutter),[Datadog](https://docs.datadoghq.com/real_user_monitoring/flutter/),[Firebase Crashlytics](https://firebase.google.com/docs/crashlytics),[Rollbar](https://rollbar.com/), or Sentry.

The error tracking service aggregates all of the crashes your users
                  experience and groups them together. This allows you to know how often your
                  app fails and where the users run into trouble.

In this recipe, learn how to report errors to the[Sentry](https://sentry.io/welcome/)crash reporting service using
                  the following steps:

1. Get a DSN from Sentry.
1. Import the Flutter Sentry package
1. Initialize the Sentry SDK
1. Capture errors programmatically

## 1. Get a DSN from Sentry

Before reporting errors to Sentry, you need a "DSN" to uniquely identify
                  your app with the Sentry.io service.

To get a DSN, use the following steps:

1. [Create an account with Sentry](https://sentry.io/signup/).
1. Log in to the account.
1. Create a new Flutter project.
1. Copy the code snippet that includes the DSN.

## 2. Import the Sentry package

Import the[sentry_flutter](https://pub.dev/packages/sentry_flutter)package into the app.
                  The sentry package makes it easier to send
                  error reports to the Sentry error tracking service.

`sentry_flutter`
To add the`sentry_flutter`package as a dependency,
                  run`flutter pub add`:

`sentry_flutter`
`flutter pub add`
`$ flutter pub add sentry_flutter`
## 3. Initialize the Sentry SDK

Initialize the SDK to capture different unhandled errors automatically:

`import 'package:flutter/widgets.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
​
Future<void> main() async {
  await SentryFlutter.init(
    (options) => options.dsn = 'https://example@sentry.io/example',
    appRunner: () => runApp(const MyApp()),
  );
}`
Alternatively, you can pass the DSN to Flutter using the`dart-define`tag:

`dart-define`
`--dart-define SENTRY_DSN=https://example@sentry.io/example`
### What does that give me?

This is all you need for Sentry to
                  capture unhandled errors in Dart and native layers.
                  This includes Swift, Objective-C, C, and C++ on iOS, and
                  Java, Kotlin, C, and C++ on Android.

## 4. Capture errors programmatically

Besides the automatic error reporting that Sentry generates by
                  importing and initializing the SDK,
                  you can use the API to report errors to Sentry:

`await Sentry.captureException(exception, stackTrace: stackTrace);`
For more information, see the[Sentry API](https://pub.dev/documentation/sentry_flutter/latest/sentry_flutter/sentry_flutter-library.html)docs on pub.dev.

## Learn more

Extensive documentation about using the Sentry SDK can be found on[Sentry's site](https://docs.sentry.io/platforms/flutter/).

## Complete example

To view a working example,
                  see the[Sentry flutter example](https://github.com/getsentry/sentry-dart/tree/main/flutter/example)app.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/maintenance/error-reporting.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/maintenance/error-reporting&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/maintenance/error-reporting.md).
