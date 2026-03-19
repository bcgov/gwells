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
import axios from 'axios'
import ApiService from '@/common/services/ApiService.js'
import { doPolygonsIntersect } from '@/common/mapbox/geometry.js'
import { SEARCH_AQUIFERS } from '@/aquifers/store/actions.types.js'
import {
  SET_SEARCH_BOUNDS,
  SET_SEARCH_ERRORS,
  SET_SEARCH_RESULTS,
  SET_SEARCH_RESULT_COUNT,
  SET_PENDING_SEARCH,
  SET_SEARCH_IN_PROGRESS,
  RESET_SEARCH,
  SET_CONSTRAIN_SEARCH,
  SET_SEARCH_QUERY,
  SET_SELECTED_SECTIONS,
  SET_MATCH_ANY,
  SET_SEARCH_MAP_CENTRE,
  SET_SEARCH_MAP_ZOOM,
  SET_NATURAL_RESOURCE_REGIONS,
  SET_AQUIFER_NOTATIONS
} from '@/aquifers/store/mutations.types.js'

const AQUIFER_NOTATION_CODE = 'Notations'
const UNPUBLISHED_AQUIFERS = 'Unpublished'

const AQUIFER_NOTATION_CODES = {
  AR: 'Application Refused',
  PWS: 'Possible Water Shortage',
  FR: 'Fully Recorded',
  'FR-EXC': 'Fully Recorded Except',
  OR: 'Office Reserve'
}

