#!/usr/bin/env bash
set -e

BUILDDIR=build-auto
VERSION=v5.1.0
RELEASE_URL="https://github.com/flare-award/scrcpy-maronn/releases/download/$VERSION"
SERVER="scrcpy-server-$VERSION"
PREBUILT_SERVER_SHA256=69fb269d901ac9c53d5d5c751f2b398fea1bae0c014b49d4b39b716a0b2bf24a

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

echo "[scrcpy] Downloading prebuilt server..."
wget "$RELEASE_URL/$SERVER" -O "$tmpdir/$SERVER"
echo "[scrcpy] Verifying prebuilt server..."
printf '%s  %s\n' "$PREBUILT_SERVER_SHA256" "$tmpdir/$SERVER" | sha256sum --check --strict
mv "$tmpdir/$SERVER" scrcpy-server

echo "[scrcpy] Building client..."
rm -rf "$BUILDDIR"
meson setup "$BUILDDIR" --buildtype=release --strip -Db_lto=true \
    -Dprebuilt_server=scrcpy-server
cd "$BUILDDIR"
ninja

echo "[scrcpy] Installing (sudo)..."
sudo ninja install
