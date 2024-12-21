export interface Credentials {
  email: string;
  password: string;
}

export interface ILogin extends Credentials {}

export interface IRegister extends Credentials {
  username: string;
}

export interface AuthResponse {
  accessToken: string;
  user: {
    id: string;
    email: string;
  };
}

export interface TokenPayload {
  email: string;
  iat: number;
  exp: number;
  sub: string;
}
