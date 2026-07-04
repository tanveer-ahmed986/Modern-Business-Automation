@echo off
REM ============================================================================
REM  MBAS Documentation Cleanup Script
REM  Archives old documentation and organizes current files
REM  Run this AFTER CLEANUP_PROJECT.bat
REM ============================================================================

title MBAS Documentation Cleanup
color 0E

echo.
echo ================================================================================
echo   MBAS Documentation Cleanup
echo   Archives old documentation files
echo ================================================================================
echo.
echo This will:
echo   - Create docs\archive\ directory
echo   - Move old v1.0.x documentation to archive
echo   - Move old fix guides to archive
echo   - Keep only current documentation at root level
echo.
pause

echo.
echo Creating archive directory...
if not exist "docs\archive" mkdir "docs\archive"
if not exist "docs\archive\v1.0.x" mkdir "docs\archive\v1.0.x"
if not exist "docs\archive\fixes" mkdir "docs\archive\fixes"

echo.
echo [PHASE 1] Archiving old version documentation...

REM Archive v1.0.x documentation
if exist "CHANGELOG_v1.0.8.md" move /Y "CHANGELOG_v1.0.8.md" "docs\archive\v1.0.x\" && echo   Archived: CHANGELOG_v1.0.8.md
if exist "DEPLOYMENT_READY_v1.0.9.txt" move /Y "DEPLOYMENT_READY_v1.0.9.txt" "docs\archive\v1.0.x\" && echo   Archived: DEPLOYMENT_READY_v1.0.9.txt
if exist "DEPLOYMENT_SUMMARY_v1.0.8.md" move /Y "DEPLOYMENT_SUMMARY_v1.0.8.md" "docs\archive\v1.0.x\" && echo   Archived: DEPLOYMENT_SUMMARY_v1.0.8.md
if exist "FIRST_CLICK_FIX_v1.0.7.md" move /Y "FIRST_CLICK_FIX_v1.0.7.md" "docs\archive\v1.0.x\" && echo   Archived: FIRST_CLICK_FIX_v1.0.7.md
if exist "INSTALL_NEW_VERSION_v2.0.1.txt" move /Y "INSTALL_NEW_VERSION_v2.0.1.txt" "docs\archive\v1.0.x\" && echo   Archived: INSTALL_NEW_VERSION_v2.0.1.txt
if exist "MBAS_v1.0.9_INTEGRATION_COMPLETE.md" move /Y "MBAS_v1.0.9_INTEGRATION_COMPLETE.md" "docs\archive\v1.0.x\" && echo   Archived: MBAS_v1.0.9_INTEGRATION_COMPLETE.md
if exist "PATH_FIX_v1.0.7_FINAL.md" move /Y "PATH_FIX_v1.0.7_FINAL.md" "docs\archive\v1.0.x\" && echo   Archived: PATH_FIX_v1.0.7_FINAL.md
if exist "PROFESSIONAL_PACKAGE_v1.0.7_FINAL.md" move /Y "PROFESSIONAL_PACKAGE_v1.0.7_FINAL.md" "docs\archive\v1.0.x\" && echo   Archived: PROFESSIONAL_PACKAGE_v1.0.7_FINAL.md
if exist "READ_THIS_FIRST_v2.0.1.txt" move /Y "READ_THIS_FIRST_v2.0.1.txt" "docs\archive\v1.0.x\" && echo   Archived: READ_THIS_FIRST_v2.0.1.txt
if exist "RELEASE_NOTES_v1.0.8.txt" move /Y "RELEASE_NOTES_v1.0.8.txt" "docs\archive\v1.0.x\" && echo   Archived: RELEASE_NOTES_v1.0.8.txt
if exist "TIMEOUT_FIX_v2.0.1.md" move /Y "TIMEOUT_FIX_v2.0.1.md" "docs\archive\v1.0.x\" && echo   Archived: TIMEOUT_FIX_v2.0.1.md
if exist "CRITICAL_FIXES_APPLIED_v2.0.1.md" move /Y "CRITICAL_FIXES_APPLIED_v2.0.1.md" "docs\archive\v1.0.x\" && echo   Archived: CRITICAL_FIXES_APPLIED_v2.0.1.md

echo.
echo [PHASE 2] Archiving old fix documentation...

