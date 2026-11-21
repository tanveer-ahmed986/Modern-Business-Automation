import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';
import ProtectedRoute from './components/routing/ProtectedRoute';
import Layout from './components/layout/Layout';
import { Toaster } from './components/ui/sonner';
import CommandPalette from './components/layout/CommandPalette';
import { ThemeProvider } from './components/theme-provider';

// Lazy-load all page components so the initial bundle is small and
// navigating between sections doesn't re-download already-cached chunks.
const LoginPage = React.lazy(() => import('./features/auth/LoginPage'));
const ChangePasswordPage = React.lazy(() => import('./features/auth/ChangePasswordPage'));
const DashboardPage = React.lazy(() => import('./features/dashboard/DashboardPage'));
const SettingsPage = React.lazy(() => import('./features/settings/SettingsPage'));
const ProductList = React.lazy(() => import('./features/inventory/ProductList'));
const BillingPage = React.lazy(() => import('./features/billing/BillingPage'));
const SalesHistoryPage = React.lazy(() => import('./features/billing/SalesHistoryPage'));
const SupplierLedger = React.lazy(() => import('./features/suppliers/SupplierLedger'));
const PurchasePage = React.lazy(() => import('./features/purchases/PurchasePage'));
const ReportsPage = React.lazy(() => import('./features/reports/ReportsPage'));
const AIChatPanel = React.lazy(() => import('./features/ai/AIChatPanel'));
const AutomaticBackupPage = React.lazy(() => import('./features/settings/AutomaticBackupPage'));
const UsersPage = React.lazy(() => import('./features/users/UsersPage'));

const PageLoader = () => (
  <div className="flex items-center justify-center h-full min-h-[200px]">
    <Loader2 className="h-8 w-8 animate-spin text-primary" />
  </div>
);

const App: React.FC = () => {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
    <Router>
      <Toaster position="top-right" closeButton richColors />
      <CommandPalette />
      <Suspense fallback={<PageLoader />}>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected but outside the app Layout (forced first-run flow) */}
          <Route element={<ProtectedRoute />}>
            <Route path="/change-password" element={<ChangePasswordPage />} />
          </Route>

          {/* Protected Routes (Wrapped in Layout) */}
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/settings" element={<SettingsPage />} />

              {/* Placeholder routes for other modules */}
              <Route path="/inventory" element={<ProductList />} />
              <Route path="/billing" element={<BillingPage />} />
              <Route path="/sales" element={<SalesHistoryPage />} />
              <Route path="/suppliers" element={<SupplierLedger />} />
              <Route path="/purchases/new" element={<PurchasePage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/users" element={<UsersPage />} />
              <Route path="/backup" element={<AutomaticBackupPage />} />
              <Route path="/ai" element={<AIChatPanel />} />
            </Route>
          </Route>

          {/* Redirect root to dashboard or login */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* Catch-all route */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Suspense>
    </Router>
    </ThemeProvider>
  );
};

export default App;
