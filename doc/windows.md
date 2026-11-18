# On Windows

## Install

### From the scrcpy-maronn release

Download and extract the archive for your computer:

 - [scrcpy-win64-v5.0.3.zip](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.0.3/scrcpy-win64-v5.0.3.zip) (64-bit)<br>
   <sub>SHA-256: `8ed9c567c4c8f2fbaf1a8a6f517f160cacd78f50f9c8875fa8ef6d2e75840784`</sub>
 - [scrcpy-win32-v5.0.3.zip](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.0.3/scrcpy-win32-v5.0.3.zip) (32-bit)<br>
   <sub>SHA-256: `3479e62f33c59ecb523ae9f31407a88b55bca0f86945214c990292ad44d1f939`</sub>
 - [scrcpy-winarm64-v5.0.3.zip](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.0.3/scrcpy-winarm64-v5.0.3.zip) (ARM 64-bit)<br>
   <sub>SHA-256: `d7ae01de6c7fc1a1ec6c0f9fef9efe702b7a01a3c5a43492fd3e3d66856cd9c2`</sub>

[Release notes](https://github.com/flare-award/scrcpy-maronn/releases/tag/v5.0.3) · [SHA-256 checksums](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.0.3/SHA256SUMS.txt).


### From a package manager (upstream scrcpy, not this fork)

From [WinGet] (ADB and other dependencies will be installed alongside scrcpy):

```bash
winget install --exact Genymobile.scrcpy
```

From [Chocolatey]:

```bash
choco install scrcpy
choco install adb    # if you don't have it yet
```

From [Scoop]:

```bash
scoop install scrcpy
scoop install adb    # if you don't have it yet
```

[WinGet]: https://github.com/microsoft/winget-cli
[Chocolatey]: https://chocolatey.org/
[Scoop]: https://scoop.sh

_See [build.md](build.md) to build and install the app manually._


## Run

_Make sure that your device meets the [prerequisites](/README.md#prerequisites)._

Scrcpy is a command line application: it is mainly intended to be executed from
a terminal with command line arguments.

To open a terminal at the expected location, double-click on
`open_a_terminal_here.bat` in your scrcpy directory, then type your command. For
example, without arguments:

```bash
scrcpy
```

or with arguments (here to disable audio and record to `file.mkv`):

```bash
scrcpy --no-audio --record=file.mkv
```

Documentation for command line arguments is available:
 - `scrcpy --help`
 - on [github](/README.md)

If you plan to always use the same arguments, create a file `myscrcpy.bat`
(enable [show file extensions] to avoid confusion) containing your command, For
example:

```bash
scrcpy --prefer-text --turn-screen-off --stay-awake
```

Add `--pause-on-exit=if-error` if you want the console to remain open when
scrcpy fails:

```bash
scrcpy --prefer-text --turn-screen-off --stay-awake --pause-on-exit=if-error
```

[show file extensions]: https://www.howtogeek.com/205086/beginner-how-to-make-windows-show-file-extensions/

Then just double-click on that file to run it.

To start scrcpy without opening a terminal, double-click `scrcpy-noconsole.vbs`
(note that errors won't be shown). To pass arguments, edit (a copy of)
`scrcpy-noconsole.vbs` and add the desired arguments.
