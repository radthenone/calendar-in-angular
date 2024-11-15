import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../environment';
import { catchError, delay, Observable, throwError } from 'rxjs';
import { ICalendarEvent } from '../../interfaces/events.interface';

@Injectable({
  providedIn: 'root',
})
export class EventService {
  constructor(private http: HttpClient) {}

  getEvents(): Observable<ICalendarEvent[]> {
    return this.http.get<ICalendarEvent[]>(`${environment.apiUrl}/events`).pipe(
      delay(1000),
      catchError((error: Error) =>
        throwError(() => new Error('Events not found')),
      ),
    );
  }

  getEvent(id: number, userId: number): Observable<ICalendarEvent> {
    if (!userId || !id) {
      return throwError(() => new Error('Missing user id or event id'));
    }
    return this.http
      .get<ICalendarEvent>(`${environment.apiUrl}/events/`, {
        params: new HttpParams()
          .set('id', id.toString())
          .set('userId', userId.toString()),
      })
      .pipe(
        delay(1000),
        catchError((error: Error) =>
          throwError(() => new Error('Event not found')),
        ),
      );
  }

  addEvent(event: ICalendarEvent): Observable<ICalendarEvent> {
    if (!event) {
      return throwError(() => new Error('Missing event'));
    }
    return this.http.post<ICalendarEvent>(
      `${environment.apiUrl}/events`,
      event,
    );
  }

  updateEvent(
    newEvent: ICalendarEvent,
    id: number,
  ): Observable<ICalendarEvent> {
    if (!newEvent || !id) {
      return throwError(() => new Error('Missing event or id'));
    }
    return this.http
      .put<ICalendarEvent>(`${environment.apiUrl}/events/`, {
        ...newEvent,
        params: new HttpParams().set('id', id.toString()),
      })
      .pipe(
        delay(1000),
        catchError((error: Error) =>
          throwError(() => new Error('Event not found')),
        ),
      );
  }

  deleteEvent(id: number): Observable<ICalendarEvent> {
    if (!id) {
      return throwError(() => new Error('Missing event id'));
    }
    return this.http
      .delete<ICalendarEvent>(`${environment.apiUrl}/events/`, {
        params: new HttpParams().set('id', id.toString()),
      })
      .pipe(
        delay(1000),
        catchError((error: Error) =>
          throwError(() => new Error('Event not found')),
        ),
      );
  }
}
