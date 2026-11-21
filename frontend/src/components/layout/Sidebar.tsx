import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  Settings,
  Users,
  BarChart3,
  Database,
  BrainCircuit,
  Loader2,
  Truck,
  FileDown,
  History,
  ChevronsLeft,
  ChevronsRight,
  Boxes,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import authService from '@/services/auth.service';
import useBranding from '@/hooks/useBranding';
import { useFeatureFlags } from '@/hooks/useFeatureFlag';

interface SidebarItem {
  name: string;
  path: string;
  icon: React.ElementType;
  roles?: string[];
  feature?: string;
}

export const sidebarItems: SidebarItem[] = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, feature: 'dashboard' },
  { name: 'Inventory', path: '/inventory', icon: Package, roles: ['admin', 'manager'], feature: 'inventory' },
  { name: 'Billing', path: '/billing', icon: ShoppingCart, feature: 'billing' },
  { name: 'Sales History', path: '/sales', icon: History, feature: 'billing' },
  { name: 'Suppliers', path: '/suppliers', icon: Truck, roles: ['admin', 'manager'], feature: 'suppliers' },
  { name: 'Purchases', path: '/purchases/new', icon: FileDown, roles: ['admin', 'manager'], feature: 'purchases' },
  { name: 'Reports', path: '/reports', icon: BarChart3, roles: ['admin', 'manager'], feature: 'advanced_reports' },
  { name: 'Users', path: '/users', icon: Users, roles: ['admin'] },
  { name: 'Backup', path: '/backup', icon: Database, roles: ['admin'], feature: 'backup_restore' },
  { name: 'AI Insights', path: '/ai', icon: BrainCircuit, roles: ['admin'], feature: 'ai_assistant' },
  { name: 'Settings', path: '/settings', icon: Settings, roles: ['admin'] },
];

const COLLAPSE_KEY = 'mbas_sidebar_collapsed';

const Sidebar: React.FC = () => {
  const user = authService.getCurrentUser();
  const { businessName, isLoading } = useBranding();
  const featureFlags = useFeatureFlags();
  const [collapsed, setCollapsed] = useState(() => localStorage.getItem(COLLAPSE_KEY) === 'true');

  const toggleCollapsed = () => {
    setCollapsed((prev) => {
      const next = !prev;
      localStorage.setItem(COLLAPSE_KEY, String(next));
      return next;
    });
  };

  const filteredItems = sidebarItems.filter((item) => {
    if (item.roles && user && !item.roles.includes(user.role)) return false;
    if (item.feature && !featureFlags[item.feature]) return false;
    return true;
  });

  return (
    <aside
      className={cn(
        'flex flex-col h-full shrink-0 bg-card border-r border-border transition-[width] duration-200',
        collapsed ? 'w-[72px]' : 'w-64'
      )}
    >
      <div className={cn('flex items-center gap-2 h-16 px-4 border-b border-border', collapsed && 'justify-center px-0')}>
        {isLoading ? (
          <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
        ) : (
          <>
            <div className="flex items-center justify-center h-8 w-8 rounded-md bg-primary text-primary-foreground shrink-0">
              <Boxes className="h-4 w-4" />
            </div>
            {!collapsed && (
              <div className="min-w-0">
                <p className="text-sm font-semibold tracking-tight truncate">{businessName}</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-widest">Automation System</p>
              </div>
            )}
          </>
        )}
      </div>

      <nav className="flex-1 px-2 py-3 space-y-0.5 overflow-y-auto">
        {filteredItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            title={collapsed ? item.name : undefined}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                collapsed && 'justify-center px-0',
                isActive
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              )
            }
          >
            <item.icon className="h-[18px] w-[18px] shrink-0" />
            {!collapsed && <span className="truncate">{item.name}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="p-2 border-t border-border">
        <button
          onClick={toggleCollapsed}
          className={cn(
            'flex items-center gap-2 w-full px-3 py-2 text-sm text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors',
            collapsed && 'justify-center px-0'
          )}
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronsRight className="h-4 w-4" /> : <ChevronsLeft className="h-4 w-4" />}
          {!collapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
