import React from 'react';
import { Button } from '../../../components/common/Button';
import { Plus } from 'lucide-react';
import { useLanguage } from '../../../context/LanguageContext';

interface SidebarHeaderProps {
  handleNewChat: () => void;
  isNewChatDisabled: boolean;
  isLoading: boolean;
}

export const SidebarHeader: React.FC<SidebarHeaderProps> = ({ handleNewChat, isNewChatDisabled, isLoading }) => {
  const { t } = useLanguage();
  return (
    <>
      <Button
        onClick={handleNewChat}
        className="w-full mb-4"
        icon={Plus}
        disabled={isNewChatDisabled || isLoading}
      >
        {t('chat.newChat')}
      </Button>
      <h3 className="font-semibold text-gray-700 mb-3">{t('chat.chatHistory')}</h3>
    </>
  );
};
