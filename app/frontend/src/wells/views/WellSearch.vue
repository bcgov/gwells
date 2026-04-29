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
  <b-card class="container p-1">
      <b-alert
        show
        variant="info"
        class="mb-4"
        v-for="(survey, index) in surveys"
        :key="`survey ${index}`">
        <p class="m-0">
          <a :href="survey.survey_link">
            {{ survey.survey_introduction_text }}
          </a>
        </p>
      </b-alert>

      <h1 class="card-title" id="wellSearchTitle">Well Search</h1>
      <div>
        <div>
          <p>
            Not all groundwater wells are registered with the province, as registration was voluntary until February 29, 2016. Data quality issues may impact search results.
          </p>
          <p>
            Search by one of the fields below, or zoom to a location on the map.
          </p>
        </div>
      </div>
      <b-row class="mt-6">
        <b-col cols="12" lg="6" xl="5">
          <b-card no-body border-variant="dark" class="mb-1">
            <b-tabs card v-model="tabIndex">
              <b-tab title="Basic Search">
                <div class="card-text">
                  <basic-search-form @search="handleSearchSubmit()" @reset="handleReset()" />
                </div>
              </b-tab>
              <b-tab title="Advanced Search">
                <div class="card-text">
                  <advanced-search-form @search="handleSearchSubmit()" @reset="handleReset()" />
                </div>
              </b-tab>
            </b-tabs>
          </b-card>
        </b-col>
        <b-col>
          <div>
            <ProgressSpinner v-if="loadingMap"/>

            <search-map
              :initialCentre="wellsStore.searchMapCentre"
              :initialZoom="wellsStore.searchMapZoom"
              :focusedWells="focusedWells"
              @boundsChanged="handleMapBoundsChange"
              @search="handleMapSearch"
              @clearSearch="handleMapClearSearch"
              @wellsLoading="mapServerErrorMessage = null; noWellsInView = null"
              @wellsLoaded="handleWellsLoaded"
              @error="handleMapError"
              @mapLoaded="handleMapReady"/>
          </div>

          <b-alert variant="danger" class="mt-2" :show="mapServerErrorMessage || noWellsInView">
            <div v-if="mapServerErrorMessage">
              {{mapServerErrorMessage}}
            </div>
            <!--  handle 0 search results in BC with "No matching wells found in BC" -->
            <div v-else-if="noWellsInView">
              <div v-if="searchBCInProgress">
                <div class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div>
                Searching all of BC for any matching wells ...
              </div>
              <div v-if="totalSearchResultsInBC === 0">
                No matching wells found
              </div>
              <div v-else>
                No matching wells found in map view.
                <span v-if="totalSearchResultsInBC <= 10">
                  <span v-if="totalSearchResultsInBC == 1">
                    <!-- Singular -->
                    Go to the
                    <a href="#" @click.prevent="focusOnWells(bcSearchResults)">one well</a>
                    that matches your search criteria
                  </span>
                  <span v-else>
                    <!-- plural -->
                    Go to the
                    <a href="#" @click.prevent="focusOnWells(bcSearchResults)">{{ englishNumber(bcSearchResults.length) }} wells</a>
                    that match your search criteria
                  </span>
                </span>
                <span v-else>
                  Please zoom out to view the {{totalSearchResultsInBC}} matching wells across BC or change your search criteria
                </span>
              </div>
            </div>
          </b-alert>
        </b-col>
      </b-row>
      <div class="my-12" v-show="wellsStore.hasSearched || hasResultErrors">
        <search-results/>
      </div>
      <div v-if="!wellsStore.hasSearched" class="mt-12">
        <p>
          Can’t find the well you are looking for? Try your search again using a different set of criteria. If you still need more assistance, Contact <a href="https://portal.nrs.gov.bc.ca/web/client/contact" target="_blank">FrontCounterBC</a>.
        </p>
        <p>
          <a href="http://www.frontcounterbc.gov.bc.ca/Start/surface-water/" target="_blank">
            Learn about and submit water license applications
          </a> with FrontCounterBC.
        </p>
      </div>
    </b-card>
