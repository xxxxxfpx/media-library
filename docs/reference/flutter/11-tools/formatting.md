> 原文链接: [https://docs.flutter.dev/tools/formatting](https://docs.flutter.dev/tools/formatting)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

While your code might follow any preferred style—in our
                  experience—teams of developers might find it more productive to:

- Have a single, shared style, and
- Enforce this style through automatic formatting.

The alternative is often tiring formatting debates during code reviews,
                  where time might be better spent on code behavior rather than code style.

## Automatically formatting code in VS Code

Install the`Flutter`extension (see[VS Code setup](https://docs.flutter.dev/tools/vs-code#setup))
                  to get automatic formatting of code in VS Code.

`Flutter`
To automatically format the code in the current source code window,
                  right-click in the code window and select`Format Document`.
                  You can add a keyboard shortcut to this VS Code**Preferences**.

`Format Document`
To automatically format code whenever you save a file, set the`editor.formatOnSave`setting to`true`.

`editor.formatOnSave`
`true`
## Automatically formatting code in Android Studio and IntelliJ

Install the`Dart`plugin (see[Android Studio and IntelliJ setup](https://docs.flutter.dev/tools/android-studio#setup))
                  to get automatic formatting of code in Android Studio and IntelliJ.
                  To format your code in the current source code window:

`Dart`
- On macOS,
                    press++.
- On Windows and Linux,
                    press++.

Android Studio and IntelliJ also provide a checkbox named**Format code on save**on the Flutter page in**Preferences**on macOS or**Settings**on Windows and Linux.
                  This option corrects formatting in the current file when you save it.

## Automatically formatting code with thedartcommand

`dart`
To correct code formatting in the command line interface (CLI),
                  run the`dart format`command:

`dart format`
`$ dart format path1 path2 [...]`
To learn more about the Dart formatter,
                  check out the dart.dev docs on[dart format](https://dart.dev/tools/dart-format).

`dart format`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/formatting.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/formatting&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/formatting.md).
