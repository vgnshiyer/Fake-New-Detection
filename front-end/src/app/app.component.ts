import { Component } from '@angular/core';
import { AuthService } from './auth.service'
import { ApiService } from './api.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
	
  constructor(private authService: AuthService,private apiService: ApiService){}

  title = 'front-end';

  ngOnInit() {
  
  }
}
