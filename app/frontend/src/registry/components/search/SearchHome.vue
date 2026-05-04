<template>
  <div id="registry-screen">

    <!-- Active surveys -->
    <Message
        show
        variant="info"
        class="container mb-3"
        severity="info"
        v-for="(survey, index) in surveys"
        :key="`survey ${index}`">
      <p class="m-0">
        <a :href="survey.survey_link">
          {{ survey.survey_introduction_text }}
        </a>
      </p>
    </Message>

    <!-- Main Registries content -->
    <Card class="rounded-lg p-1 ml-50 mr-50 bg-white">
      <template #title>Search for a Well Driller or Well Pump Installer</template>
      <template #content>
        <div class="grid grid-cols-2 mb-5 gap-4">
          <p class="col-start-1">To update contact information or for general enquiries email <a href="mailto:Groundwater@gov.bc.ca" class="text-blue-500 hover:underline">groundwater@gov.bc.ca</a>.</p>
          <p class="col-start-1">
            <a href="https://www2.gov.bc.ca/gov/content?id=63B6DFF0024949B6867C459C19C23F88" target="_blank">
              Learn more about registering as a well driller or well pump installer in B.C.
            </a>
          </p>
        </div>

        <!-- Admin options -->
        <div v-if="userRoles.registry.edit" class="p-1 mb-3">
          <div>
            <Panel :toggleable="true" :collapsed="true" header="Administrator options">
              <div class="pb-1 gap-2 flex flex-row">
                <Button
                  type="button"
                  severity="primary"
                  id="addNewEntryButton"
                  >
                  <router-link :to="{ name: 'PersonAdd' }">
                    Add new entry
                  </router-link>
                </Button>
                <Button
                  type="button"
                  severity="primary"
                  id="manageCompaniesButton"
                  >
                  <router-link :to="{ name: 'OrganizationEdit' }">
                    Manage companies
                  </router-link>
                </Button>
              </div>
            </Panel>
          </div>
        </div>

        <!-- Search options -->
        <div class="pr-3">
          <div class="grid grid-cols-2 gap-4">
            <!-- Search form -->
            <div class="col-span-1 mb-2">
              <div class="mb-4">
                Use the search function below to define your search criteria.
                Please note: The map only shows registered well drillers and well pump installers whose base operation and address are within B.C.
                Some well drillers and well pump installers may operate in multiple areas throughout B.C.
                For a complete list refer to the results table below.
              </div>
              <Form @submit="drillerSearch" @reset="resetSearch" id="drillerSearchForm">
                <div class="grid grid-cols-4 mb-4 gap-4">
                  <label class="col-span-3">Choose professional type:
                    <RadioButtonGroup v-model="searchParams.activity" name="activitySelector" class="mt-2">
                      <RadioButton inputId="activityDriller" value="DRILL"/>
                      <label for="activityDriller" style="margin-right: 10px; margin-left: 5px;">Well Driller</label>
                      <RadioButton inputId="activityInstaller" value="PUMP"/>
                      <label for="activityInstaller" style="margin-right: 10px; margin-left: 5px;">Well Pump Installer</label>
                    </RadioButtonGroup>
                  </label>
                </div>
                <div v-if="subactivities && subactivities.length > 1" class="flex flex-col gap-2 mb-2">
                  <label for="subactivitySelector" class="flex flex-col gap-2">Choose classification(s):
                    <CheckboxGroup v-model="searchParams.subactivities" class="flex flex-col gap-2">
                      <div v-for="sub of subactivities" :key="sub.value" class="flex items-center gap-2">
                        <Checkbox
                          inputId="subactivitySelector"
                          name="subactivitySelector"
                          :value="sub.value"
                        />
                        <label :for="sub.value">{{ sub.text }}</label>
                      </div>
                    </CheckboxGroup>
                  </label>
                </div>
                <div class="grid grid-flow-col gap-4 mb-4">
                  <div class="mt-2">
                    <span>Community:</span>
                    <!-- should update based on drill or pump subactivity selection -->
                    <Listbox
                      id="cityOptions"
                      v-model="searchParams.city"
                      :options="cityList"
                      optionGroupLabel="prov"
                      optionGroupChildren="cities"
                      :virtualScrollerOptions="{ itemSize: 38 }"
                      :disabled="false"
                      class="mt-2"
                      listStyle="max-height:200px;"
                    >
                      <template #optiongroup="slotProps">
                        <div style="color: #38598a; font-style: bold; font-size: 0.875rem;">
                          <div>{{ slotProps.option.prov }}</div>
                        </div>
                      </template>
                    </Listbox>
                    <Message
                      show
                      variant="warning"
                      class="mb-3"
                      severity="warn"
                      v-if="limitSearchToCurrentMapBounds && isCommunitySelected">
                      Caution: Your are filtering the search by community ({{registryStore.searchParams.city.filter(c => c).join(", ")}}) <i>and</i> by the map area.  Ensure these two selections are consistent, or you won't get any search results.
                    </Message>
                  </div>
                </div>
                <div v-if="userRoles.registry.view" class="flex flex-col gap-2 mb-4">
                  <label for="registrationStatusSelect">Registration status:</label>
                  <Select
                  :options="regStatusOptions"
                  v-model="searchParams.status"
                  id="registrationStatusSelect"
                  name="registryStatuses"
                  class="w-full md:w-80"/>
                </div>
                <div class="flex flex-col gap-2 mb-4">
                  <label>Region:</label>
                  <Listbox
                    id="regionOptions"
                    v-model="searchParams.region"
                    :options="regionOptions"
                    optionLabel="name"
                    :virtualScrollerOptions="{ itemSize: 38 }"
                    listStyle="max-height:200px;"
                  />
                </div>
                <div class="flex flex-col gap-2 mb-4">
                  <label for="regTypeInput">
                    Individual, company, or registration number:
                  </label>
                  <InputText
                    id="regTypeInput"
                    type="text"
                    class="w-full md:w-80"
                    placeholder="Search"
                    v-model="searchParams.search"
                  />
                </div>
                <div class="mb-4">
                  <span>Entries:</span>
                  <Select
                    v-model="searchParams.limit"
                    :options="[10, 25]"
                    inputId="registriesResultsNumberSelect"
                    class="ml-2 w-24"
                  />
                </div>
                <div class="flex flex-col gap-2 mb-4">
                  <legend for="mapOptionsRadioGroup" class="flex flex-col gap-2">Map options:</legend>
                  <RadioButtonGroup v-model="limitSearchToCurrentMapBounds" name="limitSearchToCurrentMapBounds" class="flex flex-col gap-2">
                    <div>
                      <RadioButton :value="false" inputId="dontLimitSearchToMap"/>
                      <label for="dontLimitSearchToMap" style="margin-right: 10px; margin-left: 5px;">Snap map to search results</label>
                    </div>
                    <div>
                      <RadioButton :value="true" inputId="limitSearchToMap"/>
                      <label for="limitSearchToMap" style="margin-right: 10px; margin-left: 5px;">Limit search to map area</label>
                    </div>
                  </RadioButtonGroup>
                  <label class="ml-4">
                    <Checkbox
                      class="ml-4"
                      v-model="refreshOnMapChange"
                      id="refreshOnMapChange"
                      :disabled="!limitSearchToCurrentMapBounds"
                      style="margin-right: 5px"
                    />
                    Refresh search results when map area changes
                  </label>
                </div>
                <div class="flex flex-row gap-2 mb-4">
                  <Button
                    label="Submit"
                    type="submit"
                    :disabled="loading || isSearchInProgress">
                    <i v-if="isSearchInProgress" class="fa fa-circle-o-notch fa-spin ml-1"/>
                  </Button>
                  <Button label="Reset" type="button" severity="warn" @click="resetSearch"/>
                </div>
              </Form>
            </div>

            <!-- search map -->
            <div class="col-span-1">
              <registry-map
                ref="registryMap"
                />
            </div>
          </div>

          <div id="registry-download" v-if="userRoles.registry.view">
            <h6 class="mt-3">Download everyone in registry</h6>
            <ul class="ml-3">
              <li><a href="drillers/xlsx" @click.prevent="downloadFile" class="text-blue-500 hover:underline">Registries extract (XLSX)</a></li>
              <li><a href="drillers/csv" @click.prevent="downloadFile" class="text-blue-500 hover:underline">Registries extract (CSV)</a></li>
            </ul>
          </div>
        </div>
      </template>

        <!-- Search results table -->
      <template id="search-results-table" #footer>
        <div v-if="!loading && !isSearchInProgress">
          <div>
            <div v-if="!hasResults && hasSearched">
              No results were found.
            </div>
            <div v-if="listError">
              <api-error :error="listError" :on-clear="() => registryStore.setListError(null)"></api-error>
            </div>
          </div>
          <div v-if="hasResults">
            <div class="col-xs-12 col-sm-4">
              <h3 class="text-2xl font-bold mb-2">{{ activityTitle }} Results</h3>
            </div>
            <div cols="12">
              To update contact information email <a href="mailto:Groundwater@gov.bc.ca" class="text-blue-500 hover:underline">groundwater@gov.bc.ca</a>.
            </div>
            <div cols="12" class="mt-2">
              <registry-table @sort="sortTable"/>
            </div>
          </div>
          <div id="searched-registry-download" v-if="hasResults && userRoles.registry.view">
            Download searched well driller or well pump installer:
            <a :href="`drillers/xlsx?${downloadLinkQS}`" @click.prevent="downloadFile" class="text-blue-500 hover:underline">XLSX</a> |
            <a :href="`drillers/csv?${downloadLinkQS}`" @click.prevent="downloadFile" class="text-blue-500 hover:underline">CSV</a>
          </div>
          <div v-if="hasResults" class="mt-5">
            <register-legal-text class="register-legal" :activity="activity"/>
          </div>
        </div>
      </template>

    </Card>
  </div>
