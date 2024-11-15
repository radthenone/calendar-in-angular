import { Component, OnInit } from '@angular/core';
import { CalendarDay } from 'models/calendar.model';

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css'],
  providers: [],
})
export class CalendarComponent implements OnInit {
  calendar: CalendarDay[];
  currentDate: Date;
  currentMonth: string | undefined;
  weekNames: string[];
  monthNames: string[];

  constructor() {
    this.calendar = [];
    this.weekNames = Array.from({ length: 7 }, (_, index) => {
      return new Date(0, 0, 1 + index).toLocaleString('default', {
        weekday: 'long',
      });
    });
    this.currentDate = new Date();
    this.monthNames = Array.from({ length: 12 }, (_, index) => {
      return new Date(0, index).toLocaleString('default', { month: 'long' });
    });
    this.generateMonthName();
  }

  ngOnInit(): void {
    this.generateCalendar();
  }

  generateCalendar() {
    this.calendar = [];

    const currentYear = this.currentDate.getFullYear();
    const currentMonth = this.currentDate.getMonth();

    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);

    const startDate = new Date(firstDayOfMonth);
    startDate.setDate(startDate.getDate() - startDate.getDay());

    for (let day = 0; day < 42; day++) {
      this.calendar.push(new CalendarDay(new Date(startDate)));
      startDate.setDate(startDate.getDate() + 1);
    }
  }

  generateMonthName() {
    this.currentMonth = this.monthNames[this.currentDate.getMonth()];
  }

  previousMonth() {
    this.currentDate = new Date(
      this.currentDate.getFullYear(),
      this.currentDate.getMonth() - 1,
    );
    this.generateMonthName();
    this.generateCalendar();
  }

  nextMonth() {
    this.currentDate = new Date(
      this.currentDate.getFullYear(),
      this.currentDate.getMonth() + 1,
    );
    this.generateMonthName();
    this.generateCalendar();
  }

  hasEvents(day: CalendarDay): boolean {
    return day.events.length > 0;
  }
}
