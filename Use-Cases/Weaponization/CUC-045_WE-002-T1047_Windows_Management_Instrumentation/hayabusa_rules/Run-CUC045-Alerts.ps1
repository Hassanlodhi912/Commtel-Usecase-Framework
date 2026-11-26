# CUC-045 - WMI detections without a SIEM (Hayabusa + Commtel Sigma rules)
# Run in an elevated PowerShell on the lab Windows VM, from the folder that holds hayabusa-*.exe
# Usage:  .\Run-CUC045-Alerts.ps1            (scan last 2 hours of local logs)
#         .\Run-CUC045-Alerts.ps1 -Hours 24

param([int]$Hours = 2)

$ErrorActionPreference = 'Stop'
$here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$exe    = Get-ChildItem -Path $here -Filter 'hayabusa-*.exe' | Select-Object -First 1
if (-not $exe) { throw "hayabusa-*.exe not found in $here" }

$rules  = Join-Path $here 'rules\cuc045'
$outDir = 'C:\ART\CUC-045\alerts'
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$stamp  = Get-Date -Format 'yyyyMMdd_HHmm'
$csv    = Join-Path $outDir "CUC-045_alerts_$stamp.csv"
$html   = Join-Path $outDir "CUC-045_alerts_$stamp.html"

Push-Location $here
& $exe.FullName dfir-timeline -l -r $rules -c (Join-Path $here 'rules\config') -w -A -a -U -C `
    --time-offset "$($Hours)h" -o $csv -H $html
Pop-Location

Write-Host ""
Write-Host "==================== CUC-045 ALERTS ====================" -ForegroundColor Cyan
Import-Csv $csv | Sort-Object Timestamp |
    Format-Table Timestamp, Level, RuleTitle, Computer, EventID -AutoSize
Write-Host "CSV : $csv"
Write-Host "HTML: $html"
Start-Process $html
