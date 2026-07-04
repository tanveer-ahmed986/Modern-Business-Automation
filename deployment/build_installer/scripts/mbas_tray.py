"""
MBAS System Tray Application
Runs MBAS server in background without CMD window.
Provides system tray icon for start/stop/exit.

Z&T Technologies - State-of-the-Art Business Solutions
"""

import sys
import subprocess
import os
import webbrowser
from pathlib import Path
from threading import Thread
import time
import traceback

# Early error logging setup - critical for diagnosing pythonw.exe crashes
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_DIR = _SCRIPT_DIR.parent

# All writable data goes to ProgramData to avoid Program Files write restrictions
_MBAS_DATA_ROOT = Path(os.environ.get("ProgramData", "C:\\ProgramData")) / "MBAS"
_LOG_DIR = _MBAS_DATA_ROOT / "logs"
try:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
except OSError:
    pass
_CRASH_LOG = _LOG_DIR / "mbas_tray.log"

# Venv location (ProgramData to avoid Program Files path issues)
_VENV_DIR = _MBAS_DATA_ROOT / "venv"

def _fatal_error(msg, exc=None):
    """Write fatal error to log and show message box before exiting."""
    error_text = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] FATAL: {msg}"
    if exc:
        error_text += f"\n{traceback.format_exc()}"
    try:
        with open(_CRASH_LOG, "a") as f:
            f.write(error_text + "\n")
    except:
        pass
    # Show error via Windows message box (works even from pythonw.exe)
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            f"MBAS failed to start:\n\n{msg}\n\nCheck log: {_CRASH_LOG}",
            "MBAS Error",
            0x10  # MB_ICONERROR
        )
    except:
        pass
    sys.exit(1)

try:
    import psutil
except ImportError as e:
    _fatal_error(f"Missing package 'psutil': {e}", e)

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    _fatal_error(f"Missing package 'pystray' or 'Pillow': {e}", e)


