> 原文链接: [https://docs.flutter.dev/cookbook/networking/update-data](https://docs.flutter.dev/cookbook/networking/update-data)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Updating data over the internet is necessary for most apps.
                  The`http`package has got that covered!

`http`
This recipe uses the following steps:

1. Add the`http`package.
1. Update data over the internet using the`http`package.
1. Convert the response into a custom Dart object.
1. Get the data from the internet.
1. Update the existing`title`from user input.
1. Update and display the response on screen.

`http`
`http`
`title`
## 1. Add thehttppackage

`http`
To add the`http`package as a dependency,
                  run`flutter pub add`:

`http`
`flutter pub add`
`$ flutter pub add http`
Import the`http`package.

`http`
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
## 2. Updating data over the internet using thehttppackage

`http`
This recipe covers how to update an album title to the[JSONPlaceholder](https://jsonplaceholder.typicode.com/)using the[http.put()](https://pub.dev/documentation/http/latest/http/put.html)method.

`http.put()`
`Future<http.Response> updateAlbum(String title) {
  return http.put(
    Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{'title': title}),
  );
}`
The`http.put()`method returns a`Future`that contains a`Response`.

`http.put()`
`Future`
`Response`
- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)is a core Dart class for working with
                    async operations. A`Future`object represents a potential
                    value or error that will be available at some time in the future.
- The`http.Response`class contains the data received from a successful
                    http call.
- The`updateAlbum()`method takes an argument,`title`,
                    which is sent to the server to update the`Album`.

`Future`
`Future`
`http.Response`
`updateAlbum()`
`title`
`Album`
## 3. Convert thehttp.Responseto a custom Dart object

`http.Response`
While it's easy to make a network request,
                  working with a raw`Future<http.Response>`isn't very convenient. To make your life easier,
                  convert the`http.Response`into a Dart object.

`Future<http.Response>`
`http.Response`
### Create an Album class

First, create an`Album`class that contains the data from the
                  network request. It includes a factory constructor that
                  creates an`Album`from JSON.

`Album`
`Album`
Converting JSON with[pattern matching](https://dart.dev/language/patterns)is only one option.
                  For more information, see the full article on[JSON and serialization](https://docs.flutter.dev/data-and-backend/serialization/json).

`class Album {
  final int id;
  final String title;
​
  const Album({required this.id, required this.title});
​
  factory Album.fromJson(Map<String, dynamic> json) {
    return switch (json) {
      {'id': int id, 'title': String title} => Album(id: id, title: title),
      _ => throw const FormatException('Failed to load album.'),
    };
  }
}`
### Convert thehttp.Responseto anAlbum

`http.Response`
`Album`
Now, use the following steps to update the`updateAlbum()`function to return a`Future<Album>`:

`updateAlbum()`
`Future<Album>`
1. Convert the response body into a JSON`Map`with the`dart:convert`package.
1. If the server returns an`UPDATED`response with a status
                    code of 200, then convert the JSON`Map`into an`Album`using the`fromJson()`factory method.
1. If the server doesn't return an`UPDATED`response with a
                    status code of 200, then throw an exception.
                    (Even in the case of a "404 Not Found" server response,
                    throw an exception. Do not return`null`.
                    This is important when examining
                    the data in`snapshot`, as shown below.)

`Map`
`dart:convert`
`UPDATED`
`Map`
`Album`
`fromJson()`
`UPDATED`
`null`
`snapshot`
`Future<Album> updateAlbum(String title) async {
  final response = await http.put(
    Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{'title': title}),
  );
​
  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Album.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to update album.');
  }
}`
Hooray!
                  Now you've got a function that updates the title of an album.

### Get the data from the internet

Get the data from internet before you can update it.
                  For a complete example, see the[Fetch data](https://docs.flutter.dev/cookbook/networking/fetch-data)recipe.

`Future<Album> fetchAlbum() async {
  final response = await http.get(
    Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
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
Ideally, you will use this method to set`_futureAlbum`during`initState`to fetch
                  the data from the internet.

`_futureAlbum`
`initState`
## 4. Update the existing title from user input

Create a`TextField`to enter a title and a`ElevatedButton`to update the data on server.
                  Also define a`TextEditingController`to
                  read the user input from a`TextField`.

`TextField`
`ElevatedButton`
`TextEditingController`
`TextField`
When the`ElevatedButton`is pressed,
                  the`_futureAlbum`is set to the value returned by`updateAlbum()`method.

`ElevatedButton`
`_futureAlbum`
`updateAlbum()`
`Column(
  mainAxisAlignment: MainAxisAlignment.center,
  children: <Widget>[
    Padding(
      padding: const EdgeInsets.all(8),
      child: TextField(
        controller: _controller,
        decoration: const InputDecoration(hintText: 'Enter Title'),
      ),
    ),
    ElevatedButton(
      onPressed: () {
        setState(() {
          _futureAlbum = updateAlbum(_controller.text);
        });
      },
      child: const Text('Update Data'),
    ),
  ],
);`
On pressing the**Update Data**button, a network request
                  sends the data in the`TextField`to the server as a`PUT`request.
                  The`_futureAlbum`variable is used in the next step.

`TextField`
`PUT`
`_futureAlbum`
## 5. Display the response on screen

To display the data on screen, use the[FutureBuilder](https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html)widget.
                  The`FutureBuilder`widget comes with Flutter and
                  makes it easy to work with async data sources.
                  You must provide two parameters:

`FutureBuilder`
`FutureBuilder`
1. The`Future`you want to work with. In this case,
                    the future returned from the`updateAlbum()`function.
1. A`builder`function that tells Flutter what to render,
                    depending on the state of the`Future`: loading,
                    success, or error.

`Future`
`updateAlbum()`
`builder`
`Future`
Note that`snapshot.hasData`only returns`true`when
                  the snapshot contains a non-null data value.
                  This is why the`updateAlbum`function should throw an exception
                  even in the case of a "404 Not Found" server response.
                  If`updateAlbum`returns`null`then`CircularProgressIndicator`will display indefinitely.

`snapshot.hasData`
`true`
`updateAlbum`
`updateAlbum`
`null`
`CircularProgressIndicator`
`FutureBuilder<Album>(
  future: _futureAlbum,
  builder: (context, snapshot) {
    if (snapshot.hasData) {
      return Text(snapshot.data!.title);
    } else if (snapshot.hasError) {
      return Text('${snapshot.error}');
    }
​
    return const CircularProgressIndicator();
  },
);`
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
Future<Album> updateAlbum(String title) async {
  final response = await http.put(
    Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{'title': title}),
  );
​
  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Album.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to update album.');
  }
}
​
class Album {
  final int id;
  final String title;
​
  const Album({required this.id, required this.title});
​
  factory Album.fromJson(Map<String, dynamic> json) {
    return switch (json) {
      {'id': int id, 'title': String title} => Album(id: id, title: title),
      _ => throw const FormatException('Failed to load album.'),
    };
  }
}
​
void main() {
  runApp(const MyApp());
}
​
class MyApp extends StatefulWidget {
  const MyApp({super.key});
​
  @override
  State<MyApp> createState() {
    return _MyAppState();
  }
}
​
class _MyAppState extends State<MyApp> {
  final TextEditingController _controller = TextEditingController();
  late Future<Album> _futureAlbum;
​
  @override
  void initState() {
    super.initState();
    _futureAlbum = fetchAlbum();
  }
​
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Update Data Example',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Update Data Example')),
        body: Container(
          alignment: Alignment.center,
          padding: const EdgeInsets.all(8),
          child: FutureBuilder<Album>(
            future: _futureAlbum,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                if (snapshot.hasData) {
                  return Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text(snapshot.data!.title),
                      TextField(
                        controller: _controller,
                        decoration: const InputDecoration(
                          hintText: 'Enter Title',
                        ),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          setState(() {
                            _futureAlbum = updateAlbum(_controller.text);
                          });
                        },
                        child: const Text('Update Data'),
                      ),
                    ],
                  );
                } else if (snapshot.hasError) {
                  return Text('${snapshot.error}');
                }
              }
​
              return const CircularProgressIndicator();
            },
          ),
        ),
      ),
    );
  }
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/update-data.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/networking/update-data&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/update-data.md).
