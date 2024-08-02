if (process.env.API_TARGET) {
  console.log(`Targetting the API ${process.env.API_TARGET}`)
}

process.env.VUE_CLI_TEST = false

module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/gwells/' : '/',
  configureWebpack: {
    devtool: 'source-map',
    resolve: {
      alias: {
        moment: 'moment/src/moment',
        lodash: 'lodash-es',
        vue$: '@vue/compat'
      },
      fallback: {
        'querystring': require.resolve('querystring-es3')
      }
    }
  },
  chainWebpack: config => {
    config.resolve.alias.set('vue', '@vue/compat')
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap(options => {
        return {
          ...options,
          compilerOptions: {
            compatConfig: {
              MODE: 2 // Enable Vue 2 compat mode
            }
          }
        }
      })
  },
  transpileDependencies: ['@geolonia/mbgl-gesture-handling'],
  devServer: {
    proxy: {
      '^/api/': {
        target: process.env.API_TARGET || 'http://localhost:8000/',
        pathRewrite: {
          '^/api': '/gwells/api/v2'
        }
      },
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
