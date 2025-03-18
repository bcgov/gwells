const webpack = require('webpack');

if (process.env.API_TARGET) {
  console.log(`Targetting the API ${process.env.API_TARGET}`);
}

module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/gwells/' : '/',
  configureWebpack: {
    resolve: {
      alias: {
        moment: 'moment/src/moment',
        lodash: 'lodash-es',
        querystring: 'querystring-es3',
        buffer: 'buffer',
        util: 'util',
      },
      fallback: {
        process: require.resolve('process/browser')
      }
    },
    plugins: [
      new webpack.ProvidePlugin({
        process: 'process/browser',
        Buffer: ['buffer', 'Buffer'],
        querystring: 'querystring-es3',
      }),
    ],
  },
  transpileDependencies: ['@geolonia/mbgl-gesture-handling'],
  devServer: {
    proxy: {
      '^/api/': {
        target: process.env.API_TARGET || 'http://localhost:8000/',
        pathRewrite: {
          '^/api': '/gwells/api/v2',
        },
      },
      '^/tiles/': {
        target: process.env.VECTOR_TILE_SERVER || 'http://localhost:7800/',
        pathRewrite: {
          '^/tiles/': '/',
        },
        changeOrigin: true,
      },
    },
    devMiddleware: {},
  },
};
