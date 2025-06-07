import { Routes } from '@angular/router';
import { ImmigrationListComponent } from './components/immigration/immigration-list/immigration-list.component';
import { ImmigrationDetailComponent } from './components/immigration/immigration-detail/immigration-detail.component';
import { ImmigrationFormComponent } from './components/immigration/immigration-form/immigration-form.component';

export const routes: Routes = [
  { path: '', redirectTo: 'records', pathMatch: 'full' },
  { path: 'records', component: ImmigrationListComponent },
  { path: 'records/:id', component: ImmigrationDetailComponent },
  { path: 'new', component: ImmigrationFormComponent },
  { path: 'edit/:id', component: ImmigrationFormComponent },
  { path: '**', redirectTo: 'records' }
];
