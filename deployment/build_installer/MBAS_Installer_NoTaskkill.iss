; MBAS - Modern Business Automation System
; PowerShell-Only Inno Setup Installer Script v1.2.1
; Fixed: Uses PowerShell instead of taskkill to avoid 0xc0000142 errors

#define MyAppName "MBAS - Modern Business Automation System"
#define MyAppVersion "1.2.1"
#define MyAppPublisher "ZT Products"
#define MyAppURL "https://github.com/your-org/mbas"
#define MyAppExeName "START_MBAS_TRAY.bat"

[Setup]
; App identification
AppId={{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation paths - Default to C:\MBAS for easier management
DefaultDirName=C:\MBAS
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
AllowNoIcons=yes

; Documentation
LicenseFile=..\MBAS_v1.0.9_Production_Ready\docs\LICENSE.txt
InfoBeforeFile=..\MBAS_v1.0.9_Production_Ready\README_FIRST.txt

; Output settings
OutputDir=.\output
OutputBaseFilename=MBAS_Setup_v1.2.1_NoTaskkill
SetupIconFile=..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico
Compression=lzma2/max
SolidCompression=yes

; UI settings
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=no
DisableReadyPage=no

; Privileges - Allow non-admin install to C:\MBAS
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog commandline

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Uninstall
UninstallDisplayIcon={app}\mbas_icon.ico
UninstallFilesDir={app}\uninstall

; Prevent multiple instances
AppMutex=MBAS_INSTALLER_MUTEX

; Close applications using files
CloseApplications=force
RestartApplications=no

; Logging for debugging
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel1=Welcome to MBAS Setup v1.2.1
WelcomeLabel2=This version fixes taskkill.exe errors (0xc0000142).%n%nThis will install {#MyAppName} on your computer.%n%nRecommended installation path: C:\MBAS (no admin required)%nProgram Files requires admin permissions for every operation.%n%nIt is recommended that you close all other applications before continuing.

[CustomMessages]
CloseApplicationsMessage=MBAS is currently running. Setup will automatically close it.%n%nClick OK to close MBAS and continue, or Cancel to exit Setup.

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startupicon"; Description: "Start MBAS automatically when Windows starts"; GroupDescription: "Startup:"; Flags: unchecked

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
Name: "{group}\Stop MBAS"; Filename: "{app}\STOP_MBAS.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Health Check"; Filename: "{app}\HEALTH_CHECK.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Documentation"; Filename: "{app}\README_FIRST.txt"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop icon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"; Tasks: desktopicon

; Startup folder (auto-start)
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"; Tasks: startupicon

[Run]
; Unblock files
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""Get-ChildItem -Path '{app}' -Recurse | Unblock-File"""; StatusMsg: "Unblocking files..."; Flags: runhidden waituntilterminated

; Add Windows Defender exclusion (if admin)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""try {{ Add-MpPreference -ExclusionPath '{app}' }} catch {{ }}"""; StatusMsg: "Configuring Windows Defender..."; Flags: runhidden

; Run installation (creates venv and installs dependencies)
Filename: "{app}\INSTALL.bat"; WorkingDir: "{app}"; StatusMsg: "Installing dependencies (2-4 minutes)..."; Flags: waituntilterminated

; Offer to launch MBAS after installation
Filename: "{app}\START_MBAS_TRAY.bat"; Description: "Launch {#MyAppName}"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent shellexec

[UninstallRun]
; Stop MBAS gracefully before uninstalling
Filename: "{app}\STOP_MBAS.bat"; RunOnceId: "StopMBAS_Graceful"; Flags: runhidden skipifdoesntexist waituntilterminated

; Force kill using PowerShell instead of taskkill
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""Get-Process | Where-Object {{$_.ProcessName -match 'python|pythonw|node'}} | Stop-Process -Force -ErrorAction SilentlyContinue"""; RunOnceId: "StopMBAS_Force"; Flags: runhidden waituntilterminated

; Wait for processes to fully terminate
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""Start-Sleep -Seconds 3"""; RunOnceId: "WaitForProcesses"; Flags: runhidden waituntilterminated

; Release file handles using PowerShell
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""Get-Process | Where-Object {{ $_.Path -like '*{app}*' }} | Stop-Process -Force -ErrorAction SilentlyContinue"""; RunOnceId: "ReleaseHandles"; Flags: runhidden

[UninstallDelete]
; Clean up virtual environment and generated files
Type: filesandordirs; Name: "{app}\venv"
Type: filesandordirs; Name: "{app}\backend\__pycache__"
Type: filesandordirs; Name: "{app}\backend\src\__pycache__"
Type: filesandordirs; Name: "{app}\backend\.pytest_cache"
Type: filesandordirs; Name: "{app}\frontend\node_modules"
Type: filesandordirs; Name: "{app}\frontend\dist"
Type: filesandordirs; Name: "{app}\frontend\build"

; Clean up database and logs (optional - user can backup first)
Type: files; Name: "{app}\backend\*.log"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\backend\mbas_database.db"
Type: files; Name: "{app}\backend\mbas_database.db-shm"
Type: files; Name: "{app}\backend\mbas_database.db-wal"

; Remove app directory if empty
Type: dirifempty; Name: "{app}\backend"
Type: dirifempty; Name: "{app}\frontend"
Type: dirifempty; Name: "{app}\scripts"
Type: dirifempty; Name: "{app}\docs"
Type: dirifempty; Name: "{app}"

[Code]
var
  PythonVersion: String;
  PythonFound: Boolean;
  IsUpgrade: Boolean;
  OldAppPath: String;

// Check if Python is installed and get version
function CheckPython(): Boolean;
var
  ResultCode: Integer;
  TmpFile: String;
begin
  Result := False;
  TmpFile := ExpandConstant('{tmp}\python_version.txt');

  // Try to get Python version
  if Exec('cmd.exe', '/C python --version > "' + TmpFile + '" 2>&1', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
    begin
      Result := True;
      // Could read version from TmpFile if needed
    end;
  end;
end;

// Forcefully kill all MBAS processes using PowerShell only (no taskkill)
procedure KillMBASProcesses();
var
  ResultCode: Integer;
  PSScript: String;
begin
  // PowerShell script to kill MBAS-related processes
  PSScript := 'Get-Process | Where-Object {' +
              '$_.ProcessName -match ''python|pythonw|node''' +
              '} | Stop-Process -Force -ErrorAction SilentlyContinue; ' +

              // Kill processes on MBAS ports
              '$ports = @(8000, 3000, 5173); ' +
              'foreach ($port in $ports) { ' +
              '  $procs = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; ' +
              '  foreach ($pid in $procs) { ' +
              '    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue ' +
              '  } ' +
              '}';

  // Execute PowerShell script
  Exec('powershell.exe',
       '-ExecutionPolicy Bypass -Command "' + PSScript + '"',
       '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

  // Wait for processes to terminate
  Sleep(2000);
end;

// Check if this is an upgrade
function IsUpgradeInstallation(): Boolean;
var
  UninstallKey: String;
begin
  UninstallKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}_is1';

  // Check HKLM for all users
  Result := RegKeyExists(HKLM, UninstallKey);

  // If not found, check HKCU for current user
  if not Result then
    Result := RegKeyExists(HKCU, UninstallKey);

  // Check if old installation directory exists
  if not Result then
  begin
    if DirExists('C:\Program Files\MBAS') or DirExists('C:\MBAS') then
      Result := True;
  end;
end;

// Backup database before upgrade
procedure BackupDatabase();
var
  SourceDB: String;
  BackupDB: String;
  BackupDir: String;
begin
  BackupDir := ExpandConstant('{userdesktop}\MBAS_Backup_Upgrade');

  // Try to backup from common locations
  if FileExists('C:\Program Files\MBAS\backend\mbas_database.db') then
    SourceDB := 'C:\Program Files\MBAS\backend\mbas_database.db'
  else if FileExists('C:\MBAS\backend\mbas_database.db') then
    SourceDB := 'C:\MBAS\backend\mbas_database.db'
  else
    Exit; // No database found

  // Create backup directory
  if not DirExists(BackupDir) then
    CreateDir(BackupDir);

  // Copy database
  BackupDB := BackupDir + '\mbas_database_' + GetDateTimeString('yyyymmdd_hhnnss', #0, #0) + '.db';

  if FileCopy(SourceDB, BackupDB, False) then
    MsgBox('Your database has been backed up to:' + #13#10 + BackupDB, mbInformation, MB_OK);
end;

// Initialize setup
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  Response: Integer;
begin
  Result := True;
  PythonFound := CheckPython();

  // Warn if Python is not found
  if not PythonFound then
  begin
    Response := MsgBox('Python 3.11 or 3.12 is required but was not detected.' + #13#10 + #13#10 +
                       'Download Python from: https://www.python.org/downloads/' + #13#10 + #13#10 +
                       'Continue anyway? (You can install Python later)',
                       mbConfirmation, MB_YESNO or MB_DEFBUTTON2);

    if Response = IDNO then
    begin
      Result := False;
      Exit;
    end;
  end;

  // Check if this is an upgrade
  IsUpgrade := IsUpgradeInstallation();

  if IsUpgrade then
  begin
    Response := MsgBox('MBAS is already installed. This will upgrade your installation.' + #13#10 + #13#10 +
                       'Your database will be automatically backed up.' + #13#10 + #13#10 +
                       'Continue with upgrade?',
                       mbConfirmation, MB_YESNO or MB_DEFBUTTON1);

    if Response = IDNO then
    begin
      Result := False;
      Exit;
    end;

    // Backup database before upgrade
    BackupDatabase();
  end;

  // Kill any running MBAS processes
  KillMBASProcesses();
end;

// Prepare to install
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  NeedsRestart := False;

  // Final process kill before file copy
  KillMBASProcesses();

  // Ensure no restart is needed
  NeedsRestart := False;
end;

// Post-install actions
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Try to add Windows Defender exclusion (requires admin)
    Exec('powershell.exe',
         '-ExecutionPolicy Bypass -Command "try { Add-MpPreference -ExclusionPath ''' + ExpandConstant('{app}') + ''' } catch { }"',
         '', SW_HIDE, ewNoWait, ResultCode);
  end;
end;

// Before uninstall
function InitializeUninstall(): Boolean;
var
  Response: Integer;
  BackupDir: String;
begin
  Result := True;

  // Ask about database backup
  Response := MsgBox('Do you want to backup your database before uninstalling?' + #13#10 + #13#10 +
                     'Recommended: Click YES to keep your data',
                     mbConfirmation, MB_YESNO or MB_DEFBUTTON1);

  if Response = IDYES then
  begin
    BackupDatabase();
  end;

  // Kill processes
  KillMBASProcesses();
end;

// During uninstall - handle locked files
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ResultCode: Integer;
  RetryCount: Integer;
  AppDir: String;
begin
  if CurUninstallStep = usUninstall then
  begin
    AppDir := ExpandConstant('{app}');

    // Multiple attempts to kill processes and release file handles
    for RetryCount := 1 to 3 do
    begin
      KillMBASProcesses();

      // Use PowerShell to force-close any remaining handles
      Exec('powershell.exe',
           '-ExecutionPolicy Bypass -Command "Get-Process | Where-Object { $_.Path -like ''*' + AppDir + '*'' } | Stop-Process -Force -ErrorAction SilentlyContinue"',
           '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

      Sleep(1000);
    end;
  end;

  if CurUninstallStep = usPostUninstall then
  begin
    // Final cleanup - remove any remaining files using PowerShell
    Exec('powershell.exe',
         '-ExecutionPolicy Bypass -Command "if (Test-Path ''' + AppDir + ''') { Remove-Item ''' + AppDir + ''' -Recurse -Force -ErrorAction SilentlyContinue }"',
         '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;
