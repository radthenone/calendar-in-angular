import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { AuthService } from '../auth.service';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

export class ValidationService {
  static getValidationMessage(validator: string, validatorValue?: any) {
    const messages: any = {
      required: 'This field is required',
      email: 'Invalid email syntax',
      minlength: `Min length is ${validatorValue.requiredLength} characters`,
      emailExists: 'Email already exists',
      usernameExists: 'Username already exists',
      passwordsDontMatch: "Passwords don't match",
      serverError: 'Server error',
      wrongCredentials: 'Wrong credentials',
      emailDoesNotExists: 'Email does not exists',
    };

    return messages[validator];
  }
}

export const checkPasswords: ValidatorFn = (
  control: AbstractControl,
): ValidationErrors | null => {
  const password = control.get('password')?.value;
  const confirmPassword = control.get('confirmPassword')?.value;
  return password === confirmPassword ? null : { passwordsDontMatch: true };
};

export class EmailExistsValidator {
  static createValidator(authService: AuthService): ValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return authService
        .checkEmail(control.value)
        .pipe(map((exists) => (exists ? { emailExists: true } : null)));
    };
  }
}

export class EmailDoesNotExistsValidator {
  static createValidator(authService: AuthService): ValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return authService
        .checkEmail(control.value)
        .pipe(map((exists) => (exists ? null : { emailDoesNotExists: true })));
    };
  }
}

export class UsernameExistsValidator {
  static createValidator(authService: AuthService): ValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return authService
        .checkUsername(control.value)
        .pipe(map((exists) => (exists ? { usernameExists: true } : null)));
    };
  }
}
