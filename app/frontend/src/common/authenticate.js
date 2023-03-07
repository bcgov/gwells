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
import Vue from 'vue'

export default {
  getInstance: function () {
    /**
     * Returns a promise that resolves to an instance of Keycloak.
     */
    return new Promise((resolve, reject) => {
      if (!Vue.prototype.$keycloak) {
        // Keycloak has not yet been loaded, get Keycloak configuration from the server.
        ApiService.query('keycloak', {})
          .then(response => {
            /*
            "A best practice is to load the JavaScript adapter directly from Keycloak Server as it will
            automatically be updated when you upgrade the server. If you copy the adapter to your web
            application instead, make sure you upgrade the adapter only after you have upgraded the server.";
            source : https://www.keycloak.org/docs/latest/securing_apps/index.html#_javascript_adapter:
            */
            const jsUrl = `${response.data['auth-server-url']}/js/keycloak.js`
            // Inject the Keycloak javascript into the DOM.
            const keyCloakScript = document.createElement('script')
            keyCloakScript.onload = () => {
              // Construct the Keycloak object and resolve the promise.
              Vue.prototype.$keycloak = window.Keycloak(response.data)
              resolve(Vue.prototype.$keycloak)
            }
            keyCloakScript.onerror = (e) => {
              // This is pretty bad - keycloak didn't load - this should never ever happen.
              // There's not much we can do, so we set keycloak to a random empty object and resolve.
              console.error(e)
              Vue.prototype.$keycloak = {}
              resolve(Vue.prototype.$keycloak)
            }
            keyCloakScript.async = true
            keyCloakScript.setAttribute('src', jsUrl)
            document.head.appendChild(keyCloakScript)
          })
          .catch(error => {
            Vue.prototype.$keycloak = {}
            reject(error)
          })
      } else {
        // Keycloak has already been loaded, so just resolve the object.
        resolve(Vue.prototype.$keycloak)
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

    instance.updateToken(1800).success((refreshed) => {
      if (refreshed) {
        this.setLocalToken(instance)
      }
      this.scheduleRenewal(instance)
    }).error((e) => {
      console.log(e)
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
        .then((instance) => {
          if (instance.authenticated && ApiService.hasAuthHeader() && !instance.isTokenExpired(0)) {
            // We've already authenticated, have a header, and we've not expired.
            resolve(instance)
          } else {
            // Attempt to retrieve a stored token, this may avoid us having to refresh the page.
            const token = localStorage.getItem('token')
            const refreshToken = localStorage.getItem('refreshToken')
            const idToken = localStorage.getItem('idToken')
            instance.init({
              pkceMethod: 'S256',
              onLoad: 'check-sso',
              checkLoginIframe: true,
              timeSkew: 10, // Allow for some deviation
              token,
              refreshToken,
              idToken }
            ).success((result) => {
              if (instance.authenticated) {
                // We may have been authenticated, but the token could be expired.
                instance.updateToken(60).success(() => {
                  // Store the token to avoid future round trips, and wire up the API
                  this.setLocalToken(instance)
                  // We update the store reference only after wiring up the API. (Someone might be waiting
                  // for login to complete before taking some action. )
                  // Assumes that store passed in includes a 'SET_KEYCLOAK' mutation!
                  store.commit('SET_KEYCLOAK', instance)
                  this.scheduleRenewal(instance)
                  resolve(instance)
                }).error(() => {
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
            }).error((e) => {
              reject(e)
            })
          }
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
}
