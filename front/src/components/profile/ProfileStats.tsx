import React from 'react';
import { MessageSquare, Bot, Calendar } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

interface ProfileStatsProps {
  totalMessages: number;
  totalChats: number;
  lastActivity: string;
}

export const ProfileStats: React.FC<ProfileStatsProps> = ({ totalMessages, totalChats, lastActivity }) => {
  const { t, language } = useLanguage(); // assuming `language` gives 'ar', 'en', etc.

  // ✅ Format the date based on the language
  const formattedLastActivity = lastActivity
    ? new Date(lastActivity).toLocaleString(language === 'ar' ? 'ar-EG' : 'en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : 'N/A';

  const stats = [
    { icon: MessageSquare, label: t('profile.totalMessages'), value: totalMessages, color: 'blue' },
    { icon: Bot, label: t('profile.totalChats'), value: totalChats, color: 'purple' },
    { icon: Calendar, label: t('profile.lastActivity'), value: formattedLastActivity, color: 'pink' },
  ];

  const colorClasses: Record<string, { bg: string; text: string; border: string }> = {
    blue: { bg: 'bg-blue-50', text: 'text-blue-600', border: 'border-blue-200' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-600', border: 'border-purple-200' },
    pink: { bg: 'bg-pink-50', text: 'text-pink-600', border: 'border-pink-200' },
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-3">
        {t('profile.activityStatistics')}
      </label>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          const colors = colorClasses[stat.color];

          return (
            <div
              key={index}
              className={`${colors.bg} p-4 rounded-lg border ${colors.border}`}
              dir={language === 'ar' ? 'rtl' : 'ltr'}
            >
              <div className="flex items-center gap-2 mb-2">
                <Icon className={`w-5 h-5 ${colors.text}`} />
                <p className="text-sm text-gray-600">{stat.label}</p>
              </div>
              <p className={`text-2xl font-bold ${colors.text}`}>
                {stat.value}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
