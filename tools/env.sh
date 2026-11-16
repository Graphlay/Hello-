# Source this to use the workspace tools:  source tools/env.sh
_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
export PATH="$_ROOT/tools/bin:$_ROOT/.venv/bin:$_ROOT/node_modules/.bin:$PATH"
export WHISPER_MODEL_DIR="$_ROOT/.whisper-models"   # whisper ... --model_dir "$WHISPER_MODEL_DIR"
unset _ROOT
