import {
  Component,
  Input,
  OnDestroy,
  OnInit,
  Signal,
  signal,
} from "@angular/core";
import { AuthService } from "../auth/auth.service";
import { UserSubject } from "models/users.model";
import { RouterLink } from "@angular/router";

@Component({
  selector: "app-header",
  templateUrl: "./header.component.html",
  styleUrls: ["./header.component.css"],
  standalone: true,
  imports: [RouterLink],
})
export class HeaderComponent implements OnInit, OnDestroy {
  @Input() isAuthenticated: boolean = false;
  @Input() user: Signal<UserSubject | null> = signal(null);

  // isAuthenticated: boolean = false;
  // user: UserSubject | null = null;

  constructor(private authService: AuthService) {}

  ngOnInit() {}

  ngOnDestroy() {}

  onLogout() {
    this.authService.logout();
  }
}
