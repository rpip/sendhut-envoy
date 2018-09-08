import React from 'react'
import Cookies from 'react-cookie'

const cookies = new Cookies();

export default class Auth {
  static logout() {
    cookies.remove('auth_token')
  }

  static loggedIn() {
    return !!this.getToken()
  }

  static getToken() {
    return cookies.get('auth_token')
  }
}
