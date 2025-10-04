export interface User {
  id: string;
  email: string;
  name: string;
  language: 'en' | 'ar';
  summary?: string;
  createdAt: Date;
}


export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials extends LoginCredentials {
  name: string;
  confirmPassword: string;
}


export interface AuthResponse {
  user: User
  accessToken: string;
  refreshToken: string
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}