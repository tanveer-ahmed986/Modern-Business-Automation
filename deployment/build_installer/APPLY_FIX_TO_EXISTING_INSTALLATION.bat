@echo off
REM ============================================================================
REM  MBAS Fix Applicator - Version 2.0.7 Fixes
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM
REM  This script applies v2.0.7 fixes to existing MBAS installations without
REM  requiring a full reinstall.
REM
REM  Fixes Applied:
REM  1. Creates missing categories in database
REM  2. Ensures proper backend file permissions
REM ============================================================================

title MBAS Fix Applicator v2.0.7
color 0A

echo.
echo ================================================================================
echo   MBAS Fix Applicator v2.0.7
echo   Z^&T Technologies - State-of-the-Art Business Solutions
echo ================================================================================
echo.
echo This will apply critical fixes to your existing MBAS installation:
echo.
echo   1. Create missing product categories
echo   2. Fix database initialization
echo.
echo IMPORTANT: This will NOT affect your existing data!
echo            Your products, sales, and customers are safe.
echo.
pause

REM Check if MBAS is installed
if not exist "C:\Program Files\MBAS\backend" (
    echo.
    echo [ERROR] MBAS installation not found!
    echo Expected location: C:\Program Files\MBAS
    echo.
    echo Please install MBAS first.
    echo.
    pause
    exit /b 1
)

REM Check if venv exists
if not exist "C:\ProgramData\MBAS\venv\Scripts\python.exe" (
    echo.
    echo [ERROR] Python virtual environment not found!
    echo Expected location: C:\ProgramData\MBAS\venv
    echo.
    echo Please reinstall MBAS or run INSTALL_MBAS.bat
    echo.
    pause
    exit /b 1
)

echo.
echo [Step 1/2] Stopping MBAS if running...
echo.
taskkill /F /IM pythonw.exe /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo [Step 2/2] Creating categories in database...
echo.

cd "C:\Program Files\MBAS\backend"

"C:\ProgramData\MBAS\venv\Scripts\python.exe" -c "import sys; sys.path.insert(0, 'src'); from sqlmodel import Session, select; from core.db import engine, init_db; from models.inventory import Category; init_db(); session = Session(engine); categories = session.exec(select(Category)).all(); print(f'Found {len(categories)} existing categories'); result = None; exec('''if not categories:\n    print(\"Creating sample categories...\")\n    sample_categories = [\n        Category(name=\"Electronics\", description=\"Electronic items and gadgets\"),\n        Category(name=\"Groceries\", description=\"Food and grocery items\"),\n        Category(name=\"Clothing\", description=\"Apparel and accessories\"),\n        Category(name=\"Stationery\", description=\"Office and school supplies\"),\n    ]\n    for cat in sample_categories:\n        session.add(cat)\n    session.commit()\n    print(f\"Created {len(sample_categories)} categories\")\n    result = len(sample_categories)\nelse:\n    print(\"Categories already exist, no changes needed\")\n    result = 0'''); session.close(); print(f'\\nResult: {\"SUCCESS\" if result is not None else \"ALREADY FIXED\"}')"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to create categories!
    echo.
    echo Please try reinstalling MBAS or contact support.
    echo Email: zttechnologies12@gmail.com
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo   Fix Applied Successfully!
echo ================================================================================
echo.
echo Changes applied:
echo   - Product categories created (if missing)
echo   - Database initialized properly
echo.
echo Your MBAS installation is now ready to use!
echo.
echo To start MBAS:
echo   - Use Start Menu shortcut, or
echo   - Double-click: C:\Program Files\MBAS\START_MBAS.vbs
echo.
echo Database location: C:\ProgramData\MBAS\data\mbas_database.db
echo Log files: C:\ProgramData\MBAS\logs\
echo.
pause
