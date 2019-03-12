<template>
  <b-card class="container container-wide p-1">
    <h1 class="card-title" id="wellSearchTitle">Well Search</h1>

    <b-row class="mt-3">
      <b-col cols="12" lg="6" xl="5">
        <b-form @submit.prevent="handleSearchSubmit()" @reset.prevent="resetButtonHandler()">
          <b-row>
            <b-col>
              <p>
                Not all groundwater wells are registered with the province, as registration was voluntary until February 29, 2016. Data quality issues may impact search results.
              </p>
              <p>
                Search by one of the fields below, or zoom to a location on the map and select the "Search Wells in this Area" button.
              </p>
            </b-col>
          </b-row>
          <b-row v-show="!showAdvancedSearch">
            <b-col>
              <b-form-group>
                <form-input id="id_search" group-class="font-weight-bold" v-model="searchParams.search">
                  <label>
                    Search by well tag or ID plate number, street address, city or owner name
                    <b-badge pill variant="primary" v-b-popover.hover="'Enter the well electronic filing number or physical identification plate number, or the street address, city or well owner name.'"><i class="fa fa-question fa-lg"></i></b-badge>
                  </label>
                </form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="my-3">
            <b-col>
              <b-btn variant="primary" type="submit">Search</b-btn>
              <b-btn variant="dark" type="reset" class="mx-2">Reset</b-btn>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-card no-body border-variant="dark">
                <b-card-header>
                  <a class="card-link" href="#" @click.prevent="toggleAdvancedSearch">Advanced Search</a>
                </b-card-header>
                <b-collapse id="advanced_search_form" v-model="showAdvancedSearch">
                  <b-card-body body-border-variant="dark">
                    <template v-for="section in defaultFilters">
                      <h3 :key="section.header">{{ section.header }}</h3>
                      <template v-for="field in section.fields">
                        <search-form-radio
                          v-if="field.type === 'radio'"
                          :key="field.id"
                          :id="`${field.id}Filter`"
                          :label="field.label"
                          label-cols="5"
                          v-model="searchParams[field.param]"
                          :options="field.options" />
                        <search-form-range
                          v-if="field.type === 'range'"
                          :key="field.id"
                          type="number"
                          label-cols="3"
                          :id="`${field.id}Filter`"
                          :label="field.label"
                          :errors="searchErrors[field.param]"
                          :step="field.step ? field.step : 'any'"
                          :min-value="searchParams[`${field.param}_min`]"
                          v-on:start-input="searchParams[`${field.param}_min`] = $event"
                          :max-value="searchParams[`${field.param}_max`]"
                          v-on:end-input="searchParams[`${field.param}_max`] = $event"/>
                        <search-form-range
                          v-if="field.type === 'dateRange'"
                          :key="field.id"
                          type="date"
                          label-cols="3"
                          :id="`${field.id}Filter`"
                          :label="field.label"
                          placeholder="YYYY/MM/DD"
                          :errors="searchErrors[field.param]"
                          :min-value="searchParams[`${field.param}_after`]"
                          v-on:start-input="searchParams[`${field.param}_after`] = $event"
                          :max-value="searchParams[`${field.param}_before`]"
                          v-on:end-input="searchParams[`${field.param}_before`] = $event"/>
                        <search-form-select
                          v-if="field.type === 'select'"
                          :key="field.id"
                          label-cols="6"
                          :id="`${field.id}Filter`"
                          :label="field.label"
                          placeholder="----------"
                          :errors="searchErrors[field.param]"
                          v-model="searchParams[field.param]"
                          :options="filterSelectOptions[field.id]"
                          :value-field="field.valueField"
                          :text-field="field.textField" />
                        <search-form-input
                          v-if="field.type === 'number' || field.type === 'text'"
                          :key="field.id"
                          :type="field.type"
                          label-cols="6"
                          :id="`${field.id}Filter`"
                          :label="field.label"
                          :errors="searchErrors[field.param]"
                          v-model="searchParams[field.param]"/>
                      </template>
                    </template>
                    <h3>Additional Fields</h3>
                    <template v-for="field in selectedFilters">
                      <b-row class="form-row" :key="field.id">
                        <b-col>
                          <search-form-radio
                            v-if="field.type === 'radio'"
                            :id="`${field.id}Filter`"
                            :label="field.label"
                            label-cols="5"
                            v-model="searchParams[field.param]"
                            :options="field.options" />
                          <search-form-range
                            v-if="field.type === 'range'"
                            type="number"
                            label-cols="6"
                            :id="`${field.id}Filter`"
                            :label="field.label"
                            :errors="searchErrors[field.param]"
                            :step="field.step ? field.step : 'any'"
                            :min-value="searchParams[`${field.param}_min`]"
                            v-on:start-input="searchParams[`${field.param}_min`] = $event"
                            :max-value="searchParams[`${field.param}_max`]"
                            v-on:end-input="searchParams[`${field.param}_max`] = $event"/>
                          <search-form-range
                            v-if="field.type === 'dateRange'"
                            type="date"
                            label-cols="5"
                            :id="`${field.id}Filter`"
                            :label="field.label"
                            placeholder="YYYY/MM/DD"
                            :errors="searchErrors[field.param]"
                            :min-value="searchParams[`${field.param}_after`]"
                            v-on:start-input="searchParams[`${field.param}_after`] = $event"
                            :max-value="searchParams[`${field.param}_before`]"
                            v-on:end-input="searchParams[`${field.param}_before`] = $event"/>
                          <search-form-select
                            v-if="field.type === 'select'"
                            label-cols="6"
                            :id="`${field.id}Filter`"
                            :label="field.label"
                            placeholder="----------"
                            :errors="searchErrors[field.param]"
                            v-model="searchParams[field.param]"
                            :options="filterSelectOptions[field.id]"
                            :value-field="field.valueField"
                            :text-field="field.textField" />
                          <search-form-input
                            v-if="field.type === 'number' || field.type === 'text'"
                            :type="field.type"
                            label-cols="6"
                            :id="`${field.id}Filter`"
                            :label="field.label"
                            :errors="searchErrors[field.param]"
                            v-model="searchParams[field.param]"/>
                        </b-col>
                        <b-col cols="1">
                          <b-button-close @click="removeSelectedFilter(field.id)" style="padding-top: calc(.375rem + 1px)">&times;</b-button-close>
                        </b-col>
                      </b-row>
                    </template>
                    <b-container class="pl-0">
                      <b-row>
                        <b-col cols="9">
                          <b-form-select id="additionalFilterInput" v-model="selectedFilter">
                            <option :value="null">Select a field to search on</option>
                            <template v-for="section in additionalFilters">
                              <optgroup v-if="section.authenticated ? userRoles.wells.view : true" :key="section.header" :label="section.header">
                                <template v-for="field in section.fields">
                                  <option v-if="field.authenticated ? userRoles.wells.view : true" :key="field.id" :value="field" :disabled="selectedFilterIds.includes(field.id)">{{ field.label }}</option>
                                </template>
                              </optgroup>
                            </template>
                          </b-form-select>
                        </b-col>
                        <b-col class="pr-0">
                          <b-button block variant="primary" @click="selectFilter" :disabled="selectedFilter === null">Add Field</b-button>
                        </b-col>
                      </b-row>
                    </b-container>
                  </b-card-body>
                </b-collapse>
              </b-card>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <well-exports/>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <p>For additional search options, try:</p>
              <ul>
                  <li><a href="http://maps.gov.bc.ca/ess/hm/wrbc/" id="BCWRAtlas">B.C. Water Resource Atlas</a></li>
                  <li><a href="http://maps.gov.bc.ca/ess/hm/imap4m/" id="iMapBC">iMapBC</a></li>
              </ul>
            </b-col>
          </b-row>
        </b-form>
      </b-col>
      <b-col>
        <search-map
            :latitude="latitude"
            :longitude="longitude"
            :locations="locations"
            v-on:coordinate="handleMapCoordinate"
            ref="searchMap"
            @moved="locationSearch"
            />
      </b-col>
    </b-row>
    <b-row class="my-5">
      <b-col>
        <div ref="tabulator"></div>
        <b-pagination class="mt-3" :disabled="isBusy" size="md" :total-rows="numberOfRecords" v-model="currentPage" :per-page="perPage" @input="wellSearch()">
        </b-pagination>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <p>
          Can’t find the well you are looking for? Try your search again using a different set of criteria. If you still need more assistance, Contact <a href="https://portal.nrs.gov.bc.ca/web/client/contact">FrontCounterBC</a>.
        </p>
        <p>
          <a href="http://www.frontcounterbc.gov.bc.ca/Start/surface-water/" onclick="handleOutboundLinkClicks('www.frontcounterbc.gov.bc.ca/Start/surface-water/')">
              Learn about and submit water license applications
          </a>  with FrontCounterBC.
        </p>
      </b-col>
    </b-row>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import {FETCH_CODES} from '@/submissions/store/actions.types.js'
