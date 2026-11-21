# PHR 0003 — Phase 3: Security & licensing hardening

- **ID:** 0003
- **Stage:** green
- **Feature:** system-overhaul
- **Date:** 2026-11-13
- **Author:** tanveer030402@gmail.com (via Claude Code)

## Prompt

> start phase 3

## Context

Phase 1 (stability) and Phase 2 (data correctness) complete and validated.
Phase 3 per `specs/system-overhaul/plan.md`: security & licensing hardening.

## Scope executed

1. `/auth/login` no longer returns the raw `User` row (was leaking
   `hashed_password`) — wrapped in a `LoginResponse` schema around
   `UserRead`. Added manual in-memory login rate limiting (5 failed
   attempts / 15 min lockout per username, `429`), no new dependency.
2. `get_current_user` rejects deactivated users on both the cache-hit and
   DB-fetch paths; removed the token-from-query-param fallback (header-only
   now); shortened the user cache TTL 60s→30s and added an explicit
   `invalidate_user_cache()` hook wired into admin user edits/deletes.
3. Forced password change: new `User.must_change_password` column
   (additive migration in `init_db()`), set on the bootstrap `admin123`
   account (with a loud startup warning replacing the silent default) and
   on any admin-driven password reset. New `POST /users/me/change-password`
   self-service endpoint clears it. Frontend `/change-password` page +
   `ProtectedRoute` force-redirect until cleared.
4. Feature flags are now derived from the signed license at runtime
   (`get_effective_feature_flags()`), falling back to the Basic tier with
   no license loaded. `settings.feature_flags` is a display-only mirror;
   `PUT /settings/` excludes it from the mutable field set, closing the
   admin self-upgrade bypass.
5. `/system/restore` whitelists `backup_filename` against
   `BackupUtility.list_backups()` (closes a path-traversal hole) and reads
   from the real ProgramData backups directory instead of a CWD-relative
   one that never matched production. `restore_backup()` deletes the live
   DB's `-wal`/`-shm` sidecars before copying in the backup.
6. Explicit LAN opt-in via `MBAS_HOST` env var (default `127.0.0.1`) on the
   dev entrypoint; installer `.bat` launchers and `watchdog.py` already
   hardcoded localhost.
7. Audited every endpoint for raw-model response leaks (the "response_model
   everywhere" item) — `/auth/login` was the only real leak; left
   non-sensitive table/paginated/CSV responses as-is rather than adding
   response_model as a blanket typing exercise.

## Response summary

Implementation + validation recorded in `specs/system-overhaul/plan.md`
(Phase 3 section, now marked COMPLETE).

Final results:
- Backend: 104/104 pytest passing (0 failures), up from 92 at the end of
  Phase 2. 12 new tests in `tests/integration/test_phase3_security.py`.
  Added test-isolation resets for two new module-level globals (login
  rate-limit counters, license validator singleton) in `conftest.py`,
  following the Phase 2 dashboard-cache precedent. Added a `premium_license`
  fixture (duck-typed fake validator) so license-gated features can be
  tested without a real RSA-signed license file.
- Frontend: `npm run build` passes; `npx vitest run` 10/10 (unchanged from
  Phase 2 — the Playwright e2e spec picked up by vitest's glob is a
  pre-existing, unrelated quirk, not a regression).
- Alembic migrations remain deferred to Phase 5 per the Phase 2 rationale;
  this phase's one schema change (`users.must_change_password`) used the
  same additive `_ensure_column()` helper pattern instead.
