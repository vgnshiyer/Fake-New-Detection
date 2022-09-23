import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import {MatDialog} from '@angular/material';
import {DialogComponent} from '../app/dialog/dialog.component';
import { INews } from './Inews';
import { Observable } from 'rxjs/Observable';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
	
  news = [];
  path = 'http://127.0.0.1:5000';
  fake = '';
  

  constructor(private http: HttpClient, public dialog: MatDialog) { }

  getFakeNews(news){
  console.log(news.news)
    this.http.get<any>(this.path + '/checknews/' +news.news).subscribe(
    res => {
    	console.log("response",res);
      this.fake =res;
      news.fakeValue = this.fake;
      
      const dialogRef = this.dialog.open(DialogComponent, {
        data: {fake: news.fakeValue, news: news.news},
      });

      dialogRef.afterClosed().subscribe(result => {
            console.log(`Dialog result: ${result}`);
          });
    })
  }

  getData(): Observable<INews[]>{
    return this.http.get<INews[]>('assets/data.json')
  }
}
