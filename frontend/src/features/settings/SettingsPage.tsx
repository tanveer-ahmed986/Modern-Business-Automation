import React, { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";
import { Label } from "../../components/ui/label";
import { Separator } from "../../components/ui/separator";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../components/ui/select";
import { toast } from "sonner";
import settingsService from "../../services/settings.service";
import type { Settings } from "../../services/settings.service";
import authService from "../../services/auth.service";

const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  
  const user = authService.getCurrentUser();
  const isAdmin = user?.role === "admin";

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const data = await settingsService.getSettings();
        setSettings(data);
      } catch (error) {
        toast.error("Failed to load settings");
      } finally {
        setIsLoading(false);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!settings || !isAdmin) return;

    setIsSaving(true);
    try {
      await settingsService.updateSettings(settings);
      toast.success("Settings updated successfully");
    } catch (error) {
      toast.error("Failed to update settings");
    } finally {
      setIsSaving(false);
    }
  };

  const handleChange = (field: keyof Settings, value: string | number) => {
    if (!settings) return;
    setSettings({ ...settings, [field]: value });
  };

  if (isLoading) {
    return <div className="flex items-center justify-center h-full">Loading settings...</div>;
  }

  if (!settings) {
    return <div className="flex items-center justify-center h-full text-destructive">Error loading settings</div>;
  }

  return (
    <div className="container mx-auto py-10 space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">System Settings</h1>
          <p className="text-muted-foreground">Manage your business identity and system configuration.</p>
        </div>
      </div>
      
      <Separator />

      <form onSubmit={handleSave} className="grid gap-8 max-w-2xl">
        <Card className="glassmorphism-card border-white/20">
          <CardHeader>
            <CardTitle>Business Branding</CardTitle>
            <CardDescription>Configure how your business appears to users and on invoices.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="business_name">Business Name</Label>
              <Input
                id="business_name"
                value={settings.business_name}
                onChange={(e) => handleChange("business_name", e.target.value)}
                disabled={!isAdmin}
                placeholder="My Business"
              />
            </div>
            
            <div className="grid gap-2">
              <Label htmlFor="currency">Currency</Label>
              <Select
                disabled={!isAdmin}
                value={settings.currency}
                onValueChange={(value) => handleChange("currency", value)}
              >
                <SelectTrigger id="currency">
                  <SelectValue placeholder="Select currency" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="USD">USD ($)</SelectItem>
                  <SelectItem value="EUR">EUR (€)</SelectItem>
                  <SelectItem value="GBP">GBP (£)</SelectItem>
                  <SelectItem value="PKR">PKR (Rs.)</SelectItem>
                  <SelectItem value="INR">INR (₹)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Card className="glassmorphism-card border-white/20">
          <CardHeader>
            <CardTitle>Financial Settings</CardTitle>
            <CardDescription>Configure taxes and financial preferences.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="tax_rate">Default Tax Rate (%)</Label>
              <Input
                id="tax_rate"
                type="number"
                step="0.01"
                value={settings.tax_rate}
                onChange={(e) => handleChange("tax_rate", parseFloat(e.target.value))}
                disabled={!isAdmin}
                placeholder="0.00"
              />
            </div>
          </CardContent>
        </Card>

        {isAdmin && (
          <div className="flex justify-end">
            <Button type="submit" size="lg" disabled={isSaving}>
              {isSaving ? "Saving..." : "Save Settings"}
            </Button>
          </div>
        )}
      </form>
    </div>
  );
};

export default SettingsPage;
