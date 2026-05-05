; MBAS - Modern Business Automation System
; Professional Windows Installer for Z&T Technologies
; Version 2.0.2 - Fixed: installation hang, timeouts, offline support

#define MyAppName "MBAS - Modern Business Automation System"
#define MyAppVersion "2.0.2"
#define MyAppPublisher "Z&T Technologies"
#define MyAppURL "https://www.zttechnologies.org"
#define MyCompanySlogan "State-of-the-Art Business Solutions"

[Setup]
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/support
AppUpdatesURL={#MyAppURL}/updates
AppCopyright=Copyright (C) 2024-2026 {#MyAppPublisher}

; Installation settings
DefaultDirName={autopf}\MBAS
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
AllowNoIcons=yes

; Output
OutputDir=output
OutputBaseFilename=MBAS_Professional_Setup_v{#MyAppVersion}_ZT_Technologies
SetupIconFile=branding\mbas_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes

; UI
WizardStyle=modern
DisableWelcomePage=no

; Privileges (requires admin for C:\Program Files)
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Uninstall
UninstallDisplayIcon={app}\mbas_icon.ico
UninstallDisplayName={#MyAppName} - {#MyAppPublisher}

; Version info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} - {#MyCompanySlogan}
VersionInfoProductName={#MyAppName}

; Logging for troubleshooting
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel1=Welcome to MBAS Setup
WelcomeLabel2=A Product of {#MyAppPublisher}%n{#MyCompanySlogan}%n%nThis will install {#MyAppName} on your computer.%n%nRequires: Python 3.11 or 3.12%n%nVisit: {#MyAppURL}

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: checkedonce
Name: "startupicon"; Description: "Start MBAS with Windows"; GroupDescription: "Startup:"; Flags: unchecked

[Files]
; Backend (exclude dev databases, caches, logs, test files, backups)
Source: "..\..\backend\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,*.pyo,.pytest_cache,tests,*.db,*.db-shm,*.db-wal,*.log,backups,config\secret.key"

; Frontend (built production files)
Source: "..\..\frontend\dist\*"; DestDir: "{app}\frontend\dist"; Flags: ignoreversion recursesubdirs createallsubdirs

; Scripts
Source: "..\..\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs

; Bundled Python wheels (offline install support)
Source: "wheels\*"; DestDir: "{app}\wheels"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

; Icon
Source: "..\..\mbas_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; License
Source: "..\..\mbas.license"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; Documentation
Source: "..\PROFESSIONAL_PACKAGE\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

; Installation script (fixed - no pause, with timeouts)
Source: "INSTALL_MBAS.bat"; DestDir: "{app}"; Flags: ignoreversion

; Launcher scripts
Source: "START_MBAS_TRAY.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "START_MBAS_DIRECT.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "STOP_MBAS.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; Comment: "{#MyAppPublisher} - {#MyCompanySlogan}"
Name: "{group}\{#MyAppName} (Direct Mode)"; Filename: "{app}\START_MBAS_DIRECT.bat"; IconFilename: "{app}\mbas_icon.ico"
Name: "{group}\Stop MBAS"; Filename: "{app}\STOP_MBAS.bat"; IconFilename: "{app}\mbas_icon.ico"
Name: "{group}\Documentation"; Filename: "{app}\docs"; Comment: "MBAS Documentation"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

; Desktop
Name: "{autodesktop}\MBAS"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; Tasks: desktopicon; Comment: "{#MyAppPublisher} - {#MyCompanySlogan}"

; Startup
Name: "{userstartup}\MBAS"; Filename: "{app}\START_MBAS_TRAY.bat"; Tasks: startupicon

[Run]
; Install dependencies using the fixed batch script (no pause, with timeouts)
Filename: "cmd.exe"; Parameters: "/C ""{app}\INSTALL_MBAS.bat"""; WorkingDir: "{app}"; StatusMsg: "Installing dependencies (this may take 2-5 minutes, please wait)..."; Flags: runhidden waituntilterminated

; Launch MBAS
Filename: "{app}\START_MBAS_TRAY.bat"; Description: "Launch MBAS"; Flags: postinstall skipifsilent nowait unchecked

[UninstallRun]
; Stop MBAS gracefully
Filename: "{app}\STOP_MBAS.bat"; Flags: runhidden skipifdoesntexist waituntilterminated

; Kill any remaining processes
Filename: "cmd.exe"; Parameters: "/C taskkill /F /IM python.exe /T >nul 2>&1 & taskkill /F /IM pythonw.exe /T >nul 2>&1"; Flags: runhidden waituntilterminated

[UninstallDelete]
Type: filesandordirs; Name: "{app}\venv"
Type: filesandordirs; Name: "{app}\wheels"
Type: filesandordirs; Name: "{app}\backend\__pycache__"
Type: filesandordirs; Name: "{app}\backend\src\__pycache__"
Type: files; Name: "{app}\backend\*.log"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\install_log.txt"
Type: files; Name: "{app}\backend\mbas_database.db*"
Type: dirifempty; Name: "{app}\backend"
Type: dirifempty; Name: "{app}\frontend"
Type: dirifempty; Name: "{app}\scripts"
Type: dirifempty; Name: "{app}"

[Code]
var
  ResultCode: Integer;

function InitializeSetup(): Boolean;
var
  Version: TWindowsVersion;
begin
  Result := True;

  // Check Windows version (Windows 10+)
  GetWindowsVersionEx(Version);
  if Version.Major < 10 then
  begin
    MsgBox('MBAS requires Windows 10 or later.' + #13#10 +
           'Your Windows version is not supported.', mbError, MB_OK);
    Result := False;
    Exit;
  end;

  // Check Python - this is required, warn clearly
  if Exec('cmd.exe', '/C python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
      Log('Python detected on system')
    else
    begin
      if MsgBox('Python 3.11 or 3.12 is required but was not detected.' + #13#10 + #13#10 +
             'MBAS will NOT work without Python installed.' + #13#10 + #13#10 +
             'Download from: https://www.python.org/downloads/' + #13#10 +
             'IMPORTANT: Check "Add Python to PATH" during Python installation.' + #13#10 + #13#10 +
             'Do you want to continue anyway?',
             mbConfirmation, MB_YESNO) = IDNO then
      begin
        Result := False;
        Exit;
      end;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create company info file
    SaveStringToFile(ExpandConstant('{app}\COMPANY_INFO.txt'),
      '================================================================================' + #13#10 +
      '  MBAS - Modern Business Automation System' + #13#10 +
      '  Version {#MyAppVersion}' + #13#10 +
      '  A Product of Z&T Technologies' + #13#10 +
      '================================================================================' + #13#10 + #13#10 +
      'Company: Z&T Technologies' + #13#10 +
      'Slogan: State-of-the-Art Business Solutions' + #13#10 +
      'Website: www.zttechnologies.org' + #13#10 +
      'Email: zttechnologies12@gmail.com' + #13#10 + #13#10 +
      'Thank you for choosing MBAS!' + #13#10 +
      'We are committed to providing you with the best business automation solution.' + #13#10 + #13#10 +
      'For support, documentation, and updates, visit:' + #13#10 +
      'www.zttechnologies.org' + #13#10 + #13#10 +
      '================================================================================' + #13#10,
      False);
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  NeedsRestart := False;

  // Kill any running MBAS processes before install/upgrade
  Exec('cmd.exe',
       '/C taskkill /F /IM python.exe /T >nul 2>&1 & taskkill /F /IM pythonw.exe /T >nul 2>&1',
       '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;
