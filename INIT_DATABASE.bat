@echo off
title Initialize MBAS Database
color 0A

echo.
echo ============================================================
echo   MBAS - Database Initialization
echo ============================================================
echo.

echo This will create the database and default admin user
echo.
pause

REM Try method 1: Use init_db.py script
echo [Method 1] Looking for init_db.py script...
if exist "backend\src\scripts\init_db.py" (
    echo [*] Found init_db.py, running...
    cd backend
    python src\scripts\init_db.py
    cd ..

    if errorlevel 1 (
        echo [ERROR] init_db.py failed
    ) else (
        goto :success
    )
)

REM Try method 2: Use create_admin_user.py
echo.
echo [Method 2] Using create_admin_user.py...
python create_admin_user.py

if errorlevel 1 (
    echo.
    echo [ERROR] Database initialization failed
    echo.
    echo Possible issues:
    echo - Backend dependencies not installed
    echo - Wrong directory
    echo - Database file locked
    echo.
    pause
    exit /b 1
)

:success
echo.
echo ============================================================
echo   SUCCESS! Database initialized
echo ============================================================
echo.
echo You can now login with:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: Change the password after first login!
echo   Settings - Users - Edit admin - Change password
echo.
pause
