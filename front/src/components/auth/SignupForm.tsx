import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { Input } from '../../components/common/Input';
import { Button } from '../../components/common/Button';
import { SignupCredentials } from '../../types/auth.types';

interface SignupFormProps {
  onSwitchToLogin: () => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({ onSwitchToLogin }) => {
  const [credentials, setCredentials] = useState<SignupCredentials>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Partial<SignupCredentials>>({});
  const [isLoading, setIsLoading] = useState(false);

  const { signup } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();

  const validate = (): boolean => {
    const newErrors: Partial<SignupCredentials> = {};

    if (!credentials.name) {
      newErrors.name = 'Name is required';
    }

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

    if (credentials.password !== credentials.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsLoading(true);
    try {
      await signup(credentials);
      navigate('/chat');
    } catch (error) {
      setErrors({ email: 'Email already exists' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        type="text"
        label={t('auth.name')}
        value={credentials.name}
        onChange={(e) => setCredentials({ ...credentials, name: e.target.value })}
        error={errors.name}
        placeholder="John Doe"
      />

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

      <Input
        type="password"
        label={t('auth.confirmPassword')}
        value={credentials.confirmPassword}
        onChange={(e) => setCredentials({ ...credentials, confirmPassword: e.target.value })}
        error={errors.confirmPassword}
        placeholder="••••••••"
      />

      <Button type="submit" className="w-full" isLoading={isLoading}>
        {t('auth.signupButton')}
      </Button>

      <p className="text-center text-sm text-gray-600">
        {t('auth.haveAccount')}{' '}
        <button
          type="button"
          onClick={onSwitchToLogin}
          className="text-blue-600 font-semibold hover:underline"
        >
          {t('auth.loginButton')}
        </button>
      </p>
    </form>
  );
};
