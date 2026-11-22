#!/usr/bin/env bash
# 9:16 encode: same as encode.sh (reuses the normalised mix from the 16:9 run if present)
set -euo pipefail
FR=$1; NAME=$2; WAV=${WAV:-audio/crenature_v8_sfx.wav}; mkdir -p out
J=$(ffmpeg -hide_banner -nostats -i $WAV -af loudnorm=I=-14:TP=-2.6:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i $WAV -af "loudnorm=I=-14:TP=-2.6:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s24le audio/mix_norm_v.wav
V="-c:v libx264 -preset slow -crf 10 -tune grain -x264-params aq-mode=3 -pix_fmt yuv420p -movflags +faststart"
ffmpeg -hide_banner -loglevel error -y -framerate 60 -i $FR/f%05d.png -i audio/mix_norm_v.wav $V -c:a aac -b:a 256k -shortest out/${NAME}_1080x1920_60fps_sound.mp4
ffmpeg -hide_banner -loglevel error -y -framerate 60 -i $FR/f%05d.png -i audio/mix_norm_v.wav -vf fps=30 $V -c:a aac -b:a 256k -shortest out/${NAME}_1080x1920_30fps_sound.mp4
ls -la out/ | grep $NAME
