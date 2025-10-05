export interface GetLastSummaryResponse {
  summary: string,
  last_updated: string
}
export interface GetSummaryResponse {
  summary: string,
  created_at: string
}

export interface GetUserSummariesSummaryResponse {
  results: GetSummaryResponse[]
}



export interface GetProfile {
  id: number;
  name: string;
  email: string;
  conversations_count: number;
  last_login: string;
  messages_count: number;
  created_at: Date;
  updated_at: Date;
}


export interface UpdateProfileDto {
  name?: string;
  email?: string;
}
