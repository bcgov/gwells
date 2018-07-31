'use strict'
const merge = require('webpack-merge')
const devEnv = require('./dev.env')

module.exports = merge(devEnv, {
  NODE_ENV: JSON.stringify('testing'),
  APPLICATION_ROOT: JSON.stringify('/gwells/registries'),
  AXIOS_BASE_URL: process.env.AXIOS_BASE_URL ? JSON.stringify(process.env.AXIOS_BASE_URL) : JSON.stringify('/gwells/api/v1/'),
  // TODO: Move ENABLE_DATA_ENTRY setting to API endpoint
  ENABLE_DATA_ENTRY: process.env.ENABLE_DATA_ENTRY ? JSON.stringify(process.env.ENABLE_DATA_ENTRY === 'True' || process.env.ENABLE_DATA_ENTRY === 'true') : JSON.stringify(false)
})
