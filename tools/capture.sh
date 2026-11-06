#!/bin/zsh
# Capture a public page as a sharp PNG for b-roll, using Chrome with a clean profile.
# Usage: capture.sh <output.png> <url> [width,height]
# Tweets: use https://platform.twitter.com/embed/Tweet.html?id=<tweet id> with size 540,400
set -e
OUT="$1"; URL="$2"; SIZE="${3:-540,960}"
PROFILE="$(mktemp -d)"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
	--user-data-dir="$PROFILE" --window-size="$SIZE" --force-device-scale-factor=2 \
	--virtual-time-budget=12000 --screenshot="$OUT" "$URL" 2>/dev/null
rm -rf "$PROFILE"
echo "$OUT"
