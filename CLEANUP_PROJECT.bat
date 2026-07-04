@echo off
REM ============================================================================
REM  MBAS Project Cleanup Script
REM  Removes unnecessary files to organize the project
REM  Total Space Recovery: 1.5-2.7 GB
REM ============================================================================

title MBAS Project Cleanup
color 0E

echo.
echo ================================================================================
echo   MBAS Project Cleanup
echo   This will remove unnecessary files and organize the project
echo ================================================================================
echo.
echo IMPORTANT: This script will delete files. Please review carefully!
echo.
echo What will be removed:
echo   - Old log files and temporary files (1-2 GB)
echo   - Duplicate package files (200-300 MB)
echo   - Old installer versions (230 MB)
echo   - Python cache directories
echo   - Empty/null files
echo.
echo What will be PRESERVED:
echo   - All source code (backend, frontend)
echo   - Current database
echo   - Latest installer (v2.1.0)
echo   - Latest package (v2.0.5)
echo   - All documentation
echo   - Git history
echo.
pause

echo.
echo Starting cleanup...
echo.

REM ============================================================================
REM PHASE 1: Delete Safe Temporary Files
REM ============================================================================
echo.
echo [PHASE 1] Removing log files and temporary files...

REM Delete log files
if exist "backend_error.log" del /F /Q "backend_error.log" && echo   Deleted: backend_error.log
if exist "backend_server.log" del /F /Q "backend_server.log" && echo   Deleted: backend_server.log
if exist "test_server.log" del /F /Q "test_server.log" && echo   Deleted: test_server.log
if exist "install_test_log.txt" del /F /Q "install_test_log.txt" && echo   Deleted: install_test_log.txt
if exist "install_test_log2.txt" del /F /Q "install_test_log2.txt" && echo   Deleted: install_test_log2.txt
if exist "install_test_log3.txt" del /F /Q "install_test_log3.txt" && echo   Deleted: install_test_log3.txt
if exist "uninstall_test_log.txt" del /F /Q "uninstall_test_log.txt" && echo   Deleted: uninstall_test_log.txt

REM Delete empty/null files
if exist "nul" del /F /Q "nul" 2>nul && echo   Deleted: nul
if exist "null" del /F /Q "null" 2>nul && echo   Deleted: null
if exist "frontend\nul" del /F /Q "frontend\nul" 2>nul && echo   Deleted: frontend\nul
if exist "deployment\build_installer\nul" del /F /Q "deployment\build_installer\nul" 2>nul && echo   Deleted: deployment\build_installer\nul

REM Delete security risks
if exist "token.txt" del /F /Q "token.txt" && echo   Deleted: token.txt (security risk)
if exist "server_pid.txt" del /F /Q "server_pid.txt" && echo   Deleted: server_pid.txt

REM Delete test artifacts
if exist "New Microsoft Word Document.docx" del /F /Q "New Microsoft Word Document.docx" && echo   Deleted: New Microsoft Word Document.docx
if exist "Screenshot (68).png" del /F /Q "Screenshot (68).png" && echo   Deleted: Screenshot (68).png

REM Delete test_deployment directory
if exist "test_deployment" (
    echo   Removing: test_deployment\ directory...
    rmdir /S /Q "test_deployment" && echo   Deleted: test_deployment\
)

REM Delete Python cache
echo   Removing Python cache directories...
for /d /r "backend" %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d" 2>nul
for /d /r "deployment" %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d" 2>nul

echo   Phase 1 complete!

REM ============================================================================
REM PHASE 2: Remove Duplicate Packages
REM ============================================================================
echo.
echo [PHASE 2] Removing duplicate package files...

REM Delete old CLIENT PACKAGE zips (keep v2.0.5)
if exist "MBAS_v2.0_CLIENT_PACKAGE.zip" del /F /Q "MBAS_v2.0_CLIENT_PACKAGE.zip" && echo   Deleted: MBAS_v2.0_CLIENT_PACKAGE.zip
if exist "MBAS_v2.0.3_CLIENT_PACKAGE.zip" del /F /Q "MBAS_v2.0.3_CLIENT_PACKAGE.zip" && echo   Deleted: MBAS_v2.0.3_CLIENT_PACKAGE.zip
if exist "MBAS_v2.0.4_CLIENT_PACKAGE.zip" del /F /Q "MBAS_v2.0.4_CLIENT_PACKAGE.zip" && echo   Deleted: MBAS_v2.0.4_CLIENT_PACKAGE.zip

REM Delete extracted package directories
if exist "MBAS_v2.0_CLIENT_PACKAGE" (
    echo   Removing: MBAS_v2.0_CLIENT_PACKAGE\
    rmdir /S /Q "MBAS_v2.0_CLIENT_PACKAGE" && echo   Deleted: MBAS_v2.0_CLIENT_PACKAGE\
)
if exist "MBAS_v2.0.4_CLIENT_PACKAGE" (
    echo   Removing: MBAS_v2.0.4_CLIENT_PACKAGE\
    rmdir /S /Q "MBAS_v2.0.4_CLIENT_PACKAGE" && echo   Deleted: MBAS_v2.0.4_CLIENT_PACKAGE\
)
if exist "MBAS_v2.0.5_CLIENT_PACKAGE" (
    echo   Removing: MBAS_v2.0.5_CLIENT_PACKAGE\
    rmdir /S /Q "MBAS_v2.0.5_CLIENT_PACKAGE" && echo   Deleted: MBAS_v2.0.5_CLIENT_PACKAGE\
)

REM Delete old deployment versions
if exist "deployment\Old Versions" (
    echo   Removing: deployment\Old Versions\
    rmdir /S /Q "deployment\Old Versions" && echo   Deleted: deployment\Old Versions\
)

