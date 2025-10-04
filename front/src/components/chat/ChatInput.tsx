import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { useChat } from '../../context/ChatContext';
import { useLanguage } from '../../context/LanguageContext';
import { Button } from '../../components/common/Button';
import { AIModel } from '../../types/chat.types';

interface ChatInputProps {
  selectedModel: AIModel;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ selectedModel, disabled }) => {
  const [message, setMessage] = useState('');
  const { currentChat, sendMessage, isLoading } = useChat();
  const { t, isRTL } = useLanguage();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [message]);

  const handleSend = async () => {
    if (!message.trim() || !currentChat || disabled || isLoading) return;

    const messageContent = message.trim();
    setMessage('');

    await sendMessage({
      conversation_id: currentChat.id,
      text: messageContent,
      provider: "Gemini",
      model: selectedModel,
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-200 p-4 bg-gray-50">
      <div className="flex items-end space-x-2">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={t('chat.typeMessage')}
          disabled={disabled || isLoading}
          className={`flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none max-h-32 ${
            isRTL ? 'text-right' : 'text-left'
          }`}
          rows={1}
        />
        <Button
          onClick={handleSend}
          disabled={!message.trim() || disabled || isLoading}
          icon={Send}
          className="flex-shrink-0"
        >
          {t('chat.send')}
        </Button>
      </div>
    </div>
  );
};
