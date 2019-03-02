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
                <form-input
                  id="id_search"
                  group-class="font-weight-bold"
                  v-model="searchParams.search"
                >
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
                  <b-button variant="link" @click="toggleAdvancedSearch">Advanced Search</b-button>
                </b-card-header>
                <b-collapse id="advanced_search_form" v-model="showAdvancedSearch">
                  <b-card-body body-border-variant="dark">
                    <h3>Search By</h3>
                    <!-- Any/all needs some work -->
                    <form-input id="search-well-tag-or-id-plate" label="Well tag or ID plate number" label-cols="6" v-model="searchParams.well"/>
                    <form-input id="search-street-address-or-city" label="Street address or city" label-cols="6" v-model="searchParams.street_address_or_city"/>
                    <form-input id="search-well-owner-name" label="Well owner" label-cols="6" v-model="searchParams.owner_full_name"/>
                    <h3>Location</h3>
                    <form-input id="search-legal-input" label="Lot, Legal plan, District lot or PID" label-cols="6" v-model="searchParams.legal"/>
                    <form-input select id="search-land-district" label="Land district" label-cols="6" v-model="searchParams.land_district" :options="landDistrictOptions"/>
                    <h3>Well Details</h3>
                    <form-input select id="search-well-status" label="Well status" label-cols="6" v-model="searchParams.well_status" :options="wellStatusOptions"/>
                    <form-input select id="search-licenced-status" label="Well licence status" label-cols="6" v-model="searchParams.licenced_status" :options="licencedStatusOptions"/>
                    <form-input select id="search-person-responsible" label="Person responsible for work" label-cols="6" v-model="searchParams.person_responsible" :options="personResponsibleOptions"/>
                    <form-input select id="search-organization-of-person-responsible" label="Company that did the work" label-cols="6" v-model="searchParams.company_of_person_responsible" :options="orgOfPersonResponsibleOptions"/>
                    <b-form-group label-cols="4" label="Date of work">
                      <b-form-group label-cols="3" label="From" label-for="search-date-of-work-before" label-align="right">
                        <b-form-input type="date" placeholder="YYYY/MM/DD" id="search-date-of-work-before" v-model="searchParams.date_of_work_before" />
                      </b-form-group>
                      <b-form-group label-cols="3" label="To" label-for="search-date-of-work-after" label-align="right">
                        <b-form-input type="date" placeholder="YYYY/MM/DD" id="search-date-of-work-after" v-model="searchParams.date_of_work_after" />
                      </b-form-group>
                    </b-form-group>
                    <b-form-group label-cols="4" label="Well depth (finished or total)">
                      <b-form-group label-cols="3" label="From" label-for="search-well-depth-min" label-align="right">
                        <b-form-input type="number" id="search-well-depth-min" v-model="searchParams.well_depth_min" />
                      </b-form-group>
                      <b-form-group label-cols="3" label="To" label-for="search-well-depth-max" label-align="right">
                        <b-form-input type="number" id="search-well-depth-max" v-model="searchParams.well_depth_max" />
                      </b-form-group>
                    </b-form-group>
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
import SearchMap from '@/wells/components/SearchMap.vue'
import Exports from '@/wells/components/Exports.vue'

const Tabulator = require('tabulator-tables')

export default {
  name: 'WellSearch',
  components: {
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

      // testing tabulator
      tabulator: null,
      tableData: [],

      // searchParams will be set by searchParamsReset()
      searchParams: {},

      // additional location search params
      mapSearchParams: {}
    }
  },
  computed: {
    ...mapGetters(['codes', 'drillerNames', 'organizationNames']),
    personResponsibleOptions: function () {
      if (!this.drillerNames) {
        return []
      }

      return this.drillerNames.map((driller) => {
        return {
          value: driller.person_guid,
          text: driller.name
        }
      })
    },
    orgOfpersonResponsibleOptions: function () {
      if (!this.organizationNames) {
        return []
      }

      return this.organizationNames.map((org) => {
        return {
          value: org.org_guid,
          text: org.name
        }
      })
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
    licencedStatusOptions: function () {
      if (!this.codes.licenced_status_codes) {
        return []
      }
      return this.codes.licenced_status_codes.map((status) => {
        return {
          value: status.licenced_status_code,
          text: status.description
        }
      })
    },
    wellStatusOptions: function () {
      if (!this.codes.well_status_codes) {
        return []
      }
      return this.codes.well_status_codes.map((status) => {
        return {
          value: status.well_status_code,
          text: status.description
        }
      })
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
      }).catch((e) => {
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
      this.searchParams = {}
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
    }
  },
  created () {
    this.$store.dispatch(FETCH_CODES)
    this.$store.dispatch(FETCH_DRILLER_NAMES)
    this.$store.dispatch(FETCH_ORGANIZATION_NAMES)

    this.initSearchParams()
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
