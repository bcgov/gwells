<template>
  <div id="registry-screen">

    <!-- Active surveys -->
    <b-alert
        show
        variant="info"
        class="container mb-3"
        v-for="(survey, index) in surveys"
        :key="`survey ${index}`">
      <p class="m-0">
        <a :href="survey.survey_link">
          {{ survey.survey_introduction_text }}
        </a>
      </p>
    </b-alert>

    <!-- Main Registries content -->
    <b-card class="container p-1">
      <h1 class="card-title">Search for a Well Driller or Well Pump Installer</h1>
      <p>To update contact information or for general enquiries email <a href="mailto:Groundwater@gov.bc.ca">groundwater@gov.bc.ca</a>.</p>
      <p>
        <a href="https://www2.gov.bc.ca/gov/content?id=63B6DFF0024949B6867C459C19C23F88" target="_blank">
          Learn more about registering as a well driller or well pump installer in B.C.
        </a>
      </p>

      <!-- Admin options -->
      <b-card v-if="userRoles.registry.edit" no-body class="container p-1 mb-3">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-btn block href="#" v-b-toggle.adminPanel variant="light" class="text-left">Administrator options</b-btn>
        </b-card-header>
        <b-collapse visible id="adminPanel">
          <b-card-body class="pb-1">
            <b-button
              class="mb-2 mr-1"
              variant="primary"
              id="addNewEntryButton"
              :to="{ name: 'PersonAdd' }"
            >
              Add new entry
            </b-button>
            <b-button
              class="mb-2"
              variant="primary"
              id="manageCompaniesButton"
              :to="{ name: 'OrganizationEdit' }"
            >
              Manage companies
            </b-button>
          </b-card-body>
        </b-collapse>
      </b-card>

      <!-- Search options -->
      <div class="pr-3 mb-4">
        <b-row class="mt-4">          
          <!-- Search form -->
          <b-col cols="12" lg="6" xl="5">
            <div class="mb-3">
              Use the search form below to locate registered well drillers and pump installers.  
              The map can be used to narrow down search results by geographic area. 
              (The map will only show wells drillers and pump installers that have known geographic positions and are in BC.)
              Registered well drillers and pump installers that do not have known geographic locations or are not in BC 
              can be located using the search form below.
            </div>
            <b-form @submit.prevent="drillerSearch" @reset.prevent="resetSearch({clearDrillers: true})" id="drillerSearchForm">
              <b-form-row>
                <b-col cols="12">
                  <b-form-group label="Choose professional type:">
                    <b-form-radio-group v-model="searchParams.activity" name="activitySelector">
                      <b-form-radio value="DRILL" id="activityDriller">Well Driller</b-form-radio>
                      <b-form-radio value="PUMP" id="activityInstaller">Well Pump Installer</b-form-radio>
                    </b-form-radio-group>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row>
                <b-col cols="12" md="12">
                  <b-form-group label="Community:" label-for="cityOptions">
                    <b-form-select
                        multiple="multiple"
                        id="cityOptions"
                        v-model="searchParams.city"
                        class="mb-3"
                        :select-size="6">
                        <option value="">All</option>
                        <optgroup
                          v-for="prov in cityList[formatActivityForCityList]"
                          v-if="prov.cities && prov.cities.length"
                          :key="prov.prov"
                          :label="prov.prov"
                        >
                          <option v-for="city in prov.cities" :key="`${city} ${prov.prov}`" :value="city">{{ city }}</option>
                        </optgroup>
                    </b-form-select>
                  </b-form-group>
                </b-col>
                <b-col cols="12" md="6" v-if="userRoles.registry.view" class="md-5">
                  <b-form-group label="Registration status" label-for="registrationStatusSelect">
                    <b-form-select
                        :options="regStatusOptions"
                        v-model="searchParams.status"
                        id="registrationStatusSelect"
                        name="registryStatuses"/>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row>
                <b-col cols="12" md="6">
                  <b-form-group label="Individual, company, or registration number" label-for="regTypeInput">
                    <b-form-input
                        type="text"
                        class="form-control"
                        id="regTypeInput"
                        placeholder="Search"
                        v-model="searchParams.search"/>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row>
                <b-col>
                  <b-form-group label="Entries:" label-for="registriesResultsNumberSelect">
                    <select
                        v-model="searchParams.limit"
                        id="registriesResultsNumberSelect">                      
                      <option>10</option>
                      <option>25</option>
                    </select>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row>
                <b-col cols="12">
                  <b-form-group label="Map options:">                    
                    <b-form-radio-group v-model="limitSearchToCurrentMapBounds" name="limitSearchToCurrentMapBounds">
                      <b-form-radio v-bind:value="false" id="dontLimitSearchToMap">Snap map to search results</b-form-radio><br/>
                      <b-form-radio v-bind:value="true" id="limitSearchToMap">Limit search to map area</b-form-radio>                                            
                    </b-form-radio-group>
                    <b-form-checkbox 
                      class="ml-4" 
                      v-model="refreshOnMapChange" 
                      id="refreshOnMapChange"
                      :disabled="!limitSearchToCurrentMapBounds">
                        Refresh search results when map area changes</b-form-checkbox>                      
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row>
                <b-col>
                  <b-form-group>
                    <button
                      type="submit"
                      class="btn btn-primary registries-search-btn mr-md-1"
                      :disabled="loading">
                      Search
                    </button>
                    <button type="reset" class="btn btn-default">Reset</button>
                  </b-form-group>
                </b-col>
              </b-form-row>
            </b-form>
          </b-col>
          
          <!-- search map -->
          <b-col>
            <registry-map
              ref="registryMap"              
              />              
          </b-col>
        </b-row>
        

        <div id="registry-download" v-if="userRoles.registry.view">
          <h6 class="mt-3">Download everyone in registry</h6>
          <ul class="ml-3">
            <li><a href="drillers/xlsx" @click.prevent="downloadFile">Registries extract (XLSX)</a></li>
            <li><a href="drillers/csv" @click.prevent="downloadFile">Registries extract (CSV)</a></li>
          </ul>
        </div>
      </div>

      <!-- Search results table -->
      <div id="search-results-table">
        <template v-if="!loading">
          <b-row>
            <b-col cols="12" v-if="!hasResults && hasSearched">
              No results were found.
            </b-col>
            <b-col cols="12" v-if="listError">
              <api-error :error="listError" resetter="SET_LIST_ERROR"></api-error>
            </b-col>
          </b-row>
          <b-row v-if="hasResults">
            <div class="col-xs-12 col-sm-4">
              <h3>{{ activityTitle }} Results</h3>
            </div>
            <b-col cols="12">
              To update contact information email <a href="mailto:Groundwater@gov.bc.ca">groundwater@gov.bc.ca</a>.
            </b-col>
            <b-col cols="12" class="mt-2">
              <registry-table @sort="sortTable"/>
            </b-col>
          </b-row>
          <div id="searched-registry-download" v-if="hasResults && userRoles.registry.view">
            Download searched well driller or well pump installer:
            <a :href="`drillers/xlsx?${downloadLinkQS}`" @click.prevent="downloadFile">XLSX</a> |
            <a :href="`drillers/csv?${downloadLinkQS}`" @click.prevent="downloadFile">CSV</a>
          </div>
          <div v-if="hasResults" class="mt-5">
            <register-legal-text class="register-legal" :activity="activity"/>
          </div>
        </template>
      </div>
    </b-card>
  </div>
