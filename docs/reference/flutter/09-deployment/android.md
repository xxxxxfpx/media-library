> 原文链接: [https://docs.flutter.dev/deployment/android](https://docs.flutter.dev/deployment/android)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

To test an app, you can use`flutter run`at the command line,
                  or the**Run**and**Debug**options in your IDE.

`flutter run`
When you're ready to prepare a*release*version of your app,
                  for example to[publish to the Google Play Store](https://developer.android.com/distribute),
                  this page can help. Before publishing,
                  you might want to put some finishing touches on your app.
                  This guide explains how to perform the following tasks:

- [Add a launcher icon](#add-a-launcher-icon)
- [Enable Material Components](#enable-material-components)
- [Sign the app](#sign-the-app)
- [Shrink your code with R8](#shrink-your-code-with-r8)
- [Enable multidex support](#enable-multidex-support)
- [Review the app manifest](#review-the-app-manifest)
- [Review the build configuration](#review-the-gradle-build-configuration)
- [Build the app for release](#build-the-app-for-release)
- [Publish to the Google Play Store](#publish-to-the-google-play-store)
- [Update the app's version number](#update-the-apps-version-number)
- [Android release FAQ](#android-release-faq)

## Add a launcher icon

When a new Flutter app is created, it has a default launcher icon.
                  To customize this icon, you might want to check out the[flutter_launcher_icons](https://pub.dev/packages/flutter_launcher_icons)package.

Alternatively, you can do it manually using the following steps:


Review the[Material Design product icons](https://m3.material.io/styles/icons)guidelines for icon design.

In the`[project]/android/app/src/main/res/`directory,
                      place your icon files in folders named using[configuration qualifiers](https://developer.android.com/guide/topics/resources/providing-resources#AlternativeResources).
                      The default`mipmap-`folders demonstrate the correct
                      naming convention.

`[project]/android/app/src/main/res/`
`mipmap-`
In`AndroidManifest.xml`, update the[application](https://developer.android.com/guide/topics/manifest/application-element)tag's`android:icon`attribute to reference icons from the previous
                      step (for example,`<application android:icon="@mipmap/ic_launcher" ...`).

`AndroidManifest.xml`
`application`
`android:icon`
`<application android:icon="@mipmap/ic_launcher" ...`
To verify that the icon has been replaced,
                      run your app and inspect the app icon in the Launcher.

## Enable Material Components

If your app uses[platform views](https://docs.flutter.dev/platform-integration/android/platform-views), you might want to enable
                  Material Components by following the steps described in the[Getting Started guide for Android](https://m3.material.io/develop/android/mdc-android).

For example:

1. Add the dependency on Android's Material in`<my-app>/android/app/build.gradle.kts`:

`<my-app>/android/app/build.gradle.kts`
- [Kotlin](#207-tab-panel)
- [Groovy](#208-tab-panel)

`dependencies {
    // ...
    implementation("com.google.android.material:material:<version>")
    // ...
}`
`dependencies {
    // ...
    implementation 'com.google.android.material:material:<version>'
    // ...
}`
To find out the latest version, visit[Google Maven](https://maven.google.com/web/index.html#com.google.android.material:material).

1. xml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. xml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Set the light theme in`<my-app>/android/app/src/main/res/values/styles.xml`:

`<my-app>/android/app/src/main/res/values/styles.xml`
`<style name="NormalTheme" parent="@android:style/Theme.Light.NoTitleBar">
<style name="NormalTheme" parent="Theme.MaterialComponents.Light.NoActionBar">`
Set the dark theme in`<my-app>/android/app/src/main/res/values-night/styles.xml`:

`<my-app>/android/app/src/main/res/values-night/styles.xml`
`<style name="NormalTheme" parent="@android:style/Theme.Black.NoTitleBar">
<style name="NormalTheme" parent="Theme.MaterialComponents.DayNight.NoActionBar">`
## Sign the app

To publish on the Play Store, you must
                  sign your app with a digital certificate.

Android uses two signing keys:*upload*and*app signing*.

- Developers upload an`.aab`or`.apk`file signed with
                    an*upload key*to the Play Store.
- The end-users download the`.apk`file signed with an*app signing key*.

`.aab`
`.apk`
`.apk`
To create your app signing key, use Play App Signing
                  as described in the[official Play Store documentation](https://support.google.com/googleplay/android-developer/answer/7384423?hl=en).

To sign your app, use the following instructions.

### Create an upload keystore

If you have an existing keystore, skip to the next step.
                  If not, create one using one of the following methods:

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Follow the[Android Studio key generation steps](https://developer.android.com/studio/publish/app-signing#generate-key).

Run the following command at the command line:

On macOS or Linux, use the following command:

`keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA \
        -storetype JKS -keysize 2048 -validity 10000 -alias upload`
On Windows, use the following command in PowerShell:

`keytool -genkey -v -keystore $env:USERPROFILE\upload-keystore.jks `
        -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 `
        -alias upload`
This command stores the`upload-keystore.jks`file in your home
                      directory. If you want to store it elsewhere, change
                      the argument you pass to the`-keystore`parameter.**However, keep thekeystorefile private;
                        don't check it into public source control!**

`upload-keystore.jks`
`-keystore`
`keystore`
### Reference the keystore from the app

Create a file named`[project]/android/key.properties`that contains a reference to your keystore.
                  Don't include the angle brackets (`< >`).
                  They indicate that the text serves as a placeholder for your values.

`[project]/android/key.properties`
`< >`
`storePassword=<password-from-previous-step>
keyPassword=<password-from-previous-step>
keyAlias=upload
storeFile=<keystore-file-location>`
The`storeFile`might be located at`/Users/<user name>/upload-keystore.jks`on macOS
                  or`C:\\Users\\<user name>\\upload-keystore.jks`on Windows.

`storeFile`
`/Users/<user name>/upload-keystore.jks`
`C:\\Users\\<user name>\\upload-keystore.jks`
### Configure signing in Gradle

When building your app in release mode, configure Gradle to use your upload key.
                  To configure Gradle, edit the`<project>/android/app/build.gradle.kts`file.

`<project>/android/app/build.gradle.kts`

Define and load the keystore properties file before the`android`property block.

`android`
Set the`keystoreProperties`object to load the`key.properties`file.

`keystoreProperties`
`key.properties`
- [Kotlin](#209-tab-panel)
- [Groovy](#210-tab-panel)

`import java.util.Properties
import java.io.FileInputStream
​
plugins {
   ...
}
​
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}
​
android {
   ...
}`
`import java.util.Properties
import java.io.FileInputStream
​
plugins {
   ...
}
​
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}
​
android {
   ...
}`
1. Add the signing configuration before the`buildTypes`property block
                    inside the`android`property block.

`buildTypes`
`android`
- [Kotlin](#211-tab-panel)
- [Groovy](#212-tab-panel)

`android {
    // ...
​
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = keystoreProperties["storeFile"]?.let { file(it) }
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    buildTypes {
        release {
            // TODO: Add your own signing config for the release build.
            // Signing with the debug keys for now,
            // so `flutter run --release` works.
            signingConfig = signingConfigs.getByName("debug")
            signingConfig = signingConfigs.getByName("release")
        }
    }
...
}`
`android {
    // ...
​
    signingConfigs {
        release {
            keyAlias = keystoreProperties['keyAlias']
            keyPassword = keystoreProperties['keyPassword']
            storeFile = keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword = keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            // TODO: Add your own signing config for the release build.
            // Signing with the debug keys for now,
            // so `flutter run --release` works.
            signingConfig = signingConfigs.debug
            signingConfig = signingConfigs.release
        }
    }
...
}`
Flutter now signs all release builds.

To learn more about signing your app, check out[Sign your app](https://developer.android.com/studio/publish/app-signing.html#generate-key)on the Android developer docs.

### Post-quantum cryptography (PQC) hybrid signing (Android 17+)

Android 17 introduces the v3.2 APK Signature Scheme.
                  This scheme combines classical signatures (such as RSA or EC)
                  with ML-DSA signatures to enable post-quantum cryptography (PQC) hybrid signing.
                  This future-proofs your app's signing identity against the potential threat of
                  attacks that make use of quantum computing.

- **Apps using Play App Signing**:
                    If you use Play App Signing,
                    you can wait for Google Play to give you the option to upgrade to a hybrid
                    signature using a PQC key generated by Google Play.
- **Apps using self-managed keys**:
                    If you manage your own signing keys,
                    you can use updated Android build tools (such as`apksigner`)
                    to rotate to a hybrid identity,
                    combining a PQC key with a new classical key.
                    Note that you must create a new classical key;
                    you cannot reuse the older one.

`apksigner`
For more information, check out the[Android documentation on PQC APK signing](https://developer.android.com/about/versions/17/features#pqc-apk-signing)

## Shrink your code with R8

[R8](https://developer.android.com/studio/build/shrink-code)is the new code shrinker from Google.
                  It's enabled by default when you build a release APK or AAB.
                  To disable R8, pass the`--no-shrink`flag to`flutter build apk`or`flutter build appbundle`.

`--no-shrink`
`flutter build apk`
`flutter build appbundle`
## Enable multidex support

When writing large apps or making use of large plugins,
                  you might encounter Android's dex limit of 64k methods
                  when targeting a minimum API of 20 or below.
                  This might also be encountered when running debug versions of your app
                  using`flutter run`that doesn't have shrinking enabled.

`flutter run`
Flutter tool supports easily enabling multidex.
                  The simplest way is to opt into multidex support when prompted.
                  The tool detects multidex build errors and
                  asks before making changes to your Android project.
                  Opting in allows Flutter to automatically depend on`androidx.multidex:multidex`and use a generated`FlutterMultiDexApplication`as the project's application.

`androidx.multidex:multidex`
`FlutterMultiDexApplication`
When you try to build and run your app with the**Run**and**Debug**options in your IDE, your build might fail with the following message:

![Build failure because Multidex support is required](https://docs.flutter.dev/assets/images/docs/deployment/android/ide-build-failure-multidex.png)

To enable multidex from the command line,
                  run`flutter run --debug`and select an Android-powered device:

`flutter run --debug`
![Selecting an Android device with the flutter CLI.](https://docs.flutter.dev/assets/images/docs/deployment/android/cli-select-device.png)

When prompted, enter`y`.
                  The Flutter tool enables multidex support and retries the build:

`y`
![The output of a successful build after adding multidex.](https://docs.flutter.dev/assets/images/docs/deployment/android/cli-multidex-added-build.png)

You might also choose to manually support multidex by following Android's guides
                  and modifying your project's Android directory configuration.
                  A[multidex keep file](https://developer.android.com/studio/build/multidex#keep)must be specified to include:

`io/flutter/embedding/engine/loader/FlutterLoader.class
io/flutter/util/PathUtils.class`
Also, include any other classes used in app startup.
                  For more detailed guidance on adding multidex support manually,
                  check out the official[Android documentation](https://developer.android.com/studio/build/multidex).

## Review the app manifest

Review the default[App Manifest](https://developer.android.com/guide/topics/manifest/manifest-intro)file.

`<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:label="[project]"
        ...
    </application>
    ...
    <uses-permission android:name="android.permission.INTERNET"/>
</manifest>`
Verify the following values:

| Tag | Attribute | Value |
| --- | --- | --- |
| application | Edit theandroid:labelin theapplicationtag to reflect the final name of the app. |  |
| uses-permission | Add theandroid.permission.INTERNETpermissionvalue to theandroid:nameattribute if your app needs Internet access. The standard template doesn't include this tag but allows Internet access during development to enable communication between Flutter tools and a running app. |  |

`application`
`android:label`
`application`
`uses-permission`
`android.permission.INTERNET`
`android:name`
## Review the Gradle build configuration

To verify the Android build configuration,
                  review the`android`block in the default[Gradle build script](https://developer.android.com/studio/build/#module-level).
                  The default Gradle build script is found at`[project]/android/app/build.gradle.kts`.

`android`
`[project]/android/app/build.gradle.kts`
`android {
    namespace = "com.example.[project]"
    // Any value starting with "flutter." gets its value from
    // the Flutter Gradle plugin.
    // To change from these defaults, make your changes in this file.
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion
​
    ...
​
    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.example.[project]"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }
​
    buildTypes {
        ...
    }
}`
### Application ID

The`applicationId`is the unique identifier for your app on the Google Play Store
                  and on developers' devices.

`applicationId`
If you update the`applicationId`and`namespace`properties,
                  you must also update the`package`statement in your`MainActivity.kt`or`MainActivity.java`file and move the file
                  to the corresponding directory structure.

`applicationId`
`namespace`
`package`
`MainActivity.kt`
`MainActivity.java`
For example:

- In Kotlin, if your new ID is`com.example.myapp`,
                    move your`MainActivity`file to`android/app/src/main/kotlin/com/example/myapp/MainActivity.kt`and ensure the first line is`package com.example.myapp`.
- In Java, move your`MainActivity`file to`android/app/src/main/java/com/example/myapp/MainActivity.java`and ensure the first line is`package com.example.myapp`.

`com.example.myapp`
`MainActivity`
`android/app/src/main/kotlin/com/example/myapp/MainActivity.kt`
`package com.example.myapp`
`MainActivity`
`android/app/src/main/java/com/example/myapp/MainActivity.java`
`package com.example.myapp`
### Android SDK versions

The Flutter tooling sets default values for the Android SDK versions:

- **compileSdk**: The version of the Android SDK used to compile the app.
- **minSdk**: The minimum Android version that the app supports.
- **targetSdk**: The Android version the app is designed and tested to run on.

`compileSdk`
`minSdk`
`targetSdk`
These default values (`flutter.compileSdkVersion`, etc.) are managed by Flutter
                  to ensure compatibility with the framework and plugins.
                  You typically**do not**need to change these unless:

`flutter.compileSdkVersion`
1. **You need a newer API**: If you are using a plugin or feature that requires a higher`minSdk`than Flutter's default, you can manually set it to a higher version number
                    (for example,`minSdk = 24`).
1. **You need to lock versions**: If you want to prevent automatic updates to these versions
                    when upgrading Flutter, you can replace the default variables with specific integer values.

`minSdk`
`minSdk = 24`
### Version code and name

The`versionCode`and`versionName`are automatically set from your`pubspec.yaml`file
                  (using the`version: 1.0.0+1`field). You generally don't need to modify these in the Gradle file.

`versionCode`
`versionName`
`pubspec.yaml`
`version: 1.0.0+1`
## Build the app for release

You have two possible release formats when
                  publishing to the Play Store.

- App bundle (preferred)
- APK

### Build an app bundle

This section describes how to build a release app bundle.
                  If you completed the signing steps,
                  the app bundle will be signed.
                  At this point, you might consider[obfuscating your Dart code](https://docs.flutter.dev/deployment/obfuscate)to make it more difficult to reverse engineer.
                  Obfuscating your code involves adding flags to your build command and
                  maintaining additional files to de-obfuscate stack traces.

From the command line:

1. Enter`cd [project]`

1. Run`flutter build appbundle`
(Running`flutter build`defaults to a release build.)

`cd [project]`
`flutter build appbundle`
`flutter build`
The release bundle for your app is created at`[project]/build/app/outputs/bundle/release/app.aab`.

`[project]/build/app/outputs/bundle/release/app.aab`
By default, the app bundle contains your Dart code and the Flutter
                  runtime compiled for[armeabi-v7a](https://developer.android.com/ndk/guides/abis#v7a)(ARM 32-bit),[arm64-v8a](https://developer.android.com/ndk/guides/abis#arm64-v8a)(ARM 64-bit), and[x86-64](https://developer.android.com/ndk/guides/abis#86-64)(x86 64-bit).

### Test the app bundle

An app bundle can be tested in multiple ways.
                  This section describes two.

#### Offline using the bundle tool

1. If you haven't done so already, download`bundletool`from
                    its[GitHub repository](https://github.com/google/bundletool/releases/latest).
1. [Generate a set of APKs](https://developer.android.com/studio/command-line/bundletool#generate_apks)from your app bundle.
1. [Deploy the APKs](https://developer.android.com/studio/command-line/bundletool#deploy_with_bundletool)to connected devices.

`bundletool`
#### Online using Google Play

1. Upload your bundle to Google Play to test it.
                    You can use the internal test track,
                    or the alpha or beta channels to test the bundle before
                    releasing it in production.
1. Follow the steps to[upload your bundle](https://developer.android.com/studio/publish/upload-bundle)to the Play Store.

### Build an APK

Although app bundles are preferred over APKs,
                  there are stores that don't yet support app bundles.
                  In this case, build a release APK for
                  each target ABI (Application Binary Interface).

If you completed the signing steps, the APK will be signed.
                  At this point, you might consider[obfuscating your Dart code](https://docs.flutter.dev/deployment/obfuscate)to make it more difficult to reverse engineer.
                  Obfuscating your code involves adding flags to your build command.

From the command line:


Enter`cd [project]`.

`cd [project]`
Run`flutter build apk --split-per-abi`.
                      (The`flutter build`command defaults to`--release`.)

`flutter build apk --split-per-abi`
`flutter build`
`--release`
This command results in three APK files:

- `[project]/build/app/outputs/flutter-apk/app-armeabi-v7a-release.apk`
- `[project]/build/app/outputs/flutter-apk/app-arm64-v8a-release.apk`
- `[project]/build/app/outputs/flutter-apk/app-x86_64-release.apk`

`[project]/build/app/outputs/flutter-apk/app-armeabi-v7a-release.apk`
`[project]/build/app/outputs/flutter-apk/app-arm64-v8a-release.apk`
`[project]/build/app/outputs/flutter-apk/app-x86_64-release.apk`
Removing the`--split-per-abi`flag results in a fat APK that contains
                  your code compiled for*all*the target ABIs.
                  Such APKs are larger in size than their split counterparts,
                  causing the user to download native binaries that
                  aren't applicable to their device's architecture.

`--split-per-abi`
### Install an APK on a device

Follow these steps to install the APK on a connected Android-powered device.

From the command line:

1. Connect your Android-powered device to your computer with a USB cable.
1. Enter`cd [project]`.
1. Run`flutter install`.

`cd [project]`
`flutter install`
## Publish to the Google Play Store

For detailed instructions on publishing your app to the Google Play Store,
                  check out the[Google Play launch](https://developer.android.com/distribute)documentation.

## Update the app's version number

The default version number of the app is`1.0.0`.
                  To update it, navigate to the`pubspec.yaml`file
                  and update the following line:

`1.0.0`
`pubspec.yaml`
`version: 1.0.0+1`
The version number is three numbers separated by dots,
                  such as`1.0.0`in the preceding example,
                  followed by an optional build number,
                  such as`1`in the preceding example, separated by a`+`.

`1.0.0`
`1`
`+`
Both the version and the build number can be overridden in
                  Flutter's build by specifying`--build-name`and`--build-number`, respectively.

`--build-name`
`--build-number`
In Android,`build-name`is used as`versionName`while`build-number`used as`versionCode`. For more information,
                  check out[Version your app](https://developer.android.com/studio/publish/versioning)in the Android documentation.

`build-name`
`versionName`
`build-number`
`versionCode`
When you rebuild the app for Android, any updates in
                  the version number from the pubspec file will
                  update the`versionName`and`versionCode`in the`local.properties`file.

`versionName`
`versionCode`
`local.properties`
## Android release FAQ

Here are some commonly asked questions about deployment for
                  Android apps.

### When should I build app bundles versus APKs?

The Google Play Store recommends that you deploy app bundles
                  over APKs because they allow a more efficient delivery of the
                  application to your users. However, if you're distributing
                  your application by means other than the Play Store,
                  an APK might be your only option.

### What is a fat APK?

A[fat APK](https://en.wikipedia.org/wiki/Fat_binary)is a single APK that contains binaries for multiple
                  ABIs embedded within it. This has the benefit that the single APK
                  runs on multiple architectures and thus has wider compatibility,
                  but it has the drawback that its file size is much larger,
                  causing users to download and store more bytes when installing
                  your application. When building APKs instead of app bundles,
                  it is strongly recommended to build split APKs,
                  as described in[build an APK](#build-an-apk)using the`--split-per-abi`flag.

`--split-per-abi`
### What are the supported target architectures?

When building your application in release mode,
                  Flutter apps can be compiled for[armeabi-v7a](https://developer.android.com/ndk/guides/abis#v7a)(ARM 32-bit),[arm64-v8a](https://developer.android.com/ndk/guides/abis#arm64-v8a)(ARM 64-bit), and[x86-64](https://developer.android.com/ndk/guides/abis#86-64)(x86 64-bit).

### How do I sign the app bundle created byflutter build appbundle?

`flutter build appbundle`
Check out[Sign the app](#sign-the-app).

### How do I build a release from within Android Studio?

In Android Studio, open the existing`android/`folder under your app's folder. Then,
                  select**build.gradle (Module: app)**in the project panel:

`android/`
![The Gradle build script menu in Android Studio.](https://docs.flutter.dev/assets/images/docs/deployment/android/gradle-script-menu.png)

Next, select the build variant. Click**Build > Select Build Variant**in the main menu. Select any of the variants in the**Build Variants**panel (debug is the default):

![The build variant menu in Android Studio with Release selected.](https://docs.flutter.dev/assets/images/docs/deployment/android/build-variant-menu.png)

The resulting app bundle or APK files are located in`build/app/outputs`within your app's folder.

`build/app/outputs`
### How to tell if an apk uses Flutter?

You can use the[apkanalyzer](https://developer.android.com/tools/apkanalyzer)tool and list the files:

`apkanalyzer`
`apkanalyzer files list --files-only <SOME-APK> files list --files-only <SOME-APK>`
Then look for a file in`/lib/<ARCH>/libflutter.so`.

`/lib/<ARCH>/libflutter.so`
For example, the following should return a number greater than 0:

`apkanalyzer files list some-flutter-app.apk | grep flutter.so | wc -l`
**Why this works**

Flutter depends on C++ code used by the Flutter engine. In Android,
                  this code is bundled with the Flutter framework and the developer's
                  Dart code as a native library called`libflutter.so`.
                  The Java/Android tooling renames the`flutter`library with the`lib`prefix
                  and handles library location across architectures.
                  This is how some reverse engineer an APK to identify it as a Flutter app.

`libflutter.so`
`flutter`
`lib`
#### Secondary Evaluation:

Run`apkanalyzer manifest print <SOME-APK>`and look for a`<meta-data>`tag with`android:name="flutterEmbedding"`.
                  The value can be`1`or`2`.

`apkanalyzer manifest print <SOME-APK>`
`<meta-data>`
`android:name="flutterEmbedding"`
`1`
`2`
Example:`apkanalyzer manifest print some-flutter-app.apk | grep flutterEmbedding -C 2`returns the following style string.

`apkanalyzer manifest print some-flutter-app.apk | grep flutterEmbedding -C 2`
`<meta-data
   android:name="flutterEmbedding"
   android:value="2" />`
**Why this works**

Flutter has had two different embedders,
                  and this flag was read to determine which embedder was used.[Flutter 3.22](https://blog.flutter.dev/whats-new-in-flutter-3-22-fbde6c164fe3)removed the ability of v1 embedder apps to build.
                  This mechanism is not recommended because it's
                  unclear how long the`flutterEmbedding`value will
                  continue to be included in all Flutter apps.
                  Additionally, this won't work for all libraries written
                  in Flutter that are imported into Android apps as AAR dependencies.

`flutterEmbedding`
#### Non-technical evaluation

- Download[Flutter Shark](https://play.google.com/store/apps/details?id=com.fluttershark.fluttersharkapp&pli=1)on a device and let it scan local apps.
- Visit the[Flutter Hunt](https://flutterhunt.com/)website.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/android.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/deployment/android&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/android.md).
