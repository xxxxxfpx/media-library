> 原文链接: [https://docs.flutter.dev/cookbook/networking/fetch-data](https://docs.flutter.dev/cookbook/networking/fetch-data)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Fetching data from the internet is necessary for most apps.
                  Luckily, Dart and Flutter provide tools, such as the`http`package, for this type of work.

`http`
This recipe uses the following steps:

1. Add the`http`package.
1. Make a network request using the`http`package.
1. Convert the response into a custom Dart object.
1. Fetch and display the data with Flutter.

`http`
`http`
## 1. Add thehttppackage

`http`
The[http](https://pub.dev/packages/http)package provides the
                  simplest way to fetch data from the internet.

`http`
To add the`http`package as a dependency,
                  run`flutter pub add`:

`http`
`flutter pub add`
`$ flutter pub add http`
Import the http package.

`import 'package:http/http.dart' as http;`
If you are deploying to Android, edit your`AndroidManifest.xml`file to
                  add the Internet permission.

`AndroidManifest.xml`
`<!-- Required to fetch data from the internet. -->
<uses-permission android:name="android.permission.INTERNET" />`
Likewise, if you are deploying to macOS, edit your`macos/Runner/DebugProfile.entitlements`and`macos/Runner/Release.entitlements`files to include the network client entitlement.

`macos/Runner/DebugProfile.entitlements`
`macos/Runner/Release.entitlements`
`<!-- Required to fetch data from the internet. -->
<key>com.apple.security.network.client</key>
<true/>`
## 2. Make a network request

This recipe covers how to fetch a sample album from the[JSONPlaceholder](https://jsonplaceholder.typicode.com/)using the[http.get()](https://pub.dev/documentation/http/latest/http/get.html)method.

`http.get()`
`Future<http.Response> fetchAlbum() {
  return http.get(Uri.parse('https://jsonplaceholder.typicode.com/albums/1'));
}`
The`http.get()`method returns a`Future`that contains a`Response`.

`http.get()`
`Future`
`Response`
- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)is a core Dart class for working with
                    async operations. A Future object represents a potential
                    value or error that will be available at some time in the future.
- The`http.Response`class contains the data received from a successful
                    http call.

`Future`
`http.Response`
## 3. Convert the response into a custom Dart object

While it's easy to make a network request, working with a raw`Future<http.Response>`isn't very convenient.
                  To make your life easier,
                  convert the`http.Response`into a Dart object.

`Future<http.Response>`
`http.Response`
### Create anAlbumclass

`Album`
First, create an`Album`class that contains the data from the
                  network request. It includes a factory constructor that
                  creates an`Album`from JSON.

`Album`
`Album`
Converting JSON using[pattern matching](https://dart.dev/language/patterns)is only one option.
                  For more information, see the full article on[JSON and serialization](https://docs.flutter.dev/data-and-backend/serialization/json).

`class Album {
  final int userId;
  final int id;
  final String title;
​
  const Album({required this.userId, required this.id, required this.title});
​
  factory Album.fromJson(Map<String, dynamic> json) {
    return switch (json) {
      {'userId': int userId, 'id': int id, 'title': String title} => Album(
        userId: userId,
        id: id,
        title: title,
      ),
      _ => throw const FormatException('Failed to load album.'),
    };
  }
}`
### Convert thehttp.Responseto anAlbum

`http.Response`
`Album`
Now, use the following steps to update the`fetchAlbum()`function to return a`Future<Album>`:

`fetchAlbum()`
`Future<Album>`
1. Convert the response body into a JSON`Map`with
                    the`dart:convert`package.
1. If the server does return an OK response with a status code of
                    200, then convert the JSON`Map`into an`Album`using the`fromJson()`factory method.
1. If the server does not return an OK response with a status code of 200,
                    then throw an exception.
                    (Even in the case of a "404 Not Found" server response,
                    throw an exception. Do not return`null`.
                    This is important when examining
                    the data in`snapshot`, as shown below.)

`Map`
`dart:convert`
`Map`
`Album`
`fromJson()`
`null`
`snapshot`
`Future<Album> fetchAlbum() async {
  final response = await http.get(
    Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
    headers: {'Accept': 'application/json'},
  );
​
  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Album.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load album');
  }
}`
Hooray!
                  Now you've got a function that fetches an album from the internet.

## 4. Fetch the data

Call the`fetchAlbum()`method in either the[initState()](https://api.flutter.dev/flutter/widgets/State/initState.html)or[didChangeDependencies()](https://api.flutter.dev/flutter/widgets/State/didChangeDependencies.html)methods.

`fetchAlbum()`
`initState()`
`didChangeDependencies()`
The`initState()`method is called exactly once and then never again.
                  If you want to have the option of reloading the API in response to an[InheritedWidget](https://api.flutter.dev/flutter/widgets/InheritedWidget-class.html)changing, put the call into the`didChangeDependencies()`method.
                  See[State](https://api.flutter.dev/flutter/widgets/State-class.html)for more details.

`initState()`
`InheritedWidget`
`didChangeDependencies()`
`State`
`class _MyAppState extends State<MyApp> {
  late Future<Album> futureAlbum;
​
  @override
  void initState() {
    super.initState();
    futureAlbum = fetchAlbum();
  }
  // ···
}`
This Future is used in the next step.

## 5. Display the data

To display the data on screen, use the[FutureBuilder](https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html)widget.
                  The`FutureBuilder`widget comes with Flutter and
                  makes it easy to work with asynchronous data sources.

`FutureBuilder`
`FutureBuilder`
You must provide two parameters:

1. The`Future`you want to work with.
                    In this case, the future returned from
                    the`fetchAlbum()`function.
1. A`builder`function that tells Flutter
                    what to render, depending on the
                    state of the`Future`: loading, success, or error.

`Future`
`fetchAlbum()`
`builder`
`Future`
Note that`snapshot.hasData`only returns`true`when the snapshot contains a non-null data value.

`snapshot.hasData`
`true`
Because`fetchAlbum`can only return non-null values,
                  the function should throw an exception
                  even in the case of a "404 Not Found" server response.
                  Throwing an exception sets the`snapshot.hasError`to`true`which can be used to display an error message.

`fetchAlbum`
`snapshot.hasError`
`true`
Otherwise, the spinner will be displayed.

`FutureBuilder<Album>(
  future: futureAlbum,
  builder: (context, snapshot) {
    if (snapshot.hasData) {
      return Text(snapshot.data!.title);
    } else if (snapshot.hasError) {
      return Text('${snapshot.error}');
    }
​
    // By default, show a loading spinner.
    return const CircularProgressIndicator();
  },
)`
## Why is fetchAlbum() called in initState()?

Although it's convenient,
                  it's not recommended to put an API call in a`build()`method.

`build()`
Flutter calls the`build()`method every time it needs
                  to change anything in the view,
                  and this happens surprisingly often.
                  The`fetchAlbum()`method, if placed inside`build()`, is repeatedly
                  called on each rebuild causing the app to slow down.

`build()`
`fetchAlbum()`
`build()`
Storing the`fetchAlbum()`result in a state variable ensures that
                  the`Future`is executed only once and then cached for subsequent
                  rebuilds.

`fetchAlbum()`
`Future`
## Testing

For information on how to test this functionality,
                  see the following recipes:

- [Introduction to unit testing](https://docs.flutter.dev/cookbook/testing/unit/introduction)
- [Mock dependencies using Mockito](https://docs.flutter.dev/cookbook/testing/unit/mocking)

## Complete example

`import 'dart:async';
import 'dart:convert';
​
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
​
Future<Album> fetchAlbum() async {
  final response = await http.get(
    Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
    headers: {'Accept': 'application/json'},
  );
​
  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Album.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load album');
  }
}
​
class Album {
  final int userId;
  final int id;
  final String title;
​
  const Album({required this.userId, required this.id, required this.title});
​
  factory Album.fromJson(Map<String, dynamic> json) {
    return switch (json) {
      {'userId': int userId, 'id': int id, 'title': String title} => Album(
        userId: userId,
        id: id,
        title: title,
      ),
      _ => throw const FormatException('Failed to load album.'),
    };
  }
}
​
void main() => runApp(const MyApp());
​
class MyApp extends StatefulWidget {
  const MyApp({super.key});
​
  @override
  State<MyApp> createState() => _MyAppState();
}
​
class _MyAppState extends State<MyApp> {
  late Future<Album> futureAlbum;
​
  @override
  void initState() {
    super.initState();
    futureAlbum = fetchAlbum();
  }
​
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fetch Data Example',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Fetch Data Example')),
        body: Center(
          child: FutureBuilder<Album>(
            future: futureAlbum,
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                return Text(snapshot.data!.title);
              } else if (snapshot.hasError) {
                return Text('${snapshot.error}');
              }
​
              // By default, show a loading spinner.
              return const CircularProgressIndicator();
            },
          ),
        ),
      ),
    );
  }
​
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/fetch-data.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/networking/fetch-data&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/fetch-data.md).
