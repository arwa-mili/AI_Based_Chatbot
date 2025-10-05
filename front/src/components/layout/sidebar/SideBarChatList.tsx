import React from 'react';
import { Loader2, MessageSquare } from 'lucide-react';
import { useLanguage } from '../../../context/LanguageContext';
import { SidebarChatItem } from './SideBarChatItem';

export const SidebarChatList = ({
  chats,
  currentChat,
  selectChat,
  exportChat,
  regenerateConversationTitle,
  loadingTitleId,
  isLoading,
  hasMoreConversations,
  observerTarget
}: any) => {
  const { t } = useLanguage();

  if (isLoading && chats.length === 0)
    return <div className="text-center py-8"><Loader2 className="w-8 h-8 mx-auto text-blue-500 animate-spin" /></div>;

  if (chats.length === 0)
    return (
      <div className="text-center py-8">
        <MessageSquare className="w-12 h-12 mx-auto text-gray-400 mb-2" />
        <p className="text-sm text-gray-500">{t('chat.noChats')}</p>
      </div>
    );

  return (
    <>
      <div className="space-y-2">
        {chats.map((chat: any) => (
          <SidebarChatItem
            key={chat.id}
            chat={chat}
            isActive={currentChat?.id === chat.id}
            selectChat={selectChat}
            exportChat={exportChat}
            regenerateConversationTitle={regenerateConversationTitle}
            loadingTitleId={loadingTitleId}
          />
        ))}
      </div>

      <div ref={observerTarget} className="py-4 text-center">
        {hasMoreConversations && (
          <Loader2 className="w-6 h-6 mx-auto text-blue-500 animate-spin" />
        )}
      </div>
    </>
  );
};
