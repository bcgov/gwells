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
import { defineStore } from 'pinia'
import ApiService from '@/common/services/ApiService.js'
import {
  DEFAULT_MAP_ZOOM,
  CENTRE_LNG_LAT_BC,
  convertLngLatBoundsToDirectionBounds
} from '@/common/mapbox/geometry'

export const DEFAULT_SEARCH_PARAMS = {
  search: '',
  city: [''],
  region: [],
  activity: 'DRILL',
  subactivities: null,
  status: 'A',
  limit: '10',
  ordering: ''
}

export const DEFAULT_MAP_POSITION = {
  centre: CENTRE_LNG_LAT_BC,
  zoom: DEFAULT_MAP_ZOOM
}

export const useRegistryStore = defineStore('registries', {
  state: () => ({
    searchParams: Object.assign({}, DEFAULT_SEARCH_PARAMS),
    hasSearched: false,
    user: null,
    loading: false,
    error: null,
    listError: null,
    cityList: {},
    searchResponse: [],
    currentDriller: {},
    drillerOptions: null,
    lastSearchedActivity: 'DRILL',
    lastSearchedParams: null,
    requestedMapPosition: null,
    currentMapBounds: null,
    doSearchOnBoundsChange: false,
    isSearchInProgress: false,
    // dual-purpose: when false, snapMapToSearchResults is true and vice versa
    limitSearchToCurrentMapBounds: false
  }),

  getters: {
    snapMapToSearchResults: (state) => !state.limitSearchToCurrentMapBounds,
    activity: (state) =>
      state.lastSearchedParams ? state.lastSearchedParams.raw.activity : null,
    provinceStateOptions (state) {
      const options = []
      if (state.drillerOptions && state.drillerOptions.province_state_codes) {
        state.drillerOptions.province_state_codes.forEach((item) => {
          options.push(item.province_state_code)
        })
      }
      return options
    },
    regionOptions (state) {
      if (state.drillerOptions && state.drillerOptions.regional_areas) {
        return state.drillerOptions.regional_areas
      }
      return []
    }
  },

  actions: {
    setError (payload) {
      this.error = payload
    },

    setLoading (payload) {
      this.loading = payload
    },

    setSearchParams (payload) {
      this.searchParams = payload
    },

    setHasSearched (payload) {
      this.hasSearched = payload
    },

    setIsSearchInProgress (payload) {
      this.isSearchInProgress = payload
    },

    setListError (payload) {
      this.listError = payload
    },

    setUser (payload) {
      this.user = payload
    },

    setCityList (payload) {
      this.cityList = payload
    },

    setDriller (payload) {
      this.currentDriller = payload
    },

    setSearchResponse (payload) {
      this.searchResponse = payload
    },

    setDrillerOptions (payload) {
      this.drillerOptions = payload
    },

    setLastSearchedActivity (payload) {
      this.lastSearchedActivity = payload
    },

    setLastSearchedParams (payload) {
      if (payload != null &&
        (!payload.hasOwnProperty('raw') || !payload.hasOwnProperty('api'))) {
        throw new Error("Must specify parameter in the format of: {'raw': {...}, 'api': {...}}")
      }
      this.lastSearchedParams = payload
    },

    setRequestedMapPosition (payload) {
      if (payload.hasOwnProperty('centre') && !payload.hasOwnProperty('zoom')) {
        payload.zoom = 10
      }
      if (payload.hasOwnProperty('bounds') && !payload.hasOwnProperty('maxZoom')) {
        payload.maxZoom = 10
      }
      if (payload && !payload.hasOwnProperty('centre') && !payload.hasOwnProperty('bounds')) {
        throw new Error("Must specify either the 'centre' or the 'bounds' parameter")
      }
      this.requestedMapPosition = payload
    },

    setCurrentMapBounds (payload) {
      if (JSON.stringify(this.currentMapBounds) === JSON.stringify(payload)) {
        return
      }
      this.currentMapBounds = payload
    },

    setDoSearchOnBoundsChange (payload) {
      this.doSearchOnBoundsChange = payload
    },

    setLimitSearchToCurrentMapBounds (payload) {
      this.limitSearchToCurrentMapBounds = payload
    },

    resetSearch (options = {}) {
      const searchParams = Object.assign({}, this.searchParams)
      searchParams.search = DEFAULT_SEARCH_PARAMS.search
      searchParams.city = DEFAULT_SEARCH_PARAMS.city
      searchParams.region = DEFAULT_SEARCH_PARAMS.region
      searchParams.status = DEFAULT_SEARCH_PARAMS.status
      searchParams.ordering = DEFAULT_SEARCH_PARAMS.ordering
      const propertiesToClear = ['ne_lat', 'ne_long', 'sw_lat', 'sw_long', 'offset']
      propertiesToClear.forEach(p => {
        if (searchParams.hasOwnProperty(p)) {
          delete searchParams[p]
        }
      })
      if (!options.keepSearchResults) {
        this.hasSearched = false
        this.searchResponse = []
      }
      if (!options.keepActivity) {
        searchParams.activity = DEFAULT_SEARCH_PARAMS.activity
        searchParams.subactivities = DEFAULT_SEARCH_PARAMS.subactivities
      }
      if (!options.keepLimit) {
        searchParams.limit = DEFAULT_SEARCH_PARAMS.limit
      }
      this.searchParams = searchParams
      this.lastSearchedParams = null
      this.limitSearchToCurrentMapBounds = false
      this.doSearchOnBoundsChange = false
      this.requestedMapPosition = Object.assign({}, DEFAULT_MAP_POSITION)
    },

    fetchCityList (activity) {
      ApiService.query('cities/' + activity)
        .then((response) => {
          const list = Object.assign({}, this.cityList)
          const data = response.data
          const listByProvince = []

          data.forEach((item) => {
            if (!listByProvince.some(prov => prov.prov === item.province_state)) {
              listByProvince.push({ prov: item.province_state, cities: [] })
            }
            listByProvince.find(prov => prov.prov === item.province_state).cities.push(item.city)
          })

          list[activity] = listByProvince
          this.cityList = list
        })
        .catch((error) => {
          this.error = error.response
        })
    },

    fetchDriller (guid) {
      this.loading = true
      ApiService.get('drillers', guid)
        .then((response) => {
          this.loading = false
          this.error = null
          this.currentDriller = response.data
        })
        .catch((error) => {
          this.loading = false
          this.error = error.response
        })
    },

    search (params) {
      if (this.limitSearchToCurrentMapBounds && this.currentMapBounds) {
        params = Object.assign({}, params, convertLngLatBoundsToDirectionBounds(this.currentMapBounds))
        params.srid = 4326
      } else {
        params = Object.assign({}, params, { sw_lat: null, sw_long: null, ne_lat: null, ne_long: null })
        params.srid = null
      }

      if (!params.subactivities.length) {
        params.subactivities = ['']
      }

      const arrayParams = ['subactivities', 'city']
      arrayParams.forEach(p => {
        if (params.hasOwnProperty(p) && typeof params[p] === 'string') {
          params[p] = params[p].split(',')
        }
      })

      const paramsForApi = Object.assign({}, params)
      for (const [key, value] of Object.entries(paramsForApi)) {
        if (Array.isArray(value)) {
          paramsForApi[key] = value.join(',')
        }
      }

      this.setLastSearchedParams({ raw: Object.assign({}, params), api: paramsForApi })

      return new Promise((resolve, reject) => {
        this.hasSearched = true
        this.isSearchInProgress = true
        ApiService.query('drillers', paramsForApi)
          .then((response) => {
            this.isSearchInProgress = false
            this.listError = null
            this.searchResponse = response.data
            resolve()
          })
          .catch((error) => {
            this.isSearchInProgress = false
            this.listError = error.response
            reject(error)
          })
      })
    },

    searchAgain () {
      if (this.searchParams) {
        this.search(this.searchParams)
      }
    },

    fetchDrillerOptions (params) {
      if (!this.drillerOptions) {
        return new Promise((resolve, reject) => {
          this.loading = true
          ApiService.query('drillers/options', params)
            .then((response) => {
              this.loading = false
              this.drillerOptions = response.data
              resolve()
            })
            .catch((error) => {
              this.loading = false
              reject(error)
            })
        })
      }
    },

    requestMapPosition (mapPosition) {
      this.setRequestedMapPosition(mapPosition)
    },

    searchRegion (payload) {
      const searchParams = Object.assign({}, this.searchParams)
      searchParams.region = payload
      this.searchParams = searchParams
      this.search(this.searchParams)
    }
  }
})
