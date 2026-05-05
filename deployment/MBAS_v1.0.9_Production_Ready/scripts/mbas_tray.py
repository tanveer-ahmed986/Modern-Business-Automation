"""
MBAS System Tray Application
Runs MBAS server in background without CMD window.
Provides system tray icon for start/stop/exit.
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

        # Use system Python (no venv required)
        self.python_exe = sys.executable

        self.server_script = self.backend_dir / "src" / "main.py"
        self.watchdog_script = self.backend_dir / "watchdog.py"
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://127.0.0.1:5173"
        self.app_url = self.frontend_url  # Users access frontend

        # Process tracking
        self.watchdog_process = None
        self.frontend_process = None

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
        for conn in psutil.net_connections():
            if conn.laddr.port == 8000 and conn.status == 'LISTEN':
                return True
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
        """Start MBAS with watchdog auto-recovery and frontend"""
        if self.is_running or self.is_server_running():
            if icon:
                icon.notify("MBAS is already running!", "MBAS Server")
            return

        try:
            # Update icon to starting state
            if icon:
                icon.icon = self.create_icon_image("gray")
                icon.notify("Starting MBAS with auto-recovery...", "MBAS Server")

            # Start hidden (no window)
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            # Try to start with watchdog if available, fallback to direct start
            use_watchdog = self.watchdog_script.exists()

            if use_watchdog:
                try:
                    # Verify watchdog dependencies
                    test_imports = subprocess.run(
                        [self.python_exe, "-c", "import requests"],
                        capture_output=True,
                        timeout=5
                    )
                    if test_imports.returncode != 0:
                        use_watchdog = False
                except:
                    use_watchdog = False

            if use_watchdog:
                # Start backend with watchdog (auto-recovery enabled)
                self.watchdog_process = subprocess.Popen(
                    [self.python_exe, str(self.watchdog_script)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    cwd=str(self.backend_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                # Direct start without watchdog
                self.watchdog_process = subprocess.Popen(
                    [self.python_exe, "-m", "uvicorn", "src.main:app",
                     "--host", "127.0.0.1", "--port", "8000"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    cwd=str(self.backend_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

            # Wait for backend to start (longer wait for first-time startup)
            max_retries = 45  # 45 seconds max wait (first startup needs time for DB init)
            for i in range(max_retries):
                time.sleep(1)
                if self.is_server_running():
                    break

            # Start frontend if dist exists (production mode)
            frontend_dist = self.frontend_dir / "dist"
            if not frontend_dist.exists():
                # Development mode - try npm run dev
                try:
                    self.frontend_process = subprocess.Popen(
                        ["cmd", "/c", "npm", "run", "dev"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        startupinfo=startupinfo,
                        cwd=str(self.frontend_dir),
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                except:
                    pass  # Frontend optional in production with embedded dist

            # Verify server is running
            if self.is_server_running():
                self.is_running = True
                if icon:
                    icon.icon = self.create_icon_image("green")
                    mode = "Auto-Recovery" if use_watchdog else "Standard"
                    icon.notify(f"MBAS started successfully! ({mode} mode)", "MBAS Server")
                    icon.title = f"MBAS - Running ({mode})"
            else:
                raise Exception("Server failed to start within 45 seconds")

        except Exception as e:
            self.is_running = False
            if icon:
                icon.icon = self.create_icon_image("red")
                icon.notify(f"Failed to start: {str(e)}", "MBAS Server")
                icon.title = "MBAS - Stopped"

    def stop_server(self, icon=None, item=None):
        """Stop MBAS (watchdog, backend, and frontend)"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("MBAS is not running!", "MBAS Server")
            return

        try:
            if icon:
                icon.notify("Stopping MBAS services...", "MBAS Server")

            # Stop watchdog process
            if self.watchdog_process:
                try:
                    self.watchdog_process.terminate()
                    self.watchdog_process.wait(timeout=5)
                except:
                    pass

            # Stop frontend process
            if self.frontend_process:
                try:
                    self.frontend_process.terminate()
                    self.frontend_process.wait(timeout=5)
                except:
                    pass

            # Find and kill the backend server
            proc = self.find_server_process()
            if proc:
                proc.terminate()
                proc.wait(timeout=5)

            # Kill by port (backend)
            for conn in psutil.net_connections():
                if conn.laddr.port == 8000 and conn.status == 'LISTEN':
                    try:
                        psutil.Process(conn.pid).terminate()
                    except:
                        pass

            # Kill by port (frontend)
            for conn in psutil.net_connections():
                if conn.laddr.port == 5173 and conn.status == 'LISTEN':
                    try:
                        psutil.Process(conn.pid).terminate()
                    except:
                        pass

            self.is_running = False
            self.watchdog_process = None
            self.frontend_process = None

            if icon:
                icon.icon = self.create_icon_image("red")
                icon.notify("MBAS stopped", "MBAS Server")
                icon.title = "MBAS - Stopped"

        except Exception as e:
            if icon:
                icon.notify(f"Error stopping: {str(e)}", "MBAS Server")

    def open_browser(self, icon=None, item=None):
        """Open MBAS in browser"""
        if not self.is_running and not self.is_server_running():
            if icon:
                icon.notify("Server is not running. Starting now...", "MBAS Server")
            self.start_server(icon)
            time.sleep(5)  # Wait for server to start

        webbrowser.open(self.app_url)

    def show_status(self, icon=None, item=None):
        """Show server status"""
        status = "Running with Auto-Recovery" if (self.is_running or self.is_server_running()) else "Stopped"
        if icon:
            icon.notify(f"Status: {status}\nApp: {self.app_url}\nAPI: {self.backend_url}", "MBAS Server")

    def exit_app(self, icon=None, item=None):
        """Exit application and stop server"""
        self.stop_server(icon)
        if icon:
            icon.stop()

    def run(self):
        """Run the system tray application"""
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
        else:
            icon_image = self.create_icon_image("red")
            title = "MBAS - Stopped"

        # Create system tray icon
        self.icon = pystray.Icon(
            "mbas",
            icon_image,
            title,
            menu
        )

        # Auto-start server on launch
        Thread(target=self.start_server, args=(self.icon,)).start()

        # Auto-open browser after server starts (professional experience)
        Thread(target=self.auto_open_browser).start()

        # Run the icon
        self.icon.run()

    def auto_open_browser(self):
        """Automatically open browser after server starts"""
        # Wait for server to be ready
        max_wait = 10  # seconds
        for _ in range(max_wait):
            time.sleep(1)
            if self.is_server_running():
                time.sleep(2)  # Extra delay to ensure server is fully ready
                webbrowser.open(self.server_url)
                break


if __name__ == "__main__":
    app = MBASTrayApp()
    app.run()
