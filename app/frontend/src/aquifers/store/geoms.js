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

import ApiService from '@/common/services/ApiService.js'

import { FETCH_SIMPLIFIED_GEOMETRY } from './actions.types.js'
import {
  SET_SIMPLIFIED_GEOJSON_LOADING,
  SET_SIMPLIFIED_GEOJSON,
  SET_SIMPLIFIED_GEOJSON_FETCHED
} from './mutations.types.js'

export default {
  namespaced: true,
  state: {
    simplifiedGeoJson: null,
    simplifiedGeoJsonLoading: false,
    simplifiedGeoJsonFetched: false
  },
  mutations: {
    [SET_SIMPLIFIED_GEOJSON_LOADING] (state, payload) {
      state.simplifiedGeoJsonLoading = payload
    },
    [SET_SIMPLIFIED_GEOJSON] (state, payload) {
      state.simplifiedGeoJson = payload
    },
    [SET_SIMPLIFIED_GEOJSON_FETCHED] (state, payload) {
      state.simplifiedGeoJsonFetched = payload
    }
  },
  actions: {
    [FETCH_SIMPLIFIED_GEOMETRY] ({ commit, state }) {
      commit(SET_SIMPLIFIED_GEOJSON_LOADING, true)

      return ApiService.query('gis/aquifers-simplified')
        .then((response) => {
          const featuresCollection = response.data || {}
          const features = featuresCollection.features || []
          // Remove any features which don't have geometry
          featuresCollection.features = features.filter((feature) => feature.geometry)

          commit(SET_SIMPLIFIED_GEOJSON, featuresCollection)
          commit(SET_SIMPLIFIED_GEOJSON_FETCHED, true)
        })
        .catch(() => {
          commit(SET_SIMPLIFIED_GEOJSON_FETCHED, false)
          commit(SET_SIMPLIFIED_GEOJSON, [])
        })
        .finally(() => {
          commit(SET_SIMPLIFIED_GEOJSON_LOADING, false)
        })
    }
  }
}