REM Archive old fix guides
if exist "ALL_CURRENCY_FIXES_COMPLETE.txt" move /Y "ALL_CURRENCY_FIXES_COMPLETE.txt" "docs\archive\fixes\" && echo   Archived: ALL_CURRENCY_FIXES_COMPLETE.txt
if exist "BACKEND_FIX_GUIDE.txt" move /Y "BACKEND_FIX_GUIDE.txt" "docs\archive\fixes\" && echo   Archived: BACKEND_FIX_GUIDE.txt
if exist "BILLING_SETTINGS_FIX.md" move /Y "BILLING_SETTINGS_FIX.md" "docs\archive\fixes\" && echo   Archived: BILLING_SETTINGS_FIX.md
if exist "BILLING_SETTINGS_FIXED.txt" move /Y "BILLING_SETTINGS_FIXED.txt" "docs\archive\fixes\" && echo   Archived: BILLING_SETTINGS_FIXED.txt
if exist "COMPLETE_SOLUTION_BOTH_ISSUES.md" move /Y "COMPLETE_SOLUTION_BOTH_ISSUES.md" "docs\archive\fixes\" && echo   Archived: COMPLETE_SOLUTION_BOTH_ISSUES.md
if exist "CURRENCY_FIX_SUPPLIERS_PURCHASES.md" move /Y "CURRENCY_FIX_SUPPLIERS_PURCHASES.md" "docs\archive\fixes\" && echo   Archived: CURRENCY_FIX_SUPPLIERS_PURCHASES.md
if exist "CURRENCY_SYNC_FIXED.md" move /Y "CURRENCY_SYNC_FIXED.md" "docs\archive\fixes\" && echo   Archived: CURRENCY_SYNC_FIXED.md
if exist "CURRENCY_SYNC_QUICK_FIX.txt" move /Y "CURRENCY_SYNC_QUICK_FIX.txt" "docs\archive\fixes\" && echo   Archived: CURRENCY_SYNC_QUICK_FIX.txt
if exist "DASHBOARD_CURRENCY_FIX.txt" move /Y "DASHBOARD_CURRENCY_FIX.txt" "docs\archive\fixes\" && echo   Archived: DASHBOARD_CURRENCY_FIX.txt
if exist "DEPLOYMENT_FIX_SUMMARY.md" move /Y "DEPLOYMENT_FIX_SUMMARY.md" "docs\archive\fixes\" && echo   Archived: DEPLOYMENT_FIX_SUMMARY.md
if exist "FEATURES_FIXED.md" move /Y "FEATURES_FIXED.md" "docs\archive\fixes\" && echo   Archived: FEATURES_FIXED.md
if exist "NPM_ERROR_FIX_GUIDE.md" move /Y "NPM_ERROR_FIX_GUIDE.md" "docs\archive\fixes\" && echo   Archived: NPM_ERROR_FIX_GUIDE.md
if exist "PYDANTIC_VERSION_CONFLICT_FIXED.md" move /Y "PYDANTIC_VERSION_CONFLICT_FIXED.md" "docs\archive\fixes\" && echo   Archived: PYDANTIC_VERSION_CONFLICT_FIXED.md
if exist "QUICK_FIX_SUMMARY.md" move /Y "QUICK_FIX_SUMMARY.md" "docs\archive\fixes\" && echo   Archived: QUICK_FIX_SUMMARY.md
if exist "QUICK_DEPLOYMENT_FIX.txt" move /Y "QUICK_DEPLOYMENT_FIX.txt" "docs\archive\fixes\" && echo   Archived: QUICK_DEPLOYMENT_FIX.txt
if exist "QUICK_FIX_SETTINGS.txt" move /Y "QUICK_FIX_SETTINGS.txt" "docs\archive\fixes\" && echo   Archived: QUICK_FIX_SETTINGS.txt
if exist "SETTINGS_FIX_COMPLETE.md" move /Y "SETTINGS_FIX_COMPLETE.md" "docs\archive\fixes\" && echo   Archived: SETTINGS_FIX_COMPLETE.md
if exist "WATCHDOG_SYSTEM_FIXED.md" move /Y "WATCHDOG_SYSTEM_FIXED.md" "docs\archive\fixes\" && echo   Archived: WATCHDOG_SYSTEM_FIXED.md

echo.
echo [PHASE 3] Removing old batch/fix scripts...

