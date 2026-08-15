> 原文链接: [https://docs.flutter.dev/perf/deferred-components](https://docs.flutter.dev/perf/deferred-components)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Introduction

With Flutter, Android and web apps have the capability to download deferred
                  components (additional code and assets) while the app is already running. This
                  is helpful if you have a large app and only want to install components if and
                  when they are needed by the user.

While Flutter supports deferred loading on Android and the web, the
                  implementations differ. Both require[Dart's deferred imports](https://dart.dev/language/libraries#lazily-loading-a-library).


Android's[dynamic feature modules](https://developer.android.com/guide/playcore/feature-delivery)deliver the
                      deferred components packaged as Android modules.

When building for Android, though you can defer loading modules,
                      you must build the entire app and upload that app as a single[Android App Bundle](https://developer.android.com/guide/app-bundle)(AAB).
                      Flutter doesn't support dispatching partial updates without re-uploading
                      new Android App Bundles for the entire application.

Flutter performs deferred loading when you compile your Android app
                      in[release or profile mode](https://docs.flutter.dev/testing/build-modes), but debug mode treats all
                      deferred components as regular imports.

The web creates deferred components as separate`*.js`files.

`*.js`
For a deeper dive into the technical details of
                  how this feature works, see[Deferred Components](https://github.com/flutter/flutter/wiki/Deferred-Components)on the[Flutter wiki](https://github.com/flutter/flutter/tree/main/docs).

## How to set your Android project up for deferred components

The following instructions explain how to set up your
                  Android app for deferred loading.

### Step 1: Dependencies and initial project setup

1. android/app/build.gradle.ktskotlin@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonandroid/app/build.gradlegroovy@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. xml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonjava@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. yaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Add Play Core to the Android app's
build.gradle dependencies.
In`android/app/build.gradle`add the following:

`android/app/build.gradle`
- [Kotlin](#200-tab-panel)
- [Groovy](#201-tab-panel)

`...
dependencies {
  ...
  implementation("com.google.android.play:core:1.8.0")
  ...
}`
`...
dependencies {
  ...
  implementation "com.google.android.play:core:1.8.0"
  ...
}`
If using the Google Play Store as the
distribution model for dynamic features,
the app must support`SplitCompat`and provide an instance
of a`PlayStoreDeferredComponentManager`.
Both of these tasks can be accomplished by setting
the`android:name`property on the application in`android/app/src/main/AndroidManifest.xml`to`io.flutter.embedding.android.FlutterPlayStoreSplitApplication`:

`SplitCompat`
`PlayStoreDeferredComponentManager`
`android:name`
`android/app/src/main/AndroidManifest.xml`
`io.flutter.embedding.android.FlutterPlayStoreSplitApplication`
`<manifest ...
  <application
     android:name="io.flutter.embedding.android.FlutterPlayStoreSplitApplication"
        ...
  </application>
</manifest>`
`io.flutter.app.FlutterPlayStoreSplitApplication`handles
both of these tasks for you. If you use`FlutterPlayStoreSplitApplication`,
you can skip to step 1.3.

`io.flutter.app.FlutterPlayStoreSplitApplication`
`FlutterPlayStoreSplitApplication`
If your Android application
is large or complex, you might want to separately support`SplitCompat`and provide the`PlayStoreDynamicFeatureManager`manually.

`SplitCompat`
`PlayStoreDynamicFeatureManager`
To support`SplitCompat`, there are three methods
(as detailed in the[Android docs](https://developer.android.com/guide/playcore/feature-delivery#declare_splitcompatapplication_in_the_manifest)), any of which are valid:

`SplitCompat`
- java@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
- java@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
- xml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Make your application class extend`SplitCompatApplication`:

`SplitCompatApplication`
`public class MyApplication extends SplitCompatApplication {
    ...
}`
Call`SplitCompat.install(this);`in the`attachBaseContext()`method:

`SplitCompat.install(this);`
`attachBaseContext()`
`@Override
protected void attachBaseContext(Context base) {
    super.attachBaseContext(base);
    // Emulates installation of future on demand modules using SplitCompat.
    SplitCompat.install(this);
}`
Declare`SplitCompatApplication`as the application
subclass and add the Flutter compatibility code from`FlutterApplication`to your application class:

`SplitCompatApplication`
`FlutterApplication`
`<application
    ...
    android:name="com.google.android.play.core.splitcompat.SplitCompatApplication">
</application>`
The embedder relies on an injected`DeferredComponentManager`instance to handle
install requests for deferred components.
Provide a`PlayStoreDeferredComponentManager`into
the Flutter embedder by adding the following code
to your app initialization:

`DeferredComponentManager`
`PlayStoreDeferredComponentManager`
`import io.flutter.embedding.engine.dynamicfeatures.PlayStoreDeferredComponentManager;
import io.flutter.FlutterInjector;
...
PlayStoreDeferredComponentManager deferredComponentManager = new
  PlayStoreDeferredComponentManager(this, null);
FlutterInjector.setInstance(new FlutterInjector.Builder()
    .setDeferredComponentManager(deferredComponentManager).build());`
Opt into deferred components by adding
the`deferred-components`entry to the app's`pubspec.yaml`under the`flutter`entry:

`deferred-components`
`pubspec.yaml`
`flutter`
`...
flutter:
  ...
  deferred-components:
  ...`
The`flutter`tool looks for the`deferred-components`entry in the`pubspec.yaml`to determine whether the
app should be built as deferred or not.
This can be left empty for now unless you already
know the components desired and the Dart deferred libraries
that go into each. You will fill in this section later
in[step 3.3](#step-3.3)once`gen_snapshot`produces the loading units.

`flutter`
`deferred-components`
`pubspec.yaml`
`gen_snapshot`
### Step 2: Implementing deferred Dart libraries

Next, implement deferred loaded Dart libraries in your
                  app's Dart code. The implementation doesn't need
                  to be feature complete yet. The example in the
                  rest of this page adds a new simple deferred widget
                  as a placeholder. You can also convert existing code
                  to be deferred by modifying the imports and
                  guarding usages of deferred code behind`loadLibrary()``Futures`.

`loadLibrary()`
`Futures`
1. code-excerpt "lib/box.dart"box.dartdart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. code-excerpt "lib/use_deferred_box.dart"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Create a new Dart library.
For example, create a new`DeferredBox`widget that
can be downloaded at runtime.
This widget can be of any complexity but,
for the purposes of this guide,
create a simple box as a stand-in.
To create a simple blue box widget,
create`box.dart`with the following contents:

`DeferredBox`
`box.dart`
`import 'package:flutter/material.dart';
​
/// A simple blue 30x30 box.
class DeferredBox extends StatelessWidget {
  const DeferredBox({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Container(height: 30, width: 30, color: Colors.blue);
  }
}`
Import the new Dart library
with the`deferred`keyword in your app and
call`loadLibrary()`(see[lazily loading a library](https://dart.dev/language/libraries#lazily-loading-a-library)).
The following example uses`FutureBuilder`to wait for the`loadLibrary``Future`(created in`initState`) to complete and display a`CircularProgressIndicator`as a placeholder.
When the`Future`completes, it returns the`DeferredBox`widget.`SomeWidget`can then be used in the app as normal and
won't ever attempt to access the deferred Dart code until
it has successfully loaded.

`deferred`
`loadLibrary()`
`FutureBuilder`
`loadLibrary`
`Future`
`initState`
`CircularProgressIndicator`
`Future`
`DeferredBox`
`SomeWidget`
`import 'package:flutter/material.dart';
import 'box.dart' deferred as box;
​
class SomeWidget extends StatefulWidget {
  const SomeWidget({super.key});
​
  @override
  State<SomeWidget> createState() => _SomeWidgetState();
}
​
class _SomeWidgetState extends State<SomeWidget> {
  late Future<void> _libraryFuture;
​
  @override
  void initState() {
    super.initState();
    _libraryFuture = box.loadLibrary();
  }
​
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<void>(
      future: _libraryFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          }
          return box.DeferredBox();
        }
        return const CircularProgressIndicator();
      },
    );
  }
}`
The`loadLibrary()`function returns a`Future<void>`that completes successfully when the code in the library
is available for use and completes with an error otherwise.
All usage of symbols from the deferred library should be
guarded behind a completed`loadLibrary()`call. All imports
of the library must be marked as`deferred`for it to be
compiled appropriately to be used in a deferred component.
If a component has already been loaded, additional calls
to`loadLibrary()`complete quickly (but not synchronously).
The`loadLibrary()`function can also be called early to
trigger a pre-load to help mask the loading time.

`loadLibrary()`
`Future<void>`
`loadLibrary()`
`deferred`
`loadLibrary()`
`loadLibrary()`
You can find another example of deferred import loading in[Flutter Gallery'slib/deferred_widget.dart](https://github.com/flutter/gallery/blob/main/lib/deferred_widget.dart).

`lib/deferred_widget.dart`
### Step 3: Building the app

Use the following`flutter`command to build a
                  deferred components app:

`flutter`
`$ flutter build appbundle`
This command assists you by validating that your project
                  is properly set up to build deferred components apps.
                  By default, the build fails if the validator detects
                  any issues and guides you through suggested changes to fix them.

1. yaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonyaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. yaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. android/settings.gradle.ktskotlin@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_buttonandroid/settings.gradlegroovy@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

The`flutter build appbundle`command
runs the validator and attempts to build the app with`gen_snapshot`instructed to produce split AOT shared libraries
as separate SO files. On the first run, the validator will
likely fail as it detects issues; the tool makes
recommendations for how to set up the project and fix these issues.

`flutter build appbundle`
`gen_snapshot`
The validator is split into two sections: prebuild
and post-gen_snapshot validation. This is because any
validation referencing loading units can't be performed
until`gen_snapshot`completes and produces a final set
of loading units.

`gen_snapshot`
The validator detects any new, changed, or removed
loading units generated by`gen_snapshot`.
The current generated loading units are tracked in your`<projectDirectory>/deferred_components_loading_units.yaml`file.
This file should be checked into source control to ensure that
changes to the loading units by other developers can be caught.

`gen_snapshot`
`<projectDirectory>/deferred_components_loading_units.yaml`
The validator also checks for the following in the`android`directory:

`android`
- xml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
- xml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

**<projectDir>/android/app/src/main/res/values/strings.xml**
An entry for every deferred component mapping the key`${componentName}Name`to`${componentName}`.
This string resource is used by the`AndroidManifest.xml`of each feature module to define the`dist:title property`.
For example:

`<projectDir>/android/app/src/main/res/values/strings.xml`
`${componentName}Name`
`${componentName}`
`AndroidManifest.xml`
`dist:title property`
`<?xml version="1.0" encoding="utf-8"?>
<resources>
  ...
  <string name="boxComponentName">boxComponent</string>
</resources>`
**<projectDir>/android/<componentName>**
An Android dynamic feature module for
each deferred component exists and contains a`build.gradle`and`src/main/AndroidManifest.xml`file.
This only checks for existence and doesn't validate
the contents of these files. If a file doesn't exist,
it generates a default recommended one.

`<projectDir>/android/<componentName>`
`build.gradle`
`src/main/AndroidManifest.xml`
**<projectDir>/android/app/src/main/res/values/AndroidManifest.xml**
Contains a meta-data entry that encodes
the mapping between loading units and component name the
loading unit is associated with. This mapping is used by the
embedder to convert Dart's internal loading unit id
to the name of a deferred component to install. For example:

`<projectDir>/android/app/src/main/res/values/AndroidManifest.xml`
`...
<application
    android:label="MyApp"
    android:name="io.flutter.app.FlutterPlayStoreSplitApplication"
    android:icon="@mipmap/ic_launcher">
    ...
    <meta-data android:name="io.flutter.embedding.engine.deferredcomponents.DeferredComponentManager.loadingUnitMapping" android:value="2:boxComponent"/>
</application>
...`
The`gen_snapshot`validator won't run until the prebuild
validator passes.

`gen_snapshot`
or each of these checks,
the tool produces the modified or new files
needed to pass the check.
These files are placed in the`<projectDir>/build/android_deferred_components_setup_files`directory.
It is recommended that the changes be applied by
copying and overwriting the same files in the
project's`android`directory. Before overwriting,
the current project state should be committed to
source control and the recommended changes should be
reviewed to be appropriate. The tool won't make any
changes to your`android/`directory automatically.

`<projectDir>/build/android_deferred_components_setup_files`
`android`
`android/`
Once the available
loading units are generated and logged in`<projectDirectory>/deferred_components_loading_units.yaml`,
it is possible to fully configure the pubspec's`deferred-components`section so that the loading units
are assigned to deferred components as desired.
To continue with the box example, the generated`deferred_components_loading_units.yaml`file would contain:

`<projectDirectory>/deferred_components_loading_units.yaml`
`deferred-components`
`deferred_components_loading_units.yaml`
`loading-units:
  - id: 2
    libraries:
      - package:MyAppName/box.Dart`
The loading unit id ('2' in this case) is used
internally by Dart, and can be ignored.
The base loading unit (id '1') is not listed
and contains everything not explicitly contained
in another loading unit.

You can now add the following to`pubspec.yaml`:

`pubspec.yaml`
`...
flutter:
  ...
  deferred-components:
    - name: boxComponent
      libraries:
        - package:MyAppName/box.Dart
  ...`
To assign a loading unit to a deferred component,
add any Dart library in the loading unit into the
libraries section of the feature module.
Keep the following guidelines in mind:


Loading units shouldn't be included
in more than one component.

Including one Dart library from a
loading unit indicates that the entire loading
unit is assigned to the deferred component.

All loading units not assigned to
a deferred component are included in the base component,
which always exists implicitly.

Loading units assigned to the same
deferred component are downloaded, installed,
and shipped together.

The base component is implicit and
need not be defined in the pubspec.

Assets can also be included by adding
an assets section in the deferred component configuration:

`deferred-components:
    - name: boxComponent
      libraries:
        - package:MyAppName/box.Dart
      assets:
        - assets/image.jpg
        - assets/picture.png
          # wildcard directory
        - assets/gallery/`
An asset can be included in multiple deferred components,
but installing both components results in a replicated asset.
Assets-only components can also be defined by omitting the
libraries section. These assets-only components must be
installed with the[DeferredComponent](https://api.flutter.dev/flutter/services/DeferredComponent-class.html)utility class in
services rather than`loadLibrary()`.
Since Dart libraries are packaged together with assets,
if a Dart library is loaded with`loadLibrary()`,
any assets in the component are loaded as well.
However, installing by component name and the services utility
won't load any Dart libraries in the component.

`DeferredComponent`
`loadLibrary()`
`loadLibrary()`
You are free to include assets in any component,
as long as they are installed and loaded when they
are first referenced, though typically,
assets and the Dart code that uses those assets
are best packed in the same component.

Manually add all deferred components
that you defined in`pubspec.yaml`into the`android/settings.gradle`file as includes.
For example, if there are three deferred components
defined in the pubspec named,`boxComponent`,`circleComponent`,
and`assetComponent`, ensure that`android/settings.gradle`contains the following:

`pubspec.yaml`
`android/settings.gradle`
`boxComponent`
`circleComponent`
`assetComponent`
`android/settings.gradle`
- [Kotlin](#202-tab-panel)
- [Groovy](#203-tab-panel)

`include(":app", ":boxComponent", ":circleComponent", ":assetComponent")
...`
`include ':app', ':boxComponent', ':circleComponent', ':assetComponent'
...`
Repeat steps[3.1](#step-3.1)through 3.6 (this step)
until all validator recommendations are handled and the tool
runs without further recommendations.

When successful, this command outputs an`app-release.aab`file in`build/app/outputs/bundle/release`.

`app-release.aab`
`build/app/outputs/bundle/release`
A successful build doesn't always mean the app was
built as intended. It is up to you to ensure that all loading
units and Dart libraries are included in the way you intended.
For example, a common mistake is accidentally importing a
Dart library without the`deferred`keyword,
resulting in a deferred library being compiled as part of
the base loading unit. In this case, the Dart library would
load properly because it is always present in the base,
and the library wouldn't be split off. This can be checked
by examining the`deferred_components_loading_units.yaml`file to verify that the generated loading units are described
as intended.

`deferred`
`deferred_components_loading_units.yaml`
When adjusting the deferred components configurations,
or making Dart changes that add, modify, or remove loading units,
you should expect the validator to fail.
Follow steps[3.1](#step-3.1)through 3.6 (this step) to apply any
recommended changes to continue the build.

### Running the app locally

Once your app has successfully built an AAB file,
                  use Android's[bundletool](https://developer.android.com/studio/command-line/bundletool)to perform
                  local testing with the`--local-testing`flag.

`bundletool`
`--local-testing`
To run the AAB file on a test device,
                  download the bundletool jar executable from[github.com/google/bundletool/releases](https://github.com/google/bundletool/releases)and run:

`$ java -jar bundletool.jar build-apks --bundle=<your_app_project_dir>/build/app/outputs/bundle/release/app-release.aab --output=<your_temp_dir>/app.apks --local-testing

$ java -jar bundletool.jar install-apks --apks=<your_temp_dir>/app.apks`
Where`<your_app_project_dir>`is the path to your app's
                  project directory and`<your_temp_dir>`is any temporary
                  directory used to store the outputs of bundletool.
                  This unpacks your AAB file into an APK file and
                  installs it on the device. All available Android dynamic
                  features are loaded onto the device locally and
                  installation of deferred components is emulated.

`<your_app_project_dir>`
`<your_temp_dir>`
Before running`build-apks`again,
                  remove the existing app APK file:

`build-apks`
`$ rm <your_temp_dir>/app.apks`
Changes to the Dart codebase require either incrementing
                  the Android build ID or uninstalling and reinstalling
                  the app, as Android won't update the feature modules
                  unless it detects a new version number.

### Releasing to the Google Play Store

The built AAB file can be uploaded directly to
                  the Play store as normal. When`loadLibrary()`is called,
                  the needed Android module containing the Dart AOT library and
                  assets is downloaded by the Flutter engine using the
                  Play store's delivery feature.

`loadLibrary()`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/deferred-components.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/perf/deferred-components&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/deferred-components.md).
