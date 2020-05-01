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
          class="mb-3"
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
      <b-row class="mt-4">
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
          <search-map
            ref="searchMap"
            :initialCentre="searchMapCentre"
            :initialZoom="searchMapZoom"
            @moved="handleMapMoveEnd"
            @zoomed="handleMapZoom"
            @search="handleMapSearch"
            @ready="handleMapReady"/>
          <b-alert variant="danger" class="mt-2" :show="locationErrorMessage !== ''">{{ locationErrorMessage }}</b-alert>
        </b-col>
      </b-row>
      <b-row class="my-5" v-show="hasSearched || hasResultErrors">
        <b-col>
          <search-results />
        </b-col>
      </b-row>
      <b-row v-if="!hasSearched" class="mt-5">
        <b-col>
          <p>
            Can’t find the well you are looking for? Try your search again using a different set of criteria. If you still need more assistance, Contact <a href="https://portal.nrs.gov.bc.ca/web/client/contact" target="_blank">FrontCounterBC</a>.
          </p>
          <p>
            <a href="http://www.frontcounterbc.gov.bc.ca/Start/surface-water/" @click="handleOutboundLinkClicks('www.frontcounterbc.gov.bc.ca/Start/surface-water/')" target="_blank">
              Learn about and submit water license applications
            </a> with FrontCounterBC.
          </p>
        </b-col>
      </b-row>
    </b-card>
</template>

<script>
import querystring from 'querystring'
import { isEqual } from 'lodash'
import ApiService from '@/common/services/ApiService.js'

import { mapGetters } from 'vuex'
import {
  RESET_WELLS_SEARCH,
  SEARCH_LOCATIONS,
  SEARCH_WELLS
} from '@/wells/store/actions.types.js'
import {
  SET_SEARCH_LIMIT,
  SET_SEARCH_OFFSET,
  SET_SEARCH_ORDERING,
  SET_SEARCH_PARAMS,
  SET_SEARCH_RESULT_COLUMNS,
  SET_SEARCH_RESULT_FILTERS,
  SET_SEARCH_MAP_CENTRE,
  SET_SEARCH_MAP_ZOOM,
  SET_CONSTRAIN_SEARCH
} from '@/wells/store/mutations.types.js'
import { QUERY_TRIGGER } from '@/wells/store/triggers.types.js'
import AdvancedSearchForm from '@/wells/components/AdvancedSearchForm.vue'
import BasicSearchForm from '@/wells/components/BasicSearchForm.vue'
import SearchMap from '@/wells/components/SearchMap.vue'
import SearchResults from '@/wells/components/SearchResults.vue'

