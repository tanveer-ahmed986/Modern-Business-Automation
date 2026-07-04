import { useEffect, useState } from 'react';
import { WifiOff, Wifi } from 'lucide-react';

/**
 * OfflineBanner - Shows a banner when the app goes offline
 *
 * Detects network status changes and displays a warning banner
 * when offline. Auto-hides when connection is restored.
 */
export const OfflineBanner = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [wasOffline, setWasOffline] = useState(false);
  const [showReconnected, setShowReconnected] = useState(false);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      if (wasOffline) {
        setShowReconnected(true);
        // Hide "reconnected" message after 3 seconds
        setTimeout(() => {
          setShowReconnected(false);
          setWasOffline(false);
        }, 3000);
      }
    };

    const handleOffline = () => {
      setIsOnline(false);
      setWasOffline(true);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [wasOffline]);

  if (!isOnline) {
    return (
      <div className="bg-amber-500 text-white p-2 text-center flex items-center justify-center gap-2 sticky top-0 z-50">
        <WifiOff className="h-4 w-4" />
        <span className="text-sm font-medium">
          You are offline. Some features may be unavailable.
        </span>
      </div>
    );
  }

  if (showReconnected) {
    return (
      <div className="bg-green-500 text-white p-2 text-center flex items-center justify-center gap-2 sticky top-0 z-50 animate-in fade-in slide-in-from-top">
        <Wifi className="h-4 w-4" />
        <span className="text-sm font-medium">
          Back online! All features restored.
        </span>
      </div>
    );
  }

  return null;
};
