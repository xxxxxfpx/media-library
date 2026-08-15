> 原文链接: [https://docs.flutter.dev/tools/vs-code](https://docs.flutter.dev/tools/vs-code)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

- [Android Studio and IntelliJ](https://docs.flutter.dev/tools/android-studio)
- Visual Studio Code

## Installation and setup

[VS Code](https://code.visualstudio.com/)is a code editor to build and debug apps.
                  With the Flutter extension installed, you can compile, deploy, and debug
                  Flutter apps.

To install the latest version of VS Code,
                  follow Microsoft's instructions for the relevant platform:

- [Install on macOS](https://code.visualstudio.com/docs/setup/mac)
- [Install on Windows](https://code.visualstudio.com/docs/setup/windows)
- [Install on Linux](https://code.visualstudio.com/docs/setup/linux)

### Install the Flutter extension


Start**VS Code**.

Open a browser and go to the[Flutter extension](https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter)page
                      on the Visual Studio Marketplace.

Click**Install**.
                      Installing the Flutter extension also installs the Dart extension.

### Validate your VS Code setup


Go to**View**>**Command Palette...**.

You can also press/++.

Type`doctor`.

`doctor`
Select**Flutter: Run Flutter Doctor**.

Once you select this command, VS Code does the following:

- Opens the**Output**panel.
- Displays**flutter (flutter)**in the dropdown on the upper right
                        of this panel.
- Displays the output of`flutter doctor`command.

`flutter doctor`
### Updating the extension

Updates to the extensions are shipped on a regular basis.
                  By default, VS Code automatically updates extensions when
                  updates are available.

To install updates yourself:

1. Click**Extensions**in the Side Bar.
1. If the Flutter extension has an available update,
                    click**Update**and then**Reload**.
1. Restart VS Code.

## Creating projects

There are a couple ways to create a new project.

### Creating a new project

To create a new Flutter project from the Flutter
                  starter app template:


Go to**View**>**Command Palette...**.

You can also press/++.

Type`flutter`.

`flutter`
Select the**Flutter: New Project**.

Press.

Select**Application**.

Press.

Select a**Project location**.

Enter your desired**Project name**.

### Opening a project from existing source code

To open an existing Flutter project:


Go to**File**>**Open**.

You can also press/+

Browse to the directory holding your existing
                      Flutter source code files.

Click**Open**.

## Editing code and viewing issues

The Flutter extension performs code analysis.
                  The code analysis can:


Highlight language syntax

Complete code based on rich type analysis

Navigate to type declarations

- Go to**Go**>**Go to Definition**.
- You can also press.

Find type usages.

- Press+.

View all current source code problems.

- Go to**View**>**Problems**.
- You can also press/++.
- The Problems pane displays any analysis issues:
![Problems pane](https://docs.flutter.dev/assets/images/docs/tools/vs-code/problems.png)

## Running and debugging

Start debugging by clicking**Run > Start Debugging**from the main IDE window, or press.

### Selecting a target device

When a Flutter project is open in VS Code,
                  you should see a set of Flutter specific entries in the status bar,
                  including a Flutter SDK version and a
                  device name (or the message**No Devices**):
![VS Code status bar](https://docs.flutter.dev/assets/images/docs/tools/vs-code/device_status_bar.png)

The Flutter extension automatically selects the last device connected.
                  However, if you have multiple devices/simulators connected, click**device**in the status bar to see a pick-list
                  at the top of the screen. Select the device you want to use for
                  running or debugging.

### Run app without breakpoints

Go to**Run**>**Start Without Debugging**.

You can also press+.

### Run app with breakpoints


If desired, set breakpoints in your source code.

Click**Run**>**Start Debugging**.
                      You can also press.
                      The status bar turns orange to show you are in a debug session.
![Debug console](https://docs.flutter.dev/assets/images/docs/tools/vs-code/debug_console.png)

- The left**Debug Sidebar**shows stack frames and variables.
- The bottom**Debug Console**pane shows detailed logging output.
- Debugging is based on a default launch configuration.
                        To customize, click the cog at the top of the**Debug Sidebar**to create a`launch.json`file.
                        You can then modify the values.

`launch.json`
### Run app in debug, profile, or release mode

Flutter offers many different build modes to run your app in.
                  You can read more about them in[Flutter's build modes](https://docs.flutter.dev/testing/build-modes).

1. json@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Open the`launch.json`file in VS Code.

`launch.json`
If you don't have a`launch.json`file:

`launch.json`

Go to**View**>**Run**.

You can also press/++

The**Run and Debug**panel displays.

Click**create a launch.json file**.

In the`configurations`section,
                      change the`flutterMode`property to
                      the build mode you want to target.

`configurations`
`flutterMode`
For example, if you want to run in debug mode,
                      your`launch.json`might look like this:

`launch.json`
`"configurations": [
  {
    "name": "Flutter",
    "request": "launch",
    "type": "dart",
    "flutterMode": "debug"
  }
]`
Run the app through the**Run**panel.

## Fast edit and refresh development cycle

Flutter offers a best-in-class developer cycle enabling you
                  to see the effect of your changes almost instantly with the*Stateful Hot Reload*feature.
                  To learn more, check out[Hot reload](https://docs.flutter.dev/tools/hot-reload).

## Advanced debugging

You might find the following advanced debugging tips useful:

### Debugging visual layout issues

During a debug session,
                  several additional debugging commands are added to the[Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette)and to the[Flutter inspector](https://docs.flutter.dev/tools/devtools/inspector).
                  When space is limited, the icon is used as the visual
                  version of the label.

Causes each RenderBox to paint a line at each of its baselines.

Shows rotating colors on layers when repainting.

Slows down animations to enable visual inspection.

Hides the debug mode banner even when running a debug build.

### Debugging external libraries

By default, debugging an external library is disabled
                  in the Flutter extension. To enable:

1. Select**Settings > Extensions > Dart Configuration**.
1. Check the`Debug External Libraries`option.

`Debug External Libraries`
## Editing tips for Flutter code

If you have additional tips we should share,[let us know](https://github.com/flutter/website/issues/new)!

### Assists & quick fixes

Assists are code changes related to a certain code identifier.
                  A number of these are available when the cursor is placed on a
                  Flutter widget identifier, as indicated by the yellow lightbulb icon.
                  To invoke the assist, click the lightbulb as shown in the following screenshot:

![Code assists](https://docs.flutter.dev/assets/images/docs/tools/vs-code/assists.png)

You can also press/+

Quick fixes are similar,
                  only they are shown with a piece of code has an error and they
                  can assist in correcting it.

This can be used when you have a widget that you want to wrap
                      in a surrounding widget, for example if you want to wrap a
                      widget in a`Row`or`Column`.

`Row`
`Column`
Similar to the assist above, but for wrapping an existing
                      list of widgets rather than an individual widget.

Changes a child argument to a children argument,
                      and wraps the argument value in a list.

Changes the implementation of a`StatelessWidget`to that of
                      a`StatefulWidget`, by creating the`State`class and moving
                      the code there.

`StatelessWidget`
`StatefulWidget`
`State`
### Snippets

Snippets can be used to speed up entering typical code structures.
                  They are invoked by typing their prefix,
                  and then selecting from the code completion window:![Snippets](https://docs.flutter.dev/assets/images/docs/tools/vs-code/snippets.png)

The Flutter extension includes the following snippets:

- Prefix`stless`: Create a new subclass of -StatelessWidget`.
- Prefix`stful`: Create a new subclass of`StatefulWidget`and its associated State subclass.
- Prefix`stanim`: Create a new subclass of`StatefulWidget`,
                    and its associated State subclass including a field initialized
                    with an`AnimationController`.

`stless`
`stful`
`StatefulWidget`
`stanim`
`StatefulWidget`
`AnimationController`
The Dart extension includes the following snippets:

| Prefix | Description | Code Example |
| --- | --- | --- |
| main | Insert a main function, used as an entry point. | void main(List<String> args) {  } |
| try | Insert a try/catch block. | try {  } catch (e) {  } |
| if | Insert an if statement. | if (condition) {  } |
| ife | Insert an if statement with an else block. | if (condition) {  } else {  } |
| switch | Insert a switch statement. | switch (variable) { case value1:  break; case value2:  break; default:  } |
| for | Insert a for loop. | for (var i = 0; i < 10; i++) {  } |
| fori | Insert a for-in loop. | for (var item in list) {  } |
| while | Insert a while loop. | while (condition) {  } |
| do | Insert a do-while loop. | do {  } while (condition); |
| fun | Insert a function definition. | void myFunction(String name) {  } |
| class | Insert a class definition. | class MyClass {  } |
| typedef | Insert a typedef. | typedef MyFunction = void Function(String); |
| test | Insert a test block. | test('My test description', () {  }); |
| group | Insert a test group block. | group('My test group', () {  }); |

`main`
`void main(List<String> args) {  }`
`try`
`try {  } catch (e) {  }`
`if`
`if (condition) {  }`
`ife`
`if (condition) {  } else {  }`
`switch`
`switch (variable) { case value1:  break; case value2:  break; default:  }`
`for`
`for (var i = 0; i < 10; i++) {  }`
`fori`
`for (var item in list) {  }`
`while`
`while (condition) {  }`
`do`
`do {  } while (condition);`
`fun`
`void myFunction(String name) {  }`
`class`
`class MyClass {  }`
`typedef`
`typedef MyFunction = void Function(String);`
`test`
`test('My test description', () {  });`
`group`
`group('My test group', () {  });`
You can also define custom snippets by executing**Configure User Snippets**from the[Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette).

### Keyboard shortcuts

To perform a hot reload during a debug session,
                      click**Hot Reload**on the**Debug Toolbar**.

You can also press+(+on macOS).

Keyboard mappings can be changed by executing the**Open Keyboard Shortcuts**command from the[Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette).

### Hot reload vs. hot restart

Hot reload works by injecting updated source code files into the
                  running Dart VM (Virtual Machine). This includes not only
                  adding new classes, but also adding methods and fields to
                  existing classes, and changing existing functions.
                  A few types of code changes cannot be hot reloaded though:

- Global variable initializers
- Static field initializers
- The`main()`method of the app

`main()`
For these changes, restart your app without
                  ending your debugging session. To perform a hot restart,
                  run the**Flutter: Hot Restart**command from the[Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette).

You can also press++or++on macOS.

## Flutter Property Editor

The Flutter Property Editor is a powerful tool provided by the[Flutter
                    extension](https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter)that lets you view and modify widget properties directly from its
                  visual interface.

### How to open the Flutter Property Editor in VS Code

1. Click on the Flutter Property Editor**icon**![Flutter Property Editor VS Code icon](https://docs.flutter.dev/assets/images/docs/tools/devtools/property-editor-icon-vscode.png)in the VS Code sidebar.
1. The Flutter Property Editor will load in the side panel.
1. Please refer to the Flutter Property Editor[documentation](https://docs.flutter.dev/tools/property-editor)for a detailed usage guide.

![Flutter Property Editor side panel in VS Code](https://docs.flutter.dev/assets/images/docs/tools/devtools/property-editor-vscode.png)

## Troubleshooting

### Known issues and feedback

All known bugs are tracked in the issue tracker:[Dart and Flutter extensions GitHub issue tracker](https://github.com/Dart-Code/Dart-Code/issues).
                  We welcome feedback,
                  both on bugs/issues and feature requests.

Prior to filing new issues:

- Do a quick search in the issue trackers to see if the
                    issue is already tracked.
- Make sure you are[up to date](#updating)with the most recent
                    version of the plugin.

When filing new issues, include[flutter doctor](https://docs.flutter.dev/resources/bug-reports/#provide-some-flutter-diagnostics)output.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/vs-code.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/vs-code&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/vs-code.md).
