<#
SeedVR2 3B (GGUF Q8_0) local video upscaler, for shots WITHOUT readable faces (or faces that pass a 100 % crop).
Real-ESRGAN (tools/upres_shot.py) is the quick option where detail will not read (fast motion, deep dark, tiny in frame).
Readable faces under about 60 px in the final frame are never upscaled: native 1080p or a new take (see the guides).

usage: ./tools/seedvr2.ps1 -In <clip.mp4> -Out <out.mkv> [-Short 1080] [-Skip 0] [-Frames 0]
  -Short         target short-side px (720x1280 -> 1080 gives 1080x1920). On a 10 GB card plan 1620 at most; 2160 failed.
  -Skip/-Frames  optional frame range (skip first N, load N frames; 0 = all)

Setup (see SETUP.md):
  SEEDVR2_DIR  folder holding  upstream\inference_cli.py  (numz/ComfyUI-SeedVR2_VideoUpscaler standalone CLI),
               models\  (seedvr2_ema_3b-Q8_0.gguf + ema_vae_fp16.safetensors)  and  .venv\  (Python 3.12, torch with CUDA)
  DCL_FFMPEG   full path to an ffmpeg that runs; otherwise ffmpeg on PATH is used

Close other GPU apps first (browsers, ChatCut, Codex): the card is shared, and a busy card means OOM or very slow runs.
Run time on an RTX 3080: about 5-8 min per 48 frames at 1080; about 17 min per 5 s clip at 1620.
Output is lossless FFV1 MKV (PNG frames, then ffmpeg).
#>
param([Parameter(Mandatory)][string]$In,[Parameter(Mandatory)][string]$Out,[int]$Short=1080,[int]$Skip=0,[int]$Frames=0,
      [string]$Model='seedvr2_ema_3b-Q8_0.gguf',[int]$MaxUsedMiB=3500,[switch]$Force)
$ErrorActionPreference='Stop'
$S=$env:SEEDVR2_DIR
if(-not $S -or -not (Test-Path "$S\upstream\inference_cli.py")){ throw 'Set SEEDVR2_DIR to the SeedVR2 folder (upstream\, models\, .venv\). See SETUP.md section 2b.' }
$ff=if($env:DCL_FFMPEG){$env:DCL_FFMPEG}else{'ffmpeg'}
# Preflight: refuse while other apps hold VRAM (6-7 GB held -> OOM or 32 min runs).
$used=[int](nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | Select-Object -First 1)
if($used -gt $MaxUsedMiB -and -not $Force){
  Write-Warning "GPU has $used MiB in use (limit $MaxUsedMiB). Close browsers, ChatCut, Codex/ChatGPT and other GPU apps, then re-run. -Force overrides."
  exit 2 }
"GPU preflight ok: $used MiB in use"
$env:PYTHONUTF8='1'
$tmp=Join-Path $env:TEMP ("seedvr2_"+[guid]::NewGuid().ToString('N')); New-Item -ItemType Directory $tmp | Out-Null
$inAbs=(Resolve-Path $In).Path
$a=@("$S\upstream\inference_cli.py",$inAbs,'--output',$tmp,'--output_format','png','--model_dir',"$S\models",'--dit_model',$Model,
 '--resolution',$Short,'--batch_size',5,'--temporal_overlap',1,'--blocks_to_swap',32,'--swap_io_components',
 '--dit_offload_device','cpu','--vae_offload_device','cpu','--vae_encode_tiled','--vae_decode_tiled',
 '--vae_encode_tile_size',384,'--vae_decode_tile_size',256,'--vae_encode_tile_overlap',48,'--vae_decode_tile_overlap',32,'--seed',42,
 '--skip_first_frames',$Skip,'--load_cap',$Frames)
$log=Join-Path $tmp 'seedvr2.log'
$ErrorActionPreference="Continue"; & "$S\.venv\Scripts\python.exe" @a 2>&1 | Tee-Object -FilePath $log | Out-Host; $ErrorActionPreference="Stop"
if($LASTEXITCODE){throw "SeedVR2 failed ($LASTEXITCODE); log: $log"}
$d=Get-ChildItem $tmp -Directory | Select-Object -First 1
if(-not $d){throw "SeedVR2 wrote no frames; log: $log"}
$first=(Get-ChildItem $d.FullName -Filter *_000000.png).Name -replace '_000000\.png$',''
$fps=24
& $ff -v error -y -framerate $fps -i "$($d.FullName)\${first}_%06d.png" -c:v ffv1 $Out; if($LASTEXITCODE){throw 'encode failed'}
Remove-Item $tmp -Recurse -Force; "ok $Out"
