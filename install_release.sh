#!/usr/bin/env bash
set -e

BUILDDIR=build-auto
VERSION=v5.0.2
RELEASE_URL="https://github.com/flare-award/scrcpy-maronn/releases/download/$VERSION"
SERVER="scrcpy-server-$VERSION"

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

echo "[scrcpy] Downloading prebuilt server..."
wget "$RELEASE_URL/$SERVER" -O "$tmpdir/$SERVER"
wget "$RELEASE_URL/SHA256SUMS.txt" -O "$tmpdir/SHA256SUMS.txt"
echo "[scrcpy] Verifying prebuilt server..."
(
    cd "$tmpdir"
    # Check only the server from this release, not any other manifest paths.
    awk -v server="$SERVER" '$2 == server {print $1 "  " server}' SHA256SUMS.txt | sha256sum --check --strict
)
mv "$tmpdir/$SERVER" scrcpy-server

echo "[scrcpy] Building client..."
rm -rf "$BUILDDIR"
meson setup "$BUILDDIR" --buildtype=release --strip -Db_lto=true \
    -Dprebuilt_server=scrcpy-server
cd "$BUILDDIR"
ninja

echo "[scrcpy] Installing (sudo)..."
sudo ninja install
