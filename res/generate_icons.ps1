# Generate launcher icons for Android/iOS/desktop from res/icon.png.
# Also syncs the in-app icon at flutter/assets/icon.png.
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Src = Join-Path $Root "res\icon.png"
$Asset = Join-Path $Root "flutter\assets\icon.png"
$FlutterDir = Join-Path $Root "flutter"

if (-not (Test-Path $Src)) {
    Write-Error @"
Missing source icon: $Src
Add a 1024x1024 PNG (no rounded corners; Android adaptive icon adds the mask).
"@
}

Copy-Item -Path $Src -Destination $Asset -Force
Write-Host "Synced $Asset from $Src"

$Python = $null
if (Get-Command py -ErrorAction SilentlyContinue) { $Python = "py -3" }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $Python = "python" }
if ($Python) {
    pip install pillow --quiet
    Invoke-Expression "$Python `"$(Join-Path $Root 'res\generate_android_notification_icon.py')`""
} else {
    Write-Warning "Python not found; skipped notification icon generation."
}

Push-Location $FlutterDir
try {
    flutter pub get
    dart run flutter_launcher_icons
    if ($LASTEXITCODE -ne 0) {
        throw "dart run flutter_launcher_icons failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

Get-ChildItem -Path (Join-Path $Root "flutter\android\app\src\main\res\mipmap-*\ic_launcher_foreground.png") -ErrorAction SilentlyContinue |
    Remove-Item -Force

Write-Host "Launcher icons generated under flutter\android\app\src\main\res\drawable-* and mipmap-*"
