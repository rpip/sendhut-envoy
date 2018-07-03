import axios from 'axios';

import config from '../config'

// @param  {Error}  error
// @return {boolean}
export function isRetryableError(error) {
  return (
    error.code !== 'ECONNABORTED' &&
    (!error.response || (error.response.status >= 500 && error.response.status <= 599))
  );
}


export default axios.create({
  baseURL: config.apiBaseURL
});
