> 原文链接: [https://docs.flutter.dev/add-to-app/ios/project-setup](https://docs.flutter.dev/add-to-app/ios/project-setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter UI components can be incrementally added into your existing iOS
                  application as embedded frameworks.
                  To embed Flutter in your existing application,
                  consider one of the following three methods.

| Embedding Method | Methodology | Benefit |
| --- | --- | --- |
| Use CocoaPods(Recommended) | Install and use the Flutter SDK and CocoaPods. Flutter compiles theflutter_modulefrom source each time Xcode builds the iOS app. | Least complicated method to embed Flutter into your app. |
| UseiOS frameworks | Create iOS frameworks for Flutter components, embed them into your iOS, and update your existing app's build settings. | Doesn't require every developer to install the Flutter SDK and CocoaPods on their local machines. |
| Use iOS frameworks and CocoaPods | Embed the frameworks for your iOS app and the plugins in Xcode, but distribute the Flutter engine as a CocoaPods podspec. | Provides an alternative to distributing the large Flutter engine (Flutter.xcframework) library. |

`flutter_module`
`Flutter.xcframework`
When you add Flutter to your existing iOS app,
                  it[increases the size of your iOS app](https://docs.flutter.dev/resources/faq#how-big-is-the-flutter-engine).

For examples using an app built with UIKit,
                  see the iOS directories in the[add_to_app code samples](https://github.com/flutter/samples/tree/main/add_to_app).
                  For an example using SwiftUI, consult the iOS directory in[News Feed App](https://github.com/flutter/put-flutter-to-work/tree/022208184ec2623af2d113d13d90e8e1ce722365).

## Development system requirements

Flutter requires the latest version of Xcode and[CocoaPods](https://cocoapods.org/).

## Create a Flutter module

To embed Flutter into your existing application with any method,
                  create a Flutter module first.
                  Use the following command to create a Flutter module.

`$ cd /path/to/my_flutter
$ flutter create --template module my_flutter`
Flutter creates module project under`/path/to/my_flutter/`.
                  If you use the[CocoaPods method](https://docs.flutter.dev/add-to-app/ios/project-setup/?tab=embed-using-cocoapods), save the module
                  in the same parent directory as your existing iOS app.

`/path/to/my_flutter/`
From the Flutter module directory,
                  you can run the same`flutter`commands you would in any other Flutter project,
                  like`flutter run`or`flutter build ios`.
                  You can also run the module in[VS Code](https://docs.flutter.dev/tools/vs-code)or[Android Studio/IntelliJ](https://docs.flutter.dev/tools/android-studio)with the Flutter and Dart plugins.
                  This project contains a single-view example version of your module
                  before embedding it in your existing iOS app.
                  This helps when testing the Flutter-only parts of your code.

`flutter`
`flutter run`
`flutter build ios`
## Organize your module

The`my_flutter`module directory structure resembles a typical Flutter app.

`my_flutter`

- test/
- pubspec.yaml

- Runner.xcworkspace

- podhelper.rb

- main.dart

Your Dart code should be added to the`lib/`directory.
                  Your Flutter dependencies, packages, and plugins must be added to the`pubspec.yaml`file.

`lib/`
`pubspec.yaml`
The`.ios/`hidden subfolder contains an Xcode workspace where
                  you can run a standalone version of your module.
                  This wrapper project bootstraps your Flutter code.
                  It contains helper scripts to facilitate building frameworks or
                  embedding the module into your existing application with CocoaPods.

`.ios/`
## Embed a Flutter module in your iOS app

After you have developed your Flutter module,
                  you can embed it using the methods described
                  in the table at the top of the page.

You can run in**Debug**mode on a simulator or a real device,
                  and**Release**mode on a real device.

- [Use CocoaPods](#111-tab-panel)
- [Use frameworks](#112-tab-panel)
- [Use frameworks and CocoaPods](#113-tab-panel)

### Use CocoaPods and the Flutter SDK

#### Approach

This first method uses CocoaPods to embed the Flutter modules.
                        CocoaPods manages dependencies for Swift projects,
                        including Flutter code and plugins.
                        Each time Xcode builds the app,
                        CocoaPods embeds the Flutter modules.

This allows rapid iteration with the most up-to-date
                        version of your Flutter module without running additional
                        commands outside of Xcode.

To learn more about CocoaPods,
                        consult the[CocoaPods getting started guide](https://guides.cocoapods.org/using/using-cocoapods.html).

#### Watch the video

If watching a video helps you learn,
                        this video covers adding Flutter to an iOS app:

#### Requirements

Every developer working on your project must have a local version
                        of the Flutter SDK and CocoaPods installed.

#### Example project structure

This section assumes that your existing app and
                        the Flutter module reside in sibling directories.
                        If you have a different directory structure,
                        adjust the relative paths.
                        The example directory structure resembles the following:


- .ios/

- podhelper.rb

- Podfile

#### Update your Podfile

Add your Flutter modules to your Podfile configuration file.
                        This section presumes you called your Swift app`MyApp`.

`MyApp`

*(Optional)*If your existing app lacks a`Podfile`config file,
                            navigate to the root of your app directory.
                            Use the`pod init`command to create the`Podfile`file.

`Podfile`
`pod init`
`Podfile`
Update your`Podfile`config file.

`Podfile`
1. MyApp/Podfileruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. MyApp/Podfileruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. MyApp/Podfileruby@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Add the following lines after the`platform`declaration.

`platform`
`flutter_application_path = '../my_flutter'
load File.join(flutter_application_path, '.ios', 'Flutter', 'podhelper.rb')`
For each[Podfile target](https://guides.cocoapods.org/syntax/podfile.html#target)that needs to embed Flutter,
                                add a call to the`install_all_flutter_pods(flutter_application_path)`method.
                                Add these calls after the settings in the previous step.

`install_all_flutter_pods(flutter_application_path)`
`target 'MyApp' do
  install_all_flutter_pods(flutter_application_path)
end`
In the`Podfile`'s`post_install`block,
                                add a call to`flutter_post_install(installer)`.
                                This block should be the last block in the`Podfile`config file.

`Podfile`
`post_install`
`flutter_post_install(installer)`
`Podfile`
`post_install do |installer|
  flutter_post_install(installer) if defined?(flutter_post_install)
end`
To review an example`Podfile`, consult this[Flutter Podfile sample](https://github.com/flutter/samples/blob/main/add_to_app/plugin/ios_using_plugin/Podfile).

`Podfile`
#### Embed your frameworks

At build time, Xcode packages your Dart code, each Flutter plugin,
                        and the Flutter engine into their own`*.xcframework`bundles.
                        CocoaPod's`podhelper.rb`script then embeds these`*.xcframework`bundles into your project.

`*.xcframework`
`podhelper.rb`
`*.xcframework`
- `Flutter.xcframework`contains the Flutter engine.
- `App.xcframework`contains the compiled Dart code for this project.
- `<plugin>.xcframework`contains one Flutter plugin.

`Flutter.xcframework`
`App.xcframework`
`<plugin>.xcframework`
To embed the Flutter engine, your Dart code, and your Flutter plugins
                        into your iOS app, complete the following procedure.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Refresh your Flutter plugins.

If you change the Flutter dependencies in the`pubspec.yaml`file,
                            run`flutter pub get`in your Flutter module directory.
                            This refreshes the list of plugins that the`podhelper.rb`script reads.

`pubspec.yaml`
`flutter pub get`
`podhelper.rb`
`flutter pub get`
Embed the plugins and frameworks with CocoaPods.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Navigate to your iOS app project at`/path/to/MyApp/MyApp`.

`/path/to/MyApp/MyApp`
Use the`pod install`command.

`pod install`
`pod install`
Your iOS app's**Debug**and**Release**build configurations embed
                            the corresponding[Flutter components for that build mode](https://docs.flutter.dev/testing/build-modes).

Build the project.


Open`MyApp.xcworkspace`in Xcode.

`MyApp.xcworkspace`
Verify that you're opening`MyApp.xcworkspace`and
                                not opening`MyApp.xcodeproj`.
                                The`.xcworkspace`file has the CocoaPod dependencies,
                                the`.xcodeproj`doesn't.

`MyApp.xcworkspace`
`MyApp.xcodeproj`
`.xcworkspace`
`.xcodeproj`
Select**Product**>**Build**or press+.

#### Set LLDB Init File

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Generate Flutter LLDB files.

1. Within your flutter application, run the following:

`flutter build ios --config-only`
This will generate the LLDB files in the`.ios/Flutter/ephemeral`directory.

`.ios/Flutter/ephemeral`
Set the LLDB Init File.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Go to**Product > Scheme > Edit Scheme**.

Select the**Run**section in the left side bar.

Set the**LLDB Init File**using the same relative path to your Flutter
                                application as you put in your Podfile in the**Update your Podfile**section.

`$(SRCROOT)/../my_flutter/.ios/Flutter/ephemeral/flutter_lldbinit`
If your scheme already has an**LLDB Init File**, you can add Flutter's
                                LLDB file to it. The path to Flutter's LLDB Init File must be relative
                                to the location of your project's LLDB Init File.

For example, if your LLDB file is located at`/path/to/MyApp/.lldbinit`,
                                you would add the following:

`/path/to/MyApp/.lldbinit`
`command source --relative-to-command-file "../my_flutter/.ios/Flutter/ephemeral/flutter_lldbinit"`
### Link and Embed frameworks in Xcode

#### Approach

In this second method, edit your existing Xcode project,
                        generate the necessary frameworks, and embed them in your app.
                        Flutter generates iOS frameworks for Flutter itself,
                        for your compiled Dart code, and for each of your Flutter plugins.
                        Embed these frameworks and update your existing application's build settings.

#### Requirements

No additional software or hardware requirements are needed for this method.
                        Use this method in the following use cases:

- Members of your team can't install the Flutter SDK and CocoaPods
- You don't want to use CocoaPods as a dependency manager in existing iOS apps

#### Limitations

Flutter can't handle[common dependencies with xcframeworks](https://github.com/flutter/flutter/issues/130220).
                        If both the host app and the Flutter module's plugin define the
                        same pod dependency and you integrate Flutter module using this option,
                        errors result.
                        These errors include issues like`Multiple commands produce 'CommonDependency.framework'`.

`Multiple commands produce 'CommonDependency.framework'`
To work around this issue, link every plugin source in its`podspec`file
                        from the Flutter module to the host app's`Podfile`.
                        Link the source instead of the plugins'`xcframework`framework.
                        The next section explains how to[produce that framework](https://github.com/flutter/flutter/issues/114692).

`podspec`
`Podfile`
`xcframework`
To prevent the error that occurs when common dependencies exist,
                        use`flutter build ios-framework`with the`--no-plugins`flag.

`flutter build ios-framework`
`--no-plugins`
#### Example project structure

The following example assumes that you want to generate the
                        frameworks to`/path/to/MyApp/Flutter/`.

`/path/to/MyApp/Flutter/`
`$ flutter build ios-framework --output=/path/to/MyApp/Flutter/`
Run this*every time*you change code in your Flutter module.

The resulting project structure should resemble this directory tree.




- Flutter.xcframework
- App.xcframework
- FlutterPluginRegistrant.xcframework(If you have plugins with iOS-platform code)
- example_plugin.xcframework(One framework file for each plugin)

- Flutter.xcframework
- App.xcframework
- FlutterPluginRegistrant.xcframework
- example_plugin.xcframework

- Flutter.xcframework
- App.xcframework
- FlutterPluginRegistrant.xcframework
- example_plugin.xcframework

#### Procedures

How you link, embed, or both the generated frameworks
                        into your existing app in Xcode depends on the type of framework.

- Link and embed dynamic frameworks.
- Link static frameworks.[Never embed them](https://developer.apple.com/library/archive/technotes/tn2435/_index.html).

Flutter plugins might produce[static or dynamic frameworks](https://stackoverflow.com/questions/32591878/ios-is-it-a-static-or-a-dynamic-framework).
                        Link static frameworks,[neverembed them](https://developer.apple.com/library/archive/technotes/tn2435/_index.html).

If you embed a static framework into your iOS app,
                        you can't publish that app to the App Store.
                        Publishing fails with a`Found an unexpected Mach-O header code`archive error.

`Found an unexpected Mach-O header code`
##### Link all frameworks

To link the necessary frameworks, follow this procedure.


Choose the frameworks to link.

1. ![Expand the **Link Binary With Libraries** build phase in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/linked-libraries.png)
1. ![Choose frameworks to link from the **Choose frameworks and libraries to add:** dialog box in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/choose-libraries.png)

In the**Project Navigator**, click on your project.

Click the**Build Phases**tab.

Expand**Link Binary With Libraries**.

Expand the**Link Binary With Libraries**build phase in Xcode

Click**+**(plus sign).

Click**Add Other...**then**Add Files...**.

From the**Choose frameworks and libraries to add:**dialog box,
                                navigate to the`/path/to/MyApp/Flutter/Release/`directory.

`/path/to/MyApp/Flutter/Release/`
Command-click the frameworks in that directory then click**Open**.

Choose frameworks to link from the**Choose frameworks and libraries to add:**dialog box in Xcode

Update the paths to the libraries to account for build modes.

1. ![The `project-pbxproj` file open in the Xcode text editor](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/project-pbxproj.png)
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Launch the Finder.

Navigate to the`/path/to/MyApp/`directory.

`/path/to/MyApp/`
Right-click on`MyApp.xcodeproj`and select**Show Package
                                  Contents**.

`MyApp.xcodeproj`
Open`project.pbxproj`with Xcode. The file opens in Xcode's text
                                editor. This also locks**Project Navigator**until you close the text editor.

`project.pbxproj`
The`project-pbxproj`file open in the Xcode text editor

`project-pbxproj`
Find the lines that resemble the following text in the`/* Begin PBXFileReference section */`.

`/* Begin PBXFileReference section */`
`312885572C1A441C009F74FF /* Flutter.xcframework */ = {
  isa = PBXFileReference;
  expectedSignature = "AppleDeveloperProgram:S8QB4VV633:FLUTTER.IO LLC";
  lastKnownFileType = wrapper.xcframework;
  name = Flutter.xcframework;
  path = Flutter/Release/Flutter.xcframework;
  sourceTree = "<group>";
};
312885582C1A441C009F74FF /* App.xcframework */ = {
  isa = PBXFileReference;
  lastKnownFileType = wrapper.xcframework;
  name = App.xcframework;
  path = Flutter/Release/App.xcframework;
  sourceTree = "<group>";
};`
Change the`Release`text highlighted in the prior step
                                and change it to`$(CONFIGURATION)`. Also wrap the path in
                                quotation marks.

`Release`
`$(CONFIGURATION)`
`312885572C1A441C009F74FF /* Flutter.xcframework */ = {
  isa = PBXFileReference;
  expectedSignature = "AppleDeveloperProgram:S8QB4VV633:FLUTTER.IO LLC";
  lastKnownFileType = wrapper.xcframework;
  name = Flutter.xcframework;
  path = "Flutter/$(CONFIGURATION)/Flutter.xcframework";
  sourceTree = "<group>";
};
312885582C1A441C009F74FF /* App.xcframework */ = {
  isa = PBXFileReference;
  lastKnownFileType = wrapper.xcframework;
  name = App.xcframework;
  path = "Flutter/$(CONFIGURATION)/App.xcframework";
  sourceTree = "<group>";
};`
Update the search paths.

1. ![Update **Framework Search Paths** in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/framework-search-paths.png)

Click the**Build Settings**tab.

Navigate to**Search Paths**

Double-click to the right of**Framework Search Paths**.

In the combo box, click**+**(plus sign).

Type`$(inherited)`.
                                and press.

`$(inherited)`
Click**+**(plus sign).

Type`$(PROJECT_DIR)/Flutter/$(CONFIGURATION)/`and press.

`$(PROJECT_DIR)/Flutter/$(CONFIGURATION)/`
Update**Framework Search Paths**in Xcode

After linking the frameworks, they should display in the**Frameworks, Libraries, and Embedded Content**section of your target's**General**settings.

##### Embed the dynamic frameworks

To embed your dynamic frameworks, complete the following procedure.

1. ![Select **Embed & Sign** for each of your frameworks in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/choose-to-embed.png)
1. ![The expanded **Embed Frameworks** build phase in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/embed-xcode.png)

Navigate to**General**>**Frameworks, Libraries, and Embedded Content**.

Click on each of your dynamic frameworks and select**Embed & Sign**.

Select**Embed & Sign**for each of your frameworks in Xcode

Don't include any static frameworks,
                            including`FlutterPluginRegistrant.xcframework`.

`FlutterPluginRegistrant.xcframework`
Click the**Build Phases**tab.

Expand**Embed Frameworks**.
                            Your dynamic frameworks should display in that section.

The expanded**Embed Frameworks**build phase in Xcode

Build the project.


Open`MyApp.xcworkspace`in Xcode.

`MyApp.xcworkspace`
Verify that you're opening`MyApp.xcworkspace`and
                                not opening`MyApp.xcodeproj`.
                                The`.xcworkspace`file has the CocoaPod dependencies,
                                the`.xcodeproj`doesn't.

`MyApp.xcworkspace`
`MyApp.xcodeproj`
`.xcworkspace`
`.xcodeproj`
Select**Product**>**Build**or press+.

#### Set LLDB Init File

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Generate Flutter LLDB files.

1. Within your flutter application, re-run`flutter build ios-framework`if
                              you haven't already:

`flutter build ios-framework`
`$ flutter build ios-framework --output=/path/to/MyApp/Flutter/`
This will generate the LLDB files in the`/path/to/MyApp/Flutter/`directory.

`/path/to/MyApp/Flutter/`
Set the LLDB Init File.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Go to**Product > Scheme > Edit Scheme**.

Select the**Run**section in the left side bar.

Set the**LLDB Init File**to the following:

`$(PROJECT_DIR)/Flutter/flutter_lldbinit`
If your scheme already has an**LLDB Init File**, you can add Flutter's
                                LLDB file to it. The path to Flutter's LLDB Init File must be relative
                                to the location of your project's LLDB Init File.

For example, if your LLDB file is located at`/path/to/MyApp/.lldbinit`,
                                you would add the following:

`/path/to/MyApp/.lldbinit`
`command source --relative-to-command-file "Flutter/flutter_lldbinit"`
### Use frameworks in Xcode and Flutter framework as podspec

#### Approach

This method generates Flutter as a CocoaPods podspec instead of
                        distributing the large`Flutter.xcframework`to other developers,
                        machines, or continuous integration systems.
                        Flutter still generates iOS frameworks for your compiled Dart code,
                        and for each of your Flutter plugins.
                        Embed these frameworks and update your existing application's build settings.

`Flutter.xcframework`
#### Requirements

No additional software or hardware requirements are needed for this method.
                        Use this method in the following use cases:

- Members of your team can't install the Flutter SDK and CocoaPods
- You don't want to use CocoaPods as a dependency manager in existing iOS apps

#### Limitations

Flutter can't handle[common dependencies with xcframeworks](https://github.com/flutter/flutter/issues/130220).
                        If both the host app and the Flutter module's plugin define the
                        same pod dependency and you integrate Flutter module using this option,
                        errors result.
                        These errors include issues like`Multiple commands produce 'CommonDependency.framework'`.

`Multiple commands produce 'CommonDependency.framework'`
To work around this issue, link every plugin source in its`podspec`file
                        from the Flutter module to the host app's`Podfile`.
                        Link the source instead of the plugins'`xcframework`framework.
                        The next section explains how to[produce that framework](https://github.com/flutter/flutter/issues/114692).

`podspec`
`Podfile`
`xcframework`
To prevent the error that occurs when common dependencies exist,
                        use`flutter build ios-framework`with the`--no-plugins`flag.

`flutter build ios-framework`
`--no-plugins`
This method only works with the`beta`or`stable`[release channels](https://docs.flutter.dev/install/upgrade#switching-flutter-channels).

`beta`
`stable`
#### Example project structure

The following example assumes that you want to generate the
                        frameworks to`/path/to/MyApp/Flutter/`.

`/path/to/MyApp/Flutter/`
`$ flutter build ios-framework --output=/path/to/MyApp/Flutter/`
Run this*every time*you change code in your Flutter module.

The resulting project structure should resemble this directory tree.




- Flutter.xcframework
- App.xcframework
- FlutterPluginRegistrant.xcframework(If you have plugins with iOS-platform code)
- example_plugin.xcframework(One framework file for each plugin)

- Flutter.xcframework
- App.xcframework
- FlutterPluginRegistrant.xcframework
- example_plugin.xcframework

- Flutter.xcframework
- App.xcframework
- FlutterPluginRegistrant.xcframework
- example_plugin.xcframework

#### Add Flutter engine to your Podfile

Host apps using CocoaPods can add the Flutter engine to their Podfile.

`pod 'Flutter', :podspec => '/path/to/MyApp/Flutter/[build mode]/Flutter.podspec'`
#### Link and embed app and plugin frameworks

Flutter plugins might produce[static or dynamic frameworks](https://stackoverflow.com/questions/32591878/ios-is-it-a-static-or-a-dynamic-framework).
                        Link static frameworks,[neverembed them](https://developer.apple.com/library/archive/technotes/tn2435/_index.html).

If you embed a static framework into your iOS app,
                        you can't publish that app to the App Store.
                        Publishing fails with a`Found an unexpected Mach-O header code`archive error.

`Found an unexpected Mach-O header code`
##### Link all frameworks

To link the necessary frameworks, follow this procedure.


Choose the frameworks to link.

1. ![Expand the **Link Binary With Libraries** build phase in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/linked-libraries.png)
1. ![Choose frameworks to link from the **Choose frameworks and libraries to add:** dialog box in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/choose-libraries.png)

In the**Project Navigator**, click on your project.

Click the**Build Phases**tab.

Expand**Link Binary With Libraries**.

Expand the**Link Binary With Libraries**build phase in Xcode

Click**+**(plus sign).

Click**Add Other...**then**Add Files...**.

From the**Choose frameworks and libraries to add:**dialog box,
                                navigate to the`/path/to/MyApp/Flutter/Release/`directory.

`/path/to/MyApp/Flutter/Release/`
Command-click the frameworks in that directory then click**Open**.

Choose frameworks to link from the**Choose frameworks and libraries to add:**dialog box in Xcode

Update the paths to the libraries to account for build modes.

1. ![The `project-pbxproj` file open in the Xcode text editor](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/project-pbxproj.png)
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Launch the Finder.

Navigate to the`/path/to/MyApp/`directory.

`/path/to/MyApp/`
Right-click on`MyApp.xcodeproj`and select**Show Package
                                  Contents**.

`MyApp.xcodeproj`
Open`project.pbxproj`with Xcode. The file opens in Xcode's text
                                editor. This also locks**Project Navigator**until you close the text editor.

`project.pbxproj`
The`project-pbxproj`file open in the Xcode text editor

`project-pbxproj`
Find the lines that resemble the following text in the`/* Begin PBXFileReference section */`.

`/* Begin PBXFileReference section */`
`312885572C1A441C009F74FF /* Flutter.xcframework */ = {
  isa = PBXFileReference;
  expectedSignature = "AppleDeveloperProgram:S8QB4VV633:FLUTTER.IO LLC";
  lastKnownFileType = wrapper.xcframework;
  name = Flutter.xcframework;
  path = Flutter/Release/Flutter.xcframework;
  sourceTree = "<group>";
};
312885582C1A441C009F74FF /* App.xcframework */ = {
  isa = PBXFileReference;
  lastKnownFileType = wrapper.xcframework;
  name = App.xcframework;
  path = Flutter/Release/App.xcframework;
  sourceTree = "<group>";
};`
Change the`Release`text highlighted in the prior step
                                and change it to`$(CONFIGURATION)`. Also wrap the path in
                                quotation marks.

`Release`
`$(CONFIGURATION)`
`312885572C1A441C009F74FF /* Flutter.xcframework */ = {
  isa = PBXFileReference;
  expectedSignature = "AppleDeveloperProgram:S8QB4VV633:FLUTTER.IO LLC";
  lastKnownFileType = wrapper.xcframework;
  name = Flutter.xcframework;
  path = "Flutter/$(CONFIGURATION)/Flutter.xcframework";
  sourceTree = "<group>";
};
312885582C1A441C009F74FF /* App.xcframework */ = {
  isa = PBXFileReference;
  lastKnownFileType = wrapper.xcframework;
  name = App.xcframework;
  path = "Flutter/$(CONFIGURATION)/App.xcframework";
  sourceTree = "<group>";
};`
Update the search paths.

1. ![Update **Framework Search Paths** in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/framework-search-paths.png)

Click the**Build Settings**tab.

Navigate to**Search Paths**

Double-click to the right of**Framework Search Paths**.

In the combo box, click**+**(plus sign).

Type`$(inherited)`.
                                and press.

`$(inherited)`
Click**+**(plus sign).

Type`$(PROJECT_DIR)/Flutter/$(CONFIGURATION)/`and press.

`$(PROJECT_DIR)/Flutter/$(CONFIGURATION)/`
Update**Framework Search Paths**in Xcode

After linking the frameworks, they should display in the**Frameworks, Libraries, and Embedded Content**section of your target's**General**settings.

##### Embed the dynamic frameworks

To embed your dynamic frameworks, complete the following procedure.

1. ![Select **Embed & Sign** for each of your frameworks in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/choose-to-embed.png)
1. ![The expanded **Embed Frameworks** build phase in Xcode](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/embed-xcode.png)

Navigate to**General**>**Frameworks, Libraries, and Embedded Content**.

Click on each of your dynamic frameworks and select**Embed & Sign**.

Select**Embed & Sign**for each of your frameworks in Xcode

Don't include any static frameworks,
                            including`FlutterPluginRegistrant.xcframework`.

`FlutterPluginRegistrant.xcframework`
Click the**Build Phases**tab.

Expand**Embed Frameworks**.
                            Your dynamic frameworks should display in that section.

The expanded**Embed Frameworks**build phase in Xcode

Build the project.


Open`MyApp.xcworkspace`in Xcode.

`MyApp.xcworkspace`
Verify that you're opening`MyApp.xcworkspace`and
                                not opening`MyApp.xcodeproj`.
                                The`.xcworkspace`file has the CocoaPod dependencies,
                                the`.xcodeproj`doesn't.

`MyApp.xcworkspace`
`MyApp.xcodeproj`
`.xcworkspace`
`.xcodeproj`
Select**Product**>**Build**or press+.

#### Set LLDB Init File

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Generate Flutter LLDB files.

1. Within your flutter application, re-run`flutter build ios-framework`if
                              you haven't already:

`flutter build ios-framework`
`$ flutter build ios-framework --output=/path/to/MyApp/Flutter/`
This will generate the LLDB files in the`/path/to/MyApp/Flutter/`directory.

`/path/to/MyApp/Flutter/`
Set the LLDB Init File.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Go to**Product > Scheme > Edit Scheme**.

Select the**Run**section in the left side bar.

Set the**LLDB Init File**to the following:

`$(PROJECT_DIR)/Flutter/flutter_lldbinit`
If your scheme already has an**LLDB Init File**, you can add Flutter's
                                LLDB file to it. The path to Flutter's LLDB Init File must be relative
                                to the location of your project's LLDB Init File.

For example, if your LLDB file is located at`/path/to/MyApp/.lldbinit`,
                                you would add the following:

`/path/to/MyApp/.lldbinit`
`command source --relative-to-command-file "Flutter/flutter_lldbinit"`
## Set local network privacy permissions

On iOS 14 and later, enable the Dart multicast DNS service in the**Debug**version of your iOS app.
                  This adds[debugging functionalities such as hot-reload and DevTools](https://docs.flutter.dev/add-to-app/debugging)using`flutter attach`.

`flutter attach`
To set local network privacy permissions only in the Debug version of your app,
                  create a separate`Info.plist`per build configuration.
                  SwiftUI projects start without an`Info.plist`file.
                  If you need to create a property list,
                  you can do so through Xcode or text editor.
                  The following instructions assume the default**Debug**and**Release**.
                  Adjust the names as needed depending on your app's build configurations.

`Info.plist`
`Info.plist`

Create a new property list.


Open your project in Xcode.

In the**Project Navigator**, click on the project name.

From the**Targets**list in the Editor pane, click on your app.

Click the**Info**tab.

Expand**Custom iOS Target Properties**.

Right-click on the list and select**Add Row**.

From the dropdown menu, select**Bonjour Services**.
                          This creates a new property list in the project directory
                          called`Info`. This displays as`Info.plist`in the Finder.

`Info`
`Info.plist`
Rename the`Info.plist`to`Info-Debug.plist`

`Info.plist`
`Info-Debug.plist`

Click on**Info**file in the project list at the left.

In the**Identity and Type**panel at the right,
                          change the**Name**from`Info.plist`to`Info-Debug.plist`.

`Info.plist`
`Info-Debug.plist`
Create a Release property list.


In the**Project Navigator**, click on`Info-Debug.plist`.

`Info-Debug.plist`
Select**File**>**Duplicate...**.
                          You can also press++.

In the dialog box, set the**Save As:**field to`Info-Release.plist`and click**Save**.

`Info-Release.plist`
Add the necessary properties to the**Debug**property list.

1. ![The `Info-Debug` property list with the **Bonjour Services** and **Privacy - Local Network Usage Description** keys added](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/debug-plist.png)

In the**Project Navigator**, click on`Info-Debug.plist`.

`Info-Debug.plist`
Add the String value`_dartVmService._tcp`to the**Bonjour Services**array.

`_dartVmService._tcp`
*(Optional)*To set your desired customized permission dialog text,
                          add the key**Privacy - Local Network Usage Description**.

The`Info-Debug`property list with the**Bonjour Services**and**Privacy - Local Network Usage Description**keys added

`Info-Debug`
Set the target to use different property lists for different build modes.

1. ![Updating the `Info.plist` build setting to use build mode-specific property lists](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/set-plist-build-setting.png)![The updated **Info.plist File** build setting displaying the configuration variations](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/plist-build-setting.png)

In the**Project Navigator**, click on your project.

Click the**Build Settings**tab.

Click**All**and**Combined**sub-tabs.

In the Search box, type`plist`.
                          This limits the settings to those that include property lists.

`plist`
Scroll through the list until you see**Packaging**.

Click on the**Info.plist File**setting.

Change the**Info.plist File**value
                          from`path/to/Info.plist`to`path/to/Info-$(CONFIGURATION).plist`.

`path/to/Info.plist`
`path/to/Info-$(CONFIGURATION).plist`
Updating the`Info.plist`build setting to use build mode-specific property lists

`Info.plist`
This resolves to the path**Info-Debug.plist**in**Debug**and**Info-Release.plist**in**Release**.

The updated**Info.plist File**build setting displaying the configuration variations

Remove the**Release**property list from the**Build Phases**.

1. ![The **Copy Bundle** build phase displaying the **Info-Release.plist** setting. Remove this setting.](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/copy-bundle.png)

In the**Project Navigator**, click on your project.

Click the**Build Phases**tab.

Expand**Copy Bundle Resources**.

If this list includes`Info-Release.plist`,
                          click on it and then click the**-**(minus sign) under it
                          to remove the property list from the resources list.

`Info-Release.plist`
The**Copy Bundle**build phase displaying the**Info-Release.plist**setting. Remove this setting.

The first Flutter screen your Debug app loads prompts
                      for local network permission.

Click**OK**.

*(Optional)*To grant permission before the app loads, enable**Settings > Privacy > Local Network > Your App**.

## Mitigate known issue with Apple Silicon Macs

On[Macs running Apple Silicon](https://support.apple.com/en-us/116943),
                  the host app builds for an`arm64`simulator.
                  While Flutter supports`arm64`simulators, some plugins might not.
                  If you use one of these plugins, you might see a compilation error like**Undefined symbols for architecture arm64**.
                  If this occurs,
                  exclude`arm64`from the simulator architectures in your host app.

`arm64`
`arm64`
`arm64`
1. ![Add `arm64` as an excluded architecture for your app](https://docs.flutter.dev/assets/images/docs/development/add-to-app/ios/project-setup/excluded-archs.png)

In the**Project Navigator**, click on your project.

Click the**Build Settings**tab.

Click**All**and**Combined**sub-tabs.

Under**Architectures**, click on**Excluded Architectures**.

Expand to see the available build configurations.

Click**Debug**.

Click the**+**(plus sign).

Select**iOS Simulator**.

Double-click in the value column for**Any iOS Simulator SDK**.

Click the**+**(plus sign).

Type`arm64`in the**Debug > Any iOS Simulator SDK**dialog box.

`arm64`
Add`arm64`as an excluded architecture for your app

`arm64`
Pressto close this dialog box.

Repeat these steps for the**Release**build mode.

Repeat for any iOS unit test targets.

## Next steps

You can now[add a Flutter screen](https://docs.flutter.dev/add-to-app/ios/add-flutter-screen)to your existing iOS app.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/ios/project-setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/add-to-app/ios/project-setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/ios/project-setup.md).
