> 原文链接: [https://docs.flutter.dev/testing/testing-plugins](https://docs.flutter.dev/testing/testing-plugins)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

All of the[usual types of Flutter tests](https://docs.flutter.dev/testing/overview)apply to
                  plugin packages as well, but because plugins contain
                  native code they often also require other kinds of tests
                  to test all of their functionality.

## Types of plugin tests

To see examples of each of these types of tests, you can[create a new plugin from the plugin template](https://docs.flutter.dev/packages-and-plugins/developing-packages#step-1-create-the-package-1)and look in the indicated directories.


**Dart**[unit tests](https://docs.flutter.dev/cookbook/testing/unit/introduction)and[widget tests](https://docs.flutter.dev/cookbook/testing/widget/introduction).
                      These tests allow you to test the Dart portion of your plugin
                      just as you would test the Dart code of a non-plugin package.
                      However, the plugin's native code[won't be loaded](https://docs.flutter.dev/testing/plugins-in-tests),
                      so any calls to platform channels need to be[mocked in tests](https://docs.flutter.dev/testing/plugins-in-tests#mock-the-platform-channel).

See the`test`directory for an example.

`test`
**Dart**[integration tests](https://docs.flutter.dev/cookbook/testing/integration/introduction).
                      Since integration tests run in the context of a
                      Flutter application (the example app),
                      they can test both the Dart and native code,
                      as well as the interaction between them.
                      They are also useful for unit testing web implementation
                      code that needs to run in a browser.

These are often the most important tests for a plugin.
                      However, Dart integration tests using`integration_test`can't
                      interact with native UI, such as native dialogs or the contents
                      of platform views. For native component interaction support,
                      consider using[patrol](https://pub.dev/packages/patrol)

`integration_test`
`patrol`
See the`example/integration_test`directory for an example.

`example/integration_test`
**Native unit tests.**Just as Dart unit tests can test the Dart portions
                      of a plugin in isolation, native unit tests can
                      test the native parts in isolation.
                      Each platform has its own native unit test system,
                      and the tests are written in the same native languages
                      as the code it is testing.

Native unit tests can be especially valuable
                      if you need to mock out APIs wrapped by your plugin code,
                      which isn't possible in a Dart integration test.

You can set up and use any native test frameworks
                      you are familiar with for each platform,
                      but the following are already configured in the plugin template:


**Android**:[JUnit](https://github.com/junit-team/junit4/wiki/Getting-started)tests can be found in`android/src/test/`.

`android/src/test/`
**iOS**and**macOS**:[XCTest](https://developer.apple.com/documentation/xctest)tests can be found in`example/ios/RunnerTests/`and`example/macos/RunnerTests/`respectively.
                          These are in the example directory,
                          not the top-level package directory,
                          because they are run via the example app's project.

`example/ios/RunnerTests/`
`example/macos/RunnerTests/`
**Linux**and**Windows**:[GoogleTest](https://github.com/google/googletest)tests can be found in`linux/test/`and`windows/test/`, respectively.

`linux/test/`
`windows/test/`
Other types of tests, which aren't currently pre-configured
                  in the template, are**native UI tests**.
                  Running your application under a native UI testing framework,
                  such as[Espresso](https://github.com/flutter/packages/tree/main/packages/espresso)or[XCUITest](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/testing_with_xcode/chapters/09-ui_testing.html),
                  enables tests that interact with both native and Flutter UI elements,
                  so can be useful if your plugin can't be tested without
                  native UI interactions.

## Running tests

### Dart unit tests

These can be run like any other Flutter unit tests,
                  either from your preferred Flutter IDE,
                  or using`flutter test`.

`flutter test`
### Integration tests

For information on running this type of test, check out the[integration test documentation](https://docs.flutter.dev/cookbook/testing/integration/introduction).
                  The commands must be run in the`example`directory.

`example`
### Native unit tests

For all platforms, you need to build the example
                  application at least once before running the unit tests,
                  to ensure that all of the platform-specific build
                  files have been created.

**Android JUnit**


If you have the example opened as an Android project
                  in Android Studio, you can run the unit tests using
                  the[Android Studio test UI](https://developer.android.com/studio/test/test-in-android-studio).

To run the tests from the command line,
                  use the following command in the`example/android`directory:

`example/android`
`./gradlew testDebugUnitTest`
**iOS and macOS XCTest**


If you have the example app opened in Xcode,
                  you can run the unit tests using the[Xcode Test UI](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/testing_with_xcode/chapters/05-running_tests.html).

To run the tests from the command line,
                  use the following command in the`example/ios`(for iOS)
                  or`example/macos`(for macOS) directory:

`example/ios`
`example/macos`
`xcodebuild test -workspace Runner.xcworkspace -scheme Runner -configuration Debug`
For iOS tests, you might need to first open`Runner.xcworkspace`in Xcode to configure code signing.

`Runner.xcworkspace`
**Linux GoogleTest**


To run the tests from the command line,
                  use the following command in the example directory,
                  replacing "my_plugin" with your plugin project name:

`build/linux/plugins/x64/debug/my_plugin/my_plugin_test`
If you built the example app in release mode rather than
                  debug, replace "debug" with "release".

**Windows GoogleTest**


If you have the example app opened in Visual Studio,
                  you can run the unit tests using the[Visual Studio test UI](https://learn.microsoft.com/en-us/visualstudio/test/getting-started-with-unit-testing?view=vs-2022&tabs=dotnet%2Cmstest#run-unit-tests).

To run the tests from the command line,
                  use the following command in the example directory,
                  replacing "my_plugin" with your plugin project name:

`build/windows/plugins/my_plugin/Debug/my_plugin_test.exe`
If you built the example app in release mode rather
                  than debug, replace "Debug" with "Release".

## What types of tests to add

The[general advice for testing Flutter projects](https://docs.flutter.dev/testing/overview)applies to plugins as well.
                  Some extra considerations for plugin testing:


Since only integration tests can test the communication
                      between Dart and the native languages,
                      try to have at least one integration test of each
                      platform channel call.

If some flows can't be tested using the`integration_test`package
                      (for example if they require interacting with native UI or mocking
                      device state), consider using the[patrol](https://pub.dev/packages/patrol)package for
                      native UI interactions, or writing "end to end" tests of the two halves
                      using unit tests:

`integration_test`
`patrol`

Native unit tests that set up the necessary mocks,
                          then call into the method channel entry point
                          with a synthesized call and validate the method response.

Dart unit tests that mock the platform channel,
                          then call the plugin's public API and validate the results.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/testing-plugins.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/testing/testing-plugins&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/testing-plugins.md).
