export interface GetLastSummaryResponse {
  summary: string,
  last_updated: string
}


export interface GetProfile {
  id: number;
  name: string;
  email: string;
  created_at: Date;
  updated_at: Date;
}


export interface UpdateProfileDto {
  name?: string;
  email?: string;
}
