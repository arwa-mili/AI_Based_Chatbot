import React from 'react';
import { User, Bot } from 'lucide-react';
import { Message } from '../../types/chat.types';

interface MessageItemProps {
  message: Message;
}

export const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const rtlLanguages = ['ar', 'he', 'fa', 'ur'];
  const isRTL = rtlLanguages.includes(message.language_code || 'en');

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start space-x-2 max-w-[75%] ${isRTL ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-blue-600' : 'bg-gray-300'
        }`}>
          {isUser ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-gray-700" />}
        </div>

        {/* Message Bubble */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div
            className={`px-4 py-3 rounded-lg break-words ${
              isUser ? 'bg-blue-600 text-white rounded-br-none' : 'bg-gray-100 text-gray-900 rounded-bl-none'
            }`}
            style={{ direction: isRTL ? 'rtl' : 'ltr' }}
          >
            {/* Render HTML safely */}
            <div dangerouslySetInnerHTML={{ __html: message.content }} />
          </div>

          {/* Timestamp & model */}
          <div className="flex items-center space-x-2 mt-1 px-1">
            <span className="text-xs text-gray-500">
              {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
            {message.model && !isUser && (
              <span className="text-xs text-gray-400">• {message.model}</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
