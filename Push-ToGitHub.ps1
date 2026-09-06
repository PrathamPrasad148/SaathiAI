# Push-ToGitHub.ps1 - Saathi AI GitHub Publisher
# Author: Pratham Prasad

param(
    [string]$CommitMessage = ""
)

$ErrorActionPreference = "Continue"
$RemoteUrl = "https://github.com/PrathamPrasad148/SaathiAI.git"

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "       Saathi AI - GitHub Publisher (Pratham Prasad)   " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    $nowStr = Get-Date -Format "dd-MM-yyyy HH:mm:ss"
    $CommitMessage = "Update Saathi AI by Pratham Prasad [$nowStr]"
}

Write-Host "Remote: $RemoteUrl" -ForegroundColor Gray
Write-Host "Commit: $CommitMessage" -ForegroundColor Gray
Write-Host ""

# 1. Clean stale locks
Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
Remove-Item ".git\HEAD.lock" -Force -ErrorAction SilentlyContinue
Remove-Item ".git\refs\heads\main.lock" -Force -ErrorAction SilentlyContinue

# 2. Repair 0-byte or broken index
if (Test-Path ".git\index") {
    $indexFile = Get-Item ".git\index" -ErrorAction SilentlyContinue
    if ($indexFile.Length -eq 0) {
        Write-Host "[WARN] 0-byte corrupted Git index detected. Rebuilding..." -ForegroundColor Yellow
        Remove-Item ".git\index" -Force -ErrorAction SilentlyContinue
        git reset HEAD *>$null
    }
}

git status *>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARN] Corrupted index detected. Reconstructing..." -ForegroundColor Yellow
    Remove-Item ".git\index" -Force -ErrorAction SilentlyContinue
    git reset HEAD *>$null
}

# 3. Configure author credentials
git config user.name "Pratham Prasad"
git config user.email "prathamprasad148@users.noreply.github.com"
git branch -M main *>$null

# 4. Stage
Write-Host "[INFO] Staging all files across the repository..." -ForegroundColor Cyan
git add -A

# 5. Check if changes exist
$status = git status --porcelain
if ($status) {
    Write-Host "[INFO] Creating commit: $CommitMessage" -ForegroundColor Green
    git commit -m "$CommitMessage"
} else {
    Write-Host "[INFO] Working tree is clean. Nothing to commit locally." -ForegroundColor Yellow
}

# 6. Push
Write-Host "[INFO] Pushing everything to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "[INFO] Remote branch has new commits. Pulling with auto-sync..." -ForegroundColor Yellow
    git pull origin main --rebase --autostash
    if ($LASTEXITCODE -ne 0) {
        git rebase --abort *>$null
        git pull origin main --no-rebase -X ours --no-edit
    }
    Write-Host "[INFO] Retrying push to GitHub..." -ForegroundColor Cyan
    git push -u origin main
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host "[SUCCESS] Saathi AI successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Author: Pratham Prasad" -ForegroundColor Green
    Write-Host "URL: $RemoteUrl" -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "========================================================" -ForegroundColor Red
    Write-Host "[FAILED] Push could not complete. Check your internet connection." -ForegroundColor Red
    Write-Host "========================================================" -ForegroundColor Red
    exit 1
}
