'use strict'
const merge = require('webpack-merge')
const devEnv = require('./dev.env')

module.exports = merge(devEnv, {
  NODE_ENV: JSON.stringify('testing'),
  APPLICATION_ROOT: JSON.stringify('/gwells/registries'),
  AXIOS_BASE_URL: process.env.AXIOS_BASE_URL ? JSON.stringify(process.env.AXIOS_BASE_URL) : JSON.stringify('/gwells/api/v1/')
})
