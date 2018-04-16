'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  ENABLE_DATA_ENTRY: 'false',
  NODE_ENV: '"development"'
})
