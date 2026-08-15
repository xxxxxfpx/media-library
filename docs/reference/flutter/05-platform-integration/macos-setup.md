> 原文链接: [https://docs.flutter.dev/platform-integration/macos/setup](https://docs.flutter.dev/platform-integration/macos/setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Learn how to set up your development environment
                  to run, build, and deploy Flutter apps for the macOS desktop platform.

## Set up tooling

With Xcode, you can run Flutter apps on macOS as well as
                  compile and debug native Swift and Objective-C code.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

### Install Xcode

If you haven't done so already,[install and set up the latest version of Xcode](https://developer.apple.com/xcode/).

If you've already installed Xcode,
                      update it to the latest version using the
                      same installation method you used originally.

### Set up Xcode command-line tools

To configure the Xcode command-line tools to use
                      the version of Xcode you installed,
                      run the following command in your preferred terminal:

`$ sudo sh -c 'xcode-select -s /Applications/Xcode.app/Contents/Developer && xcodebuild -runFirstLaunch'`
If you downloaded Xcode elsewhere or need to use a different version,
                      replace`/Applications/Xcode.app`with the path to there instead.

`/Applications/Xcode.app`
### Agree to the Xcode licenses

After you've set up Xcode and configured its command-line tools,
                      agree to the Xcode licenses.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Open your preferred terminal.

Run the following command to review and sign the Xcode licenses.

`$ sudo xcodebuild -license`
Read and agree to all necessary licenses.

Before agreeing to the terms of each license,
                          read each with care.

Once you've accepted all the necessary licenses successfully,
                          the command should output how to review the licenses.

### Install CocoaPods

To support[Flutter plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages#types)that use native macOS code,
                      install the latest version of[CocoaPods](https://cocoapods.org/).

Install CocoaPods following the[CocoaPods installation guide](https://guides.cocoapods.org/using/getting-started.html#installation).

If you've already installed CocoaPods,
                      update it following the[CocoaPods update guide](https://guides.cocoapods.org/using/getting-started.html#updating-cocoapods).

## Validate your setup

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

### Check for toolchain issues

To check for any issues with your macOS development setup,
                      run the`flutter doctor`command in your preferred terminal:

`flutter doctor`
`$ flutter doctor -v`
If you see any errors or tasks to complete
                      under the**Xcode**section,
                      complete and resolve them, then
                      run`flutter doctor -v`again to verify any changes.

`flutter doctor -v`
### Check for macOS devices

To ensure Flutter can find and connect to your macOS device correctly,
                      run`flutter devices`in your preferred terminal:

`flutter devices`
`$ flutter devices`
If you set everything up correctly,
                      there should be at least one entry with the platform marked as**macos**.

### Troubleshoot setup issues

If you need help resolving any setup issues,
                      check out[Install and setup troubleshooting](https://docs.flutter.dev/install/troubleshoot).

If you still have issues or questions,
                      reach out on one of the Flutter[community](https://flutter.dev/community)channels.

## Start developing for macOS

Congratulations!
                  Now that you've set up macOS desktop development for Flutter,
                  you can continue your Flutter learning journey while testing on macOS
                  or begin expanding integration with macOS.

- [Learn the fundamentals](https://docs.flutter.dev/learn/pathway)
- [Explore Flutter widgets](https://www.youtube.com/watch?v=b_sQ9bMltGU&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)
- [Check out samples](https://docs.flutter.dev/reference/learning-resources)

- [Build and deploy to macOS](https://docs.flutter.dev/deployment/macos)
- [Bind to native macOS code](https://docs.flutter.dev/platform-integration/macos/c-interop)
- [Embed native macOS views](https://docs.flutter.dev/platform-integration/macos/platform-views)
- [Set up app flavors](https://docs.flutter.dev/deployment/flavors-ios)
- [Use Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/macos/setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/macos/setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/macos/setup.md).
