> 原文链接: [https://docs.flutter.dev/packages-and-plugins/developing-packages](https://docs.flutter.dev/packages-and-plugins/developing-packages)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Package introduction

Packages enable the creation of modular code that can be shared easily.
                  A minimal package consists of the following:

`pubspec.yaml`
A metadata file that declares the package name,
                      version, author, and so on.

`lib`
The`lib`directory contains the public code in
                      the package, minimally a single`<package-name>.dart`file.

`lib`
`<package-name>.dart`
### Package types

Packages can contain more than one kind of content:

General packages written in Dart,
                      for example the[path](https://pub.dev/packages/path)package.
                      Some of these might contain Flutter specific
                      functionality and thus have a dependency on the
                      Flutter framework, restricting their use to Flutter only,
                      for example the[fluro](https://pub.dev/packages/fluro)package.

`path`
`fluro`
A specialized Dart package that contains an API written in
                      Dart code combined with one or more platform-specific
                      implementations.

Plugin packages can be written for Android
                      (using Kotlin or Java), iOS (using Swift or Objective-C),
                      web, macOS, Windows, or Linux, or any combination
                      thereof.

A concrete example is the[url_launcher](https://pub.dev/packages/url_launcher)plugin package.
                      To see how to use the`url_launcher`package, and how it
                      was extended to implement support for web,
                      see the Medium article by Harry Terkelsen,[How to Write a Flutter Web Plugin, Part 1](https://blog.flutter.dev/how-to-write-a-flutter-web-plugin-5e26c689ea1).

`url_launcher`
`url_launcher`
A specialized Dart package that enables calling native code using`dart:ffi`.
                      These packages work in Dart standalone and don't require OS-specific build files.
                      They are created with the`flutter create --template=package_ffi`command (see[Create an FFI package](https://docs.flutter.dev/platform-integration/bind-native-code)).
                      This is the recommended approach to build and bundle native code since Flutter 3.38.

`dart:ffi`
`flutter create --template=package_ffi`
## Developing Dart packages

The following instructions explain how to write a Flutter
                  package.

### Step 1: Create the package

To create a starter Flutter package,
                  use the`--template=package`flag with`flutter create`:

`--template=package`
`flutter create`
`$ flutter create --template=package hello`
This creates a package project in the`hello`folder with the following content:

`hello`
A (mostly) empty license text file.

The[unit tests](https://docs.flutter.dev/testing/overview#unit-tests)for the package.

A configuration file used by the IntelliJ IDEs.

A hidden file that tells Git which files or
                      folders to ignore in a project.

A hidden file used by IDEs to track the properties
                      of the Flutter project.

A yaml file containing metadata that specifies
                      the package's dependencies. Used by the pub tool.

A starter markdown file that briefly describes
                      the package's purpose.

A starter app containing Dart code for the package.

A hidden folder containing configuration files
                      for the IntelliJ IDEs.

A (mostly) empty markdown file for tracking
                      version changes to the package.

### Step 2: Implement the package

For pure Dart packages, simply add the functionality
                  inside the main`lib/<package name>.dart`file,
                  or in several files in the`lib`directory.

`lib/<package name>.dart`
`lib`
To test the package, add[unit tests](https://docs.flutter.dev/testing/overview#unit-tests)in a`test`directory.

`test`
For additional details on how to organize the
                  package contents,
                  see the[Dart library package](https://dart.dev/guides/libraries/create-library-packages)documentation.

## Developing plugin packages

If you want to develop a package that calls into
                  platform-specific APIs,
                  you need to develop a plugin package.

The API is connected to the platform-specific
                  implementation(s) using a[platform channel](https://docs.flutter.dev/platform-integration/platform-channels).

### Federated plugins

**Federated plugins**are a way of splitting the API of a plugin
                  into a platform interface, independent platform implementations
                  of that interface, and an app-facing interface that uses the
                  registered implementation of the running platform.

**Package-separated federated plugins**are federated plugins where
                  the platform interface, platform implementations, and the app-facing
                  interface are all separated into their own Dart packages.

So, a package-separated federated plugin can use one package for iOS,
                  another for Android, another for web,
                  and yet another for a car (as an example of an IoT device).
                  Among other benefits, this approach allows a domain expert
                  to extend an existing plugin to work for the platform they know best.

A federated plugin requires the following:

The interface that plugin users interact with when using the
                      plugin. This interface specifies the API used by the Flutter app.
                      In a package-separated federated plugin, this is the package
                      that plugin users depend on to use the plugin.

One or more implementations that contain the platform-specific
                      implementation code. The app-facing interface calls into
                      these implementations—they aren't directly used, or
                      depended on when package-separated, in an app unless they contain
                      platform-specific functionality accessible to the end user.

The interface that glues the app-facing interface
                      to the platform implementations(s). This declares an
                      interface that any platform implementation must implement to
                      support the app-facing interface. Having a separate package
                      that defines this interface ensures that all platform
                      packages implement the same functionality in a uniform way.

#### Endorsed federated plugin

Ideally, when adding a platform implementation to
                  a packaged-separated federated plugin, you will coordinate with
                  the package author to include your implementation.
                  In this way, the original author*endorses*your
                  implementation.

For example, say you write a`foobar_windows`implementation for the (imaginary)`foobar`plugin.
                  In an endorsed plugin, the original`foobar`author
                  adds your Windows implementation as a dependency
                  in the pubspec for the app-facing package.
                  Then, when a developer includes the`foobar`plugin
                  in their Flutter app, the Windows implementation,
                  as well as the other endorsed implementations,
                  are automatically available to the app.

`foobar_windows`
`foobar`
`foobar`
`foobar`
#### Non-endorsed federated plugin

If you can't, for whatever reason, get your implementation
                  added by the original plugin author, then your plugin
                  is*not*endorsed. A developer can still use your
                  implementation, but must manually add the plugin
                  to the app's`pubspec.yaml`file:

`pubspec.yaml`
`dependencies:
  foobar: ^1.0.0
  foobar_windows: ^1.0.0 # Non-endorsed plugin implementation`
This approach also works for overriding an already
                  endorsed plugin implementation of`foobar`.

`foobar`
For more information on federated plugins,
                  why they are useful, and how they are
                  implemented, see the Medium article by Harry Terkelsen,[How To Write a Flutter Web Plugin, Part 2](https://blog.flutter.dev/how-to-write-a-flutter-web-plugin-part-2-afdddb69ece6).

### Specifying a plugin's supported platforms

Plugins can specify the platforms they support by
                  adding keys to the`platforms`map in the`pubspec.yaml`file. For example,
                  the following pubspec file shows the`flutter:`map for the`hello`plugin,
                  which supports only iOS and Android:

`platforms`
`pubspec.yaml`
`flutter:`
`hello`
`flutter:
  plugin:
    platforms:
      android:
        package: com.example.hello
        pluginClass: HelloPlugin
      ios:
        pluginClass: HelloPlugin`
When adding plugin implementations for more platforms,
                  the`platforms`map should be updated accordingly.
                  For example, here's the map in the pubspec file
                  for the`hello`plugin,
                  when updated to add support for macOS and web:

`platforms`
`hello`
`flutter:
  plugin:
    platforms:
      android:
        package: com.example.hello
        pluginClass: HelloPlugin
      ios:
        pluginClass: HelloPlugin
      macos:
        pluginClass: HelloPlugin
      web:
        pluginClass: HelloPlugin
        fileName: hello_web.dart`
#### Federated platform packages

A platform package uses the same format,
                  but includes an`implements`entry indicating
                  which app-facing package it implements. For example,
                  a`hello_windows`plugin containing the Windows
                  implementation for`hello`would have the following`flutter:`map:

`implements`
`hello_windows`
`hello`
`flutter:`
`flutter:
  plugin:
    implements: hello
    platforms:
      windows:
        pluginClass: HelloPlugin`
#### Endorsed implementations

An app facing package can endorse a platform package by adding a
                  dependency on it, and including it as a`default_package`in the`platforms:`map. If the`hello`plugin above endorsed`hello_windows`,
                  it would look as follows:

`default_package`
`platforms:`
`hello`
`hello_windows`
`flutter:
  plugin:
    platforms:
      android:
        package: com.example.hello
        pluginClass: HelloPlugin
      ios:
        pluginClass: HelloPlugin
      windows:
        default_package: hello_windows
​
dependencies:
  hello_windows: ^1.0.0`
Note that as shown here, an app-facing package can have
                  some platforms implemented within the package,
                  and others in endorsed federated implementations.

#### Shared iOS and macOS implementations

Many frameworks support both iOS and macOS with identical
                  or mostly identical APIs, making it possible to implement
                  some plugins for both iOS and macOS with the same codebase.
                  Normally each platform's implementation is in its own
                  folder, but the`sharedDarwinSource`option allows iOS
                  and macOS to use the same folder instead:

`sharedDarwinSource`
`flutter:
  plugin:
    platforms:
      ios:
        pluginClass: HelloPlugin
        sharedDarwinSource: true
      macos:
        pluginClass: HelloPlugin
        sharedDarwinSource: true
​
environment:
  sdk: ^3.0.0
  # Flutter versions prior to 3.7 did not support the
  # sharedDarwinSource option.
  flutter: ">=3.7.0"`
When`sharedDarwinSource`is enabled, instead of
                  an`ios`directory for iOS and a`macos`directory
                  for macOS, both platforms use a shared`darwin`directory for all code and resources. When enabling
                  this option, you need to move any existing files
                  from`ios`and`macos`to the shared directory. You
                  also need to update the podspec file to set the
                  dependencies and deployment targets for both platforms,
                  for example:

`sharedDarwinSource`
`ios`
`macos`
`darwin`
`ios`
`macos`
`s.ios.dependency 'Flutter'
  s.osx.dependency 'FlutterMacOS'
  s.ios.deployment_target = '13.0'
  s.osx.deployment_target = '10.15'`
### Step 1: Create the package

To create a plugin package, use the`--template=plugin`flag with`flutter create`.

`--template=plugin`
`flutter create`
Use the`--platforms=`option followed by a
                  comma-separated list to specify the platforms
                  that the plugin supports. Available platforms are:`android`,`ios`,`web`,`linux`,`macos`, and`windows`.
                  If no platforms are specified, the
                  resulting project doesn't support any platforms.

`--platforms=`
`android`
`ios`
`web`
`linux`
`macos`
`windows`
Use the`--org`option to specify your organization,
                  using reverse domain name notation. This value is used
                  in various package and bundle identifiers in the
                  generated plugin code.

`--org`
By default, the plugin project uses Swift for iOS code and
                  Kotlin for Android code. If you prefer Objective-C or Java,
                  you can specify the iOS language using`-i`and the
                  Android language using`-a`.
                  Please choose**one**of the following:

`-i`
`-a`
`$ flutter create --org com.example --template=plugin --platforms=android,ios,linux,macos,windows -a kotlin hello`
`$ flutter create --org com.example --template=plugin --platforms=android,ios,linux,macos,windows -a java hello`
`$ flutter create --org com.example --template=plugin --platforms=android,ios,linux,macos,windows -i objc hello`
`$ flutter create --org com.example --template=plugin --platforms=android,ios,linux,macos,windows -i swift hello`
This creates a plugin project in the`hello`folder
                  with the following specialized content:

`hello`
`lib/hello.dart`
The Dart API for the plugin.

`android/src/main/java/com/example/hello/HelloPlugin.kt`
The Android platform-specific implementation of the plugin API
                      in Kotlin.

`ios/Classes/HelloPlugin.m`
The iOS-platform specific implementation of the plugin API
                      in Objective-C.

`example/`
A Flutter app that depends on the plugin,
                      and illustrates how to use it.

### Step 2: Implement the package

As a plugin package contains code for several platforms
                  written in several programming languages,
                  some specific steps are needed to ensure a smooth experience.

#### Step 2a: Define the package API (.dart)

The API of the plugin package is defined in Dart code.
                  Open the main`hello/`folder in your favorite[Flutter editor](https://docs.flutter.dev/tools/editors).
                  Locate the file`lib/hello.dart`.

`hello/`
`lib/hello.dart`
#### Step 2b: Add Android platform code (.kt/.java)

We recommend you edit the Android code using Android Studio.

Before editing the Android platform code in Android Studio,
                  first make sure that the code has been built at least once
                  (in other words, run the example app from your IDE/editor,
                  or in a terminal execute`cd hello/example; flutter build apk --config-only`).

`cd hello/example; flutter build apk --config-only`
Then use the following steps:

1. Launch Android Studio.
1. Select**Open an existing Android Studio Project**in the**Welcome to Android Studio**dialog,
                    or select**File > Open**from the menu,
                    and select either the`hello/example/android/build.gradle`or the`hello/example/android/build.gradle.kts`file.
1. In the**Gradle Sync**dialog, select**OK**.
1. In the**Android Gradle Plugin Update**dialog,
                    select**Don't remind me again for this project**.

`hello/example/android/build.gradle`
`hello/example/android/build.gradle.kts`
The Android platform code of your plugin is located in`hello/java/com.example.hello/HelloPlugin`.

`hello/java/com.example.hello/HelloPlugin`
You can run the example app from Android Studio by
                  pressing the run (▶) button.

#### Step 2c: Add iOS platform code (.swift/.h+.m)

We recommend you edit the iOS code using Xcode.

Before editing the iOS platform code in Xcode,
                  first make sure that the code has been built at least once
                  (in other words, run the example app from your IDE/editor,
                  or in a terminal execute`cd hello/example; flutter build ios --no-codesign --config-only`).

`cd hello/example; flutter build ios --no-codesign --config-only`
Then use the following steps:

1. Launch Xcode.
1. Select**File > Open**, and select the`hello/example/ios/Runner.xcworkspace`file.

`hello/example/ios/Runner.xcworkspace`
The iOS platform code for your plugin is located in`Pods/Development Pods/hello/../../example/ios/.symlinks/plugins/hello/ios/Classes`in the Project Navigator. (If you are using`sharedDarwinSource`,
                  the path will end with`hello/darwin/Classes`instead.)

`Pods/Development Pods/hello/../../example/ios/.symlinks/plugins/hello/ios/Classes`
`sharedDarwinSource`
`hello/darwin/Classes`
You can run the example app by pressing the run (▶) button.

##### Add CocoaPod dependencies

Use the following instructions to add`HelloPod`with the version`0.0.1`:

`HelloPod`
`0.0.1`
1. ruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Specify the dependency at the end of`ios/hello.podspec`:

`ios/hello.podspec`
`s.dependency 'HelloPod', '0.0.1'`
For private pods, refer to[Private CocoaPods](https://guides.cocoapods.org/making/private-cocoapods.html)to ensure repo access:

`s.source = {
    # For pods hosted on GitHub
    :git => "https://github.com/path/to/HelloPod.git",
    # Alternatively, for pods hosted locally
    # :path => "file:///path/to/private/repo",
    :tag => s.version.to_s
  }``

Installing the plugin

- Add the plugin in the project’s`pubspec.yaml`dependencies.
- Run`flutter pub get`.
- In the project’s`ios/`directory, run`pod install`.

`pubspec.yaml`
`flutter pub get`
`ios/`
`pod install`
The pod should appear in the installation summary.

If your plugin requires a privacy manifest, for example,
                  if it uses any**required reason APIs**,
                  update the`PrivacyInfo.xcprivacy`file to
                  describe your plugin's privacy impact,
                  and add the following to the bottom of your podspec file:

`PrivacyInfo.xcprivacy`
`s.resource_bundles = {'your_plugin_privacy' => ['your_plugin/Sources/your_plugin/Resources/PrivacyInfo.xcprivacy']}`
For more information,
                  check out[Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files)on the Apple developer site.

#### Step 2d: Add Linux platform code (.h+.cc)

We recommend you edit the Linux code using an IDE with
                  C++ integration. The instructions below are for
                  Visual Studio Code with the "C/C++" and "CMake" extensions
                  installed, but can be adjusted for other IDEs.

Before editing the Linux platform code in an IDE,
                  first make sure that the code has been built at least once
                  (in other words, run the example app from your Flutter
                  IDE/editor, or in a terminal execute`cd hello/example; flutter build linux`).

`cd hello/example; flutter build linux`
Then use the following steps:

1. Launch Visual Studio Code.
1. Open the`hello/example/linux/`directory.
1. Choose**Yes**in the prompt asking:`Would you like to configure project "linux"?`.
                    This will allow C++ autocomplete to work.

`hello/example/linux/`
`Would you like to configure project "linux"?`
The Linux platform code for your plugin is located in`flutter/ephemeral/.plugin_symlinks/hello/linux/`.

`flutter/ephemeral/.plugin_symlinks/hello/linux/`
You can run the example app using`flutter run`.**Note:**Creating a runnable Flutter application
                  on Linux requires steps that are part of the`flutter`tool, so even if your editor provides CMake
                  integration building and running that way won't
                  work correctly.

`flutter run`
`flutter`
#### Step 2e: Add macOS platform code (.swift)

We recommend you edit the macOS code using Xcode.

Before editing the macOS platform code in Xcode,
                  first make sure that the code has been built at least once
                  (in other words, run the example app from your IDE/editor,
                  or in a terminal execute`cd hello/example; flutter build macos --config-only`).

`cd hello/example; flutter build macos --config-only`
Then use the following steps:

1. Launch Xcode.
1. Select**File > Open**, and select the`hello/example/macos/Runner.xcworkspace`file.

`hello/example/macos/Runner.xcworkspace`
The macOS platform code for your plugin is located in`Pods/Development Pods/hello/../../example/macos/Flutter/ephemeral/.symlinks/plugins/hello/macos/Classes`in the Project Navigator. (If you are using`sharedDarwinSource`,
                  the path will end with`hello/darwin/Classes`instead.)

`Pods/Development Pods/hello/../../example/macos/Flutter/ephemeral/.symlinks/plugins/hello/macos/Classes`
`sharedDarwinSource`
`hello/darwin/Classes`
You can run the example app by pressing the run (▶) button.

#### Step 2f: Add Windows platform code (.h+.cpp)

We recommend you edit the Windows code using Visual Studio.

Before editing the Windows platform code in Visual Studio,
                  first make sure that the code has been built at least once
                  (in other words, run the example app from your IDE/editor,
                  or in a terminal execute`cd hello/example; flutter build windows`).

`cd hello/example; flutter build windows`
Then use the following steps:

1. Launch Visual Studio.
1. Select**Open a project or solution**, and select the`hello/example/build/windows/hello_example.sln`file.

`hello/example/build/windows/hello_example.sln`
The Windows platform code for your plugin is located in`hello_plugin/Source Files`and`hello_plugin/Header Files`in
                  the Solution Explorer.

`hello_plugin/Source Files`
`hello_plugin/Header Files`
You can run the example app by right-clicking`hello_example`in
                  the Solution Explorer and selecting**Set as Startup Project**,
                  then pressing the run (▶) button.**Important:**After
                  making changes to plugin code, you must select**Build > Build Solution**before running again, otherwise
                  an outdated copy of the built plugin will be run instead
                  of the latest version containing your changes.

`hello_example`
#### Step 2g: Connect the API and the platform code

Finally, you need to connect the API written in Dart code with
                  the platform-specific implementations.
                  This is done using a[platform channel](https://docs.flutter.dev/platform-integration/platform-channels),
                  or through the interfaces defined in a platform
                  interface package.

### Add support for platforms in an existing plugin project

To add support for specific platforms to an
                  existing plugin project, run`flutter create`with
                  the`--template=plugin`flag again in the project directory.
                  For example, to add web support in an existing plugin, run:

`flutter create`
`--template=plugin`
`$ flutter create --template=plugin --platforms=web .`
If this command displays a message about updating the`pubspec.yaml`file, follow the provided instructions.

`pubspec.yaml`
### Dart platform implementations

In many cases, non-web platform implementations only use the
                  platform-specific implementation language, as shown above. However,
                  platform implementations can also use platform-specific Dart as well.

#### Dart-only platform implementations

In some cases, some platforms can be
                  implemented entirely in Dart (for example, using FFI).
                  For a Dart-only platform implementation on a platform other than web,
                  replace the`pluginClass`in pubspec.yaml with a`dartPluginClass`.
                  Here is the`hello_windows`example above modified for a
                  Dart-only implementation:

`pluginClass`
`dartPluginClass`
`hello_windows`
`flutter:
  plugin:
    implements: hello
    platforms:
      windows:
        dartPluginClass: HelloPluginWindows`
In this version you would have no C++ Windows code, and would instead
                  subclass the`hello`plugin's Dart platform interface class with a`HelloPluginWindows`class that includes a static`registerWith()`method.  This method is called during startup,
                  and can be used to register the Dart implementation:

`hello`
`HelloPluginWindows`
`registerWith()`
`class HelloPluginWindows extends HelloPluginPlatform {
  /// Registers this class as the default instance of [HelloPluginPlatform].
  static void registerWith() {
    HelloPluginPlatform.instance = HelloPluginWindows();
  }`
#### Hybrid platform implementations

Platform implementations can also use both Dart and a platform-specific
                  language. For example, a plugin could use a different platform channel
                  for each platform so that the channels can be customized per platform.

A hybrid implementation uses both of the registration systems
                  described above. Here is the`hello_windows`example above modified for a
                  hybrid implementation:

`hello_windows`
`flutter:
  plugin:
    implements: hello
    platforms:
      windows:
        dartPluginClass: HelloPluginWindows
        pluginClass: HelloPlugin`
The Dart`HelloPluginWindows`class would use the`registerWith()`shown above for Dart-only implementations, while the C++`HelloPlugin`class would be the same as in a C++-only implementation.

`HelloPluginWindows`
`registerWith()`
`HelloPlugin`
### Testing your plugin

We encourage you test your plugin with automated tests
                  to ensure that functionality doesn't regress
                  as you make changes to your code.

To learn more about testing your plugins,
                  check out[Testing plugins](https://docs.flutter.dev/testing/testing-plugins).
                  If you are writing tests for your Flutter app
                  and plugins are causing crashes,
                  check out[Flutter in plugin tests](https://docs.flutter.dev/testing/plugins-in-tests).

## Developing FFI packages

If you want to develop a package that calls into native APIs using
                  Dart's FFI, you need to develop an FFI package.

### Step 1: Create the package

To create a starter FFI package,
                  use the`--template=package_ffi`flag with`flutter create`:

`--template=package_ffi`
`flutter create`
`$ flutter create --template=package_ffi hello`
This creates an FFI package project in the`hello`folder with the following specialized content:

`hello`
**lib**: The Dart code that defines the API of the package,
                    and which calls into the native code using`dart:ffi`.

`dart:ffi`
**src**: The native source code.

**hook/build.dart**: The build hook script that compiles the native code.

### Step 2: Binding to native code

To use the native code, bindings in Dart are needed.

To avoid writing these by hand,
                  they are generated from the header file
                  (`src/hello.h`) by[package:ffigen](https://pub.dev/packages/ffigen).
                  Reference the[ffigen docs](https://pub.dev/packages/ffigen/install)for information
                  on how to install this package.

`src/hello.h`
`package:ffigen`
To regenerate the bindings, run the following command:

`$ dart run tool/ffigen.dart`
### Step 3: Invoking native code

Very short-running native functions can be directly
                  invoked from any isolate.
                  For an example, see`sum`in`lib/hello.dart`.

`sum`
`lib/hello.dart`
Longer-running functions should be invoked on a[helper isolate](https://dart.dev/guides/language/concurrency#background-workers)to avoid dropping frames in
                  Flutter applications.
                  For an example, see`sumAsync`in`lib/hello.dart`.

`sumAsync`
`lib/hello.dart`
## Adding documentation

It is recommended practice to add the following documentation
                  to all packages:

1. A`README.md`file that introduces the package
1. A`CHANGELOG.md`file that documents changes in each version
1. A[LICENSE](#adding-licenses-to-the-license-file)file containing the terms under which the package
                    is licensed
1. API documentation for all public APIs (see below for details)

`README.md`
`CHANGELOG.md`
`LICENSE`
### API documentation

When you publish a package,
                  API documentation is automatically generated and
                  published to pub.dev/documentation.
                  For example, see the docs for[device_info_plus](https://pub.dev/documentation/device_info_plus).

`device_info_plus`
If you wish to generate API documentation locally on
                  your development machine, use the following commands:

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Run the `dart doc` tool
    (included as part of the Flutter SDK), as follows:@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Change directory to the location of your package:

`cd ~/dev/mypackage`
Tell the documentation tool where the
Flutter SDK is located (change the following commands to reflect
where you placed it):

`export FLUTTER_ROOT=~/dev/flutter  # on macOS or Linux

   set FLUTTER_ROOT=~/dev/flutter     # on Windows`
`$FLUTTER_ROOT/bin/cache/dart-sdk/bin/dart doc   # on macOS or Linux

   %FLUTTER_ROOT%\bin\cache\dart-sdk\bin\dart doc  # on Windows`
For tips on how to write API documentation, see[Effective Dart Documentation](https://dart.dev/guides/language/effective-dart/documentation).

### Adding licenses to the LICENSE file

Individual licenses inside each LICENSE file
                  should be separated by 80 hyphens
                  on their own on a line.

If a LICENSE file contains more than one
                  component license, then each component
                  license must start with the names of the
                  packages to which the component license applies,
                  with each package name on its own line,
                  and the list of package names separated from
                  the actual license text by a blank line.
                  (The packages need not match the names of
                  the pub package. For example, a package might itself contain
                  code from multiple third-party sources,
                  and might need to include a license for each one.)

The following example shows a well-organized license file:

`package_1

<some license text>

--------------------------------------------------------------------------------
package_2

<some license text>`
Here is another example of a well-organized license file:

`package_1

<some license text>

--------------------------------------------------------------------------------
package_1
package_2

<some license text>`
Here is an example of a poorly-organized license file:

`<some license text>

--------------------------------------------------------------------------------
<some license text>`
Another example of a poorly-organized license file:

`package_1

<some license text>
--------------------------------------------------------------------------------
<some license text>`
## Publishing your package

Once you have implemented a package, you can publish it on[pub.dev](https://pub.dev), so that other developers can easily use it.

Prior to publishing, make sure to review the`pubspec.yaml`,`README.md`, and`CHANGELOG.md`files to make sure their
                  content is complete and correct. Also, to improve the
                  quality and usability of your package (and to make it
                  more likely to achieve the status of a Flutter Favorite),
                  consider including the following items:

`pubspec.yaml`
`README.md`
`CHANGELOG.md`
- Diverse code usage examples
- Screenshots, animated gifs, or videos
- A link to the corresponding code repository

Next, run the publish command in`dry-run`mode
                  to see if everything passes analysis:

`dry-run`
`$ flutter pub publish --dry-run`
The next step is publishing to pub.dev,
                  but be sure that you are ready because[publishing is forever](https://dart.dev/tools/pub/publishing#publishing-is-forever):

`$ flutter pub publish`
For more details on publishing, see the[publishing docs](https://dart.dev/tools/pub/publishing)on dart.dev.

## Handling package interdependencies

If you are developing a package`hello`that depends on
                  the Dart API exposed by another package, you need to add
                  that package to the`dependencies`section of your`pubspec.yaml`file. The code below makes the Dart API
                  of the`url_launcher`plugin available to`hello`:

`hello`
`dependencies`
`pubspec.yaml`
`url_launcher`
`hello`
`dependencies:
  url_launcher: ^6.3.2`
You can now`import 'package:url_launcher/url_launcher.dart'`and`launch(someUrl)`in the Dart code of`hello`.

`import 'package:url_launcher/url_launcher.dart'`
`launch(someUrl)`
`hello`
This is no different from how you include packages in
                  Flutter apps or any other Dart project.

But if`hello`happens to be a*plugin*package
                  whose platform-specific code needs access
                  to the platform-specific APIs exposed by`url_launcher`,
                  you also need to add suitable dependency declarations
                  to your platform-specific build files, as shown below.

`hello`
`url_launcher`
### Android

The following example sets a dependency for`url_launcher`in`hello/android/build.gradle`:

`url_launcher`
`hello/android/build.gradle`
`android {
    // lines skipped
    dependencies {
        compileOnly rootProject.findProject(":url_launcher")
    }
}`
You can now`import io.flutter.plugins.urllauncher.UrlLauncherPlugin`and access the`UrlLauncherPlugin`class in the source code at`hello/android/src`.

`import io.flutter.plugins.urllauncher.UrlLauncherPlugin`
`UrlLauncherPlugin`
`hello/android/src`
For more information on`build.gradle`files, see the[Gradle Documentation](https://docs.gradle.org/current/userguide/tutorial_using_tasks.html)on build scripts.

`build.gradle`
### iOS

The following example sets a dependency for`url_launcher`in`hello/ios/hello.podspec`:

`url_launcher`
`hello/ios/hello.podspec`
`Pod::Spec.new do |s|
  # lines skipped
  s.dependency 'url_launcher'`
You can now`#import "UrlLauncherPlugin.h"`and
                  access the`UrlLauncherPlugin`class in the source code
                  at`hello/ios/Classes`.

`#import "UrlLauncherPlugin.h"`
`UrlLauncherPlugin`
`hello/ios/Classes`
For additional details on`.podspec`files, see the[CocoaPods Documentation](https://guides.cocoapods.org/syntax/podspec.html).

`.podspec`
### Web

All web dependencies are handled by the`pubspec.yaml`file, like any other Dart package.

`pubspec.yaml`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/developing-packages.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/packages-and-plugins/developing-packages&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/developing-packages.md).
