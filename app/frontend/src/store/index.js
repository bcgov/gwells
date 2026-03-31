import Vue from 'vue'
import Vuex from 'vuex'
import wellsStore from '@/wells/store/index.js'

export const store = new Vuex.Store({
  modules: {
    wellsStore
  }
})
