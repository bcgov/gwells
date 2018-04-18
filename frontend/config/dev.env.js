'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

console.log(process.env.APPLICATION_ROOT)

module.exports = merge(prodEnv, {
  NODE_ENV: JSON.stringify('development'),
  APPLICATION_ROOT: process.env.APPLICATION_ROOT ? JSON.stringify(process.env.APPLICATION_ROOT) : JSON.stringify('/gwells/registries')
})
