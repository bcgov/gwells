'use strict'

module.exports = {
  NODE_ENV: JSON.stringify('production'),
  APPLICATION_ROOT: JSON.stringify('/gwells/registries'),
  AXIOS_BASE_URL: JSON.stringify('/gwells/api/v1/'),
  ENABLE_DATA_ENTRY: process.env.ENABLE_DATA_ENTRY ? JSON.stringify(process.env.ENABLE_DATA_ENTRY === 'True' || process.env.ENABLE_DATA_ENTRY === 'true') : JSON.stringify(false),
  ENABLE_GOOGLE_ANALYTICS: process.env.ENABLE_GOOGLE_ANALYTICS ? JSON.stringify(process.env.ENABLE_GOOGLE_ANALYTICS === 'True' || process.env.ENABLE_GOOGLE_ANALYTICS === 'true') : JSON.stringify(false)
}
