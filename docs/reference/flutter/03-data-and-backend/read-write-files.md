> 原文链接: [https://docs.flutter.dev/cookbook/persistence/reading-writing-files](https://docs.flutter.dev/cookbook/persistence/reading-writing-files)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

In some cases, you need to read and write files to disk.
                  For example, you might need to persist data across app launches,
                  or download data from the internet and save it for later offline use.

To save files to disk on mobile or desktop apps,
                  combine the[path_provider](https://pub.dev/packages/path_provider)plugin with the[dart:io](https://api.flutter.dev/flutter/dart-io/dart-io-library.html)library.

`path_provider`
`dart:io`
This recipe uses the following steps:

1. Find the correct local path.
1. Create a reference to the file location.
1. Write data to the file.
1. Read data from the file.

To learn more, watch this Package of the Week video
                  on the`path_provider`package:

`path_provider`
## 1. Find the correct local path

This example displays a counter. When the counter changes,
                  write data on disk so you can read it again when the app loads.
                  Where should you store this data?

The[path_provider](https://pub.dev/packages/path_provider)package
                  provides a platform-agnostic way to access commonly used locations on the
                  device's file system. The plugin currently supports access to
                  two file system locations:

`path_provider`
A temporary directory (cache) that the system can
                      clear at any time. On iOS, this corresponds to the[NSCachesDirectory](https://developer.apple.com/documentation/foundation/nssearchpathdirectory/nscachesdirectory). On Android, this is the value that[getCacheDir()](https://developer.android.com/reference/android/content/Context#getCacheDir())returns.

`NSCachesDirectory`
`getCacheDir()`
A directory for the app to store files that only
                      it can access. The system clears the directory only when the app
                      is deleted.
                      On iOS, this corresponds to the`NSDocumentDirectory`.
                      On Android, this is the`AppData`directory.

`NSDocumentDirectory`
`AppData`
This example stores information in the documents directory.
                  You can find the path to the documents directory as follows:

`import 'package:path_provider/path_provider.dart';
  // ···
  Future<String> get _localPath async {
    final directory = await getApplicationDocumentsDirectory();
​
    return directory.path;
  }`
## 2. Create a reference to the file location

Once you know where to store the file, create a reference to the
                  file's full location. You can use the[File](https://api.flutter.dev/flutter/dart-io/File-class.html)class from the[dart:io](https://api.flutter.dev/flutter/dart-io/dart-io-library.html)library to achieve this.

`File`
`dart:io`
`Future<File> get _localFile async {
  final path = await _localPath;
  return File('$path/counter.txt');
}`
## 3. Write data to the file

Now that you have a`File`to work with,
                  use it to read and write data.
                  First, write some data to the file.
                  The counter is an integer, but is written to the
                  file as a string using the`'$counter'`syntax.

`File`
`'$counter'`
`Future<File> writeCounter(int counter) async {
  final file = await _localFile;
​
  // Write the file
  return file.writeAsString('$counter');
}`
## 4. Read data from the file

Now that you have some data on disk, you can read it.
                  Once again, use the`File`class.

`File`
`Future<int> readCounter() async {
  try {
    final file = await _localFile;
​
    // Read the file
    final contents = await file.readAsString();
​
    return int.parse(contents);
  } catch (e) {
    // If encountering an error, return 0
    return 0;
  }
}`
## Complete example

`import 'dart:async';
import 'dart:io';
​
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
​
void main() {
  runApp(
    MaterialApp(
      title: 'Reading and Writing Files',
      home: FlutterDemo(storage: CounterStorage()),
    ),
  );
}
​
class CounterStorage {
  Future<String> get _localPath async {
    final directory = await getApplicationDocumentsDirectory();
​
    return directory.path;
  }
​
  Future<File> get _localFile async {
    final path = await _localPath;
    return File('$path/counter.txt');
  }
​
  Future<int> readCounter() async {
    try {
      final file = await _localFile;
​
      // Read the file
      final contents = await file.readAsString();
​
      return int.parse(contents);
    } catch (e) {
      // If encountering an error, return 0
      return 0;
    }
  }
​
  Future<File> writeCounter(int counter) async {
    final file = await _localFile;
​
    // Write the file
    return file.writeAsString('$counter');
  }
​
}
​
class FlutterDemo extends StatefulWidget {
  const FlutterDemo({super.key, required this.storage});
​
  final CounterStorage storage;
​
  @override
  State<FlutterDemo> createState() => _FlutterDemoState();
}
​
class _FlutterDemoState extends State<FlutterDemo> {
  int _counter = 0;
​
  @override
  void initState() {
    super.initState();
    widget.storage.readCounter().then((value) {
      setState(() {
        _counter = value;
      });
    });
  }
​
  Future<File> _incrementCounter() {
    setState(() {
      _counter++;
    });
​
    // Write the variable as a string to the file.
    return widget.storage.writeCounter(_counter);
  }
​
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Reading and Writing Files')),
      body: Center(
        child: Text('Button tapped $_counter time${_counter == 1 ? '' : 's'}.'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/persistence/reading-writing-files.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/persistence/reading-writing-files&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/persistence/reading-writing-files.md).
