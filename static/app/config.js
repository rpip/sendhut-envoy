const ENV = process.env.NODE_ENV || 'development'


module.exports = function(){
  switch(ENV){
    case 'development':
      return {
        apiBaseURL:  'http://localhost:8000/api',
        staticUrl: staticUrl
      };

    case 'production':
      return {
        apiBaseURL: 'http://envoy.herokuapp.com',
        staticUrl: 'https://sendhut-envoy-assets.s3.amazonaws.com/static/'
      };

    case 'test':
      return {};

    default:
      return {};
  }
};
