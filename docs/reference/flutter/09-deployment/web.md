> 原文链接: [https://docs.flutter.dev/deployment/web](https://docs.flutter.dev/deployment/web)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

During a typical development cycle,
                  you test an app using`flutter run -d chrome`(for example) at the command line.
                  This builds a*debug*version of your app.

`flutter run -d chrome`
This page helps you prepare a*release*version
                  of your app and covers the following topics:

- [Building the app for release](#building-the-app-for-release)
- [Deploying to the web](#deploying-to-the-web)
- [Deploying to Firebase Hosting](#deploying-to-firebase-hosting)
- [Handling images on the web](#handling-images-on-the-web)
- [Choosing a build mode and a renderer](#choosing-a-build-mode-and-a-renderer)
- [Minification](#minification)

## Building the app for release

Build the app for deployment using the`flutter build web`command.

`flutter build web`
`flutter build web`
This
                  generates the app, including the assets, and places the files into the`/build/web`directory of the project.

`/build/web`
To validate the release build of your app,
                  launch a web server (for example,`python -m http.server 8000`,
                  or by using the[dhttpd](https://pub.dev/packages/dhttpd)package),
                  and open the /build/web directory. Navigate to`localhost:8000`in your browser
                  (given the python SimpleHTTPServer example)
                  to view the release version of your app.

`python -m http.server 8000`
`localhost:8000`
## Additional build flags

You might need to deploy a profile or debug build for testing.
                  To do this, pass the`--profile`or`--debug`flag
                  to the`flutter build web`command.
                  Profile builds are specialized for performance profiling using Chrome DevTools,
                  and debug builds can be used to configure dart2js
                  to respect assertions and change the optimization level (using the`-O`flag.)

`--profile`
`--debug`
`flutter build web`
`-O`
## Choosing a build mode and a renderer

Flutter web provides two build modes (default and WebAssembly) and two renderers
                  (`canvaskit`and`skwasm`).

`canvaskit`
`skwasm`
For more information, see[Web renderers](https://docs.flutter.dev/platform-integration/web/renderers).

## Deploying to the web

When you are ready to deploy your app,
                  upload the release bundle
                  to Firebase, the cloud, or a similar service.
                  Here are a few possibilities, but there are
                  many others:

- [Firebase Hosting](https://firebase.google.com/docs/hosting/frameworks/flutter)
- [GitHub Pages](https://pages.github.com/)
- [Google Cloud Hosting](https://cloud.google.com/solutions/web-hosting)

## Deploying to Firebase Hosting

You can use the Firebase CLI to build and release your Flutter app with Firebase
                  Hosting.

### Before you begin

To get started,[install or update](https://firebase.google.com/docs/cli#install_the_firebase_cli)the Firebase CLI:

`npm install -g firebase-tools`
### Initialize Firebase

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Enable the web frameworks preview to the[Firebase framework-aware CLI](https://firebase.google.com/docs/hosting/frameworks/frameworks-overview):

`firebase experiments:enable webframeworks`
In an empty directory or an existing Flutter project, run the initialization
                      command:

`firebase init hosting`
Answer`yes`when asked if you want to use a web framework.

`yes`
If you're in an empty directory,
                       you'll be asked to choose your web framework. Choose`Flutter Web`.

`Flutter Web`
Choose your hosting source directory; this could be an existing flutter app.

Select a region to host your files.

Choose whether to set up automatic builds and deploys with GitHub.

Deploy the app to Firebase Hosting:

`firebase deploy`
Running this command automatically runs`flutter build web --release`,
                       so you don't have to build your app in a separate step.

`flutter build web --release`
To learn more, visit the official[Firebase Hosting](https://firebase.google.com/docs/hosting/frameworks/flutter)documentation for
                  Flutter on the web.

## Handling images on the web

The web supports the standard`Image`widget to display images.
                  By design, web browsers run untrusted code without harming the host computer.
                  This limits what you can do with images compared to mobile and desktop platforms.

`Image`
For more information, see[Displaying images on the web](https://docs.flutter.dev/platform-integration/web/web-images).

## Minification

To improve app start-up the compiler reduces the size of the compiled code by
                  removing unused code (known as*tree shaking*), and by renaming code symbols to
                  shorter strings (e.g. by renaming`AlignmentGeometryTween`to something like`ab`). Which of these two optimizations are applied depends on the build mode:

`AlignmentGeometryTween`
`ab`
| Type of web app build | Code minified? | Tree shaking performed? |
| --- | --- | --- |
| debug | No | No |
| profile | No | Yes |
| release | Yes | Yes |

## Embedding a Flutter app into an HTML page

See[Embedding Flutter web](https://docs.flutter.dev/platform-integration/web/embedding-flutter-web).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/web.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/deployment/web&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/web.md).
