import React from 'react';
import { User } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { ProfileStats } from './ProfileStats';
import { AISummary } from './AISummary';
import { Card } from '../../components/common/Card';

export const ProfileView: React.FC = () => {
  const { user } = useAuth();
  const { t, language, isRTL } = useLanguage();

  if (!user) return null;

  return (
    <div className={`min-h-[calc(100vh-4rem)] bg-gray-50 py-8 ${isRTL ? 'rtl' : 'ltr'}`}>
      <div className="max-w-4xl mx-auto px-4">
        <Card>
          {/* Header */}
          <div className="flex items-center space-x-4 mb-8 pb-6 border-b border-gray-200">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center shadow-lg">
              <User className="w-10 h-10 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="text-3xl font-bold text-gray-900">{t('profile.title')}</h2>
              <p className="text-gray-600">{user.email}</p>
            </div>
          </div>

          {/* Profile Information */}
          <div className="space-y-6">
            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('auth.name')}
              </label>
              <div className="px-4 py-3 bg-gray-50 rounded-lg border border-gray-200">
                {user.name}
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('auth.email')}
              </label>
              <div className="px-4 py-3 bg-gray-50 rounded-lg border border-gray-200">
                {user.email}
              </div>
            </div>

            {/* Language */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('profile.language')}
              </label>
              <div className="px-4 py-3 bg-gray-50 rounded-lg border border-gray-200">
                {language === 'en' ? 'English' : 'العربية'}
              </div>
            </div>

            {/* Member Since */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('profile.memberSince')}
              </label>
              <div className="px-4 py-3 bg-gray-50 rounded-lg border border-gray-200">
                {new Date(user.createdAt).toLocaleDateString(language === 'en' ? 'en-US' : 'ar-SA', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </div>
            </div>

            {/* AI Summary */}
            <AISummary summary={user.summary} />

            {/* Stats */}
            <ProfileStats />
          </div>
        </Card>
      </div>
    </div>
  );
};