#!/usr/bin/env bash
# Replace the sound in finished MP4s without re-rendering the picture (video stream copied).
#   WAV=audio/crenature_v9_sfx.wav bash build/remux_sound.sh out/A.mp4 out/B.mp4 ...
set -euo pipefail
WAV=${WAV:-audio/crenature_v9_sfx.wav}
J=$(ffmpeg -hide_banner -nostats -i $WAV -af loudnorm=I=-14:TP=-2.6:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i $WAV -af "loudnorm=I=-14:TP=-2.6:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s24le audio/mix_norm_remux.wav
for f in "$@"; do
  ffmpeg -hide_banner -loglevel error -y -i "$f" -i audio/mix_norm_remux.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest "${f%.mp4}.tmp.mp4"
  mv "${f%.mp4}.tmp.mp4" "$f"; echo "remuxed $f"
done
