export interface IUser {
  id?: string;
  email: string;
  password: string;
  username: string;
  created_at?: Date;
  isActive?: boolean;
}
