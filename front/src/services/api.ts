import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { ApiCommonResponse } from '../types/common.types';
import { toast } from 'react-toastify';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ApiService {
  private api: AxiosInstance;
  private isRefreshing = false;
  private failedQueue: { resolve: (value?: unknown) => void; reject: (error: any) => void; config: InternalAxiosRequestConfig }[] = [];

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
          config.headers = config.headers ?? {};
          (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
        }

        const languageCode = localStorage.getItem('language') || 'en';
        config.headers = config.headers ?? {};
        config.params = {
          ...config.params,
          language_code: languageCode,
        };

        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        const res: ApiCommonResponse<any> = response.data;

        if (res.success === false) {
          toast.error(res.error || 'Something went wrong!');
        } else if (res.success === true && res.info) {
          const method = response.config.method?.toLowerCase();
          if (method && method !== 'get') {
            toast.success(res.info);
          }
        }

        return response;
      },
      async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

        if (
          error.response?.status === 401 &&
          !originalRequest._retry &&
          !originalRequest.url?.includes('/auth/login/') &&
          !originalRequest.url?.includes('/auth/register/')
        ) {
          if (this.isRefreshing) {
            return new Promise((resolve, reject) => {
              this.failedQueue.push({ resolve, reject, config: originalRequest });
            });
          }

          originalRequest._retry = true;
          this.isRefreshing = true;

          const refreshToken = localStorage.getItem('refreshToken');
          if (!refreshToken) {
            this.logout();
            return Promise.reject(error);
          }

          try {
            const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, { refreshToken });
            const { accessToken, refreshToken: newRefreshToken } = response.data.data;
            console.log('Token refreshed:', accessToken, newRefreshToken);

            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', newRefreshToken);

            this.failedQueue.forEach((req) => {
              req.config.headers = req.config.headers ?? {};
              (req.config.headers as Record<string, string>)['Authorization'] = `Bearer ${accessToken}`;
              this.api(req.config)
                .then(req.resolve)
                .catch(req.reject);
            });
            this.failedQueue = [];

            // Retry original request
            originalRequest.headers = originalRequest.headers ?? {};
            (originalRequest.headers as Record<string, string>)['Authorization'] = `Bearer ${accessToken}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            this.failedQueue.forEach((req) => req.reject(refreshError));
            this.failedQueue = [];
            this.logout();
            return Promise.reject(refreshError);
          } finally {
            this.isRefreshing = false;
          }
        }

        // Handle other errors
        const message =
          (error.response?.data as any)?.error || error.message || 'An unexpected error occurred';
        toast.error(message);

        return Promise.reject(error);
      }
    );
  }

  private logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    window.location.href = '/auth/login';
  }

  public async get<T>(url: string, params?: any): Promise<ApiCommonResponse<T>> {
    const response = await this.api.get<ApiCommonResponse<T>>(url, { params });
    return response.data;
  }

  public async post<T>(url: string, data?: any): Promise<ApiCommonResponse<T>> {
    const response = await this.api.post<ApiCommonResponse<T>>(url, data);
    return response.data;
  }

  public async put<T>(url: string, data?: any): Promise<ApiCommonResponse<T>> {
    const response = await this.api.put<ApiCommonResponse<T>>(url, data);
    return response.data;
  }

  public async delete<T>(url: string): Promise<ApiCommonResponse<T>> {
    const response = await this.api.delete<ApiCommonResponse<T>>(url);
    return response.data;
  }
}

export default new ApiService();
