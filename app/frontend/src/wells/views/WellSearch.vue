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
          <search-map ref="searchMap" @moved="handleMapMoveEnd" />
          <b-alert variant="danger" class="mt-2" :show="locationErrorMessage !== ''">{{ locationErrorMessage }}</b-alert>
        </b-col>
      </b-row>
      <b-row class="my-5" v-show="!isInitialSearch || hasResultErrors">
        <b-col>
          <search-results />
        </b-col>
      </b-row>
      <b-row v-if="!isInitialSearch">
        <b-col>
          <p>
            Can’t find the well you are looking for? Try your search again using a different set of criteria. If you still need more assistance, Contact <a href="https://portal.nrs.gov.bc.ca/web/client/contact">FrontCounterBC</a>.
          </p>
          <p>
            <a href="http://www.frontcounterbc.gov.bc.ca/Start/surface-water/" @click="handleOutboundLinkClicks('www.frontcounterbc.gov.bc.ca/Start/surface-water/')">
                Learn about and submit water license applications
            </a>  with FrontCounterBC.
          </p>
        </b-col>
      </b-row>
    </b-card>
</template>

<script>
import querystring from 'querystring'
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
  SET_SEARCH_RESULT_FILTERS
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
      isInitialSearch: true,
      tabIndex: 0,
      latitude: null,
      longitude: null,
      mapBounds: {},

      // flag to indicate that the search should reset without a further API request
      searchShouldReset: false
    }
  },
  computed: {
    ...mapGetters([
      'locationErrorMessage',
      'searchErrors',
      'searchLimit',
      'searchOffset',
      'searchOrdering',
      'searchParams',
      'searchResults',
      'searchResultColumns',
      'searchResultFilters'
    ]),
    hasResultErrors () {
      return (this.searchErrors.filter_group !== undefined && Object.entries(this.searchErrors.filter_group).length > 0)
    }
  },
  methods: {
    handleScroll () {
      const pos = this.$el.querySelector('#map').scrollTop | 100
      this.scrolled = window.scrollY > 0.9 * pos
    },
    handleMapMoveEnd () {
      this.updateQueryParams()
    },
    handleSearchSubmit () {
      this.updateQueryParams()

      // send the analytic event when triggering search by the search button

      const columnsRequested = {
        'search_columns': this.searchResultColumns.join(',')
      }

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
      this.$nextTick(() => {
        this.$router.push({ query: null })
      })
    },
    handleResultsUpdate () {
      // the first search that happens when page loads doesn't need
      // to automatically scroll the page.  Only scroll when updating
      // the search results.
      if (!this.isInitialSearch && !this.scrolled) {
        this.$SmoothScroll(this.$el.querySelector('#map'))
      }
      // flag that the initial search that happens on page load
      // has already occurred.
      this.isInitialSearch = false
    },
    initTabIndex () {
      const hash = this.$route.hash
      if (hash === '#advanced') {
        this.tabIndex = 1
      } else {
        this.tabIndex = 0
      }
    },
    initQueryParams () {
      const query = this.$route.query
      // check if the page loads with a query (e.g. user bookmarked a search)
      // if so, set the search boxes to the query params
      if (!(Object.entries(query).length !== 0 && query.constructor === Object)) {
        return
      }

      // Update the store with any result params in the query string
      if (query.filter_group !== undefined) {
        try {
          const resultFilters = JSON.parse(query.filter_group)
          this.$store.commit(SET_SEARCH_RESULT_FILTERS, resultFilters)
        } catch (SyntaxError) {} finally {
          delete query.filter_group
        }
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

      this.$store.commit(SET_SEARCH_PARAMS, { ...query })
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
    updateQueryParams () {
      const params = { ...this.searchParams }
      const paramsEmpty = Object.entries(params).length === 0 && params.constructor === Object

      // if params are completely empty, clear the query string,
      // otherwise add the params to the query string.  this allows
      // users to bookmark searches. Only add result params to the
      // query string if we have a search.
      const query = paramsEmpty ? null : params
      if (query !== null) {
        if (Object.entries(this.searchResultFilters).length > 0) {
          query.filter_group = JSON.stringify(this.searchResultFilters)
        }
        query.result_columns = this.searchResultColumns.join(',')
        query.limit = this.searchLimit
        query.offset = this.searchOffset
        query.ordering = this.searchOrdering
      }

      const tabHash = (this.tabIndex === 1) ? 'advanced' : null

      this.$router.push({ query: query, hash: tabHash })
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
      }).catch((e) => {
        console.error(e)
      })
    }
  },
  watch: {
    searchResults (results) {
      this.handleResultsUpdate()
    }
  },
  created () {
    this.initQueryParams()
    this.initTabIndex()
    this.fetchSurveys()

    // if the page loaded with a query, start a search.
    // Otherwise, the search does not need to run (see #1713)
    const query = this.$route.query
    if (Object.entries(query).length !== 0 && query.constructor === Object) {
      this.$store.dispatch(SEARCH_LOCATIONS)
      this.$store.dispatch(SEARCH_WELLS, { constrain: false, trigger: QUERY_TRIGGER })
    }

    this.$store.subscribeAction((action, state) => {
      if (action.type === RESET_WELLS_SEARCH) {
        this.$nextTick(() => {
          this.$router.push({ query: null })
        })
      } else if (action.type === SEARCH_WELLS) {
        this.updateQueryParams()
      }
    })
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
