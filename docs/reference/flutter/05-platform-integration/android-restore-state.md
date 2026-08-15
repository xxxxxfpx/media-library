> 原文链接: [https://docs.flutter.dev/platform-integration/android/restore-state-android](https://docs.flutter.dev/platform-integration/android/restore-state-android)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

When a user runs a mobile app and then selects another
                  app to run, the first app is moved to the background,
                  or*backgrounded*. The operating system (both iOS and Android)
                  might kill the backgrounded app to release memory and
                  improve performance for the app running in the foreground.

When the user selects the app again, bringing it
                  back to the foreground, the OS relaunches it.
                  But, unless you've set up a way to save the
                  state of the app before it was killed,
                  you've lost the state and the app starts from scratch.
                  The user has lost the continuity they expect,
                  which is clearly not ideal.
                  (Imagine filling out a lengthy form and being interrupted
                  by a phone call*before*clicking**Submit**.)

So, how can you restore the state of the app so that
                  it looks like it did before it was sent to the
                  background?

Flutter has a solution for this with the[RestorationManager](https://api.flutter.dev/flutter/services/RestorationManager-class.html)(and related classes)
                  in the[services](https://api.flutter.dev/flutter/services/services-library.html)library.
                  With the`RestorationManager`, the Flutter framework
                  provides the state data to the engine*as the state
                    changes*, so that the app is ready when the OS signals
                  that it's about to kill the app, giving the app only
                  moments to prepare.

`RestorationManager`
`RestorationManager`
## Overview

You can enable state restoration with just a few tasks:


Define a`restorationScopeId`for classes like`CupertinoApp`,`MaterialApp`, or`WidgetsApp`.

`restorationScopeId`
`CupertinoApp`
`MaterialApp`
`WidgetsApp`
Define a`restorationId`for widgets that support it,
                      such as[TextField](https://api.flutter.dev/flutter/material/TextField/restorationId.html)and[ScrollView](https://api.flutter.dev/flutter/widgets/ScrollView/restorationId.html).
                      This automatically enables built-in state restoration
                      for those widgets.

`restorationId`
`TextField`
`ScrollView`
For custom widgets,
                      you must decide what state you want to restore
                      and hold that state in a[RestorableProperty](https://api.flutter.dev/flutter/widgets/RestorableProperty-class.html).
                      (The Flutter API provides various subclasses for
                      different data types.)
                      Define those`RestorableProperty`widgets
                      in a`State`class that uses the[RestorationMixin](https://api.flutter.dev/flutter/widgets/RestorationMixin-mixin.html).
                      Register those widgets with the mixin in a`restoreState`method.

`RestorableProperty`
`RestorableProperty`
`State`
`RestorationMixin`
`restoreState`
If you use any Navigator API (like`push`,`pushNamed`, and so on)
                      migrate to the API that has "restorable" in the name
                      (`restorablePush`,`restorablePushNamed`, and so on)
                      to restore the navigation stack.

`push`
`pushNamed`
`restorablePush`
`restorablePushNamed`
Other considerations:


Providing a`restorationScopeId`to`MaterialApp`,`CupertinoApp`, or`WidgetsApp`automatically enables state restoration by
                      injecting a`RootRestorationScope`.
                      If you need to restore state*above*the app class,
                      inject a`RootRestorationScope`manually.

`restorationScopeId`
`MaterialApp`
`CupertinoApp`
`WidgetsApp`
`RootRestorationScope`
`RootRestorationScope`
**The difference between arestorationIdand
                        arestorationScopeId:**Widgets that take a`restorationScopeId`create a new`restorationScope`(a new`RestorationBucket`) into which all children
                      store their state. A`restorationId`means the widget
                      (and its children) store the data in the surrounding bucket.

`restorationId`
`restorationScopeId`
`restorationScopeId`
`restorationScope`
`RestorationBucket`
`restorationId`
## Restoring navigation state

If you want your app to return to a particular route
                  that the user was most recently viewing
                  (the shopping cart, for example), then you must implement
                  restoration state for navigation, as well.

If you use the Navigator API directly,
                  migrate the standard methods to restorable
                  methods (that have "restorable" in the name).
                  For example, replace`push`with[restorablePush](https://api.flutter.dev/flutter/widgets/Navigator/restorablePush.html).

`push`
`restorablePush`
## Testing state restoration

To test state restoration, set up your mobile device so that
                  it doesn't save state once an app is backgrounded.
                  To learn how to do this for both iOS and Android,
                  check out[Testing state restoration](https://api.flutter.dev/flutter/services/RestorationManager-class.html#testing-state-restoration)on the[RestorationManager](https://api.flutter.dev/flutter/services/RestorationManager-class.html)page.

`RestorationManager`
## Other resources

For further information on state restoration,
                  check out the following resources.


To learn more about short term and long term state,
                      check out[Differentiate between ephemeral state
                        and app state](https://docs.flutter.dev/data-and-backend/state-mgmt/ephemeral-vs-app).

You might want to check out packages on pub.dev that
                      perform state restoration, such as[statePersistence](https://pub.dev/packages/state_persistence).

`statePersistence`
For more information on navigation and the[go_router](https://pub.dev/packages/go_router)package, check out[Navigation and routing](https://docs.flutter.dev/ui/navigation)and the[State restoration](https://pub.dev/documentation/go_router/latest/topics/State%20restoration-topic.html)topic on pub.dev.

`go_router`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/android/restore-state-android.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/android/restore-state-android&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/android/restore-state-android.md).
