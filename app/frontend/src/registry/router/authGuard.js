import { store } from '../store'

export default (to, from, next) => {
  const auth = store.getters.keycloak
  if (auth && auth.authenticated && store.getters.userIsAdmin) {
    // if token is expired, send user back to home
    // otherwise, continue to next route
    auth.isTokenExpired() ? next({ name: 'SearchHome' }) : next()
  } else {
    // no auth credentials
    next({ name: 'SearchHome' })
  }
}
