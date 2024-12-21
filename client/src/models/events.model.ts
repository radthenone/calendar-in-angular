import { InjectionToken } from '@angular/core';
import { EventMode, EventRecurrenceMode } from 'interfaces/events.interface';

export const DEFAULT_EVENT_MODE: EventMode = {
  mode: 'add',
};

export const DEFAULT_EVENT_RECURRENCE_MODE: EventRecurrenceMode = {
  type: 'daily',
};

export const EVENT_MODE_TOKEN = new InjectionToken<EventMode>('EventMode');
export const EVENT_RECURRENCE_MODE_TOKEN =
  new InjectionToken<EventRecurrenceMode>('EventRecurrenceMode');
