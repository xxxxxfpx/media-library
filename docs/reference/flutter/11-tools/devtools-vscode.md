> 原文链接: [https://docs.flutter.dev/tools/devtools/vscode](https://docs.flutter.dev/tools/devtools/vscode)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Add the VS Code extensions

To use the DevTools from VS Code, you need the[Dart extension](https://marketplace.visualstudio.com/items?itemName=Dart-Code.dart-code).
                  If you're debugging Flutter applications, you should also install
                  the[Flutter extension](https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter).

## Start an application to debug

Start a debug session for your application by opening the root
                  folder of your project (the one containing`pubspec.yaml`)
                  in VS Code and clicking**Run > Start Debugging**(`F5`).

`pubspec.yaml`
`F5`
## Launch DevTools

Once the debug session is active and the application has started,
                  the**Open DevTools**commands become available in the
                  VS Code command palette (`F1`):

`F1`
![Screenshot showing Open DevTools commands](https://docs.flutter.dev/assets/images/docs/tools/vs-code/vscode_command.png)

The chosen tool will be opened embedded inside VS Code.

![Screenshot showing DevTools embedded in VS Code](https://docs.flutter.dev/assets/images/docs/tools/vs-code/vscode_embedded.png)

You can choose to have DevTools always opened
                  in a browser with the`dart.embedDevTools`setting,
                  and control whether it opens as a full window or
                  in a new column next to your current editor with the`dart.devToolsLocation`setting.

`dart.embedDevTools`
`dart.devToolsLocation`
A full list of Dart/Flutter settings are available on[dartcode.org](https://dartcode.org/docs/settings/)or in the[VS Code settings editor](https://code.visualstudio.com/docs/getstarted/settings#_settings-editor).
                  Some recommendation settings for Dart/Flutter in VS Code
                  can also be found on[dartcode.org](https://dartcode.org/docs/recommended-settings/).

You can also see whether DevTools is running
                  and launch it in a browser from the language status area
                  (the`{}`icon next to**Dart**in the status bar).

`{}`
![Screenshot showing DevTools in the VS Code language status area](https://docs.flutter.dev/assets/images/docs/tools/vs-code/vscode_status_bar.png)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/vscode.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/devtools/vscode&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/vscode.md).
