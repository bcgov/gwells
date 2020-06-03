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
import axios from 'axios'
import querystring from 'querystring'

import ApiService from '@/common/services/ApiService.js'

import {
  SEARCH_AQUIFERS
} from './actions.types.js'
import {
  SET_ERROR,
  SET_SEARCH_BOUNDS,
  SET_SEARCH_ERRORS,
  SET_SEARCH_RESULTS,
  SET_SEARCH_RESULT_COUNT,
  SET_PENDING_SEARCH,
  SET_SEARCH_PERFORMED,
  SET_SEARCH_IN_PROGRESS,
  RESET_SEARCH,
  SET_CONSTRAIN_SEARCH,
  SET_SEARCH_QUERY,
  SET_SELECTED_SECTIONS,
  SET_MATCH_ANY,
  SET_SEARCH_MAP_CENTRE,
  SET_SEARCH_MAP_ZOOM
} from './mutations.types.js'

const HYDRAULICALLY_CONNECTED_CODE = 'Hydra'

Vue.use(Vuex)

const aquiferSearchStore = {
  namespaced: true,
  state: {
    mapBounds: null,
    searchQuery: '',
    searchErrors: {},
    searchResults: [],
    searchResultCount: 0,
    selectedSections: [],
    searchMatchAny: false,
    pendingSearch: null,
    searchInProgress: false,
    searchPerformed: false,
    constrainSearch: false,
    searchMapCentre: null,
    searchMapZoom: null
  },
  mutations: {
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_CONSTRAIN_SEARCH] (state, payload) {
      state.constrainSearch = payload
    },
    [SET_SEARCH_PERFORMED] (state) {
      state.searchPerformed = true
    },
    [SET_SEARCH_IN_PROGRESS] (state, payload) {
      state.searchInProgress = payload
    },
    [SET_PENDING_SEARCH] (state, payload) {
      state.pendingSearch = payload
    },
    [SET_SEARCH_BOUNDS] (state, payload) {
      state.mapBounds = payload
    },
    [SET_SEARCH_ERRORS] (state, payload) {
      state.searchErrors = payload
    },
    [SET_SEARCH_QUERY] (state, payload) {
      state.searchQuery = payload || ''
    },
    [SET_SELECTED_SECTIONS] (state, payload) {
      state.selectedSections = payload
    },
    [SET_MATCH_ANY] (state, payload) {
      state.searchMatchAny = payload
    },
    [SET_SEARCH_RESULTS] (state, payload) {
      state.searchResults = payload
    },
    [SET_SEARCH_RESULT_COUNT] (state, payload) {
      state.searchResultCount = payload
    },
    [SET_SEARCH_MAP_CENTRE] (state, payload) {
      state.searchMapCentre = payload
    },
    [SET_SEARCH_MAP_ZOOM] (state, payload) {
      state.searchMapZoom = payload
    },
    [RESET_SEARCH] (state, payload) {
      state.searchResults = []
      state.searchQuery = ''
      state.selectedSections = []
      state.searchResultCount = 0
      state.searchPerformed = false
      state.searchMatchAny = false
      // state.aquifer_id = ''
      state.selectedSections = []
      state.currentPage = 1
      state.noSearchCriteriaError = false
      state.searchErrors = {}
      state.searchInProgress = false
      state.constrainSearch = false
      state.mapBounds = null
      state.searchMapCentre = null
      state.searchMapZoom = null
    }
  },
  actions: {
    [SEARCH_AQUIFERS] ({ commit, state }, { query, selectedSections, matchAny }) {
      commit(SET_SEARCH_PERFORMED)
      commit(SET_SEARCH_IN_PROGRESS, true)
      commit(SET_SEARCH_QUERY, query)
      commit(SET_SELECTED_SECTIONS, selectedSections)
      commit(SET_MATCH_ANY, Boolean(matchAny))

      // trigger the Google Analytics search event
      // trigger the search event, sending along the search params as a string
      if (window.ga) {
        window.ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'AquiferSearch',
          eventLabel: querystring.stringify(state.searchQuery)
        })
      }

      if (state.pendingSearch) {
        state.pendingSearch.cancel()
      }

      const cancelSource = axios.CancelToken.source()
      commit(SET_PENDING_SEARCH, cancelSource)

      let params = aquiferSearchStore.getters.searchParams(state)

      ApiService.query('aquifers', params, { cancelToken: (cancelSource || {}).token })
        .then((response) => {
          commit(SET_SEARCH_ERRORS, {})
          const responseData = response.data || { count: 0, results: [] }
          const searchResults = responseData.results
          commit(SET_SEARCH_RESULTS, searchResults)
          commit(SET_SEARCH_RESULT_COUNT, responseData.count)
          commit(SET_SEARCH_IN_PROGRESS, false)
          commit(SET_PENDING_SEARCH, null)
        }).catch((err) => {
          // If the search was cancelled, a new one is pending, so don't bother resetting.
          if (axios.isCancel(err)) {
            return
          }

          if (err.response && err.response.data) {
            commit(SET_SEARCH_ERRORS, err.response.data)
          }
          commit(SET_SEARCH_RESULTS, null)
          commit(SET_SEARCH_RESULT_COUNT, 0)
          commit(SET_PENDING_SEARCH, null)
        })
    }
  },
  getters: {
    queryParams (state) {
      const params = {}

      if (state.searchQuery.trim()) {
        params.search = state.searchQuery
      }

      const codes = state.selectedSections.filter((s) => {
        if (s === HYDRAULICALLY_CONNECTED_CODE) {
          return false
        }
        return true
      })
      if (codes.length > 0) {
        params.resources__section__code = codes.join(',')
      }

      if (state.searchMatchAny) {
        params.match_any = String(state.searchMatchAny)
      }

      if (state.selectedSections.find((o) => o === HYDRAULICALLY_CONNECTED_CODE)) {
        params.hydraulically_connected = 'yes'
      }

      if (state.searchMapCentre) {
        params.map_centre = `${state.searchMapCentre.lat.toFixed(6)},${state.searchMapCentre.lng.toFixed(6)}`
      }
      if (state.searchMapZoom) {
        params.map_zoom = String(state.searchMapZoom)
      }
      if (state.constrainSearch) {
        params.constrain = String(state.constrainSearch)
      }

      return params
    },
    searchParams (state) {
      const params = aquiferSearchStore.getters.queryParams(state)

      if (state.constrainSearch && state.mapBounds) {
        const bounds = state.mapBounds
        const mapBBox = {
          sw_lat: bounds.getSouthWest().lat,
          sw_long: bounds.getSouthWest().lng,
          ne_lat: bounds.getNorthEast().lat,
          ne_long: bounds.getNorthEast().lng
        }

        Object.assign(params, mapBBox)
      }

      return params
    },
    searchResults (state) {
      const now = new Date()
      return state.searchResults.map((result) => {
        return {
          ...result,
          retire_date: new Date(result.retire_date) <= now ? result.retire_date : null
        }
      })
    }
  }
}

export default aquiferSearchStore
