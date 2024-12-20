import { Injectable } from "@angular/core";
import { TokenPayload } from "interfaces/auth.interface";
import { jwtDecode } from "jwt-decode";

@Injectable({
  providedIn: "root",
})
export class TokenService {
  private readonly TOKEN_KEY = "authToken";

  setToken(data: string): void {
    localStorage.setItem(this.TOKEN_KEY, data);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  clearToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  decodeToken(token: string): TokenPayload {
    return jwtDecode(token) as TokenPayload;
  }
}