export const useAquiferStore = defineStore('aquifers', {
  state: () => ({
    // Root (was aquiferStore root)
    sections: [],

    // Search (was aquiferStore/search)
    search: {
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

    // View (was aquiferStore/view)
    view: {
      id: null,
      record: {},
      aquiferFiles: {
        public: [],
        private: []
      },
      aquiferWells: []
    },

    // Codes (was aquiferStore/aquiferCodes)
    aquiferCodes: {
      aquifer_resource_sections: [],
      demand_codes: [],
      known_water_use_codes: [],
      material_codes: [],
      productivity_codes: [],
      quality_concern_codes: [],
      subtype_codes: [],
      vulnerability_codes: []
    },

    // Notations (was aquiferStore/notations)
    notations: {
      naturalResourceRegions: [],
      aquiferNotations: [],
      aquiferNotationCodes: { ...AQUIFER_NOTATION_CODES }
    }
  }),

  getters: {
    // ---- Root ----
    // sections is state.sections (use state.sections in components)

    // ---- Search ----
    queryParams (state) {
      const params = {}
      const s = state.search
      if (s.searchQuery.trim()) {
        params.search = s.searchQuery
      }
      const codes = s.selectedSections.filter((x) =>
        x !== AQUIFER_NOTATION_CODE && x !== UNPUBLISHED_AQUIFERS
      )
      if (codes.length > 0) {
        params.resources__section__code = codes.join(',')
      }
      if (s.searchMatchAny) {
        params.match_any = String(s.searchMatchAny)
      }
      if (s.selectedSections.includes(AQUIFER_NOTATION_CODE)) {
        params.aquifer_notations = 'yes'
      }
      if (s.selectedSections.includes(UNPUBLISHED_AQUIFERS)) {
        params.unpublished = 'yes'
      }
      if (s.searchMapCentre) {
        params.map_centre = `${s.searchMapCentre.lat.toFixed(6)},${s.searchMapCentre.lng.toFixed(6)}`
      }
      if (s.searchMapZoom != null) {
        params.map_zoom = String(s.searchMapZoom)
      }
      if (s.constrainSearch) {
        params.constrain = String(s.constrainSearch)
      }
      return params
    },
    searchParams (state, getters) {
      const params = { ...getters.queryParams }
      const s = state.search
      if (s.constrainSearch && s.mapBounds) {
        const b = s.mapBounds
        Object.assign(params, {
          sw_lat: b.getSouthWest().lat,
          sw_long: b.getSouthWest().lng,
          ne_lat: b.getNorthEast().lat,
          ne_long: b.getNorthEast().lng
        })
      }
      return params
    },
    searchResults (state) {
      const now = new Date()
      return (state.search.searchResults || []).map((result) => ({
        ...result,
        retire_date: new Date(result.retire_date) <= now ? result.retire_date : null
      }))
    },
    searchErrors: (state) => state.search.searchErrors,
    searchInProgress: (state) => state.search.searchInProgress,
    searchPerformed: (state) => state.search.searchPerformed,
    searchMapCentre: (state) => state.search.searchMapCentre,
    searchMapZoom: (state) => state.search.searchMapZoom,
    mapBounds: (state) => state.search.mapBounds,
    searchQuery: (state) => state.search.searchQuery,
    selectedSections: (state) => state.search.selectedSections,
    searchMatchAny: (state) => state.search.searchMatchAny,
    constrainSearch: (state) => state.search.constrainSearch,
    searchResultCount: (state) => state.search.searchResultCount,
    pendingSearch: (state) => state.search.pendingSearch,

    // ---- View ----
    record: (state) => state.view.record,
    storedId: (state) => state.view.id,
    aquiferFiles: (state) => state.view.aquiferFiles,
    aquiferWells: (state) => state.view.aquiferWells,
    wellsWithAquiferCorrelation (state) {
      return state.view.aquiferWells.filter((w) => w.aquifer_id === state.view.id)
    },
    wellsWithoutAquiferCorrelation (state) {
      return state.view.aquiferWells.filter((w) => w.aquifer_id === null)
    },
    wellsCorrelatedWithADifferentAquifer (state) {
      return state.view.aquiferWells.filter((w) => w.aquifer_id !== state.view.id)
    },

    // ---- aquiferCodes (flat for Form.vue mapState) ----
    demand_codes: (state) => state.aquiferCodes.demand_codes,
    aquifer_resource_sections: (state) => state.aquiferCodes.aquifer_resource_sections,
    known_water_use_codes: (state) => state.aquiferCodes.known_water_use_codes,
    material_codes: (state) => state.aquiferCodes.material_codes,
    productivity_codes: (state) => state.aquiferCodes.productivity_codes,
    quality_concern_codes: (state) => state.aquiferCodes.quality_concern_codes,
    subtype_codes: (state) => state.aquiferCodes.subtype_codes,
    vulnerability_codes: (state) => state.aquiferCodes.vulnerability_codes,

    // ---- Notations ----
    naturalResourceRegions: (state) => state.notations.naturalResourceRegions,
    aquiferNotations: (state) => state.notations.aquiferNotations,
    aquiferNotationCodes: (state) => state.notations.aquiferNotationCodes,
    getAquiferNotationsById () {
      const state = this
      return (id, geom) => {
        const aquiferNotations = state.notations.aquiferNotations.filter(
          (a) => String(a.properties.AQUIFER_ID) === String(id)
        )
        if (aquiferNotations.length === 0) return null
        const description = this.getAquiferNotationDescription(aquiferNotations)
        if (description.includes('Possible Water Shortage')) {
          return this.filterAquiferNotationsByRegion(description, geom)
        }
        return description
      }
    },
    getAquiferNotationDescription (state) {
      return (notations) => {
        let description = ''
        const codes = state.notations.aquiferNotationCodes
        notations.forEach((notation) => {
          for (const [key, value] of Object.entries(codes)) {
            if (notation.properties.NOTATION_DESCRIPTION.includes(key)) {
              description = description + value + ', '
            }
          }
        })
        return description.replace(/,\s*$/, '')
      }
    },
    filterAquiferNotationsByRegion (state) {
      return (description, geom) => {
        for (const feature of state.notations.naturalResourceRegions) {
          if (doPolygonsIntersect(feature, geom)) {
            return description.replace(
              'Possible Water Shortage',
              'Possible Water Shortage and/or Saline Intrusion Issues'
            )
          }
        }
        return description
      }
    }
  },

  actions: {
    // ---- Root ----
    addSections (payload) {
      this.sections = payload
    },

    // ---- Search ----
    [SEARCH_AQUIFERS] ({ query, selectedSections, matchAny }) {
      this.search.searchPerformed = true
      this.search.searchInProgress = true
      this.search.searchQuery = query ?? ''
      this.search.selectedSections = selectedSections ?? []
      this.search.searchMatchAny = Boolean(matchAny)

      if (this.search.pendingSearch) {
        this.search.pendingSearch.cancel()
      }
      const cancelSource = axios.CancelToken.source()
      this.search.pendingSearch = cancelSource

      const params = this.searchParams
      ApiService.query('aquifers', params, { cancelToken: cancelSource.token })
        .then((response) => {
          this.search.searchErrors = {}
          const data = response.data || { count: 0, results: [] }
          this.search.searchResults = data.results
          this.search.searchResultCount = data.count
          this.search.searchInProgress = false
          this.search.pendingSearch = null
        })
        .catch((err) => {
          if (axios.isCancel(err)) return
          if (err.response?.data) {
            this.search.searchErrors = err.response.data
          }
          this.search.searchResults = null
          this.search.searchResultCount = 0
          this.search.pendingSearch = null
        })
    },

    [SET_SEARCH_BOUNDS] (payload) {
      this.search.mapBounds = payload
    },
    [SET_SEARCH_ERRORS] (payload) {
      this.search.searchErrors = payload
    },
    [SET_SEARCH_QUERY] (payload) {
      this.search.searchQuery = payload || ''
    },
    [SET_SELECTED_SECTIONS] (payload) {
      this.search.selectedSections = payload ?? []
    },
    [SET_MATCH_ANY] (payload) {
      this.search.searchMatchAny = payload
    },
    [SET_SEARCH_MAP_CENTRE] (payload) {
      this.search.searchMapCentre = payload
    },
    [SET_SEARCH_MAP_ZOOM] (payload) {
      this.search.searchMapZoom = payload
    },
    [SET_CONSTRAIN_SEARCH] (payload) {
      this.search.constrainSearch = payload
    },
    [RESET_SEARCH] () {
      this.search.searchResults = []
      this.search.searchQuery = ''
      this.search.selectedSections = []
      this.search.searchResultCount = 0
      this.search.searchPerformed = false
      this.search.searchMatchAny = false
      this.search.searchErrors = {}
      this.search.searchInProgress = false
      this.search.constrainSearch = false
      this.search.mapBounds = null
      this.search.searchMapCentre = null
      this.search.searchMapZoom = null
    },

    // ---- View ----
    setAquiferRecord (payload) {
      this.view.record = payload ?? {}
      this.view.id = payload?.aquifer_id ?? null
    },
    setAquiferFiles (payload) {
      this.view.aquiferFiles = payload ?? { public: [], private: [] }
    },
    setAquiferWells (payload) {
      this.view.aquiferWells = payload ?? []
    },
    resetAquiferData () {
      this.view.record = {}
      this.view.id = null
      this.view.aquiferFiles = { public: [], private: [] }
      this.view.aquiferWells = []
    },

    // ---- aquiferCodes ----
    addCodes (payload) {
      if (payload?.key != null) {
        this.aquiferCodes[payload.key] = payload.codeTable ?? []
      }
    },

    // ---- Notations ----
    [SET_NATURAL_RESOURCE_REGIONS] (payload) {
      this.notations.naturalResourceRegions = payload ?? []
    },
    [SET_AQUIFER_NOTATIONS] (payload) {
      this.notations.aquiferNotations = payload ?? []
    },
    fetchNotationsFromDataBC () {
      if (this.notations.naturalResourceRegions.length <= 0 ||
          this.notations.aquiferNotations.length <= 0) {
        this.fetchNaturalResourceRegions()
        this.fetchAquiferNotations()
      }
    },
    fetchNaturalResourceRegions () {
      const url = 'https://openmaps.gov.bc.ca/geo/pub/wfs?SERVICE=WFS&VERSION=2.0.0' +
        '&REQUEST=GetFeature&outputFormat=json&srsName=epsg:4326&typeNames=WHSE_ADMIN_BOUNDARIES.ADM_NR_REGIONS_SPG' +
        "&CQL_FILTER=REGION_NAME IN('South Coast Natural Resource Region','West Coast Natural Resource Region')"
      axios.get(url, {
        transformRequest: (data, headers) => {
          if (headers?.common) delete headers.common['Authorization']
          return data
        }
      }).then((response) => {
        if (response.data?.features) {
          this.notations.naturalResourceRegions = response.data.features
        }
      }).catch((err) => console.log(err))
    },
    fetchAquiferNotations () {
      const url = 'https://openmaps.gov.bc.ca/geo/pub/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature' +
        '&outputFormat=json&srsName=epsg:4326&typeNames=WHSE_WATER_MANAGEMENT.WLS_WATER_NOTATION_AQUIFERS_SP' +
        '&propertyName=AQUIFER_ID,NOTATION_DESCRIPTION'
      axios.get(url, {
        transformRequest: (data, headers) => {
          if (headers?.common) delete headers.common['Authorization']
          return data
        }
      }).then((response) => {
        if (response.data?.features) {
          this.notations.aquiferNotations = response.data.features
        }
      }).catch((err) => console.log(err))
    }
  }
})
