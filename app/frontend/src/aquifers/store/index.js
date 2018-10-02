/**
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 */
import Vue from 'vue'
import Vuex from 'vuex'
import auth from '@/common/store/auth.js'
import config from '@/common/store/config.js'
import ApiService from '@/common/services/ApiService.js'

import { SEARCH_AQUIFERS, RESET_RESULTS } from './actions.types'
import {
  SET_LOADING,
  SET_LIST_ERROR,
  SET_AQUIFER_LIST
} from './mutations.types'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: { auth, config },
  state: {
    loading: null,
    error: null,
    aquifers: null
  },
  actions: {
    [SEARCH_AQUIFERS] ({ commit }, params) {
      return new Promise((resolve, reject) => {
        commit(SET_LOADING, true)
        ApiService.query('aquifers/', params)
          .then((response) => {
            commit(SET_LOADING, false)
            commit(SET_LIST_ERROR, null)
            commit(SET_AQUIFER_LIST, response.data)
            resolve()
          })
          .catch((error) => {
            commit(SET_LOADING, false)
            commit(SET_LIST_ERROR, error.response)
            reject(error)
          })
      })
    },
    [RESET_RESULTS] ({ commit }) {
      commit(SET_LOADING)
      commit(SET_LIST_ERROR)
      commit(SET_AQUIFER_LIST)
    }
  },
  mutations: {
    [SET_LOADING] (state, payload) {
      state.loading = payload
    },
    [SET_LIST_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_AQUIFER_LIST] (state, payload) {
      state.aquifers = payload
    }
  },
  getters: {
    aquiferList: state => state.aquifers && state.aquifers.results,
    emptyResults: state => state.aquifers && state.aquifers.count === 0
  }
})
