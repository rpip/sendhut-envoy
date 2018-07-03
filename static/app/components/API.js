import axios from 'axios';

import config from '../config'


//console.log(config)

export default axios.create({
  baseURL: config.apiBaseURL
});
