import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './features/auth/LoginPage';
import DashboardPage from './features/dashboard/DashboardPage';
import SettingsPage from './features/settings/SettingsPage';
import ProductList from './features/inventory/ProductList';
import { BillingPage } from './features/billing/BillingPage';
import SupplierLedger from './features/suppliers/SupplierLedger';
import PurchasePage from './features/purchases/PurchasePage';
import ReportsPage from './features/reports/ReportsPage';
import AIChatPanel from './features/ai/AIChatPanel';
import AutomaticBackupPage from './features/settings/AutomaticBackupPage';
import UsersPage from './features/users/UsersPage';
import ProtectedRoute from './components/routing/ProtectedRoute';
import Layout from './components/layout/Layout';
import { Toaster } from './components/ui/sonner';
import CommandPalette from './components/layout/CommandPalette';

const App: React.FC = () => {
  return (
    <Router>
      <Toaster position="top-right" closeButton richColors />
      <CommandPalette />
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Routes (Wrapped in Layout) */}
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/settings" element={<SettingsPage />} />

            {/* Placeholder routes for other modules */}
            <Route path="/inventory" element={<ProductList />} />
            <Route path="/billing" element={<BillingPage />} />
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
    </Router>
  );
};

export default App;
