import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const Layout: React.FC = () => {
  return (
    <div className="flex h-screen bg-slate-100 overflow-hidden font-sans antialiased text-slate-900">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8 lg:p-12 relative">
        {/* Subtle glassmorphism decorative elements */}
        <div className="absolute top-0 right-0 -z-10 w-96 h-96 bg-blue-500/5 blur-3xl rounded-full translate-x-1/2 -translate-y-1/2" />
        <div className="absolute bottom-0 left-0 -z-10 w-96 h-96 bg-emerald-500/5 blur-3xl rounded-full -translate-x-1/2 translate-y-1/2" />
        
        <div className="max-w-7xl mx-auto animate-in fade-in duration-700">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;
