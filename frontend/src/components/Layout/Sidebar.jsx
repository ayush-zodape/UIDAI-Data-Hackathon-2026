import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Upload, BarChart3, MessageCircle } from 'lucide-react';
import useDataStore from '../../store/useDataStore';

const Sidebar = () => {
  const { isDataLoaded } = useDataStore();
  
  const navItems = [
    { path: '/', icon: Home, label: 'Home', always: true },
    { path: '/upload', icon: Upload, label: 'Upload Data', always: true },
    { path: '/dashboard', icon: BarChart3, label: 'Dashboard', requiresData: true },
    { path: '/chat', icon: MessageCircle, label: 'AI Assistant', requiresData: true },
  ];
  
  return (
    <aside className="w-64 bg-white shadow-lg min-h-[calc(100vh-80px)]">
      <nav className="p-4">
        <ul className="space-y-2">
          {navItems.map(({ path, icon: Icon, label, always, requiresData }) => {
            const isDisabled = requiresData && !isDataLoaded;
            
            return (
              <li key={path}>
                <NavLink
                  to={isDisabled ? '#' : path}
                  className={({ isActive }) =>
                    `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                      isDisabled
                        ? 'text-gray-400 cursor-not-allowed'
                        : isActive
                        ? 'bg-uidai-blue text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                  onClick={(e) => isDisabled && e.preventDefault()}
                >
                  <Icon size={20} />
                  <span>{label}</span>
                  {isDisabled && (
                    <span className="text-xs bg-gray-200 px-2 py-1 rounded">Upload First</span>
                  )}
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
