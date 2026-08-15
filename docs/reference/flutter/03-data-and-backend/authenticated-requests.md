> 原文链接: [https://docs.flutter.dev/cookbook/networking/authenticated-requests](https://docs.flutter.dev/cookbook/networking/authenticated-requests)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

To fetch data from most web services, you need to provide
                  authorization. There are many ways to do this,
                  but perhaps the most common uses the`Authorization`HTTP header.

`Authorization`
## Add authorization headers

The[http](https://pub.dev/packages/http)package provides a
                  convenient way to add headers to your requests.
                  Alternatively, use the[HttpHeaders](https://api.dart.dev/dart-io/HttpHeaders-class.html)class from the`dart:io`library.

`http`
`HttpHeaders`
`dart:io`
`final response = await http.get(
  Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
  // Send authorization headers to the backend.
  headers: {HttpHeaders.authorizationHeader: 'Basic your_api_token_here'},
);`
## Complete example

This example builds upon the[Fetching data from the internet](https://docs.flutter.dev/cookbook/networking/fetch-data)recipe.

`import 'dart:async';
import 'dart:convert';
import 'dart:io';
​
import 'package:http/http.dart' as http;
​
Future<Album> fetchAlbum() async {
  final response = await http.get(
    Uri.parse('https://jsonplaceholder.typicode.com/albums/1'),
    // Send authorization headers to the backend.
    headers: {HttpHeaders.authorizationHeader: 'Basic your_api_token_here'},
  );
  final responseJson = jsonDecode(response.body) as Map<String, dynamic>;
​
  return Album.fromJson(responseJson);
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
}`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/authenticated-requests.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/networking/authenticated-requests&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/authenticated-requests.md).
