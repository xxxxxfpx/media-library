> 原文链接: [https://docs.flutter.dev/ui/design/text/typography](https://docs.flutter.dev/ui/design/text/typography)
---

Flutter is back at Google I/O on May 19-20!Register now

Typographycovers the style and appearance of
                  type or fonts: it specifies how heavy the font is,
                  the slant of the font, the spacing between
                  the letters, and other visual aspects of the text.

All fonts arenotcreated the same.

A font style is defined by, at minimum, a typeface, representing the set of
                  common character rules describing fonts in the same type family, such asRobotoorNoto, a font weight (for example, Regular, Bold, or a
                  numeric value), and a style (like Regular,Italic, etc). All of these
                  and additional pre-set attributes come together to make up
                  what we would call a static font.

Variable fonts allow some of these attributes to be modified at runtime and
                  store what would normally be multiple static fonts in a single file.

## Typographic Scale

A typographical scale is a set of related text styles to provide balance,
                  cohesion, and visual variety in your apps.

The common type scale in Flutter, provided byTextTheme, includes five
                  categories of text indicating the function:

There are also three size variations for each:

Each of these fifteen combinations of a category and text size are represented
                  by a singleTextStyle.

All the platform specific typographical scales that Flutter exposes are
                  contained in theTypographyclass. Usually, you will not need to
                  reference this class directly as theTextThemewill be localized to your target platform.

## Variable fonts

Variable fontsallow you to control pre-defined aspects of text styling.
                  Variable fonts support specific axes, such as width,
                  weight, slant (to name a few).
                  The user can selectany value along the continuous axiswhen specifying the type.

### Using the Google Fonts type tester

A growing number of fonts on Google Fonts offer some variable font capabilities.
                  You can see the range of options by using the Type Tester and see how you
                  might vary a single font.

In real time, move the slider on any of the axes to
                  see how it affects the font. When programming a variable font,
                  use theFontVariationclass to modify the font's design axes.
                  TheFontVariationclass conforms to theOpenType font variables spec.

## Static fonts

Google Fonts also contains static fonts. As with variable fonts,
                  you need to know how the font is designed to know what options
                  are available to you.
                  Once again, the Google Fonts site can help.

### Using the Google Fonts package

While you can download fonts from the site and install them manually in your apps,
                  you can elect to use theme directly from thegoogle_fontspackage onpub.dev.

They can be used as is by referencing simply the font name:

or customized by setting properties on the resultingTextStyle:

### Modifying fonts

Use the following API to programmatically alter a static font
                  (but remember that this only works if the font wasdesignedto support the feature):

AFontFeaturecorresponds to anOpenType feature tagand can be thought of as a boolean flag to enable or disable
                  a feature of a given font.

## Other resources

The following video shows you some of the capabilities
                  of Flutter's typography and combines it with the MaterialandCupertino look and feel (depending on the platform
                  the app runs on), animation, and custom fragment shaders:

Watch on YouTube in a new tab: "Prototyping beautiful designs with Flutter"

To read one engineer's experience
                  customizing variable fonts and animating them as they
                  morph (and was the basis for the above video),
                  check outPlayful typography with Flutter,
                  a free article on Medium. The associated example also
                  uses a custom shader.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.View sourceorreport an issue.
