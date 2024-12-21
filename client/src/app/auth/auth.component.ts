import { Component, Input } from "@angular/core";
import { LoginComponent } from "./login/login.component";
import { RegisterComponent } from "./register/register.component";

@Component({
  selector: "app-auth",
  templateUrl: "./auth.component.html",
  styleUrls: ["./auth.component.css"],
  imports: [LoginComponent, RegisterComponent],
})
export class AuthComponent {
  @Input() isAuthenticated: boolean = false;
  isLogin = true;

  onSwitchMode() {
    this.isLogin = !this.isLogin;
  }
}
