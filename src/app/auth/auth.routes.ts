import { RouterModule, Routes } from "@angular/router";
import { NgModule } from "@angular/core";
import { AuthGuard, NonAuthGuard } from "./auth.guard";

export const authRoutes: Routes = [
  {
    path: "",
    loadComponent: () =>
      import("./auth.component").then((c) => c.AuthComponent),
    canActivate: [AuthGuard],
  },
  {
    path: "login",
    loadComponent: () =>
      import("./login/login.component").then((c) => c.LoginComponent),
    canActivate: [NonAuthGuard],
  },
  {
    path: "register",
    loadComponent: () =>
      import("./register/register.component").then((c) => c.RegisterComponent),
    canActivate: [NonAuthGuard],
  },
];

@NgModule({
  imports: [RouterModule.forChild(authRoutes)],
  exports: [RouterModule],
})
export class AuthRoutes {}
