import { Component, Input } from '@angular/core';
import { AbstractControl, FormGroup } from '@angular/forms';
import { ValidationService } from './validation.service';

@Component({
    selector: 'error-message',
    templateUrl: './error-message.component.html',
    standalone: false
})
export class ErrorMessageComponent {
  // @ts-ignore
  @Input('control') control: AbstractControl | FormGroup;

  get errorMessage(): string | null {
    if (this.control instanceof FormGroup && this.control.errors) {
      const key = Object.keys(this.control.errors)[0];
      return ValidationService.getValidationMessage(
        key,
        this.control.errors[key],
      );
    } else if (this.control.errors) {
      const key = Object.keys(this.control.errors)[0];
      return ValidationService.getValidationMessage(
        key,
        this.control.errors[key],
      );
    }

    return null;
  }
}
