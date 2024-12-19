import { effect, Injectable, Signal } from "@angular/core";
import { BehaviorSubject, mergeMap, Observable, Subject, tap } from "rxjs";
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
import { jwtDecode } from "jwt-decode";
import { Router } from "@angular/router";
import { toSignal } from "@angular/core/rxjs-interop";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private userSubject$ = new BehaviorSubject<UserSubject | null>(null);
  private isAuthenticatedSubject$ = new BehaviorSubject<boolean>(false);
  private tokenExpirationTimer: any;

  user: Signal<UserSubject | null> = toSignal(
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
  ) {
    this.userSubject$.next(this.accountUser);
  }

  public get accountUser(): UserSubject | null {
    const userString = localStorage.getItem("authUser");
    console.log("userString", userString);
    const userData = userString ? JSON.parse(userString) : null;
    if (!userData) {
      return null;
    }
    return new UserSubject(
      userData.id,
      userData.email,
      userData._token,
      new Date(userData._tokenExpirationDate),
    );
  }

  private handleAuthentication(payload: TokenPayload, token: string): void {
    const expirationDate = new Date(new Date().getTime() + payload.exp * 1000);
    const user = new UserSubject(
      payload.sub,
      payload.email,
      token,
      expirationDate,
    );
    localStorage.setItem("authUser", JSON.stringify(user));
    this.userSubject$.next(user);
    this.isAuthenticatedSubject$.next(true);
    console.log("userSubject$:", this.userSubject$.getValue());
  }

  public getUser(): Observable<UserSubject | null> {
    return this.userSubject$.asObservable();
  }

  public getUserId(): Observable<string | null> {
    return this.getUser().pipe(map((user) => user?.id || null));
  }

  public getToken(): string | null {
    return this.user()?.token || null;
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

  decodeToken(token: string): TokenPayload {
    return jwtDecode(token) as TokenPayload;
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
          const payload = this.decodeToken(response.accessToken);
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
      const payload = this.decodeToken(accountUser.token);
      const expirationDate = new Date(payload.exp * 1000);
      if (expirationDate > new Date()) {
        this.userSubject$.next(accountUser);
      }
      const timeLeft = expirationDate.getTime() - new Date().getTime();
      this.autoLogout(timeLeft);
    }
  }

  autoLogout(expirationTime: number): void {
    this.tokenExpirationTimer = setTimeout(() => {
      this.logout();
    }, expirationTime);
  }

  logout(): void {
    localStorage.removeItem("authUser");
    this.userSubject$.next(null);
    this.isAuthenticatedSubject$.next(false);
    this.router.navigate(["/auth/login"]);

    if (this.tokenExpirationTimer) {
      clearTimeout(this.tokenExpirationTimer);
    }
    this.tokenExpirationTimer = null;
  }
}
