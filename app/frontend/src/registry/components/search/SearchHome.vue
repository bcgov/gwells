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
    <Card>
      <template #title>
        <h1 class="card-title">Search for a Well Driller or Well Pump Installer</h1>
      </template>
      <template #content>
        <p>To update contact information or for general enquiries email <a href="mailto:Groundwater@gov.bc.ca">groundwater@gov.bc.ca</a>.</p>
        <p>
          <a href="https://www2.gov.bc.ca/gov/content?id=63B6DFF0024949B6867C459C19C23F88" target="_blank">
            Learn more about registering as a well driller or well pump installer in B.C.
          </a>
        </p>

        <!-- Admin options -->
        <Card v-if="userRoles.registry.edit" no-body class="container p-1 mb-3">
          <template #header header-tag="header" class="p-1" role="tab">
            <Button block href="#" v-b-toggle.adminPanel variant="light" class="text-left">Administrator options</Button>
          </template>
          <Panel header="adminPanel" toggleable>
            <template #content class="pb-1">
              <Button
                class="mb-2 mr-1"
                variant="primary"
                id="addNewEntryButton"
                :to="{ name: 'PersonAdd' }"
              >
                Add new entry
              </Button>
              <Button
                class="mb-2"
                variant="primary"
                id="manageCompaniesButton"
                :to="{ name: 'OrganizationEdit' }"
              >
                Manage companies
              </Button>
            </template>
          </Panel>
        </Card>

        <!-- Search options -->
        <div class="pr-3 mb-4">
          <tr class="row mt-4">
            <!-- Search form -->
            <td class="col-lg-6 col-xl-5 col-12">
              <div class="mb-3">
                Use the search function below to define your search criteria.
                Please note: The map only shows registered well drillers and well pump installers whose base operation and address are within B.C.
                Some well drillers and well pump installers may operate in multiple areas throughout B.C.
                For a complete list refer to the results table below.
              </div>
              <Form @submit="drillerSearch" @reset.prevent="resetSearch({clearDrillers: true})" id="drillerSearchForm">
                <tr class="form-row">
                  <td class="form-group">
                    <label>Choose professional type:
                      <RadioButtonGroup v-model="searchParams.activity" name="activitySelector" class="col-12">
                        <RadioButton inputId="activityDriller" value="DRILL"/>
                        <label for="activityDriller" style="margin-right: 10px; margin-left: 5px;">Well Driller</label>
                        <RadioButton inputId="activityInstaller" value="PUMP"/>
                        <label for="activityInstaller" style="margin-right: 10px; margin-left: 5px;">Well Pump Installer</label>
                      </RadioButtonGroup>
                    </label>
                  </td>
                </tr>
                <tr v-if="subactivities && subactivities.length > 1" class="form-row">
                  <td class="form-group">
                    <label for="subactivitySelector">Choose classification(s):
                      <div class="col-12">
                        <CheckboxGroup v-model="searchParams.subactivities">
                          <div v-for="sub of subactivities" :key="sub.value">
                            <Checkbox
                              inputId="subactivitySelector"
                              name="subactivitySelector"
                              :value="sub.value"
                              style="margin-bottom: 0.5rem; margin-right: 5px"
                              class="fixed-width font-weight-normal pt-2"
                            />
                            <label :for="sub.value">{{ sub.text }}</label>
                          </div>
                        </CheckboxGroup>
                      </div>
                    </label>
                  </td>
                </tr>
                <tr class="form-row">
                  <td class="col-12 md-12">
                    <div class="form-group">
                      <span>Community:</span>
                      <Listbox
                        id="cityOptions"
                        v-model="searchParams.city"
                        :options="cityList"
                        optionGroupLabel="prov"
                        optionGroupChildren="cities"
                        :virtualScrollerOptions="{ itemSize: 38 }"
                        :disabled="false"
                        class="mb-3"
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
                        class="container mb-3"
                        severity="warn"
                        v-if="limitSearchToCurrentMapBounds && isCommunitySelected">
                        Caution: Your are filtering the search by community ({{searchParams.city.filter(c => c).join(", ")}}) <i>and</i> by the map area.  Ensure these two selections are consistent, or you won't get any search results.
                      </Message>
                    </div>
                  </td>
                  <td v-if="userRoles.registry.view" class="md-5">
                    <label for="registrationStatusSelect">Registration status:
                      <Select
                      :options="regStatusOptions"
                      v-model="searchParams.status"
                      id="registrationStatusSelect"
                      name="registryStatuses"/>
                    </label>
                  </td>
                </tr>
                <tr class="form-row">
                  <td class="col-12">
                    <span>Region:</span>
                    <Listbox
                      id="regionOptions"
                      v-model="searchParams.region"
                      :options="regionOptions"
                      optionLabel="name"
                      :virtualScrollerOptions="{ itemSize: 38 }"
                      class="mb-3"
                      listStyle="max-height:200px;"
                    />
                  </td>
                </tr>
                <tr class="form-row">
                  <td class="col-12">
                    <label for="regTypeInput">Individual, company, or registration number:
                      <InputText
                        type="text"
                        class="form-control"
                        id="regTypeInput"
                        placeholder="Search"
                        v-model="searchParams.search"/>
                    </label>
                  </td>
                </tr>
                <tr class="form-row">
                  <td class="col-12">
                    <span>Entries:</span>
                      <Select
                        v-model="searchParams.limit"
                        :options="[10, 25]"
                        inputId="registriesResultsNumberSelect"/>
                  </td>
                </tr>
                <tr class="form-row">
                  <td class="form-group">
                    <label>Map options:
                      <RadioButtonGroup v-model="limitSearchToCurrentMapBounds" name="limitSearchToCurrentMapBounds" class="col-12">
                        <RadioButton value="false" inputId="dontLimitSearchToMap"/>
                        <label for="dontLimitSearchToMap" style="margin-right: 10px; margin-left: 5px;">Snap map to search results</label>
                        <RadioButton value="true" inputId="limitSearchToMap"/>
                        <label for="limitSearchToMap" style="margin-right: 10px; margin-left: 5px;">Limit search to map area</label>
                      </RadioButtonGroup>
                    </label>

                    <label>
                      Refresh search results when map area changes
                      <Checkbox
                        class="ml-4"
                        v-model="refreshOnMapChange"
                        id="refreshOnMapChange"
                        :disabled="!limitSearchToCurrentMapBounds"
                        style="margin-bottom: 0.5rem; margin-right: 5px"
                      />
                    </label>
                  </td>
                </tr>
                <tr class="form-row">
                  <td class="col-12">
                    <button
                      type="submit"
                      class="btn btn-primary registries-search-btn mr-md-1"
                      :disabled="loading || isSearchInProgress">
                      Search
                      <i v-if="isSearchInProgress" class="fa fa-circle-o-notch fa-spin ml-1"/>
                    </button>
                    <button type="reset" class="btn btn-default">Reset</button>
                  </td>
                </tr>
              </Form>
            </td>

            <!-- search map -->
            <div class="col">
              <registry-map
                ref="registryMap"
                />
            </div>
          </tr>

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
          <template v-if="!loading && !isSearchInProgress">
            <tr>
              <td v-if="!hasResults && hasSearched">
                No results were found.
              </td>
              <td v-if="listError">
                <api-error :error="listError" :on-clear="() => registryStore.setListError(null)"></api-error>
              </td>
            </tr>
            <tr v-if="hasResults">
              <div class="col-xs-12 col-sm-4">
                <h3>{{ activityTitle }} Results</h3>
              </div>
              <div cols="12">
                To update contact information email <a href="mailto:Groundwater@gov.bc.ca">groundwater@gov.bc.ca</a>.
              </div>
              <div cols="12" class="mt-2">
                <registry-table @sort="sortTable"/>
              </div>
            </tr>
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
    'searchParams.activity': function (activity) {
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
    sortTable (sortCode) {
      if (!this.lastSearchedParams) {
        return
      }
      if (this.lastSearchedParams.raw.ordering[0] !== '-') {
        this.lastSearchedParams.raw['ordering'] = `-${sortCode}`
      } else {
        this.lastSearchedParams.raw['ordering'] = `${sortCode}`
      }
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
