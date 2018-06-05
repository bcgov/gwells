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
import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import {
  LOGIN,
  LOGOUT,
  FETCH_CITY_LIST,
  FETCH_DRILLER,
  FETCH_DRILLER_LIST,
  FETCH_DRILLER_OPTIONS} from './actions.types.js'
import {
  SET_ERROR,
  SET_LOADING,
  SET_LIST_ERROR,
  SET_USER,
  SET_CITY_LIST,
  SET_DRILLER,
  SET_DRILLER_LIST,
  SET_KEYCLOAK,
  SET_DRILLER_OPTIONS,
  SET_LAST_SEARCHED_ACTIVITY } from './mutations.types.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    user: null,
    loading: false,
    error: null,
    listError: null,
    cityList: {},
    drillerList: [],
    currentDriller: {},
    keycloak: {},
    drillerOptions: null,
    lastSearchedActivity: 'DRILL'
  },
  mutations: {
    [SET_LOADING] (state, payload) {
      state.loading = payload
    },
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_LIST_ERROR] (state, payload) {
      state.listError = payload
    },
    [SET_USER] (state, payload) {
      state.user = payload
    },
    [SET_CITY_LIST] (state, payload) {
      state.cityList = payload
    },
    [SET_DRILLER] (state, payload) {
      state.currentDriller = payload
    },
    [SET_DRILLER_LIST] (state, payload) {
      state.drillerList = payload
    },
    [SET_KEYCLOAK] (state, payload) {
      state.keycloak = payload
    },
    [SET_DRILLER_OPTIONS] (state, payload) {
      state.drillerOptions = payload
    },
    [SET_LAST_SEARCHED_ACTIVITY] (state, payload) {
      state.lastSearchedActivity = payload
    }
  },
  actions: {
    async [LOGIN] ({commit}, credentials) {
      ApiService.post('api-token-auth/', credentials)
        .then((response) => {
          const token = response.data.token
          localStorage.setItem('token', token)

          // decode JWT token for username and expiry
          const base64Url = token.split('.')[1]
          const base64 = base64Url.replace('-', '+').replace('_', '/')
          const jsonData = JSON.parse(window.atob(base64))
          localStorage.setItem('username', jsonData.username)
          localStorage.setItem('tokenExpiry', jsonData.exp)

          // Add token to headers when making API calls
          ApiService.authHeader('JWT', token)
          commit(SET_USER, jsonData)
        })
        .catch((error) => {
          commit(SET_ERROR, error.response)
        })
    },
    [LOGOUT] ({commit}) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('tokenExpiry')
      ApiService.authHeader()
      commit(SET_USER, null)
    },
    [FETCH_CITY_LIST] ({commit}, activity) {
      ApiService.query('cities/' + activity + '/')
        .then((response) => {
          const list = Object.assign({}, this.state.cityList)
          const data = response.data
          const listByProvince = []

          /**
           * iterate through each item in the response data and filter cities into
           * an array of provinces. e.g.:
           *
           * listByProvince = [
           *   {
           *     prov: 'BC',
           *     cities: [
           *       'Duncan',
           *       'Victoria'
           *     ]
           *   },
           *   {
           *     prov: 'AB',
           *     cities: [
           *       'Jasper',
           *       'Hinton'
           *     ]
           *   }
           * ]
           *
           */
          data.forEach((item) => {
            // if a province doesn't exist in listByProvince, create a new item
            if (!listByProvince.some(prov => prov.prov === item.province_state)) {
              listByProvince.push({ prov: item.province_state, cities: [] })
            }
            listByProvince.find(prov => prov.prov === item.province_state).cities.push(item.city)
          })

          // set the list for the activity (driller or well installer) to the list of provinces/cities
          list[activity] = listByProvince
          commit(SET_CITY_LIST, list)
        })
        .catch((error) => {
          commit(SET_ERROR, error.response)
        })
    },
    [FETCH_DRILLER] ({commit}, guid) {
      commit(SET_LOADING, true)
      ApiService.get('drillers', guid)
        .then((response) => {
          commit(SET_LOADING, false)
          commit(SET_ERROR, null)
          commit(SET_DRILLER, response.data)
        })
        .catch((error) => {
          commit(SET_LOADING, false)
          commit(SET_ERROR, error.response)
        })
    },
    [FETCH_DRILLER_LIST] ({commit}, params) {
      return new Promise((resolve, reject) => {
        commit(SET_LOADING, true)
        ApiService.query('drillers/', params)
          .then((response) => {
            commit(SET_LOADING, false)
            commit(SET_LIST_ERROR, null)
            commit(SET_DRILLER_LIST, response.data)
            resolve()
          })
          .catch((error) => {
            commit(SET_LOADING, false)
            commit(SET_LIST_ERROR, error.response)
            reject(error)
          })
      })
    },
    [FETCH_DRILLER_OPTIONS] ({commit}, params) {
      // We only fetch driller options if we don't already have a copy cached
      if (!this.state.drillerOptions) {
        return new Promise((resolve, reject) => {
          commit(SET_LOADING, true)
          ApiService.query('drillers/options/', params)
            .then((response) => {
              commit(SET_LOADING, false)
              commit(SET_DRILLER_OPTIONS, response.data)
            })
            .catch((error) => {
              commit(SET_LOADING, false)
              reject(error)
            })
        })
      }
    }
  },
  getters: {
    loading (state) {
      return state.loading
    },
    error (state) {
      return state.error
    },
    listError (state) {
      return state.listError
    },
    user (state) {
      return state.user
    },
    cityList (state) {
      return state.cityList
    },
    drillers (state) {
      return state.drillerList
    },
    currentDriller (state) {
      return state.currentDriller
    },
    keycloak (state) {
      return state.keycloak
    },
    userIsAdmin (state) {
      if (state.keycloak && state.keycloak.authenticated) {
        return state.keycloak.hasRealmRole('gwells_admin')
      }
      return false
    },
    userRoles (state) {
      if (state.keycloak && state.keycloak.authenticated) {
        return {
          view: (state.keycloak.hasRealmRole('gwells_admin') ||
            state.keycloak.hasRealmRole('registries_statutory_authority') ||
            state.keycloak.hasRealmRole('registries_viewer') ||
            state.keycloak.hasRealmRole('registries_adjudicator')),
          edit: (state.keycloak.hasRealmRole('gwells_admin') ||
            state.keycloak.hasRealmRole('registries_statutory_authority') ||
            state.keycloak.hasRealmRole('registries_adjudicator')),
          approve: (state.keycloak.hasRealmRole('gwells_admin') ||
            state.keycloak.hasRealmRole('registries_statutory_authority'))
        }
      } else {
        return {}
      }
    },
    drillerOptions (state) {
      return state.drillerOptions
    },
    activity (state) {
      /**
       * last searched activity, exposed to components as "activity"
       */
      return state.lastSearchedActivity
    }
  }
})
