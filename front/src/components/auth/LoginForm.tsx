import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { Input } from '../../components/common/Input';
import { Button } from '../../components/common/Button';
import { LoginCredentials } from '../../types/auth.types';

interface LoginFormProps {
  onSwitchToSignup: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToSignup }) => {
  const [credentials, setCredentials] = useState<LoginCredentials>({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<Partial<LoginCredentials>>({});
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();

  const validate = (): boolean => {
    const newErrors: Partial<LoginCredentials> = {};

    if (!credentials.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(credentials.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!credentials.password) {
      newErrors.password = 'Password is required';
    } else if (credentials.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsLoading(true);
    try {
      await login(credentials);
      navigate('/chat');
    } catch (error) {
      setErrors({ email: 'Invalid credentials' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        type="email"
        label={t('auth.email')}
        value={credentials.email}
        onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
        error={errors.email}
        placeholder="example@email.com"
      />

      <Input
        type="password"
        label={t('auth.password')}
        value={credentials.password}
        onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        error={errors.password}
        placeholder="••••••••"
      />

      <Button type="submit" className="w-full" isLoading={isLoading}>
        {t('auth.loginButton')}
      </Button>

      <p className="text-center text-sm text-gray-600">
        {t('auth.noAccount')}{' '}
        <button
          type="button"
          onClick={onSwitchToSignup}
          className="text-blue-600 font-semibold hover:underline"
        >
          {t('auth.signupButton')}
        </button>
      </p>
    </form>
  );
};
