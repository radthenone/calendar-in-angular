import { IUser } from 'interfaces/users.interface';

export class User implements IUser {
  id?: string;
  email: string;
  password: string;
  username: string;
  created_at: Date;
  isActive: boolean;

  constructor(user: IUser) {
    this.id = user.id;
    this.email = user.email;
    this.password = user.password;
    this.username = user.username;
    this.created_at = user.created_at ?? new Date();
    this.isActive = user.isActive ?? false;
  }
}

export class UserSubject {
  id: string;
  email: string;
  _token: string;
  _tokenExpirationDate: Date;
  constructor(
    id: string,
    email: string,
    _token: string,
    _tokenExpirationDate: Date,
  ) {
    this.id = id;
    this.email = email;
    this._token = _token;
    this._tokenExpirationDate = _tokenExpirationDate;
  }

  get token(): string | null {
    if (!this._tokenExpirationDate || new Date() > this._tokenExpirationDate) {
      return null;
    }
    return this._token;
  }
}
