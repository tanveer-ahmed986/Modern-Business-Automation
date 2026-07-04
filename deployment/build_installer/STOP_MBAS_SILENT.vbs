' ============================================================================
' MBAS v2.1.0 PWA - Silent Stop Script (No CMD Window)
' Gracefully stops the MBAS server
' ============================================================================

Set objShell = CreateObject("WScript.Shell")

' Kill MBAS server processes
On Error Resume Next
intResult = objShell.Run("taskkill /FI ""WINDOWTITLE eq MBAS*"" /IM python.exe /F", 0, True)
On Error GoTo 0

If intResult = 0 Then
    MsgBox "MBAS server stopped successfully.", vbInformation, "MBAS Stopped"
Else
    MsgBox "MBAS server was not running.", vbInformation, "MBAS"
End If

WScript.Quit 0
