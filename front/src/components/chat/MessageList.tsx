import React, { useEffect, useRef } from 'react';
import { useChat } from '../../context/ChatContext';
import { MessageItem } from './MessageItem';

export const MessageList: React.FC = () => {
  const { currentChat } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentChat?.messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-gray-50 flex flex-col">
      {currentChat?.messages.map(msg => (
        <MessageItem key={msg.id} message={msg} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};
