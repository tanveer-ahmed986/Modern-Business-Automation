import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Database,
  RefreshCw,
  History,
  AlertTriangle,
  Clock,
  CheckCircle,
  Settings as SettingsIcon,
  Play,
} from 'lucide-react';
import systemService, { type BackupRecord } from '@/services/system.service';
import { toast } from 'sonner';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
// Badge available from ui/badge if needed

interface BackupSchedule {
  enabled: boolean;
  hour: number;
  minute: number;
}

interface BackupStats {
  database_size_mb: number;
  backup_count: number;
  backup_total_size_mb: number;
  oldest_backup: string | null;
  newest_backup: string | null;
  storage_location: string;
}

const AutomaticBackupPage: React.FC = () => {
  const [backups, setBackups] = useState<BackupRecord[]>([]);
  const [stats, setStats] = useState<BackupStats | null>(null);
  const [schedule, setSchedule] = useState<BackupSchedule>({ enabled: true, hour: 0, minute: 0 });
  const [nextBackup, setNextBackup] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const fetchData = async () => {
    setLoading(true);
    try {
      const [backupsData, statsData, scheduleData] = await Promise.all([
        systemService.listBackups(),
        systemService.getBackupStats(),
        systemService.getBackupSchedule(),
      ]);

      setBackups(backupsData);
      setStats(statsData);
      setSchedule(scheduleData.schedule);
      setNextBackup(scheduleData.next_backup);
    } catch (error: any) {
      toast.error('Failed to load backup data: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };


  const handleTriggerBackup = async () => {
    try {
      await systemService.triggerBackupNow();
      toast.success('Backup triggered successfully!');
      setTimeout(fetchData, 2000); // Refresh after 2 seconds
    } catch (error: any) {
      toast.error('Failed to trigger backup: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleUpdateSchedule = async () => {
    try {
      await systemService.updateBackupSchedule(schedule);
      toast.success('Backup schedule updated successfully!');
      fetchData();
    } catch (error: any) {
      toast.error('Failed to update schedule: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleRestore = async (filename: string) => {
    try {
      const result = await systemService.restoreBackup(filename);
      toast.success(result.message, { duration: 10000 });
    } catch (error: any) {
      toast.error('Restore failed: ' + (error.response?.data?.detail || error.message));
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatNextBackup = () => {
    if (!nextBackup) return 'Not scheduled';
    const date = new Date(nextBackup);
    const now = new Date();
    const diff = date.getTime() - now.getTime();
    const hours = Math.floor(diff / 1000 / 60 / 60);
    const minutes = Math.floor((diff / 1000 / 60) % 60);

    if (hours < 0) return 'Overdue';
    if (hours === 0) return `in ${minutes} minutes`;
    return `in ${hours}h ${minutes}m`;
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Automatic Backup System</h1>
          <p className="text-muted-foreground">
            Protect your data with automated backups and retention policies.
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleTriggerBackup} variant="outline">
            <Play className="mr-2 h-4 w-4" />
            Backup Now
          </Button>
          <Button onClick={fetchData} variant="outline">
            <RefreshCw className="mr-2 h-4 w-4" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Database Size</CardTitle>
            <Database className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.database_size_mb.toFixed(2)} MB</div>
            <p className="text-xs text-muted-foreground">Current active database</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Backups</CardTitle>
            <History className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.backup_count || 0}</div>
            <p className="text-xs text-muted-foreground">
              {stats?.backup_total_size_mb.toFixed(2)} MB total
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Next Backup</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNextBackup()}</div>
            <p className="text-xs text-muted-foreground">
              {schedule.enabled ? `Daily at ${schedule.hour.toString().padStart(2, '0')}:${schedule.minute.toString().padStart(2, '0')}` : 'Disabled'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Status</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {schedule.enabled ? 'Active' : 'Paused'}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.newest_backup ? `Last: ${new Date(stats.newest_backup).toLocaleDateString()}` : 'No backups yet'}
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Backup Schedule Configuration */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <SettingsIcon className="h-5 w-5" />
              Backup Schedule
            </CardTitle>
            <CardDescription>Configure automatic backup timing</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="backup_enabled"
                checked={schedule.enabled}
                onChange={(e) => setSchedule({ ...schedule, enabled: e.target.checked })}
                className="h-4 w-4"
              />
              <Label htmlFor="backup_enabled" className="cursor-pointer">
                Enable automatic backups
              </Label>
            </div>

            <div className="space-y-2">
              <Label htmlFor="backup_hour">Time (24-hour format)</Label>
              <div className="flex gap-2">
                <Input
                  id="backup_hour"
                  type="number"
                  min="0"
                  max="23"
                  value={schedule.hour}
                  onChange={(e) => setSchedule({ ...schedule, hour: parseInt(e.target.value) || 0 })}
                  className="w-20"
                  disabled={!schedule.enabled}
                />
                <span className="self-center">:</span>
                <Input
                  type="number"
                  min="0"
                  max="59"
                  value={schedule.minute}
                  onChange={(e) => setSchedule({ ...schedule, minute: parseInt(e.target.value) || 0 })}
                  className="w-20"
                  disabled={!schedule.enabled}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                Backup will run daily at{' '}
                {schedule.hour.toString().padStart(2, '0')}:{schedule.minute.toString().padStart(2, '0')}
              </p>
            </div>

            <Button onClick={handleUpdateSchedule} className="w-full">
              Save Schedule
            </Button>

            <div className="pt-4 border-t">
              <h4 className="font-semibold text-sm mb-2">Retention Policy</h4>
              <ul className="text-xs text-muted-foreground space-y-1">
                <li>✓ Keep last 7 daily backups</li>
                <li>✓ Keep last 4 weekly backups</li>
                <li>✓ Keep last 3 monthly backups</li>
                <li>✓ Auto-delete older backups</li>
              </ul>
            </div>

            {stats && (
              <div className="pt-4 border-t">
                <h4 className="font-semibold text-sm mb-2">Storage Location</h4>
                <p className="text-xs font-mono bg-muted p-2 rounded break-all">
                  {stats.storage_location}
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Backup History */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <History className="h-5 w-5" />
              Backup History
            </CardTitle>
            <CardDescription>List of available system backups</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date & Time</TableHead>
                  <TableHead>Filename</TableHead>
                  <TableHead className="text-right">Size</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center py-8">
                      <RefreshCw className="h-6 w-6 animate-spin mx-auto text-muted-foreground" />
                    </TableCell>
                  </TableRow>
                ) : backups.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">
                      No backups found. Create your first backup!
                    </TableCell>
                  </TableRow>
                ) : (
                  backups.map((backup) => (
                    <TableRow key={backup.filename}>
                      <TableCell className="text-xs">
                        {new Date(backup.created_at).toLocaleString()}
                      </TableCell>
                      <TableCell className="font-mono text-xs">{backup.filename}</TableCell>
                      <TableCell className="text-right text-xs">
                        {formatSize(backup.size)}
                      </TableCell>
                      <TableCell className="text-right">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="ghost" size="sm" className="text-blue-600 hover:text-blue-700">
                              Restore
                            </Button>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Confirm Database Restore</DialogTitle>
                              <DialogDescription>
                                Are you absolutely sure you want to restore the database from{' '}
                                <strong>{backup.filename}</strong>? This will permanently replace your current data.
                              </DialogDescription>
                            </DialogHeader>
                            <DialogFooter>
                              <Button variant="outline" onClick={() => {}}>
                                Cancel
                              </Button>
                              <Button variant="destructive" onClick={() => handleRestore(backup.filename)}>
                                Yes, Restore Data
                              </Button>
                            </DialogFooter>
                          </DialogContent>
                        </Dialog>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* Info Box */}
      <Card className="bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5 shrink-0" />
            <div className="space-y-2 text-sm text-blue-800 dark:text-blue-300">
              <p className="font-semibold">Backup Best Practices:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>Backups are stored locally in the <code>backend/backups/</code> folder</li>
                <li>Copy important backups to external USB drive or cloud storage (Dropbox/Google Drive)</li>
                <li>Test restore functionality periodically to ensure backups are valid</li>
                <li>Keep at least one backup in a separate physical location for disaster recovery</li>
                <li>The system automatically keeps 7 daily, 4 weekly, and 3 monthly backups</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AutomaticBackupPage;
