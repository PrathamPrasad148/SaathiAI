# PowerShell Script: Install Saathi AI Continuous Self-Training into Windows Startup

$startupDir = [Environment]::GetFolderPath('Startup')
$targetVbs = "C:\SAATHIAI\Start-Continuous-Advancement-Silent.vbs"
$shortcutPath = Join-Path -Path $startupDir -ChildPath "SaathiContinuousAdvancement.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"$targetVbs`""
$Shortcut.WorkingDirectory = "C:\SAATHIAI"
$Shortcut.Description = "Saathi AI Continuous Self-Advancement Daemon"
$Shortcut.Save()

Write-Host "[SUCCESS] Installed Saathi AI Continuous Self-Advancement into Windows Startup folder:" -ForegroundColor Green
Write-Host " -> $shortcutPath" -ForegroundColor Cyan

