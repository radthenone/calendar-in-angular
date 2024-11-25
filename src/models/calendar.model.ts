export class CalendarDay {
  public date: Date;
  public isPast: boolean;
  public isToday: boolean;
  public isMonthDays: boolean;
  // public events: ICalendarEvent[];

  constructor(date: Date) {
    this.date = date;
    this.isPast = this.setIsPast(date);
    this.isToday = this.setIsToday(date);
    this.isMonthDays = this.setIsMonthDays(date);
    // this.events = [];
  }

  setIsPast(date: Date): boolean {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const targetDate = date;
    targetDate.setHours(0, 0, 0, 0);
    return targetDate < today;
  }

  setIsMonthDays(date: Date): boolean {
    const month = new Date().getMonth();
    return date.getMonth() === month;
  }

  setIsToday(date: Date): boolean {
    return date.toDateString() === new Date().toDateString();
  }
}
