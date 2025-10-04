import { LoginCredentials, SignupCredentials, AuthResponse } from '../types/auth.types';
import api from './api';
import { ApiCommonResponse } from '../types/common.types';

export const login = async (credentials: LoginCredentials): Promise<ApiCommonResponse<AuthResponse>> => {

  return api.post<AuthResponse>('/auth/login/', credentials);
};

export const signup = async (credentials: SignupCredentials): Promise<ApiCommonResponse<AuthResponse>> => {
  return api.post<AuthResponse>('/auth/register/', credentials);
};

export const logout = async (): Promise<void> => {
  // return api.post('/auth/logout');
};