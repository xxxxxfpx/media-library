> 原文链接: [https://docs.flutter.dev/platform-integration/linux/setup](https://docs.flutter.dev/platform-integration/linux/setup)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Learn how to set up your development environment
                  to run, build, and deploy Flutter apps for the Linux desktop platform.

## Set up tooling

To run and debug desktop Flutter apps on Linux,
                  download and install the prerequisite packages.

Using your preferred package manager or mechanism,
                  install the latest versions of the following packages:

- `clang`
- `cmake`
- `ninja-build`
- `pkg-config`
- `libgtk-3-dev`
- `libstdc++-12-dev`

`clang`
`cmake`
`ninja-build`
`pkg-config`
`libgtk-3-dev`
`libstdc++-12-dev`
On Debian-based distros with`apt-get`, such as Ubuntu,
                  install these packages using the following commands:

`apt-get`
`$ sudo apt-get update -y && sudo apt-get upgrade -y
$ sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev libstdc++-12-dev`
## Validate your setup

1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button
1. @copy_button data={"buttonText":null,"classes":[],"title":"Copy code to clipboard"}/@copy_button

### Check for toolchain issues

To check for any issues with your Linux development setup,
                      run the`flutter doctor`command in your preferred terminal:

`flutter doctor`
`$ flutter doctor -v`
If you see any errors or tasks to complete
                      under the**Linux toolchain**section,
                      complete and resolve them, then
                      run`flutter doctor -v`again to verify any changes.

`flutter doctor -v`
### Check for Linux devices

To ensure Flutter can find and connect to your Linux device correctly,
                      run`flutter devices`in your preferred terminal:

`flutter devices`
`$ flutter devices`
If you set everything up correctly,
                      there should be at least one entry with the platform marked as**linux**.

### Troubleshoot setup issues

If you need help resolving any setup issues,
                      check out[Install and setup troubleshooting](https://docs.flutter.dev/install/troubleshoot).

If you still have issues or questions,
                      reach out on one of the Flutter[community](https://flutter.dev/community)channels.

## Start developing for Linux

Congratulations!
                  Now that you've set up Linux desktop development for Flutter,
                  you can continue your Flutter learning journey while testing on Linux
                  or begin expanding integration with Linux.

- [Learn the fundamentals](https://docs.flutter.dev/learn/pathway)
- [Explore Flutter widgets](https://www.youtube.com/watch?v=b_sQ9bMltGU&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)
- [Check out samples](https://docs.flutter.dev/reference/learning-resources)

- [Build a Linux app](https://docs.flutter.dev/platform-integration/linux/building)
- [Release a Linux app](https://docs.flutter.dev/deployment/linux)
- [Write Linux-specific code](https://docs.flutter.dev/platform-integration/platform-channels)
- [Flutter plugins for Linux](https://pub.dev/packages?q=platform%3Alinux+is%3Aplugin)
- [Design Ubuntu-themed apps](https://github.com/ubuntu-flutter-community/yaru_tutorial)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/linux/setup.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/linux/setup&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/linux/setup.md).
