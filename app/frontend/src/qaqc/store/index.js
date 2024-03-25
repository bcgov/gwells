/**
  Licensed under the Apache License, Version 2.0 (the "License")
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
  QAQC_SEARCH,
  RESET_QAQC_SEARCH,
  FETCH_QAQC_WELL_DOWNLOAD_LINKS,
  SET_QAQC_SELECTED_TAB_ACTION
} from './actions.types.js'
import {
  SET_QAQC_ERROR,
  SET_QAQC_LAST_SEARCH_TRIGGER,
  SET_QAQC_PENDING_SEARCH,
  SET_QAQC_HAS_SEARCHED,
  SET_QAQC_SEARCH_BOUNDS,
  SET_QAQC_LIMIT,
  SET_QAQC_OFFSET,
  SET_QAQC_ORDERING,
  SET_QAQC_ERRORS,
  SET_QAQC_PARAMS,
  SET_QAQC_RESULT_COLUMNS,
  SET_QAQC_RESULT_COUNT,
  SET_QAQC_RESULT_FILTERS,
  SET_QAQC_RESULTS,
  SET_QAQC_SELECTED_TAB
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
  const params = { ...state.qaqcParams }

  if (Object.entries(state.qaqcResultFilters).length > 0) {
    params['filter_group'] = JSON.stringify(state.qaqcResultFilters)
  }

  return params
}

export const RECORD_COMPLIANCE_COLUMNS = [
  'wellTagNumber',
  'identificationPlateNumber',
  'wellClass',
  'wellSubclass',
  'latitudeNull',
  'longitudeNull',
  'finishedWellDepthNull',
  'diameterNull',
  'surfaceSealDepthNull',
  'surfaceSealThicknessNull',
  'aquiferLithologyNull',
  'wellActivityType',
  'workStartDateNull',
  'workEndDateNull',
  'personResponsible',
  'orgResponsible',
  'naturalResourceRegion',
  'createDate',
  'createUser',
  'internalComments'
]

export const MISLOCATED_WELLS_COLUMNS = [
  'wellTagNumber',
  'geocodeDistance',
  'distanceToPid',
  'scoreAddress',
  'scoreCity',
  'wellActivityType',
  'workStartDateNull',
  'workEndDateNull',
  'orgResponsible',
  'naturalResourceRegion',
  'createDate',
  'createUser',
  'internalComments'
]

export const CROSS_REFERENCING_COLUMNS = [
  'wellTagNumber',
  'naturalResourceRegion',
  'createUser',
  'createDate',
  'updateUser',
  'updateDate',
  'crossReferencedDate',
  'crossReferencedBy',
  'comments',
  'internalComments'
]

const DEFAULT_ORDERING = '-well_tag_number'
const DEFAULT_LIMIT = 10

const wellsStore = {
  state: {
    error: null,
    lastSearchTrigger: null,
    qaqcPendingSearch: null,
    qaqcHasSearched: false,
    qaqcBounds: {},
    qaqcErrors: {},
    qaqcLimit: DEFAULT_LIMIT,
    qaqcOffset: 0,
    qaqcOrdering: DEFAULT_ORDERING,
    qaqcParams: {},
    qaqcResultColumns: CROSS_REFERENCING_COLUMNS,
    qaqcResultFilters: {},
    qaqcResults: null,
    qaqcResultCount: 0,
    downloads: null,
    selectedTab: 0
  },
  mutations: {
    [SET_QAQC_SELECTED_TAB] (state, payload) {
      state.selectedTab = payload
    },
    [SET_QAQC_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_QAQC_LAST_SEARCH_TRIGGER] (state, payload) {
      state.lastSearchTrigger = payload
    },
    [SET_QAQC_PENDING_SEARCH] (state, payload) {
      state.qaqcPendingSearch = payload
    },
    [SET_QAQC_HAS_SEARCHED] (state, payload) {
      state.qaqcHasSearched = payload
    },
    [SET_QAQC_ERRORS] (state, payload) {
      state.qaqcErrors = payload
    },
    [SET_QAQC_LIMIT] (state, payload) {
      if (!(payload === 10 || payload === 25 || payload === 50)) {
        return
      }
      state.qaqcLimit = payload
    },
    [SET_QAQC_OFFSET] (state, payload) {
      state.qaqcOffset = payload
    },
    [SET_QAQC_ORDERING] (state, payload) {
      state.qaqcOrdering = payload
    },
    [SET_QAQC_PARAMS] (state, payload) {
      state.qaqcParams = cleanParams(payload)
    },
    [SET_QAQC_RESULT_COLUMNS] (state, payload) {
      state.qaqcResultColumns = payload
    },
    [SET_QAQC_RESULT_FILTERS] (state, payload) {
      state.qaqcResultFilters = cleanParams(payload)
    },
    [SET_QAQC_RESULTS] (state, payload) {
      state.qaqcResults = payload
    },
    [SET_QAQC_RESULT_COUNT] (state, payload) {
      state.qaqcResultCount = payload
    }
  },
  actions: {
    [SET_QAQC_SELECTED_TAB_ACTION] ({ commit, dispatch }, tab) {
      commit('SET_QAQC_SELECTED_TAB', tab)
      // Determine which columns to use based on the selected tab
      let columns = []
      switch (tab) {
        case 0:
          columns = RECORD_COMPLIANCE_COLUMNS
          break
        case 1:
          columns = MISLOCATED_WELLS_COLUMNS
          break
        case 2:
          columns = CROSS_REFERENCING_COLUMNS
          break
        default:
          columns = [] // Default case or you can set a default column set
      }
      // Commit a mutation to set the qaqc result columns
      commit('SET_QAQC_RESULT_COLUMNS', columns)
      commit('SET_QAQC_RESULT_COLUMNS', columns)
      dispatch('QAQC_SEARCH', {})
    },
    [FETCH_QAQC_WELL_DOWNLOAD_LINKS] ({ commit, state }) {
      if (state.downloads === null) {
        ApiService.query('wells/extracts').then((response) => {
          state.downloads = response.data
        })
      }
    },
    [RESET_QAQC_SEARCH] ({ commit, state }) {
      if (state.qaqcPendingSearch !== null) {
        state.qaqcPendingSearch.cancel()
      }
      commit(SET_QAQC_HAS_SEARCHED, false)
      commit(SET_QAQC_PENDING_SEARCH, null)
      commit(SET_QAQC_SEARCH_BOUNDS, {})
      commit(SET_QAQC_ORDERING, DEFAULT_ORDERING)
      commit(SET_QAQC_LIMIT, DEFAULT_LIMIT)
      commit(SET_QAQC_OFFSET, 0)
      commit(SET_QAQC_PARAMS, {})
      commit(SET_QAQC_ERRORS, {})
      commit(SET_QAQC_RESULTS, null)
      commit(SET_QAQC_RESULT_COUNT, 0)
      commit(SET_QAQC_RESULT_FILTERS, {})
    },
    [QAQC_SEARCH] ({ commit, state }, { constrain = null, trigger = null }) {
      commit(SET_QAQC_LAST_SEARCH_TRIGGER, trigger)
      commit(SET_QAQC_HAS_SEARCHED, true)

      if (state.qaqcPendingSearch !== null) {
        state.qaqcPendingSearch.cancel()
      }

      const cancelSource = axios.CancelToken.source()
      commit(SET_QAQC_PENDING_SEARCH, cancelSource)

      const params = {
        ...buildSearchParams(state),
        ordering: state.qaqcOrdering,
        limit: state.qaqcLimit,
        offset: state.qaqcOffset
      }

      // Modify the endpoint or parameters based on the selectedTab
      let endpoint = 'qaqc'
      if (state.selectedTab === 0) {
        endpoint += '/recordcompliance'
      } else if (state.selectedTab === 1) {
        endpoint += '/mislocatedwells'
      } else if (state.selectedTab === 2) {
        endpoint += '/crossreferencing'
      }

      ApiService.query(endpoint, params, { cancelToken: cancelSource.token }).then((response) => {
        commit(SET_QAQC_ERRORS, {})
        commit(SET_QAQC_RESULTS, response.data.results)
        commit(SET_QAQC_RESULT_COUNT, response.data.count)
      }).catch((err) => {
        // If the qaqc was cancelled, a new one is pending, so don't bother resetting.
        if (axios.isCancel(err)) {
          return
        }

        if (err.response && err.response.data) {
          commit(SET_QAQC_ERRORS, err.response.data)
        }
        commit(SET_QAQC_RESULTS, null)
        commit(SET_QAQC_RESULT_COUNT, 0)
      }).finally(() => {
        commit(SET_QAQC_PENDING_SEARCH, null)
      })
    }
  },
  getters: {
    qaqcHasSearched (state) {
      return state.qaqcHasSearched
    },
    qaqcPendingSearch (state) {
      return state.qaqcPendingSearch
    },
    qaqcInProgress (state) {
      return Boolean(state.qaqcPendingSearch)
    },
    qaqcBounds (state) {
      return state.qaqcBounds
    },
    qaqcErrors (state) {
      return state.qaqcErrors
    },
    qaqcLimit (state) {
      return state.qaqcLimit
    },
    qaqcOffset (state) {
      return state.qaqcOffset
    },
    qaqcOrdering (state) {
      return state.qaqcOrdering
    },
    qaqcParams (state) {
      return state.qaqcParams
    },
    qaqcResultColumns (state) {
      return state.qaqcResultColumns
    },
    qaqcResultFilters (state) {
      return state.qaqcResultFilters
    },
    qaqcResultCount (state) {
      return state.qaqcResultCount
    },
    qaqcResults (state) {
      return state.qaqcResults
    },
    qaqcWellFileDownloads (state) {
      return state.downloads
    },
    searchQueryParams (state) {
      return buildSearchParams(state)
    },
    qaqcSelectedTab (state) {
      return state.selectedTab
    }
  }
}

export default wellsStore
