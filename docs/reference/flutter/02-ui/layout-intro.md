> 原文链接: [https://docs.flutter.dev/ui/layout](https://docs.flutter.dev/ui/layout)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## Overview

The core of Flutter's layout mechanism is widgets.
                  In Flutter, almost everything is a widget—even
                  layout models are widgets. The images, icons,
                  and text that you see in a Flutter app are all widgets.
                  But things you don't see are also widgets,
                  such as the rows, columns, and grids that arrange,
                  constrain, and align the visible widgets.
                  You create a layout by composing widgets to build more
                  complex widgets.

## Conceptual example

In the following example, the first screenshot displays
                  three icons with labels and the second screenshot includes
                  the visual layout for rows and columns. In the second
                  screenshot,`debugPaintSizeEnabled`is set to`true`so you
                  can see the visual layout.

`debugPaintSizeEnabled`
`true`
Here's a diagram of the widget tree for the previous
                  example:

Most of this should look as you might expect, but you might be wondering
                  about the containers (shown in pink).[Container](https://api.flutter.dev/flutter/widgets/Container-class.html)is a widget class
                  that allows you to customize its child widget. Use a`Container`when
                  you want to add padding, margins, borders, or background color,
                  to name some of its capabilities.

`Container`
`Container`
Each[Text](https://api.flutter.dev/flutter/widgets/Text-class.html)widget is placed in a`Container`to add margins. The entire[Row](https://api.flutter.dev/flutter/widgets/Row-class.html)is also placed in a`Container`to add padding around the row.

`Text`
`Container`
`Row`
`Container`
The rest of the UI is controlled by properties.
                  Set an[Icon](https://api.flutter.dev/flutter/material/Icons-class.html)'s color using its`color`property.
                  Use the`Text.style`property to set the font, its color, weight, and so on.
                  Columns and rows have properties that allow you to specify how their
                  children are aligned vertically or horizontally, and how much space
                  the children should occupy.

`Icon`
`color`
`Text.style`
## Lay out a widget

How do you lay out a single widget in Flutter? This section
                  shows you how to create and display a simple widget.
                  It also shows the entire code for a simple Hello World app.

In Flutter, it takes only a few steps to put text, an icon,
                  or an image on the screen.

### 1. Select a layout widget

Choose from a variety of[layout widgets](https://docs.flutter.dev/ui/widgets/layout)based
                  on how you want to align or constrain a visible widget,
                  as these characteristics are typically passed on to the
                  contained widget.

For example, you could use the[Center](https://api.flutter.dev/flutter/widgets/Center-class.html)layout widget to center a visible widget
                  horizontally and vertically:

`Center`
`Center(
  // Content to be centered here.
)`
### 2. Create a visible widget

Choose a[visible widget](https://docs.flutter.dev/ui/widgets)for your app to contain
                  visible elements, such as[text](https://api.flutter.dev/flutter/widgets/Text-class.html),[images](https://api.flutter.dev/flutter/widgets/Image-class.html), or[icons](https://api.flutter.dev/flutter/material/Icons-class.html).

For example, you could use the[Text](https://api.flutter.dev/flutter/widgets/Text-class.html)widget display
                  some text:

`Text`
`Text('Hello World')`
### 3. Add the visible widget to the layout widget

All layout widgets have either of the following:

- A`child`property if they take a single child—for example,`Center`or`Container`
- A`children`property if they take a list of widgets—for example,`Row`,`Column`,`ListView`, or`Stack`.

`child`
`Center`
`Container`
`children`
`Row`
`Column`
`ListView`
`Stack`
Add the`Text`widget to the`Center`widget:

`Text`
`Center`
`const Center(
  child: Text('Hello World'),
),`
### 4. Add the layout widget to the page

A Flutter app is itself a widget, and most widgets have a[build()](https://api.flutter.dev/flutter/widgets/StatelessWidget/build.html)method. Instantiating and returning a widget in the app's`build()`method
                  displays the widget.

`build()`
`build()`
- [Standard apps](#0-tab-panel)
- [Material apps](#1-tab-panel)
- [Cupertino apps](#2-tab-panel)

For a general app, you can add the`Container`widget to
                        the app's`build()`method:

`Container`
`build()`
`class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(color: Colors.white),
      child: const Center(
        child: Text(
          'Hello World',
          textDirection: TextDirection.ltr,
          style: TextStyle(fontSize: 32, color: Colors.black87),
        ),
      ),
    );
  }
}`
By default, a general app doesn't include an`AppBar`,
                        title, or background color. If you want these features in a
                        general app, you have to build them yourself. This app
                        changes the background color to white and the text to
                        dark grey to mimic a Material app.

`AppBar`
For a`Material`app, you can use a[Scaffold](https://api.flutter.dev/flutter/material/Scaffold-class.html)widget;
                        it provides a default banner, background color,
                        and has API for adding drawers, snack bars, and bottom sheets.
                        Then you can add the`Center`widget directly to the`body`property for the home page.

`Material`
`Scaffold`
`Center`
`body`
`class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    const String appTitle = 'Flutter layout demo';
    return MaterialApp(
      title: appTitle,
      home: Scaffold(
        appBar: AppBar(title: const Text(appTitle)),
        body: const Center(
          child: Text('Hello World'),
        ),
      ),
    );
  }
}`
To create a`Cupertino`app,
                        use the`CupertinoApp`and[CupertinoPageScaffold](https://api.flutter.dev/flutter/cupertino/CupertinoPageScaffold-class.html)widgets.

`Cupertino`
`CupertinoApp`
`CupertinoPageScaffold`
Unlike`Material`, it doesn't provide a default banner or background color.
                        You need to set these yourself.

`Material`

To set default colors, pass in a configured[CupertinoThemeData](https://api.flutter.dev/flutter/cupertino/CupertinoThemeData-class.html)to your app's`theme`property.

`CupertinoThemeData`
`theme`
To add an iOS-styled navigation bar to the top of your app, add a[CupertinoNavigationBar](https://api.flutter.dev/flutter/cupertino/CupertinoNavigationBar-class.html)widget to the`navigationBar`property of your scaffold.
                            You can use the colors that[CupertinoColors](https://api.flutter.dev/flutter/cupertino/CupertinoColors-class.html)provides to
                            configure your widgets to match iOS design.

`CupertinoNavigationBar`
`navigationBar`
`CupertinoColors`
To lay out the body of your app, set the`child`property of your scaffold
                            with the desired widget as its value, like`Center`or`Column`.

`child`
`Center`
`Column`
To learn what other UI components you can add, check out the[Cupertino library](https://api.flutter.dev/flutter/cupertino/cupertino-library.html).

`class MyApp extends StatelessWidget {
  const MyApp({super.key});
​
  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      title: 'Flutter layout demo',
      theme: CupertinoThemeData(
        brightness: Brightness.light,
        primaryColor: CupertinoColors.systemBlue,
      ),
      home: CupertinoPageScaffold(
        navigationBar: CupertinoNavigationBar(
          backgroundColor: CupertinoColors.systemGrey,
          middle: Text('Flutter layout demo'),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [Text('Hello World')],
          ),
        ),
      ),
    );
  }
}`
### 5. Run your app

After you've added your widgets, run your app. When you run
the app, you should see*Hello World*.

App source code:

- [Material app](https://github.com/flutter/website/tree/main/examples/layout/base)
- [Non-Material app](https://github.com/flutter/website/tree/main/examples/layout/non_material)

---

## Lay out multiple widgets vertically and horizontally

One of the most common layout patterns is to arrange
                  widgets vertically or horizontally. You can use a`Row`widget to arrange widgets horizontally,
                  and a`Column`widget to arrange widgets vertically.

`Row`
`Column`
To create a row or column in Flutter, you add a list of children
                  widgets to a[Row](https://api.flutter.dev/flutter/widgets/Row-class.html)or[Column](https://api.flutter.dev/flutter/widgets/Column-class.html)widget. In turn,
                  each child can itself be a row or column, and so on.
                  The following example shows how it is possible to nest rows or
                  columns inside of rows or columns.

`Row`
`Column`
This layout is organized as a`Row`. The row contains two children:
                  a column on the left, and an image on the right:

`Row`
The left column's widget tree nests rows and columns.

You'll implement some of Pavlova's layout code in[Nesting rows and columns](#nesting-rows-and-columns).

### Aligning widgets

You control how a row or column aligns its children using the`mainAxisAlignment`and`crossAxisAlignment`properties.
                  For a row, the main axis runs horizontally and the cross axis runs
                  vertically. For a column, the main axis runs vertically and the cross
                  axis runs horizontally.

`mainAxisAlignment`
`crossAxisAlignment`
The[MainAxisAlignment](https://api.flutter.dev/flutter/rendering/MainAxisAlignment.html)and[CrossAxisAlignment](https://api.flutter.dev/flutter/rendering/CrossAxisAlignment.html)enums offer a variety of constants for controlling alignment.

`MainAxisAlignment`
`CrossAxisAlignment`
In the following example, each of the 3 images is 100 pixels wide.
                  The render box (in this case, the entire screen)
                  is more than 300 pixels wide, so setting the main axis
                  alignment to`spaceEvenly`divides the free horizontal
                  space evenly between, before, and after each image.

`spaceEvenly`
`Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  children: [
    Image.asset('images/pic1.jpg'),
    Image.asset('images/pic2.jpg'),
    Image.asset('images/pic3.jpg'),
  ],
);`
**App source:**[row_column](https://github.com/flutter/website/tree/main/examples/layout/row_column)

Columns work the same way as rows. The following example shows a column
                  of 3 images, each is 100 pixels high. The height of the render box
                  (in this case, the entire screen) is more than 300 pixels, so
                  setting the main axis alignment to`spaceEvenly`divides the free vertical
                  space evenly between, above, and below each image.

`spaceEvenly`
`Column(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  children: [
    Image.asset('images/pic1.jpg'),
    Image.asset('images/pic2.jpg'),
    Image.asset('images/pic3.jpg'),
  ],
);`
**App source:**[row_column](https://github.com/flutter/website/tree/main/examples/layout/row_column)

### Sizing widgets

When a layout is too large to fit a device, a yellow
                  and black striped pattern appears along the affected edge.
                  Here is an[example](https://github.com/flutter/website/tree/main/examples/layout/sizing)of a row that is too wide:

Widgets can be sized to fit within a row or column by using the[Expanded](https://api.flutter.dev/flutter/widgets/Expanded-class.html)widget. To fix the previous example where the
                  row of images is too wide for its render box,
                  wrap each image with an`Expanded`widget.

`Expanded`
`Expanded`
`Row(
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Expanded(child: Image.asset('images/pic1.jpg')),
    Expanded(child: Image.asset('images/pic2.jpg')),
    Expanded(child: Image.asset('images/pic3.jpg')),
  ],
);`
**App source:**[sizing](https://github.com/flutter/website/tree/main/examples/layout/sizing)

Perhaps you want a widget to occupy twice as much space as its
                  siblings. For this, use the`Expanded`widget`flex`property,
                  an integer that determines the flex factor for a widget.
                  The default flex factor is 1. The following code sets
                  the flex factor of the middle image to 2:

`Expanded`
`flex`
`Row(
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Expanded(child: Image.asset('images/pic1.jpg')),
    Expanded(flex: 2, child: Image.asset('images/pic2.jpg')),
    Expanded(child: Image.asset('images/pic3.jpg')),
  ],
);`
**App source:**[sizing](https://github.com/flutter/website/tree/main/examples/layout/sizing)

### Packing widgets

By default, a row or column occupies as much space along its main axis
                  as possible, but if you want to pack the children closely together,
                  set its`mainAxisSize`to`MainAxisSize.min`. The following example
                  uses this property to pack the star icons together.

`mainAxisSize`
`MainAxisSize.min`
`Row(
  mainAxisSize: MainAxisSize.min,
  children: [
    Icon(Icons.star, color: Colors.green[500]),
    Icon(Icons.star, color: Colors.green[500]),
    Icon(Icons.star, color: Colors.green[500]),
    const Icon(Icons.star, color: Colors.black),
    const Icon(Icons.star, color: Colors.black),
  ],
)`
**App source:**[pavlova](https://github.com/flutter/website/tree/main/examples/layout/pavlova)

### Nesting rows and columns

The layout framework allows you to nest rows and columns
                  inside of rows and columns as deeply as you need.
                  Let's look at the code for the outlined
                  section of the following layout:

The outlined section is implemented as two rows. The ratings row contains
                  five stars and the number of reviews. The icons row contains three
                  columns of icons and text.

The widget tree for the ratings row:

The`ratings`variable creates a row containing a smaller row
                  of 5-star icons, and text:

`ratings`
`final stars = Row(
  mainAxisSize: MainAxisSize.min,
  children: [
    Icon(Icons.star, color: Colors.green[500]),
    Icon(Icons.star, color: Colors.green[500]),
    Icon(Icons.star, color: Colors.green[500]),
    const Icon(Icons.star, color: Colors.black),
    const Icon(Icons.star, color: Colors.black),
  ],
);
​
final ratings = Container(
  padding: const EdgeInsets.all(20),
  child: Row(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: [
      stars,
      const Text(
        '170 Reviews',
        style: TextStyle(
          color: Colors.black,
          fontWeight: FontWeight.w800,
          fontFamily: 'Roboto',
          letterSpacing: 0.5,
          fontSize: 20,
        ),
      ),
    ],
  ),
);`
The icons row, below the ratings row, contains 3 columns;
                  each column contains an icon and two lines of text,
                  as you can see in its widget tree:

The`iconList`variable defines the icons row:

`iconList`
`const descTextStyle = TextStyle(
  color: Colors.black,
  fontWeight: FontWeight.w800,
  fontFamily: 'Roboto',
  letterSpacing: 0.5,
  fontSize: 18,
  height: 2,
);
​
// DefaultTextStyle.merge() allows you to create a default text
// style that is inherited by its child and all subsequent children.
final iconList = DefaultTextStyle.merge(
  style: descTextStyle,
  child: Container(
    padding: const EdgeInsets.all(20),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        Column(
          children: [
            Icon(Icons.kitchen, color: Colors.green[500]),
            const Text('PREP:'),
            const Text('25 min'),
          ],
        ),
        Column(
          children: [
            Icon(Icons.timer, color: Colors.green[500]),
            const Text('COOK:'),
            const Text('1 hr'),
          ],
        ),
        Column(
          children: [
            Icon(Icons.restaurant, color: Colors.green[500]),
            const Text('FEEDS:'),
            const Text('4-6'),
          ],
        ),
      ],
    ),
  ),
);`
The`leftColumn`variable contains the ratings and icons rows,
                  as well as the title and text that describes the Pavlova:

`leftColumn`
`final leftColumn = Container(
  padding: const EdgeInsets.fromLTRB(20, 30, 20, 20),
  child: Column(children: [titleText, subTitle, ratings, iconList]),
);`
The left column is placed in a`SizedBox`to constrain its width.
                  Finally, the UI is constructed with the entire row (containing the
                  left column and the image) inside a`Card`.

`SizedBox`
`Card`
The[Pavlova image](https://pixabay.com/en/photos/pavlova)is from[Pixabay](https://pixabay.com/en/photos/pavlova).
                  You can embed an image from the net using`Image.network()`but,
                  for this example, the image is saved to an images directory in the project,
                  added to the[pubspec file](https://github.com/flutter/website/tree/main/examples/layout/pavlova/pubspec.yaml), and accessed using`Images.asset()`.
                  For more information, see[Adding assets and images](https://docs.flutter.dev/ui/assets/assets-and-images).

`Image.network()`
`Images.asset()`
`body: Center(
  child: Container(
    margin: const EdgeInsets.fromLTRB(0, 40, 0, 30),
    height: 600,
    child: Card(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 440, child: leftColumn),
          mainImage,
        ],
      ),
    ),
  ),
),`
**App source:**[pavlova](https://github.com/flutter/website/tree/main/examples/layout/pavlova)

---

## Common layout widgets

Flutter has a rich library of layout widgets.
                  Here are a few of those most commonly used.
                  The intent is to get you up and running as quickly as possible,
                  rather than overwhelm you with a complete list.
                  For information on other available widgets,
                  refer to the[Widget catalog](https://docs.flutter.dev/ui/widgets),
                  or use the Search box in the[API reference docs](https://api.flutter.dev/flutter).
                  Also, the widget pages in the API docs often make suggestions
                  about similar widgets that might better suit your needs.

The following widgets fall into two categories: standard widgets
                  from the[widgets library](https://api.flutter.dev/flutter/widgets/widgets-library.html), and specialized widgets from the[Material library](https://api.flutter.dev/flutter/material/material-library.html). Any app can use the widgets library but
                  only Material apps can use the Material Components library.

- [Standard widgets](#3-tab-panel)
- [Material widgets](#4-tab-panel)
- [Cupertino widgets](#5-tab-panel)

`Container`
Adds padding, margins, borders,
                            background color, or other decorations to a widget.

`GridView`
Lays widgets out as a scrollable grid.

`ListView`
Lays widgets out as a scrollable list.

`Stack`
Overlaps a widget on top of another.

`Scaffold`
Provides a structured layout framework
                            with slots for common Material Design app elements.

`AppBar`
Creates a horizontal bar that's typically
                            displayed at the top of a screen.

`Card`
Organizes related info into a box with
                            rounded corners and a drop shadow.

`ListTile`
Organizes up to 3 lines of text,
                            and optional leading and trailing icons, into a row.

`CupertinoPageScaffold`
Provides the basic layout structure for an iOS-style page.

`CupertinoNavigationBar`
Creates an iOS-style  navigation bar at the top of the screen.

`CupertinoSegmentedControl`
Creates a segmented control for selecting.

`CupertinoTabBar`
`CupertinoTabScaffold`
Creates the characteristic iOS bottom tab bar.

### Container

Many layouts make liberal use of[Container](https://api.flutter.dev/flutter/widgets/Container-class.html)s to separate
                  widgets using padding, or to add borders or margins.
                  You can change the device's background by placing the
                  entire layout into a`Container`and changing its background
                  color or image.

`Container`
`Container`
#### Summary (Container)

- Add padding, margins, borders
- Change background color or image
- Contains a single child widget, but that child can be a`Row`,`Column`, or even the root of a widget tree

`Row`
`Column`
#### Examples (Container)

This layout consists of a column with two rows, each containing
                  2 images. A[Container](https://api.flutter.dev/flutter/widgets/Container-class.html)is used to change the background color
                  of the column to a lighter grey.

`Container`
`Widget _buildImageColumn() {
  return Container(
    decoration: const BoxDecoration(color: Colors.black26),
    child: Column(children: [_buildImageRow(1), _buildImageRow(3)]),
  );
}`
A`Container`is also used to add a rounded border and margins
                  to each image:

`Container`
`Widget _buildDecoratedImage(int imageIndex) => Expanded(
  child: Container(
    decoration: BoxDecoration(
      border: Border.all(width: 10, color: Colors.black38),
      borderRadius: const BorderRadius.all(Radius.circular(8)),
    ),
    margin: const EdgeInsets.all(4),
    child: Image.asset('images/pic$imageIndex.jpg'),
  ),
);
​
Widget _buildImageRow(int imageIndex) => Row(
  children: [
    _buildDecoratedImage(imageIndex),
    _buildDecoratedImage(imageIndex + 1),
  ],
);`
You can find more`Container`examples in the[tutorial](https://docs.flutter.dev/ui/layout/tutorial).

`Container`
**App source:**[container](https://github.com/flutter/website/tree/main/examples/layout/container)

---

### GridView

Use[GridView](https://api.flutter.dev/flutter/widgets/GridView-class.html)to lay widgets out as a two-dimensional
                  list.`GridView`provides two pre-fabricated lists,
                  or you can build your own custom grid. When a`GridView`detects that its contents are too long to fit the render box,
                  it automatically scrolls.

`GridView`
`GridView`
`GridView`
#### Summary (GridView)

- Lays widgets out in a grid
- Detects when the column content exceeds the render box
                    and automatically provides scrolling
- Build your own custom grid, or use one of the provided grids:

- `GridView.count`allows you to specify the number of columns
- `GridView.extent`allows you to specify the maximum pixel
                        width of a tile

`GridView.count`
`GridView.extent`
#### Examples (GridView)

Uses`GridView.extent`to create a grid with tiles a maximum
  150 pixels wide.

`GridView.extent`
**App source:**[grid_and_list](https://github.com/flutter/website/tree/main/examples/layout/grid_and_list)

Uses`GridView.count`to create a grid that's 2 tiles
  wide in portrait mode, and 3 tiles wide in landscape mode.
  The titles are created by setting the`footer`property for
  each[GridTile](https://api.flutter.dev/flutter/material/GridTile-class.html).

`GridView.count`
`footer`
`GridTile`
**Dart code:**[grid_list_demo.dart](https://github.com/flutter/website/tree/main/examples/layout/gallery/lib/grid_list_demo.dart)

`grid_list_demo.dart`
`Widget _buildGrid() => GridView.extent(
  maxCrossAxisExtent: 150,
  padding: const EdgeInsets.all(4),
  mainAxisSpacing: 4,
  crossAxisSpacing: 4,
  children: _buildGridTileList(30),
);
​
// The images are saved with names pic0.jpg, pic1.jpg...pic29.jpg.
// The List.generate() constructor allows an easy way to create
// a list when objects have a predictable naming pattern.
List<Widget> _buildGridTileList(int count) =>
    List.generate(count, (i) => Image.asset('images/pic$i.jpg'));`
---

### ListView

[ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html), a column-like widget, automatically
                  provides scrolling when its content is too long for
                  its render box.

`ListView`
#### Summary (ListView)

- A specialized[Column](https://api.flutter.dev/flutter/widgets/Column-class.html)for organizing a list of boxes
- Can be laid out horizontally or vertically
- Detects when its content won't fit and provides scrolling
- Less configurable than`Column`, but easier to use and
                    supports scrolling

`Column`
`Column`
#### Examples (ListView)

Uses`ListView`to display a list of businesses using`ListTile`s. A`Divider`separates the theaters from
  the restaurants.

`ListView`
`ListTile`
`Divider`
**App source:**[grid_and_list](https://github.com/flutter/website/tree/main/examples/layout/grid_and_list)

Uses`ListView`to display the[Colors](https://api.flutter.dev/flutter/material/Colors-class.html)from
  the[Material 2 Design palette](https://m2.material.io/design/color/the-color-system.html#tools-for-picking-colors)for a particular color family.

`ListView`
`Colors`
**Dart code:**[colors_demo.dart](https://github.com/flutter/website/tree/main/examples/layout/gallery/lib/colors_demo.dart)

`colors_demo.dart`
`Widget _buildList() {
  return ListView(
    children: [
      _tile('CineArts at the Empire', '85 W Portal Ave', Icons.theaters),
      _tile('The Castro Theater', '429 Castro St', Icons.theaters),
      _tile('Alamo Drafthouse Cinema', '2550 Mission St', Icons.theaters),
      _tile('Roxie Theater', '3117 16th St', Icons.theaters),
      _tile(
        'United Artists Stonestown Twin',
        '501 Buckingham Way',
        Icons.theaters,
      ),
      _tile('AMC Metreon 16', '135 4th St #3000', Icons.theaters),
      const Divider(),
      _tile('K\'s Kitchen', '757 Monterey Blvd', Icons.restaurant),
      _tile('Emmy\'s Restaurant', '1923 Ocean Ave', Icons.restaurant),
      _tile('Chaiya Thai Restaurant', '272 Claremont Blvd', Icons.restaurant),
      _tile('La Ciccia', '291 30th St', Icons.restaurant),
    ],
  );
}
​
ListTile _tile(String title, String subtitle, IconData icon) {
  return ListTile(
    title: Text(
      title,
      style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 20),
    ),
    subtitle: Text(subtitle),
    leading: Icon(icon, color: Colors.blue[500]),
  );
}`
---

### Stack

Use[Stack](https://api.flutter.dev/flutter/widgets/Stack-class.html)to arrange widgets on top of a base
                  widget—often an image. The widgets can completely
                  or partially overlap the base widget.

`Stack`
#### Summary (Stack)

- Use for widgets that overlap another widget
- The first widget in the list of children is the base widget;
                    subsequent children are overlaid on top of that base widget
- A`Stack`'s content can't scroll
- You can choose to clip children that exceed the render box

`Stack`
#### Examples (Stack)

Uses`Stack`to overlay a`Container`(that displays its`Text`on a translucent
  black background) on top of a`CircleAvatar`.
  The`Stack`offsets the text using the`alignment`property and`Alignment`s.

`Stack`
`Container`
`Text`
`CircleAvatar`
`Stack`
`alignment`
`Alignment`
**App source:**[card_and_stack](https://github.com/flutter/website/tree/main/examples/layout/card_and_stack)

Uses`Stack`to overlay an icon on top of an image.

`Stack`
**Dart code:**[bottom_navigation_demo.dart](https://github.com/flutter/website/tree/main/examples/layout/gallery/lib/bottom_navigation_demo.dart)

`bottom_navigation_demo.dart`
`Widget _buildStack() {
  return Stack(
    alignment: const Alignment(0.6, 0.6),
    children: [
      const CircleAvatar(
        backgroundImage: AssetImage('images/pic.jpg'),
        radius: 100,
      ),
      Container(
        decoration: const BoxDecoration(color: Colors.black45),
        child: const Text(
          'Mia B',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
    ],
  );
}`
---

### Card

A[Card](https://api.flutter.dev/flutter/material/Card-class.html), from the[Material library](https://api.flutter.dev/flutter/material/material-library.html),
                  contains related nuggets of information and can
                  be composed of almost any widget, but is often used with[ListTile](https://api.flutter.dev/flutter/material/ListTile-class.html).`Card`has a single child,
                  but its child can be a column, row, list, grid,
                  or other widget that supports multiple children.
                  By default, a`Card`shrinks its size to 0 by 0 pixels.
                  You can use[SizedBox](https://api.flutter.dev/flutter/widgets/SizedBox-class.html)to constrain the size of a card.

`Card`
`ListTile`
`Card`
`Card`
`SizedBox`
In Flutter, a`Card`features slightly rounded corners
                  and a drop shadow, giving it a 3D effect.
                  Changing a`Card`'s`elevation`property allows you to control
                  the drop shadow effect. Setting the elevation to 24,
                  for example, visually lifts the`Card`further from the
                  surface and causes the shadow to become more dispersed.
                  For a list of supported elevation values, see[Elevation](https://m3.material.io/styles/elevation)in the[Material guidelines](https://m3.material.io/styles).
                  Specifying an unsupported value disables the drop shadow entirely.

`Card`
`Card`
`elevation`
`Card`
#### Summary (Card)

- Implements a[Material card](https://m3.material.io/components/cards)
- Used for presenting related nuggets of information
- Accepts a single child, but that child can be a`Row`,`Column`, or other widget that holds a list of children
- Displayed with rounded corners and a drop shadow
- A`Card`'s content can't scroll
- From the[Material library](https://api.flutter.dev/flutter/material/material-library.html)

`Row`
`Column`
`Card`
#### Examples (Card)

A`Card`containing 3 ListTiles and sized by wrapping
  it with a`SizedBox`. A`Divider`separates the first
  and second`ListTiles`.

`Card`
`SizedBox`
`Divider`
`ListTiles`
**App source:**[card_and_stack](https://github.com/flutter/website/tree/main/examples/layout/card_and_stack)

A`Card`containing an image and text.

`Card`
**Dart code:**[cards_demo.dart](https://github.com/flutter/website/tree/main/examples/layout/gallery/lib/cards_demo.dart)

`cards_demo.dart`
`Widget _buildCard() {
  return SizedBox(
    height: 210,
    child: Card(
      child: Column(
        children: [
          ListTile(
            title: const Text(
              '1625 Main Street',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: const Text('My City, CA 99984'),
            leading: Icon(Icons.restaurant_menu, color: Colors.blue[500]),
          ),
          const Divider(),
          ListTile(
            title: const Text(
              '(408) 555-1212',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            leading: Icon(Icons.contact_phone, color: Colors.blue[500]),
          ),
          ListTile(
            title: const Text('costa@example.com'),
            leading: Icon(Icons.contact_mail, color: Colors.blue[500]),
          ),
        ],
      ),
    ),
  );
}`
---

### ListTile

Use[ListTile](https://api.flutter.dev/flutter/material/ListTile-class.html), a specialized row widget from the[Material library](https://api.flutter.dev/flutter/material/material-library.html), for an easy way to create a row
                  containing up to 3 lines of text and optional leading
                  and trailing icons.`ListTile`is most commonly used in[Card](https://api.flutter.dev/flutter/material/Card-class.html)or[ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html), but can be used elsewhere.

`ListTile`
`ListTile`
`Card`
`ListView`
#### Summary (ListTile)

- A specialized row that contains up to 3 lines of text and
                    optional icons
- Less configurable than`Row`, but easier to use
- From the[Material library](https://api.flutter.dev/flutter/material/material-library.html)

`Row`
#### Examples (ListTile)

A`Card`containing 3`ListTile`s.

`Card`
`ListTile`
**App source:**[card_and_stack](https://github.com/flutter/website/tree/main/examples/layout/card_and_stack)

Uses`ListTile`with leading widgets.

`ListTile`
**Dart code:**[list_demo.dart](https://github.com/flutter/website/tree/main/examples/layout/gallery/lib/list_demo.dart)

`list_demo.dart`
---

## Constraints

To fully understand Flutter's layout system, you need
                  to learn how Flutter positions and sizes
                  the components in a layout. For more information,
                  see[Understanding constraints](https://docs.flutter.dev/ui/layout/constraints).

## Videos

The following videos, part of the[Flutter in Focus](https://www.youtube.com/watch?v=wgTBLj7rMPM&list=PLjxrf2q8roU2HdJQDjJzOeO6J3FoFLWr2)series,
                  explain`Stateless`and`Stateful`widgets.

`Stateless`
`Stateful`
[Flutter in Focus playlist](https://www.youtube.com/playlist?list=PLjxrf2q8roU2HdJQDjJzOeO6J3FoFLWr2)

---

Each episode of the[Widget of the Week series](https://www.youtube.com/playlist?list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)focuses on a widget.
                  Several of them include layout widgets.

[Flutter Widget of the Week playlist](https://www.youtube.com/playlist?list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)

## Other resources

The following resources might help when writing layout code.

Learn how to build a layout.

Describes many of the widgets available in Flutter.

For those familiar with web programming,
                      this page maps HTML/CSS functionality to Flutter features.

Reference documentation for all of the Flutter libraries.

Explains how to add images and other assets to your app's package.

One person's experience writing their first Flutter app.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/layout/index.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/ui/layout&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/layout/index.md).
