"""
MBAS System Tray Launcher
A Product of Z&T Technologies
Website: www.zttechnologies.org

This launcher starts MBAS directly in system tray mode
"""

import sys
import subprocess
import os
from pathlib import Path

def get_app_path():
    """Get the installation directory"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent

def main():
    """Main launcher for tray mode"""
    app_path = get_app_path()

    python_exe = app_path / "python" / "python.exe"
    tray_script = app_path / "scripts" / "mbas_tray_FIXED.py"

    if not python_exe.exists() or not tray_script.exists():
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "MBAS Error",
            "MBAS files not found!\n\n"
            "Please reinstall MBAS from:\n"
            "www.zttechnologies.org"
        )
        return 1

    try:
        # Start tray app
        subprocess.Popen(
            [str(python_exe), str(tray_script)],
            cwd=str(app_path),
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return 0

    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "MBAS Error",
            f"Failed to start:\n{str(e)}\n\n"
            "Visit: www.zttechnologies.org"
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())
