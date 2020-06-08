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
  <div id="aquifers-search" class="container p-1">
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
        v-on:submit.prevent="triggerSearch()"
        v-on:reset="triggerReset">
        <b-form-row>
          <b-col cols="12" md="12" lg="12" xl="4" class="p-4">
            <b-button
              id="aquifers-add"
              class="pull-right"
              v-on:click="navigateToNew"
              v-if="userRoles.aquifers.edit"
              variant="primary">
              Add new Aquifer
            </b-button>
            <h1 class="main-title ml-2 mt-2">Aquifer Search</h1>

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
                  <b-button class="aquifer-buttons" variant="primary" type="submit" id="aquifers-search-button" :disabled="searchInProgress">
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
              :highlightAquiferIds="searchedAquiferIds"
              :selectedId="selectedAquiferId"
              :viewBounds="mapViewBounds"
              :searchText="search"
              :showRetired="showRetiredAquifers"
              @moved="mapMoved"
              @zoomed="handleMapZoom"
              @search="mapSearch"
              @mapLoading="loadingMap = true"
              @mapLoaded="loadingMap = false"/>
          </b-col>
        </b-form-row>
      </b-form>

      <b-row>
        <b-col cols="12" class="p-5">
          <b-container fluid v-if="searchPerformed && !searchInProgress" class="p-0">
            <b-row class="mb-3">
              <b-col md="6">
                <div v-if="!emptyResults">
                  Showing {{ displayOffset }} to {{ displayPageLength }} of {{ searchResultCount }}
                </div>
              </b-col>
              <b-col md="6" class="text-right">
                <b-form-checkbox v-model="showRetiredAquifers" v-if="numRetiredAquifers > 0" class="d-inline-block">
                  Show {{numRetiredAquifers}} retired aquifers
                </b-form-checkbox>
              </b-col>
            </b-row>
          </b-container>
          <b-table
            id="aquifers-results"
            :current-page="currentPage"
            :per-page="searchResultsPerPage"
            :fields="aquiferListFields"
            :items="resultsTableData"
            :show-empty="emptyResults"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            empty-text="No aquifers could be found"
            striped
            outlined
            :busy="searchInProgress"
            v-if="searchPerformed"
            :tbody-tr-class="searchResultsRowClass"
            responsive>
            <template slot="id" slot-scope="row">
              <router-link :to="{ name: 'aquifers-view', params: {id: row.item.aquifer_id} }">{{ row.item.aquifer_id }}</router-link>
            </template>
            <template slot="name" slot-scope="row">
              {{row.item.name}}
            </template>
            <template slot="retire_date" slot-scope="row">
              <span :title="row.item.retire_date">{{ row.item.retire_date | moment("MMMM Do YYYY [at] LT") }}</span>
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

<script>
import mapboxgl from 'mapbox-gl'
import querystring from 'querystring'
import { isEqual, pick } from 'lodash'
import { mapGetters, mapMutations, mapState, mapActions } from 'vuex'
import smoothScroll from 'smoothscroll'

import ApiService from '@/common/services/ApiService.js'
import {
  SET_CONSTRAIN_SEARCH,
  SET_SEARCH_BOUNDS,
  RESET_SEARCH,
  SET_SEARCH_MAP_ZOOM,
  SET_SEARCH_MAP_CENTRE,
  SET_SELECTED_SECTIONS,
  SET_MATCH_ANY
} from '../store/mutations.types.js'
import { SEARCH_AQUIFERS } from '../store/actions.types.js'

import AquiferMap from './AquiferMap.vue'
import MapLoadingSpinner from '../../common/components/MapLoadingSpinner.vue'
import features from '../../common/features'
import { BC_LAT_LNG_BOUNDS, containsBounds } from '../../common/mapbox/geometry'

const SEARCH_RESULTS_PER_PAGE = 10
const HYDRAULICALLY_CONNECTED_CODE = 'Hydra'
const URL_QS_SEARCH_KEYS = ['constrain', 'resources__section__code', 'match_any', 'search']

