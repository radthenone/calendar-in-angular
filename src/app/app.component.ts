import { Component, effect, OnInit, Signal } from "@angular/core";
import { AuthService } from "./auth/auth.service";
import { MainComponent } from "./main/main.component";
import { HeaderComponent } from "./header/header.component";
import { UserSubject } from "models/users.model";
import { toSignal } from "@angular/core/rxjs-interop";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"],
  imports: [MainComponent, HeaderComponent],
})
export class AppComponent implements OnInit {
  user: Signal<UserSubject | null>;
  isAuthenticated: boolean = false;

  constructor(private authService: AuthService) {
    this.user = toSignal(this.authService.getUser(), { initialValue: null });

    effect(() => {
      this.isAuthenticated = this.user() !== null;
    });
  }

  ngOnInit(): void {
    if (this.user() == null) {
      this.authService.autoLogin();
    }
  }
}
