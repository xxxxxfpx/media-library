> 原文链接: [https://docs.flutter.dev/tools/devtools/console](https://docs.flutter.dev/tools/devtools/console)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The DevTools Debug console allows you to watch an
                  application's standard output (`stdout`),
                  evaluate expressions for a paused or running
                  app in debug mode, and analyze inbound and outbound
                  references for objects.

`stdout`
The Debug console is available from the[Inspector](https://docs.flutter.dev/tools/devtools/inspector),[Debugger](https://docs.flutter.dev/tools/devtools/debugger), and[Memory](https://docs.flutter.dev/tools/devtools/memory)views.

## Watch application output

The console shows the application's standard output (`stdout`):

`stdout`
![Screenshot of stdout in Console view](https://docs.flutter.dev/assets/images/docs/tools/devtools/console-stdout.png)

## Explore inspected widgets

If you click a widget on the**Inspector**screen,
                  the variable for this widget displays in the**Console**:

![Screenshot of inspected widget in Console view](https://docs.flutter.dev/assets/images/docs/tools/devtools/console-inspect-widget.png)

## Evaluate expressions

In the console, you can evaluate expressions for a paused
                  or running application, assuming that you are running
                  your app in debug mode:

![Screenshot showing evaluating an expression in the console](https://docs.flutter.dev/assets/images/docs/tools/devtools/console-evaluate-expressions.png)

To assign an evaluated object to a variable,
                  use`$0`,`$1`(through`$5`) in the form of`var x = $0`:

`$0`
`$1`
`$5`
`var x = $0`
![Screenshot showing how to evaluate variables](https://docs.flutter.dev/assets/images/docs/tools/devtools/console-evaluate-variables.png)

## Browse heap snapshot

To drop a variable to the console from a heap snapshot,
                  do the following:

1. Navigate to**Devtools > Memory > Diff Snapshots**.
1. Record a memory heap snapshot.
1. Click on the context menu`[⋮]`to view the number of**Instances**for the desired**Class**.
1. Select whether you want to store a single instance as
                    a console variable, or whether you want to store*all*currently alive instances in the app.

`[⋮]`
![Screenshot showing how to browse the heap snapshots](https://docs.flutter.dev/assets/images/docs/tools/devtools/browse-heap-snapshot.png)

The Console screen displays both live and static
                  inbound and outbound references, as well as field values:

![Screenshot showing inbound and outbound references in Console](https://docs.flutter.dev/assets/images/docs/tools/devtools/console-references.png)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/console.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/tools/devtools/console&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/tools/devtools/console.md).
