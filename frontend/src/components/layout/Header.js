import React from 'react';
import { Menu, Moon, Sun, User } from 'lucide-react';

const Header = ({ onMenuClick, theme, onThemeToggle, user }) => {
  return (
    <header className="bg-gray-900 border-b border-gray-700 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onMenuClick}
            className="p-2 text-gray-400 hover:text-white transition-colors lg:hidden"
          >
            <Menu className="w-5 h-5" />
          </button>
          <h1 className="text-xl font-semibold text-white">
            Finance AI Assistant
          </h1>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={onThemeToggle}
            className="p-2 text-gray-400 hover:text-white transition-colors"
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
          
          {user && (
            <div className="flex items-center space-x-2">
              <User className="w-5 h-5 text-gray-400" />
              <span className="text-sm text-gray-300">
                {user.name}
              </span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header; 