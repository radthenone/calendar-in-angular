import {
  booleanAttribute,
  Component,
  Input,
  OnDestroy,
  OnInit,
} from "@angular/core";
import { CalendarComponent } from "../calendar/calendar.component";
import { RouterLink } from "@angular/router";
import { AuthComponent } from "../auth/auth.component";

@Component({
  selector: "app-main",
  imports: [CalendarComponent, AuthComponent],
  templateUrl: "./main.component.html",
  styleUrl: "./main.component.css",
})
export class MainComponent implements OnInit {
  @Input() isAuthenticated: boolean = false;
  ngOnInit() {}
}
