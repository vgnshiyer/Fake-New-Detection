import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
	
  news = [];

  TOKEN_KEY = 'token'
  
  constructor(private http: HttpClient) { }
  
  get token() {
    return localStorage.getItem(this.TOKEN_KEY)
  }

  loginUser(loginData){
  	if(loginData.email == 'vignesh@gmail.com' && loginData.pwd == 'vignesh'){
  		console.log('logged in')
  	}
  	else{
  		console.log('invalid username or password')
  	}
  }
}
