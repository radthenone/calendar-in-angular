import { Injectable, Signal } from "@angular/core";
import { BehaviorSubject, mergeMap, Observable, tap } from "rxjs";
import { environment } from "environment";
import {
  AuthResponse,
  ILogin,
  IRegister,
  TokenPayload,
} from "interfaces/auth.interface";
import { HttpClient } from "@angular/common/http";
import { map } from "rxjs/operators";
import { User, UserSubject } from "models/users.model";
import { Router } from "@angular/router";
import { toSignal } from "@angular/core/rxjs-interop";
import { TokenService } from "./token.service";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private userSubject$ = new BehaviorSubject<UserSubject | null>(null);
  private isAuthenticatedSubject$ = new BehaviorSubject<boolean>(false);
  private tokenExpirationTimer: any;

  getUser: Signal<UserSubject | null> = toSignal(
    this.userSubject$.asObservable(),
    {
      initialValue: null,
    },
  );
  isAuthenticated: Signal<boolean> = toSignal(
    this.isAuthenticatedSubject$.asObservable(),
    { initialValue: false },
  );

  constructor(
    private http: HttpClient,
    private router: Router,
    private tokenService: TokenService,
  ) {
    this.initializeUser();
  }

  private initializeUser(): void {
    const user: UserSubject | null = this.accountUser;
    if (user) {
      this.userSubject$.next(user);
      this.isAuthenticatedSubject$.next(true);
    } else {
      this.userSubject$.next(null);
      this.isAuthenticatedSubject$.next(false);
    }
  }

  public get accountUser(): UserSubject | null {
    const token = this.tokenService.getToken();
    if (token) {
      return JSON.parse(token) as UserSubject;
    }
    return null;
  }

  private handleAuthentication(payload: TokenPayload, token: string): void {
    const expirationDate = new Date(payload.exp * 1000);
    const user = new UserSubject(
      payload.sub,
      payload.email,
      token,
      expirationDate,
    );
    this.tokenService.setToken(JSON.stringify(user));
    this.userSubject$.next(user);
    this.isAuthenticatedSubject$.next(true);
    this.autoLogout(expirationDate.getTime() - new Date().getTime());
  }

  checkEmail(email: string): Observable<boolean> {
    return this.http
      .get<User[]>(`${environment.apiUrl}/users`)
      .pipe(map((users) => !!users.find((user) => user.email === email)));
  }

  checkUsername(username: string): Observable<boolean> {
    return this.http
      .get<User[]>(`${environment.apiUrl}/users`)
      .pipe(map((users) => !!users.find((user) => user.username === username)));
  }

  activateUser(userId: string): Observable<User> {
    return this.http.patch<User>(`${environment.apiUrl}/users/${userId}`, {
      isActive: true,
    });
  }

  register({ username, email, password }: IRegister): Observable<AuthResponse> {
    const newUser = new User({ username, email, password });
    return this.http.post<AuthResponse>(
      `${environment.apiUrl}/register`,
      newUser,
    );
  }

  login({ email, password }: ILogin): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${environment.apiUrl}/login`, {
        email,
        password,
      })
      .pipe(
        tap((response) => {
          const payload = this.tokenService.decodeToken(response.accessToken);
          this.handleAuthentication(payload, response.accessToken);
        }),
        mergeMap((response) => {
          return this.activateUser(response.user.id).pipe(map(() => response));
        }),
      );
  }

  isLoggedIn(): boolean {
    return this.isAuthenticatedSubject$.value;
  }

  autoLogin(): void {
    const accountUser = this.accountUser;
    if (!accountUser) {
      return;
    }
    if (accountUser.token) {
      const payload = this.tokenService.decodeToken(accountUser.token);
      const expirationDate = new Date(payload.exp * 1000);
      if (expirationDate > new Date()) {
        this.userSubject$.next(accountUser);
        this.isAuthenticatedSubject$.next(true);
        console.log("User restored:", accountUser);
      }
      const timeLeft = expirationDate.getTime() - new Date().getTime();
      this.autoLogout(timeLeft);
    } else {
      this.logout();
    }
  }

  autoLogout(expirationTime: number): void {
    this.tokenExpirationTimer = setTimeout(() => {
      this.logout();
    }, expirationTime);
  }

  logout(): void {
    this.tokenService.clearToken();
    this.userSubject$.next(null);
    this.isAuthenticatedSubject$.next(false);
    this.router.navigate(["/auth/login"]);

    if (this.tokenExpirationTimer) {
      clearTimeout(this.tokenExpirationTimer);
    }
    this.tokenExpirationTimer = null;
  }
}
