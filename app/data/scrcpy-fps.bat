@echo off
setlocal
pushd "%~dp0" || exit /b 1
echo Select a screen mirroring preset. FPS is a limit, not a guarantee.
echo  [1] 30 fps - lowest phone load  (1024 px, 3 Mbps)
echo  [2] 60 fps - balanced           (1280 px, 4 Mbps)
echo  [3] 90 fps - high refresh       (1280 px, 6 Mbps)
echo  [4] 120 fps - high refresh      (1280 px, 8 Mbps)
choice /c 1234 /n /m "Press 1, 2, 3 or 4: "
set "preset=%errorlevel%"
set "options="
if "%preset%"=="1" set "options=-m1024 -b3M --max-fps=30"
if "%preset%"=="2" set "options=-m1280 -b4M --max-fps=60"
if "%preset%"=="3" set "options=-m1280 -b6M --max-fps=90"
if "%preset%"=="4" set "options=-m1280 -b8M --max-fps=120"
if not defined options exit /b 1
echo While mirroring: left Alt+1/2/3/4 changes FPS, left Alt+0 removes the cap.
".\scrcpy.exe" %options% --print-fps --pause-on-exit=if-error
set "result=%errorlevel%"
popd
exit /b %result%
