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

import { FETCH_CODES } from './actions.types.js'
import { SET_CODES, SET_ERROR } from './mutations.types.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    auth: auth,
    config: config
  },
  state: {
    error: null,
    codes: null
  },
  mutations: {
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_CODES] (state, payload) {
      state.codes = payload
    }
  },
  actions: {
    [FETCH_CODES] ({ commit }) {
      if (!this.state.codes) {
        // fetch codes once
        ApiService.query('submissions/options').then((res) => {
          commit(SET_CODES, res.data)
        }).catch((e) => {
          commit(SET_ERROR, e.response)
        })
      }
    }
  },
  getters: {
    codes (state) {
      return state.codes || {}
    },
    globalError (state) {
      return state.error
    }
  }
})
