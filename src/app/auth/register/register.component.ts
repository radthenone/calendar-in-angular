import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import {
  checkPasswords,
  EmailExistsValidator,
  UsernameExistsValidator,
} from '../validations/validation.service';
import { AuthResponse } from 'interfaces/auth.interface';

@Component({
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: ['./register.component.css'],
    standalone: false
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  submitted = false;
  constructor(
    private authService: AuthService,
    private formBuilder: FormBuilder,
    private router: Router,
  ) {
    this.registerForm = this.formBuilder.group(
      {
        email: [
          '',
          [Validators.required, Validators.email],
          EmailExistsValidator.createValidator(this.authService),
        ],
        username: [
          '',
          [Validators.required],
          UsernameExistsValidator.createValidator(this.authService),
        ],
        password: ['', [Validators.required, Validators.minLength(8)]],
        confirmPassword: ['', [Validators.required, Validators.minLength(8)]],
      },
      {
        validators: [checkPasswords],
      },
    );
  }

  ngOnInit() {}

  get fields() {
    return this.registerForm.controls;
  }

  onSubmit() {
    this.submitted = true;
    if (!this.registerForm.valid) {
      return;
    }
    const { email, username, password } = this.registerForm.value;
    this.authService.register({ email, username, password }).subscribe({
      next: (response: AuthResponse) => {
        console.log(response);
        this.router.navigate(['auth/login']);
      },
      error: (error: Error) => {
        console.log(error);
      },
    });
    this.registerForm.reset();
  }
}
