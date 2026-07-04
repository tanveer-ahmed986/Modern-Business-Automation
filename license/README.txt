================================================================
  MBAS LICENSE GENERATOR - QUICK START
================================================================

ISSUE FIXED: The batch file was missing "enabledelayedexpansion"
which caused it to close without generating the license.

================================================================
  RECOMMENDED: USE THE SIMPLE VERSION
================================================================

For the most reliable experience:

  Double-click: GENERATE_LICENSE_SIMPLE.bat

This version:
  - Simple, clear prompts
  - Better error handling
  - Won't close on errors
  - Shows detailed messages

================================================================
  ALL AVAILABLE TOOLS
================================================================

1. GENERATE_LICENSE_SIMPLE.bat   [RECOMMENDED]
   - Easiest to use
   - Best error handling
   - Won't close unexpectedly

2. GENERATE_LICENSE.bat
   - Full interactive version
   - More options
   - Fixed with enabledelayedexpansion

3. GENERATE_LICENSE.ps1
   - PowerShell version
   - Colorful output
   - Advanced features

4. TEST_LICENSE_GEN.bat
   - Tests if everything works
   - Generates test license
   - Shows debug info

================================================================
  QUICK TEST
================================================================

To verify everything works:

  1. Double-click: TEST_LICENSE_GEN.bat
  2. Wait for "SUCCESS!" message
  3. Check: license\test.license created

================================================================
  MANUAL GENERATION (IF BATCH FILES FAIL)
================================================================

Open Command Prompt and run:

  cd D:\gemini_modern_business_automation_system

  python tools\sign_license.py ^
      --licensee "ABC Pharmacy" ^
      --tier standard ^
      --type perpetual ^
      --output license\mbas.license

================================================================
  TROUBLESHOOTING
================================================================

If you get errors, see: TROUBLESHOOTING.md

Common fixes:
  - Install Python 3.11+ from python.org
  - Run: pip install cryptography
  - Run from Command Prompt (not double-click)
  - Use GENERATE_LICENSE_SIMPLE.bat instead

================================================================
  FILES IN THIS FOLDER
================================================================

GENERATE_LICENSE_SIMPLE.bat  - Recommended (easiest)
GENERATE_LICENSE.bat         - Full version (fixed)
GENERATE_LICENSE.ps1         - PowerShell version
TEST_LICENSE_GEN.bat         - Test tool
TROUBLESHOOTING.md           - Help guide
README.txt                   - This file

Generated licenses:
  mbas.license               - Main license file
  test.license               - Test license (if generated)

================================================================
  NEXT STEPS
================================================================

1. Try: GENERATE_LICENSE_SIMPLE.bat
2. If that works: Great! Use it for all licenses
3. If not: See TROUBLESHOOTING.md
4. Still stuck: Run commands manually (see above)

================================================================
