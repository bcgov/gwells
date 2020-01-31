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

import { FETCH_CODES, FETCH_WELL_TAGS } from './actions.types.js'
import { SET_CODES, SET_ERROR, SET_WELLS } from './mutations.types.js'

Vue.use(Vuex)

const submissionStore = {
  state: {
    error: null,
    codes: null,
    wells: null
  },
  mutations: {
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_CODES] (state, payload) {
      state.codes = payload
    },
    [SET_WELLS] (state, payload) {
      state.wells = payload
    }
  },
  actions: {
    [FETCH_CODES] ({ commit, state }) {
      if (state.codes === null) {
        // fetch codes once
        ApiService.query('submissions/options').then((res) => {
          commit(SET_CODES, res.data)
        }).catch((e) => {
          commit(SET_ERROR, e.response)
        })
      }
    },
    [FETCH_WELL_TAGS] ({ commit, state }) {
      if (state.wells === null) {
        // fetch the wells once
        ApiService.query('wells/tags?ordering=well_tag_number').then((res) => {
          commit(SET_WELLS, res.data)
        }).catch((e) => {
          commit(SET_ERROR, e.response)
        })
      }
    }
  },
  getters: {
    codes (state) {
      return state.codes || {
        land_district_codes: {}
      }
    },
    wells (state) {
      return state.wells
    },
    globalError (state) {
      return state.error
    }
  }
}

export default submissionStore
