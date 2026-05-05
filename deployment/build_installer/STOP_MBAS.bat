@echo off
REM ============================================================================
REM  Stop MBAS Services - Z&T Technologies
REM  IMPORTANT: No 'pause' - this script is called by the uninstaller hidden.
REM ============================================================================

title Stopping MBAS
color 0C

echo.
echo ================================================================================
echo    Stopping MBAS Services...
echo    Z^&T Technologies
echo ================================================================================
echo.

taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
taskkill /F /IM MBAS.exe /T >nul 2>&1
taskkill /F /IM MBAS_Tray.exe /T >nul 2>&1

echo [OK] MBAS Stopped
echo.

REM Exit cleanly - NO pause (this runs hidden during uninstall)
exit /b 0