</template>

<script>
import querystring from 'querystring'
import mapboxgl from 'mapbox-gl'
import { mapGetters, mapActions, mapMutations, mapState } from 'vuex'
import smoothScroll from 'smoothscroll'
import { omit } from 'lodash'

import ApiService from '@/common/services/ApiService.js'
import RegistryMap from '@/registry/components/search/RegistryMap.vue'
import SearchTable from '@/registry/components/search/SearchTable.vue'
import LegalText from '@/registry/components/Legal.vue'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import {
  FETCH_CITY_LIST,
  SEARCH,
  RESET_SEARCH,
  FETCH_DRILLER_OPTIONS,
  REQUEST_MAP_POSITION
} from '@/registry/store/actions.types'
import {
  SET_LOADING,
  SET_HAS_SEARCHED,
  SET_LAST_SEARCHED_ACTIVITY  ,
  SET_LIMIT_SEARCH_TO_CURRENT_MAP_BOUNDS,
  SET_DO_SEARCH_ON_BOUNDS_CHANGE
} from '@/registry/store/mutations.types'

export default {
  components: {
    'registry-table': SearchTable,
    'registry-map': RegistryMap,
    'api-error': APIErrorMessage,
    'register-legal-text': LegalText
  },
  data () {
    return {
      adminPanelToggle: false,
      loginPanelToggle: false,
      credentials: {
        username: null,
        password: null
      },
      lastSearchedParams: {},
      surveys: [],
    }
  },
  computed: {
    regStatusOptions () {
      let result = [
        { value: '', text: 'All' }
      ]
      if (this.drillerOptions && this.drillerOptions.approval_outcome_codes) {
        result = result.concat(this.drillerOptions.approval_outcome_codes.map((item) => { return { 'text': item.description, 'value': item.code } }))
      }
      result = result.concat({ 'text': 'Removed', 'value': 'Removed' })
      return result
    },
    formatActivityForCityList () {
      // converts activity code to a plural string compatible with cities list endpoint
      if (this.searchParams.activity === 'DRILL') {
        return 'drillers'
      }
      if (this.searchParams.activity === 'PUMP') {
        return 'installers'
      }
      return ''
    },
    activityTitle () {
      // Plain english title for results table
      const activityMap = {
        DRILL: 'Well Driller',
        PUMP: 'Well Pump Installer'
      }
      if (activityMap[this.activity]) {
        return activityMap[this.activity]
      }
      return ''
    },
    apiSearchParams () {
      // bundles searchParams into fields compatible with API
      return {
        search: this.searchParams.search,
        // prov: this.searchParams.city.split(',')[1],
        city: this.searchParams.city,
        status: this.searchParams.status,
        limit: this.searchParams.limit,
        activity: this.searchParams.activity,
        ordering: this.searchParams.ordering
      }
    },
    downloadLinkQS () {
      return querystring.stringify(omit(this.lastSearchedParams, 'limit'))
    },
    hasResults () {
      return this.searchResponse.results && this.searchResponse.results.length > 0
    },    
    refreshOnMapChange: {
      get() { return this.doSearchOnBoundsChangeFromStore },
      set(value) { this[SET_DO_SEARCH_ON_BOUNDS_CHANGE](value) }
    },
    limitSearchToCurrentMapBounds: {
      get() { return this.limitSearchToCurrentMapBoundsFromStore },
      set(value) { this[SET_LIMIT_SEARCH_TO_CURRENT_MAP_BOUNDS](value) }
    },
    ...mapState('registriesStore', {
      limitSearchToCurrentMapBoundsFromStore: 'limitSearchToCurrentMapBounds',
      doSearchOnBoundsChangeFromStore: 'doSearchOnBoundsChange'
    }),
    ...mapGetters(['userRoles']),
    ...mapGetters('registriesStore', [      
      'drillerOptions',
      'loading',
      'listError',
      'cityList',
      'searchResponse',
      'activity',
      'searchParams',
      'hasSearched',         
    ])    
  },
  watch: {
    'searchParams.activity': function () {      
      // get new city list when user changes activity (well driller or well pump installer)
      this.searchParams.city = ['']
      this.FETCH_CITY_LIST(this.formatActivityForCityList)
    },
    'searchParams.city': function (selectedCities) {
      this.zoomToSelectedCities(selectedCities)
    },
    user: function () {
      // reset search when user changes (this happens every login or logout)
      this.resetSearch()
    }
  },
  methods: {
    drillerSearch() {
      const params = this.apiSearchParams

      // save the last searched activity in the store for reference by table components
      // (e.g. for formatting table for pump installer searches)
      this[SET_LAST_SEARCHED_ACTIVITY](this.searchParams.activity || 'DRILL')

      //this[SET_LOADING](true)
      //this[SET_HAS_SEARCHED](true)
      if (window.ga) {
        window.ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'RegistrySearch',
          eventLabel: querystring.stringify(params)
        })
      }
      this.SEARCH(params).then(() => {
        smoothScroll(this.$el.querySelector('#search-results-table'), 100)

        //reset some of the form fields, but not the search results
        //this[RESET_SEARCH]({ keepActivity: true, keepLimit: true, keepSearchResults: true })
        
        this.lastSearchedParams = Object.assign({}, params)
      }).catch(() => {
        
      })
    },
    sortTable (sortCode) {
      if (this.lastSearchedParams.ordering[0] !== '-') {
        this.lastSearchedParams['ordering'] = `-${sortCode}`
      } else {
        this.lastSearchedParams['ordering'] = `${sortCode}`
      }
      this.SEARCH(this.lastSearchedParams)
    },
    downloadFile (e) {
      if (!e.ctrlKey) {
        ApiService.download(e.currentTarget.getAttribute('href'))
      }
    },        
    zoomToSelectedCities(selectedCities) {
      if (selectedCities && selectedCities != "") {
        const lngLats = []; //a list of {lat:..., lng:...} objects
        var numResponses = 0;
        const onGeocodeSuccess = (resp) => {
          numResponses++;
          if (resp.data.features.length) {
            const feature = resp.data.features[0]
            lngLats.push(new mapboxgl.LngLat(feature.geometry.coordinates[0], feature.geometry.coordinates[1]))
          }          
          checkAllGeocodesComplete();        
        }
        const onGeocodeError = (err) => {
          numResponses++;
          checkAllGeocodesComplete();
        }
        const checkAllGeocodesComplete = () => {
          if (numResponses == selectedCities.length) {
            if (lngLats.length == 1) {
              this.REQUEST_MAP_POSITION({ centre: lngLats[0] })
            }
            else if (lngLats.length > 1) {
              // Build a LngLatBounds object that contains the
              // geocoded points representing all the selected cities
              const firstLngLat = lngLats[0];
              const bounds = new mapboxgl.LngLatBounds()
              lngLats.forEach((lngLats) => {
                bounds.extend(lngLats)
              })
              this.REQUEST_MAP_POSITION({ bounds: bounds })
            }
            else {
              // None of the selected cities could be geocoded, so don't adjust the 
              // map position
            }            
          }
        }
        for (var i = 0; i < selectedCities.length; i++) {
          const city = selectedCities[i];
          ApiService.query(
            `geocoding/v5/mapbox.places/${city}.json`,
            { maxResults: 1, provinceCode: "BC", localities: city, matchPrecision: "locality" }
          ).then(onGeocodeSuccess)
        }
        
      }
    },
    resetSearch() {
      this[RESET_SEARCH]();
    },    
    ...mapMutations('registriesStore', [
      SET_LAST_SEARCHED_ACTIVITY,
      SET_HAS_SEARCHED,
      SET_LOADING,
      SET_LIMIT_SEARCH_TO_CURRENT_MAP_BOUNDS,
      SET_DO_SEARCH_ON_BOUNDS_CHANGE    
    ]),
    ...mapActions('registriesStore', [
      FETCH_DRILLER_OPTIONS,
      FETCH_CITY_LIST,
      SEARCH,  
      RESET_SEARCH, 
      REQUEST_MAP_POSITION   
    ])
  },
  created() {
    // send request for city list when app is loaded
    this.FETCH_CITY_LIST(this.formatActivityForCityList)
    this.FETCH_DRILLER_OPTIONS()

    // Fetch current surveys and add 'registries' surveys (if any) to this.surveys to be displayed
    ApiService.query('surveys').then((response) => {
      response.data.forEach((survey) => {
        if (survey.survey_page === 'r' && survey.survey_enabled) {
          this.surveys.push(survey)
        }
      })
    })
  }
}
</script>

<style lang="scss">
#registry-screen {
  #registry-download {
    ul {
      margin: 0;
      padding: 0;
    }
  }
}
</style>
