import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ChevronRight, LogOut, Search, KeyRound } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import authService from '@/services/auth.service';
import { sidebarItems } from './Sidebar';

const openCommandPalette = () => window.dispatchEvent(new Event('mbas:open-command-palette'));

const useBreadcrumb = () => {
  const { pathname } = useLocation();
  const match = sidebarItems.find((item) => pathname.startsWith(item.path));
  if (match) return match.name;
  const segment = pathname.split('/').filter(Boolean)[0];
  return segment ? segment.charAt(0).toUpperCase() + segment.slice(1) : 'Dashboard';
};

const initials = (name: string) =>
  name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('') || 'U';

const TopBar: React.FC = () => {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();
  const breadcrumb = useBreadcrumb();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <header className="h-16 shrink-0 flex items-center justify-between gap-4 px-6 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex items-center gap-1.5 text-sm min-w-0">
        <span className="text-muted-foreground">Home</span>
        <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
        <span className="font-medium truncate">{breadcrumb}</span>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <Button
          variant="outline"
          size="sm"
          className="text-muted-foreground font-normal gap-2 hidden sm:flex"
          onClick={openCommandPalette}
        >
          <Search className="h-3.5 w-3.5" />
          Search
          <kbd className="pointer-events-none ml-2 inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
            Ctrl K
          </kbd>
        </Button>
        <Button variant="ghost" size="icon" className="sm:hidden" onClick={openCommandPalette} aria-label="Search">
          <Search className="h-4 w-4" />
        </Button>

        <ThemeToggle />

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="flex items-center gap-2 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
              <Avatar className="h-8 w-8">
                <AvatarFallback className="bg-primary/10 text-primary text-xs font-semibold">
                  {initials(user?.full_name || user?.username || 'U')}
                </AvatarFallback>
              </Avatar>
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>
              <p className="font-medium truncate">{user?.full_name || user?.username}</p>
              <p className="text-xs text-muted-foreground font-normal capitalize">{user?.role}</p>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => navigate('/change-password')}>
              <KeyRound className="mr-2 h-4 w-4" />
              Change Password
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout} className="text-destructive focus:text-destructive">
              <LogOut className="mr-2 h-4 w-4" />
              Sign Out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
};

export default TopBar;
