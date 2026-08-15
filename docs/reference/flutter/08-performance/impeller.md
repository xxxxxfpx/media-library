> 原文链接: [https://docs.flutter.dev/perf/impeller](https://docs.flutter.dev/perf/impeller)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## What is Impeller?

Impeller provides a new rendering runtime for Flutter.
                  Impeller precompiles a[smaller, simpler set of shaders](https://github.com/flutter/flutter/issues/77412)at engine-build time so they don't compile at runtime.

For a video introduction to Impeller, check out the following
                  talk from Google I/O 2023.

Impeller has the following objectives:

- **Predictable performance**:
                    Impeller compiles all shaders and reflection offline at build time.
                    It builds all pipeline state objects upfront.
                    The engine controls caching and caches explicitly.
- **Instrumentable**:
                    Impeller tags and labels all graphics resources,
                    such as textures and buffers.
                    It can capture and persist animations to disk without affecting
                    per-frame rendering performance.
- **Portable**:
                    Flutter doesn't tie Impeller to a specific client-rendering API.
                    You can author shaders once and convert them to backend-specific
                    formats, as necessary.
- **Leverages modern graphics APIs**:
                    Impeller uses, but doesn't depend on, features available in
                    modern APIs like Metal and Vulkan.
- **Leverages concurrency**:
                    Impeller can distribute single-frame workloads across multiple
                    threads, if necessary.

## Availability

Where can you use Impeller? For*detailed*info, check out
                  the[Can I use Impeller?](https://flutter.dev/go/can-i-use-impeller)page.

### iOS

Impeller is the**only supported**rendering engine on iOS with
                  no ability to switch to Skia.

### Android

Impeller is**available and enabled by default on Android API 29+**.
                  On devices running lower versions of Android or don't support Vulkan,
                  Impeller falls back to the legacy OpenGL renderer.
                  No action on your part is necessary for this fallback behavior.

- @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

To*disable*Impeller when debugging,
                      pass`--no-enable-impeller`to the`flutter run`command.

`--no-enable-impeller`
`flutter run`
`flutter run --no-enable-impeller`
To*disable*Impeller when deploying your app,
                      add the following setting to your project's`AndroidManifest.xml`file under the`<application>`tag:

`AndroidManifest.xml`
`<application>`
`<meta-data
    android:name="io.flutter.embedding.android.EnableImpeller"
    android:value="false" />`
### Web

Flutter on the web offers[two renderers](https://docs.flutter.dev/platform-integration/web/renderers#renderers)--`canvaskit`and`skwasm`-- which both currently use Skia.
                  They might use Impeller in the future.

`canvaskit`
`skwasm`
### macOS

You can try out Impeller for macOS behind a flag.
                  In a future release, the ability to opt-out of
                  using Impeller will be removed.

To enable Impeller on macOS when debugging,
                  pass`--enable-impeller`to the`flutter run`command.

`--enable-impeller`
`flutter run`
`flutter run --enable-impeller`
To enable Impeller on macOS when deploying your app,
                  add the following tags under the top-level`<dict>`tag in your app's`Info.plist`file.

`<dict>`
`Info.plist`
`<key>FLTEnableImpeller</key>
  <true />`
### Bugs and issues

The team continues to improve Impeller support.
                  If you encounter performance or fidelity issues
                  with Impeller on any platform,
                  file an issue in the[GitHub tracker](https://github.com/flutter/flutter/issues/new/choose).
                  Prefix the issue title with`[Impeller]`and
                  include a small reproducible test case.

`[Impeller]`
Please include the following information when
                  submitting an issue for Impeller:

- The device you are running on,
                    including the chip information.
- Screenshots or recordings of any visible issues.
- An[export of the performance trace](https://docs.flutter.dev/tools/devtools/performance#import-and-export).
                    Zip the file and attach it to the GitHub issue.

## Architecture

To learn more details about Impeller's design and architecture,
                  check out the[README.md](https://github.com/flutter/flutter/blob/main/engine/src/flutter/impeller/README.md)file in the source tree.

## Additional information

- [Frequently asked questions](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/faq.md)
- [Impeller's coordinate system](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/coordinate_system.md)
- [How to set up Xcode for GPU frame captures with metal](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/xcode_frame_capture.md)
- [Learning to read GPU frame captures](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/read_frame_captures.md)
- [How to enable metal validation for command line apps](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/metal_validation.md)
- [How Impeller works around the lack of uniform buffers in Open GL ES 2.0](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/ubo_gles2.md)
- [Guidance for writing efficient shaders](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/shader_optimization.md)
- [How color blending works in Impeller](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/blending.md)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/impeller.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/perf/impeller&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/impeller.md).
