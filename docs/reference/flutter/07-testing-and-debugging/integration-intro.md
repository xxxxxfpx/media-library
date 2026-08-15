> 原文链接: [https://docs.flutter.dev/cookbook/testing/integration/introduction](https://docs.flutter.dev/cookbook/testing/integration/introduction)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Unit tests and widget tests validate individual classes,
                  functions, or widgets.
                  They don't validate how individual pieces work
                  together in whole or capture the performance
                  of an app running on a real device.
                  To perform these tasks, use*integration tests*.

Integration tests verify the behavior of the complete app.
                  This test can also be called end-to-end testing or GUI testing.

## Testing frameworks

Two packages are commonly used to perform Flutter integration tests.
                  These are:


[integration_test](https://github.com/flutter/flutter/tree/main/packages/integration_test)package: The official
                      integration test package that is part of the Flutter SDK. Tests written
                      with`integration_test`can perform the following tasks: run on the
                      target device, run from the host machine with`flutter test integration_test`,
                      and use`flutter_test`APIs. This makes integration tests similar to writing[widget tests](https://docs.flutter.dev/testing/overview#widget-tests). However,`integration_test`can't interact with
                      native platform UI.

`integration_test`
`flutter test integration_test`
`flutter_test`
`integration_test`
[patrol](https://pub.dev/packages/patrol)package: A popular third-party integration test package that
                      has many of the features supported by the`integration_test`package,
                      but can additionally interact with native platform UI such as
                      permission dialogs, notifications, or the contents of platform views.

`integration_test`
## Terminology

The system on which you develop your app, like a desktop computer.

The mobile device, browser, or desktop application that
                      runs your Flutter app.

If you run your app in a web browser or as a desktop application,
                      the host machine and the target device are the same.

## Getting started

To use`integration_test`, add it as a dependency for your
                  Flutter app test file.

`integration_test`
To migrate existing projects that use`flutter_driver`,
                  consult the[Migrating from flutter_driver](https://docs.flutter.dev/release/breaking-changes/flutter-driver-migration)guide.

`flutter_driver`
To use`patrol`, follow the[Patrol setup guide](https://patrol.leancode.co/getting-started).

`patrol`
## Use cases for integration testing

The other guides in this section explain how to use integration tests to validate[functionality](https://docs.flutter.dev/testing/integration-tests/)and[performance](https://docs.flutter.dev/cookbook/testing/integration/profiling/).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/testing/integration/introduction.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/testing/integration/introduction&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/testing/integration/introduction.md).
