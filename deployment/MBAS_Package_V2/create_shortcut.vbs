' VBScript to create desktop shortcut with icon
' Usage: cscript create_shortcut.vbs <target_path> <shortcut_name> <icon_path>

Set args = WScript.Arguments
If args.Count < 2 Then
    WScript.Echo "Usage: create_shortcut.vbs <target_path> <shortcut_name> [icon_path]"
    WScript.Quit 1
End If

targetPath = args(0)
shortcutName = args(1)
iconPath = ""

If args.Count >= 3 Then
    iconPath = args(2)
End If

' Get desktop path
Set objShell = CreateObject("WScript.Shell")
desktopPath = objShell.SpecialFolders("Desktop")

' Create shortcut
Set objShortcut = objShell.CreateShortcut(desktopPath & "\" & shortcutName & ".lnk")
objShortcut.TargetPath = targetPath
objShortcut.WorkingDirectory = objShell.CurrentDirectory
objShortcut.Description = "MBAS - Modern Business Automation System"

' Set icon if provided
If iconPath <> "" Then
    objShortcut.IconLocation = iconPath
End If

objShortcut.Save

WScript.Echo "Shortcut created on desktop: " & shortcutName
