#!/usr/bin/env bash
set -e

BUILDDIR=build-auto
VERSION=v5.1.0
RELEASE_URL="https://github.com/flare-award/scrcpy-maronn/releases/download/$VERSION"
SERVER="scrcpy-server-$VERSION"
PREBUILT_SERVER_SHA256=6e429868d5a2ac3743b7ea5c0d82a3bd4f35098f9d79de3f7eadd69a8504d0b5

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
