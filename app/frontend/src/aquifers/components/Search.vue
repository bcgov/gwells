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
          <b-col cols="12" md="12" lg="12" xl="5" class="p-4">
            <h1 class="main-title ml-4 mt-2">Aquifer Search
              <div v-if='userRoles.aquifers.edit' class="pb-2 pull-right">
              <b-button
                id="aquifers-add"
                v-on:click="navigateToNew"
                v-if="userRoles.aquifers.edit"
                variant="primary">Add new Aquifer</b-button>
              </div>
            </h1>

            <b-form-row>
              <b-col cols="12" md="6" class="pt-3 pl-4 pr-4 aquifer-search-column mt-3">
                <h5 class="search-title">Search by aquifer name or number (leave blank to see all aquifers)</h5>
                <b-form-group class="search-title mt-3 mb-3">
                  <b-form-input
                    type="text"
                    id="aquifers-search-field"
                    v-model="search"
                    class="w-75"/>
                </b-form-group>
                <b-form-checkbox-group
                  stacked
                  v-model="sections"
                  :options="aquifer_resource_sections"
                  class="aquifer-checkbox-group"
                />
                <b-form-row>
                    <b-form-group class="aquifer-search-actions">
                      <b-button class="aquifer-buttons" variant="primary" type="submit" id="aquifers-search">Search
                        <i v-if="loading" class="fa fa-circle-o-notch fa-spin ml-1">
                        </i>
                      </b-button>
                      <b-button class="aquifer-buttons" variant="default" type="reset">Reset</b-button>
                    </b-form-group>
                </b-form-row>
                <h6 class="mt-3">Download all aquifers</h6>
                <ul class="aquifer-download-list">
                  <li>- <a href="#" @click.prevent="downloadXLSX()">Aquifer extract (XLSX)</a></li>
                  <li>- <a href="#" @click.prevent="downloadCSV()">Aquifer extract (CSV)</a></li>
                </ul>
              </b-col>
              <b-col cols="12" md="6" class="pt-3 pl-4 pr-4 mt-3">
                <div v-if="layers.length > 0">
                  <h6>Map Layers:</h6>
                  <b-form-checkbox-group class="aquifer-checkbox-group"
                    stacked
                    v-model="activeLayers"
                    :options='layers'
                    disabled
                    checked="activeLayers"
                  />
                </div>
              </b-col>
            </b-form-row>
          </b-col>

          <b-col cols="12" md="12" lg="12" xl="7" class="map-column">
            <aquifer-map ref="aquiferMap" v-bind:aquifers="aquifers_search_results"/>
          </b-col>
        </b-form-row>

      </b-form>

      <b-row>
        <b-col cols="12" class="p-5">
          <b-container fluid v-if="aquiferList && !emptyResults" class="p-0">
            <b-row>
              <b-col cols="12" class="mb-3">
                Showing {{ displayOffset }} to {{ displayPageLength }} of {{ response.count }}
              </b-col>
            </b-row>
          </b-container>

          <b-table
            id="aquifers-results"
            :current-page="currentPage"
            :per-page="limit"
            :fields="aquiferListFields"
            :items="aquiferList"
            :show-empty="emptyResults"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            empty-text="No aquifers could be found"
            striped
            outlined
            @row-clicked="rowClicked"
            v-if="aquiferList"
            responsive>
            <template slot="aquifer_id" slot-scope="data">
              <p class="aquifer-id" v-on:click.prevent="onAquiferIdClick(data)">{{data.value}}</p>
            </template>
            <template slot="material" slot-scope="row">
              {{row.item.material_description}}
            </template>
            <template slot="subtype" slot-scope="row">
              {{row.item.subtype_description}}
            </template>
            <template slot="vulnerability" slot-scope="row">
              {{row.item.vulnerability_description}}
            </template>
            <template slot="vulnerability" slot-scope="row">
              {{row.item.vulnerability_description}}
            </template>
            <template slot="productivity" slot-scope="row">
              {{row.item.productivity_description}}
            </template>
            <template slot="demand" slot-scope="row">
              {{row.item.demand_description}}
            </template>
          </b-table>
          <b-pagination
            v-if="response.count > 30"
            class="pull-right"
            :total-rows="response.count"
            :per-page="limit"
            v-model="currentPage"/>
        </b-col>
      </b-row>
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
table.b-table .aquifer-id {
  color: #37598A;
  cursor: pointer;
  text-decoration: underline;
  font-weight: bold;
  display: inline;

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

.aquifer-search-column {
  border-right: 1px solid rgba(0,0,0,0.1);
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

.aquifer-buttons {
  padding: .300rem 1.5rem;
}

#aquifers-search {
  background-color: #38598A;
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
import querystring from 'querystring'
import ApiService from '@/common/services/ApiService.js'
import AquiferMap from './AquiferMap.vue'
import { filter } from 'lodash'

import { mapGetters } from 'vuex'
const LIMIT = 30
export default {
  components: {
    'aquifer-map': AquiferMap
  },
  data () {
    let query = this.$route.query || {}
    return {
      sortBy: 'aquifer_id',
      sortDesc: false,
      search: query.search,
      aquifer_search: query.aquifer_search,
      limit: LIMIT,
      currentPage: 1,
      filterParams: Object.assign({}, query),
      aquifers_search_results: {},
      response: {},
      aquiferListFields: [
        { key: 'aquifer_id', label: 'Aquifer number', sortable: true },
        { key: 'aquifer_name', label: 'Aquifer name', sortable: true },
        { key: 'location_description', label: 'Descriptive location', sortable: true },
        { key: 'material', label: 'Material', sortable: true },
        { key: 'litho_stratographic_unit', label: 'Litho stratigraphic unit', sortable: true },
        { key: 'subtype', label: 'Subtype', sortable: true },
        { key: 'vulnerability', label: 'Vulnerability', sortable: true },
        { key: 'area', label: 'Size-km²', sortable: true },
        { key: 'productivity', label: 'Productivity', sortable: true },
        { key: 'demand', label: 'Demand', sortable: true },
        { key: 'mapping_year', label: 'Year of mapping', sortable: true }
      ],
      activeLayers: [],
      layers: [],
      surveys: [],
      noSearchCriteriaError: false,
      aquifer_resource_sections: [],
      sections: query.resources__section__code ? query.resources__section__code.split(',') : [],
      selectMode: 'single',
      loading: false
    }
  },
  computed: {
    offset () { return parseInt(this.$route.query.offset, 10) || 0 },
    displayOffset () {
      return (this.currentPage * this.limit) - this.limit + 1
    },
    displayPageLength () {
      if (this.response.count > 30) {
        if ((this.currentPage * this.limit) > this.response.count) {
          return this.response.count
        }
        return this.currentPage * this.limit
      } else {
        return this.response.count
      }
    },
    aquiferList () { return this.response && this.response.results },
    emptyResults () { return this.response && this.response.count === 0 },
    query () { return this.$route.query },
    ...mapGetters(['userRoles'])
  },
  methods: {
    navigateToNew () {
      this.$router.push({ name: 'new' })
    },
    fetchResults () {
      this.loading = true
      // trigger the Google Analytics search event
      this.triggerAnalyticsSearchEvent(this.query)
      delete this.query.offset
      delete this.query.limit
      ApiService.query('aquifers', this.query)
        .then((response) => {
          this.aquifers_search_results = response.data.results
          this.response = response.data
          this.scrollToTableTop()
          this.loading = false
        })
    },
    downloadCSV () {
      window.open(ApiService.baseURL + 'aquifers/csv?' + querystring.stringify(this.query))
    },
    downloadXLSX () {
      window.open(ApiService.baseURL + 'aquifers/xlsx?' + querystring.stringify(this.query))
    },
    fetchResourceSections () {
      ApiService.query('aquifers/sections').then((response) => {
        this.aquifer_resource_sections = response.data.results.map(function (section) {
          return {
            text: section.name,
            value: section.code
          }
        })
        console.log('Aquifer Resource', this.aquifer_resource_sections)
        this.aquifer_resource_sections.splice(2, 0, {
          text: 'Hydraulically Connected',
          value: 'Hydra'
        })
      })
    },
    scrollToTableTop () {
      this.$SmoothScroll(this.$el, 100)
    },
    triggerReset () {
      this.response = {}
      this.aquifers_search_results = {}
      this.filterParams = {}
      this.search = ''
      this.aquifer_id = ''
      this.sections = []
      this.currentPage = 1
      this.noSearchCriteriaError = false
      this.updateQueryParams()
    },
    triggerSearch () {
      delete this.filterParams.aquifer_id
      delete this.filterParams.search
      delete this.filterParams.resources__section__code
      if (this.search) {
        this.filterParams.search = this.search
      }
      if (this.sections) {
        this.filterParams.resources__section__code = this.sections.filter(o => o !== 'Hydra').join(',')
        if (this.sections.find(o => o === 'Hydra')) {
          this.filterParams.hydraulically_connected = 'yes'
        }
      }

      this.updateQueryParams()
      this.fetchResults()
    },
    updateQueryParams () {
      this.$router.replace({query: this.filterParams})
    },
    triggerAnalyticsSearchEvent (params) {
      // trigger the search event, sending along the search params as a string
      if (window.ga) {
        window.ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'AquiferSearch',
          eventLabel: querystring.stringify(params)
        })
      }
    },
    onAquiferIdClick (data) {
      this.$router.push({
        name: 'aquifers-view',
        params: { id: data.item.aquifer_id }
      })
    },
    rowClicked (data) {
      this.$refs.aquiferMap.zoomToSelectedAquifer(data)
    }
  },
  created () {
    // Fetch current surveys and add 'aquifer' surveys (if any) to this.surveys to be displayed
    ApiService.query('surveys').then((response) => {
      if (response.data) {
        response.data.forEach((survey) => {
          if (survey.survey_page === 'a') {
            this.surveys.push(survey)
          }
        })
      }
    }).catch((e) => {
      console.error(e)
    })
    this.fetchResourceSections()
  },
  mounted () {
    this.$on('activeLayers', (data) => {
      this.layers = data.filter(o => o.layerName).map(o => o.layerName)
    })
    this.$on('featuresOnMap', (data) => {
      const aquiferIdsMap = new Map()
      data.map(o => aquiferIdsMap.set(o.defaultOptions.aquifer_id, true))
      this.response.count = aquiferIdsMap.size
      this.response.results = filter(this.aquifers_search_results, o => aquiferIdsMap.get(o.aquifer_id))
    })
  }
}
</script>
