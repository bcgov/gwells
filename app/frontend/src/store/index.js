import Vue from 'vue'
import Vuex from 'vuex'
import auth from '@/common/store/auth.js'
import config from '@/common/store/config.js'
import documentState from '@/common/store/documents.js'
import registriesStore from '@/registry/store/index.js'
import submissionStore from '@/submissions/store/index.js'
import aquiferStore from '@/aquifers/store/index.js'
import wellsStore from '@/wells/store/index.js'
import qaqcStore from '@/qaqc/store/index.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    auth,
    config,
    documentState,
    registriesStore,
    submissionStore,
    aquiferStore,
    wellsStore,
    qaqcStore
  }
})
