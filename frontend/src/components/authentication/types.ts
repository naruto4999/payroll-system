export interface AccountResponse {
    user: {
      id: string;
      username: string;
      is_active: boolean;
    };
    access: string;
    refresh: string;
  }