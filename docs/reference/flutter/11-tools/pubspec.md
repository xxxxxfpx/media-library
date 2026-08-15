> 原文链接: [https://docs.flutter.dev/tools/pubspec](https://docs.flutter.dev/tools/pubspec)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This page is primarily aimed at folks who write
                  Flutter apps. If you write packages or plugins,
                  (perhaps you want to create a federated plugin),
                  you should check out the[Developing packages and plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages)page.

## Overview

Every Flutter project includes a`pubspec.yaml`file,
                  often referred to as*the pubspec*.
                  A basic pubspec is generated when you create
                  a new Flutter project. It's located at the top
                  of the project tree and contains metadata about
                  the project that the Dart and Flutter tooling
                  needs to know. The pubspec is written in[YAML](https://yaml.org/), which is human readable, but be aware
                  that*white space (tabs v spaces) matters*.

`pubspec.yaml`
The pubspec specifies dependencies
                  that the project requires, such as:

- Particular packages and their versions
- Fonts
- Images
- Developer packages (like testing or mocking packages)
- Particular constraints on the version of the Flutter SDK

Fields common to both Dart and Flutter projects
                  are described in[the pubspec file](https://dart.dev/tools/pub/pubspec)on[dart.dev](https://dart.dev).
                  This page lists*Flutter-specific*fields and packages
                  that are only valid for a Flutter project.

## Example

When you create a new project with the`flutter create`command (or by using the
                  equivalent button in your IDE), it creates
                  a pubspec for a basic Flutter app.

`flutter create`
The first time you build your project, it
                  also creates a`pubspec.lock`file that contains
                  specific versions of the included packages.
                  This ensures that you get the same version
                  the next time the project is built.

`pubspec.lock`
Here is an example of a Flutter project pubspec file.
                  The Flutter-only fields and packages are highlighted.

`name: <project name>
description: A new Flutter project.
​
publish_to: none
version: 1.0.0+1
​
environment:
  sdk: ^3.11.0
​
dependencies:
  flutter:       # Required for every Flutter project
    sdk: flutter # Required for every Flutter project
  flutter_localizations: # Required to enable localization
    sdk: flutter         # Required to enable localization
​
  cupertino_icons: ^1.0.8 # Only required if you use Cupertino (iOS style) icons
​
dev_dependencies:
  flutter_test:
    sdk: flutter # Required for a Flutter project that includes tests
​
  flutter_lints: ^6.0.0 # Contains a set of recommended lints for Flutter code
​
flutter:
​
  uses-material-design: true # Required if you use the Material icon font
​
  generate: true # Enables generation of localized strings from arb files
​
  config: # App-specific configuration flags that mirror `flutter config`
    enable-swift-package-manager: true
​
  assets:  # Lists assets, such as image files
    - images/a_dot_burr.png
    - images/a_dot_ham.png
​
  licenses: # Lists additional license files to be bundled with the app
    - assets/my_license.txt
​
  fonts:              # Required if your app uses custom fonts
    - family: Schyler
      fonts:
        - asset: fonts/Schyler-Regular.ttf
        - asset: fonts/Schyler-Italic.ttf
          style: italic
    - family: Trajan Pro
      fonts:
        - asset: fonts/TrajanPro.ttf
        - asset: fonts/TrajanPro_Bold.ttf
          weight: 700`
## Fields

Flutter-specific and Dart-specific fields can be added to
                  the Flutter pubspec. To learn more about Flutter-specific
                  fields, see the following sections. To learn more about
                  Dart-specific fields, see[Dart's pubspec supported fields](https://dart.dev/tools/pub/pubspec#supported-fields).

### assets field

A list of asset paths that your app uses. These assets are
                  bundled with your application. Common types of assets
                  include static data (for example,`JSON`),
                  configuration files, icons, and images (`JPEG`,`WebP`,`GIF`, animated`WebP/GIF`,`PNG`,`BMP`, and`WBMP`).

`JSON`
`JPEG`
`WebP`
`GIF`
`WebP/GIF`
`PNG`
`BMP`
`WBMP`
Besides listing the images that are included in the
                  app package, an image asset can also refer to one or more
                  resolution-specific "variants". For more information,
                  see the[resolution aware](https://docs.flutter.dev/ui/assets/assets-and-images#resolution-aware)section of the[Assets and images](https://docs.flutter.dev/ui/assets/assets-and-images)page.
                  For information on adding assets from package
                  dependencies, see the[asset images in package dependencies](https://docs.flutter.dev/ui/assets/assets-and-images#from-packages)section in the same page.

The`asset`field has this structure:

`asset`
`flutter:
  assets:
    - [ path_to_file | path_to_directory ]
      [ flavor_path_field | platform_path_field ]
    [...]`
`# path_to_file structure
- path/to/directory/file`
`# path_to_directory structure
- path/to/directory/`
`# flavor_path_field strucure
- path: path/to/directory
  flavors:
  - flavor_name`
`# platform_path_field structure
- path: path/to/file
  platforms:
    - platform_name`
Subfields of`assets`:

`assets`
- `path_to_file`: A string that represents the path to
                    a file.
- `path_to_directory`: A string that represents the path to
                    a directory.
- `flavor_path_field`: A path field and its flavor
                    subfields.
- `platform_path_field`: A path field and its platform
                    subfields.
- `path`: The path to an asset file or directory.
- `flavors`: A list of flutter flavors to use with assets
                    at a specific path. To learn more about
                    flavors, see[Set up flavors for iOS and macOS](https://docs.flutter.dev/deployment/flavors-ios)and[Set up flavors for Android](https://docs.flutter.dev/deployment/flavors).
- `platforms`: A list of platforms to use with assets at a
                    specific path. Valid values are`android`,`ios`,`web`,`linux`,`macos`, and`windows`.

`path_to_file`
`path_to_directory`
`flavor_path_field`
`platform_path_field`
`path`
`flavors`
`platforms`
`android`
`ios`
`web`
`linux`
`macos`
`windows`
You can pass in a path to a file:

`flutter:
  assets:
    - assets/images/my_image_a.png
    - assets/images/my_image_b.png`
You can pass in a path to a directory:

`flutter:
  assets:
    - assets/images/
    - assets/icons/`
You can pass in a path to a directory for specific
                  flavors:

`flutter:
  assets:
    - path: assets/flavor_a_and_b/images
      flavors:
      - flavor_a
      - flavor_b
    - path: assets/flavor_c/images
      flavors:
      - flavor_c`
You can pass in a path to a file for specific platforms:

`flutter:
  assets:
    - path: assets/web_worker.js
      platforms:
        - web
    - path: assets/desktop_icon.png
      platforms:
        - windows
        - linux
        - macos`
### config field

A map of keys to flags (`true`or`false`) that influences how the`flutter`CLI
                  is executed.

`true`
`false`
`flutter`
> NOTE: This feature is only available as of[#167953](https://github.com/flutter/flutter/pull/167953)on the`main`channel.

NOTE: This feature is only available as of[#167953](https://github.com/flutter/flutter/pull/167953)on the`main`channel.

`main`
The available keys mirror those available in`flutter config --list`.

`flutter config --list`
`flutter:
  config:
    cli-animations: false
    enable-swift-package-manager: true`
Use`flutter config --help`for a description of each flag.

`flutter config --help`
Flags are only read from the current*application*package, and have no effect
                  in the context of a package or dependency.

### default-flavor field

Assign a default Flutter flavor for an app.
                  When used, you don't need to include the name of this
                  flavor in Flutter launch command.

`flutter:
  default-flavor: flavor_name`
In the following example, an Android Flutter app has a
                  flavor called`staging`and`production`. The`production`flavor is the default flavor. When that flavor is run,
                  you don't need to include it in the launch command.

`staging`
`production`
`production`
`flutter:
  default-flavor: production`
`// Use this command to run the default flavor (production).
flutter run

// Use this command to run non-default flavors (staging).
flutter run --flavor staging`
To learn how to create Flutter flavors,
                  see[Set up Flutter flavors for Android](https://docs.flutter.dev/deployment/flavors)and[Set up Flutter flavors for iOS and macOS](https://docs.flutter.dev/deployment/flavors-ios).

### deferred-components field

Defer initial the download size of an Android app. Most
                  often used with large applications, modularized applications,
                  and applications with on-demand features.

The`deferred-components`field has this structure:

`deferred-components`
`flutter:
  deferred-components:
    name: component_name
      libraries:
        - string_expression
        [...]
      assets:
        - string_expression
        [...]
    [...]`
Deferred component subfields:

- `name`: The unique identifier for a specific deferred
                    component.
- `libraries`: A list of Dart libraries that are part of
                    the deferred component.
- `assets`: A list of asset paths that are associated with
                    the deferred component.

`name`
`libraries`
`assets`
Example:

`flutter:
  deferred-components:
    - name: box_component
      libraries:
        - package:testdeferredcomponents/box.dart
    - name: gallery_feature
      libraries:
        - package:testdeferredcomponents/gallery_feature.dart
      assets:
        - assets/gallery_images/gallery_feature.png`
To learn more about how you can use deferred components with
                  a Flutter Android app, see[Deferred components for Android](https://docs.flutter.dev/perf/deferred-components).

### disable-swift-package-manager field

Disable the use of the Swift Package Manager (SPM) so that
                  it no longer manages dependencies in your iOS and macOS
                  Flutter projects.

`flutter:
  disable-swift-package-manager: true`
> NOTE: As of[#168433](https://github.com/flutter/flutter/pull/168433)on the`main`channel, this property has moved to the[config](#config)section:
> pubspec.yamlyaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

NOTE: As of[#168433](https://github.com/flutter/flutter/pull/168433)on the`main`channel, this property has moved to the[config](#config)section:

`main`
`config`
`flutter:
  config:
    enable-swift-package-manager: false`
### flutter field

A field that contains Flutter-specific settings for your
                  app.

`flutter:
  [flutter_field]
  [...]`
### fonts field

Configure and include custom fonts in your Flutter
                  application.

For examples of using fonts
                  see the[Use a custom font](https://docs.flutter.dev/cookbook/design/fonts)and[Export fonts from a package](https://docs.flutter.dev/cookbook/design/package-fonts)recipes in the
                  Flutter cookbook.

The`fonts`field has this structure:

`fonts`
`flutter:
  fonts:
    -  { font_family_field | font_asset_field }
    [...]`
`# font_family_field structure
- family: font_name
      fonts:
        - font_asset_field
        [...]`
`# font_asset_field structure
- asset: path/to/directory/font_name
  weight: int_expression # Optional
  style: string_expression # Optional`
Subfields of`fonts`:

`fonts`
- `family`: Optional. The font family name. Can have
                    multiple font assets.
- `asset`: The font to use.
- `weight`: Optional. The weight of the font. This can be`100`,`200`,`300`,`400`,`500`,`600`,`700`,`800`or`900`.
- `style`: Optional. The style of the font. This can be`italic`.

`family`
`asset`
`weight`
`100`
`200`
`300`
`400`
`500`
`600`
`700`
`800`
`900`
`style`
`italic`
Use a font that is not part of a font family:

`flutter:
  fonts:
    - asset: fonts/Roboto-Regular.ttf
      weight: 900 # Optional
      style: italic # Optional`
Use a font family:

`flutter:
  fonts:
  - family: Roboto # Optional
        fonts:
          - asset: fonts/Roboto-Regular.ttf
          - asset: fonts/Roboto-Bold.ttf
            weight: 700 # Optional
            style: italic # Optional`
Alternatively, if you have a font that requires no family,
                  weight or style requirements, you can declare it as a simple
                  asset:

`flutter:
  assets:
    - fonts/Roboto-Regular.ttf`
### generate field

Handles localization tasks. This field can appear as a
                  subfield of`flutter`and`material`.

`flutter`
`material`
Enable general localization:

`flutter:
  generate: true`
### licenses field

A list of additional license file paths that should be bundled with your
                  application. These files are typically found within your project's`assets`directory.

`assets`
The`licenses`field has this structure:

`licenses`
`flutter:
  licenses:
    - [path_to_file]`
### plugin field

Configure settings specifically for Flutter plugins.

The`plugin`field has this structure:

`plugin`
`flutter:
  plugin:
    platforms:
      android: # Optional
        package: com.example.my_plugin
        pluginClass: MyPlugin
        dartPluginClass: MyPluginClassName
        ffiPlugin: true
        default_package: my_plugin_name
        fileName: my_file.dart
      ios: # Optional
        pluginClass: MyPlugin
        dartPluginClass: MyPluginClassName
        ffiPlugin: true
        default_package: my_plugin_name
        fileName: my_file.dart
        sharedDarwinSource: true
      macos: # Optional
        pluginClass: MyPlugin
        dartPluginClass: MyPluginClassName
        ffiPlugin: true
        default_package: my_plugin_name
        fileName: my_file.dart
        sharedDarwinSource: true
      windows: # Optional
        pluginClass: MyPlugin
        dartPluginClass: MyPluginClassName
        ffiPlugin: true
        default_package: my_plugin_name
        fileName: my_file.dart
      linux: # Optional
        pluginClass: MyPlugin
        dartPluginClass: MyPluginClassName
        ffiPlugin: true
        default_package: my_plugin_name
        fileName: my_file.dart
      web: # Optional
        ffiPlugin: true
        default_package: my_plugin_name
        fileName: my_file.dart
    implements: # Optional
      - example_platform_interface`
Subfields of`plugin`:

`plugin`
- `platforms`: A list of platforms that will have
                    configuration settings.
- `package`: The Android package name of the plugin. This
                    can be used with the Android platform and is required.
- `pluginClass`: The name of the plugin class. Optional if`dartPluginClass`is used for the same platform. This
                    can be used with the Android, iOS, Linux macOS, and
                    Windows platforms.
- `default_package`: Optional. The package that should be
                    used as the default implementation of a platform
                    interface. Only applicable to federated plugins, where the
                    plugin's implementation is split into multiple
                    platform-specific packages.
- `dartPluginClass`: Optional. The Dart class that serves
                    as the entry point for a Flutter plugin. This
                    can be used with the Android, iOS, Linux macOS, and
                    Windows platforms.
- `sharedDarwinSource`: Optional. Indicates that the plugin
                    shares native code between iOS and macOS. This
                    can be used with the iOS and macOS platforms.
- `fileName`: Optional. The file that contains the plugin
                    class.
- `ffiPlugin`: Optional. True if the plugin uses a
                    Foreign Function Interface (FFI).
- `implements`: Optional. The platform interfaces that a
                    Flutter plugin implements.

`platforms`
`package`
`pluginClass`
`dartPluginClass`
`default_package`
`dartPluginClass`
`sharedDarwinSource`
`fileName`
`ffiPlugin`
`implements`
To learn more about plugins, see[Developing packages & plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages).

### shaders field

GLSL Shaders with the`FRAG`extension, must be declared in
                  the shaders section of your project's`pubspec.yaml`file.
                  The Flutter command-line tool compiles the shader to its
                  appropriate backend format, and generates its necessary
                  runtime metadata. The compiled shader is then included in
                  the application just like an asset.

`FRAG`
`pubspec.yaml`
The`shaders`field has this structure:

`shaders`
`flutter:
  shaders:
    -  { path_to_file | path_to_directory }
    [...]`
`# path_to_file structure
- assets/shaders/file`
`# path_to_directory structure
- assets/shaders/`
Add specific shaders:

`flutter:
  shaders:
    - assets/shaders/shader_a.frag
    - assets/shaders/shader_b.frag`
Add a directory of shaders:

`flutter:
  shaders:
    - assets/shaders/`
Alternatively, you can add your shader directory to the`assets`field:

`assets`
`flutter:
  assets:
    - assets/shaders/my_shader.frag`
### uses-material-design field

Use Material Design components in your Flutter app.

`flutter:
  uses-material-design: true`
## Packages

The following Flutter-specific packages can be added to the
                  pubspec. If you add a package, run`flutter pub get`in your
                  terminal to install the package.

`flutter pub get`
### flutter package

A package that represents the Flutter SDK itself and
                  can be added to the`dependencies`field. Use this if
                  your project relies on the Flutter SDK, not a regular
                  package from pub.dev.

`dependencies`
`dependencies:
  flutter:
    sdk: flutter`
### flutter_localizations package

A package that represents the Flutter SDK itself and
                  can be added to the`dependencies`field. Use this to
                  enable the localization of`ARB`files. Often used with
                  the`intl`package.

`dependencies`
`ARB`
`intl`
`dependencies:
  flutter_localizations:
    sdk: flutter
  intl: any`
### flutter_test package

A package that represents the Flutter SDK itself and
                  can be added to the`dependencies`field. Use this if you
                  have unit, widget, or integration tests for your Flutter
                  app.

`dependencies`
`dependencies:
  flutter_test:
    sdk: flutter`
### flutter_lints package

A package that that provides a set of recommended lints for
                  Flutter projects. This package can be added to the`dev_dependency`field in the pubspec.

`dev_dependency`
`dev_dependencies:
  flutter_lints: ^6.0.0`
### cupertino_icons

A package that provides a set of Apple's Cupertino icons
                  for use in Flutter applications. This package can be added
                  to the`dependency`field in the pubspec.

`dependency`
`dependencies:
  cupertino_icons: ^1.0.0`
## More information

For more information on packages, plugins,
                  and pubspec files, see the following:

- [Creating packages](https://dart.dev/guides/libraries/create-library-packages)on dart.dev
- [Glossary of package terms](https://dart.dev/tools/pub/glossary)on dart.dev
- [Package dependencies](https://dart.dev/tools/pub/dependencies)on dart.dev
- [Using packages](https://docs.flutter.dev/packages-and-plugins/using-packages)
- [What not to commit](https://dart.dev/guides/libraries/private-files#pubspeclock)on dart.dev

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/pubspec.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/pubspec&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/pubspec.md).
