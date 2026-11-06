# Source this from the project root before running any editing tool: source tools/env.sh
# Paths are worked out from this file's location, so the project folder can live anywhere.
if [ -n "$ZSH_VERSION" ]; then _ENV_SRC="${(%):-%x}"; else _ENV_SRC="${BASH_SOURCE[0]}"; fi
TOOLS="$(cd "$(dirname "$_ENV_SRC")" && pwd)"
PROJECT_ROOT="$(dirname "$TOOLS")"
export TOOLS PROJECT_ROOT
export PATH="$TOOLS/bin:$TOOLS/venv/bin:$TOOLS/realesrgan:$HOME/.local/bin:$PATH"
unset _ENV_SRC
