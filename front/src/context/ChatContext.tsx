import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Chat, Message, ChatState, AIModel, SendMessageRequest } from '../types/chat.types';
import * as chatService from '../services/chatService';
import { useAuth } from './AuthContext';

interface ChatContextType extends ChatState {
  createNewChat: (model: AIModel) => Promise<void>;
  sendMessage: (request: SendMessageRequest) => Promise<void>;
  selectChat: (chatId: number) => Promise<void>;
  exportChat: (chatId: number) => void;
  loadConversations: () => Promise<void>;
  loadMoreConversations: () => Promise<void>;
  currentChat: Chat | null;
  hasMoreConversations: boolean;
  stopTypingCallback?: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [state, setState] = useState<ChatState>({
    chats: [],
    currentChatId: null,
    isLoading: false,
    error: null,
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMoreConversations, setHasMoreConversations] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [fakeChatLock, setFakeChatLock] = useState(false); // prevents creating multiple new chats
  const pageSize = 15;

  useEffect(() => {
    if (user) loadConversations();
  }, [user]);

  const loadConversations = async () => {
    if (!user) return;
    setState(prev => ({ ...prev, isLoading: true }));
    setCurrentPage(1);

    try {
      const response = await chatService.getConversations({ pageNumber: 1, pageSize });

      const chats: Chat[] = response.data.items.map((conv: any) => ({
        id: conv.id,
        userId: user.id,
        title: conv.title,
        model: 'gpt4' as AIModel,
        messages: [],
        createdAt: new Date(conv.created_at),
        updatedAt: new Date(conv.updated_at),
      }));

      // Preserve new chat placeholder if exists
      const newChat = state.chats.find(c => c.id === 0);
      setState(prev => ({
        ...prev,
        chats: newChat ? [newChat, ...chats] : chats,
        isLoading: false,
      }));

      setHasMoreConversations(chats.length < (response.data.totalPages || 0));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load conversations',
      }));
    }
  };

  const loadMoreConversations = async () => {
    if (!user || isLoadingMore || !hasMoreConversations) return;
    setIsLoadingMore(true);
    const nextPage = currentPage + 1;

    try {
      const response = await chatService.getConversations({ pageNumber: nextPage, pageSize });

      const newChats: Chat[] = response.data.items.map((conv: any) => ({
        id: conv.id,
        userId: user.id,
        title: conv.title,
        model: 'gpt4' as AIModel,
        messages: [],
        createdAt: new Date(conv.created_at),
        updatedAt: new Date(conv.updated_at),
      }));

      const newChat = state.chats.find(c => c.id === 0);
      setState(prev => ({
        ...prev,
        chats: newChat ? [newChat, ...prev.chats.filter(c => c.id === 0), ...newChats] : [...prev.chats, ...newChats],
      }));

      setCurrentPage(nextPage);

      const totalItems = response.data.totalPages || 0;
      const totalLoaded = state.chats.length + newChats.length;
      setHasMoreConversations(totalLoaded < totalItems);
      setIsLoadingMore(false);
    } catch (error) {
      setIsLoadingMore(false);
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to load more conversations',
      }));
    }
  };

  const loadChatMessages = async (chatId: number) => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const response = await chatService.getConversationMessages(chatId, { pageNumber: 1, pageSize });

      const messages: Message[] = response.data.items.map((msg: any) => ({
        id: msg.id,
        chatId,
        language_code: msg.language_code,
        role: msg.sent_by.toLowerCase() === 'bot' ? 'assistant' : 'user',
        content: msg.text,
        timestamp: new Date(msg.created_at),
        model: msg.model_used,
      }));

      setState(prev => ({
        ...prev,
        chats: prev.chats.map(chat => (chat.id === chatId ? { ...chat, messages } : chat)),
        isLoading: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load messages',
      }));
    }
  };

  const createNewChat = async (model: AIModel) => {
    if (!user) return;

    if (fakeChatLock) {
      const existingNewChat = state.chats.find(chat => chat.id === 0);
      if (existingNewChat) setState(prev => ({ ...prev, currentChatId: 0 }));
      return;
    }

    const newChat: Chat = {
      id: 0,
      userId: user.id,
      title: 'New Chat',
      model,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setState(prev => ({
      ...prev,
      chats: [newChat, ...prev.chats],
      currentChatId: 0,
    }));

    setFakeChatLock(true);
  };

  const sendMessage = async (request: SendMessageRequest) => {
    if (state.currentChatId == null) return;

    let chatId = state.currentChatId;
    const isNewChat = chatId === 0;

    // Local user message
    const userMessage: Message = {
      id: Date.now().toString(),
      chatId,
      language_code: localStorage.getItem('language') || 'en',
      role: 'user',
      content: request.text,
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      chats: prev.chats.map(chat =>
        chat.id === chatId ? { ...chat, messages: [...chat.messages, userMessage] } : chat
      ),
    }));

    // AI placeholder
    const aiMessageId = `ai-${Date.now()}`;
    const aiMessage: Message = {
      id: aiMessageId,
      chatId,
      role: 'assistant',
      language_code: localStorage.getItem('language') || 'en',
      content: '',
      timestamp: new Date(),
      model: request.model,
      typing: true,
    };

    setState(prev => ({
      ...prev,
      chats: prev.chats.map(chat =>
        chat.id === chatId ? { ...chat, messages: [...chat.messages, aiMessage] } : chat
      ),
    }));

    try {
      const response = await chatService.sendMessage({
        ...request,
        conversation_id: isNewChat ? undefined : chatId,
      });

      const realChatId: number = response.conversation.id;

      // Replace placeholder ID with real ID
      if (isNewChat && realChatId != null) {
        setState(prev => ({
          ...prev,
          chats: prev.chats.map(chat => (chat.id === 0 ? { ...chat, id: realChatId } : chat)),
          currentChatId: realChatId,
          fakeChatLock: false,
        }));
        chatId = realChatId;
      }

      // Typing simulation
      const fullText = response.content;
      let index = 0;
      const interval = 20;
      const typingInterval = setInterval(() => {
        if (index <= fullText.length) {
          setState(prev => ({
            ...prev,
            chats: prev.chats.map(chat =>
              chat.id === chatId
                ? {
                    ...chat,
                    messages: chat.messages.map(msg =>
                      msg.id === aiMessageId ? { ...msg, content: fullText.slice(0, index), typing: true } : msg
                    ),
                  }
                : chat
            ),
          }));
          index++;
        } else {
          clearInterval(typingInterval);
          setState(prev => ({
            ...prev,
            chats: prev.chats.map(chat =>
              chat.id === chatId
                ? {
                    ...chat,
                    messages: chat.messages.map(msg =>
                      msg.id === aiMessageId ? { ...msg, content: fullText, typing: false } : msg
                    ),
                  }
                : chat
            ),
          }));
        }
      }, interval);

      setState(prev => ({ ...prev, stopTypingCallback: () => clearInterval(typingInterval) }));
    } catch (error) {
      if (isNewChat) setFakeChatLock(false);
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to send message',
      }));
    }
  };

  const selectChat = async (chatId: number) => {
    setState(prev => ({ ...prev, currentChatId: chatId }));
    const chat = state.chats.find(c => c.id === chatId);
    if (chat && chat.messages.length === 0) await loadChatMessages(chatId);
  };

  const exportChat = (chatId: number) => {
    const chat = state.chats.find(c => c.id === chatId);
    if (!chat) return;

    const content = chat.messages
      .map(msg => `[${msg.role.toUpperCase()}] ${new Date(msg.timestamp).toLocaleString()}\n${msg.content}`)
      .join('\n\n---\n\n');

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-${chat.id}-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const currentChat = state.chats.find(chat => chat.id === state.currentChatId) || null;

  return (
    <ChatContext.Provider
      value={{
        ...state,
        createNewChat,
        sendMessage,
        selectChat,
        exportChat,
        loadConversations,
        loadMoreConversations,
        currentChat,
        hasMoreConversations,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) throw new Error('useChat must be used within ChatProvider');
  return context;
};
