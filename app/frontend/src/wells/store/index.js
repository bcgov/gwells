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
  SEARCH_LOCATIONS,
  SEARCH_WELLS
} from './actions.types.js'
import {
  SET_DRILLER_NAMES,
  SET_ERROR,
  SET_LAST_SEARCH_TRIGGER,
  SET_LOCATION_ERRORS,
  SET_LOCATION_SEARCH_RESULTS,
  SET_ORGANIZATION_NAMES,
  SET_CONSTRAIN_SEARCH,
  SET_PENDING_LOCATION_SEARCH,
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

const DEFAULT_COLUMNS = [
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
]
const DEFAULT_ORDERING = '-well_tag_number'
const DEFAULT_LIMIT = 10

const wellsStore = {
  state: {
    error: null,
    drillerNames: [],
    lastSearchTrigger: null,
    locationErrors: {},
    locationSearchResults: [],
    organizationNames: [],
    pendingLocationSearch: null,
    pendingSearch: null,
    constrainSearch: false,
    searchBounds: {},
    searchErrors: {},
    searchLimit: DEFAULT_LIMIT,
    searchOffset: 0,
    searchOrdering: DEFAULT_ORDERING,
    searchParams: {},
    searchResultColumns: [...DEFAULT_COLUMNS],
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
    [SET_LAST_SEARCH_TRIGGER] (state, payload) {
      state.lastSearchTrigger = payload
    },
    [SET_LOCATION_ERRORS] (state, payload) {
      state.locationErrors = payload
    },
    [SET_LOCATION_SEARCH_RESULTS] (state, payload) {
      state.locationSearchResults = payload
    },
    [SET_ORGANIZATION_NAMES] (state, payload) {
      state.organizationNames = payload
    },
    [SET_PENDING_LOCATION_SEARCH] (state, payload) {
      state.pendingLocationSearch = payload
    },
    [SET_PENDING_SEARCH] (state, payload) {
      state.pendingSearch = payload
    },
    [SET_CONSTRAIN_SEARCH] (state, payload) {
      state.constrainSearch = payload
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
    [RESET_WELLS_SEARCH] ({ commit, state }) {
      if (state.pendingLocationSearch !== null) {
        state.pendingLocationSearch.cancel()
      }
      if (state.pendingSearch !== null) {
        state.pendingSearch.cancel()
      }

      commit(SET_PENDING_LOCATION_SEARCH, null)
      commit(SET_PENDING_SEARCH, null)
      commit(SET_CONSTRAIN_SEARCH, false)
      commit(SET_SEARCH_BOUNDS, {})
      commit(SET_SEARCH_ORDERING, DEFAULT_ORDERING)
      commit(SET_SEARCH_LIMIT, DEFAULT_LIMIT)
      commit(SET_SEARCH_OFFSET, 0)
      commit(SET_SEARCH_PARAMS, {})
      commit(SET_SEARCH_ERRORS, {})
      commit(SET_SEARCH_RESULTS, null)
      commit(SET_SEARCH_RESULT_COUNT, 0)
      commit(SET_LOCATION_SEARCH_RESULTS, [])
      commit(SET_SEARCH_RESULT_COLUMNS, [...DEFAULT_COLUMNS])
      commit(SET_SEARCH_RESULT_FILTERS, {})
    },
    [SEARCH_LOCATIONS] ({ commit, state }) {
      if (state.pendingLocationSearch !== null) {
        state.pendingLocationSearch.cancel()
      }

      const cancelSource = axios.CancelToken.source()
      commit(SET_PENDING_LOCATION_SEARCH, cancelSource)

      const params = { ...state.searchParams, ...state.searchBounds }

      if (Object.entries(state.searchResultFilters).length > 0) {
        params['filter_group'] = JSON.stringify(state.searchResultFilters)
      }

      ApiService.query('wells/locations', params, { cancelToken: cancelSource.token }).then((response) => {
        if (response.data.count === 0) {
          commit(SET_LOCATION_ERRORS, { detail: 'No well records could be found.' })
        } else if (response.data.count > response.data.results.length) {
          commit(SET_LOCATION_ERRORS, {
            detail: 'Too many wells to display on map. ' +
                    'Please zoom in or change your search criteria.'
          })
        } else {
          commit(SET_LOCATION_ERRORS, {})
          commit(SET_LOCATION_SEARCH_RESULTS, response.data.results)
        }
      }).catch((err) => {
        // If the search was cancelled, a new one is pending, so don't bother resetting.
        if (axios.isCancel(err)) {
          return
        }

        if (err.response && err.response.data) {
          commit(SET_LOCATION_ERRORS, err.response.data)
        }
        commit(SET_LOCATION_SEARCH_RESULTS, [])
      }).finally(() => {
        commit(SET_PENDING_LOCATION_SEARCH, null)
      })
    },
    [SEARCH_WELLS] ({ commit, state }, { constrain = null, trigger = null }) {
      state.lastSearchTrigger = trigger

      if (state.pendingSearch !== null) {
        state.pendingSearch.cancel()
      }

      const cancelSource = axios.CancelToken.source()
      commit(SET_PENDING_SEARCH, cancelSource)

      if (constrain !== null) {
        commit(SET_CONSTRAIN_SEARCH, constrain)
      }

      const params = {
        ...state.searchParams,
        ordering: state.searchOrdering,
        limit: state.searchLimit,
        offset: state.searchOffset
      }

      if (Object.entries(state.searchResultFilters).length > 0) {
        params['filter_group'] = JSON.stringify(state.searchResultFilters)
      }
      // if triggering the search using the map, the search will be restricted to
      // the visible map bounds
      if (state.constrainSearch) {
        Object.assign(params, state.searchBounds)
      }

      ApiService.query('wells', params, { cancelToken: cancelSource.token }).then((response) => {
        commit(SET_SEARCH_ERRORS, {})
        commit(SET_SEARCH_RESULTS, response.data.results)
        commit(SET_SEARCH_RESULT_COUNT, response.data.count)
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
      }).finally(() => {
        commit(SET_PENDING_SEARCH, null)
      })
    }
  },
  getters: {
    drillerNames (state) {
      return state.drillerNames
    },
    lastSearchTrigger (state) {
      return state.lastSearchTrigger
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
    locationSearchResults (state) {
      return state.locationSearchResults
    },
    organizationNames (state) {
      return state.organizationNames
    },
    constrainSearch (state) {
      return state.constrainSearch
    },
    pendingLocationSearch (state) {
      return state.pendingLocationSearch
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
