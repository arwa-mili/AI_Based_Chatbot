import React, { useRef, useCallback, useEffect } from 'react';
import { useChat } from '../../../context/ChatContext';
import { useLanguage } from '../../../context/LanguageContext';
import { SidebarHeader } from './SideBarHeader';
import { SidebarChatList } from './SideBarChatList';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { 
    chats, 
    currentChat, 
    createNewChat, 
    selectChat, 
    exportChat, 
    isLoading,
    loadMoreConversations,
    hasMoreConversations,
    regenerateConversationTitle,   
    loadingTitleId
  } = useChat();

  const { t, isRTL } = useLanguage();
  const observerTarget = useRef<HTMLDivElement>(null);

  const handleObserver = useCallback((entries: IntersectionObserverEntry[]) => {
    const [target] = entries;
    if (target.isIntersecting && hasMoreConversations && !isLoading) {
      loadMoreConversations();
    }
  }, [hasMoreConversations, isLoading, loadMoreConversations]);

  useEffect(() => {
    const element = observerTarget.current;
    if (!element) return;
    const observer = new IntersectionObserver(handleObserver, { root: null, rootMargin: '20px', threshold: 1.0 });
    observer.observe(element);
    return () => observer.unobserve(element);
  }, [handleObserver]);

  const handleNewChat = async () => {
    if (currentChat && currentChat.messages.length === 0) return;
    await createNewChat('GPT');
  };

  const isNewChatDisabled = currentChat !== null && currentChat.messages.length === 0;

  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden" onClick={onClose} />
      )}

      <div
        className={`fixed md:relative inset-y-0 ${isRTL ? 'right-0' : 'left-0'} z-50 bg-gray-100 border-${isRTL ? 'l' : 'r'} border-gray-200 transform transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : isRTL ? 'translate-x-full md:translate-x-0' : '-translate-x-full md:translate-x-0'
        } flex flex-col h-full resize-x overflow-auto min-w-[16rem] max-w-[22rem]`}
        style={{ width: isRTL ? '18rem' : '17rem' }}
      >
        <div className="p-4 flex-1 overflow-y-auto">
          <SidebarHeader 
            handleNewChat={handleNewChat} 
            isNewChatDisabled={isNewChatDisabled} 
            isLoading={isLoading} 
          />
          <SidebarChatList
            chats={chats}
            currentChat={currentChat}
            selectChat={selectChat}
            exportChat={exportChat}
            regenerateConversationTitle={regenerateConversationTitle}
            loadingTitleId={loadingTitleId}
            isLoading={isLoading}
            hasMoreConversations={hasMoreConversations}
            observerTarget={observerTarget}
          />
        </div>
      </div>
    </>
  );
};
