# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 语言规则

- **思考过程和结论需要输出中文** — 所有分析、推理、结论均使用中文输出

## Commands

### Backend (FastAPI)
```bash
# Run backend with hot reload
cd backend
python run.py

# Or directly
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend (Vue 3 + Vite)
```bash
cd frontend
npm install
npm run dev       # dev server on :5173, proxies /api -> :8000
npm run lint      # ESLint
npm run test      # Vitest
npm run build     # production build
```

### Mobile (Flutter)
```bash
cd mobile
flutter pub get
flutter run
flutter analyze
flutter test
flutter build apk  # Android release build
```

### Database
```bash
# Alembic migrations (configured in backend/database/alembic/)
cd backend/database
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Architecture

### Stack
- **Backend**: Python FastAPI, SQLAlchemy 2.0 async, JWT auth (python-jose), Pydantic v2
- **Frontend**: Vue 3 (Composition API), Vite, Pinia, Element Plus, Axios
- **Mobile**: Flutter 3.x, Riverpod, Dio, media_kit
- **Database**: SQLite via aiosqlite (dev), PostgreSQL via asyncpg (target)
- **File Storage**: 123 Cloud WebDAV (files served via redirect)

### Backend Structure (`backend/app/`)
- `app/main.py` — FastAPI app, CORS, lifespan (auto-creates admin user), exception handler
- `app/api/` — Routers: `user.py` (auth, userdata, settings), `media.py` (list/info/stats/batch), `file.py` (file proxy via WebDAV), `system.py` (system info)
- `app/services/` — Business logic: `auth_service.py`, `media_service.py`, `user_service.py`
- `app/schemas/` — Pydantic models and serializers: `auth.py`, `media.py`, `user.py`, `create.py`, `setting.py`
- `app/api/deps.py` — FastAPI dependencies: bearer token auth, optional auth, admin check

**Key pattern**: API routes are thin; most logic is in service functions. Dependencies use `get_db_session` (context manager yielding `AsyncSession`).

### Database Design (`backend/database/`)
- **Single-table design**: All media entities in `MediaItems` table, differentiated by `Type` enum
- **Relationships** via `ItemLinks` table (many-to-many, includes Person/Genre/Studio associations)
- **Files** in `Files` table, linked to MediaItems via `FileLinks`
- **User data** in `UserData` table (composite PK: UserId + ItemId)
- **Soft delete**: `MediaItem.IsDeleted` flag, filtered in all queries
- **Session management**: `SessionManager` context manager + `get_db_session` generator for FastAPI DI

### Frontend Structure (`frontend/src/`)
- `views/` — Page components: Login, Home, Library, Favorites, History, Media (detail), VideoPlayer, Settings, System
- `api/` — Axios-based API modules: `auth.js`, `media.js`, `file.js`, `user.js`, `system.js`
- `store/` — Pinia stores: `auth.js` (token, user info), `theme.js` (theme + user settings), `layout.js` (sidebar)
- `components/` — Reusable: `MediaCard.vue`, `FileRow.vue`, `MediaGrid.vue`, `MediaDetailDrawer.vue`, etc.
- `router/` — Vue Router with auth guard and admin check
- `composables/` — `usePlayerState.js` (player state & userdata sync)
- `utils/` — `format.js`, `url.js`
- `tests/` — Vitest unit tests

### Mobile Structure (`mobile/lib/`)
- `phone/` — Phone UI: `home/` (home/media/my tabs), `login/`, `detail.dart`, `grid_view.dart`, `video_play.dart`, `media_play_settings.dart`
- `windows/` — Windows (desktop) UI: `home.dart`, `detail.dart`（开发中）
- `component/` — Reusable widgets: `media_card.dart`, `media_tag.dart`, `horizontal_media_section.dart`
- `core/` — `constants.dart`, `config.dart`, `system_config.dart`, `auth_service.dart`, `token_manager.dart`
- `data/` — API client (`api/api_client.dart` with JWT refresh interceptor), `api/*`, `models/*`
- `providers/` — Riverpod: `settings_provider.dart`
- `services/` — `sync_service.dart` (periodic cloud settings sync)

### Config
- `backend/config/default.yaml` — production defaults
- `backend/config/setting.yaml` — UI card display config
- `backend/config/local.yaml` — local overrides (gitignored, see `local.example.yaml`)
- `backend/secrets/config.yaml` — sensitive credentials (gitignored, see `config.example.yaml`)
- `backend/config.py` — dataclass-based config loader with YAML parsing

### Key Flows

**File Streaming**: `GET /api/file/data?file_id=X` → checks diskcache → queries DB for path → requests WebDAV redirect URL → caches URL → returns 302 redirect. Falls back to random image URLs on failure.

**Media Listing**: `GET /api/media/list` → batch queries in `get_media_list()`: fetches items with filters/sort/pagination, then parallel batch queries for links, files, userdata, aliases. Serialized via `app/schemas/media.py`.

**Auth**: JWT access + refresh tokens. Mobile auto-refreshes via Dio interceptor; frontend via Axios interceptor + subscriber queue.
