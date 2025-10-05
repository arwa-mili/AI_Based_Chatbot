import { CreateChatDto, GetConversationsDto, GetConversationsResponse, GetMessagesResponse, SendMessageRequest } from '../types/chat.types';
import { ApiCommonResponse } from '../types/common.types';
import { GetLastSummaryResponse, GetProfile, UpdateProfileDto } from '../types/profile.types';
import api from './api';

interface AIResponse {
  content: string;
  model: string;
}




export const getUserSummary = async () : Promise<ApiCommonResponse<GetLastSummaryResponse>> =>{
  return api.get<GetLastSummaryResponse>('/chat/user-summary'  );
};

export const getProfileInfo = async (): Promise<ApiCommonResponse<GetProfile>> => {
  return api.get<GetProfile>(`/auth/profile`  );
};

export const setProfileInfo = async (req: UpdateProfileDto): Promise<ApiCommonResponse<undefined>> => {
    return api.put<undefined>(`/auth/profile` ,req );
  };