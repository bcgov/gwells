import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/common/services/gwells'
import { FETCH_DRILLER_LIST } from './actions.types.js'
import { SET_DRILLER_LIST, SET_LOADING, SET_ERROR } from './mutations.types.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    currentUser: 'anonymous',
    loading: false,
    error: null,
    drillerList: []
  },
  mutations: {
    [SET_LOADING] (state, payload) {
      state.loading = payload
    },
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_DRILLER_LIST] (state, payload) {
      state.drillerList = payload
    }
  },
  actions: {
    [FETCH_DRILLER_LIST] ({commit}) {
      commit(SET_LOADING, true)
      ApiService.query('drillers')
        .then((response) => {
          commit(SET_LOADING, false)
          commit(SET_DRILLER_LIST, response.data)
        })
        .catch((error) => {
          commit(SET_LOADING, false)
          commit(SET_ERROR, error)
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
    drillers (state) {
      return state.drillerList
    }
  }
})
