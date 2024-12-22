import { Component, effect, OnInit, Signal } from "@angular/core";
import { AuthService } from "./auth/auth.service";
import { MainComponent } from "./main/main.component";
import { HeaderComponent } from "./header/header.component";
import { UserSubject } from "models/users.model";
import { environment } from "environment";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"],
  imports: [MainComponent, HeaderComponent],
})
export class AppComponent implements OnInit {
  user: Signal<UserSubject | null>;
  isLoggedIn: Signal<boolean>;

  constructor(private authService: AuthService) {
    this.user = this.authService.getUser;
    this.isLoggedIn = this.authService.isAuthenticated;
    console.log(environment.secretKey);
  }

  ngOnInit(): void {
    if (this.user() == null) {
      this.authService.autoLogin();
    }
  }
}
