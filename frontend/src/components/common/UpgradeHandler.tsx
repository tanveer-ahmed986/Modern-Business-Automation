/**
 * Global component that listens for upgrade-required events from the API
 * and displays the UpgradeModal accordingly.
 *
 * Add this component once in your App root.
 */

import { useEffect, useState } from 'react';
import { upgradeRequiredEvent } from '@/services/api';
import { UpgradeModal } from './UpgradeModal';
import { toast } from 'sonner';

export function UpgradeHandler() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalConfig, setModalConfig] = useState<{
    message?: string;
    requiredTier?: 'standard' | 'premium';
  }>({});

  useEffect(() => {
    const handleUpgradeRequired = (event: Event) => {
      const customEvent = event as CustomEvent;
      const { message, requiredTier } = customEvent.detail;

      setModalConfig({
        message,
        requiredTier,
      });
      setIsModalOpen(true);
    };

    const handleLicenseExpired = (event: Event) => {
      const customEvent = event as CustomEvent;
      const { message } = customEvent.detail;

      toast.error('License Expired', {
        description: message || 'Your license has expired. Please renew to continue using this feature.',
        duration: 5000,
      });
    };

    upgradeRequiredEvent.addEventListener('upgrade-required', handleUpgradeRequired);
    upgradeRequiredEvent.addEventListener('license-expired', handleLicenseExpired);

    return () => {
      upgradeRequiredEvent.removeEventListener('upgrade-required', handleUpgradeRequired);
      upgradeRequiredEvent.removeEventListener('license-expired', handleLicenseExpired);
    };
  }, []);

  return (
    <UpgradeModal
      isOpen={isModalOpen}
      onClose={() => setIsModalOpen(false)}
      message={modalConfig.message}
      requiredTier={modalConfig.requiredTier}
    />
  );
}

export default UpgradeHandler;
