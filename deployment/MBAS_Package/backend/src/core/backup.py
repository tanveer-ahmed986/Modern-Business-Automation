import os
import shutil
import sqlite3
from datetime import datetime
from sqlmodel import Session, text
from .db import engine, DB_FILE

class BackupUtility:
    @staticmethod
    def create_backup(backup_dir: str = "backups") -> str:
        """
        Creates a consistent backup of the SQLite database using VACUUM INTO.
        Returns the path to the created backup file.
        """
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"mbas_backup_{timestamp}.db"
        backup_path = os.path.abspath(os.path.join(backup_dir, backup_filename))
        
        # Use VACUUM INTO for a safe, live backup
        with Session(engine) as session:
            # SQLModel session.exec with text() for raw SQL
            session.exec(text(f"VACUUM INTO '{backup_path}'"))
            
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
        
        # 3. Replace the file
        # We might need to handle file locking if the process still has the file open
        # In a real desktop app, we'd ideally trigger a restart after this.
        shutil.copy2(backup_path, DB_FILE)
        
        return True

    @staticmethod
    def list_backups(backup_dir: str = "backups") -> list:
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
