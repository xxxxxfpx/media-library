> 原文链接: [https://docs.flutter.dev/platform-integration/ios/ios-app-clip](https://docs.flutter.dev/platform-integration/ios/ios-app-clip)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This guide describes how to manually add another
                  Flutter-rendering iOS App Clip target to your
                  existing Flutter project or[add-to-app](https://docs.flutter.dev/add-to-app)project.

To see a working sample, see the[App Clip sample](https://github.com/flutter/samples/tree/main/ios_app_clip)on GitHub.

## Step 1 - Open project

Open your iOS Xcode project, such as`ios/Runner.xcworkspace`for full-Flutter apps.

`ios/Runner.xcworkspace`
## Step 2 - Add an App Clip target

**2.1**

Click on your project in the Project Navigator to show
                  the project settings.

Press**+**at the bottom of the target list to add a new target.

**2.2**

Select the**App Clip**type for your new target.

**2.3**

Enter your new target detail in the dialog.

Select**Storyboard**for Interface.

Select the same language as your original target for**Language**.

(In other words, to simplify the setup,
                  don't create a Swift App Clip target for
                  an Objective-C main target, and vice versa.)

**2.4**

In the following dialog,
                  activate the new scheme for the new target.

**2.5**

Back in the project settings, open the**Build Phases**tab.
                  Drag**Embedded App Clips**to above**Thin Binary**.

## Step 3 - Remove unneeded files

**3.1**

In the Project Navigator, in the newly created App Clip group,
                  delete everything except`Info.plist`and`<app clip target>.entitlements`.

`Info.plist`
`<app clip target>.entitlements`
Move files to trash.

**3.2**

If you don't use the`SceneDelegate.swift`file,
                  remove the reference to it in the`Info.plist`.

`SceneDelegate.swift`
`Info.plist`
Open the`Info.plist`file in the App Clip group.
                  Delete the entire dictionary entry for**Application Scene Manifest**.

`Info.plist`
## Step 4 - Share build configurations

This step isn't necessary for add-to-app projects
                  since add-to-app projects have their custom build
                  configurations and versions.

**4.1**

Back in the project settings,
                  select the project entry now rather than any targets.

In the**Info**tab, under the**Configurations**expandable group, expand the**Debug**,**Profile**, and**Release**entries.

For each, select the same value from the drop-down menu
                  for the App Clip target as the entry selected for the
                  normal app target.

This gives your App Clip target access to Flutter's
                  required build settings.

Set**iOS Deployment Target**to at least**16.0**to take advantage of the
                  15MB size limit.

**4.2**

In the App Clip group's`Info.plist`file, set:

`Info.plist`
- `Build version string (short)`to`$(FLUTTER_BUILD_NAME)`
- `Bundle version`to`$(FLUTTER_BUILD_NUMBER)`

`Build version string (short)`
`$(FLUTTER_BUILD_NAME)`
`Bundle version`
`$(FLUTTER_BUILD_NUMBER)`
## Step 5 - Share code and assets

### Option 1 - Share everything

Assuming the intent is to show the same Flutter UI
                  in the standard app as in the App Clip,
                  share the same code and assets.

For each of the following:`Main.storyboard`,`Assets.xcassets`,`LaunchScreen.storyboard`,`GeneratedPluginRegistrant.m`, and`AppDelegate.swift`(and`Supporting Files/main.m`if using Objective-C),
                  select the file, then in the first tab of the inspector,
                  also include the App Clip target in the`Target Membership`checkbox group.

`Main.storyboard`
`Assets.xcassets`
`LaunchScreen.storyboard`
`GeneratedPluginRegistrant.m`
`AppDelegate.swift`
`Supporting Files/main.m`
`Target Membership`
### Option 2 - Customize Flutter launch for App Clip

In this case,
                  do not delete everything listed in[Step 3](#step-3).
                  Instead, use the scaffolding and the[iOS add-to-app APIs](https://docs.flutter.dev/add-to-app/ios/add-flutter-screen)to perform a custom launch of Flutter.
                  For example to show a[custom Flutter route](https://docs.flutter.dev/add-to-app/ios/add-flutter-screen#route).

## Step 6 - Add App Clip associated domains

This is a standard step for App Clip development.
                  See the[official Apple documentation](https://developer.apple.com/documentation/app_clips/creating_an_app_clip_with_xcode#3604097).

**6.1**

Open the`<app clip target>.entitlements`file.
                  Add an`Associated Domains`Array type.
                  Add a row to the array with`appclips:<your bundle id>`.

`<app clip target>.entitlements`
`Associated Domains`
`appclips:<your bundle id>`
**6.2**

The same associated domains entitlement needs to be added
                  to your main app, as well.

Copy the`<app clip target>.entitlements`file from your
                  App Clip group to your main app group and rename it to
                  the same name as your main target
                  such as`Runner.entitlements`.

`<app clip target>.entitlements`
`Runner.entitlements`
Open the file and delete the`Parent Application Identifiers`entry for the main app's entitlement file
                  (leave that entry for the App Clip's entitlement file).

`Parent Application Identifiers`
**6.3**

Back in the project settings, select the main app's target,
                  open the**Build Settings**tab.
                  Set the**Code Signing Entitlements**setting to the
                  relative path of the second entitlements file
                  created for the main app.

## Step 7 - Integrate Flutter

These steps are not necessary for add-to-app.

**7.1**

For the Swift target,
                  set the`Objective-C Bridging Header`build setting to`Runner/Runner-Bridging-Header.h`

`Objective-C Bridging Header`
`Runner/Runner-Bridging-Header.h`
In other words,
                  the same as the main app target's build settings.

**7.2**

Now open the**Build Phases**tab. Press the**+**sign
                  and select**New Run Script Phase**.

Drag that new phase to below the**Dependencies**phase.

Expand the new phase and add this line to the script content:

`/bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" build`
Uncheck**Based on dependency analysis**.

In other words,
                  the same as the main app target's build phases.

This ensures that your Flutter Dart code is compiled
                  when running the App Clip target.

**7.3**

Press the**+**sign and select**New Run Script Phase**again.
                  Leave it as the last phase.

This time, add:

`/bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" embed_and_thin`
Uncheck**Based on dependency analysis**.

In other words,
                  the same as the main app target's build phases.

This ensures that your Flutter app and engine are embedded
                  into the App Clip bundle.

## Step 8 - Integrate plugins

**8.1**

Open the`Podfile`for your Flutter project
                  or add-to-app host project.

`Podfile`
For full-Flutter apps, replace the following section:

`target 'Runner' do
  use_frameworks!
  use_modular_headers!
​
  flutter_install_all_ios_pods File.dirname(File.realpath(__FILE__))
end`
with:

`use_frameworks!
use_modular_headers!
flutter_install_all_ios_pods File.dirname(File.realpath(__FILE__))
​
target 'Runner'
target '<name of your App Clip target>'`
At the top of the file,
                  also uncomment`platform :ios, '13.0'`and set the
                  version to the lowest of the two target's iOS
                  Deployment Target.

`platform :ios, '13.0'`
For add-to-app, add to:

`target 'MyApp' do
  install_all_flutter_pods(flutter_application_path)
end`
with:

`target 'MyApp' do
  install_all_flutter_pods(flutter_application_path)
end
​
target '<name of your App Clip target>'
  install_all_flutter_pods(flutter_application_path)
end`
**8.2**

From the command line,
                  enter your Flutter project directory
                  and then install the pod:

`cd ios
pod install`
## Run

You can now run your App Clip target from Xcode by
                  selecting your App Clip target from the scheme drop-down,
                  selecting an iOS 16 or higher device and pressing run.

To test launching an App Clip from the beginning,
                  also consult Apple's doc on[Testing Your App Clip's Launch Experience](https://developer.apple.com/documentation/app_clips/testing_your_app_clip_s_launch_experience).

## Debugging, hot reload

Unfortunately`flutter attach`cannot auto-discover
                  the Flutter session in an App Clip due to
                  networking permission restrictions.

`flutter attach`
You must then copy and paste it back into the`flutter attach`command to connect.

`flutter attach`
For example:

`flutter attach --debug-uri <copied URI>`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/ios-app-clip.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/ios/ios-app-clip&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/ios-app-clip.md).
