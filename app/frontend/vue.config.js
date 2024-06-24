if (process.env.API_TARGET) {
  console.log(`Targetting the API ${process.env.API_TARGET}`)
}

const { VueLoaderPlugin } = require('vue-loader')
const webpack = require('webpack');

module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/gwells/' : '/',
  configureWebpack: {
    resolve: {
      alias: {
        moment: 'moment/src/moment',
        lodash: 'lodash-es',
        vue$: '@vue/compat'
      },
      fallback: {
        'querystring': require.resolve('querystring-es3')
      }
    },
    // module: {
    //   rules: [
    //     {
    //       test: /\.vue$/,
    //       loader: 'vue-loader',
    //       options: {
    //         compilerOptions: {
    //           compatConfig: {
    //             MODE: 2 // Enable Vue 2 compat mode
    //           }
    //         }
    //       }
    //     }
    //   ]
    // },
    plugins: [
      new VueLoaderPlugin(),
      new webpack.ProgressPlugin()
    ],
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 1000
      }
    }
  },
  chainWebpack: config => {
    config.module
      .rule('vue')
      .use('vue-loader')
      .loader('vue-loader')
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
          '^/api': '/gwells/api/v2',
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
