> 原文链接: [https://docs.flutter.dev/ui/layout/tutorial](https://docs.flutter.dev/ui/layout/tutorial)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

This tutorial explains how to design and build layouts in Flutter.

If you use the example code provided, you can build the following app.

The finished app.

Photo by[Dino Reichmuth](https://unsplash.com/photos/red-and-gray-tents-in-grass-covered-mountain-5Rhl-kSRydQ)on[Unsplash](https://unsplash.com).
                    Text by[Switzerland Tourism](https://www.myswitzerland.com/en-us/destinations/lake-oeschinen).

To get a better overview of the layout mechanism, start with[Flutter's approach to layout](https://docs.flutter.dev/ui/layout).

## Diagram the layout

In this section, consider what type of user experience you want for
                  your app users.

Consider how to position the components of your user interface.
                  A layout consists of the total end result of these positionings.
                  Consider planning your layout to speed up your coding.
                  Using visual cues to know where something goes on screen can be a great help.

Use whichever method you prefer, like an interface design tool or a pencil
                  and a sheet of paper. Figure out where you want to place elements on your
                  screen before writing code. It's the programming version of the adage:
                  "Measure twice, cut once."


Ask these questions to break the layout down to its basic elements.

- Can you identify the rows and columns?
- Does the layout include a grid?
- Are there overlapping elements?
- Does the UI need tabs?
- What do you need to align, pad, or border?

Identify the larger elements. In this example, you arrange the image, title,
buttons, and description into a column.

Major elements in the layout: image, row, row, and text block

Diagram each row.


Row 1, the**Title**section, has three children:
a column of text, a star icon, and a number.
Its first child, the column, contains two lines of text.
That first column might need more space.

Title section with text blocks and an icon

Row 2, the**Button**section, has three children: each child contains
a column which then contains an icon and text.

The Button section with three labeled buttons

After diagramming the layout, consider how you would code it.

Would you write all the code in one class?
                  Or, would you create one class for each part of the layout?

To follow Flutter best practices, create one class, or Widget,
                  to contain each part of your layout.
                  When Flutter needs to re-render part of a UI,
                  it updates the smallest part that changes.
                  This is why Flutter makes "everything a widget".
                  If only the text changes in a`Text`widget, Flutter redraws only that text.
                  Flutter changes the least amount of the UI possible in response to user input.

`Text`
For this tutorial, write each element you have identified as its own widget.

## Create the app base code

In this section, shell out the basic Flutter app code to start your app.

1. code-excerpt "lib/main.dart (all)"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

[Set up your Flutter environment](https://docs.flutter.dev/install).

[Create a new Flutter app](https://docs.flutter.dev/reference/create-new-app).

Replace the contents of`lib/main.dart`with the following code.
                      This app uses a parameter for the app title and the title shown
                      on the app's`appBar`. This decision simplifies the code.

`lib/main.dart`
`appBar`
`import 'package:flutter/material.dart';
​
void main() => runApp(const MyApp());
​
class MyApp extends StatelessWidget {
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
## Add the Title section

In this section, create a`TitleSection`widget that resembles
                  the following layout.

`TitleSection`
The Title section as sketch and prototype UI

### Add theTitleSectionWidget

`TitleSection`
Add the following code after the`MyApp`class.

`MyApp`
`class TitleSection extends StatelessWidget {
  const TitleSection({super.key, required this.name, required this.location});
​
  final String name;
  final String location;
​
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32),
      child: Row(
        children: [
          Expanded(
            /*1*/
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                /*2*/
                Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Text(
                    name,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
                Text(location, style: TextStyle(color: Colors.grey[500])),
              ],
            ),
          ),
          /*3*/
          Icon(Icons.star, color: Colors.red[500]),
          const Text('41'),
        ],
      ),
    );
  }
}`
1. To use all remaining free space in the row, use the`Expanded`widget to
                    stretch the`Column`widget.
                    To place the column at the start of the row,
                    set the`crossAxisAlignment`property to`CrossAxisAlignment.start`.
1. To add space between the rows of text, put those rows in a`Padding`widget.
1. The title row ends with a red star icon and the text`41`.
                     The entire row falls inside a`Padding`widget and pads each edge
                     by 32 pixels.

`Expanded`
`Column`
`crossAxisAlignment`
`CrossAxisAlignment.start`
`Padding`
`41`
`Padding`
### Change the app body to a scrolling view

In the`body`property, replace the`Center`widget with a`SingleChildScrollView`widget.
                  Within the[SingleChildScrollView](https://api.flutter.dev/flutter/widgets/SingleChildScrollView-class.html)widget, replace the`Text`widget with a`Column`widget.

`body`
`Center`
`SingleChildScrollView`
`SingleChildScrollView`
`Text`
`Column`
`body: const Center(
  child: Text('Hello World'),
body: const SingleChildScrollView(
  child: Column(
    children: [`
These code updates change the app in the following ways.

- A`SingleChildScrollView`widget can scroll.
                    This allows elements that don't fit on the current screen to display.
- A`Column`widget displays any elements within its`children`property
                    in the order listed.
                    The first element listed in the`children`list displays at
                    the top of the list. Elements in the`children`list display
                    in array order on the screen from top to bottom.

`SingleChildScrollView`
`Column`
`children`
`children`
`children`
### Update the app to display the title section

Add the`TitleSection`widget as the first element in the`children`list.
                  This places it at the top of the screen.
                  Pass the provided name and location to the`TitleSection`constructor.

`TitleSection`
`children`
`TitleSection`
`children: [
  TitleSection(
    name: 'Oeschinen Lake Campground',
    location: 'Kandersteg, Switzerland',
  ),
],`
## Add the Button section

In this section, add the buttons that will add functionality to your app.

The**Button**section contains three columns that use the same layout:
                  an icon over a row of text.

The Button section as sketch and prototype UI

Plan to distribute these columns in one row so each takes the same
                  amount of space. Paint all text and icons with the primary color.

### Add theButtonSectionwidget

`ButtonSection`
Add the following code after the`TitleSection`widget to contain the code
                  to build the row of buttons.

`TitleSection`
`class ButtonSection extends StatelessWidget {
  const ButtonSection({super.key});
​
  @override
  Widget build(BuildContext context) {
    final Color color = Theme.of(context).primaryColor;
    // ···
  }
​
}`
### Create a widget to make buttons

As the code for each column could use the same syntax,
                  create a widget named`ButtonWithText`.
                  The widget's constructor accepts a color, icon data, and a label for the button.
                  Using these values, the widget builds a`Column`with an`Icon`and a stylized`Text`widget as its children.
                  To help separate these children, a`Padding`widget the`Text`widget
                  is wrapped with a`Padding`widget.

`ButtonWithText`
`Column`
`Icon`
`Text`
`Padding`
`Text`
`Padding`
Add the following code after the`ButtonSection`class.

`ButtonSection`
`class ButtonSection extends StatelessWidget {
  const ButtonSection({super.key});
  // ···
}
​
class ButtonWithText extends StatelessWidget {
  const ButtonWithText({
    super.key,
    required this.color,
    required this.icon,
    required this.label,
  });
​
  final Color color;
  final IconData icon;
  final String label;
​
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, color: color),
        Padding(
          padding: const EdgeInsets.only(top: 8),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w400,
              color: color,
            ),
          ),
        ),
      ],
    );
  }
}`
### Position the buttons with aRowwidget

`Row`
Add the following code into the`ButtonSection`widget.

`ButtonSection`
1. Add three instances of the`ButtonWithText`widget, once for each button.
1. Pass the color,`Icon`, and text for that specific button.
1. Align the columns along the main axis with the`MainAxisAlignment.spaceEvenly`value.
                    The main axis for a`Row`widget is horizontal and the main axis for a`Column`widget is vertical.
                    This value, then, tells Flutter to arrange the free space in equal amounts
                    before, between, and after each column along the`Row`.

`ButtonWithText`
`Icon`
`MainAxisAlignment.spaceEvenly`
`Row`
`Column`
`Row`
`class ButtonSection extends StatelessWidget {
  const ButtonSection({super.key});
​
  @override
  Widget build(BuildContext context) {
    final Color color = Theme.of(context).primaryColor;
    return SizedBox(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          ButtonWithText(color: color, icon: Icons.call, label: 'CALL'),
          ButtonWithText(color: color, icon: Icons.near_me, label: 'ROUTE'),
          ButtonWithText(color: color, icon: Icons.share, label: 'SHARE'),
        ],
      ),
    );
  }
