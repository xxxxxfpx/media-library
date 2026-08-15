> 原文链接: [https://docs.flutter.dev/data-and-backend/state-mgmt/options](https://docs.flutter.dev/data-and-backend/state-mgmt/options)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

State management is a complex topic.
                  If you feel that some of your questions haven't been answered,
                  or that the approach described on these pages
                  is not viable for your use cases, you are probably right.

Learn more from the following resources,
                  many of which have been contributed by the Flutter community.

## General overview

Things to review before selecting an approach.

- [Introduction to state management](https://docs.flutter.dev/data-and-backend/state-mgmt/intro),
                    which is the beginning of this very section
                    (for those of you who arrived directly to this*Options*page
                    and missed the previous pages)
- [Pragmatic State Management in Flutter](https://www.youtube.com/watch?v=d_m5csmrf7I),
                    a video from Google I/O 2019
- [Flutter Architecture Samples](https://fluttersamples.com/), by Brian Egan

## Built-in approaches

### setState

`setState`
The low-level approach to use for widget-specific, ephemeral state.

- [Adding interactivity to your Flutter app](https://docs.flutter.dev/ui/interactivity), a Flutter tutorial
- [Basic state management in Google Flutter](https://medium.com/@agungsurya/basic-state-management-in-google-flutter-6ee73608f96d), by Agung Surya

### ValueNotifierandInheritedNotifier

`ValueNotifier`
`InheritedNotifier`
An approach using only Flutter provided APIs to
                  update state and notify the UI of changes.

- [State Management using ValueNotifier and InheritedNotifier](https://www.hungrimind.com/articles/flutter-state-management), by Tadas Petra

### InheritedWidgetandInheritedModel

`InheritedWidget`
`InheritedModel`
The low-level approach used to
                  communicate between ancestors and children in the widget tree.
                  This is what`package:provider`and many other approaches use under the hood.

`package:provider`
The following instructor-led video workshop covers how to
                  use`InheritedWidget`:

`InheritedWidget`
Other useful docs include:

- [InheritedWidget docs](https://api.flutter.dev/flutter/widgets/InheritedWidget-class.html)
- [Managing Flutter Application State With InheritedWidgets](https://blog.flutter.dev/managing-flutter-application-state-with-inheritedwidgets-1140452befe1),
                    by Hans Muller
- [Inheriting Widgets](https://medium.com/@mehmetf_71205/inheriting-widgets-b7ac56dbbeb1), by Mehmet Fidanboylu
- [Widget - State - Context - InheritedWidget](https://flutteris.com/blog/en/widget-state-context-inheritedwidget), by Didier Bolelens

## Community-provided packages

Depending on the complexity of your app and preferences of your team,
                  you might find adopting a state management package useful.
                  State management packages often help reduce boilerplate code,
                  provide specialized debugging tools, and can help
                  enable a clearer and consistent application architecture.

The Flutter community offers a wide variety of state management packages.
                  The best choice for your app often depends on the app's complexity,
                  your team's preferences, and the specific problems you need to solve.

To begin exploring the available options,
                  check out the[#state-management](https://pub.dev/packages?q=topic%3Astate-management)topic on the pub.dev site and
                  refine the search to find packages that match your needs.

`#state-management`
Explore the variety of state-management packages built by and for the Flutter community.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/data-and-backend/state-mgmt/options.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/data-and-backend/state-mgmt/options&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/data-and-backend/state-mgmt/options.md).
