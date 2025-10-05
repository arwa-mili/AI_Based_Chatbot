export interface GetLastSummaryResponse {
  summary: string,
  last_updated: string
}


export interface GetProfile {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}


export interface UpdateProfileDto {
  name?: string;
  email?: string;
}
