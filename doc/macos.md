# On macOS

## Install

### From the scrcpy-maronn release

Download and extract the archive for your computer:

 - [scrcpy-macos-aarch64-v5.1.0.tar.gz](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/scrcpy-macos-aarch64-v5.1.0.tar.gz) (Apple Silicon)<br>
   <sub>SHA-256: `0189afec395c0fffa9d7b70d204b9c3c5d0fcbc120d3f259febd398d449aea96`</sub>
 - [scrcpy-macos-x86_64-v5.1.0.tar.gz](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/scrcpy-macos-x86_64-v5.1.0.tar.gz) (Intel)<br>
   <sub>SHA-256: `28b140a872fadf148cae027e5c398aba641499e152c2e2b4ccf2d5c693248cf8`</sub>

[Release notes](https://github.com/flare-award/scrcpy-maronn/releases/tag/v5.1.0) · [SHA-256 checksums](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/SHA256SUMS.txt).


### From a package manager (upstream scrcpy, not this fork)

Scrcpy is available in [Homebrew]:

```bash
brew install scrcpy
```

[Homebrew]: https://brew.sh/

You need `adb`, accessible from your `PATH`. If you don't have it yet:

```bash
brew install --cask android-platform-tools
```

Alternatively, Scrcpy is also available in [MacPorts], which sets up `adb` for you:

```bash
sudo port install scrcpy
```

[MacPorts]: https://www.macports.org/

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