REM Delete old fix batch scripts
if exist "ALTERNATIVE_INSTALL.bat" del /F /Q "ALTERNATIVE_INSTALL.bat" && echo   Deleted: ALTERNATIVE_INSTALL.bat
if exist "AUTO_START_MBAS.bat" del /F /Q "AUTO_START_MBAS.bat" && echo   Deleted: AUTO_START_MBAS.bat
if exist "AUTO_START_WITH_RECOVERY.bat" del /F /Q "AUTO_START_WITH_RECOVERY.bat" && echo   Deleted: AUTO_START_WITH_RECOVERY.bat
if exist "CHECK_SYSTEM.bat" del /F /Q "CHECK_SYSTEM.bat" && echo   Deleted: CHECK_SYSTEM.bat
if exist "COMPLETE_UNINSTALL.bat" del /F /Q "COMPLETE_UNINSTALL.bat" && echo   Deleted: COMPLETE_UNINSTALL.bat
if exist "DIAGNOSE.bat" del /F /Q "DIAGNOSE.bat" && echo   Deleted: DIAGNOSE.bat
if exist "DIAGNOSE_AND_FIX.bat" del /F /Q "DIAGNOSE_AND_FIX.bat" && echo   Deleted: DIAGNOSE_AND_FIX.bat
if exist "EMERGENCY_DIAGNOSTIC.bat" del /F /Q "EMERGENCY_DIAGNOSTIC.bat" && echo   Deleted: EMERGENCY_DIAGNOSTIC.bat
if exist "FIX_BACKEND.bat" del /F /Q "FIX_BACKEND.bat" && echo   Deleted: FIX_BACKEND.bat
if exist "FIX_BILLING_SETTINGS.bat" del /F /Q "FIX_BILLING_SETTINGS.bat" && echo   Deleted: FIX_BILLING_SETTINGS.bat
if exist "FIX_CURRENCY_SYNC.bat" del /F /Q "FIX_CURRENCY_SYNC.bat" && echo   Deleted: FIX_CURRENCY_SYNC.bat
if exist "FIX_DASHBOARD.bat" del /F /Q "FIX_DASHBOARD.bat" && echo   Deleted: FIX_DASHBOARD.bat
if exist "FIX_FRONTEND.bat" del /F /Q "FIX_FRONTEND.bat" && echo   Deleted: FIX_FRONTEND.bat
if exist "FIX_IMPORTS.bat" del /F /Q "FIX_IMPORTS.bat" && echo   Deleted: FIX_IMPORTS.bat
if exist "INIT_DATABASE.bat" del /F /Q "INIT_DATABASE.bat" && echo   Deleted: INIT_DATABASE.bat
if exist "START_WITH_WATCHDOG.bat" del /F /Q "START_WITH_WATCHDOG.bat" && echo   Deleted: START_WITH_WATCHDOG.bat
if exist "TEST_BACKEND.bat" del /F /Q "TEST_BACKEND.bat" && echo   Deleted: TEST_BACKEND.bat
if exist "TEST_FRONTEND.bat" del /F /Q "TEST_FRONTEND.bat" && echo   Deleted: TEST_FRONTEND.bat
if exist "UNINSTALL_MBAS_FOR_TESTING.bat" del /F /Q "UNINSTALL_MBAS_FOR_TESTING.bat" && echo   Deleted: UNINSTALL_MBAS_FOR_TESTING.bat
if exist "BUILD_INSTALLER_SIMPLE.bat" del /F /Q "BUILD_INSTALLER_SIMPLE.bat" && echo   Deleted: BUILD_INSTALLER_SIMPLE.bat
if exist "BUILD_PROFESSIONAL_INSTALLER.bat" del /F /Q "BUILD_PROFESSIONAL_INSTALLER.bat" && echo   Deleted: BUILD_PROFESSIONAL_INSTALLER.bat
if exist "CREATE_PACKAGE_v1.0.8.bat" del /F /Q "CREATE_PACKAGE_v1.0.8.bat" && echo   Deleted: CREATE_PACKAGE_v1.0.8.bat
if exist "CREATE_PACKAGE_v1.0.9.bat" del /F /Q "CREATE_PACKAGE_v1.0.9.bat" && echo   Deleted: CREATE_PACKAGE_v1.0.9.bat

echo.
echo ================================================================================
echo   Documentation Cleanup Complete!
echo ================================================================================
echo.
echo Archived:
echo   - Old version documentation (v1.0.x) → docs\archive\v1.0.x\
echo   - Old fix guides → docs\archive\fixes\
echo.
echo Deleted:
echo   - Old batch/fix scripts (20+ files)
echo.
echo Remaining at root level:
echo   - Current version documentation
echo   - Active batch scripts (START_MBAS.bat, STOP_MBAS.bat, etc.)
echo   - README.md, CLAUDE.md
echo.
pause
