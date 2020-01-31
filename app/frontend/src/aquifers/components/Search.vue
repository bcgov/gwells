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

<template>
  <div class="container p-1">
    <!-- Active surveys -->
    <b-alert
        show
        variant="info"
        class="mb-3"
        v-for="(survey, index) in surveys"
        :key="`survey ${index}`">
      <p class="m-0">
        <a :href="survey.survey_link">
          {{ survey.survey_introduction_text }}
        </a>
      </p>
    </b-alert>

    <b-card no-body class="main-search-card mb-4">
      <b-alert
        :show="noSearchCriteriaError"
        variant="danger">
        <i class="fa fa-exclamation-circle"/>&nbsp;&nbsp;At least one search field is required
      </b-alert>
      <b-form
        v-on:submit.prevent="triggerSearch"
        v-on:reset="triggerReset">
        <b-form-row>
          <b-col cols="12" md="12" lg="12" xl="4" class="p-4">
            <h1 class="main-title ml-2 mt-2">Aquifer Search
              <div v-if='userRoles.aquifers.edit' class="pb-2 pull-right">
              <b-button
                id="aquifers-add"
                v-on:click="navigateToNew"
                v-if="userRoles.aquifers.edit"
                variant="primary">Add new Aquifer</b-button>
              </div>
            </h1>

            <div class="pl-2 pr-2 aquifer-search-column mt-3">
              <h4>Basic Search</h4>
              <h5 class="search-title">Search by aquifer name or number (leave blank to see all aquifers)</h5>
              <b-form-group class="search-title mt-3 mb-3">
                <b-form-input
                  type="text"
                  id="aquifers-search-field"
                  v-model="search"
                  class="w-75"/>
              </b-form-group>
              <h4 class="pt-4">Advanced Search</h4>
              <b-form-group>
                <b-form-radio inline v-model="matchAny" name="match-any" value="true">Any field match</b-form-radio>
                <b-form-radio inline v-model="matchAny" name="match-any" value="false">All field match</b-form-radio>
              </b-form-group>
              <b-form-checkbox-group
                stacked
                v-model="selectedSections"
                :options="resourceSectionOptions"
                class="aquifer-checkbox-group"
              />
              <b-form-row>
                <b-button-group class="aquifer-search-actions">
                  <b-button class="aquifer-buttons" variant="primary" type="submit" id="aquifers-search" :disabled="searchInProgress">
                    Search
                    <i v-if="searchInProgress" class="fa fa-circle-o-notch fa-spin ml-1"/>
                  </b-button>
                  <b-button class="aquifer-buttons" variant="default" type="reset">Reset</b-button>
                </b-button-group>
              </b-form-row>
              <h6 class="mt-3">Download all aquifers</h6>
              <ul class="aquifer-download-list">
                <li>- <a href="#" @click.prevent="downloadXLSX(false)">Aquifer extract (XLSX)</a></li>
                <li>- <a href="#" @click.prevent="downloadCSV(false)">Aquifer extract (CSV)</a></li>
              </ul>
            </div>
          </b-col>

          <b-col cols="12" md="12" lg="12" xl="8" class="map-column">
            <map-loading-spinner :loading="loadingMap"/>

            <aquifer-map
              ref="aquiferMap"
              :initialCentre="searchMapCentre"
              :initialZoom="searchMapZoom"
              :aquifersGeometry="simplifiedAquifers"
              :aquiferDetails="searchResults"
              :highlightAquiferIds="searchedAquiferIds"
              :selectedId="selectedAquiferId"
              :loading="loadingMap"
              @moved="mapMoved"
              @zoomed="handleMapZoom"/>
          </b-col>
        </b-form-row>
      </b-form>

      <b-row>
        <b-col cols="12" class="p-5">
          <b-container fluid v-if="searchPerformed && !searchInProgress && !emptyResults" class="p-0">
            <b-row>
              <b-col cols="12" class="mb-3">
                Showing {{ displayOffset }} to {{ displayPageLength }} of {{ searchResultCount }}
              </b-col>
            </b-row>
          </b-container>
          <b-table
            id="aquifers-results"
            :current-page="currentPage"
            :per-page="searchResultsPerPage"
            :fields="aquiferListFields"
            :items="searchResults"
            :show-empty="emptyResults"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            empty-text="No aquifers could be found"
            striped
            outlined
            @row-clicked="rowClicked"
            :busy="searchInProgress"
            v-if="searchPerformed"
            responsive>
            <template slot="id" slot-scope="row">
              <router-link :to="{ name: 'aquifers-view', params: {id: row.item.id} }">{{ row.item.id }}</router-link>
            </template>
            <template slot="name" slot-scope="row">
              {{row.item.name}}
            </template>
            <template v-slot:table-busy>
              <div class="text-center my-2">
                <b-spinner class="align-middle"/>
                <strong> Loading...</strong>
              </div>
            </template>
          </b-table>
          <b-pagination
            v-if="searchResultCount > searchResultsPerPage"
            class="pull-right"
            :total-rows="searchResultCount"
            :per-page="searchResultsPerPage"
            v-model="currentPage"/>
        </b-col>
      </b-row>
      <h6 class="pl-5 pb-5 mt-3" v-if="searchResultCount > 0">Download searched aquifers :
        <a href="#" @click.prevent="downloadXLSX(true)">XLSX</a> |
        <a href="#" @click.prevent="downloadCSV(true)">CSV</a>
      </h6>
    </b-card>
  </div>
