> 原文链接: [https://docs.flutter.dev/app-architecture/design-patterns](https://docs.flutter.dev/app-architecture/design-patterns)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

If you've already read through the[architecture guide](https://docs.flutter.dev/app-architecture/guide)page,
                  or if you're comfortable with Flutter and the MVVM pattern,
                  the following articles are for you.

These articles aren't about high-level app architecture,
                  rather they're about solving specific design problems that improve your
                  application's code base regardless of how you've architected your app.
                  That said, the articles do assume the MVVM pattern laid out on the
                  previous pages in the code examples.

Optimistic state

- user experience
- asynchronous dart

Improve the perception of responsiveness of an application by implementing optimistic state.

When building user experiences,
                        the perception of performance is sometimes just as important as
                        the actual performance of the code.
                        In general, users don’t like waiting for an action to finish to see the result,
                        and anything that takes more than a few milliseconds could be considered “slow”
                        or “unresponsive” from the user’s perspective.

Developers can help mitigate this negative perception
                        by presenting a successful UI state
                        before the background task is fully completed.
                        An example of this would be tapping a “Subscribe” button,
                        and seeing it change to “Subscribed” instantly,
                        even if the background call to the ...

[Read full article](https://docs.flutter.dev/app-architecture/design-patterns/optimistic-state)

Persistent storage architecture: Key-value data

- data
- shared-preferences
- dark mode

Save application data to a user's on-device key-value store.

Most Flutter applications, no matter how small or big they are,
                        require storing data on the user’s device at some point, such as API keys,
                        user preferences or data that should be available offline.

In this recipe, you will learn how to integrate persistent storage
                        for key-value data in a Flutter application
                        that uses the recommended[Flutter architecture design](https://docs.flutter.dev/app-architecture).
                        If you aren’t familiar with storing data to disk at all,
                        you can read the[Store key-value data on disk](https://docs.flutter.dev/cookbook/persistence/key-value)recipe.

Key-value stores are often used for saving simple data,
                        such as app configuration,
                        and in this recipe you’ll ...

[Read full article](https://docs.flutter.dev/app-architecture/design-patterns/key-value-data)

Persistent storage architecture: SQL

- data
- SQL

Save complex application data to a user's device with SQL.

Most Flutter applications,
                        no matter how small or big they are,
                        might require storing data on the user’s device at some point.
                        For example, API keys,
                        user preferences or data that should be available offline.

In this recipe,
                        you will learn how to integrate persistent storage for complex data using SQL
                        in a Flutter application following the Flutter Architecture design pattern.

To learn how to store simpler key-value data,
                        take a look at the Cookbook recipe:[Persistent storage architecture: Key-value data](https://docs.flutter.dev/app-architecture/design-patterns/key-value-data).

To read this recipe,
                        you should be familiar with SQL and SQLite.
                        If you need help, you ...

[Read full article](https://docs.flutter.dev/app-architecture/design-patterns/sql)

Offline-first support

- data
- user experience
- repository pattern

Implement offline-first support for one feature in an application.

An offline-first application is an app capable of offering most
                        or all of its functionality while being disconnected from the internet.
                        Offline-first applications usually rely on stored data
                        to offer users temporary access to data
                        that would otherwise only be available online.

Some offline-first applications combine local and remote data seamlessly,
                        while other applications inform the user
                        when the application is using cached data.
                        In the same way,
                        some applications synchronize data in the background
                        while others require the user to explicitly synchronize it.
                        It all depends on the application requirements and the functionality it offers,
                        and it’s ...

[Read full article](https://docs.flutter.dev/app-architecture/design-patterns/offline-first)

The command pattern

- mvvm
- asynchronous dart
- state

Simplify view model logic by implementing a Command class.

[Model-View-ViewModel (MVVM)](https://docs.flutter.dev/app-architecture/guide#view-models)is a design pattern
                        that separates a feature of an application into three parts:
                        the model, the view model, and the view.
                        Views and view models make up the UI layer of an application.
                        Repositories and services represent the data layer of an application,
                        or the model layer of MVVM.

A command is a class that wraps a method
                        and helps to handle the different states of that method,
                        such as running, complete, and error.

[View models](https://docs.flutter.dev/app-architecture/guide#view-models)can use commands to handle interaction and run actions.
                        You can also use them to display different UI states,
                        ...

[Read full article](https://docs.flutter.dev/app-architecture/design-patterns/command)

Error handling with Result objects

- error handling
- services

Improve error handling across classes with Result objects.

Dart provides a built-in error handling mechanism
                        with the ability to throw and catch exceptions.

As mentioned in the[Error handling documentation](https://dart.dev/language/error-handling),
                        Dart's exceptions are unhandled exceptions.
                        This means that methods that throw exceptions don’t need to declare them,
                        and calling methods aren't required to catch them either.

This can lead to situations where exceptions are not handled properly.
                        In large projects,
                        developers might forget to catch exceptions,
                        and the different application layers and components
                        could throw exceptions that aren’t documented.
                        This can lead to errors and crashes.

In this guide,
                        you will learn about this limitation
                        and ...

[Read full article](https://docs.flutter.dev/app-architecture/design-patterns/result)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/app-architecture/design-patterns.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/app-architecture/design-patterns&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/app-architecture/design-patterns.md).
