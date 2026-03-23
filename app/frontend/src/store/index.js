import Vue from 'vue'
import Vuex from 'vuex'
import submissionStore from '@/submissions/store/index.js'
import wellsStore from '@/wells/store/index.js'
import qaqcStore from '@/qaqc/store/index.js'

export const store = new Vuex.Store({
  modules: {
    submissionStore,
    wellsStore,
    qaqcStore
  }
})
