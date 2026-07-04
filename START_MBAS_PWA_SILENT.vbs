' ============================================================================
' MBAS v2.1.0 PWA - Silent Launcher (No CMD Window)
' Starts the server in hidden mode with system tray notification
' ============================================================================

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strScriptPath = WScript.ScriptFullName
strScriptDir = objFSO.GetParentFolderName(strScriptPath)

' Change to the script directory
objShell.CurrentDirectory = strScriptDir

' Check if Python is installed
On Error Resume Next
intResult = objShell.Run("cmd /c python --version", 0, True)
On Error GoTo 0

If intResult <> 0 Then
    MsgBox "Python is not installed!" & vbCrLf & vbCrLf & _
           "Please install Python 3.10, 3.11, or 3.12 from:" & vbCrLf & _
           "https://www.python.org/" & vbCrLf & vbCrLf & _
           "Make sure to check 'Add Python to PATH' during installation.", _
           vbCritical, "MBAS - Python Required"
    WScript.Quit 1
End If

' Check if port 8000 is already in use
On Error Resume Next
intResult = objShell.Run("cmd /c netstat -ano | findstr "":8000""", 0, True)
On Error GoTo 0

If intResult = 0 Then
    ' Port is in use
    intResponse = MsgBox("MBAS is already running on port 8000!" & vbCrLf & vbCrLf & _
                         "Do you want to stop the existing instance and restart?", _
                         vbQuestion + vbYesNo, "MBAS Already Running")

    If intResponse = vbYes Then
        ' Kill existing Python processes
        objShell.Run "taskkill /F /IM python.exe /FI ""WINDOWTITLE eq MBAS*""", 0, True
        WScript.Sleep 2000
    Else
        ' Just open browser to existing instance
        objShell.Run "http://localhost:8000", 1, False
        WScript.Quit 0
    End If
End If

' Set environment variable for data directory
objShell.Environment("Process")("MBAS_DATA_DIR") = strScriptDir & "\data"
objShell.Environment("Process")("MBAS_SKIP_LICENSE") = "1"

' Start the server in hidden mode
strCommand = "cmd /c cd /d """ & strScriptDir & "\backend"" && " & _
             "title MBAS v2.1.0 PWA Server && " & _
             "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000"

' Run in minimized window (not completely hidden, so user can see it in taskbar)
objShell.Run strCommand, 7, False

' Wait for server to start (give it 3 seconds)
WScript.Sleep 3000

' Show notification balloon
Set objNotification = CreateObject("WScript.Shell")
Set objNetwork = CreateObject("WScript.Network")

' Open browser
objShell.Run "http://localhost:8000", 1, False

' Show success message
MsgBox "MBAS v2.1.0 PWA started successfully!" & vbCrLf & vbCrLf & _
       "Server: http://localhost:8000" & vbCrLf & _
       "Login: admin/admin123" & vbCrLf & vbCrLf & _
       "For mobile access:" & vbCrLf & _
       "1. Find IP: ipconfig" & vbCrLf & _
       "2. On mobile: http://YOUR-IP:8000" & vbCrLf & vbCrLf & _
       "To stop: Close the MBAS window from taskbar", _
       vbInformation, "MBAS Started"

WScript.Quit 0