</template>

<style>
table.b-table > thead > tr > th.sorting::before,
table.b-table > tfoot > tr > th.sorting::before {
  display: none !important;
}
table.b-table > thead > tr > th.sorting::after,
table.b-table > tfoot > tr > th.sorting::after {
  content: "\f0dc" !important;
  font-family: "FontAwesome";
  opacity: 1 !important;
}

table.b-table tr {
  cursor: pointer;
}

table.b-table td {
  padding: .5rem;
  vertical-align: middle;
}

ul.pagination {
  justify-content: end;
}

.aquifer-search-actions {
  margin-top: 1em
}

.main-search-card .main-title {
  border-bottom: 1px solid rgba(0,0,0,0.1);
  padding-bottom: 1rem;
  font-size: 1.8em;
}

.map-column {
  margin-right: -2rem;
}

.search-title {
  font-size: 1.1em;
  padding: 0;
  margin: 0;
}

.aquifer-checkbox-group .custom-control-label:before {
  background-color: white;
  border: 1px solid #CED4DA;
}

#aquifers-search {
  background-color: #38598A;
  border-color: #38598A;
}

.aquifer-download-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.aquifer-download-list li {
  color: #37598A;
}

.aquifer-download-list li a {
  color: #37598A;
  text-decoration: underline;
  text-decoration-color: #37598A;
  text-decoration-skip-ink: none;
}
</style>

<script>
import L from 'leaflet'
import querystring from 'querystring'
import { isEqual } from 'lodash'
import { mapGetters, mapMutations, mapState, mapActions } from 'vuex'

import ApiService from '@/common/services/ApiService.js'
import { SET_CONSTRAIN_SEARCH, SET_SEARCH_BOUNDS, RESET_SEARCH, SET_SEARCH_MAP_ZOOM, SET_SEARCH_MAP_CENTRE, SET_SELECTED_SECTIONS, SET_MATCH_ANY } from '../store/mutations.types.js'
import { SEARCH_AQUIFERS } from '../store/actions.types.js'

import AquiferMap from './AquiferMap.vue'
import MapLoadingSpinner from './MapLoadingSpinner.vue'

const SEARCH_RESULTS_PER_PAGE = 10
const HYDRAULICALLY_CONNECTED_CODE = 'Hydra'
const BC_LAT_LNG_BOUNDS = L.latLngBounds(L.latLng(60.0023, -114.0541379), L.latLng(48.2245556, -139.0536706))

