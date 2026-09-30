# PowerShell script for local automated daily commit (15-20 commits)
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Running daily commit generator (15-20 random commits)..."
python generate_commits.py --min 15 --max 20

Write-Host "Pushing commits to GitHub..."
git push origin main

Write-Host "All commits pushed successfully!"
