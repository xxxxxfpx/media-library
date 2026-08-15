> 原文链接: [https://docs.flutter.dev/deployment/macos](https://docs.flutter.dev/deployment/macos)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This guide provides a step-by-step walkthrough of releasing a
                  Flutter app to the[App Store](https://developer.apple.com/app-store/submissions/).

## Preliminaries

Before beginning the process of releasing your app,
                  ensure that it meets
                  Apple's[App Review Guidelines](https://developer.apple.com/app-store/review/).

In order to publish your app to the App Store,
                  you must first enroll in the[Apple Developer Program](https://developer.apple.com/programs/).
                  You can read more about the various
                  membership options in Apple's[Choosing a Membership](https://developer.apple.com/support/compare-memberships/)guide.

## Register your app on App Store Connect

Manage your app's life cycle on[App Store Connect](https://appstoreconnect.apple.com/)(formerly iTunes Connect).
                  You define your app name and description, add screenshots,
                  set pricing, and manage releases to the App Store and TestFlight.

Registering your app involves two steps: registering a unique
                  Bundle ID, and creating an application record on App Store Connect.

For a detailed overview of App Store Connect, see the[App Store Connect](https://developer.apple.com/support/app-store-connect/)guide.

### Register a Bundle ID

Every macOS application is associated with a Bundle ID,
                  a unique identifier registered with Apple.
                  To register a Bundle ID for your app, follow these steps:

1. Open the[App IDs](https://developer.apple.com/account/resources/identifiers/list)page of your developer account.
1. Click**+**to create a new Bundle ID.
1. Enter an app name, select**Explicit App ID**, and enter an ID.
1. Select the services your app uses, then click**Continue**.
1. On the next page, confirm the details and click**Register**to register your Bundle ID.

### Create an application record on App Store Connect

Register your app on App Store Connect:

1. Open[App Store Connect](https://appstoreconnect.apple.com/)in your browser.
1. On the App Store Connect landing page, click**My Apps**.
1. Click**+**in the top-left corner of the My Apps page,
                    then select**New App**.
1. Fill in your app details in the form that appears.
                    In the Platforms section, ensure that macOS is checked.
                    Since Flutter does not currently support tvOS,
                    leave that checkbox unchecked. Click**Create**.
1. Navigate to the application details for your app and select**App Information**from the sidebar.
1. In the General Information section, select the Bundle ID
                    you registered in the preceding step.

For a detailed overview,
                  see[Add an app to your account](https://help.apple.com/app-store-connect/#/dev2cd126805).

## Review Xcode project settings

This step covers reviewing the most important settings
                  in the Xcode workspace.
                  For detailed procedures and descriptions, see[Prepare for app distribution](https://help.apple.com/xcode/mac/current/#/dev91fe7130a).

Navigate to your target's settings in Xcode:

1. In Xcode, open`Runner.xcworkspace`in your app's`macos`folder.
1. To view your app's settings, select the**Runner**project in the Xcode
                    project navigator. Then, in the main view sidebar, select the**Runner**target.
1. Select the**General**tab.

`Runner.xcworkspace`
`macos`
Verify the most important settings.

In the**Identity**section:

`App Category`
The app category under which your app will be listed on the Mac App Store. This cannot be none.

`Bundle Identifier`
The App ID you registered on App Store Connect.

In the**Deployment info**section:

`Deployment Target`
The minimum macOS version that your app supports.
                      To check which versions of macOS that Flutter supports deploying to,
                      check out Flutter's[Supported deployment platforms](https://docs.flutter.dev/reference/supported-platforms).

In the**Signing & Capabilities**section:

`Automatically manage signing`
Whether Xcode should automatically manage app signing
                      and provisioning.  This is set`true`by default, which should
                      be sufficient for most apps. For more complex scenarios,
                      see the[Code Signing Guide](https://developer.apple.com/library/content/documentation/Security/Conceptual/CodeSigningGuide/Introduction/Introduction.html).

`true`
`Team`
Select the team associated with your registered Apple Developer
                      account. If required, select**Add Account...**,
                      then update this setting.

The**General**tab of your project settings should resemble
                  the following:

![Xcode Project Settings](https://docs.flutter.dev/assets/images/docs/releaseguide/macos_xcode_settings.png)

For a detailed overview of app signing, see[Create, export, and delete signing certificates](https://help.apple.com/xcode/mac/current/#/dev154b28f09).

## Configuring the app's name, bundle identifier and copyright

The configuration for the product identifiers are centralized
                  in`macos/Runner/Configs/AppInfo.xcconfig`. For the app's name,
                  set`PRODUCT_NAME`, for the copyright set`PRODUCT_COPYRIGHT`,
                  and finally set`PRODUCT_BUNDLE_IDENTIFIER`for the app's
                  bundle identifier.

`macos/Runner/Configs/AppInfo.xcconfig`
`PRODUCT_NAME`
`PRODUCT_COPYRIGHT`
`PRODUCT_BUNDLE_IDENTIFIER`
## Updating the app's version number

The default version number of the app is`1.0.0`.
                  To update it, navigate to the`pubspec.yaml`file
                  and update the following line:

`1.0.0`
`pubspec.yaml`
`version: 1.0.0+1`

`version: 1.0.0+1`
The version number is three numbers separated by dots,
                  such as`1.0.0`in the example above, followed by an optional
                  build number such as`1`in the example above, separated by a`+`.

`1.0.0`
`1`
`+`
Both the version and the build number can be overridden in Flutter's
                  build by specifying`--build-name`and`--build-number`,
                  respectively.

`--build-name`
`--build-number`
In macOS,`build-name`uses`CFBundleShortVersionString`while`build-number`uses`CFBundleVersion`.
                  Read more about iOS versioning at[Core Foundation Keys](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html)on the Apple Developer's site.

`build-name`
`CFBundleShortVersionString`
`build-number`
`CFBundleVersion`
## Add an app icon

When a new Flutter app is created, a placeholder icon set is created.
                  This step covers replacing these placeholder icons with your
                  app's icons:

1. Review the[macOS App Icon](https://developer.apple.com/design/human-interface-guidelines/macos/icons-and-images/app-icon/)guidelines.
1. In the Xcode project navigator, select`Assets.xcassets`in the`Runner`folder. Update the placeholder icons with your own app icons.
1. Verify the icon has been replaced by running your app using`flutter run -d macos`.

`Assets.xcassets`
`Runner`
`flutter run -d macos`
## Create a build archive with Xcode

This step covers creating a build archive and uploading
                  your build to App Store Connect using Xcode.

During development, you've been building, debugging, and testing
                  with*debug*builds. When you're ready to ship your app to users
                  on the App Store or TestFlight, you need to prepare a*release*build.
                  At this point, you might consider[obfuscating your Dart code](https://docs.flutter.dev/deployment/obfuscate)to make it more difficult to reverse engineer. Obfuscating
                  your code involves adding a couple flags to your build command.

In Xcode, configure the app version and build:

1. Open`Runner.xcworkspace`in your app's`macos`folder. To do this from
                    the command line, run the following command from the base directory of your
                    application project.@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Select**Runner**in the Xcode project navigator, then select the**Runner**target in the settings view sidebar.
1. In the Identity section, update the**Version**to the user-facing
                    version number you wish to publish.
1. In the Identity section, update the**Build**identifier to a unique
                    build number used to track this build on App Store Connect.
                    Each upload requires a unique build number.

`Runner.xcworkspace`
`macos`
`open macos/Runner.xcworkspace`
Finally, create a build archive and upload it to App Store Connect:

1. Create a release Archive of your application. From the base directory of
                    your application project, run the following.@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. Open Xcode and select**Product > Archive**to open the archive created
                    in the previous step.
1. Click the**Validate App**button. If any issues are reported,
                    address them and produce another build. You can reuse the same
                    build ID until you upload an archive.
1. After the archive has been successfully validated, click**Distribute App**. You can follow the status of your build in the
                    Activities tab of your app's details page on[App Store Connect](https://appstoreconnect.apple.com/).

`flutter build macos`
You should receive an email within 30 minutes notifying you that
                  your build has been validated and is available to release to testers
                  on TestFlight. At this point you can choose whether to release
                  on TestFlight, or go ahead and release your app to the App Store.

For more details, see[Upload an app to App Store Connect](https://help.apple.com/xcode/mac/current/#/dev442d7f2ca).

## Create a build archive with Codemagic CLI tools

This step covers creating a build archive and uploading
                  your build to App Store Connect using Flutter build commands
                  and[Codemagic CLI Tools](https://github.com/codemagic-ci-cd/cli-tools)executed in a terminal
                  in the Flutter project directory.

1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonbash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. bash@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Install the Codemagic CLI tools:

`pip3 install codemagic-cli-tools`
You'll need to generate an[App Store Connect API Key](https://appstoreconnect.apple.com/access/api)with App Manager access to automate operations with App Store Connect. To make
subsequent commands more concise, set the following environment variables from
the new key: issuer id, key id, and API key file.

`export APP_STORE_CONNECT_ISSUER_ID=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
export APP_STORE_CONNECT_KEY_IDENTIFIER=ABC1234567
export APP_STORE_CONNECT_PRIVATE_KEY=`cat /path/to/api/key/AuthKey_XXXYYYZZZ.p8``
You need to export or create a Mac App Distribution and a Mac Installer
Distribution certificate to perform code signing and package a build archive.

If you have existing[certificates](https://developer.apple.com/account/resources/certificates/list), you can export the
private keys by executing the following command for each certificate:

`openssl pkcs12 -in <certificate_name>.p12 -nodes -nocerts | openssl rsa -out cert_key`
Or you can create a new private key by executing the following command:

`ssh-keygen -t rsa -b 2048 -m PEM -f cert_key -q -N ""`
Later, you can have CLI tools automatically create a new Mac App Distribution and
Mac Installer Distribution certificate. You can use the same private key for
each new certificate.

Fetch the code signing files from App Store Connect:

`app-store-connect fetch-signing-files YOUR.APP.BUNDLE_ID \
    --platform MAC_OS \
    --type MAC_APP_STORE \
    --certificate-key=@file:/path/to/cert_key \
    --create`
Where`cert_key`is either your exported Mac App Distribution certificate private key
or a new private key which automatically generates a new certificate.

`cert_key`
If you do not have a Mac Installer Distribution certificate,
you can create a new certificate by executing the following:

`app-store-connect certificates create \
    --type MAC_INSTALLER_DISTRIBUTION \
    --certificate-key=@file:/path/to/cert_key \
    --save`
Use`cert_key`of the private key you created earlier.

`cert_key`
Fetch the Mac Installer Distribution certificates:

`app-store-connect certificates list \
    --type MAC_INSTALLER_DISTRIBUTION \
    --certificate-key=@file:/path/to/cert_key \
    --save`
Set up a new temporary keychain to be used for code signing:

`keychain initialize`
Now add the fetched certificates to your keychain:

`keychain add-certificates`
Update the Xcode project settings to use fetched code signing profiles:

`xcode-project use-profiles`
Install Flutter dependencies:

`flutter packages pub get`
Install CocoaPods dependencies:

`find . -name "Podfile" -execdir pod install \;`
Build the Flutter macOS project:

`flutter build macos --release`
Package the app:

`APP_NAME=$(find $(pwd) -name "*.app")
PACKAGE_NAME=$(basename "$APP_NAME" .app).pkg
xcrun productbuild --component "$APP_NAME" /Applications/ unsigned.pkg

INSTALLER_CERT_NAME=$(keychain list-certificates \
          | jq '[.[]
            | select(.common_name
            | contains("Mac Developer Installer"))
            | .common_name][0]' \
          | xargs)
xcrun productsign --sign "$INSTALLER_CERT_NAME" unsigned.pkg "$PACKAGE_NAME"
rm -f unsigned.pkg`
Publish the packaged app to App Store Connect:

`app-store-connect publish \
    --path "$PACKAGE_NAME"`
As mentioned earlier, don't forget to set your login keychain
as the default to avoid authentication issues
with apps on your machine:

`keychain use-login`
## Release your app on TestFlight

[TestFlight](https://developer.apple.com/testflight/)allows developers to push their apps
                  to internal and external testers. This optional step
                  covers releasing your build on TestFlight.

1. Navigate to the TestFlight tab of your app's application
                    details page on[App Store Connect](https://appstoreconnect.apple.com/).
1. Select**Internal Testing**in the sidebar.
1. Select the build to publish to testers, then click**Save**.
1. Add the email addresses of any internal testers.
                    You can add additional internal users in the**Users and Roles**page of App Store Connect,
                    available from the dropdown menu at the top of the page.

## Distribute to registered devices

See[distribution guide](https://help.apple.com/xcode/mac/current/#/dev295cc0fae)to prepare an archive for distribution to designated Mac computers.

## Release your app to the App Store

When you're ready to release your app to the world,
                  follow these steps to submit your app for review and
                  release to the App Store:

1. Select**Pricing and Availability**from the sidebar of your app's
                    application details page on[App Store Connect](https://appstoreconnect.apple.com/)and complete the
                    required information.
1. Select the status from the sidebar. If this is the first
                    release of this app, its status is**1.0 Prepare for Submission**. Complete all required fields.
1. Click**Submit for Review**.

Apple notifies you when their app review process is complete.
                  Your app is released according to the instructions you
                  specified in the**Version Release**section.

For more details, see[Distribute an app through the App Store](https://help.apple.com/xcode/mac/current/#/dev067853c94).

## Troubleshooting

The[Distribute your app](https://help.apple.com/xcode/mac/current/#/dev8b4250b57)guide provides a
                  detailed overview of the process of releasing an app to the App Store.

## Additional resources

To learn how to package and distribute your Flutter desktop app
                  for macOS the open source way, without using a paid Apple developer
                  account, check out the step-by-step[macOS packaging guide](https://medium.com/@fluttergems/packaging-and-distributing-flutter-desktop-apps-the-missing-guide-part-1-macos-b36438269285).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/macos.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/deployment/macos&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/macos.md).