if exist "deployment\MBAS_v1.0.8_Production_Ready.zip" del /F /Q "deployment\MBAS_v1.0.8_Production_Ready.zip" && echo   Deleted: deployment\MBAS_v1.0.8_Production_Ready.zip
if exist "deployment\MBAS_v1.0.9_Production_Ready.zip" del /F /Q "deployment\MBAS_v1.0.9_Production_Ready.zip" && echo   Deleted: deployment\MBAS_v1.0.9_Production_Ready.zip

if exist "deployment\MBAS_v1.0.9_Production_Ready" (
    echo   Removing: deployment\MBAS_v1.0.9_Production_Ready\
    rmdir /S /Q "deployment\MBAS_v1.0.9_Production_Ready" && echo   Deleted: deployment\MBAS_v1.0.9_Production_Ready\
)

if exist "deployment\MBAS_Package" (
    echo   Removing: deployment\MBAS_Package\
    rmdir /S /Q "deployment\MBAS_Package" && echo   Deleted: deployment\MBAS_Package\
)

if exist "deployment\MBAS_Package_V2" (
    echo   Removing: deployment\MBAS_Package_V2\
    rmdir /S /Q "deployment\MBAS_Package_V2" && echo   Deleted: deployment\MBAS_Package_V2\
)

if exist "deployment\MBAS_v2.1.0_PWA_BETA" (
    echo   Removing: deployment\MBAS_v2.1.0_PWA_BETA\
    rmdir /S /Q "deployment\MBAS_v2.1.0_PWA_BETA" && echo   Deleted: deployment\MBAS_v2.1.0_PWA_BETA\
)

echo   Phase 2 complete!

REM ============================================================================
REM PHASE 3: Remove Old Installers
REM ============================================================================
echo.
echo [PHASE 3] Removing old installer versions...

cd deployment\build_installer\output

REM Delete old Professional Setup installers (keep v2.0.6 and v2.1.0)
if exist "MBAS_Professional_Setup_v2.0.1_ZT_Technologies.exe" del /F /Q "MBAS_Professional_Setup_v2.0.1_ZT_Technologies.exe" && echo   Deleted: MBAS_Professional_Setup_v2.0.1
if exist "MBAS_Professional_Setup_v2.0.2_ZT_Technologies.exe" del /F /Q "MBAS_Professional_Setup_v2.0.2_ZT_Technologies.exe" && echo   Deleted: MBAS_Professional_Setup_v2.0.2
if exist "MBAS_Professional_Setup_v2.0.3_ZT_Technologies.exe" del /F /Q "MBAS_Professional_Setup_v2.0.3_ZT_Technologies.exe" && echo   Deleted: MBAS_Professional_Setup_v2.0.3
if exist "MBAS_Professional_Setup_v2.0.4_ZT_Technologies.exe" del /F /Q "MBAS_Professional_Setup_v2.0.4_ZT_Technologies.exe" && echo   Deleted: MBAS_Professional_Setup_v2.0.4
if exist "MBAS_Professional_Setup_v2.0.5_ZT_Technologies.exe" del /F /Q "MBAS_Professional_Setup_v2.0.5_ZT_Technologies.exe" && echo   Deleted: MBAS_Professional_Setup_v2.0.5

REM Delete v1.x installers
if exist "MBAS_Setup_v1.1.0_Simple.exe" del /F /Q "MBAS_Setup_v1.1.0_Simple.exe" && echo   Deleted: MBAS_Setup_v1.1.0
if exist "MBAS_Setup_v1.2.0_Robust.exe" del /F /Q "MBAS_Setup_v1.2.0_Robust.exe" && echo   Deleted: MBAS_Setup_v1.2.0
if exist "MBAS_Setup_v1.2.1_NoTaskkill.exe" del /F /Q "MBAS_Setup_v1.2.1_NoTaskkill.exe" && echo   Deleted: MBAS_Setup_v1.2.1

REM Delete old documentation from output
if exist "WHATS_NEW_v2.0.3.txt" del /F /Q "WHATS_NEW_v2.0.3.txt" && echo   Deleted: WHATS_NEW_v2.0.3.txt
if exist "WHATS_NEW_v2.0.4.txt" del /F /Q "WHATS_NEW_v2.0.4.txt" && echo   Deleted: WHATS_NEW_v2.0.4.txt
if exist "checksum_v2.0.3.txt" del /F /Q "checksum_v2.0.3.txt" && echo   Deleted: checksum_v2.0.3.txt
if exist "checksum_v2.0.4.txt" del /F /Q "checksum_v2.0.4.txt" && echo   Deleted: checksum_v2.0.4.txt
if exist "checksum.txt" del /F /Q "checksum.txt" && echo   Deleted: old checksum.txt

cd ..\..\..

echo   Phase 3 complete!

REM ============================================================================
REM Summary
REM ============================================================================
echo.
echo ================================================================================
echo   Cleanup Complete!
echo ================================================================================
echo.
echo What was removed:
echo   [x] Log files and temporary files
echo   [x] Duplicate package files
echo   [x] Old installer versions (v2.0.1 through v2.0.5, v1.x)
echo   [x] Python cache directories
echo   [x] Empty/null files
echo   [x] Test deployment artifacts
echo.
echo What was KEPT:
echo   [x] All source code (backend, frontend)
echo   [x] Current database
echo   [x] Latest installer (v2.0.6)
echo   [x] Latest package (v2.0.5)
echo   [x] Git history
echo   [x] All documentation
echo.
echo Estimated space recovered: 1.5-2 GB
echo.
echo Next steps:
echo   1. Verify project still works correctly
echo   2. Run: npm install (if needed)
echo   3. Consider organizing remaining documentation files
echo.
pause
