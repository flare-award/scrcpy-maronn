#!/usr/bin/env bash
set -e

BUILDDIR=build-auto
VERSION=v5.0.3
RELEASE_URL="https://github.com/flare-award/scrcpy-maronn/releases/download/$VERSION"
SERVER="scrcpy-server-$VERSION"
PREBUILT_SERVER_SHA256=4d91f2b5ff27f5c14f83d70365792a77d93d95e1c0bc3857c97b4aefac3a0c36

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
