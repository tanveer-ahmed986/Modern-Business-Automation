/**
 * Modal displayed when a user attempts to access a feature that requires
 * a higher license tier (Standard or Premium).
 */

import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Lock, Sparkles, TrendingUp } from "lucide-react";

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  featureName?: string;
  requiredTier?: "standard" | "premium";
  message?: string;
}

export function UpgradeModal({
  isOpen,
  onClose,
  featureName = "this feature",
  requiredTier = "standard",
  message,
}: UpgradeModalProps) {
  const tierName = requiredTier.charAt(0).toUpperCase() + requiredTier.slice(1);
  const icon = requiredTier === "premium" ? <Sparkles className="h-12 w-12 text-yellow-500" /> : <TrendingUp className="h-12 w-12 text-blue-500" />;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <div className="flex justify-center mb-4">
            {icon}
          </div>
          <DialogTitle className="text-center">
            Upgrade to {tierName} Required
          </DialogTitle>
          <DialogDescription className="text-center">
            {message || `Access to ${featureName} requires the ${tierName} package.`}
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          <div className="bg-muted rounded-lg p-4">
            <h4 className="font-semibold mb-2 flex items-center gap-2">
              <Lock className="h-4 w-4" />
              {tierName} Features Include:
            </h4>
            <ul className="space-y-1 text-sm text-muted-foreground ml-6">
              {requiredTier === "standard" && (
                <>
                  <li>• Suppliers & Purchase Management</li>
                  <li>• Advanced Reports (Monthly, Product-wise)</li>
                  <li>• Backup & Restore</li>
                  <li>• All Basic Features</li>
                </>
              )}
              {requiredTier === "premium" && (
                <>
                  <li>• AI Sales Forecasting</li>
                  <li>• AI Natural Language Queries</li>
                  <li>• Profit & Loss Reports</li>
                  <li>• All Standard Features</li>
                </>
              )}
            </ul>
          </div>
        </div>

        <DialogFooter className="flex-col sm:flex-row gap-2">
          <Button variant="outline" onClick={onClose} className="w-full sm:w-auto">
            Maybe Later
          </Button>
          <Button
            onClick={() => {
              // In a real application, this would open contact form or pricing page
              window.open("mailto:sales@mbas.example.com?subject=Upgrade%20to%20" + tierName, "_blank");
              onClose();
            }}
            className="w-full sm:w-auto"
          >
            Contact Sales
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default UpgradeModal;
