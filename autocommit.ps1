# PowerShell script for local automated daily commit (70-75 commits)
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Running daily commit generator (70-75 random commits)..."
python generate_commits.py --min 70 --max 75

Write-Host "Pushing commits to GitHub..."
git push origin main

Write-Host "All commits pushed successfully!"
