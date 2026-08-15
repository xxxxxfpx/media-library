> 原文链接: [https://docs.flutter.dev/platform-integration/platform-channels](https://docs.flutter.dev/platform-integration/platform-channels)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This guide describes how to use custom platform-specific
                  code with Flutter.

## Overview

You can use platform-specific code in your Flutter app.
                  A few common ways to do this include:


Use Flutter's platform channel APIs to pass messages
                      between Flutter and your desired platforms. For more
                      information, see[Call platform-specific code using platform channels](#example).

Use the`Pigeon`package to generate type-safe
                      platform-specific code. For more
                      information, see[Call platform-specific code using the Pigeon package](#pigeon).

`Pigeon`
Flutter supports the following platforms and
                  platform-specific languages:

- **Android**: Kotlin, Java
- **iOS**: Swift, Objective-C
- **Windows**: C++
- **macOS**: Objective-C
- **Linux**: C

## Architectural overview of platform channels

Messages are passed between the client (UI)
                  and host (platform) using platform
                  channels as illustrated in this diagram:

![Platform channels architecture](https://docs.flutter.dev/assets/images/docs/PlatformChannels.png)

In the preceding diagram, messages and responses are passed
                  asynchronously through channels to ensure the user interface
                  remains responsive. On the client side,[MethodChannelfor Flutter](https://api.flutter.dev/flutter/services/MethodChannel-class.html)enables
                  sending messages that correspond to method calls. On the
                  platform side,[MethodChannelfor Android](https://api.flutter.dev/javadoc/io/flutter/plugin/common/MethodChannel.html)and[FlutterMethodChannelfor iOS](https://api.flutter.dev/ios-embedder/interface_flutter_method_channel.html)enable receiving method
                  calls and sending back a result. These classes allow you to
                  develop a platform plugin with very little*boilerplate*code.

`MethodChannel`
`MethodChannel`
`FlutterMethodChannel`
## Data types support

The standard platform channel APIs and the Pigeon package
                  use a standard message codec called[StandardMessageCodec](https://api.flutter.dev/flutter/services/StandardMessageCodec-class.html)that supports efficient binary serialization of simple
                  JSON-like values, such as booleans, numbers, Strings,
                  byte buffers, Lists, and Maps. The serialization and
                  deserialization of these values to and from messages happens
                  automatically when you send and receive values.

`StandardMessageCodec`
The following table shows how Dart values are received on the
                  platform side and vice versa:

- [Kotlin](#160-tab-panel)
- [Java](#161-tab-panel)
- [Swift](#162-tab-panel)
- [Obj-C](#163-tab-panel)
- [C++](#164-tab-panel)
- [C](#165-tab-panel)

| Dart | Kotlin |
| --- | --- |
| null | null |
| bool | Boolean |
| int(<=32 bits) | Int |
| int(>32 bits) | Long |
| double | Double |
| String | String |
| Uint8List | ByteArray |
| Int32List | IntArray |
| Int64List | LongArray |
| Float32List | FloatArray |
| Float64List | DoubleArray |
| List | List |
| Map | HashMap |

`null`
`null`
`bool`
`Boolean`
`int`
`Int`
`int`
`Long`
`double`
`Double`
`String`
`String`
`Uint8List`
`ByteArray`
`Int32List`
`IntArray`
`Int64List`
`LongArray`
`Float32List`
`FloatArray`
`Float64List`
`DoubleArray`
`List`
`List`
`Map`
`HashMap`
| Dart | Java |
| --- | --- |
| null | null |
| bool | java.lang.Boolean |
| int(<=32 bits) | java.lang.Integer |
| int(>32 bits) | java.lang.Long |
| double | java.lang.Double |
| String | java.lang.String |
| Uint8List | byte[] |
| Int32List | int[] |
| Int64List | long[] |
| Float32List | float[] |
| Float64List | double[] |
| List | java.util.ArrayList |
| Map | java.util.HashMap |

`null`
`null`
`bool`
`java.lang.Boolean`
`int`
`java.lang.Integer`
`int`
`java.lang.Long`
`double`
`java.lang.Double`
`String`
`java.lang.String`
`Uint8List`
`byte[]`
`Int32List`
`int[]`
`Int64List`
`long[]`
`Float32List`
`float[]`
`Float64List`
`double[]`
`List`
`java.util.ArrayList`
`Map`
`java.util.HashMap`
| Dart | Swift |
| --- | --- |
| null | nil(NSNullwhen nested) |
| bool | NSNumber(value: Bool) |
| int(<=32 bits) | NSNumber(value: Int32) |
| int(>32 bits) | NSNumber(value: Int) |
| double | NSNumber(value: Double) |
| String | String |
| Uint8List | FlutterStandardTypedData(bytes: Data) |
| Int32List | FlutterStandardTypedData(int32: Data) |
| Int64List | FlutterStandardTypedData(int64: Data) |
| Float32List | FlutterStandardTypedData(float32: Data) |
| Float64List | FlutterStandardTypedData(float64: Data) |
| List | Array |
| Map | Dictionary |

`null`
`nil`
`NSNull`
`bool`
`NSNumber(value: Bool)`
`int`
`NSNumber(value: Int32)`
`int`
`NSNumber(value: Int)`
`double`
`NSNumber(value: Double)`
`String`
`String`
`Uint8List`
`FlutterStandardTypedData(bytes: Data)`
`Int32List`
`FlutterStandardTypedData(int32: Data)`
`Int64List`
`FlutterStandardTypedData(int64: Data)`
`Float32List`
`FlutterStandardTypedData(float32: Data)`
`Float64List`
`FlutterStandardTypedData(float64: Data)`
`List`
`Array`
`Map`
`Dictionary`
| Dart | Objective-C |
| --- | --- |
| null | nil(NSNullwhen nested) |
| bool | NSNumber numberWithBool: |
| int(<=32 bits) | NSNumber numberWithInt: |
| int(>32 bits) | NSNumber numberWithLong: |
| double | NSNumber numberWithDouble: |
| String | NSString |
| Uint8List | FlutterStandardTypedData typedDataWithBytes: |
| Int32List | FlutterStandardTypedData typedDataWithInt32: |
| Int64List | FlutterStandardTypedData typedDataWithInt64: |
| Float32List | FlutterStandardTypedData typedDataWithFloat32: |
| Float64List | FlutterStandardTypedData typedDataWithFloat64: |
| List | NSArray |
| Map | NSDictionary |

`null`
`nil`
`NSNull`
`bool`
`NSNumber numberWithBool:`
`int`
`NSNumber numberWithInt:`
`int`
`NSNumber numberWithLong:`
`double`
`NSNumber numberWithDouble:`
`String`
`NSString`
`Uint8List`
`FlutterStandardTypedData typedDataWithBytes:`
`Int32List`
`FlutterStandardTypedData typedDataWithInt32:`
`Int64List`
`FlutterStandardTypedData typedDataWithInt64:`
`Float32List`
`FlutterStandardTypedData typedDataWithFloat32:`
`Float64List`
`FlutterStandardTypedData typedDataWithFloat64:`
`List`
`NSArray`
`Map`
`NSDictionary`
| Dart | C++ |
| --- | --- |
| null | EncodableValue() |
| bool | EncodableValue(bool) |
| int(<=32 bits) | EncodableValue(int32_t) |
| int(>32 bits) | EncodableValue(int64_t) |
| double | EncodableValue(double) |
| String | EncodableValue(std::string) |
| Uint8List | EncodableValue(std::vector<uint8_t>) |
| Int32List | EncodableValue(std::vector<int32_t>) |
| Int64List | EncodableValue(std::vector<int64_t>) |
| Float32List | EncodableValue(std::vector<float>) |
| Float64List | EncodableValue(std::vector<double>) |
| List | EncodableValue(std::vector<EncodableValue>) |
| Map | EncodableValue(std::map<EncodableValue, EncodableValue>) |

`null`
`EncodableValue()`
`bool`
`EncodableValue(bool)`
`int`
`EncodableValue(int32_t)`
`int`
`EncodableValue(int64_t)`
`double`
`EncodableValue(double)`
`String`
`EncodableValue(std::string)`
`Uint8List`
`EncodableValue(std::vector<uint8_t>)`
`Int32List`
`EncodableValue(std::vector<int32_t>)`
`Int64List`
`EncodableValue(std::vector<int64_t>)`
`Float32List`
`EncodableValue(std::vector<float>)`
`Float64List`
`EncodableValue(std::vector<double>)`
`List`
`EncodableValue(std::vector<EncodableValue>)`
`Map`
`EncodableValue(std::map<EncodableValue, EncodableValue>)`
| Dart | C (GObject) |
| --- | --- |
| null | FlValue() |
| bool | FlValue(bool) |
| int | FlValue(int64_t) |
| double | FlValue(double) |
| String | FlValue(gchar*) |
| Uint8List | FlValue(uint8_t*) |
| Int32List | FlValue(int32_t*) |
| Int64List | FlValue(int64_t*) |
| Float32List | FlValue(float*) |
| Float64List | FlValue(double*) |
| List | FlValue(FlValue) |
| Map | FlValue(FlValue, FlValue) |

`null`
`FlValue()`
`bool`
`FlValue(bool)`
`int`
`FlValue(int64_t)`
`double`
`FlValue(double)`
`String`
`FlValue(gchar*)`
`Uint8List`
`FlValue(uint8_t*)`
`Int32List`
`FlValue(int32_t*)`
`Int64List`
`FlValue(int64_t*)`
`Float32List`
`FlValue(float*)`
`Float64List`
`FlValue(double*)`
`List`
`FlValue(FlValue)`
`Map`
`FlValue(FlValue, FlValue)`
## Call platform-specific code using platform channels

The following code demonstrates how to call
                  a platform-specific API to retrieve and display
                  the current battery level.  It uses
                  the Android`BatteryManager`API,
                  the iOS`device.batteryLevel`API,
                  the Windows`GetSystemPowerStatus`API,
                  and the Linux`UPower`API with a single
                  platform message,`getBatteryLevel()`.

`BatteryManager`
`device.batteryLevel`
`GetSystemPowerStatus`
`UPower`
`getBatteryLevel()`
The example adds the platform-specific code inside
                  the main app itself.  If you want to reuse the
                  platform-specific code for multiple apps,
                  the project creation step is slightly different
                  (see[developing packages](https://docs.flutter.dev/packages-and-plugins/developing-packages#plugin)),
                  but the platform channel code
                  is still written in the same way.

### Step 1: Create a new app project

Start by creating a new app:

- In a terminal run:`flutter create batterylevel`

`flutter create batterylevel`
By default, our template supports writing Android code using Kotlin,
                  or iOS code using Swift. To use Java or Objective-C,
                  use the`-i`and/or`-a`flags:

`-i`
`-a`
- In a terminal run:`flutter create -i objc -a java batterylevel`

`flutter create -i objc -a java batterylevel`
### Step 2: Create the Flutter platform client

The app's`State`class holds the current app state.
                  Extend that to hold the current battery state.

`State`
First, construct the channel. Use a`MethodChannel`with a single
                  platform method that returns the battery level.

`MethodChannel`
The client and host sides of a channel are connected through
                  a channel name passed in the channel constructor.
                  All channel names used in a single app must
                  be unique; prefix the channel name with a unique 'domain
                  prefix', for example:`samples.flutter.dev/battery`.

`samples.flutter.dev/battery`
`import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';`
`class _MyHomePageState extends State<MyHomePage> {
  static const platform = MethodChannel('samples.flutter.dev/battery');
  // Get battery level.`
Next, invoke a method on the method channel,
                  specifying the concrete method to call using
                  the`String`identifier`getBatteryLevel`.
                  The call might fail—for example,
                  if the platform doesn't support the
                  platform API (such as when running in a simulator),
                  so wrap the`invokeMethod`call in a try-catch statement.

`String`
`getBatteryLevel`
`invokeMethod`
Use the returned result to update the user interface state in`_batteryLevel`inside`setState`.

`_batteryLevel`
`setState`
`// Get battery level.
String _batteryLevel = 'Unknown battery level.';
​
Future<void> _getBatteryLevel() async {
  String batteryLevel;
  try {
    final result = await platform.invokeMethod<int>('getBatteryLevel');
    batteryLevel = 'Battery level at $result % .';
  } on PlatformException catch (e) {
    batteryLevel = "Failed to get battery level: '${e.message}'.";
  }
​
  setState(() {
    _batteryLevel = batteryLevel;
  });
}`
Finally, replace the`build`method from the template to
                  contain a small user interface that displays the battery
                  state in a string, and a button for refreshing the value.

`build`
`@override
Widget build(BuildContext context) {
  return Material(
    child: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          ElevatedButton(
            onPressed: _getBatteryLevel,
            child: const Text('Get Battery Level'),
          ),
          Text(_batteryLevel),
        ],
      ),
    ),
  );
}`
### Step 3: Add an Android platform-specific implementation

- [Kotlin](#166-tab-panel)
- [Java](#167-tab-panel)

Start by opening the Android host portion of your Flutter app
                        in Android Studio:


Start Android Studio

Select the menu item**File > Open...**

Navigate to the directory holding your Flutter app,
                            and select the**android**folder inside it. Click**OK**.

Open the file`MainActivity.kt`located in the**kotlin**folder in the
                            Project view.

`MainActivity.kt`
Inside the`configureFlutterEngine()`method, create a`MethodChannel`and call`setMethodCallHandler()`. Make sure to use the same channel name as
                        was used on the Flutter client side.

`configureFlutterEngine()`
`MethodChannel`
`setMethodCallHandler()`
`import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
​
class MainActivity: FlutterActivity() {
  private val CHANNEL = "samples.flutter.dev/battery"
​
  override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
    super.configureFlutterEngine(flutterEngine)
    MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
      call, result ->
      // This method is invoked on the main thread.
      // TODO
    }
  }
}`
Add the Android Kotlin code that uses the Android battery APIs to
                        retrieve the battery level. This code is exactly the same as you
                        would write in a native Android app.

First, add the needed imports at the top of the file:

`import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build.VERSION
import android.os.Build.VERSION_CODES`
Next, add the following method in the`MainActivity`class,
                        below the`configureFlutterEngine()`method:

`MainActivity`
`configureFlutterEngine()`
`private fun getBatteryLevel(): Int {
    val batteryLevel: Int
    if (VERSION.SDK_INT >= VERSION_CODES.LOLLIPOP) {
      val batteryManager = getSystemService(Context.BATTERY_SERVICE) as BatteryManager
      batteryLevel = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
    } else {
      val intent = ContextWrapper(applicationContext).registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
      batteryLevel = intent!!.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) * 100 / intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
    }
​
    return batteryLevel
  }`
Finally, complete the`setMethodCallHandler()`method added earlier.
                        You need to handle a single platform method,`getBatteryLevel()`,
                        so test for that in the`call`argument.
                        The implementation of this platform method calls the
                        Android code written in the previous step, and returns a response for both
                        the success and error cases using the`result`argument.
                        If an unknown method is called, report that instead.

`setMethodCallHandler()`
`getBatteryLevel()`
`call`
`result`
Remove the following code:

`MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
      call, result ->
      // This method is invoked on the main thread.
      // TODO
    }`
And replace with the following:

`MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
      // This method is invoked on the main thread.
      call, result ->
      if (call.method == "getBatteryLevel") {
        val batteryLevel = getBatteryLevel()
​
        if (batteryLevel != -1) {
          result.success(batteryLevel)
        } else {
          result.error("UNAVAILABLE", "Battery level not available.", null)
        }
      } else {
        result.notImplemented()
      }
    }`
Start by opening the Android host portion of your Flutter app
                        in Android Studio:


Start Android Studio

Select the menu item**File > Open...**

Navigate to the directory holding your Flutter app,
                            and select the**android**folder inside it. Click**OK**.

Open the`MainActivity.java`file located in the**java**folder in the
                            Project view.

`MainActivity.java`
Next, create a`MethodChannel`and set a`MethodCallHandler`inside the`configureFlutterEngine()`method.
                        Make sure to use the same channel name as was used on the
                        Flutter client side.

`MethodChannel`
`MethodCallHandler`
`configureFlutterEngine()`
`import androidx.annotation.NonNull;
import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodChannel;
​
public class MainActivity extends FlutterActivity {
  private static final String CHANNEL = "samples.flutter.dev/battery";
​
  @Override
  public void configureFlutterEngine(@NonNull FlutterEngine flutterEngine) {
    super.configureFlutterEngine(flutterEngine);
    new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
        .setMethodCallHandler(
          (call, result) -> {
            // This method is invoked on the main thread.
            // TODO
          }
        );
  }
}`
Add the Android Java code that uses the Android battery APIs to
                        retrieve the battery level. This code is exactly the same as you
                        would write in a native Android app.

First, add the needed imports at the top of the file:

`import android.content.ContextWrapper;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.BatteryManager;
import android.os.Build.VERSION;
import android.os.Build.VERSION_CODES;
import android.os.Bundle;`
Then add the following as a new method in the activity class,
                        below the`configureFlutterEngine()`method:

`configureFlutterEngine()`
`private int getBatteryLevel() {
    int batteryLevel = -1;
    if (VERSION.SDK_INT >= VERSION_CODES.LOLLIPOP) {
      BatteryManager batteryManager = (BatteryManager) getSystemService(BATTERY_SERVICE);
      batteryLevel = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);
    } else {
      Intent intent = new ContextWrapper(getApplicationContext()).
          registerReceiver(null, new IntentFilter(Intent.ACTION_BATTERY_CHANGED));
      batteryLevel = (intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) * 100) /
          intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1);
    }
​
    return batteryLevel;
  }`
Finally, complete the`setMethodCallHandler()`method added earlier.
                        You need to handle a single platform method,`getBatteryLevel()`,
                        so test for that in the`call`argument. The implementation of
                        this platform method calls the Android code written
                        in the previous step, and returns a response for both
                        the success and error cases using the`result`argument.
                        If an unknown method is called, report that instead.

`setMethodCallHandler()`
`getBatteryLevel()`
`call`
`result`
Remove the following code:

`new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
        .setMethodCallHandler(
          (call, result) -> {
            // This method is invoked on the main thread.
            // TODO
          }
      );`
And replace with the following:

`new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
        .setMethodCallHandler(
          (call, result) -> {
            // This method is invoked on the main thread.
            if (call.method.equals("getBatteryLevel")) {
              int batteryLevel = getBatteryLevel();
​
              if (batteryLevel != -1) {
                result.success(batteryLevel);
              } else {
                result.error("UNAVAILABLE", "Battery level not available.", null);
              }
            } else {
              result.notImplemented();
            }
          }
      );`
You should now be able to run the app on Android. If using the Android
                  Emulator, set the battery level in the Extended Controls panel
                  accessible from the**...**button in the toolbar.

### Step 4: Add an iOS platform-specific implementation

- [Swift](#168-tab-panel)
- [Objective-C](#169-tab-panel)

Start by opening the iOS host portion of your Flutter app in Xcode:


Start Xcode.

Select the menu item**File > Open...**.

Navigate to the directory holding your Flutter app, and select the**ios**folder inside it. Click**OK**.

Add support for Swift in the standard template setup that uses Objective-C:


**Expand Runner > Runner**in the Project navigator.

Open the file`AppDelegate.swift`located under**Runner > Runner**in the Project navigator.

`AppDelegate.swift`
Override the`application:didFinishLaunchingWithOptions:`function and create
                        a`FlutterMethodChannel`tied to the channel name`samples.flutter.dev/battery`:

`application:didFinishLaunchingWithOptions:`
`FlutterMethodChannel`
`samples.flutter.dev/battery`
`@main
@objc class AppDelegate: FlutterAppDelegate, FlutterImplicitEngineDelegate {
​
  func didInitializeImplicitFlutterEngine(_ engineBridge: FlutterImplicitEngineBridge) {
    GeneratedPluginRegistrant.register(with: engineBridge.pluginRegistry)
​
    let batteryChannel = FlutterMethodChannel(
      name: "samples.flutter.dev/battery",
      binaryMessenger: engineBridge.applicationRegistrar.messenger()
    )
​
    batteryChannel.setMethodCallHandler({
      [weak self] (call: FlutterMethodCall, result: FlutterResult) -> Void in
      // This method is invoked on the UI thread.
      // Handle battery messages.
    })
  }
}`
Next, add the iOS Swift code that uses the iOS battery APIs to retrieve
                        the battery level. This code is exactly the same as you
                        would write in a native iOS app.

Add the following as a new method at the bottom of`AppDelegate.swift`:

`AppDelegate.swift`
`private func receiveBatteryLevel(result: FlutterResult) {
  let device = UIDevice.current
  device.isBatteryMonitoringEnabled = true
  if device.batteryState == UIDevice.BatteryState.unknown {
    result(FlutterError(code: "UNAVAILABLE",
                        message: "Battery level not available.",
                        details: nil))
  } else {
    result(Int(device.batteryLevel * 100))
  }
}`
Finally, complete the`setMethodCallHandler()`method added earlier.
                        You need to handle a single platform method,`getBatteryLevel()`,
                        so test for that in the`call`argument.
                        The implementation of this platform method calls
                        the iOS code written in the previous step. If an unknown method
                        is called, report that instead.

`setMethodCallHandler()`
`getBatteryLevel()`
`call`
`batteryChannel.setMethodCallHandler({
  [weak self] (call: FlutterMethodCall, result: FlutterResult) -> Void in
  // This method is invoked on the UI thread.
  guard call.method == "getBatteryLevel" else {
    result(FlutterMethodNotImplemented)
    return
  }
  self?.receiveBatteryLevel(result: result)
})`
Start by opening the iOS host portion of the Flutter app in Xcode:


Start Xcode.

Select the menu item**File > Open...**.

Navigate to the directory holding your Flutter app,
                            and select the**ios**folder inside it. Click**OK**.

Make sure the Xcode projects builds without errors.

Open the file`AppDelegate.m`, located under**Runner > Runner**in the Project navigator.

`AppDelegate.m`
Create a`FlutterMethodChannel`and add a handler inside the`application didFinishLaunchingWithOptions:`method.
                        Make sure to use the same channel name
                        as was used on the Flutter client side.

`FlutterMethodChannel`
`application didFinishLaunchingWithOptions:`
`#import <Flutter/Flutter.h>
#import "GeneratedPluginRegistrant.h"
​
@implementation AppDelegate
​
- (void)didInitializeImplicitFlutterEngine:(NSObject<FlutterImplicitEngineBridge>*)engineBridge {
  [GeneratedPluginRegistrant registerWithRegistry:engineBridge.pluginRegistry];
​
  FlutterMethodChannel* batteryChannel = [FlutterMethodChannel
                                        methodChannelWithName:@"samples.flutter.dev/battery"
                                        binaryMessenger:engineBridge.applicationRegistrar.messenger];
​
  [batteryChannel setMethodCallHandler:^(FlutterMethodCall* call, FlutterResult result) {
    // This method is invoked on the UI thread.
    // TODO
  }];
}
@end`
Next, add the iOS ObjectiveC code that uses the iOS battery APIs to
                        retrieve the battery level. This code is exactly the same as you
                        would write in a native iOS app.

Add the following method in the`AppDelegate`class, just before`@end`:

`AppDelegate`
`@end`
`- (int)getBatteryLevel {
  UIDevice* device = UIDevice.currentDevice;
  device.batteryMonitoringEnabled = YES;
  if (device.batteryState == UIDeviceBatteryStateUnknown) {
    return -1;
  } else {
    return (int)(device.batteryLevel * 100);
  }
}`
Finally, complete the`setMethodCallHandler()`method added earlier.
                        You need to handle a single platform method,`getBatteryLevel()`,
                        so test for that in the`call`argument. The implementation of
                        this platform method calls the iOS code written in the previous step,
                        and returns a response for both the success and error cases using
                        the`result`argument. If an unknown method is called, report that instead.

`setMethodCallHandler()`
`getBatteryLevel()`
`call`
`result`
`__weak typeof(self) weakSelf = self;
[batteryChannel setMethodCallHandler:^(FlutterMethodCall* call, FlutterResult result) {
  // This method is invoked on the UI thread.
  if ([@"getBatteryLevel" isEqualToString:call.method]) {
    int batteryLevel = [weakSelf getBatteryLevel];
​
    if (batteryLevel == -1) {
      result([FlutterError errorWithCode:@"UNAVAILABLE"
                                 message:@"Battery level not available."
                                 details:nil]);
    } else {
      result(@(batteryLevel));
    }
  } else {
    result(FlutterMethodNotImplemented);
  }
}];`
You should now be able to run the app on iOS.
                  If using the iOS Simulator,
                  note that it doesn't support battery APIs,
                  and the app displays 'Battery level not available'.

### Step 5: Add a Windows platform-specific implementation

Start by opening the Windows host portion of your Flutter app in Visual Studio:


Run`flutter build windows`in your project directory once to generate
                      the Visual Studio solution file.

`flutter build windows`
Start Visual Studio.

Select**Open a project or solution**.

Navigate to the directory holding your Flutter app, then into the**build**folder, then the**windows**folder, then select the`batterylevel.sln`file.
                      Click**Open**.

`batterylevel.sln`
Add the C++ implementation of the platform channel method:


Expand**batterylevel > Source Files**in the Solution Explorer.

Open the file`flutter_window.cpp`.

`flutter_window.cpp`
First, add the necessary includes to the top of the file, just
                  after`#include "flutter_window.h"`:

`#include "flutter_window.h"`
`#include <flutter/event_channel.h>
#include <flutter/event_sink.h>
#include <flutter/event_stream_handler_functions.h>
#include <flutter/method_channel.h>
#include <flutter/standard_method_codec.h>
#include <windows.h>
​
#include <memory>`
Edit the`FlutterWindow::OnCreate`method and create
                  a`flutter::MethodChannel`tied to the channel name`samples.flutter.dev/battery`:

`FlutterWindow::OnCreate`
`flutter::MethodChannel`
`samples.flutter.dev/battery`
`bool FlutterWindow::OnCreate() {
  // ...
  RegisterPlugins(flutter_controller_->engine());
​
  flutter::MethodChannel<> channel(
      flutter_controller_->engine()->messenger(), "samples.flutter.dev/battery",
      &flutter::StandardMethodCodec::GetInstance());
  channel.SetMethodCallHandler(
      [](const flutter::MethodCall<>& call,
         std::unique_ptr<flutter::MethodResult<>> result) {
        // TODO
      });
​
  SetChildContent(flutter_controller_->view()->GetNativeWindow());
  return true;
}`
Next, add the C++ code that uses the Windows battery APIs to
                  retrieve the battery level. This code is exactly the same as
                  you would write in a native Windows application.

Add the following as a new function at the top of`flutter_window.cpp`just after the`#include`section:

`flutter_window.cpp`
`#include`
`static int GetBatteryLevel() {
  SYSTEM_POWER_STATUS status;
  if (GetSystemPowerStatus(&status) == 0 || status.BatteryLifePercent == 255) {
    return -1;
  }
  return status.BatteryLifePercent;
}`
Finally, complete the`setMethodCallHandler()`method added earlier.
                  You need to handle a single platform method,`getBatteryLevel()`,
                  so test for that in the`call`argument.
                  The implementation of this platform method calls
                  the Windows code written in the previous step. If an unknown method
                  is called, report that instead.

`setMethodCallHandler()`
`getBatteryLevel()`
`call`
Remove the following code:

`channel.SetMethodCallHandler(
      [](const flutter::MethodCall<>& call,
         std::unique_ptr<flutter::MethodResult<>> result) {
        // TODO
      });`
And replace with the following:

`channel.SetMethodCallHandler(
      [](const flutter::MethodCall<>& call,
         std::unique_ptr<flutter::MethodResult<>> result) {
        if (call.method_name() == "getBatteryLevel") {
          int battery_level = GetBatteryLevel();
          if (battery_level != -1) {
            result->Success(battery_level);
          } else {
            result->Error("UNAVAILABLE", "Battery level not available.");
          }
        } else {
          result->NotImplemented();
        }
      });`
You should now be able to run the application on Windows.
                  If your device doesn't have a battery,
                  it displays 'Battery level not available'.

### Step 6: Add a macOS platform-specific implementation

Start by opening the macOS host portion of your Flutter app in Xcode:


Start Xcode.

Select the menu item**File > Open...**.

Navigate to the directory holding your Flutter app, and select the**macos**folder inside it. Click**OK**.

Add the Swift implementation of the platform channel method:


**Expand Runner > Runner**in the Project navigator.

Open the file`MainFlutterWindow.swift`located under**Runner > Runner**in the Project navigator.

`MainFlutterWindow.swift`
First, add the necessary import to the top of the file, just after`import FlutterMacOS`:

`import FlutterMacOS`
`import IOKit.ps`
Create a`FlutterMethodChannel`tied to the channel name`samples.flutter.dev/battery`in the`awakeFromNib`method:

`FlutterMethodChannel`
`samples.flutter.dev/battery`
`awakeFromNib`
`override func awakeFromNib() {
    // ...
    self.setFrame(windowFrame, display: true)
​
    let batteryChannel = FlutterMethodChannel(
      name: "samples.flutter.dev/battery",
      binaryMessenger: flutterViewController.engine.binaryMessenger)
    batteryChannel.setMethodCallHandler { (call, result) in
      // This method is invoked on the UI thread.
      // Handle battery messages.
    }
​
    RegisterGeneratedPlugins(registry: flutterViewController)
​
    super.awakeFromNib()
  }
}`
Next, add the macOS Swift code that uses the IOKit battery APIs to retrieve
                  the battery level. This code is exactly the same as you
                  would write in a native macOS app.

Add the following as a new method at the bottom of`MainFlutterWindow.swift`:

`MainFlutterWindow.swift`
`private func getBatteryLevel() -> Int? {
  let info = IOPSCopyPowerSourcesInfo().takeRetainedValue()
  let sources: Array<CFTypeRef> = IOPSCopyPowerSourcesList(info).takeRetainedValue() as Array
  if let source = sources.first {
    let description =
      IOPSGetPowerSourceDescription(info, source).takeUnretainedValue() as! [String: AnyObject]
    if let level = description[kIOPSCurrentCapacityKey] as? Int {
      return level
    }
  }
  return nil
}`
Finally, complete the`setMethodCallHandler`method added earlier.
                  You need to handle a single platform method,`getBatteryLevel()`,
                  so test for that in the`call`argument.
                  The implementation of this platform method calls
                  the macOS code written in the previous step. If an unknown method
                  is called, report that instead.

`setMethodCallHandler`
`getBatteryLevel()`
`call`
`batteryChannel.setMethodCallHandler { (call, result) in
  switch call.method {
  case "getBatteryLevel":
    guard let level = getBatteryLevel() else {
      result(
        FlutterError(
          code: "UNAVAILABLE",
          message: "Battery level not available",
          details: nil))
     return
    }
    result(level)
  default:
    result(FlutterMethodNotImplemented)
  }
}`
You should now be able to run the application on macOS.
                  If your device doesn't have a battery,
                  it displays 'Battery level not available'.

### Step 7: Add a Linux platform-specific implementation

For this example you need to install the`upower`developer headers.
                  This is likely available from your distribution, for example with:

`upower`
`sudo apt install libupower-glib-dev`
Start by opening the Linux host portion of your Flutter app in the editor
                  of your choice. The instructions below are for Visual Studio Code with the
                  "C/C++" and "CMake" extensions installed, but can be adjusted for other IDEs.


Launch Visual Studio Code.

Open the**linux**directory inside your project.

Choose**Yes**in the prompt asking:`Would you like to configure project "linux"?`.
                      This enables C++ autocomplete.

`Would you like to configure project "linux"?`
Open the file`runner/my_application.cc`.

`runner/my_application.cc`
First, add the necessary includes to the top of the file, just
                  after`#include <flutter_linux/flutter_linux.h>`:

`#include <flutter_linux/flutter_linux.h>`
`#include <math.h>
#include <upower.h>`
Add an`FlMethodChannel`to the`_MyApplication`struct:

`FlMethodChannel`
`_MyApplication`
`struct _MyApplication {
  GtkApplication parent_instance;
  char** dart_entrypoint_arguments;
  FlMethodChannel* battery_channel;
};`
Make sure to clean it up in`my_application_dispose`:

`my_application_dispose`
`static void my_application_dispose(GObject* object) {
  MyApplication* self = MY_APPLICATION(object);
  g_clear_pointer(&self->dart_entrypoint_arguments, g_strfreev);
  g_clear_object(&self->battery_channel);
  G_OBJECT_CLASS(my_application_parent_class)->dispose(object);
}`
Edit the`my_application_activate`method and initialize`battery_channel`using the channel name`samples.flutter.dev/battery`, just after the call to`fl_register_plugins`:

`my_application_activate`
`battery_channel`
`samples.flutter.dev/battery`
`fl_register_plugins`
`static void my_application_activate(GApplication* application) {
  // ...
  fl_register_plugins(FL_PLUGIN_REGISTRY(self->view));
​
  g_autoptr(FlStandardMethodCodec) codec = fl_standard_method_codec_new();
  self->battery_channel = fl_method_channel_new(
      fl_engine_get_binary_messenger(fl_view_get_engine(view)),
      "samples.flutter.dev/battery", FL_METHOD_CODEC(codec));
  fl_method_channel_set_method_call_handler(
      self->battery_channel, battery_method_call_handler, self, nullptr);
​
  gtk_widget_grab_focus(GTK_WIDGET(self->view));
}`
Next, add the C code that uses the Linux battery APIs to
                  retrieve the battery level. This code is exactly the same as
                  you would write in a native Linux application.

Add the following as a new function at the top of`my_application.cc`just after the`G_DEFINE_TYPE`line:

`my_application.cc`
`G_DEFINE_TYPE`
`static FlMethodResponse* get_battery_level() {
  // Find the first available battery and report that.
  g_autoptr(UpClient) up_client = up_client_new();
  g_autoptr(GPtrArray) devices = up_client_get_devices2(up_client);
  if (devices->len == 0) {
    return FL_METHOD_RESPONSE(fl_method_error_response_new(
        "UNAVAILABLE", "Device does not have a battery.", nullptr));
  }
​
  UpDevice* device = UP_DEVICE(g_ptr_array_index(devices, 0));
  double percentage = 0;
  g_object_get(device, "percentage", &percentage, nullptr);
​
  g_autoptr(FlValue) result =
      fl_value_new_int(static_cast<int64_t>(round(percentage)));
  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}`
Finally, add the`battery_method_call_handler`function referenced
                  in the earlier call to`fl_method_channel_set_method_call_handler`.
                  You need to handle a single platform method,`getBatteryLevel`,
                  so test for that in the`method_call`argument.
                  The implementation of this function calls
                  the Linux code written in the previous step. If an unknown method
                  is called, report that instead.

`battery_method_call_handler`
`fl_method_channel_set_method_call_handler`
`getBatteryLevel`
`method_call`
Add the following code after the`get_battery_level`function:

`get_battery_level`
`static void battery_method_call_handler(FlMethodChannel* channel,
                                        FlMethodCall* method_call,
                                        gpointer user_data) {
  g_autoptr(FlMethodResponse) response = nullptr;
  if (strcmp(fl_method_call_get_name(method_call), "getBatteryLevel") == 0) {
    response = get_battery_level();
  } else {
    response = FL_METHOD_RESPONSE(fl_method_not_implemented_response_new());
  }
​
  g_autoptr(GError) error = nullptr;
  if (!fl_method_call_respond(method_call, response, &error)) {
    g_warning("Failed to send response: %s", error->message);
  }
}`
You should now be able to run the application on Linux.
                  If your device doesn't have a battery,
                  it displays 'Battery level not available'.

## Call platform-specific code using the Pigeon package

You can use the[Pigeon](https://pub.dev/packages/pigeon)package as
                  an alternative to Flutter's platform channel APIs
                  to generate code that sends messages in a
                  structured, type-safe manner. The workflow for Pigeon
                  looks like this:

`Pigeon`

The Flutter app sends structured
                      type-safe messages to its*host*, the non-Dart portion
                      of the app, over a platform channel.

The*host*listens on the platform channel, and receives
                      the message. It then calls into any number of
                      platform-specific APIs using the native programming
                      language and sends a response back to the*client*,
                      the Flutter portion of the app.

Using this package eliminates the need to match
                  strings between host and client for the names and
                  data types of messages. It supports nested classes,
                  grouping messages into APIs, generation of asynchronous
                  wrapper code, and sending messages in either direction. The
                  generated code is readable and guarantees there are no
                  conflicts between multiple clients of different versions.

With Pigeon, the messaging protocol is defined
                  in a subset of Dart that then generates messaging
                  code for Android, iOS, macOS, or Windows. For example:

`import 'package:pigeon/pigeon.dart';
​
class SearchRequest {
  final String query;
​
  SearchRequest({required this.query});
}
​
class SearchReply {
  final String result;
​
  SearchReply({required this.result});
}
​
@HostApi()
abstract class Api {
  @async
  SearchReply search(SearchRequest request);
}`
`import 'generated_pigeon.dart';
​
Future<void> onClick() async {
  SearchRequest request = SearchRequest(query: 'test');
  Api api = SomeApi();
  SearchReply reply = await api.search(request);
  print('reply: ${reply.result}');
}`
You can find a complete example and more information
                  on the[pigeon](https://pub.dev/packages/pigeon)page on pub.dev.

`pigeon`
## Channels and platform threading

When invoking channels on the platform side destined for Flutter,
                  invoke them on the platform's main thread.
                  When invoking channels in Flutter destined for the platform side,
                  either invoke them from any`Isolate`that is the root`Isolate`,*or*that is registered as a background`Isolate`.
                  The handlers for the platform side can execute on the platform's main thread
                  or they can execute on a background thread if using a Task Queue.
                  You can invoke the platform side handlers asynchronously
                  and on any thread.

`Isolate`
`Isolate`
`Isolate`
### Use plugins and channels from a background isolate

Plugins and channels can be used by any`Isolate`, but that`Isolate`has to be
                  a root`Isolate`(the one created by Flutter) or registered as a background`Isolate`for a root`Isolate`.

`Isolate`
`Isolate`
`Isolate`
`Isolate`
`Isolate`
The following example shows how to register a background`Isolate`in order to
                  use a plugin from a background`Isolate`.

`Isolate`
`Isolate`
`import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
​
void _isolateMain(RootIsolateToken rootIsolateToken) async {
  BackgroundIsolateBinaryMessenger.ensureInitialized(rootIsolateToken);
  SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
  print(sharedPreferences.getBool('isDebug'));
}
​
void main() {
  RootIsolateToken rootIsolateToken = RootIsolateToken.instance!;
  Isolate.spawn(_isolateMain, rootIsolateToken);
}`
### Execute channel handlers on a background thread (Android)

In order for a channel's platform side handler to
                  execute on a background thread on an Android app, you must
                  use the Task Queue API.

- [Kotlin](#170-tab-panel)
- [Java](#171-tab-panel)

`override fun onAttachedToEngine(@NonNull flutterPluginBinding: FlutterPlugin.FlutterPluginBinding) {
  val taskQueue =
      flutterPluginBinding.binaryMessenger.makeBackgroundTaskQueue()
  channel = MethodChannel(flutterPluginBinding.binaryMessenger,
                          "com.example.foo",
                          StandardMethodCodec.INSTANCE,
                          taskQueue)
  channel.setMethodCallHandler(this)
}`
`@Override
public void onAttachedToEngine(@NonNull FlutterPluginBinding binding) {
  BinaryMessenger messenger = binding.getBinaryMessenger();
  BinaryMessenger.TaskQueue taskQueue =
      messenger.makeBackgroundTaskQueue();
  channel =
      new MethodChannel(
          messenger,
          "com.example.foo",
          StandardMethodCodec.INSTANCE,
          taskQueue);
  channel.setMethodCallHandler(this);
}`
### Execute channel handlers on a background thread (iOS)

In order for a channel's platform side handler to
                  execute on a background thread on an iOS app, you must use
                  the Task Queue API.

- [Swift](#172-tab-panel)
- [Objective-C](#173-tab-panel)

`public static func register(with registrar: FlutterPluginRegistrar) {
  let taskQueue = registrar.messenger().makeBackgroundTaskQueue?()
  let channel = FlutterMethodChannel(name: "com.example.foo",
                                     binaryMessenger: registrar.messenger(),
                                     codec: FlutterStandardMethodCodec.sharedInstance(),
                                     taskQueue: taskQueue)
  let instance = MyPlugin()
  registrar.addMethodCallDelegate(instance, channel: channel)
}`
`+ (void)registerWithRegistrar:(NSObject<FlutterPluginRegistrar>*)registrar {
  NSObject<FlutterTaskQueue>* taskQueue =
      [[registrar messenger] makeBackgroundTaskQueue];
  FlutterMethodChannel* channel =
      [FlutterMethodChannel methodChannelWithName:@"com.example.foo"
                                  binaryMessenger:[registrar messenger]
                                            codec:[FlutterStandardMethodCodec sharedInstance]
                                        taskQueue:taskQueue];
  MyPlugin* instance = [[MyPlugin alloc] init];
  [registrar addMethodCallDelegate:instance channel:channel];
}`
### Jump to the UI thread (Android)

To comply with channels' UI thread requirement,
                  you might need to jump from a background thread
                  to Android's UI thread to execute a channel method.
                  In Android, you can accomplish this by`post()`ing a`Runnable`to Android's UI thread`Looper`,
                  which causes the`Runnable`to execute on the
                  main thread at the next opportunity.

`post()`
`Runnable`
`Looper`
`Runnable`
- [Kotlin](#174-tab-panel)
- [Java](#175-tab-panel)

`Handler(Looper.getMainLooper()).post {
  // Call the desired channel message here.
}`
`new Handler(Looper.getMainLooper()).post(new Runnable() {
  @Override
  public void run() {
    // Call the desired channel message here.
  }
});`
### Jump to the main thread (iOS)

To comply with channel's main thread requirement,
                  you might need to jump from a background thread to
                  iOS's main thread to execute a channel method.
                  You can accomplish this in iOS by executing a[block](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingwithBlocks/WorkingwithBlocks.html)on the main[dispatch queue](https://developer.apple.com/documentation/dispatch/dispatchqueue):

- [Objective-C](#176-tab-panel)
- [Swift](#177-tab-panel)

`dispatch_async(dispatch_get_main_queue(), ^{
  // Call the desired channel message here.
});`
`DispatchQueue.main.async {
  // Call the desired channel message here.
}`
## Supplementals

### Common channels and codecs

The following is a list of some common platform channel APIs
                  that you can use to write platform-specific code:


[MethodChannel](https://api.flutter.dev/flutter/services/MethodChannel-class.html)for Flutter: A named channel that you
                      can use to communicate with platform plugins using
                      asynchronous method calls. By default this channel uses
                      the[StandardMessageCodec](https://api.flutter.dev/flutter/services/StandardMessageCodec-class.html)codec.
                      This channel is not type safe, which means calling and
                      receiving messages depends on the host and client
                      declaring the same arguments and data types in order for
                      messages to work.

`MethodChannel`
`StandardMessageCodec`
[BasicMessageChannel](https://api.flutter.dev/flutter/services/BasicMessageChannel-class.html)for Flutter: A named channel
                      that supports basic, asynchronous message passing, using a
                      supported message codec. Not type safe.

`BasicMessageChannel`
[Engine Embedder APIs](https://api.dart.dev/index.html#more-documentation)for Platforms: These
                      platform-specific APIs contain platform-specific
                      channel APIs.

You can create your own codec or use an existing one. The
                  following is a list of some existing codecs that you can use
                  with platform-specific code:


[StandardMessageCodec](https://api.flutter.dev/flutter/services/StandardMessageCodec-class.html): A commonly used message codec
                      that encodes and decodes a wide range of data types into
                      a platform-agnostic binary format for transmission across
                      platform channels. The serialization and deserialization
                      of values to and from messages happens automatically when
                      you send and receive values. For a list of supported
                      data types, see[Platform channel data types support](#codec).

`StandardMessageCodec`
[BinaryCodec](https://api.flutter.dev/flutter/services/BinaryCodec-class.html): A message codec that passes raw binary
                      data between the Dart side of your Flutter app and the
                      native platform side. It does not perform any higher-level
                      encoding or decoding of data structures.

`BinaryCodec`
[StringCodec](https://api.flutter.dev/flutter/services/StringCodec-class.html): A message codec that encodes and
                      decodes strings, using UTF-8 encoding.

`StringCodec`
[JSONMessageCodec](https://api.flutter.dev/flutter/services/JSONMessageCodec-class.html): A message codec that encodes and
                      decodes JSON-formatted data, using UTF-8 encoding.

`JSONMessageCodec`
[FirestoreMessageCodec](https://github.com/firebase/flutterfire/blob/master/packages/cloud_firestore/cloud_firestore_platform_interface/lib/src/method_channel/utils/firestore_message_codec.dart): A message codec that handles
                      the exchange of messages sent across the platform channel
                      between your Flutter app and the native
                      Firebase Firestore SDKs (on Android and iOS).

`FirestoreMessageCodec`
### Separate platform-specific code from UI code

If you expect to use your platform-specific code
                  in multiple Flutter apps, you might consider
                  separating the code into a platform plugin located
                  in a directory outside your main application.
                  See[developing packages](https://docs.flutter.dev/packages-and-plugins/developing-packages)for details.

### Publish platform-specific code as a package

To share your platform-specific code with other developers
                  in the Flutter ecosystem, see[publishing packages](https://docs.flutter.dev/packages-and-plugins/developing-packages#publish).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/platform-channels.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/platform-channels&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/platform-channels.md).
