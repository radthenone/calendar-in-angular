import { Component, OnDestroy, OnInit, Signal } from "@angular/core";
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
  user: Signal<UserSubject | null>;
  isLoggedIn: Signal<boolean>;

  constructor(private authService: AuthService) {
    this.user = this.authService.getUser;
    this.isLoggedIn = this.authService.isAuthenticated;
  }

  ngOnInit() {}

  ngOnDestroy() {}

  onLogout() {
    this.authService.logout();
  }
}
