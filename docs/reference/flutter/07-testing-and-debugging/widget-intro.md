> 原文链接: [https://docs.flutter.dev/cookbook/testing/widget/introduction](https://docs.flutter.dev/cookbook/testing/widget/introduction)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

In the[introduction to unit testing](https://docs.flutter.dev/cookbook/testing/unit/introduction)recipe,
                  you learned how to test Dart classes using the`test`package.
                  To test widget classes, you need a few additional tools provided by the[flutter_test](https://api.flutter.dev/flutter/flutter_test/flutter_test-library.html)package, which ships with the Flutter SDK.

`test`
`flutter_test`
The`flutter_test`package provides the following tools for
                  testing widgets:

`flutter_test`
- The[WidgetTester](https://api.flutter.dev/flutter/flutter_test/WidgetTester-class.html)allows building and interacting
                    with widgets in a test environment.
- The[testWidgets()](https://api.flutter.dev/flutter/flutter_test/testWidgets.html)function automatically
                    creates a new`WidgetTester`for each test case,
                    and is used in place of the normal`test()`function.
- The[Finder](https://api.flutter.dev/flutter/flutter_test/Finder-class.html)classes allow searching for widgets
                    in the test environment.
- Widget-specific[Matcher](https://api.flutter.dev/flutter/package-matcher_matcher/Matcher-class.html)constants help verify
                       whether a`Finder`locates a widget or
                    multiple widgets in the test environment.

`WidgetTester`
`testWidgets()`
`WidgetTester`
`test()`
`Finder`
`Matcher`
`Finder`
If this sounds overwhelming, don't worry. Learn how all of these pieces fit
                  together throughout this recipe, which uses the following steps:

1. Add the`flutter_test`dependency.
1. Create a widget to test.
1. Create a`testWidgets`test.
1. Build the widget using the`WidgetTester`.
1. Search for the widget using a`Finder`.
1. Verify the widget using a`Matcher`.

`flutter_test`
`testWidgets`
`WidgetTester`
`Finder`
`Matcher`
## 1. Add theflutter_testdependency

`flutter_test`
Before writing tests, include the`flutter_test`dependency in the`dev_dependencies`section of the`pubspec.yaml`file.
                  If creating a new Flutter project with the command line tools or
                  a code editor, this dependency should already be in place.

`flutter_test`
`dev_dependencies`
`pubspec.yaml`
`dev_dependencies:
  flutter_test:
    sdk: flutter`
## 2. Create a widget to test

Next, create a widget for testing. For this recipe,
                  create a widget that displays a`title`and`message`.

`title`
`message`
`class MyWidget extends StatelessWidget {
  const MyWidget({super.key, required this.title, required this.message});
​
  final String title;
  final String message;
​
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      home: Scaffold(
        appBar: AppBar(title: Text(title)),
        body: Center(child: Text(message)),
      ),
    );
  }
}`
## 3. Create atestWidgetstest

`testWidgets`
With a widget to test, begin by writing your first test.
                  Use the[testWidgets()](https://api.flutter.dev/flutter/flutter_test/testWidgets.html)function provided by the`flutter_test`package to define a test.
                  The`testWidgets`function allows you to define a
                  widget test and creates a`WidgetTester`to work with.

`testWidgets()`
`flutter_test`
`testWidgets`
`WidgetTester`
This test verifies that`MyWidget`displays a given title and message.
                  It is titled accordingly, and it will be populated in the next section.

`MyWidget`
`void main() {
  // Define a test. The TestWidgets function also provides a WidgetTester
  // to work with. The WidgetTester allows you to build and interact
  // with widgets in the test environment.
  testWidgets('MyWidget has a title and message', (tester) async {
    // Test code goes here.
  });
}`
## 4. Build the widget using theWidgetTester

`WidgetTester`
Next, build`MyWidget`inside the test environment by using the[pumpWidget()](https://api.flutter.dev/flutter/flutter_test/WidgetTester/pumpWidget.html)method provided by`WidgetTester`.
                  The`pumpWidget`method builds and renders the provided widget.

`MyWidget`
`pumpWidget()`
`WidgetTester`
`pumpWidget`
Create a`MyWidget`instance that displays "T" as the title
                  and "M" as the message.

`MyWidget`
`void main() {
  testWidgets('MyWidget has a title and message', (tester) async {
    // Create the widget by telling the tester to build it.
    await tester.pumpWidget(const MyWidget(title: 'T', message: 'M'));
  });
}`
### Notes about the pump() methods

After the initial call to`pumpWidget()`, the`WidgetTester`provides
                  additional ways to rebuild the same widget. This is useful if you're
                  working with a`StatefulWidget`or animations.

`pumpWidget()`
`WidgetTester`
`StatefulWidget`
For example, tapping a button calls`setState()`, but Flutter won't
                  automatically rebuild your widget in the test environment.
                  Use one of the following methods to ask Flutter to rebuild the widget.

`setState()`
`tester.pump(Duration duration)`
Schedules a frame and triggers a rebuild of the widget.
                      If a`Duration`is specified, it advances the clock by
                      that amount and schedules a frame. It does not schedule
                      multiple frames even if the duration is longer than a
                      single frame.

`Duration`
`tester.pumpAndSettle()`
Repeatedly calls`pump()`with the given duration until
                      there are no longer any frames scheduled.
                      This, essentially, waits for all animations to complete.

`pump()`
These methods provide fine-grained control over the build lifecycle,
                  which is particularly useful while testing.

## 5. Search for our widget using aFinder

`Finder`
With a widget in the test environment, search
                  through the widget tree for the`title`and`message`Text widgets using a`Finder`. This allows verification that
                  the widgets are being displayed correctly.

`title`
`message`
`Finder`
For this purpose, use the top-level[find()](https://api.flutter.dev/flutter/flutter_test/find-constant.html)method provided by the`flutter_test`package to create the`Finders`.
                  Since you know you're looking for`Text`widgets, use the[find.text()](https://api.flutter.dev/flutter/flutter_test/CommonFinders/text.html)method.

`find()`
`flutter_test`
`Finders`
`Text`
`find.text()`
For more information about`Finder`classes, see the[Finding widgets in a widget test](https://docs.flutter.dev/cookbook/testing/widget/finders)recipe.

`Finder`
`void main() {
  testWidgets('MyWidget has a title and message', (tester) async {
    await tester.pumpWidget(const MyWidget(title: 'T', message: 'M'));
​
    // Create the Finders.
    final titleFinder = find.text('T');
    final messageFinder = find.text('M');
  });
}`
## 6. Verify the widget using aMatcher

`Matcher`
Finally, verify the title and message`Text`widgets appear on screen
                  using the`Matcher`constants provided by`flutter_test`.`Matcher`classes are a core part of the`test`package,
                  and provide a common way to verify a given
                  value meets expectations.

`Text`
`Matcher`
`flutter_test`
`Matcher`
`test`
Ensure that the widgets appear on screen exactly one time.
                  For this purpose, use the[findsOneWidget](https://api.flutter.dev/flutter/flutter_test/findsOneWidget-constant.html)`Matcher`.

`findsOneWidget`
`Matcher`
`void main() {
  testWidgets('MyWidget has a title and message', (tester) async {
    await tester.pumpWidget(const MyWidget(title: 'T', message: 'M'));
    final titleFinder = find.text('T');
    final messageFinder = find.text('M');
​
    // Use the `findsOneWidget` matcher provided by flutter_test to verify
    // that the Text widgets appear exactly once in the widget tree.
    expect(titleFinder, findsOneWidget);
    expect(messageFinder, findsOneWidget);
  });
}`
### Additional Matchers

In addition to`findsOneWidget`,`flutter_test`provides additional
                  matchers for common cases.

`findsOneWidget`
`flutter_test`
`findsNothing`
Verifies that no widgets are found.

`findsWidgets`
Verifies that one or more widgets are found.

`findsNWidgets`
Verifies that a specific number of widgets are found.

`matchesGoldenFile`
Verifies that a widget's rendering matches a particular bitmap image ("golden file" testing).

## Complete example

`import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
​
void main() {
  // Define a test. The TestWidgets function also provides a WidgetTester
  // to work with. The WidgetTester allows building and interacting
  // with widgets in the test environment.
  testWidgets('MyWidget has a title and message', (tester) async {
    // Create the widget by telling the tester to build it.
    await tester.pumpWidget(const MyWidget(title: 'T', message: 'M'));
​
    // Create the Finders.
    final titleFinder = find.text('T');
    final messageFinder = find.text('M');
​
    // Use the `findsOneWidget` matcher provided by flutter_test to
    // verify that the Text widgets appear exactly once in the widget tree.
    expect(titleFinder, findsOneWidget);
    expect(messageFinder, findsOneWidget);
  });
}
​
class MyWidget extends StatelessWidget {
  const MyWidget({super.key, required this.title, required this.message});
​
  final String title;
  final String message;
​
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      home: Scaffold(
        appBar: AppBar(title: Text(title)),
        body: Center(child: Text(message)),
      ),
    );
  }
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/testing/widget/introduction.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/testing/widget/introduction&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/testing/widget/introduction.md).
