> 原文链接: [https://docs.flutter.dev/add-to-app/debugging](https://docs.flutter.dev/add-to-app/debugging)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Once you've integrated the Flutter module to your project and used
                  Flutter's platform APIs to run the Flutter engine and/or UI,
                  you can then build and run your Android or iOS app the same way
                  you run normal Android or iOS apps.

Flutter now powers the UI wherever your code includes`FlutterActivity`or`FlutterViewController`.

`FlutterActivity`
`FlutterViewController`
## Overview

You might be used to having your suite of favorite Flutter debugging tools
                  available when running`flutter run`or an equivalent command from an IDE.
                  But you can also use all your Flutter[debugging functionalities](https://docs.flutter.dev/testing/debugging)such as
                  hot reload, performance overlays, DevTools, and setting breakpoints in
                  add-to-app scenarios.

`flutter run`
The`flutter attach`command provides these functionalities.
                  To run this command, you can use the SDK's CLI tools, VS Code
                  or IntelliJ IDEA or Android Studio.

`flutter attach`
The`flutter attach`command connects once you run your`FlutterEngine`.
                  It remains attached until you dispose your`FlutterEngine`.
                  You can invoke`flutter attach`before starting your engine.
                  The`flutter attach`command waits for the next available Dart VM that
                  your engine hosts.

`flutter attach`
`FlutterEngine`
`FlutterEngine`
`flutter attach`
`flutter attach`
## Debug from the Terminal

To attach from the terminal, run`flutter attach`.
                  To select a specific target device, add`-d <deviceId>`.

`flutter attach`
`-d <deviceId>`
`$ flutter attach`
The command should print output resembling the following:

`Syncing files to device iPhone 15 Pro...
 7,738ms (!)

To hot reload the changes while running, press "r".
To hot restart (and rebuild state). press "R".`
## Debug iOS extension in Xcode and VS Code

#### Build the iOS version of the Flutter app in the Terminal

To generate the needed iOS platform dependencies,
                  run the`flutter build`command.

`flutter build`
`$ flutter build ios --config-only --no-codesign --debug`
`Warning: Building for device with codesigning disabled. You will have to manually codesign before deploying to device.
Building com.example.myApp for device (ios)...`
- [Start from VS Code](#109-tab-panel)
- [Start from Xcode](#110-tab-panel)

#### Start debugging with VS Code first

If you use VS Code to debug most of your code, start with this section.

##### Start the Dart debugger in VS Code


To open the Flutter app directory, go to**File**>**Open Folder...**and choose the`my_app`directory.

`my_app`
Open the`lib/main.dart`file.

`lib/main.dart`
If you can build an app for more than one device,
                            you must select the device first.

Go to**View**>**Command Palette...**

You can also press/++.

Type`flutter select`.

`flutter select`
Click the**Flutter: Select Device**command.

Choose your target device.

Click the debug icon
                            (![VS Code's bug icon to trigger the debugging mode of a Flutter app](https://docs.flutter.dev/assets/images/docs/testing/debugging/vscode-ui/icons/debug.png)).
                            This opens the**Debug**pane and launches the app.
                            Wait for the app to launch on the device and for the debug pane to
                            indicate**Connected**.
                            The debugger takes longer to launch the first time.
                            Subsequent launches start faster.

This Flutter app contains two buttons:

- **Launch in browser**: This button opens this page in the
                              default browser of your device.
- **Launch in app**: This button opens this page within your app.
                              This button only works for iOS or Android. Desktop apps launch a browser.

##### Enable automatic attachment

You can configure VS Code to attach to your Flutter module project
                        whenever you start debugging.
                        To enable this feature,
                        create a`.vscode/launch.json`file in your Flutter module project.

`.vscode/launch.json`

Go to**View**>**Run**.

You can also press/++.

VS Code displays the**Run and Debug**sidebar.

In this sidebar, click**create a launch.json file**.

VS Code displays the**Select debugger**menu at the top.

Select**Dart & Flutter**.

VS Code creates then opens the`.vscode/launch.json`file.

`.vscode/launch.json`
`{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "my_app",
            "request": "launch",
            "type": "dart"
        },
        {
            "name": "my_app (profile mode)",
            "request": "launch",
            "type": "dart",
            "flutterMode": "profile"
        },
        {
            "name": "my_app (release mode)",
            "request": "launch",
            "type": "dart",
            "flutterMode": "release"
        }
    ]
}`
To attach, go to**Run**>**Start Debugging**.

You can also press.

##### Attach to the Flutter process in Xcode

To attach to the Flutter app in Xcode:


Go to**Debug**>**Attach to Process**.

Select**Runner**. It should be at the top of the**Attach to Process**menu under the**Likely Targets**heading.

#### Start debugging with Xcode first

If you use Xcode to debug most of your code, start with this section.

##### Start the Xcode debugger

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Open`ios/Runner.xcworkspace`from your Flutter app directory.

`ios/Runner.xcworkspace`
Select the correct device using the**Scheme**menu in the toolbar.

If you have no preference, choose**iPhone Pro 14**.

Run this Runner as a normal app in Xcode.

When the run completes, the**Debug**area at the bottom of Xcode displays
                             a message with the Dart VM service URI. It resembles the following response:

`2023-07-12 14:55:39.966191-0500 Runner[58361:53017145]
    flutter: The Dart VM service is listening on
    http://127.0.0.1:50642/00wEOvfyff8=/`
Copy the Dart VM service URI.

##### Attach to the Dart VM in VS Code


To open the command palette, go to**View**>**Command Palette...**

You can also press++.

Type`debug`.

`debug`
Click the**Debug: Attach to Flutter on Device**command.

In the**Paste an VM Service URI**box, paste the URI you copied
                             from Xcode and press.

## Debug Android extension in Android Studio


To open the Flutter app directory, go to**File**>**Open...**and choose the`my_app`directory.

`my_app`
Open the`lib/main.dart`file.

`lib/main.dart`
Choose a virtual Android device.
                      Go to the toolbar, open the leftmost dropdown menu, and click on**Open Android Emulator: <device>**.

You can choose any installed emulator that's doesn't include`arm64`.

`arm64`
From that same menu, select the virtual Android device.

From the toolbar, click**Run 'main.dart'**.

You can also press++.

After the app displays in the emulator, continue to the next step.

## Debug without USB connection

To debug your app over Wi-Fi on an iOS or Android device,
                  use`flutter attach`.

`flutter attach`
### Debug over Wi-Fi on iOS devices

For an iOS target, complete the follow steps:


Verify your device connects to Xcode over Wi-Fi
                      as described in the[iOS setup guide](https://docs.flutter.dev/platform-integration/ios/setup).

On your macOS development machine,
                      open**Xcode**>**Product**>**Scheme**>**Edit Scheme...**.

You can also press+.

Click**Run**.

Click**Arguments**.

In**Arguments Passed On Launch**, Click**+**.


If your dev machine uses IPv4, add`--vm-service-host=0.0.0.0`.

`--vm-service-host=0.0.0.0`
If your dev machine uses IPv6, add`--vm-service-host=::0`.

`--vm-service-host=::0`
<DashImage figure img-class="site-mobile-screenshot border" image="development/add-to-app/debugging/wireless-port.png" caption="Arguments Passed On Launch with an IPv4 network added", width="100%" />

#### To determine if you're on an IPv6 network


Open**Settings**>**Wi-Fi**.

Click on your connected network.

Click**Details...**

Click**TCP/IP**.

Check for an**IPv6 address**section.

WiFi dialog box for macOS System Settings

### Debug over Wi-Fi on Android devices

Verify your device connects to Android Studio over Wi-Fi
                  as described in the[Android setup guide](https://docs.flutter.dev/platform-integration/android/setup#set-up-devices).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/debugging.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/add-to-app/debugging&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/debugging.md).
