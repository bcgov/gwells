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
import ApiService from '@/common/services/ApiService.js'
import Keycloak from 'keycloak-js'
import Vue from 'vue'

export default {
  _app: null,

  setApp (app) {
    this._app = app
  },

  _setKeycloak (instance) {
    app.config.globalProperties.$keycloak = instance
  },

  getInstance: function () {
    /**
     * Returns a promise that resolves to an instance of Keycloak.
     */

    return new Promise((resolve, reject) => {
      if (!app.config.globalProperties.$keycloak) {
        ApiService.query('keycloak', {})
          .then(response => {
            const {
              'ssl-required': sslRequired,
              resource,
              realm,
              'public-client': publicClient,
              'confidential-port': confidentialPort,
              clientId,
              'auth-server-url': authServerUrl
            } = response.data

            const keycloak = new Keycloak({
              url: authServerUrl,
              realm,
              clientId,
              sslRequired,
              resource,
              publicClient,
              confidentialPort
            })
            this._setKeycloak(keycloak)
            resolve(keycloak)
          })
          .catch(error => {
            console.error(error)
            this._setKeycloak({})
            resolve(app.config.globalProperties.$keycloak)
          })
      } else {
        // Keycloak has already been loaded, so just resolve the object.
        resolve(app.config.globalProperties.$keycloak)
      }
    })
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

  scheduleRenewal (instance) {
    const expiresAt = instance.tokenParsed.exp

    // set delay to 50% of token's lifespan (in seconds), or at least 60 seconds
    let delay = (expiresAt - (Date.now() / 1000)) * 0.5
    delay = Math.max(60, delay)

    setTimeout(() => {
      this.renewToken(instance)
    }, delay * 1000)
  },

  renewToken (instance, retries = 0) {
    const maxRetries = 2

    instance.updateToken(1800).then((refreshed) => {
      if (refreshed) {
        this.setLocalToken(instance)
      }
      this.scheduleRenewal(instance)
    }).catch((e) => {
      // The refresh token is expired or was rejected
      // we will retry after 60 sec (up to the count defined by maxRetries)
      if (retries > maxRetries) {
        this.removeLocalToken()
        instance.clearToken()
      } else {
        setTimeout(() => {
          this.renewToken(instance, retries + 1)
        }, 60000)
      }
    })
  },

  authenticate: function (store) {
    /**
     * Return a promise that resolves on completion of authentication.
     */
    return new Promise((resolve, reject) => {
      this.getInstance()
        .then(async (instance) => {
          if (instance.authenticated && ApiService.hasAuthHeader() && !instance.isTokenExpired(0)) {
            // We've already authenticated, have a header, and we've not expired.
            resolve(instance)
          } else {
            try {
              // Attempt to retrieve a stored token, this may avoid us having to refresh the page.
              const token = localStorage.getItem('token')
              const refreshToken = localStorage.getItem('refreshToken')
              const idToken = localStorage.getItem('idToken')

              const authed = await instance.init({
                pkceMethod: 'S256',
                onLoad: 'check-sso',
                timeSkew: 10,
                checkLoginIframe: true,
                token,
                refreshToken,
                idToken
              })

              if (instance.authenticated) {
                // We may have been authenticated, but the token could be expired.
                instance.updateToken(60).then(() => {
                  // Store the token to avoid future round trips, and wire up the API
                  this.setLocalToken(instance)
                  // We update the store reference only after wiring up the API. (Someone might be waiting
                  // for login to complete before taking some action. )
                  // Assumes that store passed in includes a 'SET_KEYCLOAK' mutation!
                  store.commit('SET_KEYCLOAK', instance)
                  this.scheduleRenewal(instance)
                  resolve(instance)
                }).catch(() => {
                  // The refresh token is expired or was rejected
                  this.removeLocalToken()
                  instance.clearToken()
                  // We update the store reference only after wiring up the API. (Someone might be waiting
                  // for login to complete before taking some action. )
                  store.commit('SET_KEYCLOAK', instance)
                  resolve(instance)
                })
              } else {
                // We may have failed to authenticate, for many reasons, e.g. - it may be we never logged in,
                // or have an expired token.
                store.commit('SET_KEYCLOAK', instance)
                resolve(instance)
              }
            } catch (error) {
              console.error('Failed to initialize adapter:', error)
            }
          }
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
}
