================================================================================
    MBAS INSTALLATION ERROR FIX
    Error: taskkill.exe - Application Error (0xc0000142)
================================================================================

PROBLEM SUMMARY:
The installer hung for ~15 minutes and then showed:
"taskkill.exe - Application Error: The application was unable to start
correctly (0xc0000142). Click OK to close the application."

CAUSE:
Your Windows system has a corrupted taskkill.exe file (DLL initialization
failure). This is a Windows system file, not an MBAS issue.

Error code 0xc0000142 indicates corrupted system files, often caused by:
- Incomplete Windows updates
- Corrupted Visual C++ redistributables
- Antivirus interference
- System file corruption

================================================================================
    SOLUTION OPTIONS (Choose ONE)
================================================================================

OPTION 1: PORTABLE INSTALLATION (RECOMMENDED - Fastest)
-------------------------------------------------------
No installer needed. Direct file extraction and setup.
Perfect when system files are corrupted.

Steps:
1. Double-click: PORTABLE_INSTALL_MBAS.bat
2. Follow the prompts
3. Installation takes 3-5 minutes
4. No system file dependencies

This is the EASIEST and FASTEST option!


OPTION 2: FIX SYSTEM FILES + RETRY INSTALLER
--------------------------------------------
Repair Windows system files and try the installer again.

Steps:
1. Double-click: FIX_TASKKILL_ERROR_AND_INSTALL.bat
2. When prompted, allow it to run System File Checker (requires admin)
3. Wait 10-20 minutes for SFC scan to complete
4. Choose whether to use portable installation or retry installer


OPTION 3: USE FIXED INSTALLER (Developer must build it first)
-------------------------------------------------------------
A new installer that doesn't use taskkill.exe at all.
Uses PowerShell exclusively for process management.

Developer steps (on the development machine):
1. Go to: deployment\build_installer\
2. Run: BUILD_FIXED_INSTALLER.bat
3. This creates: MBAS_Setup_v1.2.1_NoTaskkill.exe
4. Copy this new installer to the target machine

User steps:
1. Run: MBAS_Setup_v1.2.1_NoTaskkill.exe
2. Follow normal installation process

This installer will never call taskkill.exe, avoiding the error entirely.


================================================================================
    RECOMMENDED APPROACH
================================================================================

For immediate installation:
  --> Use OPTION 1 (PORTABLE_INSTALL_MBAS.bat)
      This bypasses the entire installer and system file issues.

To fix your system for the future:
  --> Use OPTION 2 after installing with OPTION 1
      This repairs Windows system files properly.

For developers creating packages:
  --> Use OPTION 3 to build a more compatible installer
      This prevents the issue on other machines with similar problems.


================================================================================
    WHAT EACH SCRIPT DOES
================================================================================

FIX_TASKKILL_ERROR_AND_INSTALL.bat
  - Tests if taskkill.exe works
  - Runs Windows System File Checker (sfc /scannow)
  - Repairs corrupted system files including taskkill.exe
  - Offers installation options after repair

PORTABLE_INSTALL_MBAS.bat
  - Manually extracts MBAS files (no installer)
  - Uses PowerShell instead of taskkill for process management
  - Creates Python virtual environment
  - Installs dependencies
  - Creates shortcuts
  - Ready to use in 3-5 minutes

BUILD_FIXED_INSTALLER.bat (for developers)
  - Builds a new installer (MBAS_Installer_NoTaskkill.iss)
  - Uses PowerShell exclusively (no taskkill dependency)
  - More compatible with locked-down systems
  - Includes all previous fixes


================================================================================
    AFTER SUCCESSFUL INSTALLATION
================================================================================

1. Look for the MBAS icon on your desktop
2. Double-click to start MBAS
3. Wait 10-20 seconds for services to start
4. Open browser to: http://localhost:3000
5. Login with:
   Username: admin
   Password: admin123
   (Change these after first login!)


================================================================================
    NEED HELP?
================================================================================

If portable installation also fails, check:
1. Python is installed (python --version)
2. You have write permissions to C:\MBAS
3. Antivirus is not blocking the installation
4. Windows Defender hasn't quarantined files

For detailed logs:
- Check: %TEMP%\Setup Log *.txt (installer logs)
- Run: START_MBAS_TRAY_DEBUG.bat (after installation)


================================================================================
    TECHNICAL DETAILS (For IT/Developers)
================================================================================

The original installer (MBAS_Installer_Robust.iss) uses taskkill.exe in:
- KillMBASProcesses() function (lines 204, 205, 208)
- Port-based process killing (lines 211-213)
- Uninstall routines (line 139)

When taskkill.exe fails with 0xc0000142:
- Exec() calls hang waiting for taskkill to complete
- Installer appears frozen for ~15 minutes (timeout)
- Eventually fails with the error dialog

The fixed installer (MBAS_Installer_NoTaskkill.iss):
- Replaces all taskkill calls with PowerShell Stop-Process
- Uses Get-Process | Where-Object | Stop-Process pattern
- More robust error handling with -ErrorAction SilentlyContinue
- No dependency on potentially corrupted system executables

PowerShell is more reliable because:
- Native cmdlets less likely to be corrupted
- Better error handling options
- Can target processes by multiple criteria
- Works consistently across Windows versions


================================================================================
