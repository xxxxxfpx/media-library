> 原文链接: [https://docs.flutter.dev/platform-integration/macos/building](https://docs.flutter.dev/platform-integration/macos/building)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This page discusses considerations unique to building
                  macOS apps with Flutter, including shell integration
                  and distribution of macOS apps through the Apple Store.

## Integrating with macOS look and feel

While you can use any visual style or theme you choose
                  to build a macOS app, you might want to adapt your app
                  to more fully align with the macOS look and feel.
                  Flutter includes the[Cupertino](https://docs.flutter.dev/ui/widgets/cupertino)widget set,
                  which provides a set of widgets for
                  the current iOS design language.
                  Many of these widgets, including sliders,
                  switches and segmented controls,
                  are also appropriate for use on macOS.

Alternatively, you might find the[macos_ui](https://pub.dev/packages/macos_ui)package a good fit for your needs.
                  This package provides widgets and themes that
                  implement the macOS design language,
                  including a`MacosWindow`frame and scaffold,
                  toolbars, pulldown and
                  pop-up buttons, and modal dialogs.

`MacosWindow`
## Building macOS apps

To distribute your macOS application, you can either[distribute it through the macOS App Store](https://developer.apple.com/macos/submit/),
                  or you can distribute the`.app`itself,
                  perhaps from your own website.
                  You need to notarize your macOS application before
                  distributing it outside the macOS App Store.

`.app`
The first step in both of the above processes
                  involves working with your application inside of Xcode.
                  To be able to compile your application from inside of
                  Xcode you first need to build the application for release
                  using the`flutter build`command, then open the
                  Flutter macOS Runner application.

`flutter build`
`flutter build macos
open macos/Runner.xcworkspace`
Once inside of Xcode, follow either Apple's[documentation on notarizing macOS Applications](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution), or[on distributing an application through the App Store](https://help.apple.com/xcode/mac/current/#/dev067853c94).
                  You should also read through the[macOS-specific support](#entitlements-and-the-app-sandbox)section below to understand how entitlements,
                  the App Sandbox, and the Hardened Runtime
                  impact your distributable application.

[Build and release a macOS app](https://docs.flutter.dev/deployment/macos)provides a more detailed
                  step-by-step walkthrough of releasing a Flutter app to the
                  App Store.

## Entitlements and the App Sandbox

macOS builds are configured by default to be signed,
                  and sandboxed with App Sandbox.
                  This means that if you want to confer specific
                  capabilities or services on your macOS app,
                  such as the following:

- Accessing the internet
- Capturing movies and images from the built-in camera
- Accessing files

Then you must set up specific*entitlements*in Xcode.
                  The following section tells you how to do this.

### Setting up entitlements

Managing sandbox settings is done in the`macos/Runner/*.entitlements`files. When editing
                  these files, you shouldn't remove the original`Runner-DebugProfile.entitlements`exceptions
                  (that support incoming network connections and JIT),
                  as they're necessary for the`debug`and`profile`modes to function correctly.

`macos/Runner/*.entitlements`
`Runner-DebugProfile.entitlements`
`debug`
`profile`
If you're used to managing entitlement files through
                  the**Xcode capabilities UI**, be aware that the capabilities
                  editor updates only one of the two files or,
                  in some cases, it creates a whole new entitlements
                  file and switches the project to use it for all configurations.
                  Either scenario causes issues. We recommend that you
                  edit the files directly. Unless you have a very specific
                  reason, you should always make identical changes to both files.

If you keep the App Sandbox enabled (which is required if you
                  plan to distribute your application in the[App Store](https://developer.apple.com/app-store/submissions/)),
                  you need to manage entitlements for your application
                  when you add certain plugins or other native functionality.
                  For instance, using the[file_chooser](https://github.com/google/flutter-desktop-embedding/tree/master/plugins/file_chooser)plugin
                  requires adding either the`com.apple.security.files.user-selected.read-only`or`com.apple.security.files.user-selected.read-write`entitlement.
                  Another common entitlement is`com.apple.security.network.client`,
                  which you must add if you make any network requests.

`file_chooser`
`com.apple.security.files.user-selected.read-only`
`com.apple.security.files.user-selected.read-write`
`com.apple.security.network.client`
Without the`com.apple.security.network.client`entitlement,
                  for example, network requests fail with a message such as:

`com.apple.security.network.client`
`flutter: SocketException: Connection failed
(OS Error: Operation not permitted, errno = 1),
address = example.com, port = 443`
For more information on these topics,
                  see[App Sandbox](https://developer.apple.com/documentation/security/app_sandbox)and[Entitlements](https://developer.apple.com/documentation/bundleresources/entitlements)on the Apple Developer site.

## Hardened Runtime

If you choose to distribute your application outside
                  of the App Store, you need to notarize your application
                  for compatibility with macOS.
                  This requires enabling the Hardened Runtime option.
                  Once you have enabled it, you need a valid signing
                  certificate in order to build.

By default, the entitlements file allows JIT for
                  debug builds but, as with App Sandbox, you might
                  need to manage other entitlements.
                  If you have both App Sandbox and Hardened
                  Runtime enabled, you might need to add multiple
                  entitlements for the same resource.
                  For instance, microphone access would require both`com.apple.security.device.audio-input`(for Hardened Runtime)
                  and`com.apple.security.device.microphone`(for App Sandbox).

`com.apple.security.device.audio-input`
`com.apple.security.device.microphone`
For more information on this topic,
                  see[Hardened Runtime](https://developer.apple.com/documentation/security/hardened_runtime)on the Apple Developer site.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/macos/building.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/macos/building&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/macos/building.md).
