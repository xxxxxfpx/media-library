> 原文链接: [https://docs.flutter.dev/platform-integration/web/initialization](https://docs.flutter.dev/platform-integration/web/initialization)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This page details the initialization process for Flutter web apps and
                  how it can be customized.

## Bootstrapping

The`flutter build web`command produces
                  a script called`flutter_bootstrap.js`in
                  the build output directory (`build/web`).
                  This file contains the JavaScript code needed to initialize and
                  run your Flutter app.
                  You can use this script by placing an async-script tag for it in
                  your`index.html`file in the`web`subdirectory of your Flutter app:

`flutter build web`
`flutter_bootstrap.js`
`build/web`
`index.html`
`web`
`<html>
  <body>
    <script src="flutter_bootstrap.js" async></script>
  </body>
</html>`
Alternatively, you can inline the entire contents of
                  the`flutter_bootstrap.js`file by inserting the
                  template token`{{flutter_bootstrap_js}}`in
                  your`index.html`file:

`flutter_bootstrap.js`
`{{flutter_bootstrap_js}}`
`index.html`
`<html>
  <body>
    <script>
      {{flutter_bootstrap_js}}
    </script>
  </body>
</html>`
The`{{flutter_bootstrap_js}}`token is
                  replaced with the contents of the`flutter_bootstrap.js`file when
                  the`index.html`file is copied to the
                  output directory (`build/web`) during the build step.

`{{flutter_bootstrap_js}}`
`flutter_bootstrap.js`
`index.html`
`build/web`
## Customize initialization

By default,`flutter build web`generates a`flutter_bootstrap.js`file that
                  does a simple initialization of your Flutter app.
                  However, in some scenarios, you might have a reason to
                  customize this initialization process, such as:

`flutter build web`
`flutter_bootstrap.js`
- Setting a custom Flutter configuration for your app.
- Changing the settings for the Flutter service worker.
- Writing custom JavaScript code to
                    run at different stages of the startup process.

To write your own custom bootstrapping logic instead of
                  using the default script produced by the build step, you can
                  place a`flutter_bootstrap.js`file in the`web`subdirectory of your project,
                  which is copied over and used instead of
                  the default script produced by the build.
                  This file is also templated, and you can insert several special tokens that
                  the build step substitutes at build time when copying
                  the`flutter_bootstrap.js`file to the output directory.
                  The following table lists the tokens that the build step will
                  substitute in either the`flutter_bootstrap.js`or`index.html`files:

`flutter_bootstrap.js`
`web`
`flutter_bootstrap.js`
`flutter_bootstrap.js`
`index.html`
| Token | Replaced with |
| --- | --- |
| {{flutter_js}} | The JavaScript code that makes theFlutterLoaderobject available in the_flutter.loaderglobal variable. (See the_flutter.loader.load() APIsection below for more details.) |
| {{flutter_build_config}} | A JavaScript statement that sets metadata produced by the build process which gives theFlutterLoaderinformation needed to properly bootstrap your application. |
| {{flutter_service_worker_version}} | A unique number representing the build version of the service worker, which can be passed as part of the service worker configuration (see the "Common warning" info below). |
| {{flutter_bootstrap_js}} | As mentioned above, this inlines the contents of theflutter_bootstrap.jsfile directly into theindex.htmlfile. Note that this token can only be used in theindex.htmland not theflutter_bootstrap.jsfile itself. |

`{{flutter_js}}`
`FlutterLoader`
`_flutter.loader`
`_flutter.loader.load() API`
`{{flutter_build_config}}`
`FlutterLoader`
`{{flutter_service_worker_version}}`
`{{flutter_bootstrap_js}}`
`flutter_bootstrap.js`
`index.html`
`index.html`
`flutter_bootstrap.js`
## Write a custom bootstrap script

Any custom`flutter_bootstrap.js`script needs to have three components in
                  order to successfully start your Flutter app:

`flutter_bootstrap.js`
- A`{{flutter_js}}`token,
                    to make`_flutter.loader`available.
- A`{{flutter_build_config}}`token,
                    which provides information about the build to the`FlutterLoader`needed to start your app.
- A call to`_flutter.loader.load()`, which actually starts the app.

`{{flutter_js}}`
`_flutter.loader`
`{{flutter_build_config}}`
`FlutterLoader`
`_flutter.loader.load()`
The most basic`flutter_bootstrap.js`file would look something like this:

`flutter_bootstrap.js`
`{{flutter_js}}
{{flutter_build_config}}
​
_flutter.loader.load();`
## Customize the Flutter loader

The`_flutter.loader.load()`JavaScript API can be invoked with optional
                  arguments to customize initialization behavior:

`_flutter.loader.load()`
| Name | Description | JS type |
| --- | --- | --- |
| config | The Flutter configuration of your app. | Object |
| onEntrypointLoaded | The function called when the engine is ready to be initialized. Receives anengineInitializerobject as its only parameter. | Function |

`config`
`Object`
`onEntrypointLoaded`
`engineInitializer`
`Function`
The`config`argument is an object that can have the following optional fields:

`config`
| Name | Description | Dart type |
| --- | --- | --- |
| assetBase | The base URL of theassetsdirectory of the app. Add this when Flutter loads from a different domain or subdirectory than the actual web app. You might need this when you embed Flutter web into another app, or when you deploy its assets to a CDN. | String |
| canvasKitBaseUrl | The base URL from wherecanvaskit.wasmis downloaded. | String |
| canvasKitVariant | The CanvasKit variant to download. Your options cover:1.auto: Downloads the optimal variant for the browser. The option defaults to this value.2.full: Downloads the full variant of CanvasKit that works in all browsers.3.chromium: Downloads a smaller variant of CanvasKit that uses Chromium compatible APIs.Warning: Don't use thechromiumoption unless you plan on only using Chromium-based browsers. | String |
| canvasKitForceCpuOnly | Whentrue, forces CPU-only rendering in CanvasKit (the engine won't use WebGL). | bool |
| canvasKitMaximumSurfaces | The maximum number of overlay surfaces that the CanvasKit renderer can use. | double |
| debugShowSemanticNodes | Iftrue, Flutter visibly renders the semantics tree onscreen (for debugging). | bool |
| entrypointBaseUrl | The base URL of your Flutter app's entrypoint. Defaults to "/". | String |
| hostElement | HTML Element into which Flutter renders the app. When not set, Flutter web takes over the whole page. | HtmlElement |
| renderer | Specifies theweb rendererfor the current Flutter application, either"canvaskit"or"skwasm". | String |
| forceSingleThreadedSkwasm | Forces the Skia WASM renderer to run in single-threaded mode for compatibility. | bool |

`assetBase`
`assets`
`String`
`canvasKitBaseUrl`
`canvaskit.wasm`
`String`
`canvasKitVariant`
`auto`
`full`
`chromium`
`chromium`
`String`
`canvasKitForceCpuOnly`
`true`
`bool`
`canvasKitMaximumSurfaces`
`double`
`debugShowSemanticNodes`
`true`
`bool`
`entrypointBaseUrl`
`String`
`hostElement`
`HtmlElement`
`renderer`
`"canvaskit"`
`"skwasm"`
`String`
`forceSingleThreadedSkwasm`
`bool`
## forceSingleThreadedSkwasm

A boolean flag to force the Skia WebAssembly (skwasm) renderer
                  to run in**single-threaded mode**. This is useful if:

- Your environment doesn't support multi-threaded WASM. For example,`SharedArrayBuffer`is not available or required security
                    headers are missing.
- You want maximum browser compatibility.
- Use`false`(default) to allow multi-threaded rendering when
                    supported, which improves performance.

`SharedArrayBuffer`
`false`
## Example usage

`_flutter.loader.load({
  config: {
    renderer: 'skwasm',
    forceSingleThreadedSkwasm: true,
  },
});`
## Example: Customizing Flutter configuration based on URL query parameters

The following example shows a custom`flutter_bootstrap.js`that allows
                  the user to select a renderer by providing a`renderer`query parameter,
                  such as`?renderer=skwasm`, in the URL of their website:

`flutter_bootstrap.js`
`renderer`
`?renderer=skwasm`
`{{flutter_js}}
{{flutter_build_config}}
​
const searchParams = new URLSearchParams(window.location.search);
const renderer = searchParams.get('renderer');
const userConfig = renderer ? {'renderer': renderer} : {};
_flutter.loader.load({
  config: userConfig,
});`
This script evaluates the`URLSearchParams`of the page to determine whether
                  the user passed a`renderer`query parameter and then
                  changes the user configuration of the Flutter app.

`URLSearchParams`
`renderer`
## The onEntrypointLoaded callback

You can also pass an`onEntrypointLoaded`callback into the`load`API in order
                  to perform custom logic at different parts of the initialization process.
                  The initialization process is split into the following stages:

`onEntrypointLoaded`
`load`
The`load`function calls the`onEntrypointLoaded`callback once the
                      Service Worker is initialized, and the`main.dart.js`entrypoint has
                      been downloaded and run by the browser.
                      Flutter also calls`onEntrypointLoaded`on
                      every hot restart during development.

`load`
`onEntrypointLoaded`
`main.dart.js`
`onEntrypointLoaded`
The`onEntrypointLoaded`callback receives an**engine initializer**object as its only parameter.
                      Use the engine initializer`initializeEngine()`function to
                      set the run-time configuration, like`multiViewEnabled: true`,
                      and start the Flutter web engine.

`onEntrypointLoaded`
`initializeEngine()`
`multiViewEnabled: true`
The`initializeEngine()`function returns a[Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)that resolves with an**app runner**object. The app runner has a
                      single method,`runApp()`, that runs the Flutter app.

`initializeEngine()`
`Promise`
`runApp()`
The`runApp()`method returns a**flutter app**object.
                      In multi-view mode, the`addView`and`removeView`methods can be used to manage app views from the host app.
                      To learn more, check out[Embedded mode](https://docs.flutter.dev/platform-integration/web/embedding-flutter-web/#embedded-mode).

`runApp()`
`addView`
`removeView`
## Example: Display a progress indicator

To give the user of your application feedback
                  during the initialization process,
                  use the hooks provided for each stage to update the DOM:

`{{flutter_js}}
{{flutter_build_config}}
​
const loading = document.createElement('div');
document.body.appendChild(loading);
loading.textContent = "Loading Entrypoint...";
_flutter.loader.load({
  onEntrypointLoaded: async function(engineInitializer) {
    loading.textContent = "Initializing engine...";
    const appRunner = await engineInitializer.initializeEngine();
​
    loading.textContent = "Running app...";
    await appRunner.runApp();
  }
});`
## Common warning

If you experience a warning similar to the following:

`Warning: In index.html:37: Local variable for "serviceWorkerVersion" is deprecated.
Use "" template token instead.`
You can fix this by deleting the following line from the`web/index.html`file:

`web/index.html`
`var serviceWorkerVersion = null;`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/initialization.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web/initialization&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/initialization.md).
