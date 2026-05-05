@echo off
title MBAS - Installation Fix Tool
color 0C

echo.
echo ================================================================
echo    MBAS Installation Fix Tool
echo ================================================================
echo.
echo This will fix the "Permission denied" error.
echo.
pause

echo [Step 1/4] Killing all Python processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 2 /nobreak >nul
echo [OK] Python processes terminated
echo.

echo [Step 2/4] Removing old virtual environment...
if exist "venv" (
    echo [*] Found old venv folder, removing...
    rmdir /s /q venv 2>nul

    if exist "venv" (
        echo [ERROR] Failed to remove venv folder!
        echo.
        echo SOLUTIONS:
        echo   1. Close all Command Prompt windows
        echo   2. Close Visual Studio Code or any IDEs
        echo   3. Restart your computer
        echo   4. Run this script again as Administrator
        echo.
        echo Trying alternative method...
        timeout /t 2 /nobreak >nul

        REM Try to delete with takeown and icacls
        takeown /f venv /r /d y >nul 2>&1
        icacls venv /grant administrators:F /t >nul 2>&1
        rmdir /s /q venv 2>nul

        if exist "venv" (
            echo [FAILED] Please manually delete the venv folder
            echo          Then run INSTALL.bat as Administrator
            pause
            exit /b 1
        )
    )

    echo [OK] Old venv removed successfully
    echo.
) else (
    echo [OK] No old venv found
    echo.
)

echo [Step 3/4] Checking for double folder issue...
if exist "%~dp0MBAS_v1.0.9_Production_Ready" (
    echo [WARNING] Double folder detected!
    echo.
    echo You have:
    echo   %~dp0
    echo   └── MBAS_v1.0.9_Production_Ready\
    echo.
    echo This is incorrect. Files should be directly in:
    echo   %~dp0
    echo.
    echo Please:
    echo   1. Move all files from inner folder to parent
    echo   2. Delete the inner MBAS_v1.0.9_Production_Ready folder
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Folder structure is correct
    echo.
)

echo [Step 4/4] Checking write permissions...
echo test > test_file.tmp 2>nul
if exist test_file.tmp (
    del test_file.tmp
    echo [OK] Write permissions verified
    echo.
) else (
    echo [ERROR] No write permissions!
    echo.
    echo SOLUTIONS:
    echo   1. Run this script as Administrator
    echo   2. Check if F: drive is read-only
    echo   3. Try installing to C:\MBAS instead
    echo.
    pause
    exit /b 1
)

echo ================================================================
echo    [SUCCESS] All issues fixed!
echo ================================================================
echo.
echo Next step:
echo   1. Close this window
echo   2. Right-click INSTALL.bat
echo   3. Select "Run as Administrator"
echo   4. Wait for installation to complete
echo.
echo ================================================================
echo.
pause
