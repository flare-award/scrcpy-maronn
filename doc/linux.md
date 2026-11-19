# On Linux

## Install

### From the scrcpy-maronn release

Download and extract the archive for your computer:

 - [scrcpy-linux-x86_64-v5.1.0.tar.gz](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/scrcpy-linux-x86_64-v5.1.0.tar.gz) (x86_64)

[Release notes](https://github.com/flare-award/scrcpy-maronn/releases/tag/v5.1.0) · [SHA-256 checksums](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/SHA256SUMS.txt).


### From your package manager (upstream scrcpy, not this fork)

<a href="https://repology.org/project/scrcpy/versions"><img src="https://repology.org/badge/vertical-allrepos/scrcpy.svg" alt="Packaging status" align="right"></a>

Scrcpy is packaged in several distributions and package managers:

 - Debian/Ubuntu: ~~`apt install scrcpy`~~ _(obsolete version)_
 - Arch Linux: `pacman -S scrcpy`
 - Fedora: `dnf copr enable zeno/scrcpy && dnf install scrcpy`
 - Gentoo: `emerge scrcpy`
 - Snap: ~~`snap install scrcpy`~~ _(obsolete version)_
 - … (see [repology](https://repology.org/project/scrcpy/versions))


### From an install script

To install this release from source, follow this simplified process.

First, you need to install the required packages:

```bash
# for Debian/Ubuntu
sudo apt install ffmpeg libsdl3-0 libusb-1.0-0 adb wget va-driver-all \
                 gcc git pkg-config meson ninja-build libsdl3-dev \
                 libavcodec-dev libavdevice-dev libavformat-dev libavutil-dev \
                 libswresample-dev libusb-1.0-0-dev libv4l-dev libdrm-dev
```

Then clone the repo and execute the installation script
([source](/install_release.sh)):

```bash
git clone --branch v5.1.0 https://github.com/flare-award/scrcpy-maronn
cd scrcpy-maronn
./install_release.sh
```

When a new release is out, select its tag and reinstall:

```bash
git fetch --tags
git checkout v5.1.0  # replace with the new version tag
./install_release.sh
```

To uninstall:

```bash
sudo ninja -Cbuild-auto uninstall
```

_Note that this simplified process only works for released versions (it
downloads a prebuilt server binary), so for example you can't use it for testing
the development branch (`dev`)._

_See [build.md](build.md) to build and install the app manually._


## Run

_Make sure that your device meets the [prerequisites](/README.md#prerequisites)._

Once installed, run from a terminal:

```bash
scrcpy
```

or with arguments (here to disable audio and record to `file.mkv`):

```bash
scrcpy --no-audio --record=file.mkv
```

Documentation for command line arguments is available:
 - `man scrcpy`
 - `scrcpy --help`
 - on [github](/README.md)
