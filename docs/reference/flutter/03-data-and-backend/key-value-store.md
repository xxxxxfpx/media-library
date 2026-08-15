> 原文链接: [https://docs.flutter.dev/cookbook/persistence/key-value](https://docs.flutter.dev/cookbook/persistence/key-value)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

If you have a relatively small collection of key-values
                  to save, you can use the[shared_preferences](https://pub.dev/packages/shared_preferences)plugin.

`shared_preferences`
Normally, you would have to
                  write native platform integrations for storing data on each platform.
                  Fortunately, the[shared_preferences](https://pub.dev/packages/shared_preferences)plugin can be used to
                  persist key-value data to disk on each platform Flutter supports.

`shared_preferences`
This recipe uses the following steps:

1. Add the dependency.
1. Save data.
1. Read data.
1. Remove data.

## 1. Add the dependency

Before starting, add the[shared_preferences](https://pub.dev/packages/shared_preferences)package as a dependency.

`shared_preferences`
To add the`shared_preferences`package as a dependency,
                  run`flutter pub add`:

`shared_preferences`
`flutter pub add`
`flutter pub add shared_preferences`
## 2. Save data

To persist data, use the setter methods provided by the`SharedPreferences`class. Setter methods are available for
                  various primitive types, such as`setInt`,`setBool`, and`setString`.

`SharedPreferences`
`setInt`
`setBool`
`setString`
Setter methods do two things: First, synchronously update the
                  key-value pair in memory. Then, persist the data to disk.

`// Load and obtain the shared preferences for this app.
final prefs = await SharedPreferences.getInstance();
​
// Save the counter value to persistent storage under the 'counter' key.
await prefs.setInt('counter', counter);`
## 3. Read data

To read data, use the appropriate getter method provided by the`SharedPreferences`class. For each setter there is a corresponding getter.
                  For example, you can use the`getInt`,`getBool`, and`getString`methods.

`SharedPreferences`
`getInt`
`getBool`
`getString`
`final prefs = await SharedPreferences.getInstance();
​
// Try reading the counter value from persistent storage.
// If not present, null is returned, so default to 0.
final counter = prefs.getInt('counter') ?? 0;`
Note that the getter methods throw an exception if the persisted value
                  has a different type than the getter method expects.

## 4. Remove data

To delete data, use the`remove()`method.

`remove()`
`final prefs = await SharedPreferences.getInstance();
​
// Remove the counter key-value pair from persistent storage.
await prefs.remove('counter');`
## Supported types

Although the key-value storage provided by`shared_preferences`is
                  easy and convenient to use, it has limitations:

`shared_preferences`
- Only primitive types can be used:`int`,`double`,`bool`,`String`,
                    and`List<String>`.
- It's not designed to store large amounts of data.
- There is no guarantee that data will be persisted across app restarts.

`int`
`double`
`bool`
`String`
`List<String>`
## Testing support

It's a good idea to test code that persists data using`shared_preferences`.
                  To enable this, the package provides an
                  in-memory mock implementation of the preference store.

`shared_preferences`
To set up your tests to use the mock implementation,
                  call the`setMockInitialValues`static method in
                  a`setUpAll()`method in your test files.
                  Pass in a map of key-value pairs to use as the initial values.

`setMockInitialValues`
`setUpAll()`
`SharedPreferences.setMockInitialValues(<String, Object>{'counter': 2});`
## Complete example

`import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
​
void main() => runApp(const MyApp());
​
class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Shared preferences demo',
      home: MyHomePage(title: 'Shared preferences demo'),
    );
  }
}
​
class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
​
  final String title;
​
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}
​
class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;
​
  @override
  void initState() {
    super.initState();
    _loadCounter();
  }
​
  /// Load the initial counter value from persistent storage on start,
  /// or fallback to 0 if it doesn't exist.
  Future<void> _loadCounter() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _counter = prefs.getInt('counter') ?? 0;
    });
  }
​
  /// After a click, increment the counter state and
  /// asynchronously save it to persistent storage.
  Future<void> _incrementCounter() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _counter = (prefs.getInt('counter') ?? 0) + 1;
      prefs.setInt('counter', _counter);
    });
  }
​
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('You have pushed the button this many times: '),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/persistence/key-value.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/persistence/key-value&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/persistence/key-value.md).
