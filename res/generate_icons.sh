#!/usr/bin/env bash
# Generate launcher icons for Android/iOS/desktop from res/icon.png.
# Also syncs the in-app icon at flutter/assets/icon.png.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/res/icon.png"
ASSET="$ROOT/flutter/assets/icon.png"

if [[ ! -f "$SRC" ]]; then
  echo "Missing source icon: $SRC" >&2
  echo "Add a 1024x1024 PNG (no rounded corners; Android adaptive icon adds the mask)." >&2
  exit 1
fi

cp "$SRC" "$ASSET"
echo "Synced $ASSET from $SRC"

pip install pillow --quiet
python3 "$ROOT/res/generate_android_notification_icon.py"

pushd "$ROOT/flutter" >/dev/null
flutter pub get
dart run flutter_launcher_icons
popd >/dev/null

rm -f "$ROOT/flutter/android/app/src/main/res/mipmap-"*/ic_launcher_foreground.png

echo "Launcher icons generated under flutter/android/app/src/main/res/drawable-* and mipmap-*"
