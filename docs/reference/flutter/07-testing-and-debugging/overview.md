> 原文链接: [https://docs.flutter.dev/testing/overview](https://docs.flutter.dev/testing/overview)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The more features your app has, the harder it is to test manually.
                  Automated tests help ensure that your app performs correctly before
                  you publish it, while retaining your feature and bug fix velocity.

Automated testing falls into a few categories:

- A[unit test](#unit-tests)tests a single function, method, or class.
- A[widget test](#widget-tests)(in other UI frameworks referred to
                    as*component test*) tests a single widget.
- An[integration test](#integration-tests)tests a complete app or a large part of an app.

Generally speaking, a well-tested app has many unit and widget tests,
                  tracked by[code coverage](https://en.wikipedia.org/wiki/Code_coverage), plus enough integration tests
                  to cover all the important use cases. This advice is based on
                  the fact that there are trade-offs between different kinds of testing,
                  seen below.

| Tradeoff | Unit | Widget | Integration |
| --- | --- | --- | --- |
| Confidence | Low | Higher | Highest |
| Maintenance cost | Low | Higher | Highest |
| Dependencies | Few | More | Most |
| Execution speed | Quick | Quick | Slow |

## Unit tests

A*unit test*tests a single function, method, or class.
                  The goal of a unit test is to verify the correctness of a
                  unit of logic under a variety of conditions.
                  External dependencies of the unit under test are generally[mocked out](https://docs.flutter.dev/cookbook/testing/unit/mocking).
                  Unit tests generally don't read from or write
                  to disk, render to screen, or receive user actions from
                  outside the process running the test.
                  For more information regarding unit tests,
                  you can view the following recipes
                  or run`flutter test --help`in your terminal.

`flutter test --help`
### Recipes

- [Introduction to unit testing](https://docs.flutter.dev/cookbook/testing/unit/introduction)
- [Mock dependencies using Mockito](https://docs.flutter.dev/cookbook/testing/unit/mocking)

## Widget tests

A*widget test*(in other UI frameworks referred to as*component test*)
                  tests a single widget. The goal of a widget test is to verify that the
                  widget's UI looks and interacts as expected. Testing a widget involves
                  multiple classes and requires a test environment that provides the
                  appropriate widget lifecycle context.

For example, the Widget being tested should be able to receive and
                  respond to user actions and events, perform layout, and instantiate child
                  widgets. A widget test is therefore more comprehensive than a unit test.
                  However, like a unit test, a widget test's environment is replaced with
                  an implementation much simpler than a full-blown UI system.

### Recipes

- [Introduction to widget testing](https://docs.flutter.dev/cookbook/testing/widget/introduction)
- [Find widgets using finders](https://docs.flutter.dev/cookbook/testing/widget/finders)
- [Handling scrolling in widget tests](https://docs.flutter.dev/cookbook/testing/widget/scrolling)
- [Tap, drag, and enter text in widget tests](https://docs.flutter.dev/cookbook/testing/widget/tap-drag)
- [Test different orientations](https://docs.flutter.dev/cookbook/testing/widget/orientation)

## Integration tests

An*integration test*tests a complete app or a large part of an app.
                  The goal of an integration test is to verify that all the widgets
                  and services being tested work together as expected.
                  Furthermore, you can use integration
                  tests to verify your app's performance.

Generally, an*integration test*runs on a real device or an OS emulator,
                  such as iOS Simulator or Android Emulator.
                  The app under test is typically isolated
                  from the test driver code to avoid skewing the results.

The Flutter SDK includes the[integration_test](https://github.com/flutter/flutter/tree/main/packages/integration_test)package.
                  However, this package can't interact with native platform UI,
                  such as permission dialogs, notifications, or platform views.
                  For apps that need native interactions, you can use the[patrol](https://pub.dev/packages/patrol)package, an open-source framework that extends
                  Flutter's testing capabilities with native platform support.

`integration_test`
`patrol`
For more information on how to write integration tests, see the[integration
                    testing page](https://docs.flutter.dev/cookbook/testing/integration/introduction).

### Recipes

- [Integration testing concepts](https://docs.flutter.dev/cookbook/testing/integration/introduction)
- [Write and run a Flutter integration test](https://docs.flutter.dev/testing/integration-tests)
- [Write and run a Patrol integration test](https://patrol.leancode.co/documentation/write-your-first-test)
- [Measure performance with an integration test](https://docs.flutter.dev/cookbook/testing/integration/profiling)

## Continuous integration services

Continuous integration (CI) services allow you to run your
                  tests automatically when pushing new code changes.
                  This provides timely feedback on whether the code
                  changes work as expected and do not introduce bugs.

For information on running tests on various continuous
                  integration services, see the following:

- [Continuous delivery using fastlane with Flutter](https://docs.flutter.dev/deployment/cd#fastlane)
- [Test Flutter apps on Appcircle](https://blog.appcircle.io/article/flutter-ci-cd-github-ios-android-web#)
- [Test Flutter apps on Travis](https://blog.flutter.dev/test-flutter-apps-on-travis-3fd5142ecd8c)
- [Test Flutter apps on Cirrus](https://cirrus-ci.org/examples/#flutter)
- [Codemagic CI/CD for Flutter](https://blog.codemagic.io/getting-started-with-codemagic/)
- [Codemagic CI/CD for Patrol](https://docs.codemagic.io/integrations/patrol-integration/)
- [Flutter CI/CD with Bitrise](https://devcenter.bitrise.io/en/getting-started/quick-start-guides/getting-started-with-flutter-apps)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/overview.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/testing/overview&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/overview.md).
