#!/usr/bin/env bash
# Install everything the workspace needs. Safe to re-run: skips what is already installed.
set -euo pipefail
cd "$(dirname "$0")/.."
say(){ printf '\n==> %s\n' "$*"; }

say "FFmpeg"
if command -v ffmpeg >/dev/null; then ffmpeg -version | head -1
elif command -v brew >/dev/null; then brew install ffmpeg
elif command -v apt-get >/dev/null; then sudo apt-get update && sudo apt-get install -y ffmpeg
else echo "Install FFmpeg from https://ffmpeg.org/download.html"; exit 1; fi

say "Node.js (needed for Remotion + Hyperframes, >= 22)"
command -v node >/dev/null || { echo "Install Node.js 22+ from https://nodejs.org"; exit 1; }
node -v

say "Python tools: yt-dlp + Whisper (into .venv)"
if [ ! -x .venv/bin/python ]; then
  if command -v uv >/dev/null; then uv venv .venv --python 3.12; else python3 -m venv .venv; fi
fi
if ! .venv/bin/python -c "import whisper, yt_dlp" 2>/dev/null; then
  if command -v uv >/dev/null; then uv pip install --python .venv/bin/python -U "yt-dlp[default]" openai-whisper
  else .venv/bin/python -m pip install -U "yt-dlp[default]" openai-whisper; fi
fi
.venv/bin/yt-dlp --version

say "Hyperframes CLI"
[ -x node_modules/.bin/hyperframes ] || npm install
npx hyperframes --version

say "Remotion starter project"
(cd projects/_templates/remotion-starter && { [ -d node_modules ] || npm install; } && npx remotion versions | tail -1)

say "Done. Run: bash tools/check.sh"
