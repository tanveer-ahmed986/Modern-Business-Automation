"""
MBAS System Tray Application
Runs MBAS server in background without CMD window.
Provides system tray icon for start/stop/exit.

Z&T Technologies - State-of-the-Art Business Solutions
"""

import sys
import subprocess
import psutil
import os
import webbrowser
from pathlib import Path
from threading import Thread
import time

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("Installing required packages (pystray, Pillow)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "Pillow"])
    import pystray
    from PIL import Image, ImageDraw


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

        # Use the venv Python if available, otherwise system Python
        venv_python = self.project_dir / "venv" / "Scripts" / "python.exe"
        venv_pythonw = self.project_dir / "venv" / "Scripts" / "pythonw.exe"
        if venv_python.exists():
            self.python_exe = str(venv_python)
            self.pythonw_exe = str(venv_pythonw) if venv_pythonw.exists() else str(venv_python)
        else:
            self.python_exe = sys.executable
            self.pythonw_exe = sys.executable

        self.watchdog_script = self.backend_dir / "watchdog.py"

        # In production, FastAPI serves both API and frontend on port 8000
        # The frontend is pre-built in frontend/dist/ and served as static files
        self.backend_url = "http://127.0.0.1:8000"
        self.app_url = self.backend_url  # Users access everything on port 8000

        # Process tracking
        self.watchdog_process = None

        # Log file
        self.log_file = self.project_dir / "mbas_tray.log"

    def log(self, msg):
        """Write to log file for troubleshooting."""
        try:
            with open(self.log_file, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except:
            pass

    def create_icon_image(self, color="green"):
        """Create system tray icon image"""
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        dc = ImageDraw.Draw(image)

        if color == "green":
            fill_color = (34, 197, 94)
        elif color == "red":
            fill_color = (239, 68, 68)
        else:
            fill_color = (156, 163, 175)

        dc.ellipse([8, 8, 56, 56], fill=fill_color, outline='black', width=2)
        dc.text((20, 15), "M", fill='white')

        return image

    def is_server_running(self):
        """Check if server is already running on port 8000"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == 8000 and conn.status == 'LISTEN':
                    return True
        except (psutil.AccessDenied, PermissionError):
            # Fallback: try to connect
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            return result == 0
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
                icon.title = "MBAS - Running"
                icon.notify("MBAS is already running!", "MBAS Server")
            return

        try:
            if icon:
                icon.icon = self.create_icon_image("gray")
                icon.notify("Starting MBAS server...", "MBAS Server")

            self.log(f"Starting server from {self.backend_dir}")
            self.log(f"Using Python: {self.python_exe}")

            # Hidden window flags
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            # Always start uvicorn directly for fast startup
            self.log("Starting uvicorn directly...")
            self.server_process = subprocess.Popen(
                [self.python_exe, "-m", "uvicorn", "src.main:app",
                 "--host", "127.0.0.1", "--port", "8000"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                cwd=str(self.backend_dir),
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Optionally start watchdog for auto-restart monitoring
            if self.watchdog_script.exists():
                self.log("Starting watchdog monitor...")
                self.watchdog_process = subprocess.Popen(
                    [self.python_exe, str(self.watchdog_script)],
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
                    self.log(f"Server stderr: {stderr[:500]}")
                    break

            if self.is_server_running():
                self.is_running = True
                self.log("Server started successfully!")
                if icon:
                    icon.icon = self.create_icon_image("green")
                    icon.notify("MBAS is running!\nOpen: http://localhost:8000", "MBAS Server")
                    icon.title = "MBAS - Running"
            else:
                self.log("Server failed to start within timeout")
                if icon:
                    icon.icon = self.create_icon_image("red")
                    icon.notify("Server failed to start. Check mbas_tray.log", "MBAS Server")
                    icon.title = "MBAS - Failed"

        except Exception as e:
            self.is_running = False
            self.log(f"Error starting server: {e}")
            if icon:
                icon.icon = self.create_icon_image("red")
                icon.notify(f"Failed to start: {str(e)}", "MBAS Server")
                icon.title = "MBAS - Error"

    def stop_server(self, icon=None, item=None):
        """Stop MBAS server"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("MBAS is not running!", "MBAS Server")
            return

        try:
            self.log("Stopping server...")
            if icon:
                icon.notify("Stopping MBAS...", "MBAS Server")

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
                icon.notify("MBAS stopped", "MBAS Server")
                icon.title = "MBAS - Stopped"

        except Exception as e:
            self.log(f"Error stopping: {e}")
            if icon:
                icon.notify(f"Error stopping: {str(e)}", "MBAS Server")

    def open_browser(self, icon=None, item=None):
        """Open MBAS in browser"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("Starting server first...", "MBAS Server")
            self.start_server(icon)
            time.sleep(3)

        self.log(f"Opening browser: {self.app_url}")
        webbrowser.open(self.app_url)

    def show_status(self, icon=None, item=None):
        """Show server status"""
        running = self.is_running or self.is_server_running()
        status = "Running" if running else "Stopped"
        if icon:
            icon.notify(
                f"Status: {status}\nURL: {self.app_url}\nLogin: admin / admin123",
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
            title = "MBAS - Running"
        else:
            icon_image = self.create_icon_image("red")
            title = "MBAS - Starting..."

        self.icon = pystray.Icon(
            "mbas",
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
    app = MBASTrayApp()
    app.run()
