import React, { useRef, useCallback } from 'react';
import { Plus, Download, Trash2, MessageSquare, Loader2 } from 'lucide-react';
import { useChat } from '../../context/ChatContext';
import { useLanguage } from '../../context/LanguageContext';
import { Button } from '../../components/common/Button';
import { AIModel } from '../../types/chat.types';

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
    hasMoreConversations 
  } = useChat();
  const { t, isRTL } = useLanguage();
  
  const observerTarget = useRef<HTMLDivElement>(null);

  // Infinite scroll observer
  const handleObserver = useCallback((entries: IntersectionObserverEntry[]) => {
    const [target] = entries;
    if (target.isIntersecting && hasMoreConversations && !isLoading) {
      loadMoreConversations();
    }
  }, [hasMoreConversations, isLoading, loadMoreConversations]);

  React.useEffect(() => {
    const element = observerTarget.current;
    if (!element) return;

    const observer = new IntersectionObserver(handleObserver, {
      root: null,
      rootMargin: '20px',
      threshold: 1.0
    });

    observer.observe(element);

    return () => {
      if (element) {
        observer.unobserve(element);
      }
    };
  }, [handleObserver]);

  const handleNewChat = async () => {
    if (currentChat && currentChat.messages.length === 0) {
      return;
    }
    
    await createNewChat('gpt4' as AIModel);
  };

  const isNewChatDisabled = currentChat !== null && currentChat.messages.length === 0;

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed md:relative inset-y-0 ${isRTL ? 'right-0' : 'left-0'} z-50 w-64 bg-gray-100 border-${isRTL ? 'l' : 'r'} border-gray-200 transform transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : isRTL ? 'translate-x-full md:translate-x-0' : '-translate-x-full md:translate-x-0'
        } flex flex-col h-full`}
      >
        <div className="p-4 flex-1 overflow-y-auto">
          <Button
            onClick={handleNewChat}
            className="w-full mb-4"
            icon={Plus}
            disabled={isNewChatDisabled || isLoading}
          >
            {t('chat.newChat')}
          </Button>

          {isNewChatDisabled && (
            <p className="text-xs text-amber-600 mb-3 text-center">
              {t('chat.startCurrentChat') || 'Start typing in the current chat first'}
            </p>
          )}

          <h3 className="font-semibold text-gray-700 mb-3">{t('chat.chatHistory')}</h3>

          {isLoading && chats.length === 0 ? (
            <div className="text-center py-8">
              <Loader2 className="w-8 h-8 mx-auto text-blue-500 animate-spin" />
            </div>
          ) : chats.length === 0 ? (
            <div className="text-center py-8">
              <MessageSquare className="w-12 h-12 mx-auto text-gray-400 mb-2" />
              <p className="text-sm text-gray-500">{t('chat.noChats')}</p>
            </div>
          ) : (
            <>
              <div className="space-y-2">
                {chats.map((chat) => (
                  <div
                    key={chat.id}
                    onClick={() => selectChat(chat.id)}
                    className={`p-3 rounded-lg cursor-pointer transition-all ${
                      currentChat?.id === chat.id
                        ? 'bg-blue-100 border border-blue-300'
                        : 'bg-white hover:bg-gray-200'
                    }`}
                  >
                    <div className="flex justify-between items-start mb-1">
                      <span className="text-sm font-medium truncate flex-1">{chat.title}</span>
                    </div>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{chat.messages?.length || 0} messages</span>
                      <div className="flex space-x-1">
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
                  </div>
                ))}
              </div>

              {/* Infinite scroll trigger */}
              <div ref={observerTarget} className="py-4 text-center">
                {hasMoreConversations && (
                  <Loader2 className="w-6 h-6 mx-auto text-blue-500 animate-spin" />
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
};