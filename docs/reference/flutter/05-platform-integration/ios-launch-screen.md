> 原文链接: [https://docs.flutter.dev/platform-integration/ios/launch-screen](https://docs.flutter.dev/platform-integration/ios/launch-screen)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

[Launch screens](https://developer.apple.com/design/human-interface-guidelines/launching#Launch-screens)provide a simple initial experience while your iOS app loads.
                  They set the stage for your application, while allowing time for the app engine
                  to load and your app to initialize.

All apps submitted to the Apple App Store[must provide a launch screen](https://developer.apple.com/documentation/xcode/specifying-your-apps-launch-screen)with an Xcode storyboard.

## Customize the launch screen

The default Flutter template includes an Xcode
                  storyboard named`LaunchScreen.storyboard`that can be customized with your own assets.
                  By default, the storyboard displays a blank image,
                  but you can change this. To do so,
                  open the Flutter app's Xcode project
                  by typing`open ios/Runner.xcworkspace`from the root of your app directory.
                  Then select`Runner/Assets.xcassets`from the Project Navigator and
                  drop in the desired images to the`LaunchImage`image set.

`LaunchScreen.storyboard`
`open ios/Runner.xcworkspace`
`Runner/Assets.xcassets`
`LaunchImage`
Apple provides detailed guidance for launch screens as
                  part of the[Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/patterns/launching#launch-screens).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/launch-screen.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/ios/launch-screen&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/launch-screen.md).
