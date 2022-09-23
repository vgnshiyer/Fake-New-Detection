import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { DialogComponent } from './dialog/dialog.component';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {MatIconModule} from '@angular/material/icon';

import {
  MatButtonModule,
  MatCardModule,
  MatToolbarModule,
  MatInputModule,
  MatListModule,
  MatDialogModule,
  MatTabsModule
} from '@angular/material';

import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NewsComponent } from './news/news.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';

import { ApiService } from './api.service';
import { AuthService } from './auth.service';
import { AuthInterceptorService } from './auth-interceptor.service';
import { LiveComponent } from './live/live.component';
import { AboutusComponent } from './aboutus/aboutus.component';

const routes = [
  { path: '', component: LiveComponent},
  { path: 'news', component: NewsComponent},
  { path: 'faq', component: RegisterComponent },
  { path: 'recent', component: LoginComponent },
  { path: 'aboutus', component: AboutusComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    DialogComponent,
    NewsComponent,
    LoginComponent,
    RegisterComponent,
    LiveComponent,
    AboutusComponent
  ],
  entryComponents: [DialogComponent],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    BrowserAnimationsModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatToolbarModule,
    MatInputModule,
    MatListModule,
    MatDialogModule,
    MatTabsModule,
    HttpClientModule,
    RouterModule.forRoot(routes)
  ],
  providers: [ApiService, AuthService, {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
