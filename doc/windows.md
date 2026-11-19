# On Windows

## Install

### From the scrcpy-maronn release

Download and extract the archive for your computer:

 - [scrcpy-win64-v5.1.0.zip](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/scrcpy-win64-v5.1.0.zip) (64-bit)<br>
   <sub>SHA-256: `999278614b486d3b17b7324cde3b7d676d92dd8d2d3553e825306fecd996b7f6`</sub>
 - [scrcpy-win32-v5.1.0.zip](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/scrcpy-win32-v5.1.0.zip) (32-bit)<br>
   <sub>SHA-256: `c8799078bbc2764d0479b377b303c601ba008c12e15964633ac5866388d8ff70`</sub>
 - [scrcpy-winarm64-v5.1.0.zip](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/scrcpy-winarm64-v5.1.0.zip) (ARM 64-bit)<br>
   <sub>SHA-256: `35d28407e1c38b872d23a315e0999610dd0041d12172384f46e644d3de947b7e`</sub>

[Release notes](https://github.com/flare-award/scrcpy-maronn/releases/tag/v5.1.0) · [SHA-256 checksums](https://github.com/flare-award/scrcpy-maronn/releases/download/v5.1.0/SHA256SUMS.txt).


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

For a quick performance preset, open `scrcpy-fps.bat` in the extracted folder.
Choose **3** for 90 fps at up to 1280 pixels (long edge), or **1** for less
phone load. The console shows delivered frames per second. Use left Alt+1/2/3/4
to switch the cap without reconnecting; Alt+0 removes it. See [video](video.md#frame-rate).

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
