import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { AuthService } from '../auth.service';
import {Router} from "@angular/router";

@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.css']
})
export class NewsComponent implements OnInit {

  constructor(private apiService: ApiService, router: Router) { }

  postNews = '';
  fakenews = '';
  spaceScreens=[];

  ngOnInit() {
    
  }

  post(){
  	this.apiService.getFakeNews({news: this.postNews})
  }
}
