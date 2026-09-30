# PowerShell script for local automated daily commit
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logEntry = "Local activity on $timestamp"

Add-Content -Path "activity.log" -Value $logEntry
Write-Host "Appended log: $logEntry"

git add activity.log
git commit -m "chore(activity): local update $timestamp"
git push origin main

Write-Host "Committed and pushed successfully!"
