> 原文链接: [https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter's Swift Package Manager integration has several benefits:

1. **Provides access to the Swift package ecosystem**.
                    Flutter plugins can use the growing ecosystem of[Swift packages](https://swiftpackageindex.com/).
1. **Simplifies Flutter installation**.
                    Xcode includes Swift Package Manager.
                    You don't need to install Ruby and CocoaPods if your project uses
                    Swift Package Manager.

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

## How to add Swift Package Manager integration

### Add to a Flutter app

- [iOS project](#10-tab-panel)
- [macOS project](#11-tab-panel)

Once you[turn on Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-turn-on-swift-package-manager), the Flutter CLI tries to migrate
                        your project the next time you run your app using the CLI.
                        This migration updates your Xcode project to use Swift Package Manager to
                        add Flutter plugin dependencies.

To migrate your project:

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

[Turn on Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-turn-on-swift-package-manager).

Run the iOS app using the Flutter CLI.

If your iOS project doesn't have Swift Package Manager integration yet, the
                            Flutter CLI tries to migrate your project and outputs something like:

`$ flutter run
Adding Swift Package Manager integration...`
The automatic iOS migration modifies the`ios/Runner.xcodeproj/project.pbxproj`and`ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`files.

`ios/Runner.xcodeproj/project.pbxproj`
`ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`
If the Flutter CLI's automatic migration fails, follow the steps in[add Swift Package Manager integration manually](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#add-to-a-flutter-app-manually).

[Optional] To check if your project is migrated:

1. ![Ensure **Run Prepare Flutter Framework Script** runs as a pre-action](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/flutter-pre-action-build-log.png)

Run the app in Xcode.

Ensure that**Run Prepare Flutter Framework Script**runs as a pre-action
                            and that`FlutterGeneratedPluginSwiftPackage`is a target dependency.

`FlutterGeneratedPluginSwiftPackage`
Ensure**Run Prepare Flutter Framework Script**runs as a pre-action

Once you[turn on Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-turn-on-swift-package-manager), the Flutter CLI tries to migrate
                        your project the next time you run your app using the CLI.
                        This migration updates your Xcode project to use Swift Package Manager to
                        add Flutter plugin dependencies.

To migrate your project:

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

[Turn on Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-turn-on-swift-package-manager).

Run the macOS app using the Flutter CLI.

If your macOS project doesn't have Swift Package Manager integration yet, the
                            Flutter CLI tries to migrate your project and outputs something like:

`$ flutter run -d macos
Adding Swift Package Manager integration...`
The automatic iOS migration modifies the`macos/Runner.xcodeproj/project.pbxproj`and`macos/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`files.

`macos/Runner.xcodeproj/project.pbxproj`
`macos/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`
If the Flutter CLI's automatic migration fails, follow the steps in[add Swift Package Manager integration manually](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#add-to-a-flutter-app-manually).

[Optional] To check if your project is migrated:

1. ![Ensure **Run Prepare Flutter Framework Script** runs as a pre-action](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/flutter-pre-action-build-log.png)

Run the app in Xcode.

Ensure that**Run Prepare Flutter Framework Script**runs as a pre-action
                            and that`FlutterGeneratedPluginSwiftPackage`is a target dependency.

`FlutterGeneratedPluginSwiftPackage`
Ensure**Run Prepare Flutter Framework Script**runs as a pre-action

### Add to a Flutter appmanually

- [iOS project](#12-tab-panel)
- [macOS project](#13-tab-panel)

Once you[turn on Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-turn-on-swift-package-manager), the Flutter CLI tries to migrate
                        your project to use Swift Package Manager the next time you run your app
                        using the CLI.

However, the Flutter CLI tool might be unable to migrate your project
                        automatically if there are unexpected modifications.

If the automatic migration fails, use the steps below to add Swift Package
                        Manager integration to a project manually.

Before migrating manually,[file an issue](https://github.com/flutter/flutter/issues/new?template=2_bug.yml); this helps the Flutter team
                        improve the automatic migration process.
                        Include the error message and, if possible, include a copy of
                        the following files in your issue:

- `ios/Runner.xcodeproj/project.pbxproj`
- `ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`(or the xcsheme for the flavor used)

`ios/Runner.xcodeproj/project.pbxproj`
`ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`
### Step 1: Add FlutterGeneratedPluginSwiftPackage Package Dependency

1. ![The project's package dependencies](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/package-dependencies.png)
1. ![Ensure that the package is added to the `Runner` target](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/choose-package-products.png)
1. ![Ensure that `FlutterGeneratedPluginSwiftPackage` was added to **Frameworks, Libraries, and Embedded Content**](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/add-generated-framework.png)

Open your app (`ios/Runner.xcworkspace`) in Xcode.

`ios/Runner.xcworkspace`
Navigate to**Package Dependencies**for the project.

The project's package dependencies

Click theaddbutton.

In the dialog that opens, click**Add Local...**.

Navigate to`ios/Flutter/ephemeral/Packages/FlutterGeneratedPluginSwiftPackage`and click**Add Package**.

`ios/Flutter/ephemeral/Packages/FlutterGeneratedPluginSwiftPackage`
Ensure that it's added to the`Runner`target and click**Add Package**.

`Runner`
Ensure that the package is added to the`Runner`target

`Runner`
Ensure that`FlutterGeneratedPluginSwiftPackage`was added to**Frameworks,
                              Libraries, and Embedded Content**.

`FlutterGeneratedPluginSwiftPackage`
Ensure that`FlutterGeneratedPluginSwiftPackage`was added to**Frameworks, Libraries, and Embedded Content**

`FlutterGeneratedPluginSwiftPackage`
### Step 2: Add Run Prepare Flutter Framework Script Pre-Action

**The following steps must be completed for each flavor.**

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button![Add **Run Prepare Flutter Framework Script** build pre-action](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/add-flutter-pre-action.png)

Go to**Product > Scheme > Edit Scheme**.

Expand the**Build**section in the left side bar.

Click**Pre-actions**.

Click theaddbutton and
                            select**New Run Script Action**from the menu.

Click the**Run Script**title and change it to:

`Run Prepare Flutter Framework Script`
Change the**Provide build settings from**to the`Runner`app.

`Runner`
Input the following in the text box:

`"$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" prepare`
Add**Run Prepare Flutter Framework Script**build pre-action

### Step 3: Run app

1. ![Ensure **Run Prepare Flutter Framework Script** runs as a pre-action](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/flutter-pre-action-build-log.png)

Run the app in Xcode.

Ensure that**Run Prepare Flutter Framework Script**runs as a pre-action
                            and that`FlutterGeneratedPluginSwiftPackage`is a target dependency.

`FlutterGeneratedPluginSwiftPackage`
Ensure**Run Prepare Flutter Framework Script**runs as a pre-action

Ensure that the app runs on the command line with`flutter run`.

`flutter run`
Once you[turn on Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-turn-on-swift-package-manager), the Flutter CLI tries to migrate
                        your project to use Swift Package Manager the next time you run your app
                        using the CLI.

However, the Flutter CLI tool might be unable to migrate your project
                        automatically if there are unexpected modifications.

If the automatic migration fails, use the steps below to add Swift Package
                        Manager integration to a project manually.

Before migrating manually,[file an issue](https://github.com/flutter/flutter/issues/new?template=2_bug.yml); this helps the Flutter team
                        improve the automatic migration process.
                        Include the error message and, if possible, include a copy of
                        the following files in your issue:

- `macos/Runner.xcodeproj/project.pbxproj`
- `macos/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`(or the xcscheme for the flavor used)

`macos/Runner.xcodeproj/project.pbxproj`
`macos/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`
### Step 1: Add FlutterGeneratedPluginSwiftPackage Package Dependency

1. ![The project's package dependencies](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/package-dependencies.png)
1. ![Ensure that the package is added to the `Runner` target](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/choose-package-products.png)
1. ![Ensure that `FlutterGeneratedPluginSwiftPackage` was added to **Frameworks, Libraries, and Embedded Content**](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/add-generated-framework.png)

Open your app (`macos/Runner.xcworkspace`) in Xcode.

`macos/Runner.xcworkspace`
Navigate to**Package Dependencies**for the project.

The project's package dependencies

Click theaddbutton.

In the dialog that opens, click the**Add Local...**.

Navigate to`macos/Flutter/ephemeral/Packages/FlutterGeneratedPluginSwiftPackage`and click the**Add Package**.

`macos/Flutter/ephemeral/Packages/FlutterGeneratedPluginSwiftPackage`
Ensure that it's added to the Runner Target and click**Add Package**.

Ensure that the package is added to the`Runner`target

`Runner`
Ensure that`FlutterGeneratedPluginSwiftPackage`was added to**Frameworks,
                              Libraries, and Embedded Content**.

`FlutterGeneratedPluginSwiftPackage`
Ensure that`FlutterGeneratedPluginSwiftPackage`was added to**Frameworks, Libraries, and Embedded Content**

`FlutterGeneratedPluginSwiftPackage`
### Step 2: Add Run Prepare Flutter Framework Script Pre-Action

**The following steps must be completed for each flavor.**

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button![Add **Run Prepare Flutter Framework Script** build pre-action](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/add-flutter-pre-action.png)

Go to**Product > Scheme > Edit Scheme**.

Expand the**Build**section in the left side bar.

Click**Pre-actions**.

Click theaddbutton
                            and select**New Run Script Action**from the menu.

Click the**Run Script**title and change it to:

`Run Prepare Flutter Framework Script`
Change the**Provide build settings from**to the`Runner`target.

`Runner`
Input the following in the text box:

`"$FLUTTER_ROOT"/packages/flutter_tools/bin/macos_assemble.sh prepare`
Add**Run Prepare Flutter Framework Script**build pre-action

### Step 3: Run app

1. ![Ensure `Run Prepare Flutter Framework Script` runs as a pre-action](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/flutter-pre-action-build-log.png)

Run the app in Xcode.

Ensure that**Run Prepare Flutter Framework Script**runs as a pre-action
                            and that`FlutterGeneratedPluginSwiftPackage`is a target dependency.

`FlutterGeneratedPluginSwiftPackage`
Ensure`Run Prepare Flutter Framework Script`runs as a pre-action

`Run Prepare Flutter Framework Script`
Ensure that the app runs on the command line with`flutter run`.

`flutter run`
### Add to an existing app (add-to-app)

Flutter's Swift Package Manager support doesn't work with add-to-app scenarios.

To keep current on status updates, consult[flutter#146957](https://github.com/flutter/flutter/issues/146957).

### Add to a custom Xcode target

Your Flutter Xcode project can have custom[Xcode targets](https://developer.apple.com/documentation/xcode/configuring-a-new-target-in-your-project)to build additional
                  products, like frameworks or unit tests.
                  You can add Swift Package Manager integration to these custom Xcode targets.

Follow the steps in[How to add Swift Package Manager integration to a projectmanually](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#add-to-a-flutter-app-manually).

In[Step 1](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#step-1-add-fluttergeneratedpluginswiftpackage-package-dependency), list item 6 use your custom target instead
                  of the`Flutter`target.

`Flutter`
In[Step 2](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#step-2-add-run-prepare-flutter-framework-script-pre-action), list item 6 use your custom target instead
                  of the`Flutter`target.

`Flutter`
## How to remove Swift Package Manager integration

To add Swift Package Manager integration, the Flutter CLI migrates your project.
                  This migration updates your Xcode project to add Flutter plugin dependencies.

To undo this migration:

1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. ![The `FlutterGeneratedPluginSwiftPackage` to remove](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/remove-generated-package.png)
1. ![The `FlutterGeneratedPluginSwiftPackage` to remove](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/remove-generated-framework.png)
1. ![The build pre-action to remove](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/remove-flutter-pre-action.png)

[Turn off Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers/#how-to-turn-off-swift-package-manager).

Clean your project:

`flutter clean`
Open your app (`ios/Runner.xcworkspace`or`macos/Runner.xcworkspace`) in
                      Xcode.

`ios/Runner.xcworkspace`
`macos/Runner.xcworkspace`
Navigate to**Package Dependencies**for the project.

Click the`FlutterGeneratedPluginSwiftPackage`package, then click
                      theremovebutton.

`FlutterGeneratedPluginSwiftPackage`
The`FlutterGeneratedPluginSwiftPackage`to remove

`FlutterGeneratedPluginSwiftPackage`
Navigate to**Frameworks, Libraries, and Embedded Content**for the`Runner`target.

`Runner`
Click`FlutterGeneratedPluginSwiftPackage`, then click
                      theremovebutton.

`FlutterGeneratedPluginSwiftPackage`
The`FlutterGeneratedPluginSwiftPackage`to remove

`FlutterGeneratedPluginSwiftPackage`
Go to**Product > Scheme > Edit Scheme**.

Expand the**Build**section in the left side bar.

Click**Pre-actions**.

Expand**Run Prepare Flutter Framework Script**.

Click thedeletebutton.

The build pre-action to remove

## How to use a Swift Package Manager Flutter plugin that requires a higher OS version

If a Swift Package Flutter Manager plugin requires a higher OS version than
                  the project, you might get an error like this:

`Target Integrity (Xcode): The package product 'plugin_name_ios' requires minimum platform version 14.0 for the iOS platform, but this target supports 12.0`
To use the plugin:

1. ![The target's **Minimum Deployments** setting](https://docs.flutter.dev/assets/images/docs/development/packages-and-plugins/swift-package-manager/minimum-deployments.png)
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. sh@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Open your app (`ios/Runner.xcworkspace`or`macos/Runner.xcworkspace`) in
                      Xcode.

`ios/Runner.xcworkspace`
`macos/Runner.xcworkspace`
Increase your app's target**Minimum Deployments**.

The target's**Minimum Deployments**setting

If you updated your iOS app's**Minimum Deployments**,
                      regenerate the iOS project's configuration files:

`flutter build ios --config-only`
If you updated your macOS app's**Minimum Deployments**,
                      regenerate the macOS project's configuration files:

`flutter build macos --config-only`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/swift-package-manager/for-app-developers.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/packages-and-plugins/swift-package-manager/for-app-developers.md).
