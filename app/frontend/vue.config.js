module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/gwells/' : '/',
  configureWebpack: {
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 1000
      },
    }
  },
  devServer: {
    proxy: {
      '^/api/': {
        // target: 'http://backend:8000/',
        target: 'https://gwells-staging.pathfinder.gov.bc.ca/',
        pathRewrite: {
          '^/api': '/gwells/api/v2'
        }
      }
    }
  }
}
