import { Component } from "@angular/core";
import { AuthService } from "../auth.service";
import {
  FormGroup,
  FormBuilder,
  Validators,
  FormControl,
  FormsModule,
  ReactiveFormsModule,
} from "@angular/forms";
import { AuthResponse } from "interfaces/auth.interface";
import { EmailDoesNotExistsValidator } from "../validations/validation.service";
import { Router, RouterLink } from "@angular/router";
import { ErrorMessageComponent } from "../validations/error-message.component";

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.css"],
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, ErrorMessageComponent],
})
export class LoginComponent {
  loginForm: FormGroup;
  submitted = false;
  errorMessageControl: FormControl = new FormControl();

  constructor(
    private authService: AuthService,
    private formBuilder: FormBuilder,
    private router: Router,
  ) {
    this.loginForm = this.formBuilder.group({
      email: [
        "",
        [Validators.required, Validators.email],
        EmailDoesNotExistsValidator.createValidator(this.authService),
      ],
      password: ["", [Validators.required, Validators.minLength(8)]],
    });
  }

  get fields() {
    return this.loginForm.controls;
  }

  onSubmit() {
    this.submitted = true;
    this.errorMessageControl.setErrors(null);
    const { email, password } = this.loginForm.value;
    if (this.loginForm.valid) {
      if (email && password) {
        this.authService.login({ email, password }).subscribe({
          next: (response: AuthResponse) => {
            this.submitted = false;
            this.router.navigate(["/"]);
          },
          error: (error) => {
            this.errorMessageControl.setErrors({
              wrongCredentials: error.message,
            });
            this.submitted = false;
          },
        });
      } else {
        this.loginForm.reset();
      }
    } else {
      console.log(this.loginForm.errors);
      return;
    }
  }
}