​
}
​
class ButtonWithText extends StatelessWidget {
  const ButtonWithText({
    super.key,
    required this.color,
    required this.icon,
    required this.label,
  });
​
  final Color color;
  final IconData icon;
  final String label;
​
  @override
  Widget build(BuildContext context) {
    return Column(
      // ···
    );
  }
}`
### Update the app to display the button section

Add the button section to the`children`list.

`children`
`TitleSection(
    name: 'Oeschinen Lake Campground',
    location: 'Kandersteg, Switzerland',
  ),
  ButtonSection(),
],`
## Add the Text section

In this section, add the text description to this app.

The text block as sketch and prototype UI

### Add theTextSectionwidget

`TextSection`
Add the following code as a separate widget after the`ButtonSection`widget.

`ButtonSection`
`class TextSection extends StatelessWidget {
  const TextSection({super.key, required this.description});
​
  final String description;
​
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32),
      child: Text(description, softWrap: true),
    );
  }
}`
By setting[softWrap](https://api.flutter.dev/flutter/widgets/Text/softWrap.html)to`true`, text lines fill the column width before
                  wrapping at a word boundary.

`softWrap`
`true`
### Update the app to display the text section

Add a new`TextSection`widget as a child after the`ButtonSection`.
                  When adding the`TextSection`widget, set its`description`property to
                  the text of the location description.

`TextSection`
`ButtonSection`
`TextSection`
`description`
`location: 'Kandersteg, Switzerland',
  ),
  ButtonSection(),
  TextSection(
    description:
        'Lake Oeschinen lies at the foot of the Blüemlisalp in the '
        'Bernese Alps. Situated 1,578 meters above sea level, it '
        'is one of the larger Alpine Lakes. A gondola ride from '
        'Kandersteg, followed by a half-hour walk through pastures '
        'and pine forest, leads you to the lake, which warms to 20 '
        'degrees Celsius in the summer. Activities enjoyed here '
        'include rowing, and riding the summer toboggan run.',
  ),
],`
## Add the Image section

In this section, add the image file to complete your layout.

### Configure your app to use supplied images

To configure your app to reference images, modify its`pubspec.yaml`file.

`pubspec.yaml`
1. pubspec.yamlyaml@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Create an`images`directory at the top of the project.

`images`
Download the[lake.jpg](https://raw.githubusercontent.com/flutter/website/main/examples/layout/lakes/step5/images/lake.jpg)image and add it to the new`images`directory.

`lake.jpg`
`images`
To include images, add an`assets`tag to the`pubspec.yaml`file
                      at the root directory of your app.
                      When you add`assets`, it serves as the set of pointers to the images
                      available to your code.

`assets`
`pubspec.yaml`
`assets`
`flutter:
  uses-material-design: true
  assets:
    - images/lake.jpg`
### Create theImageSectionwidget

`ImageSection`
Define the following`ImageSection`widget after the other declarations.

`ImageSection`
`class ImageSection extends StatelessWidget {
  const ImageSection({super.key, required this.image});
​
  final String image;
​
  @override
  Widget build(BuildContext context) {
    return Image.asset(image, width: 600, height: 240, fit: BoxFit.cover);
  }
}`
The`BoxFit.cover`value tells Flutter to display the image with
                  two constraints. First, display the image as small as possible.
                  Second, cover all the space that the layout allotted, called the render box.

`BoxFit.cover`
### Update the app to display the image section

Add an`ImageSection`widget as the first child in the`children`list.
                  Set the`image`property to the path of the image you added in[Configure your app to use supplied images](#configure-your-app-to-use-supplied-images).

`ImageSection`
`children`
`image`
`children: [
  ImageSection(
    image: 'images/lake.jpg',
  ),
  TitleSection(
    name: 'Oeschinen Lake Campground',
    location: 'Kandersteg, Switzerland',`
## Congratulations

That's it! When you hot reload the app, your app should look like this.

The finished app

## Resources

You can access the resources used in this tutorial from these locations:

**Dart code:**[main.dart](https://github.com/flutter/website/blob/main/examples/layout/lakes/step6/lib/main.dart)
**Image:**[ch-photo](https://unsplash.com/photos/red-and-gray-tents-in-grass-covered-mountain-5Rhl-kSRydQ)
**Pubspec:**[pubspec.yaml](https://github.com/flutter/website/blob/main/examples/layout/lakes/step6/pubspec.yaml)


`main.dart`
`pubspec.yaml`
## Next Steps

To add interactivity to this layout, follow the[interactivity tutorial](https://docs.flutter.dev/ui/interactivity).

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/layout/tutorial.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/ui/layout/tutorial&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/layout/tutorial.md).
