import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    currentUser: 'anonymous',
    loading: false,
    error: null
  },
  mutations: {},
  actions: {},
  getters: {}
})
