#!/bin/zsh
# 启动 LOVER 悬浮窗（不装 LaunchAgent，按需手动启动）
cd "$(dirname "$0")" || exit 1
export USE_TF=0
# Corporate proxies may install a macOS-trusted root certificate that is not in uv's
# bundled trust store. Use the system keychain for dependency downloads.
export UV_SYSTEM_CERTS=1
# First launch downloads PyTorch/Transformers wheels.  Give slower corporate networks
# enough time; uv reuses successfully downloaded artifacts on the next run.
export UV_HTTP_TIMEOUT=300
export UV_HTTP_RETRIES=5
# uv installs to ~/.local/bin; a Finder-launched .command does not inherit a login shell
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
# same user-level env the .app launcher uses (API keys live outside the repo)
source ./packaging/bootstrap_uv.sh || exit 1
jev_load_env "$HOME/.config/lover/env"

LOG="$HOME/Library/Logs/lover.log"
mkdir -p "$(dirname "$LOG")" || exit 1
if ! jev_check_arch; then
    print -r -- "$JEV_ARCH_ERROR"
    print -r -- "详情：$LOG"
    exit 1
fi
if ! command -v uv >/dev/null 2>&1; then
    print "未找到 uv，正在自动安装；进度日志：$LOG"
fi
if ! jev_ensure_uv "$LOG"; then
    print -r -- "$JEV_UV_ERROR"
    print -r -- "详情：$LOG。也可手动运行 brew install uv 后重试。"
    exit 1
fi

exec uv run python src/hud.py
