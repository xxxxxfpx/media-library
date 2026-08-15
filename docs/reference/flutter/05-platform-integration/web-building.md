> 原文链接: [https://docs.flutter.dev/platform-integration/web/building](https://docs.flutter.dev/platform-integration/web/building)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This page provides an overview of how to configure, run, and build a web
                  application using Flutter.

## Requirements

Before you can build a web application with Flutter,
                  make sure that you have the[Flutter SDK](https://docs.flutter.dev/install)and a web browser installed.
                  Visit[Set up web development for Flutter](https://docs.flutter.dev/platform-integration/web/setup)instructions
                  for details.

## Set up a Flutter project

To set up your project, you can create a
                  new Flutter project or add web support
                  to an existing project.

### Create a new project

To create a new app that includes web support, run the following command:

`$ flutter create my_app`
### Add web support to an existing project

If you already have a project,
                  run the`flutter create`command in your project directory:

`flutter create`
`$ flutter create . --platforms web`
This creates a`web/`directory containing the web assets used to bootstrap
                  and run your Flutter app.

`web/`
## Run your app

Check out the following sections to run your app.

### Run your app from the command line

Select[Chrome](https://www.google.com/chrome/)as your app's target device to run and debug
                  a Flutter web app:

`$ flutter run -d chrome`
You can also choose Chrome as a target device in your IDE.

If you prefer, you can use the`edge`device type on Windows,
                  or use`web-server`to
                  navigate to a local URL in the browser of your choice.

`edge`
`web-server`
### Run your app using WebAssembly

You can pass the`--wasm`flag to run your app using WebAssembly:

`--wasm`
`$ flutter run -d chrome --wasm`
Flutter web offers multiple build modes and renderers.
                  For more information, check out[Web renderers](https://docs.flutter.dev/platform-integration/web/renderers).

### Disable hot reload in VS Code

To temporarily disable hot reload support from VS Code,
                  update your[launch.jsonfile](https://code.visualstudio.com/docs/debugtest/debugging-configuration)file with
                  the flag`--no-web-experimental-hot-reload`.

`launch.json`
`--no-web-experimental-hot-reload`
`"configurations": [
    ...
    {
      "name": "Flutter for web (hot reload disabled)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "args": [
        "-d",
        "chrome",
        "--no-web-experimental-hot-reload",
      ]
    }
  ]`
### Disable hot reload from the command line

If you use`flutter run`from the command line,
                  you can temporarily disable hot reload on the web with the
                  following command:

`flutter run`
`flutter run -d chrome --no-web-experimental-hot-reload`
### Use hot reload in DartPad

Hot reload is also enabled in DartPad with a new "Reload" button.
                  The feature is only available if Flutter is detected
                  in the running application. You can begin a hot reloadable
                  session by selecting a sample app provided by DartPad.

## Build your app

See the following sections to build your app.

### Build your app from the command line

Run the following command to generate a release build:

`$ flutter build web`
### Build your app using WebAssembly

You can also pass the`--wasm`flag to build your app using WebAssembly:

`--wasm`
`$ flutter build web --wasm`
This populates a`build/web`directory
                  with built files, including an`assets`directory,
                  which need to be served together.

`build/web`
`assets`
To learn more about how to deploy these assets to the web,
                  visit[Build and release a web app](https://docs.flutter.dev/deployment/web).
                  For answers to other common questions, visit the[Web FAQ](https://docs.flutter.dev/platform-integration/web/faq).

## Debugging

Use[Flutter DevTools](https://docs.flutter.dev/tools/devtools)for the following tasks:

- [Debugging](https://docs.flutter.dev/tools/devtools/debugger)
- [Logging](https://docs.flutter.dev/tools/devtools/logging)
- [Running Flutter inspector](https://docs.flutter.dev/tools/devtools/inspector)

Use[Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools)for the following tasks:

- [Generating event timeline](https://developers.google.com/web/tools/chrome-devtools/evaluate-performance/performance-reference)
- [Analyzing performance](https://developers.google.com/web/tools/chrome-devtools/evaluate-performance)—make sure to use a
                    profile build

## Testing

Use[widget tests](https://docs.flutter.dev/testing/overview#widget-tests)or integration tests. To learn more about
                  running integration tests in a browser, check out the[Integration testing](https://docs.flutter.dev/testing/integration-tests#test-in-a-web-browser)page.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/building.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web/building&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/building.md).
