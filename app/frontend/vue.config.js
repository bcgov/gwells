module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  publicPath: import.meta.env.NODE_ENV === "production" ? "/gwells/" : "/",
  configureWebpack: {
    resolve: {
      alias: {
        moment: "moment/src/moment",
        lodash: "lodash-es",
      },
    },
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 1000,
      },
    },
  },
  transpileDependencies: ["@geolonia/mbgl-gesture-handling"],
};
