> 原文链接: [https://docs.flutter.dev/add-to-app/android/project-setup](https://docs.flutter.dev/add-to-app/android/project-setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter can be embedded into your existing Android
                  application piecemeal, as a source code Gradle
                  subproject or as AARs.

The integration flow can be done using the Android Studio
                  IDE with the[Flutter plugin](https://plugins.jetbrains.com/plugin/9212-flutter)or manually.

## Integrate your Flutter module

- [With Android Studio](#65-tab-panel)
- [Without Android Studio](#66-tab-panel)

### Integrate with Android Studio

The Android Studio IDE can help integrate your Flutter module.
                        Using Android Studio, you can edit both your Android and Flutter code
                        in the same IDE.

You can also use IntelliJ Flutter plugin functionality like
                        Dart code completion, hot reload, and widget inspector.

To build your app, the Android Studio plugin configures your
                        Android project to add your Flutter module as a dependency.


Open your Android project in Android Studio.

Go to**File**>**New**>**New Project...**.
                             The**New Project**dialog displays.

Click**Flutter**.

If asked to provide your**Flutter SDK path**, do so and click**Next**.

Complete the configuration of your Flutter module.


If you have an existing project:

1. To choose an existing project, click**...**to the right of the**Project location**box.
1. Navigate to your Flutter project directory.
1. Click**Open**.

If you need to create a new Flutter project:

1. Complete the configuration dialog.
1. In the**Project type**menu, select**Module**.

Click**Finish**.

### Integrate without Android Studio

To integrate a Flutter module with an existing Android app
                        manually, without using Flutter's Android Studio plugin,
                        follow these steps:

#### Create a Flutter module

Assuming that you have an existing Android app at`some/path/MyApp`, and that you want your Flutter
                        project as a sibling, do the following:

`some/path/MyApp`
`cd some/path/
flutter create -t module --org com.example flutter_module`
This creates a`some/path/flutter_module/`Flutter module project
                        with some Dart code to get you started and a`.android/`hidden subfolder. The`.android`folder contains an
                        Android project that can both help you run a barebones
                        standalone version of your Flutter module with`flutter run`and it's also a wrapper that helps bootstrap the Flutter
                        module an embeddable Android library.

`some/path/flutter_module/`
`.android/`
`.android`
`flutter run`
#### Java version requirement

Flutter requires your project to declare compatibility with Java 17 or later.

Before attempting to connect your Flutter module project
                        to your host Android app, ensure that your host Android
                        app declares the following source compatibility within your
                        app's`build.gradle`file, under the`android { }`block.

`build.gradle`
`android { }`
`android {
    // ...
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17 // The minimum value
        targetCompatibility = JavaVersion.VERSION_17 // The minimum value
    }
    // ...
}`
#### Centralize repository settings

Starting with Gradle 7, Android recommends using centralized repository
                        declarations in`settings.gradle`instead of project or module level
                        declarations in`build.gradle`files.

`settings.gradle`
`build.gradle`
Before attempting to connect your Flutter module project to your
                        host Android app, make the following changes to your host app:

1. groovy@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Remove the`repositories`block in all of your app's`build.gradle`files.

`repositories`
`build.gradle`
`// Remove the following block, starting on the next line
    repositories {
        google()
        mavenCentral()
    }
// ...to the previous line`
Add the`dependencyResolutionManagement`displayed in this step to the`settings.gradle`file.

`dependencyResolutionManagement`
`settings.gradle`
- [Kotlin](#67-tab-panel)
- [Groovy](#68-tab-panel)

`dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    val storageUrl: String = System.getenv("FLUTTER_STORAGE_BASE_URL") ?: "https://storage.googleapis.com"
    repositories {
        google()
        mavenCentral()
        maven("$storageUrl/download.flutter.io")
    }
}`
`dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.PREFER_SETTINGS
    String storageUrl = System.env.FLUTTER_STORAGE_BASE_URL ?: "https://storage.googleapis.com"
    repositories {
        google()
        mavenCentral()
        maven {
            url = uri("$storageUrl/download.flutter.io")
        }
    }
}`
## Add the Flutter module as a dependency

Add the Flutter module as a dependency of your
                  existing app in Gradle. You can achieve this in two ways.


**Android archive**The AAR mechanism creates generic Android AARs as
                       intermediaries that packages your Flutter module.
                       This is good when your downstream app builders don't
                       want to have the Flutter SDK installed. But,
                       it adds one more build step if you build frequently.

**Module source code**The source code subproject mechanism is a convenient
                       one-click build process, but requires the Flutter SDK.
                       This is the mechanism used by the Android Studio IDE plugin.

- [Android Archive](#69-tab-panel)
- [Module source code](#72-tab-panel)

### Depend on the Android Archive (AAR)

This option packages your Flutter library as a generic local
                        Maven repository composed of AARs and POMs artifacts.
                        This option allows your team to build the host app without
                        installing the Flutter SDK. You can then distribute the
                        artifacts from a local or remote repository.

Let's assume you built a Flutter module at`some/path/flutter_module`, and then run:

`some/path/flutter_module`
`cd some/path/flutter_module
flutter build aar`
Then, follow the on-screen instructions to integrate.

More specifically, this command creates
                        (by default all debug/profile/release modes)
                        a[local repository](https://docs.gradle.org/current/userguide/declaring_repositories.html#sub:maven_local), with the following files:





- maven-metadata.xml
- maven-metadata.xml.md5
- maven-metadata.xml.sha1


- flutter_release-1.0.aar
- flutter_release-1.0.aar.md5
- flutter_release-1.0.aar.sha1
- flutter_release-1.0.pom
- flutter_release-1.0.pom.md5
- flutter_release-1.0.pom.sha1

- …

- …

To depend on the AAR, the host app must be able
                        to find these files.

To do that, edit`settings.gradle`in your host app
                        so that it includes the local repository and the dependency:

`settings.gradle`
- [Kotlin](#70-tab-panel)
- [Groovy](#71-tab-panel)

`dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        google()
        mavenCentral()
        maven("https://storage.googleapis.com/download.flutter.io")
        maven(url = "<some/path/flutter_module>/build/host/outputs/repo")
    }
}`
`dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.PREFER_SETTINGS
    repositories {
        google()
        mavenCentral()
​
        // Add the new repositories starting on the next line...
        maven {
            url = uri("<some/path/flutter_module>/build/host/outputs/repo")
            // This is relative to the location of the build.gradle file
            // if using a relative path.
        }
​
        maven {
            url = uri("https://storage.googleapis.com/download.flutter.io")
        }
        // ...to before this line
    }
}`
### Kotlin DSL based Android Project

After an`aar`build of a Kotlin DSL-based Android project,
                        follow these steps to add the flutter_module.

`aar`
Include the flutter module as a dependency in
                        the host app's`app/build.gradle`file.

`app/build.gradle`
`android {
    buildTypes {
        release {
          ...
        }
        debug {
          ...
        }
        create("profile") {
            initWith(getByName("debug"))
        }
}
​
dependencies {
  // ...
  debugImplementation("com.example.flutter_module:flutter_debug:1.0")
  releaseImplementation("com.example.flutter_module:flutter_release:1.0")
  add("profileImplementation", "com.example.flutter_module:flutter_profile:1.0")
}`
Add the custom`profileImplementation`dependency configuration to the end
                        of the same app-level build.gradle file.

`profileImplementation`
`configurations {
    getByName("profileImplementation") {
    }
}`
### Depend on the module's source code

This option enables a one-step build for both your
                        Android project and Flutter project. This option is
                        convenient when you work on both parts simultaneously
                        and rapidly iterate, but your team must install the
                        Flutter SDK to build the host app.

#### Updatingsettings.gradle

`settings.gradle`
Include the Flutter module as a subproject in the host app's`settings.gradle`. This example assumes`flutter_module`and`MyApp`exist in the same directory

`settings.gradle`
`flutter_module`
`MyApp`
If you are using Kotlin, apply the following changes:

`// Include the host app project. Assumed existing content.
include(":app")
// Replace "flutter_module" with whatever package_name you supplied when you ran:
// `$ flutter create -t module [package_name]
val filePath = settingsDir.parentFile.toString() + "/flutter_module/.android/include_flutter.groovy"
apply(from = File(filePath))`
If you are using Groovy, apply the following changes:

`// Include the host app project.
include(":app")                                   // assumed existing content
setBinding(new Binding([gradle: this]))           // new
def filePath = settingsDir.parentFile.toString() + "/flutter_module/.android/include_flutter.groovy" // new
apply from: filePath                              // new`
The binding and script evaluation allows the Flutter
                        module to`include`itself (as`:flutter`) and any
                        Flutter plugins used by the module (such as`:package_info`and`:video_player`)
                        in the evaluation context of your`settings.gradle`.

`include`
`:flutter`
`:package_info`
`:video_player`
`settings.gradle`
#### Updatingapp/build.gradle

`app/build.gradle`
Introduce an`implementation`dependency on the Flutter
                        module from your app:

`implementation`
`dependencies {
    implementation(project(":flutter"))
}`
Your app now includes the Flutter module as a dependency.

Continue to the[Adding a Flutter screen to an Android app](https://docs.flutter.dev/add-to-app/android/add-flutter-screen)guide.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/project-setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/add-to-app/android/project-setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/project-setup.md).
