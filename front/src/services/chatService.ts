import { CreateChatDto, GetConversationsDto, GetConversationsResponse, GetMessagesResponse, SendMessageRequest } from '../types/chat.types';
import { ApiCommonResponse } from '../types/common.types';
import api from './api';

interface AIResponse {
  content: string;
  model: string;
}


// export const createConversation = async (body: CreateChatDto): Promise<ApiCommonResponse<undefined>> => {
//   return api.post<undefined>('/chat/conversation', body);
// };

export const getConversations = async (dto:GetConversationsDto) : Promise<ApiCommonResponse<GetConversationsResponse>> =>{
  return api.get<GetConversationsResponse>('/chat/conversation',
    dto, 
  );
};

export const getConversationMessages = async (conversationId: number,req: GetConversationsDto): Promise<ApiCommonResponse<GetMessagesResponse>> => {
  return api.get<GetMessagesResponse>(`/chat/conversations/${conversationId}/messages`,
    req
  );
};

export const sendMessage = async (request: SendMessageRequest) => {
  const response = await api.post<{ content: string; model: string ,conversation: {id: number,title_en?: string, title_ar?: string}}>('/chat/message', request);
  return response.data;
};

export const regenerateTitle = async (id: number) => {
  const response = await api.patch<{ title_en: string; title_ar: string }>(`/chat/conversations/${id}/title`);
  return response.data;
};

