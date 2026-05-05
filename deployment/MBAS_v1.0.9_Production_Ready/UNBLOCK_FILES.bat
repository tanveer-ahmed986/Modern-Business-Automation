@echo off
title MBAS - Unblock Files (Fix Smart App Control)
color 0C

echo.
echo ========================================================================
echo    MBAS - Unblock Files Tool
echo    Fixes "Smart App Control blocked this file" error
echo ========================================================================
echo.
echo This script will:
echo   1. Unblock all MBAS files downloaded from the internet
echo   2. Add Windows Defender exclusion for MBAS folder
echo   3. Disable Smart App Control warnings for MBAS
echo.
echo IMPORTANT: This requires Administrator privileges!
echo.
pause

cd /d "%~dp0"

echo.
echo [Step 1/3] Unblocking all files in MBAS folder...
echo.

REM Unblock all files recursively using PowerShell
powershell -Command "Get-ChildItem -Path '%~dp0' -Recurse | Unblock-File"

if errorlevel 1 (
    echo [WARN] Some files may not have been unblocked.
    echo This is normal if running without Administrator privileges.
) else (
    echo [OK] All files unblocked successfully!
)

echo.
echo [Step 2/3] Adding Windows Defender exclusion...
echo.

REM Add folder to Windows Defender exclusions
powershell -Command "Add-MpPreference -ExclusionPath '%~dp0'" 2>nul

if errorlevel 1 (
    echo [WARN] Could not add Windows Defender exclusion.
    echo Please run this script as Administrator.
    echo.
    echo Manual steps:
    echo   1. Open Windows Security
    echo   2. Go to Virus and threat protection ^> Manage settings
    echo   3. Scroll to Exclusions ^> Add or remove exclusions
    echo   4. Click Add an exclusion ^> Folder
    echo   5. Select this folder: %~dp0
) else (
    echo [OK] Windows Defender exclusion added!
)

echo.
echo [Step 3/3] Verifying file status...
echo.

REM Check if files are still blocked
powershell -Command "$blockedCount = (Get-ChildItem -Path '%~dp0' -Recurse -File | Get-Item -Stream * | Where-Object {$_.Stream -eq 'Zone.Identifier'}).Count; if ($blockedCount -eq 0) {Write-Host '[OK] No blocked files found!'} else {Write-Host '[WARN] ' $blockedCount 'files are still blocked'}"

echo.
echo ========================================================================
echo    File Unblocking Complete!
echo ========================================================================
echo.
echo Next steps:
echo   1. Close this window
echo   2. Run INSTALL.bat (if not already installed)
echo   3. Run START_MBAS_TRAY.bat to start MBAS
echo.
echo If you still see Smart App Control warnings:
echo   1. Go to Windows Security ^> App and browser control
echo   2. Click "Smart App Control settings"
echo   3. Turn it Off (or set to Evaluation mode)
echo.

pause
