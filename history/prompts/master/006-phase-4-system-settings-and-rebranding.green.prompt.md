# PHR: Phase 4 - System Settings & Rebranding

**ID**: 006  
**TITLE**: Phase 4 - System Settings & Rebranding  
**STAGE**: green  
**DATE_ISO**: 2026-03-05  
**SURFACE**: agent  
**MODEL**: gemini-2.0-flash-exp  
**FEATURE**: master  
**BRANCH**: master  
**USER**: user  
**COMMAND**: proceed with Phase 4  
**LABELS**: ["settings", "branding", "backend", "frontend"]  
**LINKS**: ["specs/master/tasks.md", "specs/master/plan.md"]  

## Summary
Started Phase 4 of the MBAS project, focusing on System Settings and Rebranding. This includes backend API endpoints for settings management and frontend components for branding.

## Acceptance Criteria
- [ ] GET /settings returns current system settings.
- [ ] PUT /settings updates system settings (Admin only).
- [ ] Frontend Settings service implemented.
- [ ] Settings UI allows editing business name, tax rate, and currency.
- [ ] Branding hook provides reactive data to components.
- [ ] Sidebar/Layout reflect branding changes.

## Proposed Changes
- Create `backend/src/api/settings.py`.
- Register settings router in `backend/src/main.py`.
- Create `frontend/src/services/settings.service.ts`.
- Create `frontend/src/hooks/useBranding.ts`.
- Create `frontend/src/features/settings/SettingsPage.tsx`.
- Update `frontend/src/App.tsx` with settings route.
- Update `frontend/src/components/layout/Sidebar.tsx` for branding.

## Files Modified
- `backend/src/api/settings.py` (Created)
- `backend/src/main.py` (Modified)
- `frontend/src/services/settings.service.ts` (Created)
- `frontend/src/hooks/useBranding.ts` (Created)
- `frontend/src/features/settings/SettingsPage.tsx` (Created)
- `frontend/src/App.tsx` (Modified)
- `frontend/src/components/layout/Sidebar.tsx` (Modified)

## Tests Run/Added
- Frontend build verified: `npm run build` (Successful)

## Outcome
Phase 4 successfully implemented. The system now supports dynamic branding and system settings management with Admin-only access controls for updates.
