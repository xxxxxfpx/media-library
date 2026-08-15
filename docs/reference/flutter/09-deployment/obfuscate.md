> 原文链接: [https://docs.flutter.dev/deployment/obfuscate](https://docs.flutter.dev/deployment/obfuscate)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

## What is code obfuscation?

[Code obfuscation](https://en.wikipedia.org/wiki/Obfuscation_(software))is the process of modifying an
                  app's binary to make it harder for humans to understand.
                  Obfuscation hides function and class names in your
                  compiled Dart code, replacing each symbol with
                  another symbol, making it difficult for an attacker
                  to reverse engineer your proprietary app.

## Limitations and warnings

**Flutter's code obfuscation works
                    only on arelease build.**

Obfuscating your code does*not*encrypt resources nor does it protect against
                  reverse engineering.
                  It only renames symbols with more obscure names.

Web apps don't support obfuscation.
                  A web app can be[minified](https://en.wikipedia.org/wiki/Minification_(programming)), which provides a similar result.
                  When you build a release version of a Flutter web app,
                  the web compiler minifies the app. To learn more,
                  see[Build and release a web app](https://docs.flutter.dev/deployment/web).

## Supported targets

The following build targets
                  support the obfuscation process
                  described on this page:

- `aar`
- `apk`
- `appbundle`
- `ios`
- `ios-framework`
- `ipa`
- `linux`
- `macos`
- `macos-framework`
- `windows`

`aar`
`apk`
`appbundle`
`ios`
`ios-framework`
`ipa`
`linux`
`macos`
`macos-framework`
`windows`
For detailed information about the command line options
                  available for a build target, run the following
                  command. The`--obfuscate`and`--split-debug-info`options should
                  be listed in the output. If they aren't, you'll need to
                  install a newer version of Flutter to obfuscate your code.

`--obfuscate`
`--split-debug-info`
`$ flutter build <build-target> -h`
- `<build-target>`: The build target. For example,`apk`.

`<build-target>`
`apk`
## Obfuscate your app

To obfuscate your app and create a symbol map, use the`flutter build`command in release mode
                  with the`--obfuscate`and`--split-debug-info`options.
                  If you want to debug your obfuscated
                  app in the future, you will need the symbol map.

`flutter build`
`--obfuscate`
`--split-debug-info`
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Run the following command to obfuscate your app and
                      generate a SYMBOLS file:

`$ flutter build <build-target> \
   --obfuscate \
   --split-debug-info=/<symbols-directory>`
- `<build-target>`: The build target. For example,`apk`.
- `<symbols-directory>`: The directory where the SYMBOLS
                        file should be placed. For example,`out/android`.

`<build-target>`
`apk`
`<symbols-directory>`
`out/android`
Once you've obfuscated your binary,**backup
                        the SYMBOLS file**. You might need this if you lose
                      your original SYMBOLs file and you
                      want to de-obfuscate a stack trace.

## Read an obfuscated stack trace

To debug a stack trace created by an obfuscated app,
                  use the following steps to make it human readable:

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Find the matching SYMBOLS file.
                      For example, a crash from an Android arm64
                      device would need`app.android-arm64.symbols`.

`app.android-arm64.symbols`
Provide both the stack trace (stored in a file)
                      and the SYMBOLS file to the`flutter symbolize`command.

`flutter symbolize`
`$ flutter symbolize \
   -i <stack-trace-file> \
   -d <obfuscated-symbols-file>`
- `<stack-trace-file>`: The file path for the
                        stacktrace. For example,`???`.
- `<obfuscated-symbols-file>`: The file path for the
                        symbols file that contains the obfuscated symbols.
                        For example,`out/android/app.android-arm64.symbols`.

`<stack-trace-file>`
`???`
`<obfuscated-symbols-file>`
`out/android/app.android-arm64.symbols`
For more information about the`symbolize`command,
                      run`flutter symbolize -h`.

`symbolize`
`flutter symbolize -h`
## Read an obfuscated name

You can generate a JSON file that contains
                  an obfuscation map. An obfuscation map is a JSON array with
                  pairs of original names and obfuscated names. For example,`["MaterialApp", "ex", "Scaffold", "ey"]`, where`ex`is the obfuscated name of`MaterialApp`.

`["MaterialApp", "ex", "Scaffold", "ey"]`
`ex`
`MaterialApp`
To generate an obfuscation map, use the following command:

`$ flutter build <build-target> \
   --obfuscate \
   --split-debug-info=/<symbols-directory> \
   --extra-gen-snapshot-options=--save-obfuscation-map=/<obfuscation-map-file>`
- `<build-target>`: The build target. For example,`apk`.
- `<symbols-directory>`: The directory where the symbols
                    should be placed. For example,`out/android`
- `<obfuscation-map-file>`: The file path where the
                    JSON obfuscation map should be placed. For example,`out/android/map.json`

`<build-target>`
`apk`
`<symbols-directory>`
`out/android`
`<obfuscation-map-file>`
`out/android/map.json`
## Caveat

Be aware of the following when coding an app that will
                  eventually be an obfuscated binary.

- code-excerpt "lib/main.dart (Expect)"dart@copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

Code that relies on matching specific class, function,
                      or library names will fail.
                      For example, the following call to`expect()`won't
                      work in an obfuscated binary:

`expect()`
`expect(foo.runtimeType.toString(), equals('Foo'));`
Enum names are not obfuscated currently.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/obfuscate.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/deployment/obfuscate&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/obfuscate.md).
