import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/common/services/gwells'
import { FETCH_DRILLER, FETCH_DRILLER_LIST } from './actions.types.js'
import {
  SET_DRILLER,
  SET_DRILLER_LIST,
  SET_LOADING,
  SET_ERROR,
  SET_LIST_ERROR
} from './mutations.types.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    currentUser: 'anonymous',
    loading: false,
    error: null,
    listError: null,
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
    [SET_DRILLER] (state, payload) {
      state.currentDriller = payload
    },
    [SET_DRILLER_LIST] (state, payload) {
      state.drillerList = payload
    }
  },
  actions: {
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
      ApiService.query('drillers', params)
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
    drillers (state) {
      return state.drillerList
    },
    currentDriller (state) {
      return state.currentDriller
    }
  }
})
