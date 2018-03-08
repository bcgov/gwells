import { store } from '../store'
import ApiService from '@/common/services/gwells'
import { SET_USER } from '@/registry/store/mutations.types'

export default (to, from, next) => {
  var ts = Math.round((new Date()).getTime() / 1000)
  var token = localStorage.getItem('token')
  var expiry = localStorage.getItem('tokenExpiry')
  var user = localStorage.getItem('username')
  if (token && user) {
    if (expiry > ts) {
      if (store.getters.user && store.getters.user.username === user) {
        next()
      } else {
        store.commit(SET_USER, { username: user })
        ApiService.authHeader('JWT ', token)
        next()
      }
    } else {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('tokenExpiry')
      next('/')
    }
  } else {
    next('/')
  }
}
