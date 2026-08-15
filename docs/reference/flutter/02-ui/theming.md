> 原文链接: [https://docs.flutter.dev/cookbook/design/themes](https://docs.flutter.dev/cookbook/design/themes)
---

Flutter is back at Google I/O on May 19-20!Register now

To share colors and font styles throughout an app, use themes.

You can define app-wide themes.
                  You can extend a theme to change a theme style for one component.
                  Each theme defines the colors, type style, and other parameters
                  applicable for the type of Material component.

Flutter applies styling in the following order:

After you define aTheme, use it within your own widgets.
                  Flutter's Material widgets use your theme to set the background
                  colors and font styles for app bars, buttons, checkboxes, and more.

## Create an app theme

To share aThemeacross your entire app, set thethemeproperty
                  to yourMaterialAppconstructor.
                  This property takes aThemeDatainstance.

If you don't specify a theme in the constructor,
                  Flutter creates a default theme for you.

Most instances ofThemeDataset values for the following two properties. These properties affect the entire app.

To learn what colors, fonts, and other properties, you can define,
                  check out theThemeDatadocumentation.

## Apply a theme

To apply your new theme, use theTheme.of(context)method
                  when specifying a widget's styling properties.
                  These can include, but are not limited to,styleandcolor.

TheTheme.of(context)method looks up the widget tree and retrieves
                  the nearestThemein the tree.
                  If you have a standaloneTheme, that's applied.
                  If not, Flutter applies the app's theme.

In the following example, theContainerconstructor uses this technique to set itscolor.

## Override a theme

To override the overall theme in part of an app,
                  wrap that section of the app in aThemewidget.

You can override a theme in two ways:

### Set a uniqueThemeDatainstance

If you want a component of your app to ignore the overall theme,
                  create aThemeDatainstance.
                  Pass that instance to theThemewidget.

### Extend the parent theme

Instead of overriding everything, consider extending the parent theme.
                  To extend a theme, use thecopyWith()method.

## Watch a video onTheme

To learn more, watch this short Widget of the Week video on theThemewidget:

Watch on YouTube in a new tab: "Theme | Flutter widget of the week"

## Try an interactive example

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.View sourceorreport an issue.
