import { useCommonStore } from '@/stores/common.js'

export default (to, from, next) => {
  const auth = useCommonStore.getters.keycloak
  const app = to.meta && to.meta.app
  if (to.matched.some(record => record.meta.edit)) {
    if (auth && auth.authenticated && useCommonStore.getters.userRoles[app].edit) {
      // if token is expired, send user back to home
      // otherwise, continue to next route
      auth.isTokenExpired() ? next({ name: 'SearchHome' }) : next()
    } else {
      // no auth credentials
      next({ name: 'SearchHome' })
    }
  } else if (to.matched.some(record => record.meta.view)) {
    if (auth && auth.authenticated && useCommonStore.getters.userRoles[app].view) {
      // if token is expired, send user back to home
      // otherwise, continue to next route
      auth.isTokenExpired() ? next({ name: 'SearchHome' }) : next()
    } else {
      // no auth credentials
      next({ name: 'SearchHome' })
    }
  } else {
    next({ name: 'SearchHome' })
  }
}
