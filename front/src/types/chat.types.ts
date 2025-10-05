export interface Message {
  id: string;
  chatId: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  language_code: string;
  typing?: boolean;
  model?: string;
}

export interface Chat {
  id: number;
  userId: number;
  title: string;
  messages: Message[];
  messages_count?: number;
  model: AIModel;
  created_at: Date;
  updated_at: Date;
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
  messages_count: number;
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

export type AIModel = 'DEEPSEEK' | 'Gemini' | 'GPT';
export type AIProvider = 'DEEPSEEK' | 'Gemini' | 'GPT';
export interface ChatState {
  chats: Chat[];
  currentChatId: number | null;
  isLoading: boolean;
  error: string | null;
}

export interface SendMessageRequest {
  conversation_id?: number;
  text: string;
  model?: AIModel;
  provider: AIProvider
}