import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  Settings, 
  LogOut, 
  Users, 
  BarChart3,
  Database,
  BrainCircuit,
  Loader2,
  Truck,
  FileDown
} from 'lucide-react';
import { cn } from '@/lib/utils';
import authService from '@/services/auth.service';
import { Button } from '@/components/ui/button';
import useBranding from '@/hooks/useBranding';
import { useFeatureFlags } from '@/hooks/useFeatureFlag';

interface SidebarItem {
  name: string;
  path: string;
  icon: React.ElementType;
  roles?: string[];
  feature?: string;
}

const sidebarItems: SidebarItem[] = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, feature: 'dashboard' },
  { name: 'Inventory', path: '/inventory', icon: Package, roles: ['admin', 'manager'], feature: 'inventory' },
  { name: 'Billing', path: '/billing', icon: ShoppingCart, feature: 'billing' },
  { name: 'Suppliers', path: '/suppliers', icon: Truck, roles: ['admin', 'manager'], feature: 'suppliers' },
  { name: 'Purchases', path: '/purchases/new', icon: FileDown, roles: ['admin', 'manager'], feature: 'purchases' },
  { name: 'Reports', path: '/reports', icon: BarChart3, roles: ['admin', 'manager'], feature: 'advanced_reports' },
  { name: 'Users', path: '/users', icon: Users, roles: ['admin'] },
  { name: 'Backup', path: '/backup', icon: Database, roles: ['admin'], feature: 'backup_restore' },
  { name: 'AI Insights', path: '/ai', icon: BrainCircuit, roles: ['admin'], feature: 'ai_assistant' },
  { name: 'Settings', path: '/settings', icon: Settings, roles: ['admin'] },
];

const Sidebar: React.FC = () => {
  const user = authService.getCurrentUser();
  const navigate = useNavigate();
  const { businessName, isLoading } = useBranding();
  const featureFlags = useFeatureFlags();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const filteredItems = sidebarItems.filter(item => {
    // Check role-based access
    if (item.roles && user && !item.roles.includes(user.role)) return false;

    // Check feature flag (if specified)
    if (item.feature && !featureFlags[item.feature]) return false;

    return true;
  });

  return (
    <div className="flex flex-col h-full w-64 bg-slate-900 text-white shadow-xl">
      <div className="p-6">
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <Loader2 className="h-6 w-6 animate-spin text-blue-400" />
            <span className="text-xl font-bold tracking-tight text-slate-400">Loading...</span>
          </div>
        ) : (
          <>
            <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              {businessName}
            </h1>
            <p className="text-xs text-slate-400 mt-1 uppercase tracking-widest font-semibold">
              Automation System
            </p>
          </>
        )}
      </div>

      <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
        {filteredItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                "flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 group",
                isActive 
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-900/20" 
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              )
            }
          >
            <item.icon className={cn(
              "mr-3 h-5 w-5 transition-colors",
              "group-hover:text-blue-400"
            )} />
            {item.name}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center px-4 py-3 mb-4 rounded-lg bg-slate-800/50">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.full_name || user?.username}</p>
            <p className="text-xs text-slate-400 truncate capitalize">{user?.role}</p>
          </div>
        </div>
        <Button 
          variant="ghost" 
          className="w-full justify-start text-slate-400 hover:text-white hover:bg-slate-800"
          onClick={handleLogout}
        >
          <LogOut className="mr-3 h-5 w-5" />
          Sign Out
        </Button>
      </div>
    </div>
  );
};

export default Sidebar;
