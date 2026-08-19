import 'dart:async';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:screen_brightness/screen_brightness.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../core/constants.dart';
import '../core/app_logger.dart';
import '../data/api/api_client.dart';
import '../data/api/user_api.dart';
import '../data/models/media.dart';
import '../design_system/app_theme.dart';
import '../providers/settings_provider.dart';

class DouyinSeekBar extends StatefulWidget {
  final double value;
  final double buffered;
  final Duration position;
  final Duration duration;
  final ValueChanged<double> onSeek;
  final ValueChanged<double>? onSeekUpdate;
  final VoidCallback onSeekStart;
  final VoidCallback onSeekEnd;

  const DouyinSeekBar({
    super.key,
    required this.value,
    required this.buffered,
    required this.position,
    required this.duration,
    required this.onSeek,
    this.onSeekUpdate,
    required this.onSeekStart,
    required this.onSeekEnd,
  });

  @override
  State<DouyinSeekBar> createState() => _DouyinSeekBarState();
}

class _DouyinSeekBarState extends State<DouyinSeekBar> {
  bool _isDragging = false;
  double _dragValue = 0.0;
  Offset _lastPosition = Offset.zero;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  void _onLongPressStart(
    LongPressStartDetails details,
    BoxConstraints constraints,
  ) {
    setState(() {
      _isDragging = true;
      _dragValue = widget.value;
      _lastPosition = details.localPosition;
    });
    widget.onSeekStart();
    HapticFeedback.lightImpact();
  }

  void _onLongPressMoveUpdate(
    LongPressMoveUpdateDetails details,
    BoxConstraints constraints,
  ) {
    if (!_isDragging) return;

    final currentPosition = details.localPosition;
    final dx = currentPosition.dx - _lastPosition.dx;
    final offset = dx / constraints.maxWidth;
    final oldValue = _dragValue;
    final newValue = (_dragValue + offset).clamp(0.0, 1.0);

    _lastPosition = currentPosition;

    final oldBlock = (oldValue * 20).floor().clamp(0, 19);
    final newBlock = (newValue * 20).floor().clamp(0, 19);
    if (oldBlock != newBlock) {
      HapticFeedback.selectionClick();
    }

    setState(() {
      _dragValue = newValue;
    });
    widget.onSeekUpdate?.call(newValue);
  }

