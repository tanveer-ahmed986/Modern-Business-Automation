; MBAS - Modern Business Automation System
; Inno Setup Installer Script v1.1.0
; This creates a self-contained Windows installer with embedded Python

#define MyAppName "MBAS - Modern Business Automation System"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "ZT Products"
#define MyAppURL "https://github.com/your-org/mbas"
#define MyAppExeName "MBAS.exe"
#define PythonVersion "3.12.1"

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
InfoAfterFile=..\MBAS_v1.0.9_Production_Ready\QUICK_START_CARD.txt

; Output settings
OutputDir=.\output
OutputBaseFilename=MBAS_Setup_v1.1.0
SetupIconFile=..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico
Compression=lzma2/max
SolidCompression=yes

; UI settings
WizardStyle=modern
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

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
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "Create a &Quick Launch icon"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Start MBAS automatically when Windows starts"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Embedded Python runtime (will be downloaded/included separately)
; NOTE: Comment this out if python-3.12.1-embed-amd64 folder doesn't exist yet
; The BUILD_INSTALLER.bat will download it automatically
Source: "python-{#PythonVersion}-embed-amd64\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists(ExpandConstant('{src}\python-{#PythonVersion}-embed-amd64'))

; MBAS Application files
Source: "..\MBAS_v1.0.9_Production_Ready\backend\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\MBAS_v1.0.9_Production_Ready\frontend\*"; DestDir: "{app}\frontend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\MBAS_v1.0.9_Production_Ready\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\MBAS_v1.0.9_Production_Ready\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs

; Configuration and license files
Source: "..\MBAS_v1.0.9_Production_Ready\mbas.license"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Startup scripts
Source: "..\MBAS_v1.0.9_Production_Ready\START_MBAS_TRAY.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\STOP_MBAS.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\HEALTH_CHECK.bat"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "..\MBAS_v1.0.9_Production_Ready\README_FIRST.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "..\MBAS_v1.0.9_Production_Ready\QUICK_START_CARD.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\MBAS_v1.0.9_Production_Ready\QUICK_REFERENCE.txt"; DestDir: "{app}"; Flags: ignoreversion

; Pre-built virtual environment with all dependencies
Source: "venv_prebuilt\*"; DestDir: "{app}\venv"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu icons
Name: "{group}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"
Name: "{group}\Stop MBAS"; Filename: "{app}\STOP_MBAS.bat"; IconFilename: "{app}\mbas_icon.ico"
Name: "{group}\Health Check"; Filename: "{app}\HEALTH_CHECK.bat"; IconFilename: "{app}\mbas_icon.ico"
Name: "{group}\Quick Reference"; Filename: "{app}\QUICK_REFERENCE.txt"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop icon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; Tasks: desktopicon

; Quick Launch icon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; Tasks: quicklaunchicon

; Startup folder (auto-start)
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\START_MBAS_TRAY.bat"; IconFilename: "{app}\mbas_icon.ico"; Tasks: startupicon

[Run]
; Initialize database on first run
Filename: "{app}\venv\Scripts\python.exe"; Parameters: "-c ""from pathlib import Path; import sys; sys.path.insert(0, '{app}\\backend\\src'); from scripts.init_db import bootstrap; bootstrap()"""; WorkingDir: "{app}\backend"; StatusMsg: "Initializing database..."; Flags: runhidden

; Offer to launch MBAS after installation
Filename: "{app}\START_MBAS_TRAY.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Stop MBAS before uninstalling
Filename: "{app}\STOP_MBAS.bat"; RunOnceId: "StopMBAS"; Flags: runhidden skipifdoesntexist

[UninstallDelete]
; Clean up database and logs
Type: files; Name: "{app}\backend\mbas_database.db"
Type: files; Name: "{app}\backend\*.log"
Type: files; Name: "{app}\mbas_error.log"
Type: dirifempty; Name: "{app}"

[Code]
var
  ErrorLogPage: TOutputMsgMemoWizardPage;

procedure InitializeWizard;
begin
  // Create error log page for debugging
  ErrorLogPage := CreateOutputMsgMemoPage(wpInstalling,
    'Installation Progress', 'Detailed installation log',
    'The following operations were performed:', '');
end;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

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
  PythonPath: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Log installation completion
    ErrorLogPage.RichEditViewer.Lines.Add('Installation completed successfully.');
    ErrorLogPage.RichEditViewer.Lines.Add('');
    ErrorLogPage.RichEditViewer.Lines.Add('MBAS has been installed to: ' + ExpandConstant('{app}'));
    ErrorLogPage.RichEditViewer.Lines.Add('Database initialized: ' + ExpandConstant('{app}\backend\mbas_database.db'));

    // Add Windows Defender exclusion (optional, requires admin)
    PythonPath := ExpandConstant('{app}\python\python.exe');
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

  // Check for port 8000 availability
  if not Exec('netstat', '-ano | findstr :8000', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    ErrorLogPage.RichEditViewer.Lines.Add('Port 8000 is available.');
  end
  else
  begin
    ErrorLogPage.RichEditViewer.Lines.Add('WARNING: Port 8000 may be in use. MBAS server uses port 8000.');
  end;
end;
