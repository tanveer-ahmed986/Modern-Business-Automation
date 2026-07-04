@echo off
:: ============================================================================
::  Z&T Technologies - Trust Certificate Installer
::  Run this BEFORE installing MBAS on a new computer
::  This registers Z&T Technologies as a trusted software publisher
:: ============================================================================

title Z^&T Technologies - Certificate Installer

echo.
echo ============================================================================
echo   Z^&T Technologies - Trust Certificate Installer
echo   State-of-the-Art Business Solutions
echo ============================================================================
echo.
echo   This will register Z^&T Technologies as a trusted publisher
echo   on this computer so MBAS can be installed without security warnings.
echo.
echo   This is a ONE-TIME setup. You only need to do this once per computer.
echo.

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo   [!] Administrator privileges required.
    echo   [!] Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo   [OK] Running with administrator privileges.
echo.

:: Find the certificate file
set "CERT_FILE=%~dp0ZT_Technologies_CodeSign.cer"
if not exist "%CERT_FILE%" (
    :: Try in certificates subfolder
    set "CERT_FILE=%~dp0certificates\ZT_Technologies_CodeSign.cer"
)
if not exist "%CERT_FILE%" (
    echo   [ERROR] Certificate file not found!
    echo   Expected: ZT_Technologies_CodeSign.cer
    echo   Make sure this file is in the same folder as this script.
    echo.
    pause
    exit /b 1
)

echo   Certificate found: %CERT_FILE%
echo.
echo   Installing certificate to Trusted Root store...

:: Install to Trusted Root Certification Authorities (LocalMachine)
certutil -addstore -f "Root" "%CERT_FILE%" >nul 2>&1
if %errorLevel% equ 0 (
    echo   [OK] Added to Trusted Root Certification Authorities
) else (
    echo   [WARNING] Could not add to Trusted Root store
)

:: Install to Trusted Publishers (LocalMachine)
certutil -addstore -f "TrustedPublisher" "%CERT_FILE%" >nul 2>&1
if %errorLevel% equ 0 (
    echo   [OK] Added to Trusted Publishers
) else (
    echo   [WARNING] Could not add to Trusted Publishers store
)

echo.
echo ============================================================================
echo   Certificate Installation Complete!
echo ============================================================================
echo.
echo   Z^&T Technologies is now registered as a trusted publisher.
echo   You can now install MBAS without security warnings.
echo.
echo   Next step: Run MBAS_Professional_Setup_v2.0.4_ZT_Technologies.exe
echo.
pause