</template>

<script>
import axios from 'axios'
import { isEqual } from 'lodash'
import smoothScroll from 'smoothscroll'
import { mapStores } from 'pinia'

import ApiService from '@/common/services/ApiService.js'

import { QUERY_TRIGGER, MAP_TRIGGER } from '@/wells/triggers.types.js'
import { useWellsStore } from '@/stores/wells.js'
import { useQAQCStore } from '@/stores/qaqc'

import AdvancedSearchForm from '@/wells/components/AdvancedSearchForm.vue'
import BasicSearchForm from '@/wells/components/BasicSearchForm.vue'
import SearchMap from '@/wells/components/SearchMap.vue'
import SearchResults from '@/wells/components/SearchResults.vue'
import { convertLngLatBoundsToDirectionBounds, DEFAULT_MAP_ZOOM, CENTRE_LNG_LAT_BC } from '../../common/mapbox/geometry'

export default {
  name: 'WellSearch',
  components: {
    'advanced-search-form': AdvancedSearchForm,
    'basic-search-form': BasicSearchForm,
    'search-map': SearchMap,
    'search-results': SearchResults,
  },
  data () {
    return {
      surveys: [],
      tabIndex: 0,
      scrolled: false,
      hasManuallySearched: false,
      performInitialSearch: false,
      loadingMap: false,
      noWellsInView: false,
      focusedWells: [],
      mapServerErrorMessage: null,
      showMapErrorMessage: false,
      searchBCInProgress: false,
      totalSearchResultsInBC: 0,
      bcSearchResults: []
    }
  },
  computed: {
    ...mapStores(useQAQCStore, useWellsStore),
    hasResultErrors () {
      return (this.wellsStore.searchErrors?.filter_group !== undefined && Object.entries(this.wellsStore.searchErrors.filter_group).length > 0)
    },
    hasSearchParams () {
      return Object.keys(this.searchQueryParams ?? {} ).length > 0
    }
  },
  methods: {
    handleScroll () {
      this.scrolled = window.scrollY > 100
    },
    handleMapBoundsChange (bounds, zoom, centre) {
      let isViewReset = false
      if (zoom === DEFAULT_MAP_ZOOM) {
        if (CENTRE_LNG_LAT_BC.distanceTo(centre) < 0.001) {
          isViewReset = true
        }
      }

      this.noWellsInView = false

      this.wellsStore.setSearchMapCentre(isViewReset ? null : centre)
      this.wellsStore.setSearchMapZoom(isViewReset ? null : zoom)
      this.wellsStore.setSearchBounds(convertLngLatBoundsToDirectionBounds(bounds))

      this.updateQueryParams()
    },
    handleMapSearch (bounds, options = {}) {
      this.updateQueryParams()

      if (options.showLoadingSpinner) {
        this.loadingMap = true
      }

      this.wellsStore.setSearchBounds(convertLngLatBoundsToDirectionBounds(bounds))
      this.wellsStore.searchWells({ trigger: MAP_TRIGGER, constrain: true })
    },
    handleMapClearSearch () {
      this.updateQueryParams()

      this.wellsStore.setSearchParams({})
      this.wellsStore.setSearchResultFilters({})

      this.wellsStore.searchWells({ trigger: MAP_TRIGGER, constrain: true })
    },
    handleWellsLoaded () {
      this.loadingMap = false
    },
    handleMapError (err) {
      if (err.noFeatures) {
        this.noWellsInView = true
      } else if (err.serverError) {
        this.mapServerErrorMessage = err.serverError
      }
    },
    handleMapReady (bounds) {
      if (this.performInitialSearch) {
        this.searchWellsInBC()

        this.wellsStore.setSearchBounds(convertLngLatBoundsToDirectionBounds(bounds))
        // if the page loaded with a query, start a search.
        // Otherwise, the search does not need to run (see #1713)
        this.wellsStore.searchWells({ trigger: QUERY_TRIGGER, constrain: true })
      } else {
        this.loadingMap = false
      }
    },
    handleSearchSubmit () {
      this.updateQueryParams()

      const columnsRequested = {
        'search_columns': this.wellsStore.searchResultColumns.join(',')
      }

      this.hasManuallySearched = true

      if (this.hasSearchParams) {
        // Only show the loading spinner on the map if we are going to show the search map markers
        // on the map. If the user has no search criteria then we are already showing all the wells
        // on the map via vector tiles and there is nothing to do.
        this.loadingMap = true
      }

      this.focusedWells = []

      // We limit the returned search results in all of BC to one so we can allow the user to zoom
      // to a few matching well they are looking for. We also want the count to show the user
      // how many wells outside of their current map view match their search criteria.
      this.searchWellsInBC({ limit: 10 })
    },
    handleReset () {
      this.$emit('reset')

      this.loadingMap = false
      this.noWellsInView = false
      this.focusedWells = []
      this.mapServerErrorMessage = null
      this.showMapErrorMessage = false
      this.searchBCInProgress = false
      this.totalSearchResultsInBC = 0
      this.bcSearchResults = []

      this.wellsStore.resetWellsSearch()
      // when the URL query is set to null the `handleRouteChange()` method will be triggered
      this.$router.replace({ query: null })
    },
    handleResultsUpdate () {
      // The first search that happens when page loads doesn't need to automatically scroll the
      // page. Only scroll when updating the search results.
      if (this.hasManuallySearched && !this.scrolled) {
        smoothScroll(this.$el.querySelector('#wells-search-map'))
      }
    },
    focusOnWells (wells) {
      this.focusedWells = wells.slice()
      this.noWellsInView = false
      this.showMapErrorMessage = false
    },
    setTabIndexFromUrlHash () {
      this.tabIndex = this.$route.hash === '#advanced' ? 1 : 0
    },
    updateStoreStateFromQS () {
      const query = { ...this.$route.query }
      // check if the page loads with a query (e.g. user bookmarked a search)
      // if so, set the search boxes to the query params
      if (Object.keys(query) === 0) { return }

      // Update the store with any result params in the query string
      if (query.filter_group !== undefined) {
        try {
          const resultFilters = JSON.parse(query.filter_group)
          this.wellsStore.setSearchResultFilters(resultFilters)
        } catch (SyntaxError) {}

        delete query.filter_group
      }
      if (query.limit !== undefined) {
        this.wellsStore.setSearchLimit(query.limit)
        delete query.limit
      }
      if (query.offset !== undefined) {
        this.wellsStore.setSearchOffset(query.offset)
        delete query.offset
      }
      if (query.ordering !== undefined) {
        this.wellsStore.setSearchOrdering(query.ordering)
        delete query.ordering
      }
      if (query.result_columns !== undefined) {
        this.wellsStore.setSearchResultColumns(query.result_columns.split(','))
        delete query.result_columns
      }
      if (typeof query.map_centre === 'string') {
        const latlng = query.map_centre.split(',')
        const lat = parseFloat(latlng[0]) || null
        const lng = parseFloat(latlng[1]) || null
        if (lat && lng) {
          this.wellsStore.setSearchMapCentre({ lat, lng })
        }
        delete query.map_centre
      }
      if (query.map_zoom !== undefined) {
        this.wellsStore.setSearchMapZoom(parseInt(query.map_zoom))
        delete query.map_zoom
      }
      if (query.constrain !== undefined) {
        this.wellsStore.setConstrainSearch(Boolean(query.constrain))
        delete query.constrain
      }

      this.wellsStore.setSearchParams(query)
    },
    updateQueryParams () {
      const tabHash = (this.tabIndex === 1) ? 'advanced' : null

      this.$router.replace({ query: this.buildQueryParams(), hash: tabHash })
    },
    buildQueryParams () {
      const query = { ...this.wellsStore.searchParams }

      // If params are completely empty, clear the query string, otherwise add the params to the
      // query string. This allows users to bookmark searches. Only add result params to the query
      // string if we have a search.
      if (Object.keys(query).length > 0) {
        if (Object.keys(this.wellsStore.searchResultFilters).length > 0) {
          query.filter_group = JSON.stringify(this.wellsStore.searchResultFilters)
        }
        query.result_columns = this.wellsStore.searchResultColumns.join(',')
        query.limit = String(this.wellsStore.searchLimit)
        query.offset = String(this.wellsStore.searchOffset)
        query.ordering = this.wellsStore.searchOrdering
      }
      if (this.wellsStore.searchMapCentre) {
        query.map_centre = `${this.wellsStore.searchMapCentre.lat.toFixed(6)},${this.wellsStore.searchMapCentre.lng.toFixed(6)}`
      }
      if (this.wellsStore.searchMapZoom) {
        query.map_zoom = String(this.wellsStore.searchMapZoom)
      }
      if (!this.wellsStore.constrainSearch) {
        query.constrain = String(this.wellsStore.constrainSearch)
      }

      return query
    },
    fetchSurveys () {
      ApiService.query('surveys').then((response) => {
        if (response.data) {
          response.data.forEach((survey) => {
            if (survey.survey_page === 's' && survey.survey_enabled) {
              this.surveys.push(survey)
            }
          })
        }
      })
    },
    handleRouteChange () {
      const query = this.$route.query
      const emptyQuery = Object.keys(query).length === 0
      const storeStateAsQS = this.buildQueryParams()
      // If there are query params (which means the user has performed a search) and the current
      // store's state (as a query params object) is not equal to the current query params then we
      // need to perform the search again.
      this.performInitialSearch = !emptyQuery && !isEqual(query, storeStateAsQS)

      if (emptyQuery) {
        this.wellsStore.resetWellsSearch()
      } else {
        this.updateStoreStateFromQS()
      }
    },
    searchWellsInBC (options = {}) {
      let cancelSource = this.allWellsAxiosCancelSource
      if (cancelSource) {
        cancelSource.cancel()
      }
      cancelSource = axios.CancelToken.source()
      const params = {
        ...this.searchQueryParams,
        ...options
      }
      this.searchBCInProgress = true
      return ApiService.query('wells', params, { cancelToken: cancelSource.token })
        .then((response) => {
          this.searchBCInProgress = false
          const { count, results } = response.data
          this.totalSearchResultsInBC = count
          this.bcSearchResults = results
        }).catch((err) => {
          this.searchBCInProgress = false
          throw err
        })
    },
    englishNumber (num) {
      switch (num) {
        case 1:
          return 'one'
        case 2:
          return 'two'
        case 3:
          return 'three'
        case 4:
          return 'four'
        case 5:
          return 'five'
        case 6:
          return 'six'
        case 7:
          return 'seven'
        case 8:
          return 'eight'
        case 9:
          return 'nine'
        case 10:
          return '10'
        default:
          return ''
      }
    }
  },
  watch: {
    'wellsStore.searchResults' () {
      this.handleResultsUpdate()
    },
    $route (to, from) {
      this.handleRouteChange()
    }
  },
  created () {
    this.setTabIndexFromUrlHash()
    this.fetchSurveys()
    this.handleRouteChange()
  },
  beforeMount () {
    this.loadingMap = true
    this.scrolled = window.scrollY > 100
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount () {
    window.removeEventListener('scroll', this.handleScroll)
  }
}
</script>

<style>
.wellTable[aria-busy='false'] {
  opacity: 1;
}
.wellTable[aria-busy='true'] {
  opacity: 0.6;
}
</style>
