' ============================================================================
'  MBAS Silent Launcher
'  Z&T Technologies - State-of-the-Art Business Solutions
'  Version 2.5.0 - All runtime data in ProgramData
'  Launches MBAS tray application without any CMD window
' ============================================================================

Dim WshShell, fso, appDir, venvDir, dataDir, logDir, pythonw, pythonExe, trayScript, logFile

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS file is located
appDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Paths - writable data in ProgramData (Program Files is read-only)
dataDir = WshShell.ExpandEnvironmentStrings("%ProgramData%") & "\MBAS"
logDir = dataDir & "\logs"
venvDir = dataDir & "\venv"
pythonw = venvDir & "\Scripts\pythonw.exe"
pythonExe = venvDir & "\Scripts\python.exe"
trayScript = appDir & "\scripts\mbas_tray.py"
logFile = logDir & "\mbas_startup.log"

' Ensure log directory exists
If Not fso.FolderExists(dataDir) Then fso.CreateFolder(dataDir)
If Not fso.FolderExists(logDir) Then fso.CreateFolder(logDir)

' Write startup log
On Error Resume Next
Set logStream = fso.OpenTextFile(logFile, 8, True)
If Not logStream Is Nothing Then
    logStream.WriteLine "[" & Now & "] MBAS VBS Launcher started"
    logStream.WriteLine "[INFO] App dir: " & appDir
    logStream.WriteLine "[INFO] Venv dir: " & venvDir
    logStream.Close
End If
On Error GoTo 0

' Check 1: Virtual environment exists
If Not fso.FileExists(pythonw) And Not fso.FileExists(pythonExe) Then
    ' Try to run installer first
    If fso.FileExists(appDir & "\INSTALL_MBAS.bat") Then
        Dim installResult
        installResult = MsgBox("MBAS environment not found." & vbCrLf & vbCrLf & _
            "Would you like to run the setup now?" & vbCrLf & _
            "(This requires Administrator privileges)", _
            vbYesNo + vbQuestion, "MBAS - First Time Setup")
        If installResult = vbYes Then
            WshShell.Run "cmd.exe /C """ & appDir & "\INSTALL_MBAS.bat""", 1, True
        End If
        ' Re-check after install
        If Not fso.FileExists(pythonw) And Not fso.FileExists(pythonExe) Then
            MsgBox "MBAS environment setup failed." & vbCrLf & vbCrLf & _
                "Please check install log at:" & vbCrLf & logDir & "\install_log.txt", _
                vbCritical, "MBAS - Setup Error"
            WScript.Quit 1
        End If
    Else
        MsgBox "MBAS virtual environment not found at:" & vbCrLf & venvDir & vbCrLf & vbCrLf & _
            "Please reinstall MBAS.", _
            vbCritical, "MBAS Error"
        WScript.Quit 1
    End If
End If

' Check 2: Tray script exists
If Not fso.FileExists(trayScript) Then
    MsgBox "MBAS application files are missing:" & vbCrLf & trayScript & vbCrLf & vbCrLf & _
        "Please reinstall MBAS.", _
        vbCritical, "MBAS Error"
    WScript.Quit 1
End If

' Check 3: Backend files exist
If Not fso.FileExists(appDir & "\backend\src\main.py") Then
    MsgBox "MBAS backend files are missing." & vbCrLf & vbCrLf & _
        "Please reinstall MBAS.", _
        vbCritical, "MBAS Error"
    WScript.Quit 1
End If

' Launch the tray app silently using pythonw.exe (no console window)
Dim launcher, cmd
If fso.FileExists(pythonw) Then
    launcher = pythonw
Else
    launcher = pythonExe
End If

' Run hidden (0 = SW_HIDE), don't wait for completion (False)
WshShell.CurrentDirectory = appDir
WshShell.Run """" & launcher & """ """ & trayScript & """", 0, False

' Log success
On Error Resume Next
Set logStream = fso.OpenTextFile(logFile, 8, True)
If Not logStream Is Nothing Then
    logStream.WriteLine "[" & Now & "] Tray app launched successfully via " & launcher
    logStream.Close
End If
On Error GoTo 0

Set fso = Nothing
Set WshShell = Nothing
WScript.Quit 0
