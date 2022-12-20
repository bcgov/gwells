/*
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

export default {
  namespaced: true,
  state: {
    id: null,
    record: {},
    aquiferFiles: {
      public: [],
      private: []
    },
    aquiferWells: []
  },
  mutations: {
    setAquiferRecord (state, payload) {
      state.record = payload
      state.id = payload.aquifer_id || null
    },
    setAquiferFiles (state, payload) {
      state.aquiferFiles = payload
    },
    setAquiferWells (state, payload) {
      state.aquiferWells = payload
    }
  },
  actions: {
    resetAquiferData ({ commit, state }) {
      commit('setAquiferRecord', {})
      commit('setAquiferFiles', {
        public: [],
        private: []
      })
      commit('setAquiferWells', [])
    }
  },
  getters: {
    wellsWithAquiferCorrelation: (state) => {
      return state.aquiferWells.filter((w) => w.aquifer_id === state.id)
    },
    wellsWithoutAquiferCorrelation: (state) => {
      return state.aquiferWells.filter((w) => w.aquifer_id === null)
    },
    wellsCorrelatedWithADifferentAquifer: (state) => {
      return state.aquiferWells.filter((w) => w.aquifer_id !== state.id)
    }
  }
}
