> 原文链接: [https://docs.flutter.dev/ui/animations/overview](https://docs.flutter.dev/ui/animations/overview)
---

Flutter is back at Google I/O on May 19-20![Register now](https://io.google/2026/?utm_source=flutter&utm_medium=embedded_marketing&utm_campaign=flutter)

The animation system in Flutter is based on typed[Animation](https://api.flutter.dev/flutter/animation/Animation-class.html)objects. Widgets can either
                  incorporate these animations in their build
                  functions directly by reading their current value and listening to their
                  state changes or they can use the animations as the basis of more elaborate
                  animations that they pass along to other widgets.

`Animation`
## Animation

The primary building block of the animation system is the[Animation](https://api.flutter.dev/flutter/animation/Animation-class.html)class. An animation represents a value
                  of a specific type that can change over the lifetime of
                  the animation. Most widgets that perform an animation
                  receive an`Animation`object as a parameter,
                  from which they read the current value of the animation
                  and to which they listen for changes to that value.

`Animation`
`Animation`
### addListener

`addListener`
Whenever the animation's value changes,
                  the animation notifies all the listeners added with[addListener](https://api.flutter.dev/flutter/animation/Animation/addListener.html). Typically, a[State](https://api.flutter.dev/flutter/widgets/State-class.html)object that listens to an animation calls[setState](https://api.flutter.dev/flutter/widgets/State/setState.html)on itself in its listener callback
                  to notify the widget system that it needs to
                  rebuild with the new value of the animation.

`addListener`
`State`
`setState`
This pattern is so common that there are two widgets
                  that help widgets rebuild when animations change value:[AnimatedWidget](https://api.flutter.dev/flutter/widgets/AnimatedWidget-class.html)and[AnimatedBuilder](https://api.flutter.dev/flutter/widgets/AnimatedBuilder-class.html).
                  The first,`AnimatedWidget`, is most useful for
                  stateless animated widgets. To use`AnimatedWidget`,
                  simply subclass it and implement the[build](https://api.flutter.dev/flutter/widgets/AnimatedWidget/build.html)function.
                  The second,`AnimatedBuilder`, is useful for more complex widgets
                  that wish to include an animation as part of a larger build function.
                  To use`AnimatedBuilder`, simply construct the widget
                  and pass it a`builder`function.

`AnimatedWidget`
`AnimatedBuilder`
`AnimatedWidget`
`AnimatedWidget`
`build`
`AnimatedBuilder`
`AnimatedBuilder`
`builder`
### addStatusListener

`addStatusListener`
Animations also provide an[AnimationStatus](https://api.flutter.dev/flutter/animation/AnimationStatus.html),
                  which indicates how the animation will evolve over time.
                  Whenever the animation's status changes,
                  the animation notifies all the listeners added with[addStatusListener](https://api.flutter.dev/flutter/animation/Animation/addStatusListener.html). Typically, animations start
                  out in the`dismissed`status, which means they're
                  at the beginning of their range. For example,
                  animations that progress from 0.0 to 1.0
                  will be`dismissed`when their value is 0.0.
                  An animation might then run`forward`(from 0.0 to 1.0)
                  or perhaps in`reverse`(from 1.0 to 0.0).
                  Eventually, if the animation reaches the end of its range
                  (1.0), the animation reaches the`completed`status.

`AnimationStatus`
`addStatusListener`
`dismissed`
`dismissed`
`forward`
`reverse`
`completed`
## Animation­Controller

To create an animation, first create an[AnimationController](https://api.flutter.dev/flutter/animation/AnimationController-class.html).
                  As well as being an animation itself, an`AnimationController`lets you control the animation. For example,
                  you can tell the controller to play the animation[forward](https://api.flutter.dev/flutter/animation/AnimationController/forward.html)or[stop](https://api.flutter.dev/flutter/animation/AnimationController/stop.html)the animation.
                  You can also[fling](https://api.flutter.dev/flutter/animation/AnimationController/fling.html)animations,
                  which uses a physical simulation, such as a spring,
                  to drive the animation.

`AnimationController`
`AnimationController`
`forward`
`stop`
`fling`
Once you've created an animation controller,
                  you can start building other animations based on it.
                  For example, you can create a[ReverseAnimation](https://api.flutter.dev/flutter/animation/ReverseAnimation-class.html)that mirrors the original animation but runs in the
                  opposite direction (from 1.0 to 0.0).
                  Similarly, you can create a[CurvedAnimation](https://api.flutter.dev/flutter/animation/CurvedAnimation-class.html)whose value is adjusted by a[Curve](https://api.flutter.dev/flutter/animation/Curves-class.html).

`ReverseAnimation`
`CurvedAnimation`
`Curve`
## Tweens

To animate beyond the 0.0 to 1.0 interval, you can use a[Tween<T>](https://api.flutter.dev/flutter/animation/Tween-class.html), which interpolates between its[begin](https://api.flutter.dev/flutter/animation/Tween/begin.html)and[end](https://api.flutter.dev/flutter/animation/Tween/end.html)values. Many types have specific`Tween`subclasses that provide type-specific interpolation.
                  For example,[ColorTween](https://api.flutter.dev/flutter/animation/ColorTween-class.html)interpolates between colors and[RectTween](https://api.flutter.dev/flutter/animation/RectTween-class.html)interpolates between rects.
                  You can define your own interpolations by creating
                  your own subclass of`Tween`and overriding its[lerp](https://api.flutter.dev/flutter/animation/Tween/lerp.html)function.

`Tween<T>`
`begin`
`end`
`Tween`
`ColorTween`
`RectTween`
`Tween`
`lerp`
By itself, a tween just defines how to interpolate
                  between two values. To get a concrete value for the
                  current frame of an animation, you also need an
                  animation to determine the current state.
                  There are two ways to combine a tween
                  with an animation to get a concrete value:


You can[evaluate](https://api.flutter.dev/flutter/animation/Animatable/evaluate.html)the tween at the current
                      value of an animation. This approach is most useful
                      for widgets that are already listening to the animation and hence
                      rebuilding whenever the animation changes value.

`evaluate`
You can[animate](https://api.flutter.dev/flutter/animation/Animatable/animate.html)the tween based on the animation.
                      Rather than returning a single value, the animate function
                      returns a new`Animation`that incorporates the tween.
                      This approach is most useful when you want to give the
                      newly created animation to another widget,
                      which can then read the current value that incorporates
                      the tween as well as listen for changes to the value.

`animate`
`Animation`
## Architecture

Animations are actually built from a number of core building blocks.

### Scheduler

The[SchedulerBinding](https://api.flutter.dev/flutter/scheduler/SchedulerBinding-mixin.html)is a singleton class
                  that exposes the Flutter scheduling primitives.

`SchedulerBinding`
For this discussion, the key primitive is the frame callbacks.
                  Each time a frame needs to be shown on the screen,
                  Flutter's engine triggers a "begin frame" callback that
                  the scheduler multiplexes to all the listeners registered using[scheduleFrameCallback()](https://api.flutter.dev/flutter/scheduler/SchedulerBinding/scheduleFrameCallback.html). All these callbacks are
                  given the official time stamp of the frame, in
                  the form of a`Duration`from some arbitrary epoch. Since all the
                  callbacks have the same time, any animations triggered from these
                  callbacks will appear to be exactly synchronised even
                  if they take a few milliseconds to be executed.

`scheduleFrameCallback()`
`Duration`
### Tickers

The[Ticker](https://api.flutter.dev/flutter/scheduler/Ticker-class.html)class hooks into the scheduler's[scheduleFrameCallback()](https://api.flutter.dev/flutter/scheduler/SchedulerBinding/scheduleFrameCallback.html)mechanism to invoke a callback every tick.

`Ticker`
`scheduleFrameCallback()`
A`Ticker`can be started and stopped. When started,
                  it returns a`Future`that will resolve when it is stopped.

`Ticker`
`Future`
Each tick, the`Ticker`provides the callback with the
                  duration since the first tick after it was started.

`Ticker`
Because tickers always give their elapsed time relative to the first
                  tick after they were started; tickers are all synchronised. If you
                  start three tickers at different times between two ticks, they will all
                  nonetheless be synchronised with the same starting time, and will
                  subsequently tick in lockstep. Like people at a bus-stop,
                  all the tickers wait for a regularly occurring event
                  (the tick) to begin moving (counting time).

### Simulations

The[Simulation](https://api.flutter.dev/flutter/physics/Simulation-class.html)abstract class maps a
                  relative time value (an elapsed time) to a
                  double value, and has a notion of completion.

`Simulation`
In principle simulations are stateless but in practice
                  some simulations (for example,[BouncingScrollSimulation](https://api.flutter.dev/flutter/widgets/BouncingScrollSimulation-class.html)and[ClampingScrollSimulation](https://api.flutter.dev/flutter/widgets/ClampingScrollSimulation-class.html))
                  change state irreversibly when queried.

`BouncingScrollSimulation`
`ClampingScrollSimulation`
There are[various concrete implementations](https://api.flutter.dev/flutter/physics/physics-library.html)of the`Simulation`class for different effects.

`Simulation`
### Animatables

The[Animatable](https://api.flutter.dev/flutter/animation/Animatable-class.html)abstract class maps a
                  double to a value of a particular type.

`Animatable`
`Animatable`classes are stateless and immutable.

`Animatable`
#### Tweens

The[Tween<T>](https://api.flutter.dev/flutter/animation/Tween-class.html)abstract class maps a double
                  value nominally in the range 0.0-1.0 to a typed value
                  (for example, a`Color`, or another double).
                  It is an`Animatable`.

`Tween<T>`
`Color`
`Animatable`
It has a notion of an output type (`T`),
                  a`begin`value and an`end`value of that type,
                  and a way to interpolate (`lerp`) between the begin
                  and end values for a given input value (the double nominally in
                  the range 0.0-1.0).

`T`
`begin`
`end`
`lerp`
`Tween`classes are stateless and immutable.

`Tween`
#### Composing animatables

Passing an`Animatable<double>`(the parent) to an`Animatable`'s`chain()`method creates a new`Animatable`subclass that applies the
                  parent's mapping then the child's mapping.

`Animatable<double>`
`Animatable`
`chain()`
`Animatable`
### Curves

The[Curve](https://api.flutter.dev/flutter/animation/Curves-class.html)abstract class maps doubles
                  nominally in the range 0.0-1.0 to doubles
                  nominally in the range 0.0-1.0.

`Curve`
`Curve`classes are stateless and immutable.

`Curve`
### Animations

The[Animation](https://api.flutter.dev/flutter/animation/Animation-class.html)abstract class provides a
                  value of a given type, a concept of animation
                  direction and animation status, and a listener interface to
                  register callbacks that get invoked when the value or status change.

`Animation`
Some subclasses of`Animation`have values that never change
                  ([kAlwaysCompleteAnimation](https://api.flutter.dev/flutter/animation/kAlwaysCompleteAnimation-constant.html),[kAlwaysDismissedAnimation](https://api.flutter.dev/flutter/animation/kAlwaysDismissedAnimation-constant.html),[AlwaysStoppedAnimation](https://api.flutter.dev/flutter/animation/AlwaysStoppedAnimation-class.html)); registering callbacks on
                  these has no effect as the callbacks are never called.

`Animation`
`kAlwaysCompleteAnimation`
`kAlwaysDismissedAnimation`
`AlwaysStoppedAnimation`
The`Animation<double>`variant is special because it can be used to
                  represent a double nominally in the range 0.0-1.0, which is the input
                  expected by`Curve`and`Tween`classes, as well as some further
                  subclasses of`Animation`.

`Animation<double>`
`Curve`
`Tween`
`Animation`
Some`Animation`subclasses are stateless,
                  merely forwarding listeners to their parents.
                  Some are very stateful.

`Animation`
#### Composable animations

Most`Animation`subclasses take an explicit "parent"`Animation<double>`. They are driven by that parent.

`Animation`
`Animation<double>`
The`CurvedAnimation`subclass takes an`Animation<double>`class (the
                  parent) and a couple of`Curve`classes (the forward and reverse
                  curves) as input, and uses the value of the parent as input to the
                  curves to determine its output.`CurvedAnimation`is immutable and
                  stateless.

`CurvedAnimation`
`Animation<double>`
`Curve`
`CurvedAnimation`
The`ReverseAnimation`subclass takes an`Animation<double>`class as its parent and reverses
                  all the values of the animation. It assumes the parent
                  is using a value nominally in the range 0.0-1.0 and returns
                  a value in the range 1.0-0.0. The status and direction of the parent
                  animation are also reversed.`ReverseAnimation`is immutable and
                  stateless.

`ReverseAnimation`
`Animation<double>`
`ReverseAnimation`
The`ProxyAnimation`subclass takes an`Animation<double>`class as
                  its parent and merely forwards the current state of that parent.
                  However, the parent is mutable.

`ProxyAnimation`
`Animation<double>`
The`TrainHoppingAnimation`subclass takes two parents,
                  and switches between them when their values cross.

`TrainHoppingAnimation`
#### Animation controllers

The[AnimationController](https://api.flutter.dev/flutter/animation/AnimationController-class.html)is a stateful`Animation<double>`that uses a`Ticker`to give itself life.
                  It can be started and stopped. At each tick, it takes the time
                  elapsed since it was started and passes it to a`Simulation`to obtain
                  a value. That is then the value it reports. If the`Simulation`reports that at that time it has ended, then the controller stops
                  itself.

`AnimationController`
`Animation<double>`
`Ticker`
`Simulation`
`Simulation`
The animation controller can be given a lower and upper bound to
                  animate between, and a duration.

In the simple case (using`forward()`or`reverse()`), the animation controller simply does a linear
                  interpolation from the lower bound to the upper bound (or vice versa,
                  for the reverse direction) over the given duration.

`forward()`
`reverse()`
When using`repeat()`, the animation controller uses a linear
                  interpolation between the given bounds over the given duration, but
                  does not stop.

`repeat()`
When using`animateTo()`, the animation controller does a linear
                  interpolation over the given duration from the current value to the
                  given target. If no duration is given to the method, the default
                  duration of the controller and the range described by the controller's
                  lower bound and upper bound is used to determine the velocity of the
                  animation.

`animateTo()`
When using`fling()`, a`Force`is used to create a specific
                  simulation which is then used to drive the controller.

`fling()`
`Force`
When using`animateWith()`, the given simulation is used to drive the
                  controller.

`animateWith()`
These methods all return the future that the`Ticker`provides and
                  which will resolve when the controller next stops or changes
                  simulation.

`Ticker`
#### Attaching animatables to animations

Passing an`Animation<double>`(the new parent) to an`Animatable`'s`animate()`method creates a new`Animation`subclass that acts like
                  the`Animatable`but is driven from the given parent.

`Animation<double>`
`Animatable`
`animate()`
`Animation`
`Animatable`
Unless stated otherwise, the documentation on this site reflects Flutter 3.41.5. Page last updated on 2026-05-05.[View source](https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/animations/overview.md)or[report an issue](https://github.com/flutter/website/issues/new?template=1_page_issue.yml&page-url=https://docs.flutter.dev/ui/animations/overview&page-source=https://github.com/flutter/website/blob/main/sites/docs/src/content/ui/animations/overview.md).
