import React from 'react'
import ReactDOM from 'react-dom'

import RideEstimate from './app/components/RideEstimate'
import './styles/main.scss';


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

let homeMapEl = document.getElementById('ride-estimate')

if (homeMapEl) {
  ReactDOM.render(<RideEstimate />, homeMapEl);
}
