import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LoaderService {
  public loading$ = new Subject<boolean | Error>();

  show() {
    this.loading$.next(true);
  }

  hide() {
    this.loading$.next(false);
  }

  error(err: any) {
    this.loading$.error(err);
  }

  complete() {
    this.loading$.complete();
  }
}
