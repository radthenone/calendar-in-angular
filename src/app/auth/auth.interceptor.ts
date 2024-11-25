import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { AuthService } from './auth.service';
import { Injectable } from '@angular/core';
import { Observable, take, switchMap, catchError, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler,
  ): Observable<HttpEvent<any>> {
    return this.authService.userSubject$.pipe(
      take(1),
      switchMap((account) => {
        if (account && account.token) {
          request = request.clone({
            setHeaders: {
              Authorization: `Bearer ${account.token}`,
            },
          });
        }
        return next.handle(request).pipe(
          catchError((error: HttpErrorResponse) => {
            if (error.status === 401) {
              this.authService.logout();
            }
            return throwError(() => error);
          }),
        );
      }),
    );
  }
}
