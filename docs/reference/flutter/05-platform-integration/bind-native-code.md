> 原文链接: [https://docs.flutter.dev/platform-integration/bind-native-code](https://docs.flutter.dev/platform-integration/bind-native-code)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter apps can use the[dart:ffi](https://api.dart.dev/dart-ffi/dart-ffi-library.html)library to call native APIs.*FFI*stands
                  for[foreign function interface](https://en.wikipedia.org/wiki/Foreign_function_interface). Other terms for similar functionality
                  include*native interface*and*language bindings.*

Since Flutter 3.38, the recommended way to bind to native code is to use the`flutter create --template=package_ffi`command. This template uses[build hooks](https://dart.dev/tools/hooks)to configure the native build in a`build.dart`script, and no longer requires OS-specific build files. This
                  approach works for both Flutter and Dart standalone projects.

`flutter create --template=package_ffi`
`build.dart`
If you need to use the Flutter Plugin API, or if you need to configure a Google
                  Play services runtime on Android, use the standard plugin template (`flutter create --template=plugin`).

`flutter create --template=plugin`
## Create an FFI package

To create an FFI package, run the following command:

`$ flutter create --template=package_ffi native_add
$ cd native_add`
This creates a package with the following specialized content:

- **lib/native_add.dart**: The Dart code that defines the API of the package.
- **lib/native_add_bindings_generated.dart**: The generated Dart bindings
                    for the native code.
- **src/native_add.c**: The native C source code.
- **src/native_add.h**: The C header file for the native code.
- **hook/build.dart**: A script that is run by the Flutter SDK to compile the
                    native code.
- **ffigen.yaml**: The configuration file for[package:ffigen](https://pub.dev/packages/ffigen)to generate
                    the Dart bindings.
- **pubspec.yaml**: The package definition, which enables the`build.dart`hook.

`lib/native_add.dart`
`lib/native_add_bindings_generated.dart`
`src/native_add.c`
`src/native_add.h`
`hook/build.dart`
`ffigen.yaml`
`package:ffigen`
`pubspec.yaml`
`build.dart`
## The native code

The native code is located in`src/native_add.c`and`src/native_add.h`. The C
                  function`sum`is defined in the`.c`file and its signature is in the header
                  file. The function is marked to be exported so that it can be called from Dart.

`src/native_add.c`
`src/native_add.h`
`sum`
`.c`
## The build hook

The native code is compiled and bundled with your app automatically. This is
                  done by the`hook/build.dart`script, which is a[build hook](https://dart.dev/tools/hooks).

`hook/build.dart`
This means you no longer need to write OS-specific build files (like`CMakeLists.txt`for Linux/Windows,`.podspec`for iOS/macOS, or`build.gradle`for Android) to compile your native code.

`CMakeLists.txt`
`.podspec`
`build.gradle`
The build hook uses`package:native_toolchain_c`to compile the C code into a
                  dynamic library. You can customize this file to build other native languages or
                  to download pre-compiled binaries.

`package:native_toolchain_c`
## The Dart code

The Dart code defines the public API of the package.

### Generating the bindings

To bind to the native code, the template uses[package:ffigen](https://pub.dev/packages/ffigen)to generate
                  bindings from the header file (`src/native_add.h`). The generation is configured
                  in`ffigen.yaml`.

`package:ffigen`
`src/native_add.h`
`ffigen.yaml`
This generates`lib/native_add_bindings_generated.dart`.

`lib/native_add_bindings_generated.dart`
### Calling the native function

The generated bindings in`lib/native_add_bindings_generated.dart`contain`@Native() external`functions. These functions are automatically resolved at
                  runtime against the code asset outputted by the build hook (which runs at build
                  time). This means there is no OS-specific logic required for`dlopen`-ing the
                  dynamic libraries, making the Dart code truly cross-platform.

`lib/native_add_bindings_generated.dart`
`@Native() external`
`dlopen`
The main library file`lib/native_add.dart`exposes these functions. Your app
                  can then call these functions by importing`package:native_add/native_add.dart`.

`lib/native_add.dart`
`package:native_add/native_add.dart`
## Testing

The generated package includes a unit test in`test/native_add_test.dart`that
                  shows how to test the native function.

`test/native_add_test.dart`
## Other use cases

### System libraries

To link against a system library, you modify the`build.dart`hook to specify
                  the linking mode. Instead of compiling source code, you create a`CodeAsset`and
                  set its`linkMode`.

`build.dart`
`CodeAsset`
`linkMode`
For many system libraries on Android, iOS, Linux, and macOS, you can use`LookupInProcess()`to find symbols in the main process.

`LookupInProcess()`
For Windows, you often use`DynamicLoadingSystem()`and provide the name of the
                  DLL.

`DynamicLoadingSystem()`
Here is an example`build.dart`that links against system libraries to get the
                  host name:

`build.dart`
`// hook/build.dart
import 'package:hooks/hooks.dart';
import 'package:code_assets/code_assets.dart';
​
void main(List<String> args) async {
  await build(args, (input, output) async {
    final targetOS = input.target.os;
    switch (targetOS) {
      case OS.android || OS.iOS || OS.linux || OS.macOS:
        output.assets.code.add(
          CodeAsset(
            package: 'host_name',
            name: 'src/third_party/unix.dart',
            linkMode: LookupInProcess(),
          ),
        );
      case OS.windows:
        output.assets.code.add(
          CodeAsset(
            package: 'host_name',
            name: 'src/third_party/windows.dart',
            linkMode: DynamicLoadingSystem(Uri.file('ws2_32.dll')),
          ),
        );
      default:
        throw Exception('Unsupported target os: $targetOS');
    }
  });
}`
The Dart files (`unix.dart`,`windows.dart`) would then contain the`external`functions that use the symbols from these system libraries.

`unix.dart`
`windows.dart`
`external`
#### Bundlinglibc++_shared.soon Android

`libc++_shared.so`
Although`libc++_shared.so`ships with the Android NDK,
                  it isn't a system library.
                  If your app or package uses the[C++ standard library](https://developer.android.com/ndk/guides/cpp-support#cs),
                  or includes[multiple shared libraries](https://developer.android.com/ndk/guides/cpp-support#shared_runtimes)that depend on it,
                  your app needs to bundle`libc++_shared.so`.

`libc++_shared.so`
`libc++_shared.so`
To bundle the library in your app,
                  add a dependency on[package:android_libcpp_shared](https://pub.dev/packages/android_libcpp_shared),
                  which uses its own build hook to bundle`libc++_shared.so`from the locally installed NDK for each target architecture.

`package:android_libcpp_shared`
`libc++_shared.so`
### Closed-source libraries

You can also use build hooks to link against pre-compiled, closed-source
                  libraries. The recommended approach is to download the pre-compiled binaries at
                  build time and verify their integrity with a file hash.

In your`build.dart`hook, you would:

`build.dart`
1. Download the library from a URL.
1. Verify the hash of the downloaded file.
1. Place the library in the build output directory.
1. Create a`CodeAsset`with`DynamicLoading`pointing to the library.

`CodeAsset`
`DynamicLoading`
Here is a simplified example of the`CodeAsset`creation:

`CodeAsset`
`// hook/build.dart
import 'package:hooks/hooks.dart';
import 'package:code_assets/code_assets.dart';
​
void main(List<String> args) async {
  await build(args, (input, output) async {
    // 1. Download the library from a URL.
    // 2. Verify the hash of the downloaded file.
    // 3. Place the library in the build output directory.
​
    output.assets.code.add(
      CodeAsset(
        package: input.packageName,
        name: 'src/my_lib.dart', // Dart file with bindings
        linkMode: DynamicLoadingBundled(),
        file: input.outputDirectory.resolve('my_lib.so'),
      ),
    );
  });
}`
You would need to handle different architectures and platforms by having
                  different versions of your pre-compiled library.

For more examples, see the[code_assets package
                    examples](https://pub.dev/packages/code_assets/example).

## Dynamic library naming guidelines

When implementing`build.dart`hooks for packages that bundle code assets, it
                  is critical to ensure consistent naming of your dynamic libraries across all
                  target architectures and SDKs.

`build.dart`
On Apple platforms (iOS and macOS), dynamic libraries are bundled into
                  frameworks. Flutter's build system relies on these names to generate metadata
                  and package distributable formats like XCFrameworks.

### Consistency across architectures

For a given asset ID, your hook will be invoked multiple times, once per
                  architecture. Your hook must produce the same filename regardless of the target
                  architecture (for example,`arm64`vs.`x64`).

`arm64`
`x64`
- **Why?**Within a single SDK build, Flutter combines architecture-specific
                    binaries into a single universal (fat) binary using`lipo`. If architectures
                    have different filenames, the tool will pick one non-deterministically and
                    issue a warning. Furthermore, error messages at runtime will be confusing
                    for your users if dynamic libraries are renamed.
- **Recommended action**: Avoid adding architecture suffixes to your
                    filenames (for example, use`libsqlite3.dylib`instead of`libsqlite3_arm64.dylib`). Instead, write the file to`input.outputDirectory`(which is unique per architecture) or to an
                    architecture-specific subdirectory of`input.outputDirectoryShared`(for
                    example,`input.outputDirectoryShared.resolve('$architecture/')`).

`lipo`
`libsqlite3.dylib`
`libsqlite3_arm64.dylib`
`input.outputDirectory`
`input.outputDirectoryShared`
`input.outputDirectoryShared.resolve('$architecture/')`
### Consistency across SDKs (iOS)

When building for iOS, your hook will be invoked multiple times with different
                  values for the SDK and architecture. Both physical device (`iphoneos`) and
                  simulator (`iphonesimulator`) invocations must produce the same framework name
                  for the same asset ID.

`iphoneos`
`iphonesimulator`
- **Why?**Flutter uses`xcodebuild -create-xcframework`to combine these
                    outputs. Xcode requires that all platform slices within an XCFramework
                    share the same framework name to allow seamless linking. If filenames
                    differ, the Flutter tool cannot create a correct XCFramework, and commands
                    like`flutter build ios-framework`will fail.
- **Recommended action**: Do not use suffixes like`_sim`or`_simulator`for
                    the simulator build. The XCFramework structure already handles the platform
                    separation internally (for example,`MyLib.xcframework/ios-arm64_x86_64-simulator/MyLib.framework`). Instead,
                    write the file to`input.outputDirectory`(which is unique per SDK) or to an
                    SDK-specific subdirectory of`input.outputDirectoryShared`.

`xcodebuild -create-xcframework`
`flutter build ios-framework`
`_sim`
`_simulator`
`MyLib.xcframework/ios-arm64_x86_64-simulator/MyLib.framework`
`input.outputDirectory`
`input.outputDirectoryShared`
### Consistency in the set of assets

Your hook must produce the same set of Asset IDs across all SDKs for a given
                  target platform.

- **Why?**Apple's build system and App Store validation require that all
                    frameworks included in an application are compatible with the target
                    device. If you produce an asset for the simulator (`iphonesimulator`) but
                    not for the physical device (`iphoneos`), the resulting XCFramework will
                    contain a slice that has no counterpart for the device. This can lead to
                    build failures or Apple rejecting the application for including
                    simulator-only binaries in a device build.
- **Recommended action**: Ensure that your`build.dart`hook logic handles
                    all supported SDKs consistently. If you produce an asset for one SDK, you
                    must produce a corresponding asset for all other SDKs for that platform.
                    For SDK-specific code, you can use stub implementations for other SDKs.

`iphonesimulator`
`iphoneos`
`build.dart`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/bind-native-code.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/bind-native-code&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/bind-native-code.md).
