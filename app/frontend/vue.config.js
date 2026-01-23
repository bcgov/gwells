module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/gwells/' : '/',
  configureWebpack: {
    resolve: {
      alias: {
        moment: 'moment/src/moment',
        lodash: 'lodash-es'
      }
    },
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 1000
      }
    }
  },
  transpileDependencies: [
    '@geolonia/mbgl-gesture-handling'
  ],
  devServer: {
    proxy: {
      '^/tiles/': {
        target: process.env.VECTOR_TILE_SERVER || 'http://localhost:7800/',
        pathRewrite: {
          '^/tiles/': '/'
        },
        changeOrigin: true
      }
    }
  }
}
