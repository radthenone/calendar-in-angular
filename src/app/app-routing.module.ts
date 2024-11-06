import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageNotFoundComponent } from './common/page-not-found-component/page-not-found-component.component';
import { HeaderComponent } from './header/header.component';

const authModule = () =>
  import('src/app/auth/auth-routing.module').then((x) => x.AuthRoutingModule);

const routes: Routes = [
  {
    path: '',
    component: HeaderComponent,
  },
  {
    path: 'auth',
    loadChildren: authModule,
  },
  { path: '**', component: PageNotFoundComponent },
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
