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
// import ApiService from '@/common/services/ApiService.js'
import {
  SET_KEYCLOAK
} from './mutations.types.js'
Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    keycloak: {}
  },
  mutations: {
    [SET_KEYCLOAK] (state, payload) {
      state.keycloak = payload
    }
  },
  actions: {},
  getters: {
    userRoles (state) {
      if (state.keycloak && state.keycloak.authenticated) {
        return {
          view: (state.keycloak.hasRealmRole('gwells_admin') || state.keycloak.hasRealmRole('wells_viewer')),
          edit: false,
          approve: false
        }
      } else {
        return {}
      }
    },
    keycloak (state) {
      return state.keycloak
    }
  }
})
