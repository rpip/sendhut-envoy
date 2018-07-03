const ENV = process.env.NODE_ENV || 'development'

console.log(ENV)

let loadConf = function(){
  switch(ENV){
    case 'development':
      return {
        apiBaseURL:  'http://localhost:8000/api',
        staticUrl: '/static'
      };

    case 'production':
      return {
        apiBaseURL: 'http://envoy.herokuapp.com/api',
        staticUrl: 'https://sendhut-envoy-assets.s3.amazonaws.com/static/'
      };

    case 'test':
      return {};

    default:
      return {};
  }
};


export default loadConf()
