> 原文链接: [https://docs.flutter.dev/cookbook/networking/web-sockets](https://docs.flutter.dev/cookbook/networking/web-sockets)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

In addition to normal HTTP requests,
                  you can connect to servers using`WebSockets`.`WebSockets`allow for two-way communication with a server
                  without polling.

`WebSockets`
`WebSockets`
In this example, connect to a[test WebSocket server](https://websocket.org/tools/websocket-echo-server/).
                  The server sends back the same message you send to it.
                  This recipe uses the following steps:

1. Connect to a WebSocket server.
1. Listen for messages from the server.
1. Send data to the server.
1. Close the WebSocket connection.

## 1. Connect to a WebSocket server

The[web_socket_channel](https://pub.dev/packages/web_socket_channel)package provides the
                  tools you need to connect to a WebSocket server.

`web_socket_channel`
The package provides a`WebSocketChannel`that allows you to both listen for messages
                  from the server and push messages to the server.

`WebSocketChannel`
In Flutter, use the following line to
                  create a`WebSocketChannel`that connects to a server:

`WebSocketChannel`
`final WebSocketChannel channel = WebSocketChannel.connect(
  Uri.parse('wss://echo.websocket.org'),
);`
## 2. Listen for messages from the server

Now that you've established a connection,
                  listen to messages from the server.

After sending a message to the test server,
                  it sends the same message back.

In this example, use a[StreamBuilder](https://api.flutter.dev/flutter/widgets/StreamBuilder-class.html)widget to listen for new messages, and a[Text](https://api.flutter.dev/flutter/widgets/Text-class.html)widget to display them.

`StreamBuilder`
`Text`
`StreamBuilder(
  stream: channel.stream,
  builder: (context, snapshot) {
    return Text(snapshot.hasData ? '${snapshot.data}' : '');
  },
),`
### How this works

The`WebSocketChannel`provides a[Stream](https://api.flutter.dev/flutter/dart-async/Stream-class.html)of messages from the server.

`WebSocketChannel`
`Stream`
The`Stream`class is a fundamental part of the`dart:async`package.
                  It provides a way to listen to async events from a data source.
                  Unlike`Future`, which returns a single async response,
                  the`Stream`class can deliver many events over time.

`Stream`
`dart:async`
`Future`
`Stream`
The[StreamBuilder](https://api.flutter.dev/flutter/widgets/StreamBuilder-class.html)widget connects to a`Stream`and asks Flutter to rebuild every time it
                  receives an event using the given`builder()`function.

`StreamBuilder`
`Stream`
`builder()`
## 3. Send data to the server

To send data to the server,`add()`messages to the`sink`provided
                  by the`WebSocketChannel`.

`add()`
`sink`
`WebSocketChannel`
`channel.sink.add('Hello!');`
### How this works

The`WebSocketChannel`provides a[StreamSink](https://api.flutter.dev/flutter/dart-async/StreamSink-class.html)to push messages to the server.

`WebSocketChannel`
`StreamSink`
The`StreamSink`class provides a general way to add sync or async
                  events to a data source.

`StreamSink`
## 4. Close the WebSocket connection

After you're done using the WebSocket, close the connection:

`channel.sink.close();`
## Complete example

`import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
​
void main() => runApp(const MyApp());
​
class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    const title = 'WebSocket Demo';
    return const MaterialApp(
      title: title,
      home: MyHomePage(title: title),
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
  final TextEditingController _controller = TextEditingController();
  final WebSocketChannel _channel = WebSocketChannel.connect(
    Uri.parse('wss://echo.websocket.org'),
  );
​
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Form(
              child: TextFormField(
                controller: _controller,
                decoration: const InputDecoration(labelText: 'Send a message'),
              ),
            ),
            const SizedBox(height: 24),
            StreamBuilder(
              stream: _channel.stream,
              builder: (context, snapshot) {
                return Text(snapshot.hasData ? '${snapshot.data}' : '');
              },
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _sendMessage,
        tooltip: 'Send message',
        child: const Icon(Icons.send),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
​
  void _sendMessage() {
    if (_controller.text.isNotEmpty) {
      _channel.sink.add(_controller.text);
    }
  }
​
  @override
  void dispose() {
    _channel.sink.close();
    _controller.dispose();
    super.dispose();
  }
}`
![Web sockets demo](https://docs.flutter.dev/assets/images/docs/cookbook/web-sockets.webp)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/web-sockets.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/cookbook/networking/web-sockets&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/cookbook/networking/web-sockets.md).
