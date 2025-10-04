import React from 'react';
import { MessageSquare, Bot, Calendar } from 'lucide-react';
import { useChat } from '../../context/ChatContext';
import { useLanguage } from '../../context/LanguageContext';

export const ProfileStats: React.FC = () => {
  const { chats } = useChat();
  const { t } = useLanguage();

  const totalMessages = chats.reduce((acc, chat) => acc + chat.messages.length, 0);
  const totalChats = chats.length;
  const lastChatDate = chats.length > 0 
    ? new Date(Math.max(...chats.map(c => new Date(c.updatedAt).getTime())))
    : null;

  const stats = [
    {
      icon: MessageSquare,
      label: t('profile.totalMessages'),
      value: totalMessages,
      color: 'blue',
    },
    {
      icon: Bot,
      label: t('profile.totalChats'),
      value: totalChats,
      color: 'purple',
    },
    {
      icon: Calendar,
      label: 'Last Activity',
      value: lastChatDate ? lastChatDate.toLocaleDateString() : 'N/A',
      color: 'pink',
    },
  ];

  const colorClasses: Record<string, { bg: string; text: string }> = {
    blue: { bg: 'bg-blue-50', text: 'text-blue-600' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-600' },
    pink: { bg: 'bg-pink-50', text: 'text-pink-600' },
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-3">Activity Statistics</label>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          const colors = colorClasses[stat.color];

          return (
            <div key={index} className={`${colors.bg} p-4 rounded-lg border border-${stat.color}-200`}>
              <div className="flex items-center space-x-2 mb-2">
                <Icon className={`w-5 h-5 ${colors.text}`} />
                <p className="text-sm text-gray-600">{stat.label}</p>
              </div>
              <p className={`text-2xl font-bold ${colors.text}`}>{stat.value}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};