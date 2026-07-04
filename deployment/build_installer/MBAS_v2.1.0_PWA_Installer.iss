; MBAS - Modern Business Automation System
; PWA Edition v2.1.0 - Installer Script
; Optimized for Windows 7/10/11, tablets, and smartphones

#define MyAppName "MBAS - Business Automation System"
#define MyAppVersion "2.1.0"
#define MyAppPublisher "Z&T Technologies"
#define MyAppURL "https://www.zttechnologies.org"
#define MyCompanySlogan "Progressive Web App Edition"

[Setup]
AppId={{B2C3D4E5-F6A7-4B5C-9D0E-1F2A3B4C5D6E}
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
OutputBaseFilename=MBAS_v2.1.0_PWA_Professional_Setup
SetupIconFile=..\..\mbas_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes

; UI
WizardStyle=modern
DisableWelcomePage=no

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Uninstall
UninstallDisplayIcon={app}\mbas_icon.ico
UninstallDisplayName={#MyAppName} v{#MyAppVersion}

; Version info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} - {#MyCompanySlogan}
VersionInfoProductName={#MyAppName}

; Logging
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel1=Welcome to MBAS v2.1.0 PWA Setup
WelcomeLabel2=A Product of {#MyAppPublisher}%n{#MyCompanySlogan}%n%nProgressive Web App - Works offline!%n%nSupports:%n  - Windows 7/10/11%n  - Python 3.10/3.11/3.12%n  - Mobile devices via WiFi%n%nVisit: {#MyAppURL}

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: checkedonce
Name: "startupicon"; Description: "Start MBAS with Windows"; GroupDescription: "Startup:"; Flags: unchecked

[Files]
; Backend (exclude dev files)
Source: "..\..\backend\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,*.pyo,.pytest_cache,tests,*.db,*.db-shm,*.db-wal,*.log,backups,config\secret.key,data"

; Frontend (PWA build)
Source: "..\..\frontend\dist\*"; DestDir: "{app}\frontend\dist"; Flags: ignoreversion recursesubdirs createallsubdirs

; Scripts
Source: "..\..\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

; Icon
Source: "..\..\mbas_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Production License (STANDARD tier, perpetual, valid signature)
Source: "production_license.json"; DestDir: "{app}"; DestName: "mbas.license"; Flags: ignoreversion confirmoverwrite

; Documentation
Source: "PWA_QUICK_START.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "MOBILE_TESTING_GUIDE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\PWA_TESTING_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion skipifsourcedoesntexist

; Installation and launcher scripts
Source: "INSTALL_PWA.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "START_MBAS_PWA.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "START_MBAS_PWA_SILENT.vbs"; DestDir: "{app}"; Flags: ignoreversion
Source: "STOP_MBAS.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "STOP_MBAS_SILENT.vbs"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MBAS"; Filename: "{app}\START_MBAS_PWA_SILENT.vbs"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"
Name: "{group}\Stop MBAS"; Filename: "{app}\STOP_MBAS_SILENT.vbs"; WorkingDir: "{app}"
Name: "{group}\Uninstall MBAS"; Filename: "{uninstallexe}"
Name: "{autodesktop}\MBAS v2.1.0"; Filename: "{app}\START_MBAS_PWA_SILENT.vbs"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{autostartup}\MBAS"; Filename: "{app}\START_MBAS_PWA_SILENT.vbs"; IconFilename: "{app}\mbas_icon.ico"; WorkingDir: "{app}"; Tasks: startupicon

[Run]
; Install Python dependencies (hidden window)
Filename: "{app}\INSTALL_PWA.bat"; Description: "Install Python dependencies and initialize database"; Flags: postinstall runascurrentuser waituntilterminated runhidden

; Start MBAS after installation (silent, no CMD window)
Filename: "wscript.exe"; Parameters: """{app}\START_MBAS_PWA_SILENT.vbs"""; Description: "Launch MBAS now"; Flags: postinstall nowait skipifsilent runascurrentuser

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  PythonVer: String;
begin
  Result := True;

  // Check if Python is installed
  if not Exec('cmd.exe', '/c python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if MsgBox('Python is not installed or not in PATH.' + #13#10 + #13#10 +
              'MBAS requires Python 3.10, 3.11, or 3.12.' + #13#10 + #13#10 +
              'Do you want to continue anyway? (You''ll need to install Python manually)',
              mbConfirmation, MB_YESNO) = IDYES then
      Result := True
    else
      Result := False;
  end;
end;
