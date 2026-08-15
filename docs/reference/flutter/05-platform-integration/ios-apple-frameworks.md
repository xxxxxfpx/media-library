> 原文链接: [https://docs.flutter.dev/platform-integration/ios/apple-frameworks](https://docs.flutter.dev/platform-integration/ios/apple-frameworks)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

When you come from iOS development, you might need to find
                  Flutter plugins that offer the same abilities as Apple's system
                  libraries. This might include accessing device hardware or interacting
                  with specific frameworks like`HealthKit`.

`HealthKit`
For an overview of how the SwiftUI framework compares to Flutter,
                  see[Flutter for SwiftUI developers](https://docs.flutter.dev/flutter-for/swiftui-devs).

## Introducing Flutter plugins

Dart calls libraries that contain platform-specific code*plugins*,
                  short for "plugin package".
                  When developing an app with Flutter, you use*plugins*to interact
                  with system libraries.

In your Dart code, you use the plugin's Dart API to call the native
                  code from the system library being used. This means that you can write
                  the code to call the Dart API. The API then makes it work for all
                  platforms that the plugin supports.

To learn more about plugins, see[Using packages](https://docs.flutter.dev/packages-and-plugins/using-packages).
                  Though this page links to some popular plugins,
                  you can find thousands more, along with examples,
                  on[pub.dev](https://pub.dev/packages).
                  The following table does not endorse any particular plugin.
                  If you can't find a package that meets your needs,
                  you can create your own or
                  use platform channels directly in your project.
                  To learn more, check out[Writing platform-specific code](https://docs.flutter.dev/platform-integration/platform-channels).

## Adding a plugin to your project

To use an Apple framework within your native project,
                  import it into your Swift or Objective-C file.

To add a Flutter plugin, run`flutter pub add package_name`from the root of your project.
                  This adds the dependency to your[pubspec.yaml](https://docs.flutter.dev/tools/pubspec)file.
                  After you add the dependency, add an`import`statement for the package
                  in your Dart file.

`flutter pub add package_name`
`pubspec.yaml`
`import`
You might need to change app settings or initialization logic.
                  If that's needed, the package's "Readme" page on[pub.dev](https://pub.dev/packages)should provide details.

### Flutter Plugins and Apple Frameworks

| Use Case | Apple Framework or Class | Flutter Plugin |
| --- | --- | --- |
| Access the photo library | PhotoKitusing thePhotosandPhotosUIframeworks andUIImagePickerController | image_picker |
| Access the camera | UIImagePickerControllerusing the.camerasourceType | image_picker |
| Use advanced camera features | AVFoundation | camera |
| Offer In-app purchases | StoreKit | in_app_purchase1 |
| Process payments | PassKit | pay2 |
| Send push notifications | UserNotifications | firebase_messaging3 |
| Access GPS coordinates | CoreLocation | geolocator |
| Access sensor data4 | CoreMotion | sensors_plus |
| Make network requests | URLSession | http |
| Store key-values | @AppStorageproperty wrapper andNSUserDefaults | shared_preferences |
| Persist to a database | CoreDataor SQLite | sqflite |
| Access health data | HealthKit | health |
| Use machine learning | CoreML | google_ml_kit5 |
| Recognize text | VisionKit | google_ml_kit5 |
| Recognize speech | Speech | speech_to_text |
| Use augmented reality | ARKit | ar_flutter_plugin |
| Access weather data | WeatherKit | weather6 |
| Access and manage contacts | Contacts | contacts_service |
| Expose quick actions on the home screen | UIApplicationShortcutItem | quick_actions |
| Index items in Spotlight search | CoreSpotlight | flutter_core_spotlight |
| Configure, update and communicate with Widgets | WidgetKit | home_widget |
| Automate app actions with Siri/Shortcuts | AppIntents | intelligence |

`PhotoKit`
`Photos`
`PhotosUI`
`UIImagePickerController`
`image_picker`
`UIImagePickerController`
`.camera`
`sourceType`
`image_picker`
`AVFoundation`
`camera`
`StoreKit`
`in_app_purchase`
`PassKit`
`pay`
`UserNotifications`
`firebase_messaging`
`CoreLocation`
`geolocator`
`CoreMotion`
`sensors_plus`
`URLSession`
`http`
`@AppStorage`
`NSUserDefaults`
`shared_preferences`
`CoreData`
`sqflite`
`HealthKit`
`health`
`CoreML`
`google_ml_kit`
`VisionKit`
`google_ml_kit`
`Speech`
`speech_to_text`
`ARKit`
`ar_flutter_plugin`
`WeatherKit`
`weather`
`Contacts`
`contacts_service`
`UIApplicationShortcutItem`
`quick_actions`
`CoreSpotlight`
`flutter_core_spotlight`
`WidgetKit`
`home_widget`
`AppIntents`
`intelligence`

Supports both Google Play Store on Android and Apple App Store on iOS.[↩](#fnref-1)

Adds Google Pay payments on Android and Apple Pay payments on iOS.[↩](#fnref-2)

Uses Firebase Cloud Messaging and integrates with APNs.[↩](#fnref-3)

Includes sensors like accelerometer, gyroscope, etc.[↩](#fnref-4)

Uses Google's ML Kit and supports various features like text recognition, face detection, image labeling, landmark recognition, and barcode scanning. You can also create a custom model with Firebase. To learn more, see[Use a custom TensorFlow Lite model with Flutter](https://firebase.google.com/docs/ml/flutter/use-custom-models).[↩](#fnref-5)[↩2](#fnref-5-2)

Uses the[OpenWeatherMap API](https://openweathermap.org/api). Other packages exist that can pull from different weather APIs.[↩](#fnref-6)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/apple-frameworks.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/ios/apple-frameworks&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/ios/apple-frameworks.md).
