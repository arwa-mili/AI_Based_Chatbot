export interface Message {
  id: string;
  chatId: string | number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  language_code: string;
  typing?: boolean;
  model?: string;
}

export interface Chat {
  id: string;
  userId: string;
  title: string;
  messages: Message[];
  model: AIModel;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateChatDto {
  userId: string;
}

export interface GetConversationsDto {
  pageNumber: number;
  pageSize: number;
}

export interface ConversationItem {
  id: string;
  title: string;
}

export interface MessageItem {
  id: string
  text: string
  sent_by: 'USER' | 'BOT'
  created_at: string
  model_used: string
  
}

export interface GetConversationsResponse {
  items: ConversationItem[];
  totalPages: number;
  pageNumber: number;
  pageSize: number;
}

export interface GetMessagesResponse {
  items: MessageItem[];
  totalPages: number;
  pageNumber: number;
  pageSize: number;
}

export type AIModel = 'gpt4' | 'claude' | 'deepseek';
export type AIProvider = 'DeepSeek' | 'Gemini' | 'OpenAi';
export interface ChatState {
  chats: Chat[];
  currentChatId: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface SendMessageRequest {
  conversation_id?: number | string;
  text: string;
  model?: AIModel;
  provider: AIProvider
}