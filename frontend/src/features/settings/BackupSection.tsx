import React, { useState, useEffect } from "react";
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import { 
  Database, 
  Download, 
  RefreshCw, 
  History, 
  AlertTriangle,
  HardDrive
} from "lucide-react";
import systemService, { BackupRecord } from "@/services/system.service";
import { toast } from "sonner";
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from "@/components/ui/dialog";

const BackupSection: React.FC = () => {
  const [backups, setBackups] = useState<BackupRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);

  const fetchBackups = async () => {
    setLoading(true);
    try {
      const data = await systemService.listBackups();
      setBackups(data);
    } catch (error: any) {
      toast.error("Failed to load backups: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBackup = async () => {
    setCreating(true);
    try {
      const result = await systemService.createBackup();
      toast.success(result.message);
      fetchBackups();
    } catch (error: any) {
      toast.error("Backup failed: " + (error.response?.data?.detail || error.message));
    } finally {
      setCreating(false);
    }
  };

  const handleRestore = async (filename: string) => {
    try {
      const result = await systemService.restoreBackup(filename);
      toast.success(result.message, {
        duration: 10000,
      });
    } catch (error: any) {
      toast.error("Restore failed: " + (error.response?.data?.detail || error.message));
    }
  };

  useEffect(() => {
    fetchBackups();
  }, []);

  const formatSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Database Backup & Restore</h2>
          <p className="text-muted-foreground">Manage your offline data safety.</p>
        </div>
        <Button onClick={handleCreateBackup} disabled={creating}>
          {creating ? (
            <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Database className="mr-2 h-4 w-4" />
          )}
          Create New Backup
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <HardDrive className="h-5 w-5" />
              Storage Info
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-sm">
              <p className="font-semibold text-slate-500">Current Database</p>
              <p className="text-lg font-mono">mbas_database.db</p>
            </div>
            <div className="text-sm">
              <p className="font-semibold text-slate-500">Backup Directory</p>
              <p className="text-lg font-mono">/backups</p>
            </div>
            <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg text-amber-800 dark:text-amber-400">
              <div className="flex items-start gap-2">
                <AlertTriangle className="h-5 w-5 mt-0.5 shrink-0" />
                <p className="text-xs leading-relaxed">
                  Restoring a backup will overwrite all current data. 
                  Please ensure you have a recent backup before performing a restore. 
                  The application may require a restart after restoration.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <History className="h-5 w-5" />
              Backup History
            </CardTitle>
            <CardDescription>List of available system backups.</CardDescription>
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
                      No backups found.
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
                                Are you absolutely sure you want to restore the database from <strong>{backup.filename}</strong>? 
                                This will permanently replace your current data.
                              </DialogDescription>
                            </DialogHeader>
                            <DialogFooter>
                              <Button variant="outline" onClick={() => {}}>Cancel</Button>
                              <Button 
                                variant="destructive" 
                                onClick={() => handleRestore(backup.filename)}
                              >
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
    </div>
  );
};

export default BackupSection;
