/**
 * 图标注册表（动态图标的唯一白名单）
 *
 * 静态图标请直接使用 <i-lucide-xxx />（unplugin-icons 构建时按需打包）；
 * 仅 JS 数据驱动的图标（如 Home.vue 统计卡）通过 AppIcon + 本注册表引用。
 * 新增图标 = 在此登记一行 + 确保 @iconify-json/lucide 含该图标。
 */
import Home from '~icons/lucide/home'
import Clapperboard from '~icons/lucide/clapperboard'
import Star from '~icons/lucide/star'
import History from '~icons/lucide/history'
import Settings from '~icons/lucide/settings'
import Activity from '~icons/lucide/activity'
import Sun from '~icons/lucide/sun'
import Moon from '~icons/lucide/moon'
import PanelLeftClose from '~icons/lucide/panel-left-close'
import PanelLeftOpen from '~icons/lucide/panel-left-open'
import ChevronDown from '~icons/lucide/chevron-down'
import LogOut from '~icons/lucide/log-out'
import Headphones from '~icons/lucide/headphones'
import Image from '~icons/lucide/image'
import BookOpen from '~icons/lucide/book-open'
import Palette from '~icons/lucide/palette'
import Monitor from '~icons/lucide/monitor'
import Check from '~icons/lucide/check'
import Video from '~icons/lucide/video'
import Music from '~icons/lucide/music'
import Tv from '~icons/lucide/tv'
import Film from '~icons/lucide/film'
import Clock from '~icons/lucide/clock'
import ClockPlus from '~icons/lucide/clock-plus'
import ArrowRight from '~icons/lucide/arrow-right'
import ArrowLeft from '~icons/lucide/arrow-left'
import User from '~icons/lucide/user'
import Lock from '~icons/lucide/lock'
import Folder from '~icons/lucide/folder'
import FolderOpen from '~icons/lucide/folder-open'
import Library from '~icons/lucide/library'
import Search from '~icons/lucide/search'
import LayoutGrid from '~icons/lucide/layout-grid'
import List from '~icons/lucide/list'
import X from '~icons/lucide/x'
import LoaderCircle from '~icons/lucide/loader-circle'
import Play from '~icons/lucide/play'
import Pause from '~icons/lucide/pause'
import Maximize from '~icons/lucide/maximize'
import Bell from '~icons/lucide/bell'
import XCircle from '~icons/lucide/circle-x'
import Info from '~icons/lucide/info'
import FileText from '~icons/lucide/file-text'
import MessageSquare from '~icons/lucide/message-square'
import Notebook from '~icons/lucide/notebook'
import ChartLine from '~icons/lucide/chart-line'
import Cpu from '~icons/lucide/cpu'
import Coins from '~icons/lucide/coins'
import Menu from '~icons/lucide/menu'
import Layers from '~icons/lucide/layers'
import CirclePlay from '~icons/lucide/circle-play'
import Tag from '~icons/lucide/tag'
import Bookmark from '~icons/lucide/bookmark'
import Package from '~icons/lucide/package'

export const iconRegistry = {
  home: Home,
  clapperboard: Clapperboard,
  star: Star,
  history: History,
  settings: Settings,
  activity: Activity,
  sun: Sun,
  moon: Moon,
  'panel-left-close': PanelLeftClose,
  'panel-left-open': PanelLeftOpen,
  'chevron-down': ChevronDown,
  'log-out': LogOut,
  headphones: Headphones,
  image: Image,
  'book-open': BookOpen,
  palette: Palette,
  monitor: Monitor,
  check: Check,
  video: Video,
  music: Music,
  tv: Tv,
  film: Film,
  clock: Clock,
  'clock-plus': ClockPlus,
  'arrow-right': ArrowRight,
  'arrow-left': ArrowLeft,
  user: User,
  lock: Lock,
  folder: Folder,
  'folder-open': FolderOpen,
  library: Library,
  search: Search,
  'layout-grid': LayoutGrid,
  list: List,
  x: X,
  'loader-circle': LoaderCircle,
  play: Play,
  pause: Pause,
  maximize: Maximize,
  bell: Bell,
  'circle-x': XCircle,
  info: Info,
  'file-text': FileText,
  'message-square': MessageSquare,
  notebook: Notebook,
  'chart-line': ChartLine,
  cpu: Cpu,
  coins: Coins,
  menu: Menu,
  layers: Layers,
  'play-circle': CirclePlay,
  tag: Tag,
  bookmark: Bookmark,
  package: Package,
}
