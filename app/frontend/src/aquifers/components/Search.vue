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
    <Message
        severity="info"
        class="mb-4"
        v-for="(survey, index) in surveys"
        :key="`survey ${index}`">
      <p class="m-0">
        <a :href="survey.survey_link">
          {{ survey.survey_introduction_text }}
        </a>
      </p>
    </Message>

    <Card class="main-search-card mb-4">
      <template #content>
        <Message
          v-if="noSearchCriteriaError"
          severity="danger">
          <i class="fa fa-exclamation-circle"/>&nbsp;&nbsp;At least one search field is required
        </Message>
        <Form
          @submit="triggerSearch()"
          @reset="triggerReset">
          <responsive-grid :gap="4" :cols="12" :lg="[4, 8]">
            <div>
              <Button
                id="aquifers-add"
                class="pull-right"
                @click="navigateToNew"
                v-if="commonStore.userRoles.aquifers.edit"
                label="Add new Aquifer"/>
              <h1 class="main-title ml-2 mt-2">Aquifer Search</h1>

              <div class="pl-2 pr-2 aquifer-search-column mt-4">
                <h4>Basic Search</h4>
                <h5 class="search-title">Search by aquifer name or number (leave blank to see all aquifers)</h5>
                <div class="search-title mt-4 mb-4">
                  <InputText
                    type="text"
                    id="aquifers-search-field"
                    v-model="search"
                    class="w-75"/>
                </div>
                <h4 class="pt-6">Advanced Search</h4>
                <div class="mb-4 flex flex-row gap-4">
                  <RadioButton value="true" v-model="matchAny" inputId="matchTrue"/>
                  <label for="matchTrue">Any field match</label>
                  <RadioButton value="false" v-model="matchAny" inputId="matchFalse"/>
                  <label for="matchFalse">All field match</label>
                </div>
                <CheckboxGroup
                  v-model="selectedSections"
                  class="aquifer-checkbox-group flex flex-col"
                  >
                  <div
                    v-for="option of resourceSectionOptions"
                    :key="option.value"
                    class="flex items-center gap-2">
                    <Checkbox
                      v-model="selectedSections"
                      :inputId="option.text"
                      :name="option.text"
                      :value="option.text"/>
                    <label :for="option.text">{{ option.text }}</label>
                  </div>
                </CheckboxGroup>
                <div class="aquifer-search-actions">
                  <Button class="aquifer-buttons" type="submit" id="aquifers-search-button" :disabled="searchInProgress" label="Search"/>
                  <i v-if="searchInProgress" class="fa fa-circle-o-notch fa-spin ml-1"/>
                  <Button class="aquifer-buttons" variant="default" type="reset" label="Reset"/>
                </div>
                <h6 class="mt-4">Download all aquifers</h6>
                <ul class="aquifer-download-list">
                  <li>- <a href="#" @click.prevent="downloadXLSX(false)">Aquifer extract (XLSX)</a></li>
                  <li>- <a href="#" @click.prevent="downloadCSV(false)">Aquifer extract (CSV)</a></li>
                </ul>
              </div>
            </div>

            <div>
              <ProgressSpinner v-if="loadingMap"/>

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
            </div>
          </responsive-grid>
        </Form>

        <responsive-grid cols="12" class="p-12">
          <div>
            <div v-if="searchPerformed && !searchInProgress" class="w-full">
              <responsive-grid md="6" class="mb-4">
                <div>
                  <div v-if="!emptyResults">
                    Showing {{ displayOffset }} to {{ displayPageLength }} of {{ searchResultCount }}
                  </div>
                </div>
                <div v-if="numRetiredAquifers > 0" class="text-right gap-2 flex items-center justify-end">
                  <Checkbox
                    v-model="showRetiredAquifers"
                    inputId="showRetired"
                    :binary="true"
                    class="d-inline-block"/>
                  <label for="showRetired">Show {{numRetiredAquifers}} retired aquifers</label>
                </div>
              </responsive-grid>
            </div>
            <DataTable
              id="aquifers-results"
              :value="resultsTableData || []"
              v-if="searchPerformed"
              paginator
              :rows="searchResultsPerPage"
              v-model:sort-field="sortBy"
              v-model:sort-order="sortDesc"
              :loading="searchInProgress"
              :row-class="searchResultsRowClass"
              stripedRows
              showGridlines
              tableStyle="min-width: 50rem">
              <Column
                v-for="field of aquiferListFields"
                :key="field.key"
                :field="field.key"
                :header="field.label"
                sortable>
                <template #body="{ data }">
                  <template v-if="field.key === 'id'">
                    <router-link :to="{ name: 'aquifers-view', params: {id: data.aquifer_id} }">{{ data.aquifer_id }}</router-link>
                  </template>

                  <template v-else-if="field.key === 'retire_date'"">
                  <span :title="data.retire_date">{{ formatDate(data.retire_date) }}</span></template>

                  <span v-else>
                    {{ data[field.key] }}
                  </span>
                </template>
              </Column>

              <template #empty>
                No aquifers could be found.
              </template>

              <template #loading>
                <div class="text-center my-2">
                  <ProgressSpinner class="align-middle"/>
                  <strong> Loading...</strong>
                </div>
              </template>
            </DataTable>
          </div>
        </responsive-grid>
        <h6 class="pl-12 pb-12 mt-4" v-if="searchResultCount > 0">Download searched aquifers :
          <a href="#" @click.prevent="downloadXLSX(true)">XLSX</a> |
          <a href="#" @click.prevent="downloadCSV(true)">CSV</a>
        </h6>
      </template>
    </Card>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl'
