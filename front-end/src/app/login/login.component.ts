import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service'
import { HttpClient} from '@angular/common/http';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
	
  public newscontent=[];

  constructor(private apiService : ApiService) { }

  ngOnInit() {
    this.apiService.getData()
      .subscribe(data => {this.newscontent = data;
        console.log(this.newscontent[0].img);
      });
  }
}
