import { SET_KEYCLOAK } from '@/registry/store/mutations.types.js'
import { store } from '@/registry/store'
import Keycloak from 'keycloak-js'
import ApiService from '@/common/services/ApiService.js'
import Vue from 'vue'

export default {
  getInstance: function () {
    if (!Vue.prototype.$keycloak) {
      // TODO: This has to read settings from environment configuration!
      console.log('making keycloak instance')
      Vue.prototype.$keycloak = Keycloak({
        'realm': 'gwells',
        'url': 'https://dev-sso.pathfinder.gov.bc.ca/auth',
        'clientId': 'webapp-dev-local'
      })
    } else {
      console.log('already have keycloak instance')
    }
    Vue.prototype.$keycloak.onReady = (authenticated) => {
      console.log('keycloak callback : onReady', authenticated)
    }
    Vue.prototype.$keycloak.onAuthSuccess = () => {
      console.log('keycloak callback : onAuthSuccess')
    }
    Vue.prototype.$keycloak.onAuthError = () => {
      console.log('keycloak callback : onAuthError')
    }
    Vue.prototype.$keycloak.onAuthRefreshSuccess = () => {
      console.log('keycloak callback : onAuthRefreshSuccess')
    }
    Vue.prototype.$keycloak.onAuthRefreshError = () => {
      console.log('keycloak callback : onAuthRefreshError')
    }
    Vue.prototype.$keycloak.onTokenExpired = () => {
      console.log('keycloak callback : onTokenExpired')
    }
    return Vue.prototype.$keycloak
  },

  authenticate: function () {
    return new Promise((resolve, reject) => {
      console.log('authenticate.js::authenticate...')
      const instance = this.getInstance()
      if (instance.authenticated && ApiService.hasAuthHeader()) {
        console.log('skipping auth - already good to go')
        // Already authenticated. We can skip this.
        resolve()
      } else {
        const token = localStorage.getItem('token')
        const refreshToken = localStorage.getItem('refreshToken')
        const idToken = localStorage.getItem('idToken')

        console.log('authenticate.js::authenticate : going to try to init....')
        instance.init({
          onLoad: 'check-sso',
          checkLoginIframe: true,
          timeSkew: 10,
          token,
          refreshToken,
          idToken }
        ).success((result) => {
          console.log('authenticate.js::authenticate : init success, result:', result)
          store.commit(SET_KEYCLOAK, instance)
          if (instance.authenticated) {
            if (instance.isTokenExpired(0)) {
              // The token is expired!
              console.log('authenticate.js::authenticate : but wait - the token is expired!')
              result = false
              localStorage.removeItem('token')
              localStorage.removeItem('refreshToken')
              localStorage.removeItem('idToken')
              ApiService.authHeader()
            } else {
              localStorage.setItem('token', instance.token)
              localStorage.setItem('refreshToken', instance.refreshToken)
              localStorage.setItem('idToken', instance.idToken)
              ApiService.authHeader('JWT', instance.token)
            }
          }
          // We may have failed to authenticate, for many reasons, e.g. - it may be we never logged in.
          resolve(result)
        }).error((e) => {
          console.error(e)
          reject(e)
        })
      }
    })
  }
}
