//require our dependencies
var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

const ExtractTextPlugin = require('extract-text-webpack-plugin');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')


module.exports = env => {
  console.log(env)

  return {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    //the entry point we created earlier. Note that './' means
    //your current directory. You don't have to specify the extension  now,
    //because you will specify extensions later in the `resolve` section
    entry: './app.js',
    mode: 'development',
    output: {
      //where you want your compiled bundle to be stored
      path: path.resolve(__dirname, 'dist'),
      // naming convention webpack should use for your files
      //filename: '[name]-[hash].js',
      filename: 'bundle.js',
      //publicPath: 'http://localhost:3000/assets/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
    },
    module: {
      rules: [
        {
          test: /\.(scss|css)$/,
          use: ExtractTextPlugin.extract({
            fallback: 'style-loader',
            use: [
              {
                loader: 'css-loader',
                options: {
                  // If you are having trouble with urls not resolving add this setting.
                  // See https://github.com/webpack-contrib/css-loader#url
                  url: false,
                  minimize: true,
                  sourceMap: true
                }
              },
              {
                loader: 'sass-loader',
                options: {
                  sourceMap: true
                }
              }
            ]
          })
        },
        {
          test: /\.(woff(2)?|ttf|eot|otf)(\?v=\d+\.\d+\.\d+)?$/,
          use: [{
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts/'
            }
          }]
        },
        {
          test: /\.(png|jpg|gif|svg)$/,
          use: [
            {
              //loader: 'file-loader!postcss-loader',
              loader: 'file-loader',
              options: {
                name: '[path][name].[ext]',
                //outputPath: 'images/',
                //include: './images',
                publicPath: '/static'
              }
            }, 'image-webpack-loader'
          ]
        },
        //a regexp that tells webpack use the following loaders on all
        //.js and .jsx files
        {
          test: /\.(js|jsx)?$/,
          //we definitely don't want babel to transpile all the files in
          //node_modules. That would take a long time.
          exclude: /node_modules/,
          //use the babel loader
          loader: 'babel-loader',
          query: {
            //specify that we will be dealing with React code
            presets: ['react']
          }
        }
      ]
    },
    plugins: [
      // TODO(yao): split vendor from internal code
      new CleanWebpackPlugin(['dist']),
      //new webpack.HotModuleReplacementPlugin(),
      new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error
      //new UglifyJSPlugin(),
      new ExtractTextPlugin('main.css'),
      //tells webpack where to store data about your bundles.
      new BundleTracker({filename: './webpack-stats.json'}),
      //makes jQuery available in every module
      new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        'window.jQuery': 'jquery',
        Cookies: 'Cookies',
        Cookie: 'js-cookie'
      }),
      // copies all the images to the bundle folder
      new CopyWebpackPlugin([
        { from: 'images', to: 'images' }
      ]),
      new CopyWebpackPlugin([
        { from: 'images', to: 'images' }
      ]),
      new CopyWebpackPlugin([
        { from: 'vendor', to: 'vendor' }
      ]),
      new CopyWebpackPlugin([
        { from: 'fonts', to: 'fonts' }
      ])
    ],
    devServer: {
      contentBase: '.'
    },
    watch: true,
    resolve: {
      //tells webpack where to look for modules
      modules: [path.resolve(__dirname, 'vendor'), 'node_modules'],
      //extensions that should be used to resolve modules
      extensions: ['.js', '.jsx']
    }
  }
}
