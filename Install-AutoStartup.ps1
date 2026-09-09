# PowerShell Script: Install Saathi AI Continuous Self-Training into Windows Startup (Foreground Mode)

$startupDir = [Environment]::GetFolderPath('Startup')
$targetBat = "C:\SAATHIAI\Start-Continuous-Advancement.bat"
$shortcutPath = Join-Path -Path $startupDir -ChildPath "SaathiContinuousAdvancement.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c start `"Saathi AI Live Self-Advancement`" `"$targetBat`""
$Shortcut.WorkingDirectory = "C:\SAATHIAI"
$Shortcut.Description = "Saathi AI Continuous Self-Advancement Interactive Console"
$Shortcut.Save()

Write-Host "[SUCCESS] Installed Saathi AI Live Self-Advancement into Windows Startup folder:" -ForegroundColor Green
Write-Host " -> $shortcutPath" -ForegroundColor Cyan


