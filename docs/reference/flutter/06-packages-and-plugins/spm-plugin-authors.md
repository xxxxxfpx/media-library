> 原文链接: [https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-plugin-authors](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-plugin-authors)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter's Swift Package Manager integration has several benefits:

1. **Provides access to the Swift package ecosystem**.
                    Flutter plugins can use the growing ecosystem of[Swift packages](https://swiftpackageindex.com/)!
1. **Simplifies Flutter installation**.
                    Swift Package Manager is bundled with Xcode.
                    In the future, you won’t need to install Ruby and CocoaPods to target iOS or
                    macOS.

## How to turn on Swift Package Manager

Flutter's Swift Package Manager support is turned off by default.
                  To turn it on:

1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Upgrade to the latest Flutter SDK:

`flutter upgrade`
Turn on the Swift Package Manager feature:

`flutter config --enable-swift-package-manager`
Using the Flutter CLI to run an app[migrates the project](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-add-swift-package-manager-integration)to add
                  Swift Package Manager integration.
                  This makes your project download the Swift packages that
                  your Flutter plugins depend on.
                  An app with Swift Package Manager integration requires Flutter version 3.24 or
                  higher.
                  To use an older Flutter version,
                  you will need to[remove Swift Package Manager integration](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers#how-to-remove-swift-package-manager-integration)from the app.

Flutter falls back to CocoaPods for dependencies that do not support Swift
                  Package Manager yet.

## How to turn off Swift Package Manager

Disabling Swift Package Manager causes Flutter to use CocoaPods for all
                  dependencies.
                  However, Swift Package Manager remains integrated with your project.
                  To remove Swift Package Manager integration completely from your project,
                  follow the[How to remove Swift Package Manager integration](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers#how-to-remove-swift-package-manager-integration)instructions.

### Turn off for a single project

In the project's`pubspec.yaml`file, under the`flutter`section,
                  set`enable-swift-package-manager`to`false`in the`config`subsection.

`pubspec.yaml`
`flutter`
`enable-swift-package-manager`
`false`
`config`
`# The following section is specific to Flutter packages.
flutter:
  config:
    enable-swift-package-manager: false`
This turns off Swift Package Manager for all contributors to this project.

### Turn off globally for all projects

Run the following command:

`flutter config --no-enable-swift-package-manager`
This turns off Swift Package Manager for the current user.

If a project is incompatible with Swift Package Manager, all contributors
                  need to run this command.

## How to add Swift Package Manager support to an existing Flutter plugin

This guide shows how to add Swift Package Manager support to a plugin that
                  already supports CocoaPods.
                  This ensures the plugin is usable by all Flutter projects.

Flutter plugins should support*both*Swift Package Manager and CocoaPods until
                  further notice.

Swift Package Manager adoption will be gradual.
                  Plugins that don't support CocoaPods won't be usable by projects that haven't
                  migrated to Swift Package Manager yet.
                  Plugins that don't support Swift Package Manager can cause problems for projects
                  that have migrated.

- [Swift plugin](#14-tab-panel)
- [Objective-C plugin](#15-tab-panel)

Replace`plugin_name`throughout this guide with the name of your plugin.
                        The example below uses`ios`, replace`ios`with`macos`/`darwin`as applicable.

`plugin_name`
`ios`
`ios`
`macos`
`darwin`
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonpubspec.yamlyaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. pigeons/messages.dartdart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. ios/plugin_name.podspecruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. swift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. .gitignore@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

[Turn on the Swift Package Manager feature](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-plugin-authors#how-to-turn-on-swift-package-manager).

Start by creating a directory under the`ios`,`macos`, and/or`darwin`directories.
                            Name this new directory the name of the platform package.

`ios`
`macos`
`darwin`


- …
- plugin_name/

Within this new directory, create the following files/directories:

- `Package.swift`(file)
- `Sources`(directory)
- `Sources/plugin_name`(directory)

`Package.swift`
`Sources`
`Sources/plugin_name`
Your plugin should look like:



- …

- Package.swift

- plugin_name/

Use the following template in the`Package.swift`file:

`Package.swift`
`// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.
​
import PackageDescription
​
let package = Package(
    // TODO: Update your plugin name.
    name: "plugin_name",
    platforms: [
        // TODO: Update the platforms your plugin supports.
        // If your plugin only supports iOS, remove `.macOS(...)`.
        // If your plugin only supports macOS, remove `.iOS(...)`.
        .iOS("13.0"),
        .macOS("10.15")
    ],
    products: [
        // TODO: Update your library and target names.
        // If the plugin name contains "_", replace with "-" for the library name.
        .library(name: "plugin-name", targets: ["plugin_name"])
    ],
    dependencies: [
        .package(name: "FlutterFramework", path: "../FlutterFramework")
    ],
    targets: [
        .target(
            // TODO: Update your target name.
            name: "plugin_name",
            dependencies: [
                .product(name: "FlutterFramework", package: "FlutterFramework")
            ],
            resources: [
                // TODO: If your plugin requires a privacy manifest
                // (e.g. if it uses any required reason APIs), update the PrivacyInfo.xcprivacy file
                // to describe your plugin's privacy impact, and then uncomment this line.
                // For more information, see:
                // https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
                // .process("PrivacyInfo.xcprivacy"),
​
                // TODO: If you have other resources that need to be bundled with your plugin, refer to
                // the following instructions to add them:
                // https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
            ]
        )
    ]
)`
Update the[supported platforms](https://developer.apple.com/documentation/packagedescription/supportedplatform)in your`Package.swift`file.

`Package.swift`
`platforms: [
        // TODO: Update the platforms your plugin supports.
        // If your plugin only supports iOS, remove `.macOS(...)`.
        // If your plugin only supports macOS, remove `.iOS(...)`.
        .iOS("13.0"),
        .macOS("10.15")
    ],`
Update the package, library, and target names in your`Package.swift`file.

`Package.swift`
`let package = Package(
    // TODO: Update your plugin name.
    name: "plugin_name",
    platforms: [
        .iOS("13.0"),
        .macOS("10.15")
    ],
    products: [
        // TODO: Update your library and target names.
        // If the plugin name contains "_", replace with "-" for the library name
        .library(name: "plugin-name", targets: ["plugin_name"])
    ],
    dependencies: [],
    targets: [
        .target(
            // TODO: Update your target name.
            name: "plugin_name",
            dependencies: [],
            resources: [
                // TODO: If your plugin requires a privacy manifest
                // (e.g. if it uses any required reason APIs), update the PrivacyInfo.xcprivacy file
                // to describe your plugin's privacy impact, and then uncomment this line.
                // For more information, see:
                // https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
                // .process("PrivacyInfo.xcprivacy"),
​
                // TODO: If you have other resources that need to be bundled with your plugin, refer to
                // the following instructions to add them:
                // https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
            ]
        )
    ]
)`
If your plugin has a[PrivacyInfo.xcprivacyfile](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files), move it to`ios/plugin_name/Sources/plugin_name/PrivacyInfo.xcprivacy`and uncomment
                            the resource in the`Package.swift`file.

`PrivacyInfo.xcprivacy`
`ios/plugin_name/Sources/plugin_name/PrivacyInfo.xcprivacy`
`Package.swift`
`resources: [
                // TODO: If your plugin requires a privacy manifest
                // (e.g. if it uses any required reason APIs), update the PrivacyInfo.xcprivacy file
                // to describe your plugin's privacy impact, and then uncomment this line.
                // For more information, see:
                // https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
                .process("PrivacyInfo.xcprivacy"),
​
                // TODO: If you have other resources that need to be bundled with your plugin, refer to
                // the following instructions to add them:
                // https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
            ],`
Move any resource files from`ios/Assets`to`ios/plugin_name/Sources/plugin_name`(or a subdirectory).
                            Add the resource files to your`Package.swift`file, if applicable.
                            For more instructions, see[https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package](https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package).

`ios/Assets`
`ios/plugin_name/Sources/plugin_name`
`Package.swift`
Move all files from`ios/Classes`to`ios/plugin_name/Sources/plugin_name`.

`ios/Classes`
`ios/plugin_name/Sources/plugin_name`
**New in Flutter 3.41!**Add the FlutterFramework as a dependency and update Dart/Flutter version.

Update`Package.swift`to include`FlutterFramework`:

`Package.swift`
`FlutterFramework`
`dependencies: [
    .package(name: "FlutterFramework", path: "../FlutterFramework")
],
targets: [
    .target(
        // TODO: Update your target name.
        name: "plugin_name",
        dependencies: [
            .product(name: "FlutterFramework", package: "FlutterFramework")
        ],`
In`pubspec.yaml`, update versions to:

`pubspec.yaml`
`environment:
  sdk: ^3.11.0
  flutter: ">=3.41.0"`
The`ios/Assets`,`ios/Resources`, and`ios/Classes`directories should now
                            be empty and can be deleted.

`ios/Assets`
`ios/Resources`
`ios/Classes`
If your plugin uses[Pigeon](https://pub.dev/packages/pigeon), update your Pigeon input file.

`kotlinOptions: KotlinOptions(),
javaOut: 'android/app/src/main/java/io/flutter/plugins/Messages.java',
javaOptions: JavaOptions(),
swiftOut: 'ios/Classes/messages.g.swift',
swiftOut: 'ios/plugin_name/Sources/plugin_name/messages.g.swift',
swiftOptions: SwiftOptions(),`
Update your`Package.swift`file with any customizations you might need.

`Package.swift`
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Open the`ios/plugin_name/`directory in Xcode.

`ios/plugin_name/`
In Xcode, open your`Package.swift`file.
                                Verify Xcode doesn't produce any warnings or errors for this file.

`Package.swift`
If your`ios/plugin_name.podspec`file has[CocoaPodsdependency](https://guides.cocoapods.org/syntax/podspec.html#dependency)s,
                                add the corresponding[Swift Package Manager dependencies](https://developer.apple.com/documentation/packagedescription/package/dependency)to your`Package.swift`file.

`ios/plugin_name.podspec`
`dependency`
`Package.swift`
If your package must be linked explicitly`static`or`dynamic`([not recommended by Apple](https://developer.apple.com/documentation/packagedescription/product/library(name:type:targets:))), update the[Product](https://developer.apple.com/documentation/packagedescription/product)to define the
                                type:

`static`
`dynamic`
`products: [
    .library(name: "plugin-name", type: .static, targets: ["plugin_name"])
],`
Make any other customizations. For more information on how to write a`Package.swift`file, see[https://developer.apple.com/documentation/packagedescription](https://developer.apple.com/documentation/packagedescription).

`Package.swift`
Update your`ios/plugin_name.podspec`to point to new paths.

`ios/plugin_name.podspec`
`s.source_files = 'Classes/**/*.swift'
s.resource_bundles = {'plugin_name_privacy' => ['Resources/PrivacyInfo.xcprivacy']}
s.source_files = 'plugin_name/Sources/plugin_name/**/*.swift'
s.resource_bundles = {'plugin_name_privacy' => ['plugin_name/Sources/plugin_name/PrivacyInfo.xcprivacy']}`
Update loading of resources from bundle to use[Bundle.module](https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package#Access-a-resource-in-code).

`Bundle.module`
`#if SWIFT_PACKAGE
     let settingsURL = Bundle.module.url(forResource: "image", withExtension: "jpg")
#else
     let settingsURL = Bundle(for: Self.self).url(forResource: "image", withExtension: "jpg")
#endif`
If your`.gitignore`doesn't include`.build/`and`.swiftpm/`directories,
                            you'll want to update your`.gitignore`to include:

`.gitignore`
`.build/`
`.swiftpm/`
`.gitignore`
`.build/
.swiftpm/`
Commit your plugin's changes to your version control system.

Verify the plugin still works with CocoaPods.

1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonsh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Turn off Swift Package Manager.

`flutter config --no-enable-swift-package-manager`
Navigate to the plugin's example app.

`cd path/to/plugin/example/`
Ensure the plugin's example app builds and runs.

`flutter run`
Navigate to the plugin's top-level directory.

`cd path/to/plugin/`
Run CocoaPods validation lints.

`pod lib lint ios/plugin_name.podspec  --configuration=Debug --skip-tests --use-modular-headers --use-libraries`
`pod lib lint ios/plugin_name.podspec  --configuration=Debug --skip-tests --use-modular-headers`
Verify the plugin works with Swift Package Manager.

1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Turn on Swift Package Manager.

`flutter config --enable-swift-package-manager`
Navigate to the plugin's example app.

`cd path/to/plugin/example/`
Ensure the plugin's example app builds and runs.

`flutter run`
Open the plugin's example app in Xcode.
                                Ensure that**Package Dependencies**shows in the left**Project Navigator**.

Verify tests pass.


**If your plugin has native unit tests (XCTest), make sure you alsoupdate unit tests in the plugin's example app.**

Follow instructions for[testing plugins](https://docs.flutter.dev/testing/testing-plugins).

Replace`plugin_name`throughout this guide with the name of your plugin.
                        The example below uses`ios`, replace`ios`with`macos`/`darwin`as applicable.

`plugin_name`
`ios`
`ios`
`macos`
`darwin`
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonTests/TestFile.mobjc@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Sources/plugin_name/ImplementationFile.mobjc@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. pigeons/messages.dartdart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonpigeons/messages.dartdart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. ios/plugin_name.podspecruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. objc@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. .gitignore@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

[Turn on the Swift Package Manager feature](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-plugin-authors#how-to-turn-on-swift-package-manager).

Start by creating a directory under the`ios`,`macos`, and/or`darwin`directories.
                            Name this new directory the name of the platform package.

`ios`
`macos`
`darwin`


- …
- plugin_name/

Within this new directory, create the following files/directories:

- `Package.swift`(file)
- `Sources`(directory)
- `Sources/plugin_name`(directory)
- `Sources/plugin_name/include`(directory)
- `Sources/plugin_name/include/plugin_name`(directory)
- `Sources/plugin_name/include/plugin_name/.gitkeep`(file)

`Package.swift`
`Sources`
`Sources/plugin_name`
`Sources/plugin_name/include`
`Sources/plugin_name/include/plugin_name`
`Sources/plugin_name/include/plugin_name/.gitkeep`
- This file ensures the directory is committed.
                                  You can remove the`.gitkeep`file if other files are added to the
                                  directory.

`.gitkeep`
Your plugin should look like:



- …

- Package.swift

- .gitkeep/

Use the following template in the`Package.swift`file:

`Package.swift`
`// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.
​
import PackageDescription
​
let package = Package(
    // TODO: Update your plugin name.
    name: "plugin_name",
    platforms: [
        // TODO: Update the platforms your plugin supports.
        // If your plugin only supports iOS, remove `.macOS(...)`.
        // If your plugin only supports macOS, remove `.iOS(...)`.
        .iOS("13.0"),
        .macOS("10.15")
    ],
    products: [
        // TODO: Update your library and target names.
        // If the plugin name contains "_", replace with "-" for the library name
        .library(name: "plugin-name", targets: ["plugin_name"])
    ],
    dependencies: [],
    targets: [
        .target(
            // TODO: Update your target name.
            name: "plugin_name",
            dependencies: [],
            resources: [
                // TODO: If your plugin requires a privacy manifest
                // (e.g. if it uses any required reason APIs), update the PrivacyInfo.xcprivacy file
                // to describe your plugin's privacy impact, and then uncomment this line.
                // For more information, see:
                // https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
                // .process("PrivacyInfo.xcprivacy"),
​
                // TODO: If you have other resources that need to be bundled with your plugin, refer to
                // the following instructions to add them:
                // https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
            ],
            cSettings: [
                // TODO: Update your plugin name.
                .headerSearchPath("include/plugin_name")
            ]
        )
    ]
)`
Update the[supported platforms](https://developer.apple.com/documentation/packagedescription/supportedplatform)in your`Package.swift`file.

`Package.swift`
`platforms: [
        // TODO: Update the platforms your plugin supports.
        // If your plugin only supports iOS, remove `.macOS(...)`.
        // If your plugin only supports macOS, remove `.iOS(...)`.
        .iOS("13.0"),
        .macOS("10.15")
    ],`
Update the package, library, and target names in your`Package.swift`file.

`Package.swift`
`let package = Package(
    // TODO: Update your plugin name.
    name: "plugin_name",
    platforms: [
        .iOS("13.0"),
        .macOS("10.15")
    ],
    products: [
        // TODO: Update your library and target names.
        // If the plugin name contains "_", replace with "-" for the library name
        .library(name: "plugin-name", targets: ["plugin_name"])
    ],
    dependencies: [],
    targets: [
        .target(
            // TODO: Update your target name.
            name: "plugin_name",
            dependencies: [],
            resources: [
                // TODO: If your plugin requires a privacy manifest
                // (e.g. if it uses any required reason APIs), update the PrivacyInfo.xcprivacy file
                // to describe your plugin's privacy impact, and then uncomment this line.
                // For more information, see:
                // https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
                // .process("PrivacyInfo.xcprivacy"),
​
                // TODO: If you have other resources that need to be bundled with your plugin, refer to
                // the following instructions to add them:
                // https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
            ],
            cSettings: [
                // TODO: Update your plugin name.
                .headerSearchPath("include/plugin_name")
            ]
        )
    ]
)`
If your plugin has a[PrivacyInfo.xcprivacyfile](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files), move it to`ios/plugin_name/Sources/plugin_name/PrivacyInfo.xcprivacy`and uncomment
                            the resource in the`Package.swift`file.

`PrivacyInfo.xcprivacy`
`ios/plugin_name/Sources/plugin_name/PrivacyInfo.xcprivacy`
`Package.swift`
`resources: [
                // TODO: If your plugin requires a privacy manifest
                // (e.g. if it uses any required reason APIs), update the PrivacyInfo.xcprivacy file
                // to describe your plugin's privacy impact, and then uncomment this line.
                // For more information, see:
                // https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
                .process("PrivacyInfo.xcprivacy"),
​
                // TODO: If you have other resources that need to be bundled with your plugin, refer to
                // the following instructions to add them:
                // https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
            ],`
Move any resource files from`ios/Assets`to`ios/plugin_name/Sources/plugin_name`(or a subdirectory).
                            Add the resource files to your`Package.swift`file, if applicable.
                            For more instructions, see[https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package](https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package).

`ios/Assets`
`ios/plugin_name/Sources/plugin_name`
`Package.swift`
Move any public headers from`ios/Classes`to`ios/plugin_name/Sources/plugin_name/include/plugin_name`.

`ios/Classes`
`ios/plugin_name/Sources/plugin_name/include/plugin_name`

If you're unsure which headers are public, check your`podspec`file's[public_header_files](https://guides.cocoapods.org/syntax/podspec.html#public_header_files)attribute.
                                If this attribute isn't specified, all of your headers were public.
                                You should consider whether you want all of your headers to be public.

`podspec`
`public_header_files`
The`pluginClass`defined in your`pubspec.yaml`file must be public and
                                within this directory.

`pluginClass`
`pubspec.yaml`
Handling`modulemap`.

`modulemap`
Skip this step if your plugin does not have a`modulemap`.

`modulemap`
If you're using a`modulemap`for CocoaPods to create a Test submodule,
                            consider removing it for Swift Package Manager.
                            Note that this makes all public headers available through the module.

`modulemap`
To remove the`modulemap`for Swift Package Manager but keep it for
                            CocoaPods, exclude the`modulemap`and umbrella header in the plugin's`Package.swift`file.

`modulemap`
`modulemap`
`Package.swift`
The example below assumes the`modulemap`and umbrella header are located
                            in the`ios/plugin_name/Sources/plugin_name/include`directory.

`modulemap`
`ios/plugin_name/Sources/plugin_name/include`
`.target(
    name: "plugin_name",
    dependencies: [],
    exclude: ["include/cocoapods_plugin_name.modulemap", "include/plugin_name-umbrella.h"],`
If you want to keep your unit tests compatible with both CocoaPods and
                             Swift Package Manager, you can try the following:

`@import plugin_name;
@import plugin_name.Test;
#if __has_include(<plugin_name/plugin_name-umbrella.h>)
  @import plugin_name.Test;
#endif`
If you would like to use a custom`modulemap`with your Swift package,
                             refer to[Swift Package Manager's documentation](https://github.com/apple/swift-package-manager/blob/main/Documentation/Usage.md#creating-c-language-targets).

`modulemap`
Move all remaining files from`ios/Classes`to`ios/plugin_name/Sources/plugin_name`.

`ios/Classes`
`ios/plugin_name/Sources/plugin_name`
The`ios/Assets`,`ios/Resources`, and`ios/Classes`directories should now
                            be empty and can be deleted.

`ios/Assets`
`ios/Resources`
`ios/Classes`
If your header files are no longer in the same directory as your
                            implementation files, you should update your import statements.

For example, imagine the following migration:

- @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
- @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Before:

`ios/Classes/
├── PublicHeaderFile.h
└── ImplementationFile.m`
After:

`ios/plugin_name/Sources/plugin_name/
└── include/plugin_name/
   └── PublicHeaderFile.h
└── ImplementationFile.m`
In this example, the import statements in`ImplementationFile.m`should be updated:

`ImplementationFile.m`
`#import "PublicHeaderFile.h"
#import "./include/plugin_name/PublicHeaderFile.h"`
If your plugin uses[Pigeon](https://pub.dev/packages/pigeon), update your Pigeon input file.

`javaOptions: JavaOptions(),
objcHeaderOut: 'ios/Classes/messages.g.h',
objcSourceOut: 'ios/Classes/messages.g.m',
objcHeaderOut: 'ios/plugin_name/Sources/plugin_name/messages.g.h',
objcSourceOut: 'ios/plugin_name/Sources/plugin_name/messages.g.m',
copyrightHeader: 'pigeons/copyright.txt',`
If your`objcHeaderOut`file is no longer within the same directory as the`objcSourceOut`, you can change the`#import`using`ObjcOptions.headerIncludePath`:

`objcHeaderOut`
`objcSourceOut`
`#import`
`ObjcOptions.headerIncludePath`
`javaOptions: JavaOptions(),
objcHeaderOut: 'ios/Classes/messages.g.h',
objcSourceOut: 'ios/Classes/messages.g.m',
objcHeaderOut: 'ios/plugin_name/Sources/plugin_name/include/plugin_name/messages.g.h',
objcSourceOut: 'ios/plugin_name/Sources/plugin_name/messages.g.m',
objcOptions: ObjcOptions(
  headerIncludePath: './include/plugin_name/messages.g.h',
),
copyrightHeader: 'pigeons/copyright.txt',`
Run Pigeon to re-generate its code with the latest configuration.

Update your`Package.swift`file with any customizations you might need.

`Package.swift`
1. Package.swiftswift@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Open the`ios/plugin_name/`directory in Xcode.

`ios/plugin_name/`
In Xcode, open your`Package.swift`file.
                                Verify Xcode doesn't produce any warnings or errors for this file.

`Package.swift`
If your`ios/plugin_name.podspec`file has[CocoaPodsdependency](https://guides.cocoapods.org/syntax/podspec.html#dependency)s,
                                add the corresponding[Swift Package Manager dependencies](https://developer.apple.com/documentation/packagedescription/package/dependency)to your`Package.swift`file.

`ios/plugin_name.podspec`
`dependency`
`Package.swift`
If your package must be linked explicitly`static`or`dynamic`([not recommended by Apple](https://developer.apple.com/documentation/packagedescription/product/library(name:type:targets:))), update the[Product](https://developer.apple.com/documentation/packagedescription/product)to define the
                                type:

`static`
`dynamic`
`products: [
    .library(name: "plugin-name", type: .static, targets: ["plugin_name"])
],`
Make any other customizations. For more information on how to write a`Package.swift`file, see[https://developer.apple.com/documentation/packagedescription](https://developer.apple.com/documentation/packagedescription).

`Package.swift`
Update your`ios/plugin_name.podspec`to point to new paths.

`ios/plugin_name.podspec`
`s.source_files = 'Classes/**/*.{h,m}'
s.public_header_files = 'Classes/**/*.h'
s.module_map = 'Classes/cocoapods_plugin_name.modulemap'
s.resource_bundles = {'plugin_name_privacy' => ['Resources/PrivacyInfo.xcprivacy']}
s.source_files = 'plugin_name/Sources/plugin_name/**/*.{h,m}'
s.public_header_files = 'plugin_name/Sources/plugin_name/include/**/*.h'
s.module_map = 'plugin_name/Sources/plugin_name/include/cocoapods_plugin_name.modulemap'
s.resource_bundles = {'plugin_name_privacy' => ['plugin_name/Sources/plugin_name/PrivacyInfo.xcprivacy']}`
Update loading of resources from bundle to use`SWIFTPM_MODULE_BUNDLE`:

`SWIFTPM_MODULE_BUNDLE`
`#if SWIFT_PACKAGE
   NSBundle *bundle = SWIFTPM_MODULE_BUNDLE;
 #else
   NSBundle *bundle = [NSBundle bundleForClass:[self class]];
 #endif
 NSURL *imageURL = [bundle URLForResource:@"image" withExtension:@"jpg"];`
If your`ios/plugin_name/Sources/plugin_name/include`directory only
                            contains a`.gitkeep`, you'll want update your`.gitignore`to include the
                            following:

`ios/plugin_name/Sources/plugin_name/include`
`.gitkeep`
`.gitignore`
`!.gitkeep`
Run`flutter pub publish --dry-run`to ensure the`include`directory
                             is published.

`flutter pub publish --dry-run`
`include`
Commit your plugin's changes to your version control system.

Verify the plugin still works with CocoaPods.

1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonsh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Turn off Swift Package Manager:

`flutter config --no-enable-swift-package-manager`
Navigate to the plugin's example app.

`cd path/to/plugin/example/`
Ensure the plugin's example app builds and runs.

`flutter run`
Navigate to the plugin's top-level directory.

`cd path/to/plugin/`
Run CocoaPods validation lints:

`pod lib lint ios/plugin_name.podspec  --configuration=Debug --skip-tests --use-modular-headers --use-libraries`
`pod lib lint ios/plugin_name.podspec  --configuration=Debug --skip-tests --use-modular-headers`
Verify the plugin works with Swift Package Manager.

1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Turn on Swift Package Manager:

`flutter config --enable-swift-package-manager`
Navigate to the plugin's example app.

`cd path/to/plugin/example/`
Ensure the plugin's example app builds and runs.

`flutter run`
Open the plugin's example app in Xcode.
                                Ensure that**Package Dependencies**shows in the left**Project Navigator**.

Verify tests pass.


**If your plugin has native unit tests (XCTest), make sure you alsoupdate unit tests in the plugin's example app.**

Follow instructions for[testing plugins](https://docs.flutter.dev/testing/testing-plugins).

## (Optional, but Recommended) Add plugin as local package in example app

If your plugin includes an example, it is recommended to add the plugin as a local package in the example app. This is not required, but provides better Xcode support when editing the plugin's source code in the example app. See[issue #179032](https://github.com/flutter/flutter/issues/179032).

### Add plugin as local package


In a terminal navigate to`my_plugin`.

`my_plugin`
Run the following command to open the example app's workspace in Xcode, (replace`ios`with`macos`if your plugin targets macOS):

`ios`
`macos`
`open example/ios/Runner.xcworkspace`

Right click**Flutter**>**Add Files to “Runner”**.

![Add Files to Runner](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/add-files-to-runner.png)

Select`my_plugin/ios/my_plugin`(or`macos`or`darwin`depending on what platforms your plugin supports).

`my_plugin/ios/my_plugin`
`macos`
`darwin`
Make sure “Reference files in place” is selected (it should be the default), and click**Finish**.

![Select Reference files in place](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/reference-files-in-place.png)

This adds the plugin as a local package, but it will be referenced by absolute path, which is not desirable for distribution. To change it to a relative path, follow the steps below.

### Change to relative path

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Copy “Full Path” for plugin from the File Inspector.

![Copy Full Path](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/copy-full-path.png)

In terminal:`open -a Xcode example/ios/Runner.xcodeproj/project.pbxproj`

`open -a Xcode example/ios/Runner.xcodeproj/project.pbxproj`
Find the following:

`path = [COPIED FULL PATH]; sourceTree = "<absolute>"`
For example:

`path = /Users/username/path/to/my_plugin/ios/my_plugin; sourceTree = "<absolute>"`
And replace with relative path:

`path = ../../ios/my_plugin; sourceTree = "<group>"`
(Adjust`ios`to`macos`or`darwin`as needed).

`ios`
`macos`
`darwin`
## How to update unit tests in a plugin's example app

If your plugin has native XCTests, you might need to update them to work with
                  Swift Package Manager if one of the following is true:

- You're using a CocoaPod dependency for the test.
- Your plugin is explicitly set to`type: .dynamic`in its`Package.swift`file.

`type: .dynamic`
`Package.swift`
To update your unit tests:

1. ios/Podfileruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. ![The project's package dependencies](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/package-dependencies.png)
1. ![Search for test-only dependencies](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/search-for-ocmock.png)
1. ![Ensure the dependency is added to the `RunnerTests` target](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/choose-package-products-test.png)

Open your`example/ios/Runner.xcworkspace`in Xcode.

`example/ios/Runner.xcworkspace`
If you were using a CocoaPod dependency for tests, such as`OCMock`,
                      you'll want to remove it from your`Podfile`file.

`OCMock`
`Podfile`
`target 'RunnerTests' do
  inherit! :search_paths
​
  pod 'OCMock', '3.5'
end`
Then in the terminal, run`pod install`in the`plugin_name_ios/example/ios`directory.

`pod install`
`plugin_name_ios/example/ios`
Navigate to**Package Dependencies**for the project.

The project's package dependencies

Click the**+**button and add any test-only dependencies by searching for
                      them in the top right search bar.

Search for test-only dependencies

Ensure the dependency is added to the`RunnerTests`Target.

`RunnerTests`
Ensure the dependency is added to the`RunnerTests`target

`RunnerTests`
Click the**Add Package**button.

If you've explicitly set your plugin's library type to`.dynamic`in its`Package.swift`file
                      ([not recommended by Apple](https://developer.apple.com/documentation/packagedescription/product/library(name:type:targets:))),
                      you'll also need to add it as a dependency to the`RunnerTests`target.

`.dynamic`
`Package.swift`
`RunnerTests`
1. ![The `Link Binary With Libraries` Build Phase in the `RunnerTests` target](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/runner-tests-link-binary-with-libraries.png)![Add `Link Binary With Libraries` Build Phase](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/add-runner-tests-link-binary-with-libraries.png)

Ensure`RunnerTests`**Build Phases**has a**Link Binary With Libraries**build phase:

`RunnerTests`
The`Link Binary With Libraries`Build Phase in the`RunnerTests`target

`Link Binary With Libraries`
`RunnerTests`
If the build phase doesn't exist already, create one.
                          Click theaddbutton and
                          then click**New Link Binary With Libraries Phase**.

Add`Link Binary With Libraries`Build Phase

`Link Binary With Libraries`
Navigate to**Package Dependencies**for the project.

Click theaddbutton.

In the dialog that opens, click the**Add Local...**button.

Navigate to`plugin_name/plugin_name_ios/ios/plugin_name_ios`and click
                          the**Add Package**button.

`plugin_name/plugin_name_ios/ios/plugin_name_ios`
Ensure that it's added to the`RunnerTests`target and click the**Add Package**button.

`RunnerTests`
Ensure tests pass**Product > Test**.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/swift-package-manager/for-plugin-authors.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-plugin-authors&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/swift-package-manager/for-plugin-authors.md).
