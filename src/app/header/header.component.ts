import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { UserSubject } from '../../models/users.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent implements OnInit, OnDestroy {
  isAuthenticated: boolean = false;
  user: UserSubject | null = null;
  userSubscription: Subscription | undefined;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.userSubscription = this.authService.getUser().subscribe((user) => {
      this.user = user;
      this.isAuthenticated = !!user;
    });
  }

  ngOnDestroy() {
    if (this.userSubscription) {
      this.userSubscription.unsubscribe();
    }
  }

  onLogout() {
    this.authService.logout();
  }
}
