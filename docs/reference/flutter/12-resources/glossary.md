> 原文链接: [https://docs.flutter.dev/resources/glossary](https://docs.flutter.dev/resources/glossary)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The following are definitions of terms used across the Flutter documentation.

## Adaptive

Adaptive design is about the UI being*usable*in the space,
                        as opposed to responsive design which is about fitting the UI*into*the space.
                        An adaptive app selects the appropriate layout
                        (such as having a bottom nav instead of a side panel)
                        and input devices (for example, mouse versus touch)
                        to feel natural on the current device.

### Related docs and resources

- [articleAdaptive vs responsive design](https://docs.flutter.dev/ui/adaptive-responsive#what-is-responsive-vs-adaptive)
- [articleBuilding adaptive apps](https://docs.flutter.dev/ui/adaptive-responsive)

## Agent skill

An agent skill is a specialized set of instructions,
                        scripts, and resources that extend an AI agent's capabilities
                        for a specific domain or task.
                        Skills enable agents to interact with the environment,
                        execute multi-step workflows,
                        and perform complex problem-solving autonomously.

## Cupertino

Flutter's`cupertino`library implements the iOS design language,
                        comprising a set of widgets that implement Apple's Human Interface Guidelines.

`cupertino`
The`cupertino`library, originally part of the main Flutter repo,
                        will be decoupled into a separate package.
                        For more information,
                        visit[flutter.dev/go/decouple-design](https://flutter.dev/go/decouple-design).

`cupertino`
### Related docs and resources

- [open_in_newHuman Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [articleCupertino widgets](https://docs.flutter.dev/ui/widgets/cupertino)

## Dart

Dart is an approachable, portable, and performant language designed
                        for full-stack app development. It offers sound null safety,
                        a strong type system, and compiles to native machine code
                        for mobile, desktop, and backend, as well as JavaScript or WebAssembly
                        for the web. While Dart is the foundation of Flutter,
                        it is also used for building command-line tools, servers,
                        and other applications.

### Related docs and resources

- [open_in_newDart language site](https://dart.dev)

## Declarative

Declarative programming is a style where you describe the*current state*of your UI, and the framework takes care
                        of transitioning the UI to match that state.

In Flutter, widgets are immutable "blueprints".
                        To change the UI, a widget triggers a rebuild on itself
                        (usually by calling`setState`) and constructs a new widget subtree.
                        This contrasts with*imperative*programming,
                        where you manually construct and mutate UI entities.

`setState`
### Related docs and resources

- [articleIntroduction to declarative UI](https://docs.flutter.dev/get-started/flutter-for/declarative)
- [articleStart thinking declaratively](https://docs.flutter.dev/data-and-backend/state-mgmt/declarative)

## Embedder

Each native platform supported by Flutter has an*embedder*for platform-specific logic. The embedder is the bridge
                        that coordinates with the underlying operating system.
                        It provides access to services like input, accessibility,
                        message event loops, and more.
                        The embedder also launches and manages the Flutter engine.

Each embedder is written in the platform's native language:
                        Java and Kotlin for Android, Swift and Objective-C for iOS and macOS,
                        and C++ for Windows and Linux.

Each embedder enables plugin packages to add additional
                        platform-specific functionality to the app.

The embedder is launched and managed by the runner app.

### Related docs and resources

- [articleArchitectural overview: The Embedder](https://docs.flutter.dev/resources/architectural-overview#platform-embedding)
- [articleFlutter on embedded devices](https://docs.flutter.dev/embedded)

## Engine

The engine is Flutter's platform-agnostic logic that's written
                        in native code, mostly C++.

The main responsibilities of the engine are as follows:

1. Exposes the`dart:ui`API, which are the low-level primitives
                          that the Flutter[framework](https://docs.flutter.dev/resources/architectural-overview#architectural-layers)builds upon.
1. Converts low-level drawing commands into pixels (also called*rasterization*, this includes@simple_tooltip data={"target":"ref-4nSxTWmT","content":"ref-7PvvEsIf"}[Impeller](https://docs.flutter.dev/resources/glossary#impeller)ImpellerFlutter's modern graphics rendering engine,
designed for smooth, predictable performance.[Learn more](https://docs.flutter.dev/resources/glossary#impeller)/@simple_tooltipand Skia).
1. Responsible for launching and managing Dart's runtime.
1. Responsible for laying out text.
1. Responsible for asset resolution.

`dart:ui`
### Related docs and resources

- [articleArchitectural overview: The Engine](https://docs.flutter.dev/resources/architectural-overview#architectural-layers)
- [code_blocksEngine repository](https://github.com/flutter/flutter/tree/main/engine/src/flutter)

## Frame

Flutter aims to produce 60 frames per second (fps),
                        or 120 fps on capable devices.
                        This means the framework has approximately 16ms (at 60 fps)
                        or 8ms (at 120 fps) to render each frame.
                        If the app takes longer than this to render a frame,
                        the user might see@simple_tooltip data={"target":"ref-jfP2IuC5","content":"ref--Jtfebwn"}[jank](https://docs.flutter.dev/resources/glossary#jank)JankWhen an app appears to stutter or jerk visually instead of animating
smoothly.[Learn more](https://docs.flutter.dev/resources/glossary#jank)/@simple_tooltip.

### Related docs and resources

- [articleRendering performance](https://docs.flutter.dev/perf/rendering-performance)

## Hot reload

This feature is also called "stateful hot reload".
                        After the Dart runtime updates classes with the new versions
                        of fields and functions, the Flutter framework automatically
                        rebuilds the widget tree, allowing you to quickly view the effects
                        of your changes. Hot reload greatly increases the speed of development.

Hot reload works on mobile, web, and desktop apps that are
                        running in debug mode and is fully supported in VS Code,
                        Android Studio, and IntelliJ IDEA. It does not re-run`main`or`initState`; for that, use@simple_tooltip data={"target":"ref-No8PTzzs","content":"ref-i3wM8F-k"}[hot restart](https://docs.flutter.dev/resources/glossary#hot-restart)Hot restartSimilar to hot reload, but it does not maintain app state.
Use hot restart to re-run `main` or `initState`.[Learn more](https://docs.flutter.dev/resources/glossary#hot-restart)/@simple_tooltip.

`main`
`initState`
### Related docs and resources

- [articleHot reload documentation](https://docs.flutter.dev/tools/hot-reload)
- [play_arrowFast development cycles with Flutter's hot reload](https://youtu.be/YScJS8obxlo?si=QxJDIf_LGmle2Xs6)
- [play_arrowStateful hot reload for web is here](https://youtu.be/7nT3BHm6Gyg?si=nLUM0n69PSQnm8CF)

## Hot restart

`main`
`initState`
Hot restart is still faster than a full restart, which also
                        recompiles the native, platform code (such as Swift).
                        On the web, it also restarts the Dart Development Compiler (DDC).

### Related docs and resources

- [articleDifference between hot reload, hot restart, and full restart](https://docs.flutter.dev/tools/hot-reload#hot-restart)

## Impeller

*Impeller*is Flutter's high-performance rendering engine,
                        built from the ground up for Flutter's needs and modern graphics APIs.

Its primary goal is to provide consistently smooth performance and
                        eliminate stuttering while rendering, particularly that
                        caused by shader compilation during animations and interactions.

Impeller achieves this by pre-compiling a specific, smaller set of
                        shaders at application build time, rather than compiling at runtime.

### Related docs and resources

- [articleImpeller documentation](https://docs.flutter.dev/perf/impeller)
- [open_in_newImpeller FAQ](https://github.com/flutter/flutter/blob/main/docs/engine/impeller/docs/faq.md)

## Jank

Jank occurs when a system can't keep up with the expected frame rate
                        and drops frames. Jank is a performance problem. Flutter offers
                        information and tooling, such as the Performance tool in DevTools,
                        that can help you diagnose and fix jank in your application.

### Related docs and resources

- [articleUse the Performance view in DevTools](https://docs.flutter.dev/tools/devtools/performance)
- [articleImproving rendering performance](https://docs.flutter.dev/perf/rendering-performance)
- [articlePerformance best practices](https://docs.flutter.dev/perf/best-practices)
- [articleMeasure performance with an integration test](https://docs.flutter.dev/cookbook/testing/integration/profiling)

## Material

Material Design is an adaptable system of guidelines, components, and tools
                        that support the best practices of user interface design.
                        Flutter's`material`library implements Material Design widgets.

`material`
The`material`library, originally part of the main Flutter repo,
                        will be decoupled into a separate package.
                        For more information,
                        visit[flutter.dev/go/decouple-design](https://flutter.dev/go/decouple-design).

`material`
### Related docs and resources

- [open_in_newMaterial Design site](https://m3.material.io)
- [articleMaterial widgets](https://docs.flutter.dev/ui/widgets/material)

## Null safety

`null`
Dart's null safety prevents errors that result from unintentional access
                        of variables set to`null`.

`null`
With[sound null safety](https://dart.dev/null-safety), variables are non-nullable by default:
                        they can only be assigned a value of`null`if you explicitly declare
                        them as nullable.
                        This differs from other "mixed" null safety implementations,
                        where a non-nullable variable could still contain`null`at runtime.
                        With Dart's sound null safety, the compiler guarantees that a
                        non-nullable variable can never be`null`.

`null`
`null`
`null`
### Related docs and resources

- [open_in_newSound null safety](https://dart.dev/null-safety)
- [schoolNull safety codelab](https://dart.dev/codelabs/null-safety)

## Prop drilling

The process of passing data through multiple layers of widgets
                        through constructor parameters, usually to reach a deeper descendant.
                        This pattern can become verbose, which is
                        why other state management solutions
                        (like`InheritedWidget`or`Provider`) are often used.

`InheritedWidget`
`Provider`
### Related docs and resources

- [articleState management introduction](https://docs.flutter.dev/data-and-backend/state-mgmt/intro)

## pub

Pub is the tool used for managing Dart packages.
                        It allows you to install, upgrade, and manage dependencies for your Dart app.
                        Dependencies are defined in the[pubspec.yaml](https://dart.dev/tools/pub/pubspec)file.
                        Packages are hosted on[pub.dev](https://pub.dev), the official package repository.

`pubspec.yaml`
### Related docs and resources

- [open_in_newpub.dev](https://pub.dev)
- [articleUsing packages](https://docs.flutter.dev/packages-and-plugins/using-packages)

## RenderObject

While widgets are immutable blueprints,`RenderObject`s are mutable objects that persist between frames.
                        They handle the heavy lifting of determining exactly where elements
                         should be placed and how they should look.

`RenderObject`
They represent a node in the render tree,
                        which is the most detailed tree in Flutter's multi-tree architecture.

### Related docs and resources

- [articleArchitectural Overview: The Rendering Layer](https://docs.flutter.dev/resources/architectural-overview#architectural-layers)
- [descriptionRenderObject API documentation](https://api.flutter.dev/flutter/rendering/RenderObject-class.html)

## Sliver

A sliver is a portion of a scrollable area that you can define
                        to behave in a special way.
                        Think of slivers as building blocks that you can compose together
                        inside a`CustomScrollView`to create custom scrolling experiences,
                        like elastic scrolling or a collapsing header.
                        Slivers are built lazily, which means that Flutter only renders
                        the slivers that are visible on screen,
                        making them very efficient for long lists of content.

`CustomScrollView`
### Related docs and resources

- [articleSliver documentation](https://docs.flutter.dev/ui/layout/scrolling/slivers)
- [articleSlivers demystified](https://blog.flutter.dev/slivers-demystified-6ff68ab0296f)
- [play_arrowSliverList and SliverGrid WotW](https://youtu.be/ORiTTaVY6mM)
- [play_arrowSliverAppBar WotW](https://youtu.be/R9C5KMJKluE)
- [descriptionCustomScrollView class](https://api.flutter.dev/flutter/widgets/CustomScrollView-class.html)
- [descriptionSliverAppBar class](https://api.flutter.dev/flutter/material/SliverAppBar-class.html)
- [descriptionSliverGrid class](https://api.flutter.dev/flutter/widgets/SliverGrid-class.html)
- [descriptionSliverList class](https://api.flutter.dev/flutter/widgets/SliverList-class.html)

## Viewport

A viewport is the visual component of the scrolling machinery.
                        It displays a subset of its children (usually slivers)
                        based on the current scroll offset.
                        It is often described as being "bigger on the inside"
                        because it can contain more content than is visible on the screen.

### Related docs and resources

- [descriptionViewport class](https://api.flutter.dev/flutter/widgets/Viewport-class.html)
- [articleSlivers](https://docs.flutter.dev/ui/layout/scrolling/slivers)

## Widget

An immutable description of part of a user interface.

In Flutter, almost everything is a*widget*.
                        Widgets are the fundamental building blocks you use to
                        create your application's UI with Flutter.
                        Each widget is an immutable declaration of _what the UI should
                        look like based on its current configuration and state.

Widgets are composed together in a hierarchy to form the widget tree.
                        When a widget's state changes, the Flutter framework
                        rebuilds the necessary parts of the tree to update the UI.

The two primary types of widgets are[StatelessWidget](https://api.flutter.dev/flutter/widgets/StatelessWidget-class.html), which have no mutable state, and[StatefulWidget](https://api.flutter.dev/flutter/widgets/StatefulWidget-class.html), which have a persistent[state](https://api.flutter.dev/flutter/widgets/State-class.html)that can be updated.

`StatelessWidget`
`StatefulWidget`
### Related docs and resources

- [articleWidget fundamentals](https://docs.flutter.dev/learn/pathway/tutorial/widget-fundamentals)
- [articleWidget catalog](https://docs.flutter.dev/ui/widgets)
- [descriptionWidget class](https://api.flutter.dev/flutter/widgets/Widget-class.html)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5.[Report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/resources/glossary).
