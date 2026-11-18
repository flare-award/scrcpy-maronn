# On macOS

## Install

### From the scrcpy-maronn release

Download and extract the archive for your computer:

 - Apple Silicon: look for `scrcpy-macos-aarch64-v5.0.3.tar.gz` in the
   [release assets](https://github.com/flare-award/scrcpy-maronn/releases/tag/v5.0.3).
   If no native archive is listed, [build this version from source](build.md).
 - [scrcpy-macos-x86_64-v5.0.3.tar.gz](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.0.3/scrcpy-macos-x86_64-v5.0.3.tar.gz) (Intel)<br>
   <sub>SHA-256: `6813d4e5c8fbd69220cd62029ea4bd60993b74ccb5fb81f7f23f7a685eba05b9`</sub>

[Release notes](https://github.com/flare-award/scrcpy-maronn/releases/tag/v5.0.3) · [SHA-256 checksums](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.0.3/SHA256SUMS.txt).


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
