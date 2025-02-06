import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('/api/login', { email, password });
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        setIsAuthenticated(true);
      }
    } catch (error) {
      throw new Error('Invalid credentials');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}