export default {
  name: 'WellSearch',
  components: {
    'advanced-search-form': AdvancedSearchForm,
    'basic-search-form': BasicSearchForm,
    'search-map': SearchMap,
    'search-results': SearchResults
  },
  data () {
    return {
      surveys: [],
      scrolled: false,
      mapError: null,

      isBusy: false,
      tabIndex: 0,
      latitude: null,
      longitude: null,
      mapBounds: {},

      // flag to indicate that the search should reset without a further API request
      searchShouldReset: false,
      hasManuallySearched: false,

      performInitialSearch: false
    }
  },
  computed: {
    ...mapGetters([
      'locationErrorMessage',
      'hasSearched',
      'searchErrors',
      'searchLimit',
      'searchOffset',
      'searchOrdering',
      'searchParams',
      'searchResults',
      'searchResultColumns',
      'searchResultFilters',
      'searchMapCentre',
      'searchMapZoom',
      'constrainSearch'
    ]),
    hasResultErrors () {
      return (this.searchErrors.filter_group !== undefined && Object.entries(this.searchErrors.filter_group).length > 0)
    }
  },
  methods: {
    handleScroll () {
      this.scrolled = window.scrollY > 100
    },
    handleMapMoveEnd (centre, isViewReset) {
      const coords = {
        lat: centre.lat,
        lng: centre.lng
      }
      this.$store.commit(SET_SEARCH_MAP_CENTRE, isViewReset ? null : coords)
      this.updateQueryParams()
    },
    handleMapZoom (zoom, isViewReset) {
      this.$store.commit(SET_SEARCH_MAP_ZOOM, isViewReset ? null : zoom)
      this.updateQueryParams()
    },
    handleSearchSubmit () {
      this.updateQueryParams()

      const columnsRequested = {
        'search_columns': this.searchResultColumns.join(',')
      }

      this.hasManuallySearched = true

      // send the analytic event when triggering search by the search button
      this.triggerAnalyticsSearchEvent(
        Object.assign(
          {},
          this.searchParams,
          columnsRequested
        )
      )
    },
    handleReset () {
      this.resetMapBounds()
      this.$store.dispatch(RESET_WELLS_SEARCH)
      this.$router.replace({ query: null })
    },
    handleResultsUpdate () {
      // The first search that happens when page loads doesn't need to automatically scroll the
      // page. Only scroll when updating the search results.
      if (this.hasManuallySearched && !this.scrolled) {
        this.$SmoothScroll(this.$el.querySelector('#well-search-map'))
      }
    },
    handleMapSearch () {
      this.updateQueryParams()
    },
    handleMapReady () {
      if (this.performInitialSearch) {
        // if the page loaded with a query, start a search.
        // Otherwise, the search does not need to run (see #1713)
        this.$store.dispatch(SEARCH_LOCATIONS)
        this.$store.dispatch(SEARCH_WELLS, { trigger: QUERY_TRIGGER })
      }
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
          this.$store.commit(SET_SEARCH_RESULT_FILTERS, resultFilters)
        } catch (SyntaxError) {}

        delete query.filter_group
      }
      if (query.limit !== undefined) {
        this.$store.commit(SET_SEARCH_LIMIT, query.limit)
        delete query.limit
      }
      if (query.offset !== undefined) {
        this.$store.commit(SET_SEARCH_OFFSET, query.offset)
        delete query.offset
      }
      if (query.ordering !== undefined) {
        this.$store.commit(SET_SEARCH_ORDERING, query.ordering)
        delete query.ordering
      }
      if (query.result_columns !== undefined) {
        this.$store.commit(SET_SEARCH_RESULT_COLUMNS, query.result_columns.split(','))
        delete query.result_columns
      }
      if (query.map_centre !== undefined) {
        const latlng = query.map_centre.split(',')
        const lat = parseFloat(latlng[0])
        const lng = parseFloat(latlng[1])
        this.$store.commit(SET_SEARCH_MAP_CENTRE, { lat, lng })
        delete query.map_centre
      }
      if (query.map_zoom !== undefined) {
        this.$store.commit(SET_SEARCH_MAP_ZOOM, parseInt(query.map_zoom))
        delete query.map_zoom
      }
      if (query.constrain !== undefined) {
        this.$store.commit(SET_CONSTRAIN_SEARCH, Boolean(query.constrain))
        delete query.constrain
      }

      this.$store.commit(SET_SEARCH_PARAMS, query)
    },
    updateQueryParams () {
      const tabHash = (this.tabIndex === 1) ? 'advanced' : null

      this.$router.replace({ query: this.buildQueryParams(), hash: tabHash })
    },
    buildQueryParams () {
      const query = { ...this.searchParams }

      // If params are completely empty, clear the query string, otherwise add the params to the
      // query string. This allows users to bookmark searches. Only add result params to the query
      // string if we have a search.
      if (Object.keys(query).length > 0) {
        if (Object.keys(this.searchResultFilters).length > 0) {
          query.filter_group = JSON.stringify(this.searchResultFilters)
        }
        query.result_columns = this.searchResultColumns.join(',')
        query.limit = String(this.searchLimit)
        query.offset = String(this.searchOffset)
        query.ordering = this.searchOrdering
      }
      if (this.searchMapCentre) {
        query.map_centre = `${this.searchMapCentre.lat.toFixed(6)},${this.searchMapCentre.lng.toFixed(6)}`
      }
      if (this.searchMapZoom) {
        query.map_zoom = String(this.searchMapZoom)
      }
      if (this.constrainSearch) {
        query.constrain = String(this.constrainSearch)
      }

      return query
    },
    handleOutboundLinkClicks (link) {
      if (window.ga) {
        window.ga('send', 'event', {
          eventCategory: 'Outbound Link',
          eventAction: 'click',
          eventLabel: link
        })
      }
    },
    triggerAnalyticsSearchEvent (params) {
      // trigger the search event, sending along the search params as a string

      if (window.ga) {
        window.ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'WellSearch',
          eventLabel: querystring.stringify(params)
        })
      }
    },
    resetMapBounds () {
      if (this.$refs.searchMap && this.$refs.searchMap.resetView) {
        this.$refs.searchMap.resetView()
      }
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
        this.$store.dispatch(RESET_WELLS_SEARCH)
      } else {
        this.updateStoreStateFromQS()
      }
    }
  },
  watch: {
    searchResults (results) {
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
    this.scrolled = window.scrollY > 100
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeDestroy () {
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
