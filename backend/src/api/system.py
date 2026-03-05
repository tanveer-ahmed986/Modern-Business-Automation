from fastapi import APIRouter, Depends, HTTPException, status
import os
from sqlmodel import Session
from typing import List, Dict, Any
from ..core.db import get_session
from ..core.auth import get_current_user
from ..core.features import check_feature
from ..core.backup import BackupUtility
from ..models.core import User, UserRole

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
