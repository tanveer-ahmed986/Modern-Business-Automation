"""
MBAS Backend Watchdog Service
Monitors backend health and auto-restarts if unresponsive
"""

import requests
import subprocess
import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Configuration
HEALTH_CHECK_URL = "http://127.0.0.1:8000/health"
CHECK_INTERVAL = 30  # seconds
MAX_FAILURES = 3  # Number of consecutive failures before restart
RESTART_COOLDOWN = 60  # seconds to wait after restart before checking again
LOG_FILE = Path(__file__).parent.parent / "watchdog.log"

class BackendWatchdog:
    def __init__(self):
        self.failure_count = 0
        self.backend_process = None
        self.last_restart = None

    def log(self, message, level="INFO"):
        """Log message to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def check_health(self):
        """Check if backend is healthy."""
        try:
            response = requests.get(HEALTH_CHECK_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    return True
            self.log(f"Health check failed: HTTP {response.status_code}", "WARN")
            return False
        except requests.exceptions.Timeout:
            self.log("Health check timed out", "WARN")
            return False
        except requests.exceptions.ConnectionError:
            self.log("Cannot connect to backend", "WARN")
            return False
        except Exception as e:
            self.log(f"Health check error: {e}", "ERROR")
            return False

    def kill_backend(self):
        """Kill existing backend process."""
        try:
            # Find and kill Python processes running uvicorn
            if sys.platform == "win32":
                # Windows
                subprocess.run(
                    ["taskkill", "/F", "/FI", "IMAGENAME eq python.exe", "/FI", "WINDOWTITLE eq MBAS*"],
                    capture_output=True,
                    timeout=10
                )
                subprocess.run(
                    ["taskkill", "/F", "/FI", "IMAGENAME eq pythonw.exe", "/FI", "WINDOWTITLE eq MBAS*"],
                    capture_output=True,
                    timeout=10
                )
                # Also kill by port
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                for line in result.stdout.split("\n"):
                    if ":8000" in line and "LISTENING" in line:
                        parts = line.split()
                        if parts:
                            pid = parts[-1]
                            try:
                                subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, timeout=5)
                                self.log(f"Killed process on port 8000 (PID: {pid})")
                            except:
                                pass
            else:
                # Linux/Mac
                subprocess.run(
                    ["pkill", "-f", "uvicorn.*mbas"],
                    capture_output=True,
                    timeout=10
                )

            time.sleep(2)  # Wait for processes to die
            self.log("Backend processes terminated")
            return True
        except Exception as e:
            self.log(f"Failed to kill backend: {e}", "ERROR")
            return False

    def start_backend(self):
        """Start backend server."""
        try:
            backend_dir = Path(__file__).parent

            if sys.platform == "win32":
                # Windows - use pythonw to run in background
                self.backend_process = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn", "src.main:app",
                     "--host", "127.0.0.1", "--port", "8000"],
                    cwd=str(backend_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                # Linux/Mac
                self.backend_process = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn", "src.main:app",
                     "--host", "127.0.0.1", "--port", "8000"],
                    cwd=str(backend_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

            self.log(f"Backend started (PID: {self.backend_process.pid})")
            self.last_restart = datetime.now()
            return True
        except Exception as e:
            self.log(f"Failed to start backend: {e}", "ERROR")
            return False

    def restart_backend(self):
        """Restart backend server."""
        self.log("Initiating backend restart...", "WARN")

        if self.kill_backend():
            time.sleep(3)  # Wait for cleanup
            if self.start_backend():
                self.log("Backend restarted successfully", "INFO")
                self.failure_count = 0
                return True

        self.log("Backend restart failed", "ERROR")
        return False

    def run(self):
        """Main watchdog loop."""
        self.log("MBAS Backend Watchdog started")
        self.log(f"Monitoring: {HEALTH_CHECK_URL}")
        self.log(f"Check interval: {CHECK_INTERVAL}s")
        self.log(f"Max failures: {MAX_FAILURES}")

        try:
            while True:
                # Check if backend is healthy
                is_healthy = self.check_health()

                if is_healthy:
                    if self.failure_count > 0:
                        self.log("Backend recovered")
                    self.failure_count = 0
                else:
                    self.failure_count += 1
                    self.log(f"Health check failed ({self.failure_count}/{MAX_FAILURES})", "WARN")

                    if self.failure_count >= MAX_FAILURES:
                        self.log("Max failures reached - restarting backend", "ERROR")
                        if self.restart_backend():
                            # Wait longer after restart
                            self.log(f"Waiting {RESTART_COOLDOWN}s before next check...")
                            time.sleep(RESTART_COOLDOWN)
                            continue
                        else:
                            self.log("Restart failed - will retry on next check", "ERROR")

                # Wait before next check
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            self.log("Watchdog stopped by user")
            sys.exit(0)
        except Exception as e:
            self.log(f"Watchdog error: {e}", "ERROR")
            sys.exit(1)

if __name__ == "__main__":
    watchdog = BackendWatchdog()
    watchdog.run()
