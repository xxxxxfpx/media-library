> 原文链接: [https://docs.flutter.dev/add-to-app/multiple-flutters](https://docs.flutter.dev/add-to-app/multiple-flutters)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Scenarios

If you're integrating Flutter into an existing app,
                  or gradually migrating an existing app to use Flutter,
                  you might find yourself wanting to add multiple
                  Flutter instances to the same project.
                  In particular, this can be useful in the
                  following scenarios:

- An application where the integrated Flutter screen is not a leaf node of
                    the navigation graph, and the navigation stack might be a hybrid mixture of
                    native -> Flutter -> native -> Flutter.
- A screen where multiple partial screen Flutter views might be integrated
                    and visible at once.

The advantage of using multiple Flutter instances is that each
                  instance is independent and maintains its own internal navigation
                  stack, UI, and application states. This simplifies the overall application code's
                  responsibility for state keeping and improves modularity. More details on the
                  scenarios motivating the usage of multiple Flutters can be found at[flutter.dev/go/multiple-flutters](https://docs.flutter.dev/go/multiple-flutters).

Flutter is optimized for this scenario, with a low incremental
                  memory cost (~180kB) for adding additional Flutter instances. This fixed cost
                  reduction allows the multiple Flutter instance pattern to be used more liberally
                  in your add-to-app integration.

## Components

The primary API for adding multiple Flutter instances on both Android and iOS
                  is based on a new`FlutterEngineGroup`class ([Android API](https://cs.opensource.google/flutter/engine/+/main:shell/platform/android/io/flutter/embedding/engine/FlutterEngineGroup.java),[iOS API](https://cs.opensource.google/flutter/engine/+/main:shell/platform/darwin/ios/framework/Headers/FlutterEngineGroup.h))
                  to construct`FlutterEngine`s, rather than the`FlutterEngine`constructors used previously.

`FlutterEngineGroup`
`FlutterEngine`
`FlutterEngine`
Whereas the`FlutterEngine`API was direct and easier to consume, the`FlutterEngine`spawned from the same`FlutterEngineGroup`have the performance
                  advantage of sharing many of the common, reusable resources such as the GPU
                  context, font metrics, and isolate group snapshot, leading to a faster initial
                  rendering latency and lower memory footprint.

`FlutterEngine`
`FlutterEngine`
`FlutterEngineGroup`

`FlutterEngine`s spawned from`FlutterEngineGroup`can be used to
                       connect to UI classes like[FlutterActivity](https://api.flutter.dev/javadoc/io/flutter/embedding/android/FlutterActivity.html)or[FlutterViewController](https://api.flutter.dev/ios-embedder/interface_flutter_view_controller.html)in the same way as normally constructed cached`FlutterEngine`s.

`FlutterEngine`
`FlutterEngineGroup`
`FlutterActivity`
`FlutterViewController`
`FlutterEngine`
The first`FlutterEngine`spawned from the`FlutterEngineGroup`doesn't need
                      to continue surviving in order for subsequent`FlutterEngine`s to share
                      resources as long as there's at least 1 living`FlutterEngine`at all
                      times.

`FlutterEngine`
`FlutterEngineGroup`
`FlutterEngine`
`FlutterEngine`
Creating the very first`FlutterEngine`from a`FlutterEngineGroup`has
                      the same[performance characteristics](https://docs.flutter.dev/add-to-app/performance)as constructing a`FlutterEngine`using the constructors did previously.

`FlutterEngine`
`FlutterEngineGroup`
`FlutterEngine`
When all`FlutterEngine`s from a`FlutterEngineGroup`are destroyed, the next`FlutterEngine`created has the same performance characteristics as the very
                      first engine.

`FlutterEngine`
`FlutterEngineGroup`
`FlutterEngine`
The`FlutterEngineGroup`itself doesn't need to live beyond all of the spawned
                      engines. Destroying the`FlutterEngineGroup`doesn't affect existing spawned`FlutterEngine`s but does remove the ability to spawn additional`FlutterEngine`s that share resources with existing spawned engines.

`FlutterEngineGroup`
`FlutterEngineGroup`
`FlutterEngine`
`FlutterEngine`
## Communication

Communication between Flutter instances is handled using[platform channels](https://docs.flutter.dev/platform-integration/platform-channels)(or[Pigeon](https://pub.dev/packages/pigeon)) through the host platform. To see our roadmap on communication,
                  or other planned work on enhancing multiple Flutter instances, check out[Issue 72009](https://github.com/flutter/flutter/issues/72009).

## Samples

You can find a sample demonstrating how to use`FlutterEngineGroup`on both Android and iOS on[GitHub](https://github.com/flutter/samples/tree/main/add_to_app/multiple_flutters).

`FlutterEngineGroup`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/multiple-flutters.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/add-to-app/multiple-flutters&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/add-to-app/multiple-flutters.md).
