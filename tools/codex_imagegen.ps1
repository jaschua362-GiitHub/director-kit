<#
.SYNOPSIS
  Bridge: generate ONE image with Codex's built-in image generation (your ChatGPT subscription)
  and save it to an exact path inside your project folder (the parent of this tools\ folder).

.EXAMPLE
  .\codex_imagegen.ps1 -PromptFile ..\bible\lookdev-v01\prompts\LD-YAN-a02.txt `
      -Out bible\lookdev-v01\returns\LD-YAN-a02.png `
      -Refs bible\source-masters\C01-Ren-full-body-master.png, bible\lookdev-v01\returns\LD-YAN-a01.png
  Paths in -Out and -Refs are relative to the lab root.
#>
param(
  [Parameter(Mandatory)][string]$PromptFile,
  [Parameter(Mandatory)][string]$Out,
  [string[]]$Refs = @(),
  [string]$Aspect = "2:3"
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent   # project root = the folder that contains tools\

# Find codex.exe (the path changes when the Codex app updates)
$codex = (Get-Command codex -ErrorAction SilentlyContinue).Source
if (-not $codex) {
  $pkg = Get-AppxPackage -Name 'OpenAI.Codex' -ErrorAction SilentlyContinue | Sort-Object Version -Descending | Select-Object -First 1
  if ($pkg) { $codex = Join-Path $pkg.InstallLocation 'app\resources\codex.exe' }
}
if (-not $codex -or -not (Test-Path -LiteralPath $codex)) { throw 'codex.exe not found. Is the Codex app installed?' }

$promptPath = (Resolve-Path -LiteralPath $PromptFile).Path
$imagePrompt = Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8
$outFull = Join-Path $root $Out
if (Test-Path -LiteralPath $outFull) { throw "Refusing to overwrite existing file: $Out" }
if ($Refs.Count -gt 5) { throw "Codex image generation accepts at most 5 reference images; got $($Refs.Count)." }
$refArgs = @()
$refList = @()
$i = 1
foreach ($r in $Refs) {
  $full = Join-Path $root $r
  if (-not (Test-Path -LiteralPath $full)) { throw "Reference not found: $r" }
  $refArgs += @('-i', $full)
  $refList += "Image $i = $r"
  $i++
}

$task = @"
You are an image-generation operator for this film project. Do exactly this and nothing else:
1. Use your built-in image generation tool to generate EXACTLY ONE image from the IMAGE PROMPT below, in aspect ratio $Aspect, using the attached images as references, in this order:
$($refList -join "`n")
2. Save the generated PNG to this exact path: $Out  (relative to the current folder). Do not overwrite any existing file.
3. Do not create, edit, move or delete any other file. Do not run other tasks.
4. Final reply: only the saved path, then one line describing the image.

IMAGE PROMPT:
$imagePrompt
"@

$log = [System.IO.Path]::ChangeExtension($outFull, '.codex.log')
$last = [System.IO.Path]::ChangeExtension($outFull, '.codex.reply.txt')
# Prompt goes via stdin: -i is variadic and would swallow a positional prompt.
# Native stderr must not trip $ErrorActionPreference=Stop in Windows PowerShell 5.1.
$ErrorActionPreference = 'Continue'
# Lean run (token discipline): no project instruction files, low reasoning, no saved session.
$lean = @('--ephemeral', '-c', 'project_doc_max_bytes=0', '-c', 'model_reasoning_effort="low"')
$task | & $codex exec -C $root -s workspace-write --skip-git-repo-check @lean -o $last @refArgs 2>&1 | Out-File -LiteralPath $log -Encoding utf8
$code = $LASTEXITCODE
$ErrorActionPreference = 'Stop'

$receipt = [ordered]@{
  date = (Get-Date).ToString('o'); route = 'codex exec + built-in image_generation (ChatGPT subscription)'
  codex = $codex; prompt_file = $promptPath; output = $Out; aspect = $Aspect; references = $Refs; exit_code = $code
  output_exists = (Test-Path -LiteralPath $outFull)
  output_sha256 = $(if (Test-Path -LiteralPath $outFull) { (Get-FileHash -LiteralPath $outFull -Algorithm SHA256).Hash.ToLower() } else { $null })
}
$receipt | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath ([System.IO.Path]::ChangeExtension($outFull, '.json')) -Encoding utf8
$receipt | ConvertTo-Json -Depth 4
