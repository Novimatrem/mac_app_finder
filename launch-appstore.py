#!/usr/bin/env python3
"""
Launch the Mac App Store and detach so the Terminal can be closed.
Works on macOS with Python 3.2+.
"""
import subprocess
import os
import sys

def launch_appstore():
    # Use DEVNULL to drop stdin/stdout/stderr
    DEVNULL = subprocess.DEVNULL

    # 'open -a "App Store"' launches the App Store app by name.
    cmd = ["open", "-a", "App Store"]

    # start_new_session=True makes the child the leader of a new session
    # so it won't receive SIGHUP when this script/terminal exits.
    try:
        p = subprocess.Popen(
            cmd,
            stdin=DEVNULL,
            stdout=DEVNULL,
            stderr=DEVNULL,
            close_fds=True,
            start_new_session=True
        )
    except Exception as e:
        print("Failed to launch App Store:", e, file=sys.stderr)
        return 1

    # Optionally print the PID of the 'open' helper (not the GUI app)
    print("Launched App Store (helper PID {}). You may close the Terminal.".format(p.pid))
    return 0

if __name__ == "__main__":
    sys.exit(launch_appstore())