const RESULTS_TABLE_FIELDS = [
  { key: 'id', label: 'Aquifer\xa0number', sortable: true },
  { key: 'name', label: 'Aquifer\xa0name', sortable: true },
  { key: 'location', label: 'Descriptive\xa0location', sortable: true },
  { key: 'material', label: 'Material', sortable: true },
  { key: 'lsu', label: 'Litho\xa0stratigraphic\xa0unit', sortable: true },
  { key: 'subtype', label: 'Subtype', sortable: true },
  { key: 'vulnerability', label: 'Vulnerability', sortable: true },
  { key: 'area', label: 'Size\u2011km²', sortable: true },
  { key: 'productivity', label: 'Productivity', sortable: true },
  { key: 'demand', label: 'Demand', sortable: true },
  { key: 'mapping_year', label: 'Year\xa0of\xa0mapping', sortable: true },
]

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
      includeRetired: false,
      layers: [],
      surveys: [],
      noSearchCriteriaError: false,
      selectedSections,
      matchAny: Boolean(query.match_any),
      selectMode: 'single',
      selectedAquiferId: null,
      mapViewBounds: null,
      loadingMap: false,
      showRetiredAquifers: Boolean(query.retired)
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
    searchedAquiferIds () { return (this.resultsTableData || []).map((aquifer) => aquifer.aquifer_id) },
    searchedAquifersBounds () {
      const bounds = new mapboxgl.LngLatBounds()
      const results = (this.resultsTableData || [])
      results.forEach((aquifer) => bounds.extend(aquifer.extent))
      return bounds
    },
    resourceSectionOptions () {
      return this.resourceSections && this.resourceSections.map((s) => ({ text: s.name, value: s.code }))
    },
    aquiferListFields () {
      const fields = RESULTS_TABLE_FIELDS.slice()
      if (this.showRetiredAquifers) {
        fields.splice(1, 0, { key: 'retire_date', label: 'Date\xa0retired', sortable: true })
      }
      return fields
    },
    resultsTableData () {
      return this.searchResults.filter((result) => {
        if (this.showRetiredAquifers) {
          return true
        }
        return result.retire_date ? new Date(result.retire_date) > new Date() : true
      })
    },
    retiredAquifers () {
      return this.searchResults.filter((result) => {
        return result.retire_date && new Date(result.retire_date) <= new Date()
      })
    },
    retiredAquifersIds () {
      return this.retiredAquifers.map((aquifer) => aquifer.aquifer_id)
    },
    numRetiredAquifers () {
      return this.retiredAquifers.length
    },
    searchResultCount () {
      return this.resultsTableData.length
    },
    ...mapGetters(['userRoles']),
    ...mapGetters('aquiferStore/search', ['queryParams', 'searchParams', 'searchResults']),
    ...mapState('aquiferStore/search', [
      'searchErrors',
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
    ...mapMutations('aquiferStore/search', [
      SET_CONSTRAIN_SEARCH,
      SET_SEARCH_BOUNDS,
      SET_CONSTRAIN_SEARCH,
      RESET_SEARCH,
      SET_SEARCH_MAP_CENTRE,
      SET_SEARCH_MAP_ZOOM,
      SET_SELECTED_SECTIONS,
      SET_MATCH_ANY
    ]),
    ...mapMutations('aquiferStore', ['addSections']),
    navigateToNew () {
      this.$router.push({ name: 'new' })
    },
    downloadCSV (filterOnly) {
      let url = `${ApiService.baseURL}aquifers/csv`
      if (filterOnly) {
        url += `?${querystring.stringify(this.searchParams)}`
      }
      window.open(url)
    },
    downloadXLSX (filterOnly) {
      let url = `${ApiService.baseURL}aquifers/xlsx`
      if (filterOnly) {
        url += `?${querystring.stringify(this.searchParams)}`
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
    scrollToMap () {
      const map = this.$el.ownerDocument.getElementById('aquifer-search-map')
      smoothScroll(map, 200)
    },
    triggerReset (e) {
      e.preventDefault()
      this.search = ''
      this.selectedSections = []
      this.matchAny = false
      this.selectedAquiferId = null
      this.showRetiredAquifers = false
      this[RESET_SEARCH]()
      this.$emit('resetLayers')
    },
    triggerSearch (options = {}) {
      let constrainSearch = !!options.constrain
      // If the search-in-map feature is not enabled use the old behaviour where all searches are
      // constrained to the visible map area.
      if (!features.searchInAquiferMap) {
        constrainSearch = true
      }

      this.loadingMap = true

      this.selectedAquiferId = null
      this[SET_CONSTRAIN_SEARCH](constrainSearch)
      this[SEARCH_AQUIFERS]({
        selectedSections: this.selectedSections,
        matchAny: this.matchAny,
        query: this.search
      })
    },
    mapSearch (zoom, bounds) {
      this[SET_SEARCH_MAP_CENTRE](bounds.getCenter())
      this[SET_SEARCH_MAP_ZOOM](zoom)
      this.triggerSearch({ constrain: true })
    },
    updateQueryParams () {
      const query = { ...this.queryParams }
      if (this.showRetiredAquifers) {
        query['show-retired'] = true
      }
      this.$router.replace({ query })
    },
    mapMoved (bounds, featuresOnMap, isViewReset) {
      const viewingBC = containsBounds(bounds, BC_LAT_LNG_BOUNDS)

      this[SET_SEARCH_MAP_CENTRE](viewingBC ? null : bounds.getCenter())
      this[SET_SEARCH_BOUNDS](viewingBC ? null : bounds)
      this.updateQueryParams()
    },
    handleMapZoom (zoom, bounds) {
      const viewingBC = containsBounds(bounds, BC_LAT_LNG_BOUNDS)

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

        this.showRetiredAquifers = Boolean(query['show-retired'])

        const cleanedQuery = pick(query, URL_QS_SEARCH_KEYS)

        const shouldSearch = !isEqual(cleanedQuery, pick(this.queryParams, URL_QS_SEARCH_KEYS))

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

      if (typeof query.map_centre === 'string') {
        const latlng = query.map_centre.split(',')
        const lat = parseFloat(latlng[0]) || null
        const lng = parseFloat(latlng[1]) || null
        if (lat && lng) {
          this[SET_SEARCH_MAP_CENTRE](new mapboxgl.LngLat(lng, lat))
        }
      }
      if (query.map_zoom !== undefined) {
        this[SET_SEARCH_MAP_ZOOM](parseInt(query.map_zoom))
      }
      if (query.constrain !== undefined) {
        this[SET_CONSTRAIN_SEARCH](Boolean(query.constrain))
      }
      if (query.resources__section__code) {
        this[SET_SELECTED_SECTIONS](query.resources__section__code.split(',').map(code => code.trim()))
      }
      if (query.match_any) {
        this[SET_MATCH_ANY](Boolean(query.match_any))
      }
    },
    searchResultsRowClass (item, type) {
      const classes = []
      if (!item || type !== 'row') { return }
      if (item.aquifer_id === this.selectedAquiferId) {
        classes.push('selected')
      }
      if (this.retiredAquifersIds.indexOf(item.aquifer_id) >= 0) {
        classes.push('retired')
      }
      return classes.join(' ')
    },
    selectAquifer (data) {
      if (this.selectedAquiferId === data.aquifer_id) { // toggle off
        this.mapViewBounds = this.searchedAquifersBounds
        this.selectedAquiferId = null
      } else {
        this.mapViewBounds = new mapboxgl.LngLatBounds(data.extent)
        this.selectedAquiferId = data.aquifer_id
      }

      this.scrollToMap()
    }
  },
  watch: {
    queryParams () {
      this.updateQueryParams()
    },
    searchInProgress () {
      // search has finished
      if (this.searchInProgress === false) {
        this.loadingMap = false
        this.mapViewBounds = this.searchedAquifersBounds
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

    this.handleRouteChange()
  }
}
</script>

<style lang="scss">
#aquifers-search {
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

  .aquifer-checkbox-group {
    .custom-control-label:before {
      background-color: white;
      border: 1px solid #CED4DA;
    }

    .custom-control-input:checked~.custom-control-label:before {
      background-color: #007bff;
    }
  }

  #aquifers-search-button {
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

  #aquifers-results {
    tr {
      &.selected {
        background-color: rgba(119, 204, 119, 0.7);
        outline-color: rgb(55, 153, 37);
      }

      &.retired td {
        opacity: 0.7;
        background-color: rgba(255, 255, 232, 0.7);
      }
    }
  }
}
</style>
