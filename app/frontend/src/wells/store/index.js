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
import ApiService from '@/common/services/ApiService.js'

import {
  FETCH_DRILLER_NAMES,
  FETCH_ORGANIZATION_NAMES,
  RESET_WELLS_SEARCH,
  SEARCH_WELLS,
  SEARCH_WELL_LOCATIONS
} from './actions.types.js'
import {
  SET_DRILLER_NAMES,
  SET_ERROR,
  SET_LOCATION_ERRORS,
  SET_LOCATION_PENDING_SEARCH,
  SET_LOCATION_SEARCH_RESULTS,
  SET_LOCATION_SEARCH_RESULT_COUNT,
  SET_ORGANIZATION_NAMES,
  SET_PENDING_SEARCH,
  SET_SEARCH_BOUNDS,
  SET_SEARCH_LIMIT,
  SET_SEARCH_OFFSET,
  SET_SEARCH_ORDERING,
  SET_SEARCH_ERRORS,
  SET_SEARCH_PARAMS,
  SET_SEARCH_RESULT_COLUMNS,
  SET_SEARCH_RESULT_COUNT,
  SET_SEARCH_RESULT_FILTERS,
  SET_SEARCH_RESULTS
} from './mutations.types.js'

Vue.use(Vuex)

const cleanParams = (payload) => {
  // Clear any null or empty string values, to keep URLs clean.
  return Object.entries(payload).filter(([key, value]) => {
    return !(value === undefined || value === '' || value === null)
  }).reduce((cleanedParams, [key, value]) => {
    cleanedParams[key] = value
    return cleanedParams
  }, {})
}

