> 原文链接: [https://docs.flutter.dev/data-and-backend/state-mgmt/declarative](https://docs.flutter.dev/data-and-backend/state-mgmt/declarative)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

If you're coming to Flutter from an imperative framework
                  (such as Android SDK or iOS UIKit), you need to start
                  thinking about app development from a new perspective.

Many assumptions that you might have don't apply to Flutter. For example, in
                  Flutter it's okay to rebuild parts of your UI from scratch instead of modifying
                  it. Flutter is fast enough to do that, even on every frame if needed.

Flutter is*declarative*. This means that Flutter builds its user interface to
                  reflect the current state of your app:

When the state of your app changes
                  (for example, the user flips a switch in the settings screen),
                  you change the state, and that triggers a redraw of the user interface.
                  There is no imperative changing of the UI itself
                  (like`widget.setText`)—you change the state,
                  and the UI rebuilds from scratch.

`widget.setText`
Read more about the declarative approach to UI programming
                  in the[Introduction to declarative UI](https://docs.flutter.dev/flutter-for/declarative).

The declarative style of UI programming has many benefits.
                  Remarkably, there is only one code path for any state of the UI.
                  You describe what the UI should look
                  like for any given state, once—and that is it.

At first,
                  this style of programming might not seem as intuitive as the
                  imperative style. This is why this section is here. Read on.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/data-and-backend/state-mgmt/declarative.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/data-and-backend/state-mgmt/declarative&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/data-and-backend/state-mgmt/declarative.md).
