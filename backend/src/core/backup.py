import os
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime
from .db import engine, DB_FILE, _DATA_DIR

# Default backup dir alongside the database in ProgramData
_DEFAULT_BACKUP_DIR = str(_DATA_DIR / "backups")

class BackupUtility:
    @staticmethod
    def create_backup(backup_dir: str = _DEFAULT_BACKUP_DIR) -> str:
        """
        Creates a consistent backup of the SQLite database using VACUUM INTO.
        Returns the path to the created backup file.
        """
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"mbas_backup_{timestamp}.db"
        backup_path = os.path.abspath(os.path.join(backup_dir, backup_filename))

        # Use VACUUM INTO for a safe, live backup. Run it on a DEDICATED
        # sqlite3 connection (not the SQLAlchemy pool) so a long-running
        # backup never occupies a pooled connection and starves requests.
        conn = sqlite3.connect(DB_FILE, timeout=30.0)
        try:
            conn.execute("VACUUM INTO ?", (backup_path,))
        finally:
            conn.close()

        return backup_path

    @staticmethod
    def restore_backup(backup_path: str) -> bool:
        """
        Restores the database from a backup file.
        WARNING: This replaces the current database.
        """
        if not os.path.exists(backup_path):
            return False

        # 1. Verify it's a valid SQLite file
        try:
            conn = sqlite3.connect(backup_path)
            conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
            conn.close()
        except sqlite3.Error:
            return False

        # 2. Close current connections (Engine disposal)
        engine.dispose()

        # 3. Drop the live database's WAL/SHM sidecar files BEFORE copying in
        # the backup. In WAL mode, SQLite replays "-wal" onto whichever main
        # file it finds on next connect — leaving the old WAL in place would
        # silently reapply pre-restore writes on top of the restored data.
        for suffix in ("-wal", "-shm"):
            sidecar = DB_FILE + suffix
            if os.path.exists(sidecar):
                os.remove(sidecar)

        # 4. Replace the file
        # In a real desktop app, we'd ideally trigger a restart after this.
        shutil.copy2(backup_path, DB_FILE)

        return True

    @staticmethod
    def list_backups(backup_dir: str = _DEFAULT_BACKUP_DIR) -> list:
        """Returns a list of available backups in the directory."""
        if not os.path.exists(backup_dir):
            return []
            
        backups = []
        for f in os.listdir(backup_dir):
            if f.endswith(".db"):
                path = os.path.join(backup_dir, f)
                stats = os.stat(path)
                backups.append({
                    "filename": f,
                    "path": os.path.abspath(path),
                    "size": stats.st_size,
                    "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat()
                })
        
        # Sort by creation time descending
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        return backups
