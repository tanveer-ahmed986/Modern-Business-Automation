@echo off
title MBAS - Manual Backend Test
color 0E

echo.
echo ========================================================================
echo    MBAS Backend Manual Test
echo    This will show you the actual backend error messages
echo ========================================================================
echo.

cd /d "C:\Program Files\MBAS\backend"

echo [*] Activating virtual environment...
call "..\venv\Scripts\activate.bat"

echo.
echo [*] Starting backend server manually...
echo.
echo This window will show all backend messages.
echo If there are errors, you'll see them here.
echo.
echo Press Ctrl+C to stop the server.
echo.
echo ========================================================================
echo.

python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo Backend stopped.
pause