import {FETCH_DRILLER_NAMES, FETCH_ORGANIZATION_NAMES} from '@/wells/store/actions.types.js'
import SearchFormInput from '@/wells/components/SearchFormInput.vue'
import SearchFormRadio from '@/wells/components/SearchFormRadio.vue'
import SearchFormRange from '@/wells/components/SearchFormRange.vue'
import SearchFormSelect from '@/wells/components/SearchFormSelect.vue'
import SearchMap from '@/wells/components/SearchMap.vue'
import Exports from '@/wells/components/Exports.vue'
import searchFields from '@/wells/searchFields.js'

const Tabulator = require('tabulator-tables')

export default {
  name: 'WellSearch',
  components: {
    'search-form-input': SearchFormInput,
    'search-form-radio': SearchFormRadio,
    'search-form-range': SearchFormRange,
    'search-form-select': SearchFormSelect,
    'search-map': SearchMap,
    'well-exports': Exports
  },
  data () {
    return {
      isBusy: false,
      isInitialSearch: true,
      showAdvancedSearch: false,
      currentPage: 1,
      perPage: 10,
      numberOfRecords: 0,
      latitude: null,
      longitude: null,
      locations: [],

      showAdvancedSearch: false,
      selectedFilter: null,
      selectedFilters: [],

      // testing tabulator
      tabulator: null,
      tableData: [],

      // searchParams will be set by searchParamsReset()
      searchParams: {},
      searchErrors: {},

      // additional location search params
      mapSearchParams: {},
      defaultFilters: searchFields.default,
      additionalFilters: searchFields.optional
    }
  },
  computed: {
    ...mapGetters(['codes', 'drillerNames', 'organizationNames', 'userRoles']),
    selectedFilterIds: function () {
      return this.selectedFilters.map(filter => filter.id)
    },
    additionalFilterFields: function () {
      return this.additionalFilters.map(section => section.fields).reduce((a, b) => a.concat(b), [])
    },
    landDistrictOptions: function () {
      if (!this.codes.land_district_codes || Object.entries(this.codes.land_district_codes).length === 0) {
        return []
      }
      return this.codes.land_district_codes.map((district) => {
        return {
          value: district.land_district_code,
          text: `${district.land_district_code} - ${district.name}`
        }
      })
    },
    wellSubclassOptions: function () {
      if (!this.codes.well_classes) {
        return []
      }
      const options = []
      this.codes.well_classes.forEach((wellClass) => {
        wellClass.wellsubclasscode_set.forEach((wellSubclass) => {
          options.push({
            value: wellSubclass.well_subclass_guid,
            text: `${wellClass.description} - ${wellSubclass.description}`
          })
        })
      })

      return options
    },
    filterSelectOptions: function () {
      return {
        coordinateAcquisitionCode: this.codes.coordinate_acquisition_codes,
        developmentMethods: this.codes.development_methods,
        drillingMethods: this.codes.drilling_methods,
        filterPackMaterial: this.codes.filter_pack_material,
        filterPackMaterialSize: this.codes.filter_pack_material_size,
        groundElevationMethod: this.codes.ground_elevation_methods,
        intendedWaterUse: this.codes.intended_water_uses,
        landDistrict: this.landDistrictOptions,
        licencedStatus: this.codes.licenced_status_codes,
        linerMaterial: this.codes.liner_material_codes,
        orgResponsible: this.organizationNames,
        ownerProvince: this.codes.province_codes,
        personResponsible: this.drillerNames,
        publicationStatus: this.codes.well_publication_status_codes,
        screenIntakeMethod: this.codes.screen_intake_methods,
        screenBottoms: this.codes.screen_bottoms,
        screenMaterial: this.codes.screen_materials,
        screenOpenings: this.codes.screen_openings,
        screenType: this.codes.screen_types,
        surfaceSealMaterial: this.codes.surface_seal_materials,
        surfaceSealMethod: this.codes.surface_seal_methods,
        waterQualityCharacteristics: this.codes.water_quality_characteristics,
        waterQualityColour: this.codes.water_quality_colours,
        wellClass: this.codes.well_classes,
        wellStatus: this.codes.well_status_codes,
        wellSubclass: this.wellSubclassOptions,
        yieldEstimationMethod: this.codes.yield_estimation_methods
      }
    }
  },
  methods: {
    /**
    * wellSearch searches for wells based on parameters in the querystring
    */
    wellSearch (ctx = { perPage: this.perPage, currentPage: this.currentPage }) {
      const params = {
        limit: ctx.perPage,
        offset: ctx.perPage * (ctx.currentPage - 1)
      }

      // add other search parameters into the params object.
      // these will be urlencoded and the API will filter on these values.
      Object.assign(params, this.searchParams)
      return ApiService.query('wells', params).then((response) => {
        this.searchErrors = {}
        this.numberOfRecords = response.data.count
        this.tableData = response.data.results
        this.tabulator.clearData()
        this.tabulator.replaceData(this.tableData)

        // the first search that happens when page loads doesn't need
        // to automatically scroll the page.  Only scroll when updating
        // the search results.
        if (!this.isInitialSearch) {
          this.$SmoothScroll(this.$el.querySelector('#map'))
        }
        // flag that the initial search that happens on page load
        // has already occurred.
        this.isInitialSearch = false

        return response.data.results || []
      }).catch((err) => {
        if (err.response && err.response.data) {
          this.searchErrors = err.response.data
        }

        return []
      })
    },
    locationSearch () {
      let params = Object.assign({}, this.searchParams)
      if (this.$refs.searchMap && this.$refs.searchMap.map) {
        const bounds = this.$refs.searchMap.map.getBounds()
        const sw = bounds.getSouthWest()
        const ne = bounds.getNorthEast()
        const boundBox = {

          sw_lat: sw.lat,
          sw_long: sw.lng,
          ne_lat: ne.lat,
          ne_long: ne.lng

        }
        params = Object.assign(params, boundBox)
      }
      ApiService.query('wells/locations', params).then((response) => {
        this.locations = response.data.map((well) => {
          return [well.latitude, well.longitude, well.well_tag_number, well.identification_plate_number]
        })
      })
    },
    handleSearchSubmit () {
      this.updateQueryParams()
      this.wellSearch()
      this.locationSearch()
    },
    resetButtonHandler () {
      this.searchParamsReset()
      this.wellSearch()
      this.locationSearch()
    },
    searchParamsReset () {
      this.searchParams = {match_any: 'true'}
      this.selectedFilters = []
      this.$router.push({ query: null })
    },
    initSearchParams () {
      const query = this.$route.query
      // check if the page loads with a query (e.g. user bookmarked a search)
      // if so, set the search boxes to the query params
      if (Object.entries(query).length !== 0 && query.constructor === Object) {
        this.searchParams = Object.assign({}, query)
      } else {
        this.searchParamsReset()
      }
    },
    initSelectedFilters () {
      const query = this.$route.query
      this.additionalFilterFields.filter((field) => {
        return (query[field.param] !== undefined) ||
          (field.minParam && query[field.minParam] !== undefined) ||
          (field.maxParam && query[field.maxParam] !== undefined)
      }).forEach(field => this.selectedFilters.push(field))
    },
    handleMapCoordinate (latln) {
      this.latitude = null
      this.longitude = null
      setTimeout(() => {
        this.latitude = latln.lat
        this.longitude = latln.lng
      }, 0)
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
    tableLinkParams (cell) {
      return {
        url: `/gwells/well/${cell.getValue()}/`
      }
    },
    updateQueryParams () {
      const params = Object.assign({}, this.searchParams)

      // check if every key on the params object is empty.
      // evaluations to boolean
      const paramsEmpty = Object.keys(params).every((x) => {
        return params[x] === '' || params[x] === null
      })

      // if params are completely empty, clear the query string,
      // otherwise add the params to the query string.  this allows
      // users to bookmark searches.
      this.$router.push({ query: paramsEmpty ? null : this.searchParams })
    },
    toggleAdvancedSearch () {
      this.showAdvancedSearch = !this.showAdvancedSearch
    },
    selectFilter () {
      if (this.selectedFilter) {
        this.selectedFilters.push(this.selectedFilter)
      }

      this.selectedFilter = null
    },
    removeSelectedFilter (filterId) {
      const index = this.selectedFilters.findIndex(filter => filterId === filter.id)
      this.selectedFilters.splice(index, 1)
    }
  },
  created () {
    this.$store.dispatch(FETCH_CODES)
    this.$store.dispatch(FETCH_DRILLER_NAMES)
    this.$store.dispatch(FETCH_ORGANIZATION_NAMES)

    this.initSearchParams()
    this.initSelectedFilters()
    setTimeout(() => {
      this.locationSearch()
    }, 0)
    this.wellSearch()
  },
  mounted () {
    this.tabulator = new Tabulator(this.$refs.tabulator, {
      data: this.tableData,
      height: '36rem',
      columns: [
        { title: 'Well Tag', field: 'well_tag_number', formatter: 'link', formatterParams: (cell) => ({ url: `/gwells/well/${cell.getValue()}` }) },
        { title: 'ID Plate', field: 'identification_plate_number' },
        { title: 'Owner Name', field: 'owner_full_name' },
        { title: 'Street Address', field: 'street_address' },
        { title: 'Legal Lot', field: 'legal_lot' },
        { title: 'Legal Plan', field: 'legal_plan' },
        { title: 'Legal District Lot', field: 'legal_district_lot' },
        { title: 'Land District', field: 'land_district' },
        { title: 'Legal PID', field: 'legal_pid' },
        { title: 'Diameter', field: 'diameter' },
        { title: 'Finished Well Depth', field: 'finished_well_depth' }
      ]
    })
  }
}
</script>

<style>
</style>
