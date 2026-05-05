"""
MBAS Professional Launcher
A Product of Z&T Technologies
Website: www.zttechnologies.org

This launcher starts MBAS in professional mode (system tray, no CMD window)
"""

import sys
import subprocess
import os
from pathlib import Path
import time

def get_app_path():
    """Get the installation directory"""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent.parent

def main():
    """Main launcher"""
    app_path = get_app_path()

    # Paths
    python_exe = app_path / "python" / "python.exe"
    tray_script = app_path / "scripts" / "mbas_tray_FIXED.py"
    backend_dir = app_path / "backend"

    # Check if files exist
    if not python_exe.exists():
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "MBAS Error",
            "Python runtime not found!\n\n"
            f"Expected at: {python_exe}\n\n"
            "Please reinstall MBAS.\n\n"
            "Visit: www.zttechnologies.org"
        )
        return 1

    if not tray_script.exists():
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "MBAS Error",
            "Application files not found!\n\n"
            f"Expected at: {tray_script}\n\n"
            "Please reinstall MBAS.\n\n"
            "Visit: www.zttechnologies.org"
        )
        return 1

    # Start MBAS in system tray mode
    try:
        subprocess.Popen(
            [str(python_exe), str(tray_script)],
            cwd=str(app_path),
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Small delay to ensure process starts
        time.sleep(1)

        return 0

    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "MBAS Startup Error",
            f"Failed to start MBAS:\n\n{str(e)}\n\n"
            "Please contact support:\n"
            "www.zttechnologies.org"
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())
