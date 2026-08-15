> 原文链接: [https://docs.flutter.dev/release/breaking-changes](https://docs.flutter.dev/release/breaking-changes)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

As described in the[breaking change policy](https://docs.flutter.dev/release/compatibility-policy),
                  on occasion we publish guides
                  for migrating code across a breaking change.

To be notified about future breaking changes,
                  join the groups[Flutter announce](https://groups.google.com/forum/#!forum/flutter-announce)and[Dart announce](https://groups.google.com/a/dartlang.org/g/announce).

When facing Dart errors after upgrading Flutter,
                  consider using the[dart fix](https://docs.flutter.dev/tools/flutter-fix)command
                  to automatically migrate your code.
                  Not every breaking change is supported in this way,
                  but many are.

`dart fix`
To avoid being broken by future versions of Flutter,
                  consider submitting your tests to the framework's[test registry](https://github.com/flutter/tests).

## Breaking changes by release

The following guides are available.
                  They're sorted by release and listed in alphabetical order:

### Not yet released to stable

- [Changing RawMenuAnchor close order](https://docs.flutter.dev/release/breaking-changes/raw-menu-anchor-close-order)
- [DeprecateonReordercallback](https://docs.flutter.dev/release/breaking-changes/deprecate-onreorder-callback)
- [DeprecatedcacheExtentandcacheExtentStyle](https://docs.flutter.dev/release/breaking-changes/scroll-cache-extent)
- [DeprecateTextInputConnection.setStyle](https://docs.flutter.dev/release/breaking-changes/deprecate-text-input-connection-set-style)
- [IconDataclass marked asfinal](https://docs.flutter.dev/release/breaking-changes/icondata-class-marked-final)
- [Large screen orientation and resizability restrictions ignored on Android 17](https://docs.flutter.dev/release/breaking-changes/android-large-screens-restrictions-ignored)
- [ListTile reports error in debug when wrapped in a colored widget](https://docs.flutter.dev/release/breaking-changes/list-tile-color-warning)
- [Migrating Flutter Android projects to built-in Kotlin](https://docs.flutter.dev/release/breaking-changes/migrate-to-built-in-kotlin)
- [Page transition builders reorganization](https://docs.flutter.dev/release/breaking-changes/decouple-page-transition-builders)

`onReorder`
`cacheExtent`
`cacheExtentStyle`
`TextInputConnection.setStyle`
`IconData`
`final`
### Released in Flutter 3.41

- [Merged threads on Linux](https://docs.flutter.dev/release/breaking-changes/linux-merged-threads)
- [FontWeightalso controls the weight attribute of variable fonts](https://docs.flutter.dev/release/breaking-changes/font-weight-variation)
- [DeprecatecontainsSemanticsin favor ofisSemantics](https://docs.flutter.dev/release/breaking-changes/deprecate-contains-semantics)
- [DeprecatefindChildIndexCallbackin favor offindItemIndexCallbackinListViewandSliverListseparated constructors](https://docs.flutter.dev/release/breaking-changes/separated-builder-find-child-index-callback)
- [Material 3 tokens update](https://docs.flutter.dev/release/breaking-changes/material-color-utilities)

`FontWeight`
`containsSemantics`
`isSemantics`
`findChildIndexCallback`
`findItemIndexCallback`
`ListView`
`SliverList`
### Released in Flutter 3.38

- [CupertinoDynamicColorwide gamut support](https://docs.flutter.dev/release/breaking-changes/wide-gamut-cupertino-dynamic-color)
- [DeprecateOverlayPortal.targetsRootOverlay](https://docs.flutter.dev/release/breaking-changes/deprecate-overlay-portal-targets-root)
- [DeprecateSemanticsProperties.focusableandSemanticsConfiguration.isFocusable](https://docs.flutter.dev/release/breaking-changes/deprecate-focusable)
- [SnackBar with action no longer auto-dismisses](https://docs.flutter.dev/release/breaking-changes/snackbar-with-action-behavior-update)
- [The default page transition on Android is nowPredictiveBackPageTransitionBuilder](https://docs.flutter.dev/release/breaking-changes/default-android-page-transition)
- [UISceneDelegate adoption](https://docs.flutter.dev/release/breaking-changes/uiscenedelegate)

`CupertinoDynamicColor`
`OverlayPortal.targetsRootOverlay`
`SemanticsProperties.focusable`
`SemanticsConfiguration.isFocusable`
`PredictiveBackPageTransitionBuilder`
### Released in Flutter 3.35

- [Component theme normalization updates](https://docs.flutter.dev/release/breaking-changes/component-theme-normalization-updates)
- [DeprecateDropdownButtonFormFieldvalueparameter in favor ofinitialValue](https://docs.flutter.dev/release/breaking-changes/deprecate-dropdownbuttonformfield-value)
- [Deprecate app bar color](https://docs.flutter.dev/release/breaking-changes/appbar-theme-color)
- [Redesigned theRadiowidget](https://docs.flutter.dev/release/breaking-changes/radio-api-redesign)
- [Removed semantics elevation and thickness](https://docs.flutter.dev/release/breaking-changes/remove-semantics-elevation-and-thickness)
- [TheFormwidget no longer supports being a sliver](https://docs.flutter.dev/release/breaking-changes/form-semantics)
- [Flutter now sets defaultabiFiltersin Android builds](https://docs.flutter.dev/release/breaking-changes/default-abi-filters-android)
- [Merged threads on macOS and Windows](https://docs.flutter.dev/release/breaking-changes/macos-windows-merged-threads)
- [TheVisibilitywidget is no longer focusable by default whenmaintainStateis enabled](https://docs.flutter.dev/release/breaking-changes/visibility-maintainfocusability)
- [$FLUTTER_ROOT/versionreplaced by$FLUTTER_ROOT/bin/cache/flutter.version.json](https://docs.flutter.dev/release/breaking-changes/flutter-root-version-file)

`DropdownButtonFormField`
`value`
`initialValue`
`Radio`
`Form`
`abiFilters`
`Visibility`
`maintainState`
`$FLUTTER_ROOT/version`
`$FLUTTER_ROOT/bin/cache/flutter.version.json`
### Released in Flutter 3.32

- [DeprecateSystemContextMenuController.show](https://docs.flutter.dev/release/breaking-changes/system_context_menu_controller_show)
- [DeprecateExpansionTileControllerin favor ofExpansibleController](https://docs.flutter.dev/release/breaking-changes/expansion-tile-controller)
- [DeprecateRouteTransitionRecord.markForRemove](https://docs.flutter.dev/release/breaking-changes/navigator-complete-route)in favor of`RouteTransitionRecord.markForComplete`
- [DeprecateThemeData.indicatorColorin favor ofTabBarThemeData.indicatorColor](https://docs.flutter.dev/release/breaking-changes/deprecate-themedata-indicatorcolor)
- [Material Theme System Updates](https://docs.flutter.dev/release/breaking-changes/material-theme-system-updates)
- [.flutter-plugins-dependenciesreplaces.flutter-plugins](https://docs.flutter.dev/release/breaking-changes/flutter-plugins-configuration)
- [Localized messages are generated into source, not a synthetic package](https://docs.flutter.dev/release/breaking-changes/flutter-generate-i10n-source)
- [Changing the defaultgoldenFileComparatorforintegration_tests](https://docs.flutter.dev/release/breaking-changes/integration-test-default-golden-comparator)
- [DeprecateInputDecoration.maintainHintHeightin favor ofInputDecoration.maintainHintSize](https://docs.flutter.dev/release/breaking-changes/deprecate-inputdecoration-maintainhintheight)
- [Underdamped spring formula changed](https://docs.flutter.dev/release/breaking-changes/spring-description-underdamped)

`SystemContextMenuController.show`
`ExpansionTileController`
`ExpansibleController`
`RouteTransitionRecord.markForRemove`
`RouteTransitionRecord.markForComplete`
`ThemeData.indicatorColor`
`TabBarThemeData.indicatorColor`
`.flutter-plugins-dependencies`
`.flutter-plugins`
`goldenFileComparator`
`integration_test`
`InputDecoration.maintainHintHeight`
`InputDecoration.maintainHintSize`
### Released in Flutter 3.29

- [Removal of v1 Android embedding Java APIs](https://docs.flutter.dev/release/breaking-changes/v1-android-embedding)
- [DeprecateWebGoldenComparator](https://docs.flutter.dev/release/breaking-changes/web-golden-comparator)
- [DeprecateThemeData.dialogBackgroundColorin favor ofDialogThemeData.backgroundColor](https://docs.flutter.dev/release/breaking-changes/deprecate-themedata-dialogbackgroundcolor)
- [ImageFilter.blurdefault tile mode automatic selection](https://docs.flutter.dev/release/breaking-changes/image-filter-blur-tilemode)
- [Updated Material 3Slider](https://docs.flutter.dev/release/breaking-changes/updated-material-3-slider)
- [Updated Material 3 progress indicators](https://docs.flutter.dev/release/breaking-changes/updated-material-3-progress-indicators)

`WebGoldenComparator`
`ThemeData.dialogBackgroundColor`
`DialogThemeData.backgroundColor`
`ImageFilter.blur`
`Slider`
### Released in Flutter 3.27

- [Colorwide gamut support](https://docs.flutter.dev/release/breaking-changes/wide-gamut-framework)
- [Component theme normalization](https://docs.flutter.dev/release/breaking-changes/component-theme-normalization)
- [Deep links flag change](https://docs.flutter.dev/release/breaking-changes/deep-links-flag-change)
- [Material 3 Tokens Update in Flutter](https://docs.flutter.dev/release/breaking-changes/material-design-3-token-update)
- [Remove invalid parameters forInputDecoration.collapsed](https://docs.flutter.dev/release/breaking-changes/input-decoration-collapsed)
- [Set default for SystemUiMode to Edge-to-Edge](https://docs.flutter.dev/release/breaking-changes/default-systemuimode-edge-to-edge)

`Color`
`InputDecoration.collapsed`
### Released in Flutter 3.24

- [Navigator's page APIs breaking change](https://docs.flutter.dev/release/breaking-changes/navigator-and-page-api)
- [Generic types inPopScope](https://docs.flutter.dev/release/breaking-changes/popscope-with-result)
- [DeprecateButtonBarin favor ofOverflowBar](https://docs.flutter.dev/release/breaking-changes/deprecate-buttonbar)
- [New APIs for Android plugins that render to aSurface](https://docs.flutter.dev/release/breaking-changes/android-surface-plugins)

`PopScope`
`ButtonBar`
`OverflowBar`
`Surface`
### Released in Flutter 3.22

- [Deprecated API removed after v3.19](https://docs.flutter.dev/release/breaking-changes/3-19-deprecations)
- [RenameMaterialStatetoWidgetState](https://docs.flutter.dev/release/breaking-changes/material-state)
- [Introduce newColorSchemeroles](https://docs.flutter.dev/release/breaking-changes/new-color-scheme-roles)
- [Dropping support for Android KitKat](https://docs.flutter.dev/release/breaking-changes/android-kitkat-deprecation)
- [NullablePageView.controller](https://docs.flutter.dev/release/breaking-changes/pageview-controller)
- [RenameMemoryAllocationstoFlutterMemoryAllocations](https://docs.flutter.dev/release/breaking-changes/flutter-memory-allocations)

`MaterialState`
`WidgetState`
`ColorScheme`
`PageView.controller`
`MemoryAllocations`
`FlutterMemoryAllocations`
### Released in Flutter 3.19

- [Deprecated API removed after v3.16](https://docs.flutter.dev/release/breaking-changes/3-16-deprecations)
- [Migrate RawKeyEvent/RawKeyboard system to KeyEvent/HardwareKeyboard system](https://docs.flutter.dev/release/breaking-changes/key-event-migration)
- [Deprecate imperative apply of Flutter's Gradle plugins](https://docs.flutter.dev/release/breaking-changes/flutter-gradle-plugin-apply)
- [Default multitouch scrolling](https://docs.flutter.dev/release/breaking-changes/multi-touch-scrolling)
- [Accessibility traversal order of tooltip changed](https://docs.flutter.dev/release/breaking-changes/tooltip-semantics-order)
- [Stop generatingAssetManifest.json](https://docs.flutter.dev/release/breaking-changes/asset-manifest-dot-json)

`AssetManifest.json`
### Released in Flutter 3.16

- [Migrating to Material 3](https://docs.flutter.dev/release/breaking-changes/material-3-migration)
- [Migrate ShortcutActivator and ShortcutManager to KeyEvent system](https://docs.flutter.dev/release/breaking-changes/shortcut-key-event-migration)
- [TheThemeData.useMaterial3property is now set to true by default](https://docs.flutter.dev/release/breaking-changes/material-3-default)
- [Deprecated API removed after v3.13](https://docs.flutter.dev/release/breaking-changes/3-13-deprecations)
- [Customize tabs alignment using the newTabBar.tabAlignmentproperty](https://docs.flutter.dev/release/breaking-changes/tab-alignment)
- [DeprecatetextScaleFactorin favor ofTextScaler](https://docs.flutter.dev/release/breaking-changes/deprecate-textscalefactor)
- [Android 14 nonlinear font scaling enabled](https://docs.flutter.dev/release/breaking-changes/android-14-nonlinear-text-scaling-migration)
- [DeprecatedescribeEnumand updateEnumPropertyto be type strict](https://docs.flutter.dev/release/breaking-changes/describe-enum)
- [Deprecated just-in-time navigation pop APIs for Android Predictive Back](https://docs.flutter.dev/release/breaking-changes/android-predictive-back)
- [DeprecatedPaint.enableDithering](https://docs.flutter.dev/release/breaking-changes/paint-enableDithering)
- [Updated default text styles for menus](https://docs.flutter.dev/release/breaking-changes/menus-text-style)
- [Windows: External windows should notify Flutter engine of lifecycle changes](https://docs.flutter.dev/release/breaking-changes/win-lifecycle-process-function)
- [Windows build path changed to add the target architecture](https://docs.flutter.dev/release/breaking-changes/windows-build-architecture)

`ThemeData.useMaterial3`
`TabBar.tabAlignment`
`textScaleFactor`
`TextScaler`
`describeEnum`
`EnumProperty`
`Paint.enableDithering`
### Released in Flutter 3.13

- [Added missingdispose()for some disposable objects in Flutter](https://docs.flutter.dev/release/breaking-changes/dispose)
- [Deprecated API removed after v3.10](https://docs.flutter.dev/release/breaking-changes/3-10-deprecations)
- [Added AppLifecycleState.hidden](https://docs.flutter.dev/release/breaking-changes/add-applifecyclestate-hidden)enum value
- [Moved ReorderableListView's localized strings](https://docs.flutter.dev/release/breaking-changes/material-localized-strings)from material to widgets localizations
- [RemovedignoringSemantics](https://docs.flutter.dev/release/breaking-changes/ignoringsemantics-migration)properties
- [DeprecatedRouteInformation.location](https://docs.flutter.dev/release/breaking-changes/route-information-uri)and its related APIs
- [Updated EditableText scroll into view behavior](https://docs.flutter.dev/release/breaking-changes/editable-text-scroll-into-view)
- [Migrate a Windows project to ensure the window is shown](https://docs.flutter.dev/release/breaking-changes/windows-show-window-migration)
- [UpdatedCheckbox.fillColorbehavior](https://docs.flutter.dev/release/breaking-changes/checkbox-fillColor)

`dispose()`
`ignoringSemantics`
`RouteInformation.location`
`Checkbox.fillColor`
### Released in Flutter 3.10

- [Dart 3 changes in Flutter v3.10 and later](https://dart.dev/resources/dart-3-migration)
- [Deprecated API removed after v3.7](https://docs.flutter.dev/release/breaking-changes/3-7-deprecations)
- [Insert content text input client](https://docs.flutter.dev/release/breaking-changes/insert-content-text-input-client)
- [Deprecated the window singleton](https://docs.flutter.dev/release/breaking-changes/window-singleton)
- [Resolve the Android Java Gradle error](https://docs.flutter.dev/release/breaking-changes/android-java-gradle-migration-guide)
- [Require one data variant forClipboardDataconstructor](https://docs.flutter.dev/release/breaking-changes/clipboard-data-required)
- ["Zone mismatch" message](https://docs.flutter.dev/release/breaking-changes/zone-errors)

`ClipboardData`
### Released in Flutter 3.7

- [Deprecated API removed after v3.3](https://docs.flutter.dev/release/breaking-changes/3-3-deprecations)
- [Replaced parameters for customizing context menus with a generic widget builder](https://docs.flutter.dev/release/breaking-changes/context-menus)
- [iOS FlutterViewController splashScreenView made nullable](https://docs.flutter.dev/release/breaking-changes/ios-flutterviewcontroller-splashscreenview-nullable)
- [Migrateofto non-nullable return values, and addmaybeOf](https://docs.flutter.dev/release/breaking-changes/supplemental-maybeOf-migration)
- [Removed RouteSettings.copyWith](https://docs.flutter.dev/release/breaking-changes/routesettings-copywith-migration)
- [ThemeData's toggleableActiveColor property has been deprecated](https://docs.flutter.dev/release/breaking-changes/toggleable-active-color)
- [Migrate a Windows project to support dark title bars](https://docs.flutter.dev/release/breaking-changes/windows-dark-mode)

`of`
`maybeOf`
### Released in Flutter 3.3

- [Adding ImageProvider.loadBuffer](https://docs.flutter.dev/release/breaking-changes/image-provider-load-buffer)
- [Default PrimaryScrollController on Desktop](https://docs.flutter.dev/release/breaking-changes/primary-scroll-controller-desktop)
- [Trackpad gestures can trigger GestureRecognizer](https://docs.flutter.dev/release/breaking-changes/trackpad-gestures)
- [Migrate a Windows project to set version information](https://docs.flutter.dev/release/breaking-changes/windows-version-information)

### Released in Flutter 3

- [Deprecated API removed after v2.10](https://docs.flutter.dev/release/breaking-changes/2-10-deprecations)
- [Migrate useDeleteButtonTooltip to deleteButtonTooltipMessage of Chips](https://docs.flutter.dev/release/breaking-changes/chip-usedeletebuttontooltip-migration)
- [Page transitions replaced by ZoomPageTransitionsBuilder](https://docs.flutter.dev/release/breaking-changes/page-transition-replaced-by-ZoomPageTransitionBuilder)

### Released in Flutter 2.10

- [Deprecated API removed after v2.5](https://docs.flutter.dev/release/breaking-changes/2-5-deprecations)
- [Raw images on Web uses correct origin and colors](https://docs.flutter.dev/release/breaking-changes/raw-images-on-web-uses-correct-origin-and-colors)
- [Required Kotlin version](https://docs.flutter.dev/release/breaking-changes/kotlin-version)
- [Scribble Text Input Client](https://docs.flutter.dev/release/breaking-changes/scribble-text-input-client)

### Released in Flutter 2.5

- [Default drag scrolling devices](https://docs.flutter.dev/release/breaking-changes/default-scroll-behavior-drag)
- [Deprecated API removed after v2.2](https://docs.flutter.dev/release/breaking-changes/2-2-deprecations)
- [Change the enterText method to move the caret to the end of the input text](https://docs.flutter.dev/release/breaking-changes/enterText-trailing-caret)
- [GestureRecognizer cleanup](https://docs.flutter.dev/release/breaking-changes/gesture-recognizer-add-allowed-pointer)
- [Introducing package:flutter_lints](https://docs.flutter.dev/release/breaking-changes/flutter-lints-package)
- [Replace AnimationSheetBuilder.display with collate](https://docs.flutter.dev/release/breaking-changes/animation-sheet-builder-display)
- [ThemeData's accent properties have been deprecated](https://docs.flutter.dev/release/breaking-changes/theme-data-accent-properties)
- [Transition of platform channel test interfaces to flutter_test package](https://docs.flutter.dev/release/breaking-changes/mock-platform-channels)
- [Using HTML slots to render platform views in the web](https://docs.flutter.dev/release/breaking-changes/platform-views-using-html-slots-web)
- [Migrate a Windows project to the idiomatic run loop](https://docs.flutter.dev/release/breaking-changes/windows-run-loop)

### Reverted change in 2.2

The following breaking change was reverted in release 2.2:

Introduced in version: 2.0.0
Reverted in version:   2.2.0

### Released in Flutter 2.2

- [Default Scrollbars on Desktop](https://docs.flutter.dev/release/breaking-changes/default-desktop-scrollbars)

### Released in Flutter 2

- [Added BuildContext parameter to TextEditingController.buildTextSpan](https://docs.flutter.dev/release/breaking-changes/buildtextspan-buildcontext)
- [Android ActivityControlSurface attachToActivity signature change](https://docs.flutter.dev/release/breaking-changes/android-activity-control-surface-attach)
- [Android FlutterMain.setIsRunningInRobolectricTest testing API removed](https://docs.flutter.dev/release/breaking-changes/android-setIsRunningInRobolectricTest-removed)
- [Clip behavior](https://docs.flutter.dev/release/breaking-changes/clip-behavior)
- [Deprecated API removed after v1.22](https://docs.flutter.dev/release/breaking-changes/1-22-deprecations)
- [Dry layout support for RenderBox](https://docs.flutter.dev/release/breaking-changes/renderbox-dry-layout)
- [Eliminating nullOk Parameters](https://docs.flutter.dev/release/breaking-changes/eliminating-nullok-parameters)
- [Material Chip button semantics](https://docs.flutter.dev/release/breaking-changes/material-chip-button-semantics)
- [SnackBars managed by the ScaffoldMessenger](https://docs.flutter.dev/release/breaking-changes/scaffold-messenger)
- [TextSelectionTheme migration](https://docs.flutter.dev/release/breaking-changes/text-selection-theme)
- [Transition of platform channel test interfaces to flutter_test package](https://docs.flutter.dev/release/breaking-changes/mock-platform-channels)
- [Use maxLengthEnforcement instead of maxLengthEnforced](https://docs.flutter.dev/release/breaking-changes/use-maxLengthEnforcement-instead-of-maxLengthEnforced)

### Released in Flutter 1.22

- [Android v1 embedding app and plugin creation deprecation](https://docs.flutter.dev/release/breaking-changes/android-v1-embedding-create-deprecation)
- [Cupertino icons 1.0.0](https://docs.flutter.dev/release/breaking-changes/cupertino-icons-1.0.0)
- [The new Form, FormField auto-validation API](https://docs.flutter.dev/release/breaking-changes/form-field-autovalidation-api)

### Released in Flutter 1.20

- [Actions API revision](https://docs.flutter.dev/release/breaking-changes/actions-api-revision)
- [Adding TextInputClient.currentAutofillScope property](https://docs.flutter.dev/release/breaking-changes/add-currentAutofillScope-to-TextInputClient)
- [New Buttons and Button Themes](https://docs.flutter.dev/release/breaking-changes/buttons)
- [Dialogs' Default BorderRadius](https://docs.flutter.dev/release/breaking-changes/dialog-border-radius)
- [More Strict Assertions in the Navigator and the Hero Controller Scope](https://docs.flutter.dev/release/breaking-changes/hero-controller-scope)
- [The Route Transition record and Transition delegate updates](https://docs.flutter.dev/release/breaking-changes/route-transition-record-and-transition-delegate)
- [The RenderEditable needs to be laid out before hit testing](https://docs.flutter.dev/release/breaking-changes/rendereditable-layout-before-hit-test)
- [Reversing the dependency between the scheduler and services layer](https://docs.flutter.dev/release/breaking-changes/services-scheduler-dependency-reversed)
- [Semantics Order of the Overlay Entries in Modal Routes](https://docs.flutter.dev/release/breaking-changes/modal-router-semantics-order)
- [showAutocorrectionPromptRect method added to TextInputClient](https://docs.flutter.dev/release/breaking-changes/add-showAutocorrectionPromptRect)
- [TestWidgetsFlutterBinding.clock](https://docs.flutter.dev/release/breaking-changes/test-widgets-flutter-binding-clock)
- [TextField requires MaterialLocalizations](https://docs.flutter.dev/release/breaking-changes/text-field-material-localizations)

### Released in Flutter 1.17

- [Adding 'linux' and 'windows' to TargetPlatform enum](https://docs.flutter.dev/release/breaking-changes/target-platform-linux-windows)
- [Annotations return local position relative to object](https://docs.flutter.dev/release/breaking-changes/annotations-return-local-position-relative-to-object)
- [Container color optimization](https://docs.flutter.dev/release/breaking-changes/container-color)
- [CupertinoTabBar requires Localizations parent](https://docs.flutter.dev/release/breaking-changes/cupertino-tab-bar-localizations)
- [Generic type of ParentDataWidget changed to ParentData](https://docs.flutter.dev/release/breaking-changes/parent-data-widget-generic-type)
- [ImageCache and ImageProvider changes](https://docs.flutter.dev/release/breaking-changes/image-cache-and-provider)
- [ImageCache large images](https://docs.flutter.dev/release/breaking-changes/imagecache-large-images)
- [MouseTracker moved to rendering](https://docs.flutter.dev/release/breaking-changes/mouse-tracker-moved-to-rendering)
- [MouseTracker no longer attaches annotations](https://docs.flutter.dev/release/breaking-changes/mouse-tracker-no-longer-attaches-annotations)
- [Nullable CupertinoTheme.brightness](https://docs.flutter.dev/release/breaking-changes/nullable-cupertinothemedata-brightness)
- [Rebuild optimization for OverlayEntries and Routes](https://docs.flutter.dev/release/breaking-changes/overlay-entry-rebuilds)
- [Scrollable AlertDialog](https://docs.flutter.dev/release/breaking-changes/scrollable-alert-dialog)
- [TestTextInput state reset](https://docs.flutter.dev/release/breaking-changes/test-text-input)
- [TextInputClient currentTextEditingValue](https://docs.flutter.dev/release/breaking-changes/text-input-client-current-value)
- [The forgetChild() method must call super](https://docs.flutter.dev/release/breaking-changes/forgetchild-call-super)
- [The Route and Navigator refactoring](https://docs.flutter.dev/release/breaking-changes/route-navigator-refactoring)
- [FloatingActionButton and ThemeData's accent properties](https://docs.flutter.dev/release/breaking-changes/fab-theme-data-accent-properties)

Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/release/breaking-changes/index.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/release/breaking-changes&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/release/breaking-changes/index.md).
