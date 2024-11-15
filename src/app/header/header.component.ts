import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { UserSubject } from 'models/users.model';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent implements OnInit, OnDestroy {
  isAuthenticated: boolean = false;
  user: UserSubject | null = null;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.authService.getUser().subscribe((user) => {
      this.user = user;
      this.isAuthenticated = !!user;
    });
  }

  ngOnDestroy() {}

  onLogout() {
    this.authService.logout();
  }
}
