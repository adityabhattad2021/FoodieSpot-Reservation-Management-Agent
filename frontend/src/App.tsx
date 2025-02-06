import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChatPage } from './pages/ChatPage';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { LandingPage } from './pages/LandingPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/dashboard/*"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;