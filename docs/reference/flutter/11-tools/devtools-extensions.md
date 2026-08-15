> 原文链接: [https://docs.flutter.dev/tools/devtools/extensions](https://docs.flutter.dev/tools/devtools/extensions)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## What are DevTools extensions?

[DevTools extensions](https://pub.dev/packages/devtools_extensions)are developer tools provided by third-party packages that are
                  tightly integrated into the DevTools tooling suite.
                  Extensions are distributed as part of a pub package,
                  and they are dynamically loaded into DevTools when
                  a user is debugging their app.

## Use a DevTools extension

If your app depends on a package that provides a
                  DevTools extension, the extension automatically
                  shows up in a new tab when you open DevTools.

### Configure extension enablement states

You need to manually enable the extension before it loads
                  for the first time. Make sure the extension is provided by
                  a source you trust before enabling it.

When you open the extension for the first time, you'll see a prompt to enable
                  the extension:

![Screenshot of extension enablement prompt](https://docs.flutter.dev/assets/images/docs/tools/devtools/extension_enable_prompt.png)

You can modify the setting at any time from the DevTools Extensions dialog:

![Screenshot of DevTools Extensions dialog button](https://docs.flutter.dev/assets/images/docs/tools/devtools/extension_dialog_button.png)

![Screenshot of extension enablement dialog](https://docs.flutter.dev/assets/images/docs/tools/devtools/extension_dialog.png)

Extension enablement states are stored in a`devtools_options.yaml`file in the root of the user's project
                  (similar to`analysis_options.yaml`).

`devtools_options.yaml`
`analysis_options.yaml`
`description: This file stores settings for Dart & Flutter DevTools.
documentation: https://docs.flutter.dev/tools/devtools/extensions#configure-extension-enablement-states
extensions:
  - provider: true
  - shared_preferences: true
  - foo: false`
This file stores per-project
                  (or optionally, per user) settings for DevTools.

If this file is**checked into source control**,
                  the specified options are configured for the project.
                  This means that anyone who pulls a project's
                  source code and works on the project uses the same settings.

If this file is**omitted from source control**,
                  for example by adding`devtools_options.yaml`as an entry in the`.gitignore`file, then the specified
                  options are configured separately for each user.
                  Since each user or contributor to the project
                  uses a local copy of the`devtools_options.yaml`file in this case, the specified options might
                  differ between project contributors.

`devtools_options.yaml`
`.gitignore`
`devtools_options.yaml`
## Build a DevTools extension

For an in-depth guide on how to build a DevTools extension, visit[Build custom tooling in Flutter and Dart DevTools](https://docs.flutter.dev/tools/devtools/custom-tool)

You might also check out the following video:

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/extensions.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/devtools/extensions&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/extensions.md).
