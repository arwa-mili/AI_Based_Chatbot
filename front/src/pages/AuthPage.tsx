import { Navigate } from "react-router-dom";
import { AuthLayout } from "../components/auth/AuthLayout";
import { LoginForm } from "../components/auth/LoginForm";
import { SignupForm } from "../components/auth/SignupForm";
import { useLanguage } from "../context/LanguageContext";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";

export const AuthPage: React.FC = () => {
  const [mode, setMode] = useState<'login' | 'signup'>('login');
  const { isAuthenticated, isLoading } = useAuth();
  const { t } = useLanguage();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/chat" replace />;
  }

  return (
    <AuthLayout title={mode === 'login' ? t('auth.loginTitle') : t('auth.signupTitle')}>
      {mode === 'login' ? (
        <LoginForm onSwitchToSignup={() => setMode('signup')} />
      ) : (
        <SignupForm onSwitchToLogin={() => setMode('login')} />
      )}
    </AuthLayout>
  );
};
