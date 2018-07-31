'use strict'

module.exports = {
  NODE_ENV: JSON.stringify('production'),
  APPLICATION_ROOT: JSON.stringify('/gwells/registries'),
  AXIOS_BASE_URL: JSON.stringify('/gwells/api/v1/'),
  // Unless explicitly enabled, we always disable data entry in production.
  ENABLE_DATA_ENTRY: process.env.ENABLE_DATA_ENTRY ? JSON.stringify(process.env.ENABLE_DATA_ENTRY) : JSON.stringify(false),
  // Unless explicitly disabled, we always enable analytics in production.
  ENABLE_GOOGLE_ANALYTICS: process.env.ENABLE_GOOGLE_ANALYTICS ? JSON.stringify(process.env.ENABLE_GOOGLE_ANALYTICS) : JSON.stringify(true)
}
