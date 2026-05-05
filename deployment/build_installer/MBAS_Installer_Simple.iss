; MBAS - Modern Business Automation System
; Inno Setup Installer Script v1.1.0 (Simplified Version)
; This creates a Windows installer (requires Python on target system)

#define MyAppName "MBAS - Modern Business Automation System"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "ZT Products"
#define MyAppURL "https://github.com/your-org/mbas"

[Setup]
; App identification
AppId={{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation paths
DefaultDirName={autopf}\MBAS
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\MBAS_v1.0.9_Production_Ready\docs\LICENSE.txt
InfoBeforeFile=..\MBAS_v1.0.9_Production_Ready\README_FIRST.txt
InfoAfterFile=..\MBAS_v1.0.9_Production_Ready\START_HERE_IF_PROBLEMS.txt

; Output settings
OutputDir=.\output
OutputBaseFilename=MBAS_Setup_v1.1.0_Simple
SetupIconFile=..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico
Compression=lzma2/max
SolidCompression=yes

; UI settings
WizardStyle=modern

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Uninstall
UninstallDisplayIcon={app}\mbas_icon.ico
UninstallFilesDir={app}\uninstall

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "Create a &Quick Launch icon"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Start MBAS automatically when Windows starts"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; MBAS Application files
Source: "..\MBAS_v1.0.9_Production_Ready\backend\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\MBAS_v1.0.9_Production_Ready\frontend\*"; DestDir: "{app}\frontend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\MBAS_v1.0.9_Production_Ready\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\MBAS_v1.0.9_Production_Ready\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs

; Configuration and license files
Source: "..\MBAS_v1.0.9_Production_Ready\mbas.license"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Installation and startup scripts
Source: "..\MBAS_v1.0.9_Production_Ready\INSTALL.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\START_MBAS_TRAY.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\START_MBAS_TRAY_DEBUG.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\STOP_MBAS.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\HEALTH_CHECK.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\EMERGENCY_FIX.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\UNBLOCK_FILES.bat"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "..\MBAS_v1.0.9_Production_Ready\README_FIRST.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "..\MBAS_v1.0.9_Production_Ready\START_HERE_IF_PROBLEMS.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\FIX_INSTALLATION_ISSUES.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\QUICK_REFERENCE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\INSTALLATION_FIXES_SUMMARY.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu icons
Name: "{group}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Start MBAS (Debug)"; Filename: "{app}\START_MBAS_TRAY_DEBUG.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Stop MBAS"; Filename: "{app}\STOP_MBAS.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Health Check"; Filename: "{app}\HEALTH_CHECK.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Emergency Fix"; Filename: "{app}\EMERGENCY_FIX.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Documentation"; Filename: "{app}\README_FIRST.txt"
Name: "{group}\Troubleshooting Guide"; Filename: "{app}\START_HERE_IF_PROBLEMS.txt"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop icon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"; Tasks: desktopicon

; Quick Launch icon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"; Tasks: quicklaunchicon

; Startup folder (auto-start)
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"; Tasks: startupicon

[Run]
; Unblock files and add Windows Defender exclusion
Filename: "powershell.exe"; Parameters: "-Command ""Get-ChildItem -Path '{app}' -Recurse | Unblock-File"""; StatusMsg: "Unblocking files..."; Flags: runhidden
Filename: "powershell.exe"; Parameters: "-Command ""Add-MpPreference -ExclusionPath '{app}'"""; StatusMsg: "Adding Windows Defender exclusion..."; Flags: runhidden

; Run installation (creates venv and installs dependencies)
Filename: "{app}\INSTALL.bat"; Parameters: ""; WorkingDir: "{app}"; StatusMsg: "Installing dependencies (this may take 2-4 minutes)..."; Flags: waituntilterminated

; Offer to launch MBAS after installation
Filename: "{app}\START_MBAS_TRAY.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent shellexec

[UninstallRun]
; Stop MBAS before uninstalling
Filename: "{app}\STOP_MBAS.bat"; RunOnceId: "StopMBAS"; Flags: runhidden skipifdoesntexist waituntilterminated

[UninstallDelete]
; Clean up virtual environment
Type: filesandordirs; Name: "{app}\venv"
; Clean up database and logs
Type: files; Name: "{app}\backend\mbas_database.db"
Type: files; Name: "{app}\backend\*.log"
Type: files; Name: "{app}\*.log"
Type: dirifempty; Name: "{app}"

[Code]
var
  PythonVersion: String;
  PythonFound: Boolean;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  PythonFound := False;

  // Check if Python is installed
  if Exec('cmd.exe', '/C python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
    begin
      PythonFound := True;
    end;
  end;

  if not PythonFound then
  begin
    if MsgBox('Python 3.11 or 3.12 is required but was not found on your system.' + #13#10 + #13#10 +
              'Would you like to:' + #13#10 +
              '  - Click YES to continue anyway (you can install Python later)' + #13#10 +
              '  - Click NO to cancel and install Python first' + #13#10 + #13#10 +
              'Download Python from: https://www.python.org/downloads/',
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;

  // Check if MBAS is already running
  if CheckForMutexes('MBAS_SYSTEM_MUTEX') then
  begin
    if MsgBox('MBAS is currently running. Do you want to close it and continue with installation?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Try to stop MBAS gracefully
      Exec('taskkill', '/F /IM python.exe /T', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Sleep(2000);
    end
    else
    begin
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Add Windows Defender exclusion (may fail if not admin, that's ok)
    Exec('powershell.exe',
         '-Command "Add-MpPreference -ExclusionPath ''' + ExpandConstant('{app}') + '''"',
         '', SW_HIDE, ewNoWait, ResultCode);
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  Result := '';

  // Stop any running Python processes
  Exec('taskkill', '/F /IM python.exe /T', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Exec('taskkill', '/F /IM pythonw.exe /T', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Sleep(1000);

  // Kill anything using port 8000
  Exec('cmd.exe', '/C for /f "tokens=5" %a in (''netstat -ano ^| findstr ":8000"'') do taskkill /F /PID %a', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Sleep(1000);
end;
