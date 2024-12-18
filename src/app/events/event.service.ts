import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../environment';
import { catchError, delay, Observable, throwError } from 'rxjs';
import { Event } from '../../interfaces/events.interface';

@Injectable({
  providedIn: 'root',
})
export class EventService {
  constructor(private http: HttpClient) {}

  getEvents(): Observable<Event[]> {
    return this.http.get<Event[]>(`${environment.apiUrl}/events`).pipe(
      delay(1000),
      catchError((error: Error) =>
        throwError(() => new Error('Events not found')),
      ),
    );
  }

  getEvent(id: number, userId: number): Observable<Event> {
    if (!userId || !id) {
      return throwError(() => new Error('Missing user id or event id'));
    }
    return this.http
      .get<Event>(`${environment.apiUrl}/events/`, {
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


  addEvent(newEvent: Event): Observable<Event> {
    if (!newEvent || !newEvent.userId) {
      return throwError(() => new Error('Missing event'));
    }
    return this.http
      .post<Event>(`${environment.apiUrl}/events`, newEvent)
      .pipe(
        catchError((error: Error) =>
          throwError(() => new Error('Failed to add event')),
        ),
      );
  }

  updateEvent(updatedEvent: Event, id: number): Observable<Event> {
    if (!updatedEvent || !id) {
      return throwError(() => new Error('Missing event or id'));
    }
    return this.http
      .put<Event>(`${environment.apiUrl}/events/`, {
        ...updatedEvent,
        params: new HttpParams().set('id', id.toString()),
      })
      .pipe(
        delay(1000),
        catchError((error: Error) =>
          throwError(() => new Error('Event not found')),
        ),
      );
  }

  deleteEvent(id: number): Observable<Event> {
    if (!id) {
      return throwError(() => new Error('Missing event id'));
    }
    return this.http
      .delete<Event>(`${environment.apiUrl}/events/`, {
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
