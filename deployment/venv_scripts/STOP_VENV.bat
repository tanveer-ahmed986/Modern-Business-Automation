@echo off
title MBAS - Stop Server
color 0C

echo.
echo ================================================================
echo    MBAS - Stopping Server
echo ================================================================
echo.

REM Kill any Python processes running uvicorn
taskkill /F /FI "WINDOWTITLE eq MBAS Server" >nul 2>&1
taskkill /F /IM python.exe /FI "IMAGENAME eq python.exe" /FI "MEMUSAGE gt 50000" >nul 2>&1

echo [OK] All MBAS server processes stopped.
echo.
echo You can now:
echo    - Close this window
echo    - Run START_MBAS.bat to restart the server
echo    - Run INSTALL.bat to reinstall
echo.
pause
