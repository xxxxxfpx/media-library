> 原文链接: [https://docs.flutter.dev/packages-and-plugins/using-packages](https://docs.flutter.dev/packages-and-plugins/using-packages)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter supports using shared packages contributed by other developers
                  to the Flutter and Dart ecosystems. This allows quickly building
                  an app without having to develop everything from scratch.

Existing packages enable many use cases—for example,
                  making network requests ([http](https://docs.flutter.dev/cookbook/networking/fetch-data)),
                  navigation/route handling ([go_router](https://pub.dev/packages/go_router)),
                  integration with device APIs
                  ([url_launcher](https://pub.dev/packages/url_launcher)and[battery_plus](https://pub.dev/packages/battery_plus)),
                  and using third-party platform SDKs like Firebase
                  ([FlutterFire](https://github.com/firebase/flutterfire)).

`http`
`go_router`
`url_launcher`
`battery_plus`
To write a new package, see[developing packages](https://docs.flutter.dev/packages-and-plugins/developing-packages).
                  To add assets, images, or fonts,
                  whether stored in files or packages,
                  see[Adding assets and images](https://docs.flutter.dev/ui/assets/assets-and-images).

## Using packages

The following section describes how to use
                  existing published packages.

### Searching for packages

Packages are published to[pub.dev](https://pub.dev).

The[Flutter landing page](https://pub.dev/flutter)on pub.dev displays
                  top packages that are compatible with Flutter
                  (those that declare dependencies generally compatible with Flutter),
                  and supports searching among all published packages.

The[Flutter Favorites](https://pub.dev/flutter/favorites)page on pub.dev lists
                  the plugins and packages that have been identified as
                  packages you should first consider using when writing
                  your app. For more information on what it means to
                  be a Flutter Favorite, see the[Flutter Favorites program](https://docs.flutter.dev/packages-and-plugins/favorites).

You can also browse the packages on pub.dev by filtering
                  on[Android](https://pub.dev/packages?q=sdk%3Aflutter+platform%3Aandroid),[iOS](https://pub.dev/packages?q=sdk%3Aflutter+platform%3Aios),[web](https://pub.dev/packages?q=sdk%3Aflutter+platform%3Aweb),[Linux](?q=sdk%3Aflutter+platform%3Alinux),[Windows](https://pub.dev/packages?q=sdk%3Aflutter+platform%3Awindows),[macOS](https://pub.dev/packages?q=sdk%3Aflutter+platform%3Amacos),
                  or any combination thereof.

### Adding a package dependency to an app usingflutter pub add

`flutter pub add`
To add the package`english_words`to an app:

`english_words`

Use the[pub add](https://dart.dev/tools/pub/cmd/pub-add)command from inside the project directory

`pub add`
- `flutter pub add english_words`

`flutter pub add english_words`
Import it

- Add a corresponding`import`statement in the Dart code.

`import`
Stop and restart the app, if necessary

- If the package brings platform-specific code
                        (Kotlin/Java for Android, Swift/Objective-C for iOS),
                        that code must be built into your app.
                        Hot reload and hot restart only update the Dart code,
                        so a full restart of the app might be required to avoid
                        errors like`MissingPluginException`when using the package.

`MissingPluginException`
### Adding a package dependency to an app

To add the package`english_words`to an app:

`english_words`

Depend on it

- Open the`pubspec.yaml`file located inside the app folder,
                        and add`english_words: ^4.0.0`under`dependencies`.

`pubspec.yaml`
`english_words: ^4.0.0`
`dependencies`
Install it

- From the terminal: Run`flutter pub get`.
**OR**
- From VS Code: Click**Get Packages**located in right side of the action
                        ribbon at the top of`pubspec.yaml`indicated by the Download icon.
- From Android Studio/IntelliJ: Click**Pub get**in the action
                        ribbon at the top of`pubspec.yaml`.

`flutter pub get`
`pubspec.yaml`
`pubspec.yaml`
Import it

- Add a corresponding`import`statement in the Dart code.

`import`
Stop and restart the app, if necessary

- If the package brings platform-specific code
                        (Kotlin/Java for Android, Swift/Objective-C for iOS),
                        that code must be built into your app.
                        Hot reload and hot restart only update the Dart code,
                        so a full restart of the app might be required to avoid
                        errors like`MissingPluginException`when using the package.

`MissingPluginException`
### Removing a package dependency from an app usingflutter pub remove

`flutter pub remove`
To remove the package`english_words`from an app:

`english_words`
1. Use the[pub remove](https://dart.dev/tools/pub/cmd/pub-remove)command from inside the project directory

`pub remove`
- `flutter pub remove english_words`

`flutter pub remove english_words`
The[Installing tab](https://pub.dev/packages/english_words/install),
                  available on any package page on pub.dev,
                  is a handy reference for these steps.

For a complete example,
                  see the[english_words example](#english-words-example)below.

### Conflict resolution

Suppose you want to use`some_package`and`another_package`in an app,
                  and both of these depend on`url_launcher`,
                  but in different versions.
                  That causes a potential conflict.
                  The best way to avoid this is for package authors to use[version ranges](https://dart.dev/tools/pub/dependencies#version-constraints)rather than specific versions when
                  specifying dependencies.

`some_package`
`another_package`
`url_launcher`
`dependencies:
  url_launcher: ^5.4.0    # Good, any version >= 5.4.0 but < 6.0.0
  image_picker: '5.4.3'   # Not so good, only version 5.4.3 works.`
If`some_package`declares the dependencies above
                  and`another_package`declares a compatible`url_launcher`dependency like`'5.4.6'`or`^5.5.0`, pub resolves the issue automatically.
                  Platform-specific dependencies on[Gradle modules](https://docs.gradle.org/current/userguide/declaring_dependencies.html)and/or[CocoaPods](https://guides.cocoapods.org/syntax/podspec.html#dependency)are solved in a similar way.

`some_package`
`another_package`
`url_launcher`
`'5.4.6'`
`^5.5.0`
Even if`some_package`and`another_package`declare incompatible versions for`url_launcher`,
                  they might actually use`url_launcher`in
                  compatible ways. In this situation,
                  the conflict can be resolved by adding
                  a dependency override declaration to the app's`pubspec.yaml`file, forcing the use of a particular version.

`some_package`
`another_package`
`url_launcher`
`url_launcher`
`pubspec.yaml`
For example, to force the use of`url_launcher`version`5.4.0`,
                  make the following changes to the app's`pubspec.yaml`file:

`url_launcher`
`5.4.0`
`pubspec.yaml`
`dependencies:
  some_package:
  another_package:
dependency_overrides:
  url_launcher: '5.4.0'`
If the conflicting dependency is not itself a package,
                  but an Android-specific library like`guava`,
                  the dependency override declaration must be added to
                  Gradle build logic instead.

`guava`
To force the use of`guava`version`28.0`, make the following
                  changes to the app's`android/build.gradle`file:

`guava`
`28.0`
`android/build.gradle`
- [Kotlin](#16-tab-panel)
- [Groovy](#17-tab-panel)

`configurations.all {
    resolutionStrategy {
        force("com.google.guava:guava:28.0-android")
    }
}`
`configurations.all {
    resolutionStrategy {
        force 'com.google.guava:guava:28.0-android'
    }
}`
CocoaPods doesn't currently offer dependency
                  override functionality.

## Developing new packages

If no package exists for your specific use case,
                  you can[write a custom package](https://docs.flutter.dev/packages-and-plugins/developing-packages).

## Managing package dependencies and versions

To minimize the risk of version collisions,
                  specify a version range in the`pubspec.yaml`file.

`pubspec.yaml`
### Package versions

All packages have a version number, specified in the
                  package's`pubspec.yaml`file. The current version of a package
                  is displayed next to its name (for example,
                  see the[url_launcher](https://pub.dev/packages/url_launcher)package), as
                  well as a list of all prior versions
                  (see[url_launcherversions](https://pub.dev/packages/url_launcher/versions)).

`pubspec.yaml`
`url_launcher`
`url_launcher`
To ensure that the app doesn't break when you update a package,
                  specify a version range using one of the following formats.

- yaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
- yaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

**Ranged constraints:**Specify a minimum and maximum version.

`dependencies:
  url_launcher: '>=5.4.0 <6.0.0'`
**Ranged constraints using thecaret syntax:**Specify the version that serves as the inclusive minimum version.
                      This covers all versions from that version to the next major version.

`dependencies:
  collection: '^5.4.0'`
This syntax means the same as the one noted in the first bullet.

To learn more, check out the[package versioning guide](https://dart.dev/tools/pub/versioning).

### Updating package dependencies

When running`flutter pub get`for the first time after adding a package,
                  Flutter saves the concrete package version found in the`pubspec.lock`[lockfile](https://dart.dev/tools/pub/glossary#lockfile). This ensures that you get the same version again
                  if you, or another developer on your team, run`flutter pub get`.

`flutter pub get`
`pubspec.lock`
`flutter pub get`
To upgrade to a new version of the package,
                  for example to use new features in that package,
                  run`flutter pub upgrade`to retrieve the highest available version of the package
                  that is allowed by the version constraint specified in`pubspec.yaml`.
                  Note that this is a different command from`flutter upgrade`or`flutter update-packages`,
                  which both update Flutter itself.

`flutter pub upgrade`
`pubspec.yaml`
`flutter upgrade`
`flutter update-packages`
### Dependencies on unpublished packages

Packages can be used even when not published on pub.dev.
                  For private packages, or for packages not ready for publishing,
                  additional dependency options are available:

A Flutter app can depend on a package using a file system`path:`dependency. The path can be either relative or absolute.
                      Relative paths are evaluated relative to the directory
                      containing`pubspec.yaml`. For example, to depend on a
                      package, packageA, located in a directory next to the app,
                      use the following syntax:

`path:`
`pubspec.yaml`
`dependencies:
  packageA:
    path: ../packageA/`
You can also depend on a package stored in a Git repository.
                      If the package is located at the root of the repo,
                      use the following syntax:

`dependencies:
    packageA:
      git:
        url: https://github.com/flutter/packageA.git`
If the repository is private and you can connect to it using SSH,
                      depend on the package by using the repo's SSH url:

`dependencies:
    packageA:
      git:
        url: git@github.com:flutter/packageA.git`
Pub assumes the package is located in
                      the root of the Git repository. If that isn't
                      the case, specify the location with the`path`argument.
                      For example:

`path`
`dependencies:
  packageA:
    git:
      url: https://github.com/flutter/packages.git
      path: packages/packageA`
Finally, use the`ref`argument to pin the dependency to a
                      specific git commit, branch, or tag. For more details, see[Package dependencies](https://dart.dev/tools/pub/dependencies).

`ref`
## Examples

The following examples walk through the necessary steps for
                  using packages.

### Example: Using the english_words package

The[english_words](https://pub.dev/packages/english_words)package contains a few thousand
                  of the most used English words plus some utility functions.

`english_words`
To use this package:

1. code-excerpt "lib/english_words.dart (english-words)"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Create a new project called`words_demo`.

`words_demo`
Run`dart pub add english_words`to add the dependency.

`dart pub add english_words`
Open`lib/main.dart`and replace its full contents with:

`lib/main.dart`
`import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
​
void main() {
  runApp(const MyApp());
}
​
class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: DemoPage());
  }
}
​
class DemoPage extends StatelessWidget {
  const DemoPage({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(child: Text(generateWordPairs().first.asPascalCase)),
    );
  }
}`
Run the app. The app's text should display a random English word pair.

### Example: Using the url_launcher package to launch the browser

The[url_launcher](https://pub.dev/packages/url_launcher)plugin package enables opening
                  the default browser on the mobile platform to display
                  a given URL, and is supported on Android, iOS, web,
                  Windows, Linux, and macOS.
                  This package is a special Dart package called a*plugin package*(or*plugin*),
                  which includes platform-specific code.

`url_launcher`
To use this plugin:

1. yaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. code-excerpt "lib/url_launcher.dart (url-launcher)"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Create a new project called`launchdemo`.

`launchdemo`
Open`pubspec.yaml`, and add the`url_launcher`dependency:

`pubspec.yaml`
`url_launcher`
`dependencies:
  flutter:
    sdk: flutter
  url_launcher: ^5.4.0`
Run`flutter pub get`in the terminal,
                      or click**Get Packages get**in VS Code.

`flutter pub get`
Open`lib/main.dart`and replace its full contents with the
                      following:

`lib/main.dart`
`import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
​
void main() {
  runApp(const MyApp());
}
​
class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: DemoPage());
  }
}
​
class DemoPage extends StatelessWidget {
  const DemoPage({super.key});
​
  void launchURL() {
    launchUrl(Uri.parse('https://flutter.dev'));
  }
​
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ElevatedButton(
          onPressed: launchURL,
          child: const Text('Show Flutter homepage'),
        ),
      ),
    );
  }
}`
Run the app (or stop and restart it, if it was already running
                      before adding the plugin). Click**Show Flutter homepage**.
                      You should see the default browser open on the device,
                      displaying the homepage for flutter.dev.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/using-packages.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/packages-and-plugins/using-packages&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/using-packages.md).
