import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { PageNotFoundComponent } from "./common/page-not-found-component/page-not-found-component.component";
import { AppComponent } from "./app.component";

export const routes: Routes = [
  {
    path: "",
    component: AppComponent,
  },
  {
    path: "main",
    loadComponent: () =>
      import("./main/main.component").then((c) => c.MainComponent),
  },
  {
    path: "header",
    loadComponent: () =>
      import("./header/header.component").then((c) => c.HeaderComponent),
  },
  {
    path: "auth",
    loadChildren: () => import("./auth/auth.routes").then((m) => m.authRoutes),
  },
  { path: "**", component: PageNotFoundComponent },
];
