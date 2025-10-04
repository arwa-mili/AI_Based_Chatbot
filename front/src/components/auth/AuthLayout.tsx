import React from 'react';
import { useLanguage } from '../../context/LanguageContext';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title }) => {
  const { isRTL } = useLanguage();

  return (
    <div className={`min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center px-4 ${isRTL ? 'rtl' : 'ltr'}`}>
      <div className="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-center mb-6 text-gray-900">{title}</h2>
        {children}
      </div>
    </div>
  );
};