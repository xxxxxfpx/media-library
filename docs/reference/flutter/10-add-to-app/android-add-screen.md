> 原文链接: [https://docs.flutter.dev/add-to-app/android/add-flutter-screen](https://docs.flutter.dev/add-to-app/android/add-flutter-screen)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This guide describes how to add a single Flutter screen to an
                  existing Android app. A Flutter screen can be added as a normal,
                  opaque screen, or as a see-through, translucent screen.
                  Both options are described in this guide.

## Add a normal Flutter screen

### Step 1: Add FlutterActivity to AndroidManifest.xml

Flutter provides[FlutterActivity](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterActivity.html)to display a Flutter
                  experience within an Android app. Like any other[Activity](https://developer.android.com/reference/android/app/Activity),`FlutterActivity`must be registered in your`AndroidManifest.xml`. Add the following XML to your`AndroidManifest.xml`file under your`application`tag:

`FlutterActivity`
`Activity`
`FlutterActivity`
`AndroidManifest.xml`
`AndroidManifest.xml`
`application`
`<activity
  android:name="io.flutter.embedding.android.FlutterActivity"
  android:theme="@style/LaunchTheme"
  android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
  android:hardwareAccelerated="true"
  android:windowSoftInputMode="adjustResize"
  />`
The reference to`@style/LaunchTheme`can be replaced
                  by any Android theme that want to apply to your`FlutterActivity`.
                  The choice of theme dictates the colors applied to
                  Android's system chrome, like Android's navigation bar, and to
                  the background color of the`FlutterActivity`just before
                  the Flutter UI renders itself for the first time.

`@style/LaunchTheme`
`FlutterActivity`
`FlutterActivity`
### Step 2: Launch FlutterActivity

With`FlutterActivity`registered in your manifest file,
                  add code to launch`FlutterActivity`from whatever point
                  in your app that you'd like. The following example shows`FlutterActivity`being launched from an`OnClickListener`.

`FlutterActivity`
`FlutterActivity`
`FlutterActivity`
`OnClickListener`
- [Jetpack Compose](#95-tab-panel)
- [Kotlin](#96-tab-panel)
- [Java](#97-tab-panel)

`MyButton(onClick = {
    startActivity(
        FlutterActivity.createDefaultIntent(this)
    )
})
​
@Composable
fun MyButton(onClick: () -> Unit) {
    Button(onClick = onClick) {
        Text("Launch Flutter!")
    }
}`
`myButton.setOnClickListener {
  startActivity(
    FlutterActivity.createDefaultIntent(this)
  )
}`
`myButton.setOnClickListener(new OnClickListener() {
  @Override
  public void onClick(View v) {
    startActivity(
      FlutterActivity.createDefaultIntent(currentActivity)
    );
  }
});`
The previous example assumes that your Dart entrypoint
                  is called`main()`, and your initial Flutter route is '/'.
                  The Dart entrypoint can't be changed using`Intent`,
                  but the initial route can be changed using`Intent`.
                  The following example demonstrates how to launch a`FlutterActivity`that initially renders a custom
                  route in Flutter.

`main()`
`Intent`
`Intent`
`FlutterActivity`
- [Jetpack Compose](#98-tab-panel)
- [Kotlin](#99-tab-panel)
- [Java](#100-tab-panel)

`MyButton(onClick = {
  startActivity(
    FlutterActivity
      .withNewEngine()
      .initialRoute("/my_route")
      .build(this)
  )
})
​
@Composable
fun MyButton(onClick: () -> Unit) {
    Button(onClick = onClick) {
        Text("Launch Flutter!")
    }
}`
`myButton.setOnClickListener {
  startActivity(
    FlutterActivity
      .withNewEngine()
      .initialRoute("/my_route")
      .build(this)
  )
}`
`myButton.addOnClickListener(new OnClickListener() {
  @Override
  public void onClick(View v) {
    startActivity(
      FlutterActivity
        .withNewEngine()
        .initialRoute("/my_route")
        .build(currentActivity)
      );
  }
});`
Replace`"/my_route"`with your desired initial route.

`"/my_route"`
The use of the`withNewEngine()`factory method
                  configures a`FlutterActivity`that internally create
                  its own[FlutterEngine](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/FlutterEngine.html)instance. This comes with a
                  non-trivial initialization time. The alternative approach
                  is to instruct`FlutterActivity`to use a pre-warmed,
                  cached`FlutterEngine`, which minimizes Flutter's
                  initialization time. That approach is discussed next.

`withNewEngine()`
`FlutterActivity`
`FlutterEngine`
`FlutterActivity`
`FlutterEngine`
### Step 3: (Optional) Use a cached FlutterEngine

Every`FlutterActivity`creates its own`FlutterEngine`by default. Each`FlutterEngine`has a non-trivial
                  warm-up time. This means that launching a standard`FlutterActivity`comes with a brief delay before your Flutter
                  experience becomes visible. To minimize this delay,
                  you can warm up a`FlutterEngine`before arriving at
                  your`FlutterActivity`, and then you can use
                  your pre-warmed`FlutterEngine`instead.

`FlutterActivity`
`FlutterEngine`
`FlutterEngine`
`FlutterActivity`
`FlutterEngine`
`FlutterActivity`
`FlutterEngine`
To pre-warm a`FlutterEngine`, find a reasonable
                  location in your app to instantiate a`FlutterEngine`.
                  The following example arbitrarily pre-warms a`FlutterEngine`in the`Application`class:

`FlutterEngine`
`FlutterEngine`
`FlutterEngine`
`Application`
- [Kotlin](#101-tab-panel)
- [Java](#102-tab-panel)

`class MyApplication : Application() {
  lateinit var flutterEngine : FlutterEngine
​
  override fun onCreate() {
    super.onCreate()
​
    // Instantiate a FlutterEngine.
    flutterEngine = FlutterEngine(this)
​
    // Start executing Dart code to pre-warm the FlutterEngine.
    flutterEngine.dartExecutor.executeDartEntrypoint(
      DartExecutor.DartEntrypoint.createDefault()
    )
​
    // Cache the FlutterEngine to be used by FlutterActivity.
    FlutterEngineCache
      .getInstance()
      .put("my_engine_id", flutterEngine)
  }
}`
`public class MyApplication extends Application {
  public FlutterEngine flutterEngine;
​
  @Override
  public void onCreate() {
    super.onCreate();
    // Instantiate a FlutterEngine.
    flutterEngine = new FlutterEngine(this);
​
    // Start executing Dart code to pre-warm the FlutterEngine.
    flutterEngine.getDartExecutor().executeDartEntrypoint(
      DartEntrypoint.createDefault()
    );
​
    // Cache the FlutterEngine to be used by FlutterActivity.
    FlutterEngineCache
      .getInstance()
      .put("my_engine_id", flutterEngine);
  }
}`
The ID passed to the[FlutterEngineCache](https://api.flutter.dev/javadoc/io/flutter/embedding/engine/FlutterEngineCache.html)can be whatever you want.
                  Make sure that you pass the same ID to any`FlutterActivity`or[FlutterFragment](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterFragment.html)that should use the cached`FlutterEngine`.
                  Using`FlutterActivity`with a cached`FlutterEngine`is discussed next.

`FlutterEngineCache`
`FlutterActivity`
`FlutterFragment`
`FlutterEngine`
`FlutterActivity`
`FlutterEngine`
With a pre-warmed, cached`FlutterEngine`, you now need
                  to instruct your`FlutterActivity`to use the cached`FlutterEngine`instead of creating a new one.
                  To accomplish this, use`FlutterActivity`'s`withCachedEngine()`builder:

`FlutterEngine`
`FlutterActivity`
`FlutterEngine`
`FlutterActivity`
`withCachedEngine()`
- [Kotlin](#103-tab-panel)
- [Java](#104-tab-panel)

`myButton.setOnClickListener {
  startActivity(
    FlutterActivity
      .withCachedEngine("my_engine_id")
      .build(this)
  )
}`
`myButton.addOnClickListener(new OnClickListener() {
  @Override
  public void onClick(View v) {
    startActivity(
      FlutterActivity
        .withCachedEngine("my_engine_id")
        .build(currentActivity)
      );
  }
});`
When using the`withCachedEngine()`factory method,
                  pass the same ID that you used when caching the desired`FlutterEngine`.

`withCachedEngine()`
`FlutterEngine`
Now, when you launch`FlutterActivity`,
                  there is significantly less delay in
                  the display of Flutter content.

`FlutterActivity`
#### Initial route with a cached engine

The concept of an initial route is available when configuring a`FlutterActivity`or a`FlutterFragment`with a new`FlutterEngine`.
                  However,`FlutterActivity`and`FlutterFragment`don't offer the
                  concept of an initial route when using a cached engine.
                  This is because a cached engine is expected to already be
                  running Dart code, which means it's too late to configure the
                  initial route.

`FlutterActivity`
`FlutterFragment`
`FlutterEngine`
`FlutterActivity`
`FlutterFragment`
Developers that would like their cached engine to begin
                  with a custom initial route can configure their cached`FlutterEngine`to use a custom initial route just before
                  executing the Dart entrypoint. The following example
                  demonstrates the use of an initial route with a cached engine:

`FlutterEngine`
- [Kotlin](#105-tab-panel)
- [Java](#106-tab-panel)

`class MyApplication : Application() {
  lateinit var flutterEngine : FlutterEngine
  override fun onCreate() {
    super.onCreate()
    // Instantiate a FlutterEngine.
    flutterEngine = FlutterEngine(this)
    // Configure an initial route.
    flutterEngine.navigationChannel.setInitialRoute("your/route/here");
    // Start executing Dart code to pre-warm the FlutterEngine.
    flutterEngine.dartExecutor.executeDartEntrypoint(
      DartExecutor.DartEntrypoint.createDefault()
    )
    // Cache the FlutterEngine to be used by FlutterActivity or FlutterFragment.
    FlutterEngineCache
      .getInstance()
      .put("my_engine_id", flutterEngine)
  }
}`
`public class MyApplication extends Application {
  @Override
  public void onCreate() {
    super.onCreate();
    // Instantiate a FlutterEngine.
    flutterEngine = new FlutterEngine(this);
    // Configure an initial route.
    flutterEngine.getNavigationChannel().setInitialRoute("your/route/here");
    // Start executing Dart code to pre-warm the FlutterEngine.
    flutterEngine.getDartExecutor().executeDartEntrypoint(
      DartEntrypoint.createDefault()
    );
    // Cache the FlutterEngine to be used by FlutterActivity or FlutterFragment.
    FlutterEngineCache
      .getInstance()
      .put("my_engine_id", flutterEngine);
  }
}`
By setting the initial route of the navigation channel, the associated`FlutterEngine`displays the desired route upon initial execution of the`runApp()`Dart function.

`FlutterEngine`
`runApp()`
Changing the initial route property of the navigation channel
                  after the initial execution of`runApp()`has no effect.
                  Developers who would like to use the same`FlutterEngine`between different`Activity`s and`Fragment`s and switch
                  the route between those displays need to set up a method channel and
                  explicitly instruct their Dart code to change`Navigator`routes.

`runApp()`
`FlutterEngine`
`Activity`
`Fragment`
`Navigator`
## Add a translucent Flutter screen

Most full-screen Flutter experiences are opaque.
                  However, some apps would like to deploy a Flutter
                  screen that looks like a modal, for example,
                  a dialog or bottom sheet. Flutter supports translucent`FlutterActivity`s out of the box.

`FlutterActivity`
To make your`FlutterActivity`translucent,
                  make the following changes to the regular process of
                  creating and launching a`FlutterActivity`.

`FlutterActivity`
`FlutterActivity`
### Step 1: Use a theme with translucency

Android requires a special theme property for`Activity`s that render
                  with a translucent background. Create or update an Android theme with the
                  following property:

`Activity`
`<style name="MyTheme" parent="@style/MyParentTheme">
  <item name="android:windowIsTranslucent">true</item>
</style>`
Then, apply the translucent theme to your`FlutterActivity`.

`FlutterActivity`
`<activity
  android:name="io.flutter.embedding.android.FlutterActivity"
  android:theme="@style/MyTheme"
  android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
  android:hardwareAccelerated="true"
  android:windowSoftInputMode="adjustResize"
  />`
Your`FlutterActivity`now supports translucency.
                  Next, you need to launch your`FlutterActivity`with explicit transparency support.

`FlutterActivity`
`FlutterActivity`
### Step 2: Start FlutterActivity with transparency

To launch your`FlutterActivity`with a transparent background,
                  pass the appropriate`BackgroundMode`to the`IntentBuilder`:

`FlutterActivity`
`BackgroundMode`
`IntentBuilder`
- [Kotlin](#107-tab-panel)
- [Java](#108-tab-panel)

`// Using a new FlutterEngine.
startActivity(
  FlutterActivity
    .withNewEngine()
    .backgroundMode(FlutterActivityLaunchConfigs.BackgroundMode.transparent)
    .build(this)
);
​
// Using a cached FlutterEngine.
startActivity(
  FlutterActivity
    .withCachedEngine("my_engine_id")
    .backgroundMode(FlutterActivityLaunchConfigs.BackgroundMode.transparent)
    .build(this)
);`
`// Using a new FlutterEngine.
startActivity(
  FlutterActivity
    .withNewEngine()
    .backgroundMode(FlutterActivityLaunchConfigs.BackgroundMode.transparent)
    .build(context)
);
​
// Using a cached FlutterEngine.
startActivity(
  FlutterActivity
    .withCachedEngine("my_engine_id")
    .backgroundMode(FlutterActivityLaunchConfigs.BackgroundMode.transparent)
    .build(context)
);`
You now have a`FlutterActivity`with a transparent background.

`FlutterActivity`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/add-flutter-screen.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/add-to-app/android/add-flutter-screen&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/android/add-flutter-screen.md).
