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
import ApiService from '@/common/services/ApiService.js'

import { FETCH_DRILLER_NAMES, FETCH_ORGANIZATION_NAMES } from './actions.types.js'
import { SET_DRILLER_NAMES, SET_ERROR, SET_ORGANIZATION_NAMES } from './mutations.types.js'

Vue.use(Vuex)

const wellsStore = {
  state: {
    error: null,
    drillerNames: null,
    organizationNames: null
  },
  mutations: {
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_DRILLER_NAMES] (state, payload) {
      state.drillerNames = payload
    },
    [SET_ORGANIZATION_NAMES] (state, payload) {
      state.organizationNames = payload
    }
  },
  actions: {
    [FETCH_DRILLER_NAMES] ({ commit }) {
      if (!this.state.drillerNames) {
        // fetch codes once
        ApiService.query('drillers/names').then((res) => {
          commit(SET_DRILLER_NAMES, res.data)
        }).catch((e) => {
          commit(SET_ERROR, e.response)
        })
      }
    },
    [FETCH_ORGANIZATION_NAMES] ({ commit }) {
      if (!this.state.organizationNames) {
        // fetch the wells once
        ApiService.query('organizations/names').then((res) => {
          commit(SET_ORGANIZATION_NAMES, res.data)
        }).catch((e) => {
          commit(SET_ERROR, e.response)
        })
      }
    }
  },
  getters: {
    drillerNames (state) {
      return state.drillerNames
    },
    organizationNames (state) {
      return state.organizationNames
    }
  }
}

export default wellsStore
