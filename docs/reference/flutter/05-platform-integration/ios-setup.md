> 原文链接: [https://docs.flutter.dev/platform-integration/ios/setup](https://docs.flutter.dev/platform-integration/ios/setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Learn how to set up your development environment
                  to run, build, and deploy Flutter apps for iOS devices.

## Set up iOS tooling

With Xcode, you can run Flutter apps on
                  an iOS physical device or on the iOS Simulator.

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
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

### Download prerequisite tooling

To download iOS platform support and
                      the latest iOS Simulator runtimes,
                      run the following command in your preferred terminal.

`$ xcodebuild -downloadPlatform iOS`
### Install CocoaPods

To support[Flutter plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages#types)that use native iOS or macOS code,
                      install the latest version of[CocoaPods](https://guides.cocoapods.org/using/getting-started.html#installation).

Install CocoaPods by following the[CocoaPods installation guide](https://guides.cocoapods.org/using/getting-started.html#installation).

If you've already installed CocoaPods,
                      update it by following the[CocoaPods update guide](https://guides.cocoapods.org/using/getting-started.html#updating-cocoapods).

## Set up an iOS device

We recommend starting with the iOS Simulator as
                  it's easier to get set up than a physical iOS device.
                  However, you should also test your app on an actual
                  physical device.

- [Simulator](#190-tab-panel)
- [Physical device](#191-tab-panel)

Start the iOS Simulator with the following command:

`$ open -a Simulator`
If you need to install a simulator for a different OS version,
                        check out[Downloading and installing additional Xcode components](https://developer.apple.com/documentation/xcode/downloading-and-installing-additional-xcode-components)on the Apple Developer site.

Set up each iOS device on which you want to test.


### Configure your physical iOS device


Attach your iOS device to the USB port on your Mac.

On first connecting an iOS device to your Mac,
                                your device displays the**Trust this computer?**dialog.

Click**Trust**.

![Trust Mac](https://docs.flutter.dev/assets/images/docs/setup/trust-computer.png)

### Configure your physical iOS device

Apple requires enabling**Developer Mode**on the device to protect against malicious software.


Tap on**Settings**>**Privacy & Security**>**Developer Mode**.

Tap to toggle**Developer Mode**to**On**.

Restart the device.

When the**Turn on Developer Mode?**dialog appears,
                                tap**Turn On**.

### Create a developer code signing certificate

To send your app to a physical iOS device,*even*for testing, you must establish trust
                            between your Mac and the device.
                            In addition to trusting the device when that
                            popup appears, you must upload a signed
                            developer certificate to your device.

To create a signed development certificate,
                            you need an Apple ID.
                            If you don't have one,[create one](https://support.apple.com/en-us/108647).
                            You must also enroll in the[Apple Developer program](https://developer.apple.com/programs/)and create an[Apple Developer account](https://developer.apple.com/account).
                            If you're just*testing*your app on an iOS device,
                            a personal Apple Developer account is free and works.

### Prepare the device


Find the**VPN & Device Management**menu under**Settings**.

Toggle your certificate to**Enable**.

Under the**Developer App**heading,
                                you should find your certificate.

Tap the certificate.

Tap**Trust "<certificate>"**.

When the dialog displays, tap**Trust**.

If the**codesign wants to access key...**dialog appears:


Enter your macOS password.

Tap**Always Allow**.

---

## Start developing for iOS

**Congratulations.**Now that you've set up iOS development for Flutter,
                  you can continue your Flutter learning journey while testing on iOS
                  or begin improving integration with iOS.

- [Learn the fundamentals](https://docs.flutter.dev/learn/pathway)
- [Explore Flutter widgets](https://www.youtube.com/watch?v=b_sQ9bMltGU&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)
- [Check out samples](https://docs.flutter.dev/reference/learning-resources)

- [Build and deploy to iOS](https://docs.flutter.dev/deployment/ios)
- [Bind to native iOS code](https://docs.flutter.dev/platform-integration/ios/c-interop)
- [Leverage system frameworks](https://docs.flutter.dev/platform-integration/ios/apple-frameworks)
- [Embed native iOS views](https://docs.flutter.dev/platform-integration/ios/platform-views)
- [Use Swift Package Manager](https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-app-developers)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-07.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/ios/setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/setup.md).
