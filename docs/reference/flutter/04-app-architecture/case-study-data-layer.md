> 原文链接: [https://docs.flutter.dev/app-architecture/case-study/data-layer](https://docs.flutter.dev/app-architecture/case-study/data-layer)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The data layer of an application, known as the*model*in MVVM terminology,
                  is the source of truth for all application data.
                  As the source of truth,
                  it's the only place that application data should be updated.

It's responsible for consuming data from various external APIs,
                  exposing that data to the UI,
                  handling events from the UI that require data to be updated,
                  and sending update requests to those external APIs as needed.

The data layer in this guide has two main components,[repositories](https://docs.flutter.dev/app-architecture/guide#repositories)and[services](https://docs.flutter.dev/app-architecture/guide#services).

![A diagram that highlights the data layer components of an application.](https://docs.flutter.dev/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Data-highlighted.png)

- **Repositories**are the source of the truth for application data, and contain
                    logic that relates to that data, like updating the data in response to new
                    user events or polling for data from services. Repositories are responsible
                    for synchronizing the data when offline capabilities are supported, managing
                    retry logic, and caching data.
- **Services**are stateless Dart classes that interact with APIs, like HTTP
                    servers and platform plugins. Any data that your application needs that isn't
                    created inside the application code itself should be fetched from within
                    service classes.

## Define a service

A service class is the least ambiguous of all the architecture components.
                  It's stateless, and its functions don't have side effects.
                  Its only job is to wrap an external API.
                  There's generally one service class per data source,
                  such as a client HTTP server or a platform plugin.

![A diagram that shows the inputs and outputs of service objects.](https://docs.flutter.dev/assets/images/docs/app-architecture/case-study/mvvm-case-study-services-architecture.png)

In the Compass app, for example, there's an[APIClient](https://github.com/flutter/samples/blob/main/compass_app/app/lib/data/services/api/api_client.dart)service that
                  handles the CRUD calls to the client-facing server.

`APIClient`
`class ApiClient {
  // Some code omitted for demo purposes.
​
  Future<Result<List<ContinentApiModel>>> getContinents() async { /* ... */ }
​
  Future<Result<List<DestinationApiModel>>> getDestinations() async { /* ... */ }
​
  Future<Result<List<ActivityApiModel>>> getActivityByDestination(String ref) async { /* ... */ }
​
  Future<Result<List<BookingApiModel>>> getBookings() async { /* ... */ }
​
  Future<Result<BookingApiModel>> getBooking(int id) async { /* ... */ }
​
  Future<Result<BookingApiModel>> postBooking(BookingApiModel booking) async { /* ... */ }
​
  Future<Result<void>> deleteBooking(int id) async { /* ... */ }
​
  Future<Result<UserApiModel>> getUser() async { /* ... */ }
}`
The service itself is a class,
                  where each method wraps a different API endpoint and
                  exposes asynchronous response objects.
                  Continuing the earlier example of deleting a saved booking,
                  the`deleteBooking`method returns a`Future<Result<void>>`.

`deleteBooking`
`Future<Result<void>>`
## Define a repository

A repository's sole responsibility is to manage application data.
                  A repository is the source of truth for a single type of application data,
                  and it should be the only place where that data type is mutated.
                  The repository is responsible for polling new data from external sources,
                  handling retry logic, managing cached data,
                  and transforming raw data into domain models.

![A diagram that highlights the repository component of an application.](https://docs.flutter.dev/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Repository-highlighted.png)

You should have a separate repository for
                  each different type of data in your application.
                  For example, the Compass app has repositories called`UserRepository`,`BookingRepository`,`AuthRepository`,`DestinationRepository`, and more.

`UserRepository`
`BookingRepository`
`AuthRepository`
`DestinationRepository`
The following example is the`BookingRepository`from the Compass app,
                  and shows the basic structure of a repository.

`BookingRepository`
`class BookingRepositoryRemote implements BookingRepository {
  BookingRepositoryRemote({
    required ApiClient apiClient,
  }) : _apiClient = apiClient;
​
  final ApiClient _apiClient;
  List<Destination>? _cachedDestinations;
​
  Future<Result<void>> createBooking(Booking booking) async {...}
  Future<Result<Booking>> getBooking(int id) async {...}
  Future<Result<List<BookingSummary>>> getBookingsList() async {...}
  Future<Result<void>> delete(int id) async {...}
}`
The`BookingRepository`takes the`ApiClient`service as an input,
                  which it uses to get and update the raw data from the server.
                  It's important that the service is a private member,
                  so that the UI layer can't bypass the repository and call a service directly.

`BookingRepository`
`ApiClient`
With the`ApiClient`service,
                  the repository can poll for updates to a user's saved bookings that
                  might happen on the server, and make`POST`requests to delete saved bookings.

`ApiClient`
`POST`
The raw data that a repository transforms into application models can come from
                  multiple sources and multiple services,
                  and therefore repositories and services have a many-to-many relationship.
                  A service can be used by any number of repositories,
                  and a repository can use more than one service.

![A diagram that highlights the data layer components of an application.](https://docs.flutter.dev/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Data-highlighted.png)

### Domain models

The`BookingRepository`outputs`Booking`and`BookingSummary`objects,
                  which are*domain models*.
                  All repositories output corresponding domain models.
                  These data models differ from API models in that they only contain the data
                  needed by the rest of the app.
                  API models contain raw data that often needs to be filtered,
                  combined, or deleted to be useful to the app's view models.
                  The repo refines the raw data and outputs it as domain models.

`BookingRepository`
`Booking`
`BookingSummary`
In the example app, domain models are exposed through
                  return values on methods like`BookingRepository.getBooking`.
                  The`getBooking`method is responsible for getting the raw data from
                  the`ApiClient`service, and transforming it into a`Booking`object.
                  It does this by combining data from multiple service endpoints.

`BookingRepository.getBooking`
`getBooking`
`ApiClient`
`Booking`
`// This method was edited for brevity.
Future<Result<Booking>> getBooking(int id) async {
  try {
    // Get the booking by ID from server.
    final resultBooking = await _apiClient.getBooking(id);
    if (resultBooking is Error<BookingApiModel>) {
      return Result.error(resultBooking.error);
    }
    final booking = resultBooking.asOk.value;
​
    final destination = _apiClient.getDestination(booking.destinationRef);
    final activities = _apiClient.getActivitiesForBooking(
            booking.activitiesRef);
​
    return Result.ok(
      Booking(
        startDate: booking.startDate,
        endDate: booking.endDate,
        destination: destination,
        activity: activities,
      ),
    );
  } on Exception catch (e) {
    return Result.error(e);
  }
}`
### Complete the event cycle

Throughout this page, you've seen how a user can delete a saved booking,
                  starting with an event—a user swiping on a`Dismissible`widget.
                  The view model handles that event by delegating
                  the actual data mutation to the`BookingRepository`.
                  The following snippet shows the`BookingRepository.deleteBooking`method.

`Dismissible`
`BookingRepository`
`BookingRepository.deleteBooking`
`Future<Result<void>> delete(int id) async {
  try {
    return _apiClient.deleteBooking(id);
  } on Exception catch (e) {
    return Result.error(e);
  }
}`
The repository sends a`POST`request to the API client with
                  the`_apiClient.deleteBooking`method, and returns a`Result`.
                  The`HomeViewModel`consumes the`Result`and the data it contains,
                  then ultimately calls`notifyListeners`, completing the cycle.

`POST`
`_apiClient.deleteBooking`
`Result`
`HomeViewModel`
`Result`
`notifyListeners`
## Feedback

As this section of the website is evolving,
                  we[welcome your feedback](https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page=%22case-study/data-layer%22)!

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/app-architecture/case-study/data-layer.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/app-architecture/case-study/data-layer&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/app-architecture/case-study/data-layer.md).
