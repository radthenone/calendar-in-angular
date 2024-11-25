import { Component } from '@angular/core';

@Component({
    selector: 'app-auth',
    templateUrl: './auth.component.html',
    styleUrls: ['./auth.component.css'],
    standalone: false
})
export class AuthComponent {
  isLogin = true;

  onSwitchMode() {
    this.isLogin = !this.isLogin;
  }
}