class MBASTrayApp:
    def __init__(self):
        self.server_process = None
        self.icon = None
        self.is_running = False

        # Get paths
        self.script_dir = Path(__file__).resolve().parent
        self.project_dir = self.script_dir.parent
        self.backend_dir = self.project_dir / "backend"
        self.frontend_dir = self.project_dir / "frontend"

        # Venv in ProgramData (avoids Program Files path confusion)
        venv_dir = _VENV_DIR
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pythonw = venv_dir / "Scripts" / "pythonw.exe"

        # Also check legacy location (in-app venv)
        if not venv_python.exists():
            venv_python = self.project_dir / "venv" / "Scripts" / "python.exe"
            venv_pythonw = self.project_dir / "venv" / "Scripts" / "pythonw.exe"

        if venv_python.exists():
            self.python_exe = str(venv_python)
            self.pythonw_exe = str(venv_pythonw) if venv_pythonw.exists() else str(venv_python)
        else:
            _fatal_error(
                f"Python virtual environment not found.\n\n"
                f"Checked:\n"
                f"  {_VENV_DIR / 'Scripts' / 'python.exe'}\n"
                f"  {self.project_dir / 'venv' / 'Scripts' / 'python.exe'}\n\n"
                f"Please run INSTALL_MBAS.bat as Administrator."
            )

        self.watchdog_script = self.backend_dir / "watchdog.py"

        # In production, FastAPI serves both API and frontend on port 8000
        self.backend_url = "http://127.0.0.1:8000"
        self.app_url = self.backend_url

        # Process tracking
        self.watchdog_process = None

        # Log file (in ProgramData, not Program Files)
        self.log_file = _LOG_DIR / "mbas_tray.log"

        # Icon file (use custom .ico if available)
        self.icon_file = self.project_dir / "mbas_icon.ico"

    def log(self, msg):
        """Write to log file for troubleshooting."""
        try:
            with open(self.log_file, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except:
            pass

    def create_icon_image(self, color="green"):
        """Create system tray icon image."""
        # Try to use the custom .ico file first
        if color == "green" and self.icon_file.exists():
            try:
                return Image.open(str(self.icon_file))
            except:
                pass

        # Fallback: generate a colored circle icon
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)

        if color == "green":
            fill_color = (34, 197, 94)
        elif color == "red":
            fill_color = (239, 68, 68)
        else:
            fill_color = (156, 163, 175)

        # Draw filled circle with border
        dc.ellipse([4, 4, 60, 60], fill=fill_color, outline=(255, 255, 255), width=3)

        # Draw "M" letter
        try:
            font = ImageFont.truetype("arial.ttf", 30)
            dc.text((17, 10), "M", fill='white', font=font)
        except:
            dc.text((22, 16), "M", fill='white')

        return image

    def is_server_running(self):
        """Check if server is already running on port 8000"""
        # Use socket connect as primary check (works without admin)
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            return result == 0
        except:
            pass
        # Fallback: psutil (may need admin on some systems)
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == 8000 and conn.status == 'LISTEN':
                    return True
        except (psutil.AccessDenied, PermissionError):
            pass
        return False

    def find_server_process(self):
        """Find the uvicorn server process"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline')
                if cmdline and 'uvicorn' in ' '.join(cmdline) and 'src.main:app' in ' '.join(cmdline):
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def start_server(self, icon=None, item=None):
        """Start MBAS backend server"""
        if self.is_running or self.is_server_running():
            self.is_running = True
            self.log("Server already running")
            if icon:
                icon.icon = self.create_icon_image("green")
                icon.title = "MBAS - Running (http://localhost:8000)"
            return

        try:
            if icon:
                icon.icon = self.create_icon_image("gray")
                icon.title = "MBAS - Starting..."

            self.log(f"Starting server from {self.backend_dir}")
            self.log(f"Using Python: {self.python_exe}")

            # Hidden window flags
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            # Start uvicorn directly - no console window
            # Use pythonw.exe to prevent any console window from appearing
            self.log("Starting uvicorn directly...")
            self.log(f"Using pythonw: {self.pythonw_exe}")
            self.server_process = subprocess.Popen(
                [self.pythonw_exe, "-m", "uvicorn", "src.main:app",
                 "--host", "127.0.0.1", "--port", "8000", "--workers", "1",
                 "--timeout-keep-alive", "30"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                cwd=str(self.backend_dir),
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Wait for server to start (up to 30 seconds)
            self.log("Waiting for server to start...")
            for i in range(30):
                time.sleep(1)
                if self.is_server_running():
                    break
                # Check if process died
                if self.server_process.poll() is not None:
                    stderr = self.server_process.stderr.read().decode(errors='ignore')
                    self.log(f"Server process exited with code {self.server_process.returncode}")
                    self.log(f"Server stderr: {stderr[:1000]}")
                    break

            if self.is_server_running():
                self.is_running = True
                self.log("Server started successfully!")
                if icon:
                    icon.icon = self.create_icon_image("green")
                    icon.title = "MBAS - Running (http://localhost:8000)"
            else:
                self.log("Server failed to start within timeout")
                if icon:
                    icon.icon = self.create_icon_image("red")
                    icon.title = "MBAS - Failed to start"
                    icon.notify("Server failed to start.\nCheck mbas_tray.log for details.", "MBAS Error")

        except Exception as e:
            self.is_running = False
            self.log(f"Error starting server: {e}\n{traceback.format_exc()}")
            if icon:
                icon.icon = self.create_icon_image("red")
                icon.title = "MBAS - Error"
                icon.notify(f"Failed to start: {str(e)}", "MBAS Error")

    def stop_server(self, icon=None, item=None):
        """Stop MBAS server"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("MBAS is not running.", "MBAS Server")
            return

        try:
            self.log("Stopping server...")

            # Stop direct server process
            if self.server_process:
                try:
                    self.server_process.terminate()
                    self.server_process.wait(timeout=5)
                except:
                    try:
                        self.server_process.kill()
                    except:
                        pass

            # Stop watchdog process
            if self.watchdog_process:
                try:
                    self.watchdog_process.terminate()
                    self.watchdog_process.wait(timeout=5)
                except:
                    pass

            # Find and kill the backend server
            proc = self.find_server_process()
            if proc:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except:
                    proc.kill()

            # Kill by port
            try:
                for conn in psutil.net_connections():
                    if conn.laddr.port == 8000 and conn.status == 'LISTEN':
                        try:
                            psutil.Process(conn.pid).terminate()
                        except:
                            pass
            except (psutil.AccessDenied, PermissionError):
                pass

            self.is_running = False
            self.watchdog_process = None
            self.log("Server stopped")

            if icon:
                icon.icon = self.create_icon_image("red")
                icon.title = "MBAS - Stopped"
                icon.notify("MBAS server stopped.", "MBAS Server")

        except Exception as e:
            self.log(f"Error stopping: {e}")

    def open_browser(self, icon=None, item=None):
        """Open MBAS in browser"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("Starting server first...", "MBAS Server")
            self.start_server(icon)
            # Wait for server to be ready
            for _ in range(15):
                time.sleep(1)
                if self.is_server_running():
                    break

        self.log(f"Opening browser: {self.app_url}")
        webbrowser.open(self.app_url)

    def show_status(self, icon=None, item=None):
        """Show server status"""
        running = self.is_running or self.is_server_running()
        status = "Running" if running else "Stopped"
        if icon:
            icon.notify(
                f"Status: {status}\nURL: {self.app_url}",
                "MBAS Server"
            )

    def exit_app(self, icon=None, item=None):
        """Exit application and stop server"""
        self.stop_server(icon)
        if icon:
            icon.stop()

    def run(self):
        """Run the system tray application"""
        self.log("=" * 50)
        self.log("MBAS Tray App starting")
        self.log(f"Project dir: {self.project_dir}")
        self.log(f"Backend dir: {self.backend_dir}")
        self.log(f"Python: {self.python_exe}")

        menu = pystray.Menu(
            pystray.MenuItem("Open MBAS", self.open_browser, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Start Server", self.start_server),
            pystray.MenuItem("Stop Server", self.stop_server),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Status", self.show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.exit_app)
        )

        if self.is_server_running():
            self.is_running = True
            icon_image = self.create_icon_image("green")
            title = "MBAS - Running (http://localhost:8000)"
        else:
            icon_image = self.create_icon_image("gray")
            title = "MBAS - Starting..."

        self.icon = pystray.Icon(
            "MBAS",
            icon_image,
            title,
            menu
        )

        # Auto-start server in background
        Thread(target=self.start_server, args=(self.icon,), daemon=True).start()

        # Auto-open browser after server starts
        Thread(target=self._auto_open_browser, daemon=True).start()

        # Run the tray icon (blocks)
        self.icon.run()

    def _auto_open_browser(self):
        """Automatically open browser after server starts"""
        for _ in range(45):  # Wait up to 45 seconds
            time.sleep(1)
            if self.is_server_running():
                time.sleep(2)  # Extra delay for full readiness
                webbrowser.open(self.app_url)
                self.log("Browser opened automatically")
                return
        self.log("Timeout waiting for server - browser not opened")


if __name__ == "__main__":
    try:
        app = MBASTrayApp()
        app.run()
    except Exception as e:
        _fatal_error(f"Unhandled exception: {e}", e)
