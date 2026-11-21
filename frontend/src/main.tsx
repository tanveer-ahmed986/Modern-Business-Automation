import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './index.css'
import App from './App.tsx'
import { registerSW } from 'virtual:pwa-register'

// Central server-state cache: replaces the hand-rolled TTL caches in the
// service modules. 30s staleTime absorbs tab-switch refetch storms; mutations
// invalidate their query keys so data is never stale after a write.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

// One-time cleanup: older service worker versions cached API responses in
// these runtime caches (stale business data served for up to 30 days).
// The new SW no longer caches API calls, but installed clients still carry
// the old cache storage — delete it so fresh data is always shown.
if ('caches' in window) {
  caches.delete('mbas-api-cache').catch(() => {})
  caches.delete('mbas-assets-cache').catch(() => {})
}

// Register Service Worker for PWA
const updateSW = registerSW({
  onNeedRefresh() {
    // Show update prompt to user
    if (confirm('New version available! Reload to update?')) {
      updateSW(true)
    }
  },
  onOfflineReady() {
    console.log('App ready to work offline')
  },
  onRegistered(registration) {
    console.log('Service Worker registered:', registration)
  },
  onRegisterError(error) {
    console.error('Service Worker registration error:', error)
  }
})

// Check for updates every hour
setInterval(() => {
  updateSW()
}, 60 * 60 * 1000)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
