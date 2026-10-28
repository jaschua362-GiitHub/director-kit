<#
.SYNOPSIS  Route B: run a pack's JOBS.json (paths relative to the lab root) through the Codex image bridge. Skips jobs whose output exists.
.EXAMPLE   .\tools\run_jobs.ps1 -Pack "bible\pack-a" [-Only PA-YAN-01,PA-TAOTIE-01] [-DryRun]
#>
param([Parameter(Mandatory)][string]$Pack, [string[]]$Only = @(), [switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$packFull = Join-Path $root $Pack
$jobs = Get-Content -LiteralPath (Join-Path $packFull 'JOBS.json') -Raw -Encoding utf8 | ConvertFrom-Json
if ($jobs.PSObject.Properties.Name -contains "jobs") { $jobs = $jobs.jobs }
foreach ($j in $jobs) {
  if ($Only.Count -and ($Only -notcontains $j.id)) { continue }
  $outRel = Join-Path $Pack $j.out
  if (Test-Path -LiteralPath (Join-Path $root $outRel)) { Write-Output "skip $($j.id): already exists"; continue }
  $promptFull = Join-Path $packFull $j.prompt
  if ($DryRun) { Write-Output "would run $($j.id) -> $outRel ($($j.aspect), $(@($j.refs).Count) refs)"; continue }
  Write-Output "running $($j.id) ..."
  & (Join-Path $PSScriptRoot 'codex_imagegen.ps1') -PromptFile $promptFull -Out $outRel -Refs @($j.refs) -Aspect $j.aspect
}
