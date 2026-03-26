import Vue from 'vue'
import Vuex from 'vuex'
import auth from '@/common/store/auth.js'
import config from '@/common/store/config.js'
import documentState from '@/common/store/documents.js'
import submissionStore from '@/submissions/store/index.js'
import wellsStore from '@/wells/store/index.js'
import qaqcStore from '@/qaqc/store/index.js'

export const store = new Vuex.Store({
  modules: {
    auth,
    config,
    documentState,
    submissionStore,
    wellsStore,
    qaqcStore
  }
})
