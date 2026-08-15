> 原文链接: [https://docs.flutter.dev/platform-integration/web/web-dev-config-file](https://docs.flutter.dev/platform-integration/web/web-dev-config-file)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

Flutter web includes a development server that defaults to
                  serving your application in the`localhost`domain using HTTP
                  on a randomly assigned port. While command-line arguments offer
                  a quick way to modify the server's behavior,
                  this document focuses on a more structured approach:
                  defining your server's behavior through a centralized`web_dev_config.yaml`file.
                  This configuration file allows you to
                  customize server settings—host, port, HTTPS settings, and
                  proxy rules—ensuring a consistent development environment.

`localhost`
`web_dev_config.yaml`
## Create a configuration file

Add a`web_dev_config.yaml`file to the root directory of your Flutter project.
                  If you haven't set up a Flutter project,
                  visit[Building a web application with Flutter](https://docs.flutter.dev/platform-integration/web/building)to get started.

`web_dev_config.yaml`
## Add configuration settings

### Basic server configuration

You can define the host, port, and HTTPS settings for your development server.

`server:
  host: "0.0.0.0" # Defines the binding address <string>
  port: 8080 # Specifies the port <int> for the development server
  https:
    cert-path: "/path/to/cert.pem" # Path <string> to your TLS certificate
    cert-key-path: "/path/to/key.pem" # Path <string> to TLS certificate key`
### Custom headers

You can also inject custom HTTP headers into the development server's responses.

`server:
  headers:
    - name: "X-Custom-Header" # Name <string> of the HTTP header
      value: "MyValue" # Value <string> of the HTTP header
    - name: "Cache-Control"
      value: "no-cache, no-store, must-revalidate"`
### Proxy configuration

Requests are matched in order from the`web_dev_config.yaml`file.

`web_dev_config.yaml`
#### Basic string proxy

Use the`prefix`field for simple path prefix matching.

`prefix`
`server:
  proxy:
    - target: "http://localhost:5000/" # Base URL <string> of your backend
      prefix: "/users/" # Path <string>
    - target: "http://localhost:3000/"
      prefix: "/data/"
      replace: "/report/" # Replacement <string> of path in redirected URL (optional)
    - target: "http://localhost:4000/"
      prefix: "/products/"
      replace: ""`
**Explanation:**

- A request to`/users/names`is
                    forwarded to`http://localhost:5000/users/names`.
- A request to`/data/2023/`is
                    forwarded to`http://localhost:3000/report/2023`because`replace: “/report/”`replaces the`/data/`prefix.
- A request to`/products/item/123`is
                    forwarded to`http://localhost:4000/item/123`because`replace: ""`removes the`/products/`prefix by replacing it with an empty string.

`/users/names`
`http://localhost:5000/users/names`
`/data/2023/`
`http://localhost:3000/report/2023`
`replace: “/report/”`
`/data/`
`/products/item/123`
`http://localhost:4000/item/123`
`replace: ""`
`/products/`
#### Advanced regex proxy

You can also use the`regex`field for more flexible and complex matching.

`regex`
`server:
  proxy:
    - target: "http://localhost:5000/"
      regex: "/users/(\d+)/$" # Path <string> matches requests like /users/123/
    - target: "http://localhost:4000/"
      regex: "^/api/(v\d+)/(.*)" # Matches requests like /api/v1/users
      replace: "/$2?apiVersion=$1" # Allows capture groups (optional)`
**Explanation:**

- A request to`/users/123/`matches the first rule exactly,
                    so it is forwarded to`http://localhost:5000/users/123/`.
- A request to`/api/v1/users/profile/`starts with the second rule path
                    so it is forwarded to`http://localhost:4000/users/profile/?apiVersion=v1`.

`/users/123/`
`http://localhost:5000/users/123/`
`/api/v1/users/profile/`
`http://localhost:4000/users/profile/?apiVersion=v1`
## Configuration precedence

Remember the order of precedence for settings:

1. **Command-line arguments**(such as`--web-hostname`,`--web-port`)
1. **web_dev_config.yamlsettings**
1. **Built-in default values**

`--web-hostname`
`--web-port`
`web_dev_config.yaml`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/web-dev-config-file.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/platform-integration/web/web-dev-config-file&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/platform-integration/web/web-dev-config-file.md).
