export interface EventMode {
  mode: 'add' | 'edit';
}

export interface EventRecurrenceMode {
  type: 'daily' | 'weekly' | 'monthly';
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
