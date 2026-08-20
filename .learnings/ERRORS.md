# Errors

## [ERR-20260819-001] alembic-multiple-heads-and-existing-schema

**Logged**: 2026-08-19
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
The repository has multiple Alembic heads, and the configured development database already contains tables without a matching migration version.

### Error
`upgrade head` first reported multiple heads. After adding a merge migration, the existing database failed on `table "Files" already exists` while applying `initial_schema`.

### Context
- Operation: verify the new GuangYaPan configuration migration
- Database: configured development SQLite database
- No destructive database operation was performed

### Suggested Fix
Inspect and reconcile the existing database's Alembic version before upgrading; do not stamp or reset it without confirming its schema history.

---

## [ERR-20260819-002] fastapi-route-introspection

**Logged**: 2026-08-19
**Priority**: low
**Status**: resolved
**Area**: backend

### Summary
The direct `app.routes` inspection did not expose included API routes as ordinary `APIRoute` objects.

### Context
The project/FastAPI runtime represents included routers as internal `_IncludedRouter` entries. The GuangYaPan router itself contains all 14 expected routes, so this was a verification-script issue rather than an application failure.

### Resolution
Inspected `app.api.guangyapan.router.routes` directly and verified the configuration and save-url routes.

---
