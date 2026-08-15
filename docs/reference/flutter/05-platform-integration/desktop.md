> 原文链接: [https://docs.flutter.dev/platform-integration/desktop](https://docs.flutter.dev/platform-integration/desktop)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter provides support for compiling
                  a native Windows, macOS, or Linux desktop app.
                  Flutter's desktop support also extends to plugins—you
                  can install existing plugins that support the Windows,
                  macOS, or Linux platforms, or you can create your own.

## Create a new project

You can use the following steps
                  to create a new project with desktop support.

### Set up desktop devtools

Consult the guide for your target desktop environment:

- [Install Linux desktop devtools](https://docs.flutter.dev/platform-integration/linux/setup#set-up-tooling)
- [Install macOS desktop devtools](https://docs.flutter.dev/platform-integration/macos/setup#set-up-tooling)
- [Install Windows desktop devtools](https://docs.flutter.dev/platform-integration/windows/setup#set-up-tooling)

If`flutter doctor`finds problems or missing components
                  for a platform that you don't want to develop for,
                  you can ignore those warnings. Or you can disable the
                  platform altogether using the`flutter config`command,
                  for example:

`flutter doctor`
`flutter config`
`$ flutter config --no-enable-ios`
Other available flags:

- `--no-enable-windows-desktop`
- `--no-enable-linux-desktop`
- `--no-enable-macos-desktop`
- `--no-enable-web`
- `--no-enable-android`
- `--no-enable-ios`

`--no-enable-windows-desktop`
`--no-enable-linux-desktop`
`--no-enable-macos-desktop`
`--no-enable-web`
`--no-enable-android`
`--no-enable-ios`
After enabling desktop support,
                  restart your IDE so that it can detect the new device.

### Create and run

Creating a new project with desktop support is no different
                  from[creating a new Flutter project](https://docs.flutter.dev/reference/create-new-app)for other platforms.

Once you've configured your environment for desktop
                  support, you can create and run a desktop application
                  either in the IDE or from the command line.

#### Using an IDE

After you've configured your environment to support
                  desktop, make sure you restart the IDE if it was
                  already running.

Create a new application in your IDE and it automatically
                  creates iOS, Android, web, and desktop versions of your app.
                  From the device pulldown, select**windows (desktop)**,**macOS (desktop)**, or**linux (desktop)**and run your application to see it launch on the desktop.

#### From the command line

To create a new application that includes desktop support
                  (in addition to mobile and web support), run the following commands,
                  substituting`my_app`with the name of your project:

`my_app`
`$ flutter create my_app
$ cd my_app`
To launch your application from the command line,
                  enter one of the following commands from the top
                  of the package:

`C:\> flutter run -d windows
$ flutter run -d macos
$ flutter run -d linux`
## Build a release app

To generate a release build,
                  run one of the following commands:

`PS C:\> flutter build windows
$ flutter build macos
$ flutter build linux`
## Add desktop support to an existing Flutter app

To add desktop support to an existing Flutter project,
                  run the following command in a terminal from the
                  root project directory:

`$ flutter create --platforms=windows,macos,linux .`
This adds the necessary desktop files and directories
                  to your existing Flutter project.
                  To add only specific desktop platforms,
                  change the`platforms`list to include only
                  the platform(s) you want to add.

`platforms`
## Plugin support

Flutter on the desktop supports using and creating plugins.
                  To use a plugin that supports desktop,
                  follow the steps for plugins in[using packages](https://docs.flutter.dev/packages-and-plugins/using-packages).
                  Flutter automatically adds the necessary native code
                  to your project, as with any other platform.

### Writing a plugin

When you start building your own plugins,
                  you'll want to keep federation in mind.
                  Federation is the ability to define several
                  different packages, each targeted at a
                  different set of platforms, brought together
                  into a single plugin for ease of use by developers.
                  For example, the Windows implementation of the`url_launcher`is really`url_launcher_windows`,
                  but a Flutter developer can simply add the`url_launcher`package to their`pubspec.yaml`as a dependency and the build process pulls in
                  the correct implementation based on the target platform.
                  Federation is handy because different teams with
                  different expertise can build plugin implementations
                  for different platforms.
                  You can add a new platform implementation to any
                  endorsed federated plugin on pub.dev,
                  so long as you coordinate this effort with the
                  original plugin author.

`url_launcher`
`url_launcher_windows`
`url_launcher`
`pubspec.yaml`
For more information, including information
                  about endorsed plugins, see the following resources:

- [Developing packages and plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages), particularly the[Federated plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages#federated-plugins)section.
- [How to write a Flutter web plugin, part 2](https://blog.flutter.dev/how-to-write-a-flutter-web-plugin-part-2-afdddb69ece6),
                    covers the structure of federated plugins and
                    contains information applicable to desktop
                    plugins.
- [Modern Flutter Plugin Development](https://blog.flutter.dev/modern-flutter-plugin-development-4c3ee015cf5a)covers
                    recent enhancements to Flutter's plugin support.

## Samples

You can run the following samples as desktop apps,
                  as well as download and inspect the source code to
                  learn more about Flutter desktop support.

A showcase app that uses Flutter to create a highly expressive user interface.
                      Wonderous focuses on delivering an accessible and high-quality user experience
                      while including engaging interactions and novel animations.
                      To run Wonderous as a desktop app, clone the project and
                      follow the instructions provided in the[README](https://github.com/gskinnerTeam/flutter-wonderous-app#wonderous).

A Google contacts manager that integrates with GitHub and Twitter.
                      It syncs with your Google account, imports your contacts,
                      and allows you to manage them.

A sample application built as a desktop application that
                      uses desktop-supported plugins.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/desktop.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/desktop&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/desktop.md).