  void _onLongPressEnd(LongPressEndDetails details) {
    if (_isDragging) {
      widget.onSeek(_dragValue);
      setState(() {
        _isDragging = false;
      });
      widget.onSeekEnd();
      HapticFeedback.lightImpact();
    }
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    final displayValue = _isDragging ? _dragValue : widget.value;

    return LayoutBuilder(
      builder: (context, constraints) {
        return GestureDetector(
          behavior: HitTestBehavior.opaque,
          onLongPressStart: (details) =>
              _onLongPressStart(details, constraints),
          onLongPressMoveUpdate: (details) =>
              _onLongPressMoveUpdate(details, constraints),
          onLongPressEnd: _onLongPressEnd,
          child: Container(
            padding: EdgeInsets.only(top: 6, bottom: 6),
            alignment: Alignment.center,
            child: Stack(
              clipBehavior: Clip.none,
              alignment: Alignment.centerLeft,
              children: [
                AnimatedContainer(
                  duration: const Duration(milliseconds: 100),
                  height: _isDragging ? 9.0 : 5.0,
                  decoration: BoxDecoration(
                    color: cs.onSurface.withValues(alpha: 0.3),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
                AnimatedContainer(
                  duration: const Duration(milliseconds: 100),
                  height: _isDragging ? 9.0 : 5.0,
                  width: constraints.maxWidth * widget.buffered,
                  decoration: BoxDecoration(
                    color: cs.onSurface.withValues(alpha: 0.55),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
                AnimatedContainer(
                  duration: const Duration(milliseconds: 100),
                  height: _isDragging ? 9.0 : 5.0,
                  width: constraints.maxWidth * displayValue,
                  decoration: BoxDecoration(
                    color: cs.primary,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class VideoPlayPage extends ConsumerStatefulWidget {
  final int fileId;
  final int itemId;
  final String title;

  const VideoPlayPage({
    super.key,
    required this.fileId,
    required this.itemId,
    this.title = '',
  });

  @override
  ConsumerState<VideoPlayPage> createState() => _VideoPlayPageState();
}

class _VideoPlayPageState extends ConsumerState<VideoPlayPage>
    with WidgetsBindingObserver {
  late final Player _player;
  late final VideoController _controller;

  bool _isInitialized = false;
  bool _isLoadingUrl = true;
  String? _error;

  String _itemTitle = '';

  Duration _position = Duration.zero;
  Duration _duration = Duration.zero;
  bool _isPlaying = false;
  bool _controlsVisible = true;
  double _volume = 1.0;
  Timer? _controlsTimer;

  double _speed = 1.0;
  double _systemBrightness = 1.0;
  double _showBrightnessValue = 1.0;
  bool _isLandscapeLocked = true;
  double? _showBrightnessIndicator;
  double? _showVolumeIndicator;
  Offset _lastSpeedPosition = Offset.zero;
  double _speedBeforeLongPress = 1.0;
  String? _speedLabelText;
  Timer? _speedLabelTimer;
  bool _speedLabelVisible = false;

  static const List<double> _speeds = [0.5, 1.0, 1.5, 2.0, 3.0];

  bool _isLongPressActive = false;

  BoxFit _fitMode = BoxFit.contain;

  bool _isSeeking = false;
  bool _wasPlayingBeforeSeek = false;
  double _seekSensitivity = 1.0;
  double _verticalDragOffset = 0.0;
  Duration _seekStartPos = Duration.zero;
  Duration _seekPosition = Duration.zero;
  double _totalHorizontalDx = 0.0;
  Duration _lastSeekToPosition = Duration.zero;
  final double _minSensitivity = 0.3;
  final double _maxSensitivity = 3.0;

  UserApi? _userApi;
  Timer? _reportTimer;
  double _watchedThreshold = 0.9;
  bool _reportedAsPlayed = false;
  int _progressFailureCount = 0;

  bool _showRestartButton = false;
  Timer? _restartButtonTimer;

  StreamSubscription<bool>? _playingSubscription;
  StreamSubscription<Duration>? _positionSubscription;
  StreamSubscription<Duration>? _durationSubscription;
  StreamSubscription<double>? _rateSubscription;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _player = Player();
    _controller = VideoController(_player);
    _initPlayer();
    _enterFullscreen();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused) {
      _player.pause();
    }
  }

  Future<void> _enterFullscreen() async {
    await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    await SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);
  }

  Future<void> _exitFullscreen() async {
    await SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    await SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);
  }

  Future<void> _initPlayer() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);

      final results = await Future.wait([
        client.getRedirectUrl(
          '/api/file/data',
          queryParameters: {'file_id': widget.fileId},
        ),
        client.get('/api/media/info', queryParameters: {'id': widget.itemId}),
        ScreenBrightness().current,
      ]);

      final redirectUrl = results[0] as String;
      final infoData = (results[1] as Response).data as Map<String, dynamic>?;
      _systemBrightness = results[2] as double;
      _showBrightnessValue = _systemBrightness;
      Duration resumePosition = Duration.zero;
      if (infoData != null) {
        _itemTitle = (infoData['name'] as String?) ?? '';
        final userdata = infoData['userdata'] as Map<String, dynamic>?;
        if (userdata != null) {
          final ticks = userdata['playback_position_ticks'] as int? ?? 0;
          if (ticks > 0) {
            resumePosition = Duration(microseconds: ticks ~/ 10);
          }
        }
      }

      _playingSubscription = _player.stream.playing.listen((playing) {
        if (mounted && !_isSeeking) {
          setState(() => _isPlaying = playing);
        }
      });

      _positionSubscription = _player.stream.position.listen((position) {
        if (mounted) {
          setState(() => _position = position);
        }
      });

      _durationSubscription = _player.stream.duration.listen((duration) {
        if (mounted) {
          setState(() => _duration = duration);
        }
      });

      _rateSubscription = _player.stream.rate.listen((rate) {
        if (mounted && !_isLongPressActive) {
          setState(() => _speed = rate);
        }
      });

      // 从设置中读取 player 配置
      final hwEnabled = ref.getHardwareAcceleration();
      final cacheMode = ref.getCacheMode();
      final forwardSize = ref.getForwardCacheSize();
      final backwardSize = ref.getBackwardCacheSize();
      final playbackRate = ref.getDefaultPlaybackRate();
      final resumeEnabled = ref.getResumePlayback();

      // 等待播放器初始化完成后再设置自定义属性
      await _player.platform!.waitForPlayerInitialization;

      if (_player.platform is NativePlayer) {
        final np = _player.platform as NativePlayer;
        await np.setProperty('hwdec', hwEnabled ? 'auto' : 'no');
        await np.setProperty('cache', 'yes');
        await np.setProperty(
          'cache-on-disk',
          cacheMode == 'disk' ? 'yes' : 'no',
        );
        await np.setProperty(
          'demuxer-max-bytes',
          (forwardSize * 1024 * 1024).toString(),
        );
        await np.setProperty(
          'demuxer-max-back-bytes',
          (backwardSize * 1024 * 1024).toString(),
        );
        await np.setProperty('network-timeout', '10');
      }

      await _player.open(Media(redirectUrl));

      // 等待 duration 可用（表示媒体已加载完成）
      try {
        if (_player.state.duration <= Duration.zero) {
          await _player.stream.duration
              .firstWhere((d) => d > Duration.zero)
              .timeout(const Duration(seconds: 15));
        }
      } catch (error, stackTrace) {
        AppLogger.warning(
          'duration_unavailable_continue_playback',
          error: error,
          stackTrace: stackTrace,
          category: 'player',
          fields: {'item_id': widget.itemId},
        );
      }

      if (resumeEnabled && resumePosition > Duration.zero) {
        await _player.seek(resumePosition);
        setState(() {
          _showRestartButton = true;
        });
        _restartButtonTimer = Timer(const Duration(seconds: 3), () {
          if (mounted) {
            setState(() {
              _showRestartButton = false;
            });
          }
        });
      }

      if (playbackRate != 1.0) {
        await _player.setRate(playbackRate);
      }

      final muted = prefs.getBool('muted') ?? false;
      if (muted) {
        _player.setVolume(0);
        _volume = 0;
      } else {
        _player.setVolume(100);
        _volume = 1.0;
      }
      _watchedThreshold =
          prefs.getDouble(AppConstants.storageKeyWatchedThreshold) ?? 0.9;

      if (mounted) {
        setState(() {
          _isInitialized = true;
          _isLoadingUrl = false;
        });
        _resetControlsTimer();
        _userApi = UserApi(client);
        _startProgressReporting();
      }
    } catch (error, stackTrace) {
      AppLogger.error(
        'player_initialization_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'player',
        fields: {'item_id': widget.itemId, 'file_id': widget.fileId},
      );
      if (mounted) {
        setState(() {
          _isLoadingUrl = false;
          _error = '视频加载失败，请检查网络连接后重试';
        });
      }
    }
  }

  void _resetControlsTimer() {
    _controlsTimer?.cancel();
    _controlsTimer = Timer(const Duration(seconds: 4), () {
      if (mounted && _isPlaying) {
        setState(() => _controlsVisible = false);
      }
    });
  }

  void _togglePlayPause() {
    if (_isPlaying) {
      _player.pause();
      _reportProgress();
    } else {
      _player.play();
    }
    _resetControlsTimer();
  }

  static const Map<BoxFit, String> _fitModeLabels = {
    BoxFit.contain: '适应',
    BoxFit.cover: '裁剪',
    BoxFit.fill: '拉伸',
  };

  static const Map<BoxFit, IconData> _fitModeIcons = {
    BoxFit.contain: Icons.aspect_ratio,
    BoxFit.cover: Icons.crop,
    BoxFit.fill: Icons.photo_size_select_large,
  };

  void _cycleFitMode() {
    const modes = [BoxFit.contain, BoxFit.cover, BoxFit.fill];
    final idx = modes.indexOf(_fitMode);
    setState(() => _fitMode = modes[(idx + 1) % modes.length]);
  }

  void _startProgressReporting() {
    _reportTimer?.cancel();
    _reportTimer = Timer.periodic(const Duration(seconds: 1), (_) {
      _reportProgress();
    });
  }

  Future<void> _reportProgress() async {
    if (_userApi == null || _duration == Duration.zero) return;
    final ticks = _position.inMicroseconds * 10;
    final progress = _duration.inMilliseconds > 0
        ? _position.inMilliseconds / _duration.inMilliseconds
        : 0.0;
    bool? isPlayed;
    if (!_reportedAsPlayed && progress >= _watchedThreshold) {
      isPlayed = true;
      _reportedAsPlayed = true;
    }
    try {
      await _userApi!.updateUserData(
        UpdateUserDataRequest(
          itemId: widget.itemId,
          playbackPosition: ticks.toDouble(),
          playbackRate: _speed,
          isPlayed: isPlayed,
        ),
      );
      if (_progressFailureCount > 0) {
        AppLogger.info(
          'playback_progress_recovered',
          category: 'player',
          fields: {
            'item_id': widget.itemId,
            'failed_updates': _progressFailureCount,
          },
        );
        _progressFailureCount = 0;
      }
    } catch (error, stackTrace) {
      _progressFailureCount++;
      if (_progressFailureCount == 1 || _progressFailureCount % 10 == 0) {
        AppLogger.warning(
          'playback_progress_update_failed',
          error: error,
          stackTrace: stackTrace,
          category: 'player',
          fields: {
            'item_id': widget.itemId,
            'consecutive_failures': _progressFailureCount,
          },
        );
      }
    }
  }

  void _seekTo(double value) {
    final seekPos = Duration(
      milliseconds: (value * _duration.inMilliseconds).round(),
    );
    _player.seek(seekPos);
    setState(() => _seekPosition = seekPos);
    _resetControlsTimer();
  }

  void _seekUpdate(double value) {
    final seekPos = Duration(
      milliseconds: (value * _duration.inMilliseconds).round(),
    );
    setState(() => _seekPosition = seekPos);
    if ((seekPos - _lastSeekToPosition).abs() >= const Duration(seconds: 1)) {
      _player.seek(seekPos);
      _lastSeekToPosition = seekPos;
    }
  }

  void _setSpeed(double speed) {
    _player.setRate(speed);
    setState(() => _speed = speed);
  }

  void _toggleRotation() {
    if (_isLandscapeLocked) {
      SystemChrome.setPreferredOrientations([
        DeviceOrientation.portraitUp,
        DeviceOrientation.portraitDown,
        DeviceOrientation.landscapeLeft,
        DeviceOrientation.landscapeRight,
      ]);
    } else {
      SystemChrome.setPreferredOrientations([
        DeviceOrientation.landscapeLeft,
        DeviceOrientation.landscapeRight,
      ]);
    }
    setState(() => _isLandscapeLocked = !_isLandscapeLocked);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _controlsTimer?.cancel();
    _speedLabelTimer?.cancel();
    _reportTimer?.cancel();
    _restartButtonTimer?.cancel();

    _playingSubscription?.cancel();
    _positionSubscription?.cancel();
    _durationSubscription?.cancel();
    _rateSubscription?.cancel();

    _player.dispose();
    _exitFullscreen();
    unawaited(_reportProgress());
    super.dispose();
  }

  void _restartFromBeginning() {
    _player.seek(Duration.zero);
    setState(() {
      _showRestartButton = false;
    });
    _restartButtonTimer?.cancel();
  }

  String _formatDuration(Duration d, {Duration? alignTo}) {
    final hours = d.inHours;
    final minutes = d.inMinutes.remainder(60);
    final seconds = d.inSeconds.remainder(60);

    if (alignTo != null) {
      final refHours = alignTo.inHours;
      final refMinutes = alignTo.inMinutes.remainder(60);
      if (refHours > 0) {
        return '${hours.toString().padLeft(2, '0')}:${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
      }
      if (refMinutes > 0 || refHours > 0) {
        return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
      }
      return seconds.toString().padLeft(2, '0');
    }

    if (hours > 0) {
      return '${hours.toString().padLeft(2, '0')}:${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
    }
    if (minutes > 0) {
      return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
    }
    return seconds.toString().padLeft(2, '0');
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return PopScope(
      canPop: true,
      onPopInvokedWithResult: (didPop, result) {
        if (didPop) {
          _exitFullscreen();
        }
      },
      child: Scaffold(
        backgroundColor: cs.surfaceContainerLowest,
        body: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    final cs = Theme.of(context).colorScheme;
    if (_isLoadingUrl) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(color: cs.primary),
            SizedBox(height: 16),
            Text(
              '正在获取视频地址...',
              style: TextStyle(color: cs.onSurfaceVariant, fontSize: 14),
            ),
          ],
        ),
      );
    }

    if (_error != null) {
      return _buildError();
    }

    if (!_isInitialized) {
      return Center(child: CircularProgressIndicator(color: cs.primary));
    }

    return Stack(
      fit: StackFit.expand,
      children: [
        Center(
          child: Video(
            controller: _controller,
            controls: NoVideoControls,
            fill: cs.surface,
            fit: _fitMode,
          ),
        ),

        Positioned.fill(
          child: IgnorePointer(
            child: AnimatedOpacity(
              opacity: _controlsVisible ? 1.0 : 0.0,
              duration: const Duration(milliseconds: 300),
              child: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [
                      cs.surface.withValues(alpha: 0.6),
                      cs.surface.withValues(alpha: 0.0),
                      cs.surface.withValues(alpha: 0.0),
                      cs.surface.withValues(alpha: 0.6),
                    ],
                    stops: const [0.0, 0.12, 0.88, 1.0],
                  ),
                ),
              ),
            ),
          ),
        ),

        Positioned.fill(child: _buildUnifiedGesture()),

        Positioned(
          top: 0,
          left: 0,
          right: 0,
          child: AnimatedOpacity(
            opacity: _controlsVisible ? 1.0 : 0.0,
            duration: const Duration(milliseconds: 200),
            child: IgnorePointer(
              ignoring: !_controlsVisible,
              child: _buildTopBar(),
            ),
          ),
        ),

        Positioned(
          bottom: 0,
          left: 0,
          right: 0,
          child: AnimatedOpacity(
            opacity: _controlsVisible ? 1.0 : 0.0,
            duration: const Duration(milliseconds: 200),
            child: IgnorePointer(
              ignoring: !_controlsVisible,
              child: _buildBottomControls(),
            ),
          ),
        ),

        Positioned(
          top: MediaQuery.of(context).padding.top + 56,
          left: 0,
          right: 0,
          child: IgnorePointer(
            child: AnimatedOpacity(
              opacity: _speedLabelVisible ? 1.0 : 0.0,
              duration: const Duration(milliseconds: 200),
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: context.semantic.playerOverlay,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _speedLabelText ?? '',
                    style: TextStyle(
                      color: context.semantic.playerOverlayText,
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),

        if (_isSeeking)
          Positioned(
            top: MediaQuery.of(context).size.height * 0.4,
            left: 0,
            right: 0,
            child: IgnorePointer(
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: context.semantic.playerOverlay,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(
                    "${_formatDuration(_seekPosition, alignTo: _duration)}/${_formatDuration(_duration)}",
                    style: TextStyle(
                      color: context.semantic.playerOverlayText,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ),

        if (_showRestartButton)
          Positioned(
            right: 16,
            bottom: 56,
            child: AnimatedOpacity(
              opacity: _showRestartButton ? 1.0 : 0.0,
              duration: const Duration(milliseconds: 300),
              child: GestureDetector(
                onTap: _restartFromBeginning,
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: context.semantic.playerOverlay,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.refresh,
                        color: context.semantic.playerOverlayText,
                        size: 18,
                      ),
                      const SizedBox(width: 6),
                      Text(
                        '从头播放',
                        style: TextStyle(
                          color: context.semantic.playerOverlayText,
                          fontSize: 13,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),

        if (_showBrightnessIndicator != null)
          _buildEdgeIndicator(
            icon: _showBrightnessIndicator! <= 0.2
                ? Icons.brightness_2_outlined
                : _showBrightnessIndicator! <= 0.5
                ? Icons.brightness_3_outlined
                : _showBrightnessIndicator! <= 0.8
                ? Icons.brightness_5_outlined
                : Icons.brightness_7_outlined,
            value: _showBrightnessIndicator!,
            alignment: Alignment.centerRight,
          ),

        if (_showVolumeIndicator != null)
          _buildEdgeIndicator(
            icon: _showVolumeIndicator! == 0
                ? Icons.volume_off_outlined
                : _showVolumeIndicator! <= 0.33
                ? Icons.volume_mute_outlined
                : _showVolumeIndicator! <= 0.66
                ? Icons.volume_down_outlined
                : Icons.volume_up_outlined,
            value: _showVolumeIndicator!,
            alignment: Alignment.centerLeft,
          ),

        if (!_isPlaying && _controlsVisible)
          Positioned.fill(
            child: GestureDetector(
              onTap: _togglePlayPause,
              child: Center(
                child: Icon(
                  Icons.play_arrow,
                  color: context.semantic.playerOverlayText,
                  size: 72,
                  shadows: [
                    Shadow(
                      blurRadius: 12,
                      color: context.semantic.playerOverlay,
                    ),
                  ],
                ),
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildError() {
    final cs = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.error_outline, color: cs.error, size: 48),
            SizedBox(height: 16),
            Text('加载失败', style: TextStyle(color: cs.onSurface, fontSize: 16)),
            SizedBox(height: 8),
            Text(
              _error!,
              style: TextStyle(color: cs.onSurfaceVariant, fontSize: 12),
              textAlign: TextAlign.center,
              maxLines: 3,
              overflow: TextOverflow.ellipsis,
            ),
            SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () {
                setState(() {
                  _isLoadingUrl = true;
                  _isInitialized = false;
                  _error = null;
                });
                _initPlayer();
              },
              icon: const Icon(Icons.refresh),
              label: const Text('重试'),
            ),
            SizedBox(height: 12),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('返回', style: TextStyle(color: cs.onSurfaceVariant)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUnifiedGesture() {
    final cs = Theme.of(context).colorScheme;
    return GestureDetector(
      behavior: HitTestBehavior.translucent,
      onTapUp: (_) {
        setState(() {
          _controlsVisible = !_controlsVisible;
        });
        if (_controlsVisible) {
          _resetControlsTimer();
        }
      },
      onDoubleTap: () {
        _togglePlayPause();
      },
      onVerticalDragStart: (details) {
        if (_isLongPressActive) return;
        _controlsTimer?.cancel();
      },
      onVerticalDragUpdate: (details) {
        if (_isLongPressActive) return;

        final half = context.size!.width / 2;
        if (details.localPosition.dx < half) {
          final newBrightness = (_showBrightnessValue - details.delta.dy / 160)
              .clamp(0.0, 1.0);

          setState(() {
            _showBrightnessValue = newBrightness;
            _showBrightnessIndicator = newBrightness;
          });

          final oldBlock =
              ((_showBrightnessValue + details.delta.dy / 160) * 20)
                  .floor()
                  .clamp(0, 19);
          final newBlock = (newBrightness * 20).floor().clamp(0, 19);
          if (oldBlock != newBlock) {
            HapticFeedback.selectionClick();
          }

          ScreenBrightness()
              .setScreenBrightness(newBrightness)
              .catchError((_) {});
        } else {
          final oldVolume = _volume;
          _volume = (oldVolume - details.delta.dy / 160).clamp(0.0, 1.0);
          _player.setVolume(_volume * 100);
          setState(() => _showVolumeIndicator = _volume);

          final oldBlock = (oldVolume * 20).floor().clamp(0, 19);
          final newBlock = (_volume * 20).floor().clamp(0, 19);
          if (oldBlock != newBlock) {
            HapticFeedback.selectionClick();
          }
        }
      },
      onVerticalDragEnd: (_) {
        if (mounted) {
          setState(() {
            _showBrightnessIndicator = null;
            _showVolumeIndicator = null;
          });
        }
        _resetControlsTimer();
      },
      onVerticalDragCancel: () {},
      onLongPressStart: (details) {
        setState(() => _isLongPressActive = true);
        _speedBeforeLongPress = _speed;
        final speed = 3.0;
        _player.setRate(speed);
        _speedLabelTimer?.cancel();
        _speedLabelTimer = Timer(const Duration(milliseconds: 500), () {
          if (mounted) {
            setState(() => _speedLabelVisible = false);
          }
        });
        setState(() {
          _speed = speed;
          _speedLabelText = '${speed.toStringAsFixed(1)}x';
          _speedLabelVisible = true;
          _lastSpeedPosition = details.localPosition;
        });
      },
      onLongPressMoveUpdate: (details) {
        final currentPosition = details.localPosition;
        final dy = currentPosition.dy - _lastSpeedPosition.dy;
        _lastSpeedPosition = currentPosition;

        final oldSpeed = _speed;
        final newSpeed = (_speed - dy / 50).clamp(0.0, 9.0);

        final oldBlock = (oldSpeed * 2).floor().clamp(0, 18);
        final newBlock = (newSpeed * 2).floor().clamp(0, 18);
        if (oldBlock != newBlock) {
          HapticFeedback.selectionClick();
        }

        final rounded = (newSpeed * 100).roundToDouble() / 100;
        _player.setRate(rounded);

        final newText = '${rounded.toStringAsFixed(1)}x';
        if (newText != _speedLabelText) {
          _speedLabelTimer?.cancel();
          _speedLabelTimer = Timer(const Duration(milliseconds: 500), () {
            if (mounted) {
              setState(() {
                _speedLabelVisible = false;
              });
            }
          });
          setState(() {
            _speedLabelText = newText;
            _speedLabelVisible = true;
          });
        }

        setState(() {
          _speed = rounded;
        });
      },
      onLongPressEnd: (_) {
        setState(() => _isLongPressActive = false);
        _speedLabelTimer?.cancel();
        _player.setRate(_speedBeforeLongPress);
        setState(() {
          _speedLabelVisible = false;
          _speed = _speedBeforeLongPress;
          _speedLabelText = null;
        });
      },
      onLongPressCancel: () {
        setState(() => _isLongPressActive = false);
        _speedLabelTimer?.cancel();
        _player.setRate(_speedBeforeLongPress);
        setState(() {
          _speedLabelVisible = false;
          _speed = _speedBeforeLongPress;
          _speedLabelText = null;
        });
      },
      onHorizontalDragStart: (details) {
        if (_duration == Duration.zero) return;
        setState(() {
          _isSeeking = true;
          _wasPlayingBeforeSeek = _isPlaying;
          _seekStartPos = _position;
          _seekPosition = _position;
          _lastSeekToPosition = _position;
          _totalHorizontalDx = 0.0;
          _verticalDragOffset = 0.0;
          _seekSensitivity = 1.0;
        });
        _controlsTimer?.cancel();
        if (_wasPlayingBeforeSeek) {
          HapticFeedback.lightImpact();
        }
      },
      onHorizontalDragUpdate: (details) {
        if (!_isSeeking) return;

        _verticalDragOffset += details.delta.dy;
        setState(() {
          _seekSensitivity = 1.0 - (_verticalDragOffset / 200);
          _seekSensitivity = _seekSensitivity.clamp(
            _minSensitivity,
            _maxSensitivity,
          );
        });

        _totalHorizontalDx += details.delta.dx;
        final seconds = (_totalHorizontalDx / 50) * 10 * _seekSensitivity;
        var newPos = _seekStartPos + Duration(seconds: seconds.round());
        if (newPos < Duration.zero) newPos = Duration.zero;
        if (newPos > _duration) newPos = _duration;
        _seekPosition = newPos;
        if ((newPos - _lastSeekToPosition).abs() >=
            const Duration(seconds: 1)) {
          _player.seek(newPos);
          _lastSeekToPosition = newPos;
        }
      },
      onHorizontalDragEnd: (details) {
        if (!_isSeeking) return;
        _player.seek(_seekPosition);
        if (_wasPlayingBeforeSeek) {
          _player.play();
        }
        setState(() => _isSeeking = false);
        _wasPlayingBeforeSeek = false;
        _resetControlsTimer();
        HapticFeedback.lightImpact();
      },
      onHorizontalDragCancel: () {
        if (!_isSeeking) return;
        if (_wasPlayingBeforeSeek) {
          _player.play();
        }
        setState(() => _isSeeking = false);
        _wasPlayingBeforeSeek = false;
        _resetControlsTimer();
      },
      child: Container(color: cs.surface.withValues(alpha: 0.0)),
    );
  }

  Widget _buildEdgeIndicator({
    required IconData icon,
    required double value,
    required Alignment alignment,
  }) {
    final cs = Theme.of(context).colorScheme;
    return Positioned.fill(
      child: IgnorePointer(
        child: Container(
          alignment: alignment,
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Container(
            width: 40,
            height: 160,
            decoration: BoxDecoration(
              color: cs.surface.withValues(alpha: 0.7),
              borderRadius: BorderRadius.circular(20),
            ),
            padding: const EdgeInsets.symmetric(vertical: 12),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Expanded(
                  child: RotatedBox(
                    quarterTurns: 3,
                    child: LinearProgressIndicator(
                      value: value,
                      backgroundColor: cs.onSurface.withValues(alpha: 0.2),
                      valueColor: AlwaysStoppedAnimation<Color>(cs.primary),
                    ),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '${(value * 100).round()}%',
                  style: TextStyle(color: cs.onSurface, fontSize: 11),
                ),
                const SizedBox(height: 8),
                Icon(icon, color: cs.onSurface, size: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTopBar() {
    final cs = Theme.of(context).colorScheme;
    return SafeArea(
      bottom: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(4, 4, 16, 4),
        child: Row(
          children: [
            IconButton(
              icon: Icon(Icons.arrow_back, color: cs.onSurface, size: 28),
              onPressed: () => Navigator.pop(context),
            ),
            const SizedBox(width: 4),
            Flexible(
              flex: 0,
              child: Text(
                _itemTitle.isNotEmpty ? _itemTitle : widget.title,
                style: TextStyle(color: cs.onSurface, fontSize: 15),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            const Spacer(),
            GestureDetector(
              onTap: _cycleFitMode,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  border: Border.all(color: cs.outline.withValues(alpha: 0.3)),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      _fitModeIcons[_fitMode]!,
                      color: cs.onSurface,
                      size: 12,
                    ),
                    const SizedBox(width: 2),
                    Text(
                      _fitModeLabels[_fitMode]!,
                      style: TextStyle(color: cs.onSurface, fontSize: 11),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBottomControls() {
    final cs = Theme.of(context).colorScheme;
    final positionMs = _position.inMilliseconds.toDouble();
    final durationMs = _duration.inMilliseconds.toDouble();
    final sliderValue = durationMs > 0
        ? (positionMs / durationMs).clamp(0.0, 1.0)
        : 0.0;

    return SafeArea(
      top: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 4),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            DouyinSeekBar(
              value: sliderValue,
              buffered: _duration.inMilliseconds > 0
                  ? (_player.state.buffer.inMilliseconds /
                            _duration.inMilliseconds)
                        .clamp(0.0, 1.0)
                  : 0.0,
              position: _position,
              duration: _duration,
              onSeek: _seekTo,
              onSeekUpdate: _seekUpdate,
              onSeekStart: () {
                setState(() {
                  _isSeeking = true;
                  _wasPlayingBeforeSeek = _isPlaying;
                  _seekPosition = _position;
                  _lastSeekToPosition = _position;
                });
                _controlsTimer?.cancel();
              },
              onSeekEnd: () {
                if (_wasPlayingBeforeSeek) {
                  _player.play();
                }
                setState(() => _isSeeking = false);
                _wasPlayingBeforeSeek = false;
                _resetControlsTimer();
              },
            ),
            Row(
              children: [
                Text(
                  '${_formatDuration(_position, alignTo: _duration)} / ${_formatDuration(_duration)}',
                  style: TextStyle(color: cs.onSurface, fontSize: 12),
                ),
                const Spacer(),
                IconButton(
                  icon: Icon(
                    _volume == 0
                        ? Icons.volume_off_outlined
                        : _volume <= 0.33
                        ? Icons.volume_mute_outlined
                        : _volume <= 0.66
                        ? Icons.volume_down_outlined
                        : Icons.volume_up_outlined,
                    color: cs.onSurface,
                    size: 20,
                  ),
                  onPressed: () async {
                    final prefs = await SharedPreferences.getInstance();
                    if (_volume > 0) {
                      _player.setVolume(0);
                      setState(() => _volume = 0);
                      prefs.setBool('muted', true);
                    } else {
                      _player.setVolume(100);
                      setState(() => _volume = 1.0);
                      prefs.setBool('muted', false);
                    }
                  },
                  constraints: const BoxConstraints(
                    minWidth: 36,
                    minHeight: 36,
                  ),
                  padding: EdgeInsets.zero,
                ),
                const SizedBox(width: 2),
                PopupMenuButton<double>(
                  onSelected: _setSpeed,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  itemBuilder: (context) => _speeds.map((s) {
                    final isSelected = _speed == s;
                    return PopupMenuItem<double>(
                      value: s,
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            '${s}x',
                            style: TextStyle(
                              fontWeight: isSelected
                                  ? FontWeight.bold
                                  : FontWeight.normal,
                              color: isSelected ? cs.primary : cs.onSurface,
                            ),
                          ),
                          if (isSelected) ...[
                            const SizedBox(width: 8),
                            Icon(Icons.check, size: 16, color: cs.primary),
                          ],
                        ],
                      ),
                    );
                  }).toList(),
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: cs.outline.withValues(alpha: 0.3),
                      ),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      '${_speed}x',
                      style: TextStyle(color: cs.onSurface, fontSize: 11),
                    ),
                  ),
                ),
                const SizedBox(width: 2),
                IconButton(
                  icon: Icon(
                    _isPlaying ? Icons.pause : Icons.play_arrow,
                    color: cs.onSurface,
                    size: 24,
                  ),
                  onPressed: _togglePlayPause,
                  constraints: const BoxConstraints(
                    minWidth: 36,
                    minHeight: 36,
                  ),
                  padding: EdgeInsets.zero,
                ),
                IconButton(
                  icon: Icon(
                    Icons.screen_rotation,
                    color: cs.onSurface,
                    size: 20,
                  ),
                  onPressed: _toggleRotation,
                  padding: EdgeInsets.zero,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
