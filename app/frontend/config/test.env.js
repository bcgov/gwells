'use strict'
const merge = require('webpack-merge')
const devEnv = require('./dev.env')

module.exports = merge(devEnv, {
  NODE_ENV: JSON.stringify('testing'),
  APPLICATION_ROOT: JSON.stringify('/gwells/registries'),
  ENABLE_DATA_ENTRY: JSON.stringify(true)
})
