> 原文链接: [https://docs.flutter.dev/deployment/windows](https://docs.flutter.dev/deployment/windows)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

One convenient approach to distributing Windows apps
                  is the[Microsoft Store](https://www.microsoft.com/store/apps/windows).
                  This guide provides a step-by-step walkthrough
                  of packaging and deploying a Flutter app in this way.

## Preliminaries

Before beginning the process of releasing
                  a Flutter Windows desktop app to the Microsoft Store,
                  first confirm that it satisfies[Microsoft Store Policies](https://docs.microsoft.com/windows/uwp/publish/store-policies/).

Also, you must join the[Microsoft Partner Network](https://partner.microsoft.com/)to be able to submit apps.

## Set up your application in the Partner Center

Manage an application's life cycle in the[Microsoft Partner Center](https://partner.microsoft.com/).

First, reserve the application name and
                  ensure that the required rights to the name exist.
                  Once the name is reserved, the application
                  will be provisioned for services (such as
                  push notifications), and you can start adding add-ons.

Options such as pricing, availability,
                  age ratings, and category have to be
                  configured together with the first submission
                  and are automatically retained
                  for the subsequent submissions.

## Packaging and deployment

In order to publish an application to Microsoft Store,
                  you must first package it.
                  The valid formats are**.msix**,**.msixbundle**,**.msixupload**,**.appx**,**.appxbundle**,**.appxupload**, and**.xap**.

### Manual packaging and deployment for the Microsoft Store

Check out[MSIX packaging](https://docs.flutter.dev/platform-integration/windows/building#msix-packaging)to learn about packaging
                  Flutter Windows desktop applications.

Note that each product has a unique identity,
                  which the Store assigns.

If the package is being built manually,
                  you have to include its identity details
                  manually during the packaging.
                  The essential information can be retrieved
                  from the Partner Center using the following instructions:

1. In the Partner Center, navigate to the application.
1. Select**Product management**.
1. Retrieve the package identity name, publisher,
                    and publisher display name by clicking**Product identity**.

After manually packaging the application,
                  manually submit it to the[Microsoft Partner Center](https://partner.microsoft.com/).
                  You can do this by creating a new submission,
                  navigating to**Packages**,
                  and uploading the created application package.

### Continuous deployment

In addition to manually creating and deploying the package,
                  you can automate the build, package, versioning,
                  and deployment process using CI/CD tooling after having submitted
                  the application to the Microsoft Store for the first time.

#### Codemagic CI/CD

[Codemagic CI/CD](https://codemagic.io/start/)uses the[msixpub package](https://pub.dev/packages/msix)to package
                  Flutter Windows desktop applications.

`msix`
For Flutter applications, use either the[Codemagic Workflow Editor](https://docs.codemagic.io/flutter-publishing/publishing-to-microsoft-store/)or[codemagic.yaml](https://docs.codemagic.io/yaml-publishing/microsoft-store/)to package the application and deploy it
                  to the Microsoft Partner Center.
                  Additional options (such as the list of
                  capabilities and language resources
                  contained in the package)
                  can be configured using this package.

For publishing, Codemagic uses the[Partner Center submission API](https://docs.microsoft.com/azure/marketplace/azure-app-apis);
                  so, Codemagic requires[associating the Azure Active Directory
                    and Partner Center accounts](https://docs.microsoft.com/windows/uwp/publish/associate-azure-ad-with-partner-center).

#### GitHub Actions CI/CD

GitHub Actions can use the[Microsoft Dev Store CLI](https://learn.microsoft.com/windows/apps/publish/msstore-dev-cli/overview)to package applications into an MSIX and publish them to the Microsoft Store.
                  The[setup-msstore-cli](https://github.com/microsoft/setup-msstore-cli)GitHub Action installs the cli so that the Action can use it for packaging
                  and publishing.

As packaging the MSIX uses the[msixpub package](https://pub.dev/packages/msix), the project's`pubspec.yaml`must contain an appropriate`msix_config`node.

`msix`
`pubspec.yaml`
`msix_config`
You must create an Azure AD directory from the Dev Center with[global administrator permission](https://azure.microsoft.com/documentation/articles/active-directory-assign-admin-roles/).

The GitHub Action requires environment secrets from the partner center.`AZURE_AD_TENANT_ID`,`AZURE_AD_ClIENT_ID`, and`AZURE_AD_CLIENT_SECRET`are visible on the Dev Center following the instructions for the[Windows Store Publish Action](https://github.com/marketplace/actions/windows-store-publish#obtaining-your-credentials).
                  You also need the`SELLER_ID`secret, which can be found in the Dev Center
                  under**Account Settings**>**Organization Profile**>**Legal Info**.

`AZURE_AD_TENANT_ID`
`AZURE_AD_ClIENT_ID`
`AZURE_AD_CLIENT_SECRET`
`SELLER_ID`
The application must already be present in the Microsoft Dev Center with at
                  least one complete submission, and`msstore init`must be run once within
                  the repository before the Action can be performed. Once complete, running[msstore package .](https://learn.microsoft.com/windows/apps/publish/msstore-dev-cli/package-command)and[msstore publish](https://learn.microsoft.com/windows/apps/publish/msstore-dev-cli/publish-command)in a GitHub Action packages the
                  application into an MSIX and uploads it to a new submission on the dev center.

`msstore init`
`msstore package .`
`msstore publish`
The steps necessary for MSIX publishing resemble the following

`- uses: microsoft/setup-msstore-cli@v1
​
- name: Configure the Microsoft Store CLI
  run: msstore reconfigure --tenantId $ --clientId $ --clientSecret $ --sellerId $
​
- name: Install Dart dependencies
  run: flutter pub get
​
- name: Create MSIX package
  run: msstore package .
​
- name: Publish MSIX to the Microsoft Store
  run: msstore publish -v`
## Updating the app's version number

For apps published to the Microsoft Store,
                  the version number must be set during the
                  packaging process.

The default version number of the app is`1.0.0.0`.

`1.0.0.0`
For apps not published to the Microsoft Store, you
                  can set the app's executable's file and product versions.
                  The executable's default file version is`1.0.0.1`,
                  and its default product version is`1.0.0+1`. To update these,
                  navigate to the`pubspec.yaml`file and update the
                  following line:

`1.0.0.1`
`1.0.0+1`
`pubspec.yaml`
`version: 1.0.0+1`
The build name is three numbers separated by dots,
                  followed by an optional build number that is separated
                  by a`+`. In the example above, the build name is`1.0.0`and the build number is`1`.

`+`
`1.0.0`
`1`
The build name becomes the first three numbers of the
                  file and product versions, while the build number becomes
                  the fourth number of the file and product versions.

Both the build name and number can be overridden in`flutter build windows`by specifying`--build-name`and`--build-number`, respectively.

`flutter build windows`
`--build-name`
`--build-number`
## Add app icons

To update the icon of a Flutter Windows
                  desktop application before packaging use the
                  following instructions:

1. In the Flutter project, navigate to**windows\runner\resources**.
1. Replace the**app_icon.ico**with the desired icon.
1. If the name of the icon is other than**app_icon.ico**,
                    proceed to change the**IDI_APP_ICON**value in the**windows\runner\Runner.rc**file to point to the new path.

When packaging with the[msixpub package](https://pub.dev/packages/msix),
                  the logo path can also be configured inside the`pubspec.yaml`file.

`msix`
`pubspec.yaml`
To update the application image in the Store listing,
                  navigate to the Store listing step of the submission
                  and select Store logos.
                  From there, you can upload the logo with
                  the size of 300 x 300 pixels.

All uploaded images are retained for subsequent submissions.

## Validating the application package

Before publication to the Microsoft Store,
                  first validate the application package locally.

[Windows App Certification Kit](https://docs.microsoft.com/windows/uwp/debug-test-perf/windows-app-certification-kit)is a tool included in the
                  Windows Software Development Kit (SDK).

To validate the application:

1. Launch Windows App Cert Kit.
1. Select the Flutter Windows desktop package
                    (**.msix**,**.msixbundle**, etc.).
1. Choose a destination for the test report.

The report might contain important warnings and information,
                  even if the certification passes.

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/windows.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/deployment/windows&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/deployment/windows.md).
