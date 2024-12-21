export interface EventMode {
  mode: 'add' | 'edit' | 'view';
}

export interface EventRecurrenceMode {
  type: 'none' | 'daily' | 'weekly' | 'monthly';
  repeatUntil?: Date | null;
}

export interface Event {
  id?: number;
  title: string;
  description?: string;
  startDate: Date;
  endDate: Date;
  recurrence: EventRecurrenceMode;
  userId: string;
}

export interface EventForm {
  isOpen: boolean;
  mode: EventMode;
  position: {
    x: number;
    y: number;
  };
  selectedDate: Date;
  selectedEvent?: Event;
}
