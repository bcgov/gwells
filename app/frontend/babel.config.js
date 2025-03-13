module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        targets: 'es2020', // Specifies targeting ECMAScript 2020
        useBuiltIns: 'usage', // Only include polyfills for features actually used in your code
        corejs: 3 // Specify the version of core-js to use (recommended to use core-js 3)
      }
    ]
  ]
}
