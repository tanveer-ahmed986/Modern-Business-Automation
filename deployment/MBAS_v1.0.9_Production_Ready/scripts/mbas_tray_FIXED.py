"""
MBAS System Tray Application - FIXED VERSION
Runs MBAS server in background without CMD window.
Provides system tray icon for start/stop/exit.

FIXES:
- Fixed undefined self.server_url bug (line 321)
- Increased startup timeout to 30 seconds for first-time runs
- Added proper virtual environment support
- Added comprehensive error logging
- Fixed frontend URL references
"""

import sys
import subprocess
import psutil
import os
import webbrowser
from pathlib import Path
from threading import Thread
import time
import traceback

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "Pillow", "psutil"])
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
        self.venv_dir = self.project_dir / "venv"

        # Use virtual environment Python if exists, otherwise system Python
        if (self.venv_dir / "Scripts" / "python.exe").exists():
            self.python_exe = str(self.venv_dir / "Scripts" / "python.exe")
            print(f"Using virtual environment: {self.python_exe}")
        else:
            self.python_exe = sys.executable
            print(f"Using system Python: {self.python_exe}")

        self.server_script = self.backend_dir / "src" / "main.py"
        self.watchdog_script = self.backend_dir / "watchdog.py"
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://127.0.0.1:5173"

        # FIXED: Changed to use backend_url (FastAPI serves frontend in production)
        self.app_url = self.backend_url

        # Log file for debugging
        self.log_file = self.project_dir / "mbas_tray.log"

        # Process tracking
        self.watchdog_process = None
        self.frontend_process = None

    def log(self, message):
        """Log message to file and console"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_msg + "\n")
        except Exception as e:
            print(f"Failed to write log: {e}")

    def create_icon_image(self, color="green"):
        """Create system tray icon image"""
        # Create a simple colored circle icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        dc = ImageDraw.Draw(image)

        # Draw circle
        if color == "green":
            fill_color = (34, 197, 94)  # Green when running
        elif color == "red":
            fill_color = (239, 68, 68)  # Red when stopped
        else:
            fill_color = (156, 163, 175)  # Gray when starting

        dc.ellipse([8, 8, 56, 56], fill=fill_color, outline='black', width=2)

        # Draw M in center
        dc.text((20, 15), "M", fill='white', font=None)

        return image

    def is_server_running(self):
        """Check if server is already running on port 8000"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == 8000 and conn.status == 'LISTEN':
                    return True
        except Exception as e:
            self.log(f"Error checking server status: {e}")
        return False

    def find_server_process(self):
        """Find the uvicorn server process"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline')
                    if cmdline and 'uvicorn' in ' '.join(cmdline) and 'src.main:app' in ' '.join(cmdline):
                        return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            self.log(f"Error finding server process: {e}")
        return None

    def start_server(self, icon=None, item=None):
        """Start MBAS with watchdog auto-recovery"""
        if self.is_running or self.is_server_running():
            self.log("Server already running")
            if icon:
                icon.notify("MBAS is already running!", "MBAS Server")
            return

        try:
            self.log("Starting MBAS server...")

            # Update icon to starting state
            if icon:
                icon.icon = self.create_icon_image("gray")
                icon.notify("Starting MBAS (this may take 30 seconds)...", "MBAS Server")

            # Start hidden (no window)
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            # Check if watchdog dependencies are available
            use_watchdog = False
            if self.watchdog_script.exists():
                try:
                    test_imports = subprocess.run(
                        [self.python_exe, "-c", "import requests"],
                        capture_output=True,
                        timeout=5
                    )
                    use_watchdog = (test_imports.returncode == 0)
                except Exception as e:
                    self.log(f"Watchdog check failed: {e}")
                    use_watchdog = False

            # Start backend server
            if use_watchdog:
                self.log("Starting backend with watchdog (auto-recovery enabled)")
                self.watchdog_process = subprocess.Popen(
                    [self.python_exe, str(self.watchdog_script)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    cwd=str(self.backend_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.log("Starting backend in direct mode (no watchdog)")
                self.watchdog_process = subprocess.Popen(
                    [self.python_exe, "-m", "uvicorn", "src.main:app",
                     "--host", "127.0.0.1", "--port", "8000"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    cwd=str(self.backend_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

            # FIXED: Increased timeout to 30 seconds for first-time startup
            max_retries = 30  # 30 seconds max wait
            self.log(f"Waiting for server to start (max {max_retries} seconds)...")

            for i in range(max_retries):
                time.sleep(1)
                if self.is_server_running():
                    self.log(f"Server started successfully after {i+1} seconds")
                    break
                if i % 5 == 0:
                    self.log(f"Still waiting... ({i}/{max_retries})")

            # Check if process crashed
            if self.watchdog_process.poll() is not None:
                stdout, stderr = self.watchdog_process.communicate()
                error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "Unknown error"
                self.log(f"Server process crashed: {error_msg}")
                raise Exception(f"Server crashed during startup: {error_msg[:200]}")

            # Verify server is running
            if self.is_server_running():
                self.is_running = True
                if icon:
                    icon.icon = self.create_icon_image("green")
                    mode = "Auto-Recovery" if use_watchdog else "Standard"
                    icon.notify(f"MBAS started successfully! ({mode} mode)", "MBAS Server")
                    icon.title = f"MBAS - Running ({mode})"
                self.log(f"MBAS is ready at {self.backend_url}")
            else:
                # Get error output
                if self.watchdog_process:
                    stdout, stderr = self.watchdog_process.communicate(timeout=2)
                    error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "Unknown error"
                    self.log(f"Startup error: {error_msg}")
                raise Exception(f"Server failed to start within {max_retries} seconds")

        except Exception as e:
            error_trace = traceback.format_exc()
            self.log(f"Failed to start server: {e}\n{error_trace}")
            self.is_running = False
            if icon:
                icon.icon = self.create_icon_image("red")
                icon.notify(f"Failed to start: {str(e)[:100]}", "MBAS Server")
                icon.title = "MBAS - Stopped"

    def stop_server(self, icon=None, item=None):
        """Stop MBAS (watchdog, backend, and frontend)"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("MBAS is not running!", "MBAS Server")
            return

        try:
            self.log("Stopping MBAS services...")
            if icon:
                icon.notify("Stopping MBAS services...", "MBAS Server")

            # Stop watchdog process
            if self.watchdog_process:
                try:
                    self.watchdog_process.terminate()
                    self.watchdog_process.wait(timeout=5)
                    self.log("Watchdog process stopped")
                except Exception as e:
                    self.log(f"Error stopping watchdog: {e}")

            # Stop frontend process
            if self.frontend_process:
                try:
                    self.frontend_process.terminate()
                    self.frontend_process.wait(timeout=5)
                    self.log("Frontend process stopped")
                except Exception as e:
                    self.log(f"Error stopping frontend: {e}")

            # Find and kill the backend server
            proc = self.find_server_process()
            if proc:
                proc.terminate()
                proc.wait(timeout=5)
                self.log("Backend server stopped")

            # Kill by port (backend)
            for conn in psutil.net_connections():
                if conn.laddr.port == 8000 and conn.status == 'LISTEN':
                    try:
                        psutil.Process(conn.pid).terminate()
                        self.log(f"Killed process on port 8000 (PID: {conn.pid})")
                    except Exception as e:
                        self.log(f"Error killing port 8000: {e}")

            # Kill by port (frontend)
            for conn in psutil.net_connections():
                if conn.laddr.port == 5173 and conn.status == 'LISTEN':
                    try:
                        psutil.Process(conn.pid).terminate()
                        self.log(f"Killed process on port 5173 (PID: {conn.pid})")
                    except Exception as e:
                        self.log(f"Error killing port 5173: {e}")

            self.is_running = False
            self.watchdog_process = None
            self.frontend_process = None

            if icon:
                icon.icon = self.create_icon_image("red")
                icon.notify("MBAS stopped", "MBAS Server")
                icon.title = "MBAS - Stopped"

            self.log("All services stopped successfully")

        except Exception as e:
            error_trace = traceback.format_exc()
            self.log(f"Error stopping server: {e}\n{error_trace}")
            if icon:
                icon.notify(f"Error stopping: {str(e)}", "MBAS Server")

    def open_browser(self, icon=None, item=None):
        """Open MBAS in browser"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("Server is not running. Starting now...", "MBAS Server")
            self.start_server(icon)
            time.sleep(5)  # Wait for server to start

        self.log(f"Opening browser: {self.app_url}")
        webbrowser.open(self.app_url)

    def show_status(self, icon=None, item=None):
        """Show server status"""
        status = "Running" if (self.is_running or self.is_server_running()) else "Stopped"
        msg = f"Status: {status}\nApp: {self.app_url}\nAPI: {self.backend_url}\nLog: {self.log_file}"
        self.log(f"Status check: {status}")
        if icon:
            icon.notify(msg, "MBAS Server")

    def exit_app(self, icon=None, item=None):
        """Exit application and stop server"""
        self.log("Exiting MBAS Tray App")
        self.stop_server(icon)
        if icon:
            icon.stop()

    def run(self):
        """Run the system tray application"""
        self.log("=== MBAS Tray App Starting ===")
        self.log(f"Project dir: {self.project_dir}")
        self.log(f"Python exe: {self.python_exe}")
        self.log(f"Backend dir: {self.backend_dir}")

        # Create menu
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

        # Check if server is already running
        if self.is_server_running():
            self.is_running = True
            icon_image = self.create_icon_image("green")
            title = "MBAS - Running"
            self.log("Server already running")
        else:
            icon_image = self.create_icon_image("red")
            title = "MBAS - Stopped"
            self.log("Server not running")

        # Create system tray icon
        self.icon = pystray.Icon(
            "mbas",
            icon_image,
            title,
            menu
        )

        # Auto-start server on launch
        Thread(target=self.start_server, args=(self.icon,)).start()

        # FIXED: Auto-open browser after server starts
        Thread(target=self.auto_open_browser).start()

        # Run the icon
        self.log("System tray icon ready")
        self.icon.run()

    def auto_open_browser(self):
        """Automatically open browser after server starts"""
        # Wait for server to be ready
        max_wait = 35  # FIXED: Increased to 35 seconds
        self.log("Waiting for server before auto-opening browser...")

        for i in range(max_wait):
            time.sleep(1)
            if self.is_server_running():
                self.log(f"Server ready after {i+1} seconds, opening browser...")
                time.sleep(2)  # Extra delay to ensure server is fully ready
                # FIXED: Use self.backend_url instead of undefined self.server_url
                webbrowser.open(self.backend_url)
                break


if __name__ == "__main__":
    app = MBASTrayApp()
    app.run()
