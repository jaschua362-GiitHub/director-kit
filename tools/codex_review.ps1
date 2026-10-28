<#
.SYNOPSIS  Bridge: run a text-only Codex review task (no images) in lean mode, writing one review file.
.EXAMPLE   .\tools\codex_review.ps1 -PromptFile tools\prompts\R4.txt -Out reviews\REVIEW_R4_codex.md
#>
param([Parameter(Mandatory)][string]$PromptFile, [Parameter(Mandatory)][string]$Out)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$codex = (Get-Command codex -ErrorAction SilentlyContinue).Source
if (-not $codex) {
  $pkg = Get-AppxPackage -Name 'OpenAI.Codex' -ErrorAction SilentlyContinue | Sort-Object Version -Descending | Select-Object -First 1
  if ($pkg) { $codex = Join-Path $pkg.InstallLocation 'app\resources\codex.exe' }
}
if (-not $codex -or -not (Test-Path -LiteralPath $codex)) { throw 'codex.exe not found.' }
$outFull = Join-Path $root $Out
if (Test-Path -LiteralPath $outFull) { throw "Refusing to overwrite existing file: $Out" }
$task = (Get-Content -LiteralPath (Resolve-Path -LiteralPath $PromptFile) -Raw) + "`n`nWrite your review ONLY to: $Out (relative to the current folder). Do not create, edit, move or delete any other file. Final reply: the verdict line only."
$log = [System.IO.Path]::ChangeExtension($outFull, '.codex.log')
$ErrorActionPreference = 'Continue'
$lean = @('--ephemeral', '-c', 'project_doc_max_bytes=0', '-c', 'model_reasoning_effort="medium"')
$task | & $codex exec -C $root -s workspace-write --skip-git-repo-check @lean 2>&1 | Out-File -LiteralPath $log -Encoding utf8
$code = $LASTEXITCODE
[ordered]@{ exit_code = $code; output_exists = (Test-Path -LiteralPath $outFull); log = $log } | ConvertTo-Json
