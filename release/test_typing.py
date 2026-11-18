#!/usr/bin/env python3
"""Exercise SDK typing in a native EditText on a disposable Android emulator."""

import re
import socket
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET


SERVER = '/data/local/tmp/scrcpy-typing-test.jar'
DUMP = '/data/local/tmp/scrcpy-typing-test.xml'
TUNNEL = 'localabstract:scrcpy_00000001'


def adb(*args):
    return subprocess.check_output(['adb', *args], timeout=30)


def field():
    adb('shell', 'uiautomator', 'dump', DUMP)
    root = ET.fromstring(adb('exec-out', 'cat', DUMP))
    return next(n for n in root.iter('node')
                if n.get('class') == 'android.widget.EditText')


def key(code, meta=0):
    return b''.join(struct.pack('>BBIII', 0, action, code, 0, meta)
                    for action in (0, 1))


def string(text):
    data = text.encode('utf-8')
    return struct.pack('>I', len(data)) + data


def check(server_binary, version):
    if adb('shell', 'getprop', 'ro.kernel.qemu').strip() != b'1':
        raise RuntimeError('Run only on a disposable emulator')
    adb('shell', 'input', 'keyevent', 'KEYCODE_WAKEUP')
    adb('shell', 'wm', 'dismiss-keyguard')
    # The system Save As dialog has a native filename editor. Never press Save.
    adb('shell', 'am', 'start', '-W', '-a', 'android.intent.action.CREATE_DOCUMENT',
        '-c', 'android.intent.category.OPENABLE', '-t', 'text/plain',
        '--es', 'android.intent.extra.TITLE', 'start')
    left, top, right, bottom = map(int, re.findall(r'\d+', field().get('bounds')))
    adb('shell', 'input', 'tap', str((left + right) // 2), str((top + bottom) // 2))

    adb('push', server_binary, SERVER)
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        listener.listen(1)
        listener.settimeout(25)
        adb('reverse', TUNNEL, f'tcp:{listener.getsockname()[1]}')
        server = subprocess.Popen(['adb', 'shell', 'CLASSPATH=' + SERVER, 'app_process', '/',
                                   'com.genymobile.scrcpy.Server', version, 'scid=1', 'video=false',
                                   'audio=false', 'cleanup=false', 'send_device_meta=false'])
        try:
            conn, _ = listener.accept()
            with conn:
                # Set the test clipboard, then type EN -> RU -> EN without any pauses.
                saved = '[saved]'
                conn.sendall(struct.pack('>BQB', 9, 0, 0) + string(saved))
                conn.sendall(key(29, 0x1000) + key(67))  # Ctrl+A, Backspace
                conn.sendall(key(29))  # A key on the English layout
                for c in 'Привет, Ёж №1!':
                    kind = 23 if ord(c) > 127 else 1  # PASTE_TEXT or INJECT_TEXT
                    conn.sendall(bytes([kind]) + string(c))
                conn.sendall(key(54) + key(279))  # English Z, then paste the saved clipboard
                expected = 'aПривет, Ёж №1!z' + saved
                actual = field().get('text')
                if actual != expected:
                    raise AssertionError(f'Expected {expected!r}, got {actual!r}')
                print(f'Android editor: {actual}')
        finally:
            server.terminate()
            server.wait(timeout=10)
            adb('reverse', '--remove', TUNNEL)
            adb('shell', 'rm', '-f', SERVER, DUMP)


if __name__ == '__main__':
    try:
        check(*sys.argv[1:])
    except Exception as error:
        print(f'::error::Android typing smoke test: {error}', file=sys.stderr)
        raise
