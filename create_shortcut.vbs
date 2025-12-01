Set oWS = WScript.CreateObject("WScript.Shell")
strDesktop = oWS.SpecialFolders("Desktop")
Set oLink = oWS.CreateShortcut(strDesktop & "\Voice Cloner Pro.lnk")
oLink.TargetPath = "d:\Dev Projects 2025\Voice Cloner\VoiceCloner.bat"
oLink.WorkingDirectory = "d:\Dev Projects 2025\Voice Cloner"
oLink.Description = "Voice Cloning Desktop Application"
oLink.Save
WScript.Echo "Shortcut created successfully"
