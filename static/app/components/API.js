// api.js
import axios from 'axios';

/**
 * @param  {Error}  error
 * @return {boolean}
 */
/* export function isRetryableError(error) {
 *   return (
 *     error.code !== 'ECONNABORTED' &&
 *     (!error.response || (error.response.status >= 500 && error.response.status <= 599))
 *   );
 * }
 * */
// retries errors once.
// see: https://github.com/axios/axios/issues/164
// TODO(yao): do exponential backoff retries in certain cases
// - don't retry exponential back-offs
/* function retryFailedRequest (err) {
 *   if (err.status >= 300 && err.config && !err.config.__isRetryRequest) {
 *     err.config.__isRetryRequest = true;
 *     // return resolve instead?
 *     // resolve(axios(err.config))
 *     return axios(err.config);
 *   }
 *   throw err;
 * }
 *
 * axios.interceptors.response.use(retryFailedRequest);
 * */
const prodUrl = 'http://sendhut.com/api'
const devUrl = 'http://localhost:8000/api'
const PROD = 'prod'
const DEV = 'dev'

export default axios.create({
  baseURL: process.env.ENVIRONMENT == PROD ? prodUrl : devUrl
  // timeout: 2500
});
