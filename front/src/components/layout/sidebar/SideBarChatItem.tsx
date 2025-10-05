import React from 'react';
import { Download, RefreshCcw, Loader2 } from 'lucide-react';
import { useLanguage } from '../../../context/LanguageContext';

export const SidebarChatItem = ({
  chat,
  isActive,
  selectChat,
  exportChat,
  regenerateConversationTitle,
  loadingTitleId
}: any) => {
  const { t } = useLanguage();

  return (
    <div
      onClick={() => selectChat(chat.id)}
      className={`p-3 rounded-lg cursor-pointer transition-all ${
        isActive ? 'bg-blue-100 border border-blue-300' : 'bg-white hover:bg-gray-200'
      }`}
    >
      <div className="flex justify-between items-start mb-1">
        <span className="text-sm font-medium break-words">{chat.title}</span>

        <button
          onClick={(e) => {
            e.stopPropagation();
            regenerateConversationTitle(chat.id);
          }}
          className="p-1 hover:bg-gray-300 rounded"
          title={t('chat.regenerateTitle') || 'Regenerate title'}
          disabled={loadingTitleId === chat.id}
        >
          {loadingTitleId === chat.id ? (
            <Loader2 className="w-3 h-3 animate-spin text-blue-500" />
          ) : (
            <RefreshCcw className="w-3 h-3 text-gray-600" />
          )}
        </button>
      </div>

      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>{chat.messages_count ?? 0} {t('chat.Messages')}</span>
        <button
          onClick={(e) => {
            e.stopPropagation();
            exportChat(chat.id);
          }}
          className="p-1 hover:bg-gray-300 rounded"
          title={t('chat.export')}
        >
          <Download className="w-3 h-3" />
        </button>
      </div>
    </div>
  );
};
