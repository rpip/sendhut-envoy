import React from 'react'

export default class Auth {
  login(username, pass, cb) {
    if (localStorage.flighthound_token) {
      if (cb) cb(true)
      return
    }
    this.getToken(username, pass, (res) => {
      if (res.authenticated) {
        localStorage.flighthound_token = res.token
        if (cb) cb(true)
      } else {
        if (cb) cb(false)
      }
    })
  }

  logout() {
    delete localStorage.flighthound_token
  }

  loggedIn() {
    return !!localStorage.flighthound_token
  }


  getToken(username, pass, cb) {
    $.ajax({
      type: 'POST',
      url: '/api/auth-token/',
      data: {
        username: username,
        password: pass
      },
      success: function(res){
        cb({
          authenticated: true,
          token: res.token
        })
      }
    })
  }
}
