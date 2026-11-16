#!/usr/bin/env bash
# Quick health check for every tool. Prints a checklist.
cd "$(dirname "$0")/.."
source tools/env.sh
T=$(mktemp -d); OUT=()
row(){ OUT+=("$1|$2|$3"); }

ffmpeg -v error -y -f lavfi -i testsrc=d=2:s=320x240 -f lavfi -i sine=d=2 -shortest "$T/a.mp4" 2>/dev/null \
  && row "FFmpeg" "OK" "$(ffmpeg -version | head -1 | cut -d' ' -f3)" || row "FFmpeg" "FAIL" "could not encode a test clip"

if yt-dlp --enable-file-urls -q -o "$T/dl.%(ext)s" "file://$T/a.mp4" 2>/dev/null; then
  if yt-dlp -q --simulate "https://www.youtube.com/watch?v=jNQXAC9IVRw" >/dev/null 2>&1; then row "yt-dlp" "OK" "$(yt-dlp --version), YouTube reachable"
  else row "yt-dlp" "PARTIAL" "$(yt-dlp --version) works; YouTube not reachable from this network"; fi
else row "yt-dlp" "FAIL" "not installed (run tools/setup.sh)"; fi

if whisper --help >/dev/null 2>&1; then
  if whisper "$T/a.mp4" --model tiny --model_dir "$WHISPER_MODEL_DIR" --output_dir "$T" --output_format srt >/dev/null 2>&1; then
    row "Whisper" "OK" "transcribed a test clip"
  else row "Whisper" "PARTIAL" "installed; model download blocked or failed"; fi
else row "Whisper" "FAIL" "not installed"; fi

(cd projects/_templates/remotion-starter && timeout 300 npx remotion render HelloWorld "$T/r.mp4" --frames=0-29 >/dev/null 2>&1) \
  && row "Remotion" "OK" "rendered test video ($(cd projects/_templates/remotion-starter && node -p 'require("remotion/package.json").version'))" \
  || row "Remotion" "FAIL" "test render failed"

(cd projects/_templates/hyperframes-starter && timeout 300 npx hyperframes render -o "$T/h.mp4" >/dev/null 2>&1) \
  && row "Hyperframes" "OK" "rendered test video ($(npx hyperframes --version))" || row "Hyperframes" "FAIL" "test render failed"

python3 tools/sfx.py search whoosh -n 1 >/dev/null 2>&1 && row "Openverse" "OK" "search works" \
  || row "Openverse" "BLOCKED" "api.openverse.org not reachable"
if python3 tools/sfx.py search whoosh -n 1 --source freesound >/dev/null 2>"$T/fs.err"; then row "Freesound" "OK" "search works"
elif grep -q FREESOUND_API_KEY "$T/fs.err"; then row "Freesound" "NEEDS KEY" "set FREESOUND_API_KEY"
else row "Freesound" "BLOCKED" "freesound.org not reachable"; fi

printf '\n%-12s %-10s %s\n' TOOL STATUS NOTES; printf '%.0s-' {1..70}; echo
for r in "${OUT[@]}"; do IFS='|' read -r a b c <<<"$r"
  case $b in OK) m="✅";; FAIL) m="❌";; *) m="⚠️ ";; esac
  printf '%s %-12s %-10s %s\n' "$m" "$a" "$b" "$c"; done
rm -rf "$T"
