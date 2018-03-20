import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/common/services/gwells'
import {
  LOGIN,
  LOGOUT,
  FETCH_CITY_LIST,
  FETCH_DRILLER,
  FETCH_DRILLER_LIST } from './actions.types.js'
import {
  SET_ERROR,
  SET_LOADING,
  SET_LIST_ERROR,
  SET_USER,
  SET_CITY_LIST,
  SET_DRILLER,
  SET_DRILLER_LIST } from './mutations.types.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    user: null,
    loading: false,
    error: null,
    listError: null,
    cityList: {}, // object looks like: { drillers: ['Duncan', 'Atlin'], installers: ['Squamish'] }
    drillerList: [],
    currentDriller: {}
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
    }
  },
  actions: {
    [LOGIN] ({commit}, credentials) {
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
          list[activity] = response.data
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
      commit(SET_LOADING, true)
      ApiService.query('drillers/', params)
        .then((response) => {
          commit(SET_LOADING, false)
          commit(SET_LIST_ERROR, null)
          commit(SET_DRILLER_LIST, response.data)
        })
        .catch((error) => {
          commit(SET_LOADING, false)
          commit(SET_LIST_ERROR, error.response)
        })
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
    }
  }
})
