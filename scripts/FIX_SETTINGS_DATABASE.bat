@echo off
title MBAS - Fix Settings Database Schema
color 0E

echo.
echo ================================================================
echo    MBAS - Settings Database Schema Migration
echo ================================================================
echo.
echo This script will update your Settings table to fix the
echo "Failed to update settings" error.
echo.
echo Changes:
echo   - Rename currency_symbol to currency
echo   - Add created_at and updated_at timestamps
echo.
echo IMPORTANT: Your data will be preserved!
echo.
pause

echo.
echo [*] Starting migration...
echo.

REM Navigate to backend directory
cd /d "%~dp0..\backend"

REM Run migration script
python src\scripts\migrate_settings_schema.py

if errorlevel 1 (
    echo.
    echo [ERROR] Migration failed!
    echo.
    echo Please contact support with the error message above.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo    [SUCCESS] Migration Complete!
echo ================================================================
echo.
echo Your Settings table has been updated.
echo You can now save settings without errors.
echo.
echo Next steps:
echo   1. Start MBAS (run START_MBAS.bat)
echo   2. Go to Settings page
echo   3. Make changes and click "Save Settings"
echo   4. Should work perfectly now!
echo.
pause
