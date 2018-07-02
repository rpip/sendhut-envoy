import React from 'react'
import ReactDOM from 'react-dom'

import RideEstimate from './app/components/RideEstimate'
import Auth from './app/components/Auth'
import './styles/main.scss';

function requireAuth(nextState, replace) {
  if (!Auth.loggedIn()) {
    // TODO(yao): redirect, display errors etc
  }
}

function initMastheadAnimtion() {
  // site banner
  var words = [
    'done right',
    'made easy',
  ], i = 0;

  setInterval(function(){
    $('#hero-title-dynamic').fadeOut(function(){
      $(this).html(words[i=(i+1)%words.length]).fadeIn('slow', 'swing');
    });
    // 5 seconds
  }, 5000);
}

initMastheadAnimtion()

ReactDOM.render(<RideEstimate />, document.getElementById('ride-estimate'));
