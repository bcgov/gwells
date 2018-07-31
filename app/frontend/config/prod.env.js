'use strict'

module.exports = {
  NODE_ENV: JSON.stringify('production'),
  APPLICATION_ROOT: JSON.stringify('/gwells/registries'),
  AXIOS_BASE_URL: JSON.stringify('/gwells/api/v1/'),
  ENABLE_DATA_ENTRY: JSON.stringify(false),
  // Unless disabled, we always analytics in production.
  ENABLE_GOOGLE_ANALYTICS: process.env.ENABLE_GOOGLE_ANALYTICS ? JSON.stringify(process.env.ENABLE_GOOGLE_ANALYTICS) : JSON.stringify(true)
}
