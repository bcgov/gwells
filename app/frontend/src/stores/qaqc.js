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
import { defineStore } from 'pinia'
import axios from 'axios'
import ApiService from '@/common/services/ApiService.js'

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
  const params = { ...state.params }

  if (Object.entries(state.resultFilters).length > 0) {
    params['filter_group'] = JSON.stringify(state.resultFilters)
  }

  return params
}

const RECORD_COMPLIANCE_COLUMNS = [
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

const MISLOCATED_WELLS_COLUMNS = [
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

const CROSS_REFERENCING_COLUMNS = [
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

export const useQAQCStore = defineStore('qaqc', {
  state: () => ({
    error: null,
    pendingSearch: null,
    hasSearched: false,
    bounds: {},
    errors: {},
    limit: DEFAULT_LIMIT,
    offset: 0,
    ordering: DEFAULT_ORDERING,
    params: {},
    resultColumns: CROSS_REFERENCING_COLUMNS,
    resultFilters: {},
    results: null,
    resultCount: 0,
    downloads: null,
    selectedTab: null
  }),

  getters: {
    inProgress: (state) => Boolean(state.pendingSearch),
    searchQueryParams (state) {
      return buildSearchParams(state)
    }
  },

  actions: {
    setSelectedTab (payload) {
      this.selectedTab = payload
    },
    setLimit (payload) {
      if (!(payload === 10 || payload === 25 || payload === 50)) {
        return
      }
      this.limit = payload
    },
    setOffset (payload) {
      this.offset = payload
    },
    setOrdering (payload) {
      this.ordering = payload
    },
    setResultFilters (payload) {
      this.resultFilters = cleanParams(payload)
    },
    setSelectedTabAction (tab) {
      this.selectedTab = tab
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
      // Set the qaqc result columns
      this.resultColumns = columns
      this.search()
    },
    resetSearch () {
      if (this.pendingSearch !== null) {
        this.pendingSearch.cancel()
      }
      this.hasSearched = false
      this.pendingSearch = null
      this.bounds = {}

      this.ordering = DEFAULT_ORDERING
      this.limit = DEFAULT_LIMIT
      this.offset = 0
      this.params = cleanParams({})
      this.errors = {}
      this.results = null
      this.resultCount = 0
      this.resultFilters = {}
    },
    search () {
      this.hasSearched = true

      if (this.pendingSearch !== null) {
        this.pendingSearch.cancel()
      }

      const cancelSource = axios.CancelToken.source()
      this.pendingSearch = cancelSource

      const params = {
        ...buildSearchParams(this),
        ordering: this.ordering,
        limit: this.limit,
        offset: this.offset
      }

      // Modify the endpoint or parameters based on the selectedTab
      let endpoint = 'qaqc'
      if (this.selectedTab === 0) {
        endpoint += '/recordcompliance'
      } else if (this.selectedTab === 1) {
        endpoint += '/mislocatedwells'
      } else if (this.selectedTab === 2) {
        endpoint += '/crossreferencing'
      }

      ApiService.query(endpoint, params, { cancelToken: cancelSource.token }).then((response) => {
        this.errors = {}
        this.results = response.data.results
        this.resultCount = response.data.count
      }).catch((err) => {
        // If the qaqc was cancelled, a new one is pending, so don't bother resetting.
        if (axios.isCancel(err)) {
          return
        }

        if (err.response && err.response.data) {
          this.errors = err.response.data
        }
        this.results = null
        this.resultCount = 0
      }).finally(() => {
        this.pendingSearch = null
      })
    }
  }
})
