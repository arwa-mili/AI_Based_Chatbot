import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthState, LoginCredentials, SignupCredentials } from '../types/auth.types';
import * as authService from '../services/authService';

interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  signup: (credentials: SignupCredentials) => Promise<void>;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    isLoading: true, // wait for initialization
  });

  useEffect(() => {
    const initAuth = () => {
      const token = localStorage.getItem('accessToken');
      const refreshToken = localStorage.getItem('refreshToken');
      const userStr = localStorage.getItem('user');

      if (token && userStr) {
        try {
          const user = JSON.parse(userStr);
          setState({
            user,
            accessToken: token,
            refreshToken,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          console.error('Failed to parse stored user:', error);
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          localStorage.removeItem('user');
          setState({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      } else {
        setState({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    const { user, accessToken, refreshToken } = (await authService.login(credentials)).data;
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    localStorage.setItem('user', JSON.stringify(user));
    setState({ user, accessToken, refreshToken, isAuthenticated: true, isLoading: false });
  };

  const signup = async (credentials: SignupCredentials) => {
    const { user, accessToken, refreshToken } = (await authService.signup(credentials)).data;
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    localStorage.setItem('user', JSON.stringify(user));
    setState({ user, accessToken, refreshToken, isAuthenticated: true, isLoading: false });
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    localStorage.removeItem('chats');
    setState({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false, isLoading: false });
  };

  const updateUser = (updatedFields: Partial<User>) => {
    if (state.user) {
      const updatedUser = { ...state.user, ...updatedFields };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      setState({ ...state, user: updatedUser });
    }
  };

  return (
    <AuthContext.Provider value={{ ...state, login, signup, logout, updateUser }}>
      {state.isLoading ? <div>Loading...</div> : children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
