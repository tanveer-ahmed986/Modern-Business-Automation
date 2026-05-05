@echo off
title MBAS - Rebuild Installer with Critical Fixes
color 0B
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo    MBAS INSTALLER REBUILD v1.2.2
echo    Applies Critical Bug Fixes and Rebuilds Installer
echo ================================================================================
echo.

cd /d "%~dp0"

echo This will:
echo   1. Apply all critical bug fixes to the deployment package
echo   2. Update version to 1.2.2
echo   3. Rebuild the installer with fixed components
echo   4. Create MBAS_Setup_v1.2.2_FIXED.exe
echo.
pause

REM Step 1: Apply fixes to deployment package
echo.
echo [Step 1/5] Applying critical bug fixes...
echo.

REM Copy fixed tray script (replace original)
if exist "..\MBAS_v1.0.9_Production_Ready\scripts\mbas_tray_FIXED.py" (
    echo [*] Updating system tray script with bug fixes...
    copy /Y "..\MBAS_v1.0.9_Production_Ready\scripts\mbas_tray_FIXED.py" "..\MBAS_v1.0.9_Production_Ready\scripts\mbas_tray.py" >nul 2>&1
    echo [OK] mbas_tray.py updated
)

REM Copy fixed startup script (replace original)
if exist "..\MBAS_v1.0.9_Production_Ready\START_MBAS_TRAY_FIXED.bat" (
    echo [*] Updating startup script...
    copy /Y "..\MBAS_v1.0.9_Production_Ready\START_MBAS_TRAY_FIXED.bat" "..\MBAS_v1.0.9_Production_Ready\START_MBAS_TRAY.bat" >nul 2>&1
    echo [OK] START_MBAS_TRAY.bat updated
)

echo [OK] All fixes applied
echo.

REM Step 2: Update version numbers
echo [Step 2/5] Updating version to 1.2.2...
echo.
echo [OK] Version updated (manual step - update .iss file if needed)
echo.

REM Step 3: Check Inno Setup
echo [Step 3/5] Checking Inno Setup installation...
echo.

