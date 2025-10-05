import React, { useState } from 'react';
import { Menu } from 'lucide-react';
import { Sidebar } from '../../components/layout/Sidebar';
import { ModelSelector } from './ModelSelector';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { useChat } from '../../context/ChatContext';
import { useLanguage } from '../../context/LanguageContext';
import { AIModel } from '../../types/chat.types';

export const ChatInterface: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedModel, setSelectedModel] = useState<AIModel>('GPT');
  const { currentChat, isLoading } = useChat();
  const { isRTL } = useLanguage();

  return (
    <div className={`flex h-[calc(100vh-4rem)] ${isRTL ? 'rtl' : 'ltr'}`}>
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="flex-1 flex flex-col bg-white">
        {/* Header */}
        <div className="border-b border-gray-200 p-4 flex items-center justify-between bg-gray-50">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-gray-200 rounded-lg transition"
          >
            <Menu className="w-5 h-5" />
          </button>

          <ModelSelector selectedModel={selectedModel} onSelectModel={setSelectedModel} />
        </div>

        {/* Messages */}
        <MessageList />

        {/* Input */}
        <ChatInput selectedModel={selectedModel} disabled={!currentChat || isLoading} />
      </div>
    </div>
  );
};