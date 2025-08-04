import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';

// Components
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';
import ChatInterface from './components/chat/ChatInterface';
import NewsDashboard from './components/news/NewsDashboard';
import StockAnalysis from './components/stocks/StockAnalysis';
import MarketOverview from './components/market/MarketOverview';
import Settings from './components/settings/Settings';
import LoadingSpinner from './components/common/LoadingSpinner';

// Hooks
import { useAuth } from './hooks/useAuth';
import { useTheme } from './hooks/useTheme';

// Styles
import './styles/globals.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { user, loading } = useAuth();
  const { theme, toggleTheme } = useTheme();

  if (loading) {
    return <LoadingSpinner size="lg" text="Loading application..." />;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className={`min-h-screen bg-black text-white ${theme}`}>
        <Router>
          <div className="flex h-screen">
            {/* Sidebar */}
            <Sidebar 
              isOpen={sidebarOpen} 
              onToggle={() => setSidebarOpen(!sidebarOpen)}
              user={user}
            />
            
            {/* Main Content */}
            <div className="flex-1 flex flex-col">
              {/* Header */}
              <Header 
                onMenuClick={() => setSidebarOpen(!sidebarOpen)}
                theme={theme}
                onThemeToggle={toggleTheme}
                user={user}
              />
              
              {/* Main Content Area */}
              <main className="flex-1 overflow-hidden">
                <AnimatePresence mode="wait">
                  <Routes>
                    <Route 
                      path="/" 
                      element={
                        <motion.div
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="h-full"
                        >
                          <ChatInterface />
                        </motion.div>
                      } 
                    />
                    <Route 
                      path="/news" 
                      element={
                        <motion.div
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="h-full"
                        >
                          <NewsDashboard />
                        </motion.div>
                      } 
                    />
                    <Route 
                      path="/stocks" 
                      element={
                        <motion.div
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="h-full"
                        >
                          <StockAnalysis />
                        </motion.div>
                      } 
                    />
                    <Route 
                      path="/market" 
                      element={
                        <motion.div
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="h-full"
                        >
                          <MarketOverview />
                        </motion.div>
                      } 
                    />
                    <Route 
                      path="/settings" 
                      element={
                        <motion.div
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="h-full"
                        >
                          <Settings />
                        </motion.div>
                      } 
                    />
                  </Routes>
                </AnimatePresence>
              </main>
            </div>
          </div>
        </Router>
        
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#1f2937',
              color: '#fff',
              border: '1px solid #374151',
            },
          }}
        />
      </div>
    </QueryClientProvider>
  );
}

export default App; 