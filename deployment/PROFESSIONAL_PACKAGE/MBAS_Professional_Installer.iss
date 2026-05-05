; MBAS - Modern Business Automation System
; Professional Windows Installer
; A Product of Z&T Technologies
; Version 2.0.2 - Fixed: installation hang, timeouts, offline support

#define MyAppName "MBAS - Business Automation System"
#define MyAppVersion "2.0.2"
#define MyAppPublisher "Z&T Technologies"
#define MyAppURL "https://www.zttechnologies.org"
#define MyAppExeName "MBAS.exe"
#define MyCompanyName "Z&T Technologies"
#define MyCompanySlogan "State-of-the-Art Business Solutions"

[Setup]
; App identification
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/support
AppUpdatesURL={#MyAppURL}/updates
AppCopyright=Copyright (C) 2024-2026 {#MyCompanyName}

; Installation paths
DefaultDirName={autopf}\MBAS
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
AllowNoIcons=yes

; Output settings
OutputDir=Output
OutputBaseFilename=MBAS_Professional_Setup_v{#MyAppVersion}_ZT_Technologies
SetupIconFile=branding\mbas_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
InternalCompressLevel=ultra64

; UI settings
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=no
DisableReadyPage=no

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Uninstall
UninstallDisplayIcon={app}\mbas_icon.ico
UninstallDisplayName={#MyAppName} ({#MyCompanyName})
UninstallFilesDir={app}\uninstall

; Version info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyCompanyName}
VersionInfoDescription={#MyAppName} - {#MyCompanySlogan}
VersionInfoCopyright=Copyright (C) 2024-2026 {#MyCompanyName}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

; Logging
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel1=Welcome to MBAS Setup
WelcomeLabel2=A Product of {#MyCompanyName}%n%n{#MyCompanySlogan}%n%nThis will install {#MyAppName} version {#MyAppVersion} on your computer.%n%nMBAS is a state-of-the-art business automation solution that helps you manage inventory, sales, purchases, and customer relationships.%n%nRequires: Python 3.11 or 3.12

[CustomMessages]
LaunchProgram=Launch {#MyAppName}
CreateDesktopIcon=Create a desktop icon
StartWithWindows=Start MBAS automatically when Windows starts

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "Shortcuts:"; Flags: checkedonce
Name: "startupicon"; Description: "{cm:StartWithWindows}"; GroupDescription: "Startup:"; Flags: unchecked
Name: "quicklaunch"; Description: "Create Quick Launch icon"; GroupDescription: "Shortcuts:"; Flags: unchecked

[Files]
; Embedded Python runtime (if available)
Source: "python-embed\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

; Backend application (exclude dev databases, caches, logs, backups)
Source: "package\backend\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,*.pyo,.pytest_cache,tests,*.db,*.db-shm,*.db-wal,*.log,backups,config\secret.key"

; Frontend application
Source: "package\frontend\*"; DestDir: "{app}\frontend"; Flags: ignoreversion recursesubdirs createallsubdirs

; Scripts and launchers
Source: "package\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs

; Bundled Python wheels (offline install support)
Source: "package\wheels\*"; DestDir: "{app}\wheels"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

; Branding files
Source: "branding\mbas_icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "branding\company_logo.png"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "branding\mbas.license"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; Documentation
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

; Launcher executables (if pre-built)
Source: "launchers\MBAS.exe"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "launchers\MBAS_Tray.exe"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; Configuration
Source: "config\settings.json"; DestDir: "{app}\config"; Flags: ignoreversion skipifsourcedoesntexist

; Installation script (fixed version - no pause, with timeouts)
Source: "..\build_installer\INSTALL_MBAS.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\build_installer\START_MBAS_TRAY.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\build_installer\START_MBAS_DIRECT.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\build_installer\STOP_MBAS.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; Comment: "Launch {#MyAppName} - A Product of {#MyCompanyName}"
Name: "{group}\{#MyAppName} (Direct Mode)"; Filename: "{app}\START_MBAS_DIRECT.bat"; IconFilename: "{app}\mbas_icon.ico"
Name: "{group}\Stop MBAS"; Filename: "{app}\STOP_MBAS.bat"; IconFilename: "{app}\mbas_icon.ico"
Name: "{group}\{#MyAppName} Documentation"; Filename: "{app}\docs"; Comment: "MBAS Documentation"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; Tasks: desktopicon; Comment: "Launch MBAS - {#MyCompanyName}"

; Quick Launch
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; Tasks: quicklaunch

; Startup
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; Tasks: startupicon

[Run]
; Install dependencies using the fixed batch script
; CRITICAL: Uses cmd.exe /C to ensure proper process termination
; The INSTALL_MBAS.bat has NO pause commands and exits cleanly with exit /b
Filename: "cmd.exe"; Parameters: "/C ""{app}\INSTALL_MBAS.bat"""; WorkingDir: "{app}"; StatusMsg: "Installing dependencies (this may take 2-5 minutes, please wait)..."; Flags: runhidden waituntilterminated

; Configure Windows Defender exclusion (non-blocking)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""try {{ Add-MpPreference -ExclusionPath '{app}' }} catch {{ }}"""; StatusMsg: "Configuring Windows security..."; Flags: runhidden waituntilterminated

; Launch MBAS
Filename: "{app}\START_MBAS_TRAY.bat"; Description: "{cm:LaunchProgram}"; Flags: nowait postinstall skipifsilent unchecked

[UninstallRun]
; Stop MBAS gracefully
Filename: "{app}\STOP_MBAS.bat"; RunOnceId: "StopMBAS"; Flags: runhidden skipifdoesntexist waituntilterminated

; Kill any remaining processes
Filename: "cmd.exe"; Parameters: "/C taskkill /F /IM python.exe /T >nul 2>&1 & taskkill /F /IM pythonw.exe /T >nul 2>&1 & taskkill /F /IM MBAS.exe /T >nul 2>&1"; RunOnceId: "KillProcesses"; Flags: runhidden waituntilterminated

[UninstallDelete]
; Clean up generated files
Type: filesandordirs; Name: "{app}\venv"
Type: filesandordirs; Name: "{app}\wheels"
Type: filesandordirs; Name: "{app}\backend\__pycache__"
Type: filesandordirs; Name: "{app}\backend\src\__pycache__"
Type: filesandordirs; Name: "{app}\backend\*.log"
Type: filesandordirs; Name: "{app}\*.log"
Type: files; Name: "{app}\install_log.txt"
Type: files; Name: "{app}\backend\mbas_database.db*"
Type: dirifempty; Name: "{app}\backend"
Type: dirifempty; Name: "{app}\frontend"
Type: dirifempty; Name: "{app}\scripts"
Type: dirifempty; Name: "{app}\python"
Type: dirifempty; Name: "{app}"

[Code]
var
  CompanyInfoPage: TOutputMsgWizardPage;
  ResultCode: Integer;

procedure InitializeWizard;
begin
  // Create company info page
  CompanyInfoPage := CreateOutputMsgPage(wpWelcome,
    'About Z&T Technologies',
    'State-of-the-Art Business Solutions',
    'Z&T Technologies is a leading provider of innovative business automation solutions. ' +
    'Our mission is to empower businesses with cutting-edge technology that streamlines operations, ' +
    'increases efficiency, and drives growth.' + #13#10 + #13#10 +
    'MBAS (Modern Business Automation System) is our flagship product, designed to help businesses ' +
    'of all sizes manage their inventory, sales, purchases, and customer relationships with ease.' + #13#10 + #13#10 +
    'Features:' + #13#10 +
    '  - Comprehensive inventory management' + #13#10 +
    '  - Point of sale (POS) system' + #13#10 +
    '  - Customer relationship management (CRM)' + #13#10 +
    '  - Purchase order management' + #13#10 +
    '  - Financial reporting and analytics' + #13#10 +
    '  - Multi-user support with role-based access' + #13#10 +
    '  - Automated backups and data security' + #13#10 + #13#10 +
    'Thank you for choosing Z&T Technologies!');
end;

function InitializeSetup(): Boolean;
var
  Version: TWindowsVersion;
begin
  Result := True;

  // Check Windows version
  GetWindowsVersionEx(Version);
  if Version.Major < 10 then
  begin
    MsgBox('MBAS requires Windows 10 or later.' + #13#10 + #13#10 +
           'Your version of Windows is not supported.' + #13#10 +
           'Please upgrade to Windows 10 or 11 to use MBAS.',
           mbError, MB_OK);
    Result := False;
    Exit;
  end;

  // Check Python - warn if not found
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
      '=================================================================================' + #13#10 +
      '  MBAS - Modern Business Automation System' + #13#10 +
      '  Version {#MyAppVersion}' + #13#10 +
      '  A Product of Z&T Technologies' + #13#10 +
      '=================================================================================' + #13#10 + #13#10 +
      'Company: Z&T Technologies' + #13#10 +
      'Slogan: State-of-the-Art Business Solutions' + #13#10 +
      'Website: https://www.zttechnologies.org' + #13#10 +
      'Email: zttechnologies12@gmail.com' + #13#10 + #13#10 +
      'Thank you for choosing MBAS!' + #13#10 +
      'We are committed to providing you with the best business automation solution.' + #13#10 + #13#10 +
      'For support, documentation, and updates, visit:' + #13#10 +
      'https://www.zttechnologies.org' + #13#10,
      False);
  end;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = CompanyInfoPage.ID then
  begin
    WizardForm.NextButton.Caption := 'Continue';
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  NeedsRestart := False;

  // Kill any running MBAS processes before install/upgrade
  Exec('cmd.exe',
       '/C taskkill /F /IM python.exe /T >nul 2>&1 & taskkill /F /IM pythonw.exe /T >nul 2>&1 & taskkill /F /IM MBAS.exe /T >nul 2>&1',
       '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;
