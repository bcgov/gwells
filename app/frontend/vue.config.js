module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/gwells/' : '/',
  configureWebpack: {
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 1000
      }
    }
  }
}
