/**
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 */
import Keycloak from 'keycloak-js'
import ApiService from '@/common/services/ApiService.js'
import Vue from 'vue'

export default {
  getInstance: function () {
    if (!Vue.prototype.$keycloak) {
      Vue.prototype.$keycloak = Keycloak(`${process.env.AXIOS_BASE_URL}keycloak`)
    }
    return Vue.prototype.$keycloak
  },

  setLocalToken: function (instance) {
    localStorage.setItem('token', instance.token)
    localStorage.setItem('refreshToken', instance.refreshToken)
    localStorage.setItem('idToken', instance.idToken)
    ApiService.authHeader('JWT', instance.token)
  },
  removeLocalToken: function () {
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('idToken')
    ApiService.authHeader()
  },

  authenticate: function (store) {
    /**
     * authenticates a user and then stores a reference to the keycloak instance in the store
     * passed into the function
     */
    return new Promise((resolve, reject) => {
      const instance = this.getInstance()
      if (instance.authenticated && ApiService.hasAuthHeader() && !instance.isTokenExpired(0)) {
        resolve() // We've already authenticated, have a header, and we've not expired.
      } else {
        // Attempt to retrieve a stored token, this may avoid us having to refresh the page.
        const token = localStorage.getItem('token')
        const refreshToken = localStorage.getItem('refreshToken')
        const idToken = localStorage.getItem('idToken')
        instance.init({
          onLoad: 'check-sso',
          checkLoginIframe: true,
          timeSkew: 10, // Allow for some deviation
          token,
          refreshToken,
          idToken }
        ).success((result) => {
          // assumes the store passed in includes a 'SET_KEYCLOAK' mutation.
          store.commit('SET_KEYCLOAK', instance)
          if (instance.authenticated) {
            // We may have been authenticated, but the token could be expired.
            instance.updateToken(3600).then(() => {
              // Store the token to avoid future round trips
              this.setLocalToken(instance)
            }).catch(() => {
              // The refresh token is expired or was rejected
              result = false
              this.removeLocalToken()
              instance.clearToken()
            })
          }
          instance.onTokenExpired = () => {
            instance.updateToken().then(() => {
              this.setLocalToken(instance)
            }).catch(() => {
              this.removeLocalToken()
              instance.clearToken()
            })
          }
          // We may have failed to authenticate, for many reasons, e.g. - it may be we never logged in,
          // or have an expired token.
          resolve(result)
        }).error((e) => {
          reject(e)
        })
      }
    })
  }
}
