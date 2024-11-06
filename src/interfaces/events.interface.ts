export interface ICalendarEvent {
  id?: number;
  title: string;
  description?: string;
  startDate: Date;
  endDate: Date;
  recurrence?: {
    type: 'daily' | 'weekly' | 'monthly';
  };
}

export interface ICalendarEventForm {
  isOpen: boolean;
  mode: 'add' | 'edit';
  position: {
    x: number;
    y: number;
  };
  selectedDate: Date;
  selectedEvent?: ICalendarEvent;
}
