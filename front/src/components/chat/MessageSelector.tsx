import React, { useRef, useEffect } from 'react';
import { Bot } from 'lucide-react';
import { MessageItem } from './MessageItem';
import { useChat } from '../../context/ChatContext';
import { useLanguage } from '../../context/LanguageContext';
import { LoadingSpinner } from '../../components/common/LoadingSpinner';

export const MessageList: React.FC = () => {
  const { currentChat, isLoading } = useChat();
  const { t } = useLanguage();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentChat?.messages, isLoading]);

  if (!currentChat) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-400">
        <div className="text-center">
          <Bot className="w-16 h-16 mx-auto mb-4 opacity-50" />
          <p className="text-lg">{t('chat.typeMessage')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {currentChat.messages.length === 0 ? (
        <div className="h-full flex items-center justify-center text-gray-400">
          <div className="text-center">
            <Bot className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg">{t('chat.typeMessage')}</p>
          </div>
        </div>
      ) : (
        <>
          {currentChat.messages.map((message) => (
            <MessageItem key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 p-4 rounded-lg flex items-center gap-2">
                <LoadingSpinner size="sm" />
                <span className="text-gray-600">{t('chat.thinking')}</span>
              </div>
            </div>
          )}
        </>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};