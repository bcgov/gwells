import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/common/services/gwells'
import {
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

const logging = true

export const store = new Vuex.Store({
  state: {
    user: null,
    loading: false,
    error: null,
    listError: null,
    cityList: [],
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
      logging && console.log('switched to user', payload && payload.username)
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
    [FETCH_CITY_LIST] ({commit}, activity) {
      logging && console.log('fetching city list...')
      ApiService.query('cities/' + activity + '/')
        .then((response) => {
          commit(SET_CITY_LIST, response.data)
          logging && console.log('fetched city list:', response.data)
        })
        .catch((error) => {
          commit(SET_ERROR, error.response)
          logging && console.log('error fetching cities:', error.response)
        })
    },
    [FETCH_DRILLER] ({commit}, guid) {
      logging && console.log('fetching driller...')
      commit(SET_LOADING, true)
      ApiService.get('drillers', guid)
        .then((response) => {
          commit(SET_LOADING, false)
          commit(SET_ERROR, null)
          commit(SET_DRILLER, response.data)
          logging && console.log('fetched driller:', response.data)
        })
        .catch((error) => {
          commit(SET_LOADING, false)
          commit(SET_ERROR, error.response)
          logging && console.log('error fetching driller:', error.response)
        })
    },
    [FETCH_DRILLER_LIST] ({commit}, params) {
      commit(SET_LOADING, true)
      logging && console.log('fetching driller list...')
      ApiService.query('drillers/', params)
        .then((response) => {
          commit(SET_LOADING, false)
          commit(SET_LIST_ERROR, null)
          commit(SET_DRILLER_LIST, response.data)
          logging && console.log('fetched driller list:', response.data)
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
