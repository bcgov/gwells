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
  // SEARCH_LOCATIONS,
  SEARCH_WELLS,
  RESET_WELL_DATA,
  FETCH_WELL_DOWNLOAD_LINKS
} from './actions.types.js'
import {
  SET_DRILLER_NAMES,
  SET_ERROR,
  SET_LAST_SEARCH_TRIGGER,
  // SET_LOCATION_ERRORS,
  SET_LOCATION_SEARCH_RESULTS,
  SET_ORGANIZATION_NAMES,
  SET_CONSTRAIN_SEARCH,
  SET_PENDING_LOCATION_SEARCH,
  SET_PENDING_SEARCH,
  SET_HAS_SEARCHED,
  SET_SEARCH_BOUNDS,
  SET_SEARCH_LIMIT,
  SET_SEARCH_OFFSET,
  SET_SEARCH_ORDERING,
  SET_SEARCH_ERRORS,
  SET_SEARCH_PARAMS,
  SET_SEARCH_RESULT_COLUMNS,
  SET_SEARCH_RESULT_COUNT,
  SET_SEARCH_RESULT_FILTERS,
  SET_SEARCH_RESULTS,
  SET_SEARCH_MAP_CENTRE,
  SET_SEARCH_MAP_ZOOM,
  SET_WELL_RECORD,
  SET_WELL_LICENCE
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

function buildSearchParams (state) {
  const params = { ...state.searchParams }

  if (Object.entries(state.searchResultFilters).length > 0) {
    params['filter_group'] = JSON.stringify(state.searchResultFilters)
  }

  return params
}

export const DEFAULT_COLUMNS = [
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
    locationSearchResults: [],
    organizationNames: [],
    pendingLocationSearch: null,
    pendingSearch: null,
    constrainSearch: true,
    hasSearched: false,
    searchBounds: {},
    searchErrors: {},
    searchLimit: DEFAULT_LIMIT,
    searchOffset: 0,
    searchOrdering: DEFAULT_ORDERING,
    searchParams: {},
    searchResultColumns: DEFAULT_COLUMNS,
    // searchResultFilters provides a second level of filtering.
    searchResultFilters: {},
    searchResults: null,
    searchResultCount: 0,
    wellId: null,
    wellRecord: {},
    recordLicence: {
      status: '',
      number: ''
    },
    searchMap: {
      centre: null,
      zoom: null
    },
    downloads: null
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
    [SET_HAS_SEARCHED] (state, payload) {
      state.hasSearched = payload
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
    },
    [SET_SEARCH_MAP_CENTRE] (state, payload) {
      state.searchMap.centre = payload
    },
    [SET_SEARCH_MAP_ZOOM] (state, payload) {
      state.searchMap.zoom = payload
    },
    [SET_WELL_RECORD] (state, payload) {
      state.wellRecord = payload
      state.wellId = payload.well || null
    },
    [SET_WELL_LICENCE] (state, payload) {
      state.recordLicence = payload
    }
  },
  actions: {
    [FETCH_WELL_DOWNLOAD_LINKS] ({ commit, state }) {
      if (state.downloads === null) {
        ApiService.query('wells/extracts').then((response) => {
          state.downloads = response.data
        })
      }
    },
    [FETCH_DRILLER_NAMES] ({ commit, state }) {
      // fetch only once
      if (state.drillerNames.length === 0) {
        ApiService.query('drillers/names').then((response) => {
          commit(SET_DRILLER_NAMES, response.data)
        }).catch((err) => {
          commit(SET_ERROR, err.response)
        })
      }
    },
    [RESET_WELL_DATA] ({ commit }) {
      commit(SET_WELL_RECORD, {})
      commit(SET_WELL_LICENCE, {
        status: '',
        number: ''
      })
    },
    [FETCH_ORGANIZATION_NAMES] ({ commit, state }) {
      // fetch only once
      if (state.organizationNames.length === 0) {
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
      commit(SET_HAS_SEARCHED, false)
      commit(SET_PENDING_SEARCH, null)
      commit(SET_CONSTRAIN_SEARCH, true)
      commit(SET_SEARCH_BOUNDS, {})
      commit(SET_SEARCH_ORDERING, DEFAULT_ORDERING)
      commit(SET_SEARCH_LIMIT, DEFAULT_LIMIT)
      commit(SET_SEARCH_OFFSET, 0)
      commit(SET_SEARCH_PARAMS, {})
      commit(SET_SEARCH_ERRORS, {})
      commit(SET_SEARCH_RESULTS, null)
      commit(SET_SEARCH_RESULT_COUNT, 0)
      commit(SET_LOCATION_SEARCH_RESULTS, [])
      commit(SET_SEARCH_RESULT_COLUMNS, DEFAULT_COLUMNS)
      commit(SET_SEARCH_RESULT_FILTERS, {})
      commit(SET_SEARCH_MAP_CENTRE, null)
      commit(SET_SEARCH_MAP_ZOOM, null)
    },
    [SEARCH_WELLS] ({ commit, state }, { constrain = null, trigger = null }) {
      commit(SET_LAST_SEARCH_TRIGGER, trigger)
      commit(SET_HAS_SEARCHED, true)

      if (state.pendingSearch !== null) {
        state.pendingSearch.cancel()
      }

      const cancelSource = axios.CancelToken.source()
      commit(SET_PENDING_SEARCH, cancelSource)

      if (constrain !== null) {
        commit(SET_CONSTRAIN_SEARCH, constrain)
      }

      const params = {
        ...buildSearchParams(state),
        ordering: state.searchOrdering,
        limit: state.searchLimit,
        offset: state.searchOffset
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
    hasSearched (state) {
      return state.hasSearched
    },
    pendingSearch (state) {
      return state.pendingSearch
    },
    searchInProgress (state) {
      return Boolean(state.pendingSearch)
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
    },
    well (state) {
      return state.wellRecord
    },
    wellLicence (state) {
      return state.recordLicence
    },
    storedWellId (state) {
      return state.wellId
    },
    searchMapCentre (state) {
      return state.searchMap.centre
    },
    searchMapZoom (state) {
      return state.searchMap.zoom
    },
    wellFileDownloads (state) {
      return state.downloads
    },
    searchQueryParams (state) {
      return buildSearchParams(state)
    }
  }
}

export default wellsStore