import moment from 'moment'
import querystring from 'querystring'
import { isEqual, pick } from 'lodash-es'
import { useCommonStore } from '@/stores/common.js'
import smoothScroll from 'smoothscroll'
import { useAquiferStore } from '@/stores/aquifers.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

import ApiService from '@/common/services/ApiService.js'

import AquiferMap from './AquiferMap.vue'
import features from '../../common/features.js'
import { BC_LAT_LNG_BOUNDS, containsBounds } from '../../common/mapbox/geometry.js'

const SEARCH_RESULTS_PER_PAGE = 10
const AQUIFER_NOTATION_CODE = 'Notations'
const UNPUBLISHED_AQUIFERS = 'Unpublished'
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
  { key: 'mapping_year', label: 'Year\xa0of\xa0mapping', sortable: true }
]

export default {
  components: {
    'aquifer-map': AquiferMap,
    ResponsiveGrid
  },
  data () {
    let query = this.$route.query

    let selectedSections = query.resources__section__code ? query.resources__section__code.split(',') : []
    if (query.aquifer_notations) {
      selectedSections.push(AQUIFER_NOTATION_CODE)
    }
    if (query.unpublished) {
      selectedSections.push(UNPUBLISHED_AQUIFERS)
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
    commonStore () { return useCommonStore() },
    aquiferStore () {
      return useAquiferStore()
    },
    queryParams () { return this.aquiferStore.queryParams },
    searchParams () { return this.aquiferStore.searchParams },
    searchResults () { return this.aquiferStore.searchResults },
    searchErrors () { return this.aquiferStore.searchErrors },
    searchInProgress () { return this.aquiferStore.searchInProgress },
    searchPerformed () { return this.aquiferStore.searchPerformed },
    searchMapCentre () { return this.aquiferStore.searchMapCentre },
    searchMapZoom () { return this.aquiferStore.searchMapZoom },
    resourceSections () { return this.aquiferStore.sections }
  },
  methods: {
    searchAquifers (payload) { this.aquiferStore.searchAquifers(payload) },
    setConstrainSearch (v) { this.aquiferStore.setConstrainSearch(v) },
    setSearchBounds (v) { this.aquiferStore.setSearchBounds(v) },
    resetSearch () { this.aquiferStore.resetSearch() },
    setSearchMapCentre (v) { this.aquiferStore.setSearchMapCentre(v) },
    setSearchMapZoom (v) { this.aquiferStore.setSearchMapZoom(v) },
    setSelectedSections (v) { this.aquiferStore.setSelectedSections(v) },
    setMatchAny (v) { this.aquiferStore.setMatchAny(v) },
    addSections (payload) { this.aquiferStore.addSections(payload) },
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
        // remove pumping stress index option
        const idx = sections.findIndex(s => s.code === 'P')
        if (idx > -1) {
          sections.splice(idx, 1)
        }
        // add aquifer notations to search options
        sections.splice(1, 0, {
          name: 'Aquifer notations',
          code: AQUIFER_NOTATION_CODE
        })
        if (this.commonStore.userRoles.aquifers.edit) {
          sections.push({
            name: 'Unpublished aquifers',
            code: UNPUBLISHED_AQUIFERS
          })
        }
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
      this.resetSearch()
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
      this.setConstrainSearch(constrainSearch)
      this.searchAquifers({
        selectedSections: this.selectedSections,
        matchAny: this.matchAny,
        query: this.search
      })
    },
    mapSearch (zoom, bounds) {
      this.setSearchMapCentre(bounds.getCenter())
      this.setSearchMapZoom(zoom)
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

      this.setSearchMapCentre(viewingBC ? null : bounds.getCenter())
      this.setSearchBounds(viewingBC ? null : bounds)
      this.updateQueryParams()
    },
    handleMapZoom (zoom, bounds) {
      const viewingBC = containsBounds(bounds, BC_LAT_LNG_BOUNDS)

      this.setSearchMapZoom(viewingBC ? null : zoom)
      this.updateQueryParams()
    },
    handleRouteChange () {
      const query = { ...this.$route.query }
      const emptyQuery = Object.keys(query).length === 0

      if (emptyQuery) {
        this.resetSearch()
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
          this.setSearchMapCentre(new mapboxgl.LngLat(lng, lat))
        }
      }
      if (query.map_zoom !== undefined) {
        this.setSearchMapZoom(parseInt(query.map_zoom))
      }
      if (query.constrain !== undefined) {
        this.setConstrainSearch(Boolean(query.constrain))
      }
      if (query.resources__section__code) {
        this.setSelectedSections(query.resources__section__code.split(',').map(code => code.trim()))
      }
      if (query.match_any) {
        this.setMatchAny(Boolean(query.match_any))
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
    },
    formatDate (value) {
      if (!value) {
        return ''
      }
      const m = moment(value)
      return m.isValid() ? m.format("MMMM Do YYYY [at] LT") : ''
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