export default {
  components: {
    'aquifer-map': AquiferMap,
    'map-loading-spinner': MapLoadingSpinner
  },
  data () {
    let query = this.$route.query

    let selectedSections = query.resources__section__code ? query.resources__section__code.split(',') : []
    if (query.hydraulically_connected) {
      selectedSections.push(HYDRAULICALLY_CONNECTED_CODE)
    }

    return {
      sortBy: 'id',
      sortDesc: false,
      search: query.search,
      searchResultsPerPage: SEARCH_RESULTS_PER_PAGE,
      currentPage: 1,
      response: {},
      aquiferListFields: [
        { key: 'id', label: 'Aquifer number', sortable: true },
        { key: 'name', label: 'Aquifer name', sortable: true },
        { key: 'location', label: 'Descriptive location', sortable: true },
        { key: 'material', label: 'Material', sortable: true },
        { key: 'lsu', label: 'Litho stratigraphic unit', sortable: true },
        { key: 'subtype', label: 'Subtype', sortable: true },
        { key: 'vulnerability', label: 'Vulnerability', sortable: true },
        { key: 'area', label: 'Size-km²', sortable: true },
        { key: 'productivity', label: 'Productivity', sortable: true },
        { key: 'demand', label: 'Demand', sortable: true },
        { key: 'mapping_year', label: 'Year of mapping', sortable: true }
      ],
      layers: [],
      surveys: [],
      noSearchCriteriaError: false,
      selectedSections,
      matchAny: Boolean(query.match_any),
      selectMode: 'single',
      selectedAquiferId: null,
      loadingMap: false
    }
  },
  computed: {
    offset () { return parseInt(this.$route.query.offset, 10) || 0 },
    displayOffset () {
      return (this.currentPage * this.searchResultsPerPage) - this.searchResultsPerPage + 1
    },
    displayPageLength () {
      if (this.searchResultCount > this.searchResultsPerPage) {
        if ((this.currentPage * this.searchResultsPerPage) > this.searchResultCount) {
          return this.searchResultCount
        }
        return this.currentPage * this.searchResultsPerPage
      } else {
        return this.searchResultCount
      }
    },
    emptyResults () { return this.searchResultCount === 0 },
    query () { return this.$route.query },
    searchedAquiferIds () { return (this.searchResults || []).map((aquifer) => aquifer.id) },
    resourceSectionOptions () { return this.resourceSections && this.resourceSections.map((s) => ({ text: s.name, value: s.code })) },
    ...mapGetters(['userRoles']),
    ...mapGetters('aquiferStore/search', ['queryParams']),
    ...mapState('aquiferStore/aquiferGeoms', {
      simplifiedAquifers: 'simplifiedGeoJson'
    }),
    ...mapState('aquiferStore/search', [
      'searchErrors',
      'searchResults',
      'searchResultCount',
      'searchInProgress',
      'searchPerformed',
      'searchMapCentre',
      'searchMapZoom'
    ]),
    ...mapState('aquiferStore', {
      resourceSections: 'sections'
    })
  },
  methods: {
    ...mapActions('aquiferStore/search', [SEARCH_AQUIFERS]),
    ...mapMutations('aquiferStore/aquiferGeoms', ['updateSimplifiedGeoJson']),
    ...mapMutations('aquiferStore/search', [SET_CONSTRAIN_SEARCH, SET_SEARCH_BOUNDS, SET_CONSTRAIN_SEARCH, RESET_SEARCH, SET_SEARCH_MAP_CENTRE, SET_SEARCH_MAP_ZOOM]),
    ...mapMutations('aquiferStore', ['addSections']),
    navigateToNew () {
      this.$router.push({ name: 'new' })
    },
    downloadCSV (filterOnly) {
      let url = ApiService.baseURL + 'aquifers/csv?'
      if (filterOnly) {
        url += querystring.stringify(this.query)
      }
      window.open(url)
    },
    downloadXLSX (filterOnly) {
      let url = ApiService.baseURL + 'aquifers/xlsx?'
      if (filterOnly) {
        url += querystring.stringify(this.query)
      }
      window.open(url)
    },
    fetchSurveys () {
      ApiService.query('surveys').then((response) => {
        if (response.data) {
          response.data.forEach((survey) => {
            if (survey.survey_page === 'a' && survey.survey_enabled) {
              this.surveys.push(survey)
            }
          })
        }
      })
    },
    fetchResourceSections () {
      ApiService.query('aquifers/sections').then((response) => {
        let sections = (response.data || {}).results || []
        sections.splice(2, 0, {
          name: 'Hydraulically connected',
          code: HYDRAULICALLY_CONNECTED_CODE
        })
        this.addSections(sections)
      })
    },
    fetchSimplifiedGeometry () {
      if (this.simplifiedAquifers !== null) {
        return Promise.resolve(this.simplifiedAquifers)
      }

      return ApiService.query('gis/aquifers-simplified').then((response) => {
        const featuresCollection = response.data || {}
        const features = featuresCollection.features || []
        // Remove any features which don't have geometry
        featuresCollection.features = features.filter((feature) => feature.geometry)
        this.updateSimplifiedGeoJson(featuresCollection)
        return featuresCollection
      })
    },
    scrollToMap () {
      const map = this.$el.ownerDocument.getElementById('map')
      this.$SmoothScroll(map, 100)
    },
    triggerReset (e) {
      e.preventDefault()
      this.search = ''
      this.selectedSections = []
      this.matchAny = false
      this.selectedAquiferId = null
      this[RESET_SEARCH]()
      this.$nextTick(() => {
        this.$emit('resetLayers')
      })
    },
    triggerSearch () {
      this[SEARCH_AQUIFERS]({
        selectedSections: this.selectedSections,
        matchAny: this.matchAny,
        query: this.search
      })
    },
    updateQueryParams () {
      this.$router.replace({ query: this.queryParams })
    },
    rowClicked (data) {
      this.selectedAquiferId = data.id
      this.scrollToMap()
    },
    mapMoved (bounds, featuresOnMap, isViewReset) {
      const viewingBC = bounds.contains(BC_LAT_LNG_BOUNDS)

      this[SET_SEARCH_MAP_CENTRE](viewingBC ? null : bounds.getCenter())
      this[SET_SEARCH_BOUNDS](bounds)
      this[SET_CONSTRAIN_SEARCH](!viewingBC)
      this.updateQueryParams()
    },
    handleMapZoom (zoom, bounds) {
      const viewingBC = bounds.contains(BC_LAT_LNG_BOUNDS)

      this[SET_SEARCH_MAP_ZOOM](viewingBC ? null : zoom)
      this.updateQueryParams()
    },
    handleRouteChange () {
      const query = { ...this.$route.query }
      const emptyQuery = Object.keys(query).length === 0

      if (emptyQuery) {
        this[RESET_SEARCH]()
      } else {
        this.updateStoreStateFromQS()

        const shouldSearch = !isEqual(query, this.queryParams)

        if (shouldSearch) {
          this.triggerSearch()
        }
      }
    },
    updateStoreStateFromQS () {
      const query = this.$route.query
      // check if the page loads with a query (e.g. user bookmarked a search)
      // if so, set the search boxes to the query params
      if (Object.keys(query) === 0) { return }

      if (query.map_centre !== undefined) {
        const latlng = query.map_centre.split(',')
        const lat = parseFloat(latlng[0])
        const lng = parseFloat(latlng[1])
        this[SET_SEARCH_MAP_CENTRE](new L.latLng(lat, lng))
      }
      if (query.map_zoom !== undefined) {
        this[SET_SEARCH_MAP_ZOOM](parseInt(query.map_zoom))
      }
      if (query.constrain !== undefined) {
        this[SET_CONSTRAIN_SEARCH](Boolean(query.constrain))
      }
      if (query.resources__section__code) {
        this[SET_SELECTED_SECTIONS, query.resources__section__code.split(',').map(code => code.trim())]
      }
      if (query.match_any) {
        this[SET_MATCH_ANY, Boolean(query.match_any)]
      }
    }
  },
  watch: {
    queryParams () {
      this.updateQueryParams()
    },
    searchInProgress () {
      if (this.searchInProgress === false) {
        this.scrollToMap()
      }
    },
    $route (to, from) {
      this.handleRouteChange()
    }
  },
  created () {
    // Fetch current surveys and add 'aquifer' surveys (if any) to this.surveys to be displayed
    this.fetchSurveys()

    if (this.resourceSections.length === 0) {
      this.fetchResourceSections()
    }

    this.loadingMap = true
    this.fetchSimplifiedGeometry().then(() => {
      this.loadingMap = false
    })

    this.handleRouteChange()
  }
}
</script>
