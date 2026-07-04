@echo off
title MBAS - Machine ID Generator
color 0B

echo.
echo ================================================================
echo   MBAS - Machine ID Generator
echo   Z^&T Technologies
echo ================================================================
echo.
echo   This generates your unique Machine ID for hardware-locked
echo   licensing. Send this ID to your MBAS vendor.
echo.
echo ================================================================
echo.

python -c "import platform,uuid,hashlib;mid=hashlib.sha256(('|'.join([platform.processor(),str(uuid.getnode()),platform.node()])).encode()).hexdigest();print('  Your Machine ID:');print();print('  '+mid)"

if errorlevel 1 (
    echo   [ERROR] Python is not installed or not in PATH.
    echo   Please install Python from https://www.python.org/downloads/
)

echo.
echo ================================================================
echo   Copy the ID above and send it to your MBAS vendor.
echo ================================================================
echo.
pause
