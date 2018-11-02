import Vue from 'vue'
import Vuex from 'vuex'
import auth from '@/common/store/auth.js'
import config from '@/common/store/config.js'
import aquiferCodes from './codes.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: { auth, aquiferCodes, config }
})
