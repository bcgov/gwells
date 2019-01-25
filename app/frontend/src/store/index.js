import Vue from 'vue'
import Vuex from 'vuex'
import auth from '@/common/store/auth.js'
import config from '@/common/store/config.js'
import documentState from '@/common/store/documents.js'
import registriesStore from '@/registry/store/index.js'
import submissionStore from '@/submissions/store/index.js'
import aquiferCodes from '@/aquifers/store/codes.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    auth: auth,
    config: config,
    documentState: documentState,
    registriesStore: registriesStore,
    submissionStore: submissionStore,
    aquiferCodes: aquiferCodes
  }
})
