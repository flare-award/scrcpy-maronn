#!/usr/bin/env python3
"""Test live FPS reconfiguration on a disposable Android emulator, not its speed."""

import re
import socket
import struct
import subprocess
import sys
import time

SERVER = '/data/local/tmp/scrcpy-fps-test.jar'
TUNNEL = 'localabstract:scrcpy_00000002'


def adb(*args):
    return subprocess.check_output(['adb', *args], timeout=30)


def read_exact(stream, size):
    data = stream.read(size)
    if len(data) != size:
        raise EOFError('video stream unexpectedly closed')
    return data


def next_session(stream):
    """Skip any in-flight packets; wait for a new session AND real H.264 data."""
    deadline = time.monotonic() + 30
    size = None
    while time.monotonic() < deadline:
        flags, width_or_pts, length = struct.unpack('>III', read_exact(stream, 12))
        if flags & 0x80000000:  # session: flags, width, height
            size = (width_or_pts, length)
            assert min(size) > 0 and max(size) <= 1280, size
        else:
            assert 0 < length < 16 * 1024 * 1024, length
            read_exact(stream, length)
            if size and not flags & 0x40000000:  # not just codec configuration
                return size
    raise TimeoutError('no frame from the reconfigured session')


def check(server_binary, version):
    if adb('shell', 'getprop', 'ro.kernel.qemu').strip() != b'1':
        raise RuntimeError('Run only on a disposable emulator')
    api = int(adb('shell', 'getprop', 'ro.build.version.sdk'))
    adb('shell', 'input', 'keyevent', 'KEYCODE_WAKEUP')
    adb('shell', 'wm', 'dismiss-keyguard')
    adb('push', server_binary, SERVER)
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        listener.listen(2)
        listener.settimeout(30)
        adb('reverse', TUNNEL, f'tcp:{listener.getsockname()[1]}')
        server = subprocess.Popen(['adb', 'shell', 'CLASSPATH=' + SERVER, 'app_process', '/',
                                   'com.genymobile.scrcpy.Server', version, 'scid=2', 'audio=false',
                                   'max_size=1280', 'max_fps=60', 'cleanup=false', 'log_level=debug',
                                   'send_device_meta=false'])
        try:
            with listener.accept()[0] as video, listener.accept()[0] as control:
                video.settimeout(30)
                with video.makefile('rb') as stream:
                    assert read_exact(stream, 4) == b'h264'
                    for fps in (60, 90, 30, 120, 0):
                        if fps != 60:  # 60 supplied at startup; the rest on the SAME connection
                            control.sendall(struct.pack('>BH', 24, fps))
                        size = next_session(stream)
                        if api >= 34:
                            # Inspect the virtual display's REQUEST, not the emulator's throughput.
                            dump = adb('shell', 'dumpsys', 'display').decode()
                            assert re.search(r'^\s*mRequestedRefreshRate=' + str(fps) + r'\.0\s*$', dump, re.M), fps
                        print(f'Android API {api}: cap {fps}, receiving {size[0]}x{size[1]} video', flush=True)
        finally:
            server.terminate()
            server.wait(timeout=10)
            adb('reverse', '--remove', TUNNEL)
            adb('shell', 'rm', '-f', SERVER)


if __name__ == '__main__':
    try:
        check(*sys.argv[1:])
    except Exception as error:
        print(f'::error::Android mirror FPS smoke test: {error!r}', file=sys.stderr)
        raise
