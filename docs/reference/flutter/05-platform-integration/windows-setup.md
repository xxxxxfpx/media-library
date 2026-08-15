> 原文链接: [https://docs.flutter.dev/platform-integration/windows/setup](https://docs.flutter.dev/platform-integration/windows/setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Learn how to set up your development environment
                  to run, build, and deploy Flutter apps for the Windows desktop platform.

## Set up tooling

With[Visual Studio](https://visualstudio.microsoft.com/), you can run Flutter apps on Windows as well as
                  compile and debug native C and C++ code.

Note that**Visual Studio**is an IDE separate from**Visual StudioCode**and only supported on Windows.


### Install Visual Studio

If you haven't done so already,
                      follow the Microsoft guide to[install and set up Visual Studio](https://visualstudio.microsoft.com/).

If you've already installed Visual Studio,[update it to the latest version](https://learn.microsoft.com/en-us/visualstudio/install/update-visual-studio).

### Set up Visual Studio workloads

When the Visual Studio installer prompts you to choose workloads,
                      select and install the**Desktop development with C++**workload.

If you already installed Visual Studio,
                      follow the Microsoft guide to[Modify Visual Studio workloads](https://learn.microsoft.com/en-us/visualstudio/install/modify-visual-studio).

## Validate your setup

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

### Check for toolchain issues

To check for any issues with your Windows development setup,
                      run the`flutter doctor`command in your preferred terminal:

`flutter doctor`
`$ flutter doctor -v`
If you see any errors or tasks to complete under the**Windows version**and**Visual Studio - develop Windows apps**sections,
                      complete and resolve them, then
                      run`flutter doctor -v`again to verify any changes.

`flutter doctor -v`
### Check for Windows devices

To ensure Flutter can find and connect to your Windows device correctly,
                      run`flutter devices`in your preferred terminal:

`flutter devices`
`$ flutter devices`
If you've set everything up correctly,
                      there should be at least one entry with the platform marked as**windows**.

### Troubleshoot setup issues

If you need help resolving any setup issues,
                      check out[installation and setup troubleshooting](https://docs.flutter.dev/install/troubleshoot).
                      Depending on your issue,
                      also check out Microsoft's guide on[Visual Studio troubleshooting](https://learn.microsoft.com/en-us/troubleshoot/developer/visualstudio/installation/troubleshoot-installation-issues).

If you still have issues or questions,
                      reach out on one of the Flutter[community](https://flutter.dev/community)channels.

## Start developing for Windows

Congratulations!
                  Now that you've set up Windows desktop development for Flutter,
                  you can continue your Flutter learning journey while testing on Windows
                  or begin expanding integration with Windows.

- [Learn the fundamentals](https://docs.flutter.dev/learn/pathway)
- [Explore Flutter widgets](https://www.youtube.com/watch?v=b_sQ9bMltGU&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)
- [Check out samples](https://docs.flutter.dev/reference/learning-resources)

- [Build a Windows app](https://docs.flutter.dev/platform-integration/windows/building)
- [Deploy to windows](https://docs.flutter.dev/deployment/windows)
- [Write Windows-specific code](https://docs.flutter.dev/platform-integration/platform-channels)
- [Customize the app window](https://docs.flutter.dev/platform-integration/windows/building#customizing-the-windows-host-application)
- [Access Win32 APIs with Dart](https://pub.dev/packages/win32)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/windows/setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/windows/setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/windows/setup.md).