const wellsStore = {
  state: {
    error: null,
    drillerNames: [],
    locationErrors: {},
    locationPendingSearch: null,
    locationSearchResults: [],
    locationSearchResultCount: 0,
    organizationNames: [],
    pendingSearch: null,
    searchBounds: {},
    searchErrors: {},
    searchLimit: 10,
    searchOffset: 0,
    searchOrdering: '-well_tag_number',
    searchParams: {},
    searchResultColumns: [
      'wellTagNumber',
      'identificationPlateNumber',
      'ownerName',
      'streetAddress',
      'legalLot',
      'legalPlan',
      'legalDistrictLot',
      'landDistrict',
      'legalPid',
      'diameter',
      'finishedWellDepth'
    ],
    // searchResultFilters provides a second level of filtering.
    searchResultFilters: {},
    searchResults: null,
    searchResultCount: 0
  },
  mutations: {
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_DRILLER_NAMES] (state, payload) {
      state.drillerNames = payload
    },
    [SET_LOCATION_ERRORS] (state, payload) {
      state.locationErrors = payload
    },
    [SET_LOCATION_PENDING_SEARCH] (state, payload) {
      state.locationPendingSearch = payload
    },
    [SET_LOCATION_SEARCH_RESULTS] (state, payload) {
      state.locationSearchResults = payload
    },
    [SET_LOCATION_SEARCH_RESULT_COUNT] (state, payload) {
      state.locationSearchResultCount = payload
    },
    [SET_ORGANIZATION_NAMES] (state, payload) {
      state.organizationNames = payload
    },
    [SET_PENDING_SEARCH] (state, payload) {
      state.pendingSearch = payload
    },
    [SET_SEARCH_BOUNDS] (state, payload) {
      state.searchBounds = payload
    },
    [SET_SEARCH_ERRORS] (state, payload) {
      state.searchErrors = payload
    },
    [SET_SEARCH_LIMIT] (state, payload) {
      if (!(payload === 10 || payload === 25 || payload === 50)) {
        return
      }
      state.searchLimit = payload
    },
    [SET_SEARCH_OFFSET] (state, payload) {
      state.searchOffset = payload
    },
    [SET_SEARCH_ORDERING] (state, payload) {
      state.searchOrdering = payload
    },
    [SET_SEARCH_PARAMS] (state, payload) {
      state.searchParams = cleanParams(payload)
    },
    [SET_SEARCH_RESULT_COLUMNS] (state, payload) {
      state.searchResultColumns = payload
    },
    [SET_SEARCH_RESULT_FILTERS] (state, payload) {
      state.searchResultFilters = cleanParams(payload)
    },
    [SET_SEARCH_RESULTS] (state, payload) {
      state.searchResults = payload
    },
    [SET_SEARCH_RESULT_COUNT] (state, payload) {
      state.searchResultCount = payload
    }
  },
  actions: {
    [FETCH_DRILLER_NAMES] ({ commit }) {
      // fetch only once
      if (!this.state.drillerNames) {
        ApiService.query('drillers/names').then((response) => {
          commit(SET_DRILLER_NAMES, response.data)
        }).catch((err) => {
          commit(SET_ERROR, err.response)
        })
      }
    },
    [FETCH_ORGANIZATION_NAMES] ({ commit }) {
      // fetch only once
      if (!this.state.organizationNames) {
        ApiService.query('organizations/names').then((response) => {
          commit(SET_ORGANIZATION_NAMES, response.data)
        }).catch((err) => {
          commit(SET_ERROR, err.response)
        })
      }
    },
    [RESET_WELLS_SEARCH] ({ commit }) {
      commit(SET_SEARCH_PARAMS, {})
      commit(SET_SEARCH_ERRORS, {})
      commit(SET_SEARCH_RESULTS, null)
      commit(SET_SEARCH_RESULT_COUNT, 0)
    },
    [SEARCH_WELLS] ({ commit, state }, { bounded = false }) {
      return new Promise((resolve, reject) => {
        if (state.pendingSearch !== null) {
          state.pendingSearch.cancel()
        }
        commit(SET_PENDING_SEARCH, axios.CancelToken.source())

        const params = { ...state.searchParams }

        if (Object.entries(state.searchResultFilters).length > 0) {
          params['filter_group'] = JSON.stringify(state.searchResultFilters)
        }
        // if triggering the search using the map, the search will be restricted to
        // the visible map bounds
        if (bounded) {
          Object.assign(params, state.searchBounds)
        }

        params['limit'] = state.searchLimit
        params['offset'] = state.searchOffset
        params['ordering'] = state.searchOrdering

        ApiService.query('wells', params, { cancelToken: state.pendingSearch.token }).then((response) => {
          commit(SET_SEARCH_ERRORS, {})
          commit(SET_SEARCH_RESULTS, response.data.results)
          commit(SET_SEARCH_RESULT_COUNT, response.data.count)
          resolve(response.data)
        }).catch((err) => {
          if (err.response && err.response.data) {
            commit(SET_SEARCH_ERRORS, err.response.data)
          }
          reject(err)
        }).finally(() => {
          commit(SET_PENDING_SEARCH, null)
        })
      })
    },
    [SEARCH_WELL_LOCATIONS] ({ commit, state }, { bounded = false }) {
      return new Promise((resolve, reject) => {
        if (state.locationPendingSearch) {
          state.locationPendingSearch.cancel()
        }
        commit(SET_LOCATION_PENDING_SEARCH, axios.CancelToken.source())

        const params = { ...state.searchParams }

        if (Object.entries(state.searchResultFilters).length > 0) {
          params['filter_group'] = JSON.stringify(state.searchResultFilters)
        }

        // if triggering the search using the map, the search will be restricted to
        // the visible map bounds
        if (bounded) {
          Object.assign(params, state.searchBounds)
        }

        ApiService.query('wells/locations', params, { cancelToken: state.locationPendingSearch.token }).then((response) => {
          const locations = response.data.map((well) => {
            return [well.latitude, well.longitude, well.well_tag_number, well.identification_plate_number]
          })
          commit(SET_LOCATION_ERRORS, {})
          commit(SET_LOCATION_SEARCH_RESULTS, locations)
          commit(SET_LOCATION_SEARCH_RESULT_COUNT, response.data.count)
          resolve(locations)
        }).catch((err) => {
          if (err.response && err.response.data) {
            commit(SET_LOCATION_ERRORS, err.response.data)
          }
          commit(SET_LOCATION_SEARCH_RESULTS, [])
        }).finally(() => {
          commit(SET_LOCATION_PENDING_SEARCH, null)
        })
      })
    }
  },
  getters: {
    drillerNames (state) {
      return state.drillerNames
    },
    locationErrors (state) {
      return state.locationErrors
    },
    locationErrorMessage (state) {
      if (Object.entries(state.locationErrors).length === 0 && state.locationErrors.constructor === Object) {
        return ''
      } else {
        return state.locationErrors.detail
      }
    },
    locationPendingSearch (state) {
      return state.locationPendingSearch
    },
    locationSearchResults (state) {
      return state.locationSearchResults
    },
    locationSearchResultCount (state) {
      return state.locationSearchResultCount
    },
    organizationNames (state) {
      return state.organizationNames
    },
    pendingSearch (state) {
      return state.pendingSearch
    },
    searchBounds (state) {
      return state.searchBounds
    },
    searchErrors (state) {
      return state.searchErrors
    },
    searchLimit (state) {
      return state.searchLimit
    },
    searchOffset (state) {
      return state.searchOffset
    },
    searchOrdering (state) {
      return state.searchOrdering
    },
    searchParams (state) {
      return state.searchParams
    },
    searchResultColumns (state) {
      return state.searchResultColumns
    },
    searchResultFilters (state) {
      return state.searchResultFilters
    },
    searchResultCount (state) {
      return state.searchResultCount
    },
    searchResults (state) {
      return state.searchResults
    }
  }
}

export default wellsStore