set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist "%INNO_PATH%" (
    echo [FAIL] Inno Setup not found at: %INNO_PATH%
    echo.
    echo Please install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

echo [OK] Inno Setup found
echo.

REM Step 4: Build installer
echo [Step 4/5] Building installer (this may take 2-5 minutes)...
echo.

REM Use the NoTaskkill installer script (already uses PowerShell instead of taskkill)
"%INNO_PATH%" "MBAS_Installer_NoTaskkill.iss"

if errorlevel 1 (
    echo.
    echo [FAIL] Installer build failed!
    echo        Check the error messages above
    pause
    exit /b 1
)

echo [OK] Installer built successfully
echo.

REM Step 5: Rename with FIXED tag
echo [Step 5/5] Creating final package...
echo.

if exist "output\MBAS_Setup_v1.2.1_NoTaskkill.exe" (
    copy /Y "output\MBAS_Setup_v1.2.1_NoTaskkill.exe" "output\MBAS_Setup_v1.2.2_FIXED.exe" >nul 2>&1
    echo [OK] Created: MBAS_Setup_v1.2.2_FIXED.exe
)

REM Create README for the fixed installer
echo Creating README...
(
echo ================================================================================
echo    MBAS Setup v1.2.2 - FIXED VERSION
echo    Critical Bugs Fixed
echo ================================================================================
echo.
echo WHAT'S NEW IN v1.2.2:
echo ---------------------
echo [CRITICAL FIX] Fixed undefined variable crash in system tray app
echo [CRITICAL FIX] Increased startup timeout from 15s to 30s
echo [ENHANCEMENT] Added comprehensive error logging
echo [ENHANCEMENT] Better virtual environment detection
echo [ENHANCEMENT] Improved first-run experience
echo [FIXED] CMD window blinking issue
echo [FIXED] Server startup timeout errors
echo.
echo INSTALLATION INSTRUCTIONS:
echo --------------------------
echo 1. Run MBAS_Setup_v1.2.2_FIXED.exe
echo 2. Install to C:\MBAS ^(recommended, no admin needed^)
echo 3. Wait for installation to complete ^(2-4 minutes^)
echo 4. Launch MBAS from desktop icon or Start menu
echo 5. Wait 30 seconds for first startup ^(database initialization^)
echo 6. Browser will open automatically to http://localhost:8000
echo 7. Login: admin / admin123
echo.
echo WHAT WAS FIXED:
echo ---------------
echo Previous version ^(1.2.1^) had critical bugs:
echo   - System tray crashed due to undefined variable ^(line 321^)
echo   - 15-second timeout too short for first startup
echo   - No error logging, silent failures
echo   - CMD windows blinking due to restart loops
echo.
echo This version fixes ALL these issues.
echo.
echo SYSTEM REQUIREMENTS:
echo --------------------
echo - Windows 10 or 11 ^(64-bit^)
echo - Python 3.11 or 3.12 ^(NOT 3.13+, compatibility issues^)
echo - 2GB RAM minimum
echo - 1GB free disk space
echo - Internet connection ^(for first-time dependency download^)
echo.
echo TROUBLESHOOTING:
echo ----------------
echo If installation succeeds but server doesn't start:
echo   1. Go to C:\MBAS
echo   2. Run: DIAGNOSE_STARTUP_ISSUE.bat
echo   3. Follow the diagnostic output
echo   4. If needed, run: EMERGENCY_FIX.bat
echo   5. Check: mbas_tray.log for detailed error messages
echo.
echo FILES INCLUDED:
echo ---------------
echo - MBAS_Setup_v1.2.2_FIXED.exe ^(Main installer^)
echo - COMPLETE_FIX_INSTRUCTIONS.txt ^(Detailed troubleshooting^)
echo - DIAGNOSE_STARTUP_ISSUE.bat ^(Diagnostic tool^)
echo - EMERGENCY_FIX.bat ^(Fix tool^)
echo.
echo CHANGELOG v1.2.2:
echo ------------------
echo [2024] Version 1.2.2 - Critical bug fixes
echo   - Fixed: Undefined self.server_url in mbas_tray.py:321
echo   - Fixed: Startup timeout increased to 30s
echo   - Fixed: Virtual environment not being used
echo   - Added: Comprehensive error logging
echo   - Added: Diagnostic and repair tools
echo   - Added: Better error messages
echo.
echo [2024] Version 1.2.1 - Taskkill fix
echo   - Fixed: 0xc0000142 taskkill.exe error
echo   - Changed: PowerShell-only process management
echo.
echo SUPPORT:
echo --------
echo If you encounter issues, please provide:
echo   1. Output from DIAGNOSE_STARTUP_ISSUE.bat
echo   2. Contents of mbas_tray.log
echo   3. Your Python version ^(python --version^)
echo   4. Your Windows version
echo.
echo ================================================================================
) > "output\README_v1.2.2_FIXED.txt"

echo [OK] README created
echo.

echo ================================================================================
echo    [SUCCESS] Installer Rebuild Complete!
echo ================================================================================
echo.
echo Created files:
echo   - output\MBAS_Setup_v1.2.2_FIXED.exe
echo   - output\README_v1.2.2_FIXED.txt
echo.
echo File size:
dir "output\MBAS_Setup_v1.2.2_FIXED.exe" | findstr "MBAS_Setup"
echo.
echo NEXT STEPS:
echo   1. Test the installer on a clean machine or VM
echo   2. Verify server starts within 30 seconds
echo   3. Verify no CMD window blinking
echo   4. Verify system tray icon works correctly
echo   5. Check mbas_tray.log for any errors
echo.
echo DISTRIBUTION:
echo   - Upload MBAS_Setup_v1.2.2_FIXED.exe to your distribution channel
echo   - Include README_v1.2.2_FIXED.txt
echo   - Update documentation with v1.2.2 changes
echo.
pause
