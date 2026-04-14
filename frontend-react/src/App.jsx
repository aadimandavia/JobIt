import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Analytics } from '@vercel/analytics/react';
import { AuthProvider, useAuth } from './hooks/useAuth';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading-screen"><div className="loading-spinner"></div><p>Loading...</p></div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function PublicRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading-screen"><div className="loading-spinner"></div><p>Loading...</p></div>;
  if (user) return <Navigate to="/dashboard" replace />;
  return children;
}

function TokenGrabber() {
  const { checkAuth } = useAuth();
  
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    if (token) {
      localStorage.setItem('access_token', token);
      // Clean URL to remove token from history
      window.history.replaceState({}, document.title, window.location.pathname);
      checkAuth();
    }
  }, [checkAuth]);
  
  return null;
}

function App() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <AuthProvider>
      <TokenGrabber />
      <BrowserRouter>
        <div className="bg-mesh"></div>
        <div className="content">
          <Routes>
            <Route path="/login" element={
              <PublicRoute>
                <LoginPage theme={theme} toggleTheme={toggleTheme} />
              </PublicRoute>
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <DashboardPage theme={theme} toggleTheme={toggleTheme} />
              </ProtectedRoute>
            } />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </div>
      </BrowserRouter>
      <Analytics />
    </AuthProvider>
  );
}

export default App;
