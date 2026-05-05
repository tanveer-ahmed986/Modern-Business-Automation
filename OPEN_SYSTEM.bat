@echo off
echo ========================================
echo   MBAS - Quick Start Launcher
echo ========================================
echo.
echo Starting Backend Server...
start "MBAS Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn backend.src.main:app --host 127.0.0.1 --port 8000 --reload"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend Server...
start "MBAS Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Waiting 10 seconds for frontend to start...
timeout /t 10 /nobreak > nul

echo.
echo Opening browser...
start http://localhost:5173

echo.
echo ========================================
echo   MBAS System Started!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo.
echo Login: admin / admin123
echo.
echo Keep the Backend and Frontend windows open.
echo Press any key to close this launcher window...
pause > nul
