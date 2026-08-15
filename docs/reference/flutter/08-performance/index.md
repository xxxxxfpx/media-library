> 原文链接: [https://docs.flutter.dev/perf](https://docs.flutter.dev/perf)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

What is performance? Why is performance important? How do I improve performance?

Our goal is to answer those three questions (mainly the third one), and
                  anything related to them. This document should serve as the single entry
                  point or the root node of a tree of resources that addresses any questions
                  that you have about performance.

The answers to the first two questions are mostly philosophical,
                  and not as helpful to many developers who visit this page with specific
                  performance issues that need to be solved.
                  Therefore, the answers to those
                  questions are in the[appendix](https://docs.flutter.dev/perf/appendix).

To improve performance, you first need metrics: some measurable numbers to
                  verify the problems and improvements.
                  In the[metrics](https://docs.flutter.dev/perf/metrics)page,
                  you'll see which metrics are currently used,
                  and which tools and APIs are available to get the metrics.

There is a list of[Frequently asked questions](https://docs.flutter.dev/perf/faq),
                  so you can find out if the questions you have or the problems you're having
                  were already answered or encountered, and whether there are existing solutions.
                  (Alternatively, you can check the Flutter GitHub issue database using the[performance](https://github.com/flutter/flutter/issues?q=+label%3A%22severe%3A+performance%22)label.)

Finally, the performance issues are divided into four categories. They
                  correspond to the four labels that are used in the Flutter GitHub issue
                  database: "[perf: speed](https://github.com/flutter/flutter/issues?q=is%3Aopen+label%3A%22perf%3A+speed%22+sort%3Aupdated-asc+)", "[perf: memory](https://github.com/flutter/flutter/issues?q=is%3Aopen+label%3A%22perf%3A+memory%22+sort%3Aupdated-asc+)",
                  "[perf: app size](https://github.com/flutter/flutter/issues?q=is%3Aopen+label%3A%22perf%3A+app+size%22+sort%3Aupdated-asc+)", "[perf: energy](https://github.com/flutter/flutter/issues?q=is%3Aopen+label%3A%22perf%3A+energy%22+sort%3Aupdated-asc+)".

The rest of the content is organized using those four categories.

## Speed

Are your animations janky (not smooth)? Learn how to
                  evaluate and fix rendering issues.

[Improving rendering performance](https://docs.flutter.dev/perf/rendering-performance)

## App size

How to measure your app's size. The smaller the size,
                  the quicker it is to download.

[Measuring your app's size](https://docs.flutter.dev/perf/app-size)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/index.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/perf&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/perf/index.md).