</template>

<script>
import querystring from 'querystring-es3'
import mapboxgl from 'mapbox-gl'
import { omit } from 'lodash'
import axios from 'axios'

import ApiService from '@/common/services/ApiService.js'
import RegistryMap from '@/registry/components/search/RegistryMap.vue'
import SearchTable from '@/registry/components/search/SearchTable.vue'
import LegalText from '@/registry/components/Legal.vue'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import { useRegistryStore } from '@/stores/registry.js'
import { useCommonStore } from '@/stores/common.js'

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
      surveys: [],
      registryStore: useRegistryStore(),
      commonStore: useCommonStore()
    }
  },
  computed: {
    userRoles () { return this.commonStore.userRoles },
    searchParams () { return this.registryStore.searchParams },
    drillerOptions () { return this.registryStore.drillerOptions },
    loading () { return this.registryStore.loading },
    listError () { return this.registryStore.listError },
    cityList () { return this.registryStore.cityList[this.formatActivityForCityList] },
    regionOptions () { return this.registryStore.regionOptions},
    searchResponse () { return this.registryStore.searchResponse },
    activity () { return this.registryStore.activity },
    hasSearched () { return this.registryStore.hasSearched },
    isSearchInProgress () { return this.registryStore.isSearchInProgress },
    lastSearchedParams () { return this.registryStore.lastSearchedParams },
    user () { return this.registryStore.user },
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
    subactivities () {
      if (!this.drillerOptions) {
        return []
      }
      return this.drillerOptions[this.searchParams.activity].subactivity_codes.map((item) => { return { 'text': item.description, 'value': item.registries_subactivity_code } })
    },
    isCommunitySelected () {
      return this.searchParams && this.searchParams.city && this.searchParams.city.filter(c => c !== '').length > 0
    },
    downloadLinkQS () {
      if (!this.lastSearchedParams || !this.lastSearchedParams.api) {
        return ''
      }
      return querystring.stringify(omit(this.lastSearchedParams.api, 'limit'))
    },
    hasResults () {
      return this.searchResponse && this.searchResponse.results && this.searchResponse.results.length > 0
    },
    refreshOnMapChange: {
      get () { return this.registryStore.doSearchOnBoundsChange },
      set (value) { this.registryStore.setDoSearchOnBoundsChange(value) }
    },
    limitSearchToCurrentMapBounds: {
      get () { return this.registryStore.limitSearchToCurrentMapBounds },
      set (value) { this.registryStore.setLimitSearchToCurrentMapBounds(value) }
    }
  },
  watch: {
    'searchParams.activity': function () {
      this.registryStore.setSearchParams(Object.assign({}, this.searchParams, { city: [''] }))
      this.resetSelectedSubactivities(this.subactivities)
      this.registryStore.fetchCityList(this.formatActivityForCityList)
    },
    subactivities: function (subactivities) {
      if (!this.searchParams.subactivities || !this.searchParams.subactivities.length) {
        this.resetSelectedSubactivities(subactivities)
      }
    },
    'searchParams.city': function (selectedCities) {
      this.zoomToSelectedCities(selectedCities)
    },
    'searchParams.region': function (selectedRegions) {
    },
    user: function () {
      this.resetSearch()
    }
  },
  methods: {
    resetSelectedSubactivities (subactivities) {
      const newSubactivities = subactivities
        ? subactivities.map(item => item.value)
        : []
      this.registryStore.setSearchParams(Object.assign({}, this.searchParams, { subactivities: newSubactivities }))
    },
    drillerSearch () {
      const params = this.searchParams

      // If the search parameters specify a page offset, disregard it.
      // (This method always performs a fresh search and results should
      // start at page 1.)
      if (params.hasOwnProperty('offset')) {
        delete params.offset
      }
      this.registryStore.search(params)
    },
    sortTable ({ field, order }) {
      if (!this.lastSearchedParams) {
        return
      }
      this.lastSearchedParams.raw['ordering'] = order === 1 ? field : `-${field}`
      this.registryStore.search(this.lastSearchedParams.raw)
    },
    downloadFile (e) {
      if (!e.ctrlKey) {
        ApiService.download(e.currentTarget.getAttribute('href'))
      }
    },
    // returns a promise with results from BC Physical Address Geocoder API
    geocodeCity (city) {
      return axios.get(
        'https://geocoder.api.gov.bc.ca/addresses.json',
        { params: { maxResults: 1, provinceCode: 'BC', localities: city, matchPrecision: 'locality', addressString: city } }
      )
    },
    zoomToSelectedCities (selectedCities) {
      if (selectedCities && selectedCities !== '') {
        const lngLats = []
        let numResponses = 0
        const onGeocodeSuccess = (resp) => {
          numResponses++
          // Although we can ask the geocoder to return only locations in BC, it doesn't
          // respect this request.  We work around this limitation by filtering out non-BC
          // feature from the response.
          const featuresInBc = resp.data.features.filter(
            f => f.properties.provinceCode === 'BC'
          )
          if (featuresInBc.length) {
            const feature = featuresInBc[0]
            lngLats.push(new mapboxgl.LngLat(feature.geometry.coordinates[0], feature.geometry.coordinates[1]))
          }
          checkAllGeocodesComplete()
        }
        const onGeocodeError = (err) => {
          console.log(err)
          numResponses++
          checkAllGeocodesComplete()
        }
        const checkAllGeocodesComplete = () => {
          if (numResponses === selectedCities.length) {
            if (lngLats.length === 1) {
              this.registryStore.requestMapPosition({ centre: lngLats[0] })
            } else if (lngLats.length > 1) {
              // Build a LngLatBounds object that contains the
              // geocoded points representing all the selected cities
              const bounds = new mapboxgl.LngLatBounds()
              lngLats.forEach((lngLats) => {
                bounds.extend(lngLats)
              })
              this.registryStore.requestMapPosition({ bounds: bounds })
            }
          }
        }
        for (var i = 0; i < selectedCities.length; i++) {
          const city = selectedCities[i]
          this.geocodeCity(city).then(
            onGeocodeSuccess,
            onGeocodeError
          )
        }
      }
    },
    resetSearch () {
      this.registryStore.resetSearch()
    }
  },
  created () {
    this.registryStore.fetchCityList(this.formatActivityForCityList)
    this.registryStore.fetchDrillerOptions()

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
