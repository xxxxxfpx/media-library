> 原文链接: [https://docs.flutter.dev/ui/navigation](https://docs.flutter.dev/ui/navigation)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter provides a complete system for navigating between screens and handling
                  deep links. Small applications without complex deep linking can use[Navigator](https://api.flutter.dev/flutter/widgets/Navigator-class.html), while apps with specific deep linking and navigation
                  requirements should also use the[Router](https://api.flutter.dev/flutter/widgets/Router-class.html)to correctly handle deep links on
                  Android and iOS, and to stay in sync with the address bar when the app is
                  running on the web.

`Navigator`
`Router`
To configure your Android or iOS application to handle deep links, see[Deep linking](https://docs.flutter.dev/ui/navigation/deep-linking).

## Using the Navigator

The`Navigator`widget displays screens as a stack using the correct transition
                  animations for the target platform. To navigate to a new screen, access the`Navigator`through the route's`BuildContext`and call imperative methods such
                  as`push()``or pop()`:

`Navigator`
`Navigator`
`BuildContext`
`push()`
`or pop()`
`child: const Text('Open second screen'),
onPressed: () {
  Navigator.of(context).push(
    MaterialPageRoute<void>(
      builder: (context) => const SecondScreen(),
    ),
  );
},`
Because`Navigator`keeps a stack of`Route`objects (representing the history
                  stack), The`push()`method also takes a`Route`object. The`MaterialPageRoute`object is a subclass of`Route`that specifies the transition animations for
                  Material Design. For more examples of how to use the`Navigator`, follow the[navigation recipes](https://docs.flutter.dev/cookbook/navigation)from the Flutter Cookbook or
                  visit the[Navigator API documentation](https://api.flutter.dev/flutter/widgets/Navigator-class.html).

`Navigator`
`Route`
`push()`
`Route`
`MaterialPageRoute`
`Route`
`Navigator`
## Using named routes

Applications with simple navigation and deep linking requirements can use the`Navigator`for navigation and the[MaterialApp.routes](https://api.flutter.dev/flutter/material/MaterialApp/routes.html)parameter for deep
                  links:

`Navigator`
`MaterialApp.routes`
`child: const Text('Open second screen'),
onPressed: () {
  Navigator.pushNamed(context, '/second');
},`
`/second`represents a*named route*that was declared in the`MaterialApp.routes`list. For a complete example, follow the[Navigate with named routes](https://docs.flutter.dev/cookbook/navigation/named-routes)recipe from the Flutter Cookbook.

`/second`
`MaterialApp.routes`
### Limitations

Although named routes can handle deep links, the behavior is always the same and
                  can't be customized. When a new deep link is received by the platform, Flutter
                  pushes a new`Route`onto the Navigator regardless of where the user currently is.

`Route`
Flutter also doesn't support the browser forward button for applications using
                  named routes. For these reasons, we don't recommend using named routes in most
                  applications. Instead, use a routing package like[go_router](https://pub.dev/packages/go_router)or
                  use`Navigator`with[MaterialPageRoute](https://api.flutter.dev/flutter/material/MaterialPageRoute-class.html).

`Navigator`
`MaterialPageRoute`
## Using the Router

Flutter applications with advanced navigation and routing requirements (such as
                  a web app that uses direct links to each screen, or an app with multiple`Navigator`widgets) should use a routing package such as[go_router](https://pub.dev/packages/go_router)that can
                  parse the route path and configure the`Navigator`whenever the app receives a
                  new deep link.

`Navigator`
`Navigator`
To use the Router, switch to the`router`constructor on`MaterialApp`or`CupertinoApp`and provide it with a`Router`configuration. Routing packages,
                  such as[go_router](https://pub.dev/packages/go_router), typically provide route configuration and routes
                  can be used as follows:

`router`
`MaterialApp`
`CupertinoApp`
`Router`
`child: const Text('Open second screen'),
onPressed: () => context.go('/second'),`
Because packages like go_router are*declarative*, they will always display the
                  same screen(s) when a deep link is received.

## Using Router and Navigator together

The`Router`and`Navigator`are designed to work together. You can navigate
                  using the`Router`API through a declarative routing package, such as`go_router`, or by calling imperative methods such as`push()`and`pop()`on
                  the`Navigator`.

`Router`
`Navigator`
`Router`
`go_router`
`push()`
`pop()`
`Navigator`
When you navigate using the`Router`or a declarative routing package, each
                  route on the Navigator is*page-backed*, meaning it was created from a[Page](https://api.flutter.dev/flutter/widgets/Page-class.html)using the[pages](https://api.flutter.dev/flutter/widgets/Navigator/pages.html)argument on the`Navigator`constructor. Conversely, any`Route`created by calling`Navigator.push`or`showDialog`will add a*pageless*route to the Navigator. If you are using a routing package, Routes that are*page-backed*are always deep-linkable, whereas*pageless*routes
                  are not.

`Router`
`Page`
`pages`
`Navigator`
`Route`
`Navigator.push`
`showDialog`
When a*page-backed*`Route`is removed from the`Navigator`, all of the*pageless*routes after it are also removed. For example, if a deep link
                  navigates by removing a*page-backed*route from the Navigator, all*pageless*routes after (up until the next*page-backed*route) are removed too.

`Route`
`Navigator`
## Web support

Apps using the`Router`class integrate with the browser History API to provide
                  a consistent experience when using the browser's back and forward buttons.
                  Whenever you navigate using the`Router`, a History API entry is added to the
                  browser's history stack. Pressing the**back**button uses*reverse
                      chronological navigation*, meaning that the user is taken to the previously
                  visited location that was shown using the`Router`. This means that if the user
                  pops a page from the`Navigator`and then presses the browser**back**button
                  the previous page is pushed back onto the stack.

`Router`
`Router`
`Router`
`Navigator`
## More information

For more information on navigation and routing, check out the following
                  resources:

- The Flutter cookbook includes multiple[navigation recipes](https://docs.flutter.dev/cookbook/navigation)that show how to
                    use the`Navigator`.
- The[Navigator](https://api.flutter.dev/flutter/widgets/Navigator-class.html)and[Router](https://api.flutter.dev/flutter/widgets/Router-class.html)API documentation contain details on how
                    to set up declarative navigation without a routing package.
- [Understanding navigation](https://material.io/design/navigation/understanding-navigation.html), a page from the Material Design documentation,
                    outlines concepts for designing the navigation in your app, including
                    explanations for forward, upward, and chronological navigation.
- [Learning Flutter's new navigation and routing system](https://medium.com/flutter/learning-flutters-new-navigation-and-routing-system-7c9068155ade), an article on
                    Medium, describes how to use the`Router`widget directly, without
                    a routing package.
- The[Router design document](https://flutter.dev/go/navigator-with-router)contains the motivation and design of the`Router`API.

`Navigator`
`Navigator`
`Router`
`Router`
`Router`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/navigation/index.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/ui/navigation&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/navigation/index.md).
