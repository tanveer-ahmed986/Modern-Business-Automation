"""
Automatic Backup Scheduler
Handles scheduled backups with retention policy
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from pathlib import Path
import logging
from .backup import BackupUtility
from .db import get_session
from ..models.core import Settings

logger = logging.getLogger(__name__)

class BackupScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)

    def start(self):
        """Start the backup scheduler"""
        # Load schedule from settings
        schedule = self._get_backup_schedule()

        if schedule.get("enabled", True):
            # Daily backup at midnight by default
            hour = schedule.get("hour", 0)
            minute = schedule.get("minute", 0)

            self.scheduler.add_job(
                self._run_backup,
                CronTrigger(hour=hour, minute=minute),
                id="daily_backup",
                name="Daily Automatic Backup",
                replace_existing=True
            )

            logger.info(f"Automatic backup scheduled: Daily at {hour:02d}:{minute:02d}")

        # Apply retention policy daily at 1 AM
        self.scheduler.add_job(
            self._apply_retention_policy,
            CronTrigger(hour=1, minute=0),
            id="retention_policy",
            name="Backup Retention Policy",
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("Backup scheduler started")

    def stop(self):
        """Stop the backup scheduler"""
        self.scheduler.shutdown()
        logger.info("Backup scheduler stopped")

    def _get_backup_schedule(self):
        """Get backup schedule from settings"""
        try:
            session = next(get_session())
            try:
                settings = session.get(Settings, 1)
                if settings and settings.feature_flags:
                    return settings.feature_flags.get("backup_schedule", {})
            finally:
                session.close()
        except Exception as e:
            logger.error(f"Failed to get backup schedule: {e}")

        return {"enabled": True, "hour": 0, "minute": 0}

    def _run_backup(self):
        """Execute automatic backup"""
        try:
            logger.info("Starting automatic backup...")
            backup_path = BackupUtility.create_backup()
            logger.info(f"Automatic backup completed: {backup_path}")

            # TODO: Send notification/email if configured
            self._send_backup_notification(success=True, path=backup_path)

        except Exception as e:
            logger.error(f"Automatic backup failed: {e}")
            self._send_backup_notification(success=False, error=str(e))

    def _apply_retention_policy(self):
        """
        Apply backup retention policy:
        - Keep last 7 daily backups
        - Keep last 4 weekly backups (one per week)
        - Keep last 3 monthly backups (one per month)
        - Delete all others
        """
        try:
            logger.info("Applying backup retention policy...")

            backups = BackupUtility.list_backups()
            if not backups:
                logger.info("No backups to clean up")
                return

            # Sort by date (newest first)
            backups.sort(key=lambda x: x["created_at"], reverse=True)

            now = datetime.now()
            keep_backups = set()

            # 1. Keep last 7 daily backups
            daily_backups = backups[:7]
            keep_backups.update(b["filename"] for b in daily_backups)
            logger.info(f"Keeping {len(daily_backups)} daily backups")

            # 2. Keep last 4 weekly backups (one per week)
            weekly_backups = []
            weeks_covered = set()
            for backup in backups:
                backup_date = datetime.fromisoformat(backup["created_at"])
                week_key = backup_date.strftime("%Y-W%U")

                if week_key not in weeks_covered:
                    weekly_backups.append(backup)
                    weeks_covered.add(week_key)
                    keep_backups.add(backup["filename"])

                    if len(weekly_backups) >= 4:
                        break

            logger.info(f"Keeping {len(weekly_backups)} weekly backups")

            # 3. Keep last 3 monthly backups (one per month)
            monthly_backups = []
            months_covered = set()
            for backup in backups:
                backup_date = datetime.fromisoformat(backup["created_at"])
                month_key = backup_date.strftime("%Y-%m")

                if month_key not in months_covered:
                    monthly_backups.append(backup)
                    months_covered.add(month_key)
                    keep_backups.add(backup["filename"])

                    if len(monthly_backups) >= 3:
                        break

            logger.info(f"Keeping {len(monthly_backups)} monthly backups")

            # 4. Delete backups not in keep list
            deleted_count = 0
            for backup in backups:
                if backup["filename"] not in keep_backups:
                    backup_path = Path(backup["path"])
                    if backup_path.exists():
                        backup_path.unlink()
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {backup['filename']}")

            logger.info(f"Retention policy applied: kept {len(keep_backups)}, deleted {deleted_count}")

        except Exception as e:
            logger.error(f"Failed to apply retention policy: {e}")

    def _send_backup_notification(self, success: bool, path: str = None, error: str = None):
        """
        Send notification about backup status
        TODO: Implement email/SMS notifications if configured
        """
        if success:
            logger.info(f"✅ Backup successful: {path}")
        else:
            logger.error(f"❌ Backup failed: {error}")

    def trigger_backup_now(self):
        """Manually trigger a backup (for testing)"""
        self._run_backup()

    def get_next_backup_time(self):
        """Get the next scheduled backup time"""
        job = self.scheduler.get_job("daily_backup")
        if job:
            return job.next_run_time
        return None

# Global scheduler instance
_scheduler = None

def get_scheduler() -> BackupScheduler:
    """Get the global backup scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackupScheduler()
    return _scheduler

def start_scheduler():
    """Start the global backup scheduler"""
    scheduler = get_scheduler()
    scheduler.start()

def stop_scheduler():
    """Stop the global backup scheduler"""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
        _scheduler = None
