import {
  booleanAttribute,
  Component,
  Input,
  input,
  OnDestroy,
  OnInit,
  effect,
  Signal,
} from "@angular/core";
import { CalendarComponent } from "../calendar/calendar.component";
import { RouterLink } from "@angular/router";
import { AuthComponent } from "../auth/auth.component";
import { AuthService } from "../auth/auth.service";

@Component({
  selector: "app-main",
  imports: [CalendarComponent, AuthComponent],
  templateUrl: "./main.component.html",
  styleUrl: "./main.component.css",
  standalone: true
})
export class MainComponent implements OnInit {
  isLoggedIn: Signal<boolean>;

  constructor(private authService: AuthService) {
    this.isLoggedIn = this.authService.isAuthenticated;
  }

  ngOnInit() {}
}
