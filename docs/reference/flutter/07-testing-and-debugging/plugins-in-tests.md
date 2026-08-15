> 原文链接: [https://docs.flutter.dev/testing/plugins-in-tests](https://docs.flutter.dev/testing/plugins-in-tests)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Almost all[Flutter plugins](https://docs.flutter.dev/packages-and-plugins/using-packages)have two parts:

- Dart code, which provides the API your code calls.
- Code written in a platform-specific (or "host") language,
                    such as Kotlin or Swift, which implements those APIs.

In fact, the native (or host) language code distinguishes
                  a plugin package from a standard package.

Building and registering the host portion of a plugin
                  is part of the Flutter application build process,
                  so plugins only work when your code is running
                  in your application, such as with`flutter run`or when running[integration tests](https://docs.flutter.dev/cookbook/testing/integration/introduction).
                  When running[Dart unit tests](https://docs.flutter.dev/cookbook/testing/unit/introduction)or[widget tests](https://api.flutter.dev/flutter/flutter_test/flutter_test-library.html), the host code isn't available.
                  If the code you are testing calls any plugins,
                  this often results in errors like the following:

`flutter run`
`MissingPluginException(No implementation found for method someMethodName on channel some_channel_name)`
When unit testing code that uses plugins,
                  there are several options to avoid this exception.
                  The following solutions are listed in order of preference.

## Wrap the plugin

In most cases, the best approach is to wrap plugin
                  calls in your own API,
                  and provide a way of[mocking](https://docs.flutter.dev/cookbook/testing/unit/mocking)your own API in tests.

This has several advantages:

- If the plugin API changes,
                    you won't need to update your tests.
- You are only testing your own code,
                    so your tests can't fail due to behavior of
                    a plugin you're using.
- You can use the same approach regardless of
                    how the plugin is implemented,
                    or even for non-plugin package dependencies.

## Mock the plugin's public API

If the plugin's API is already based on class instances,
                  you can mock it directly, with the following caveats:

- This won't work if the plugin uses
                    non-class functions or static methods.
- Tests will need to be updated when
                    the plugin API changes.

## Mock the plugin's platform interface

If the plugin is a[federated plugin](https://docs.flutter.dev/packages-and-plugins/developing-packages#federated-plugins),
                  it will include a platform interface that allows
                  registering implementations of its internal logic.
                  You can register a mock of that platform interface
                  implementation instead of the public API with the
                  following caveats:

- This won't work if the plugin isn't federated.
- Your tests will include part of the plugin's code,
                    so plugin behavior could cause problems for your tests.
                    For instance, if a plugin writes files as part of an
                    internal cache, your test behavior might change
                    based on whether you had run the test previously.
- Tests might need to be updated when the platform interface changes.

An example of when this might be necessary is
                  mocking the implementation of a plugin used by
                  a package that you rely on,
                  rather than your own code,
                  so you can't change how it's called.
                  However, if possible,
                  you should mock the dependency that uses the plugin instead.

## Mock the platform channel

If the plugin uses[platform channels](https://docs.flutter.dev/platform-integration/platform-channels),
                  you can mock the platform channels using[TestDefaultBinaryMessenger](https://api.flutter.dev/flutter/flutter_test/TestDefaultBinaryMessenger-class.html).
                  This should only be used if, for some reason,
                  none of the methods above are available,
                  as it has several drawbacks:

`TestDefaultBinaryMessenger`
- Only implementations that use platform channels
                    can be mocked. This means that if some implementations
                    don't use platform channels,
                    your tests will unexpectedly use
                    real implementations when run on some platforms.
- Platform channels are usually internal implementation
                    details of plugins.
                    They might change substantially even
                    in a bugfix update to a plugin,
                    breaking your tests unexpectedly.
- Platform channels might differ in each implementation
                    of a federated plugin. For instance,
                    you might set up mock platform channels to
                    make tests pass on a Windows machine,
                    then find that they fail if run on macOS or Linux.
- Platform channels aren't strongly typed.
                    For example, method channels often use dictionaries
                    and you have to read the plugin's implementation
                    to know what the key strings and value types are.

Because of these limitations,`TestDefaultBinaryMessenger`is mainly useful in the internal tests
                  of plugin implementations,
                  rather than tests of code using plugins.

`TestDefaultBinaryMessenger`
You might also want to check out[Testing plugins](https://docs.flutter.dev/testing/testing-plugins).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/plugins-in-tests.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/testing/plugins-in-tests&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/testing/plugins-in-tests.md).
