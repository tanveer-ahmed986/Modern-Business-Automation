from fastapi import APIRouter, Depends, HTTPException, status
import os
from sqlmodel import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from ..core.db import get_session
from ..core.auth import get_current_user
from ..core.features import check_feature
from ..core.backup import BackupUtility
from ..core.scheduler import get_scheduler
from ..models.core import User, UserRole, Settings

router = APIRouter(prefix="/system", tags=["system"])

def get_admin(current_user: User = Depends(get_current_user)):
    """Ensures only admins can manage backups."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can manage backups."
        )
    return current_user

@router.get("/backups")
def list_backups(
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("backup_restore"))
):
    """List all available database backups."""
    return BackupUtility.list_backups()

@router.post("/backup")
def create_backup(
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("backup_restore"))
):
    """Trigger a new database backup."""
    try:
        path = BackupUtility.create_backup()
        return {"message": "Backup created successfully.", "path": path}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Backup failed: {str(e)}"
        )

@router.post("/restore")
def restore_backup(
    backup_filename: str,
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("backup_restore"))
):
    """
    Restore the database from a backup file.
    Note: Requires process restart or database reconnection.
    """
    backup_dir = "backups"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    if not os.path.exists(backup_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backup file not found."
        )
        
    try:
        success = BackupUtility.restore_backup(backup_path)
        if success:
            return {"message": "Database restored successfully. Please restart the application."}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restore failed. Invalid backup file."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Restore error: {str(e)}"
        )

class BackupScheduleConfig(BaseModel):
    enabled: bool = True
    hour: int = 0  # 0-23
    minute: int = 0  # 0-59

@router.get("/backup/schedule")
def get_backup_schedule(
    current_user: User = Depends(get_admin),
    session: Session = Depends(get_session)
):
    """Get current backup schedule configuration"""
    settings = session.get(Settings, 1)
    if settings and settings.feature_flags:
        schedule = settings.feature_flags.get("backup_schedule", {
            "enabled": True,
            "hour": 0,
            "minute": 0
        })
    else:
        schedule = {"enabled": True, "hour": 0, "minute": 0}

    # Get next backup time
    scheduler = get_scheduler()
    next_run = scheduler.get_next_backup_time()

    return {
        "schedule": schedule,
        "next_backup": next_run.isoformat() if next_run else None
    }

@router.post("/backup/schedule")
def update_backup_schedule(
    config: BackupScheduleConfig,
    current_user: User = Depends(get_admin),
    session: Session = Depends(get_session)
):
    """Update backup schedule configuration"""
    # Validate hour and minute
    if not (0 <= config.hour <= 23):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hour must be between 0 and 23"
        )
    if not (0 <= config.minute <= 59):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minute must be between 0 and 59"
        )

    # Update settings
    settings = session.get(Settings, 1)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settings not found"
        )

    if not settings.feature_flags:
        settings.feature_flags = {}

    settings.feature_flags["backup_schedule"] = {
        "enabled": config.enabled,
        "hour": config.hour,
        "minute": config.minute
    }

    session.add(settings)
    session.commit()

    # Restart scheduler with new schedule
    scheduler = get_scheduler()
    scheduler.stop()
    scheduler.start()

    return {
        "message": "Backup schedule updated successfully",
        "schedule": settings.feature_flags["backup_schedule"]
    }

@router.post("/backup/trigger")
def trigger_backup_now(
    current_user: User = Depends(get_admin)
):
    """Manually trigger a backup immediately"""
    try:
        scheduler = get_scheduler()
        scheduler.trigger_backup_now()
        return {"message": "Backup triggered successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger backup: {str(e)}"
        )

@router.get("/backup/stats")
def get_backup_stats(
    current_user: User = Depends(get_admin)
):
    """Get backup statistics and database size info"""
    import os
    from pathlib import Path

    # Get database size
    db_path = Path("database/mbas_database.db")
    db_size = db_path.stat().st_size if db_path.exists() else 0

    # Get backup directory size
    backup_dir = Path("backups")
    backup_size = sum(f.stat().st_size for f in backup_dir.glob("*.db") if f.is_file())

    # Get backup count
    backups = BackupUtility.list_backups()

    # Calculate total size of all backups
    total_backup_size = sum(b["size"] for b in backups)

    return {
        "database_size": db_size,
        "database_size_mb": round(db_size / 1024 / 1024, 2),
        "backup_count": len(backups),
        "backup_total_size": total_backup_size,
        "backup_total_size_mb": round(total_backup_size / 1024 / 1024, 2),
        "oldest_backup": backups[-1]["created_at"] if backups else None,
        "newest_backup": backups[0]["created_at"] if backups else None,
        "storage_location": str(backup_dir.absolute())
    }
