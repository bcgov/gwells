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
          <b-row>
            <b-col cols="8">

              <form-input
                id="id_well"
                group-class="font-weight-bold"
                v-model="searchParams.well"
              >
                <label>
                  Well Tag or Identification Plate Number
                  <b-badge pill variant="primary" v-b-popover.hover="'Well electronic filing number or physical identification plate number'"><i class="fa fa-question fa-lg"></i></b-badge>
                </label>
              </form-input>
              <b-form-group>

              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="id_addr"
                group-class="font-weight-bold"
                label="Street Address"
                v-model="searchParams.street_address"
              ></form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="id_legal"
                group-class="font-weight-bold"
                v-model="searchParams.search"
              >
              <label>
                  Legal Plan or District Lot or Parcel Identification Number (PID)
                  <b-badge pill variant="primary"
                    v-b-popover.hover="'Find the legal plan, district lot, or 9-digit PID \
                      (parcel identifier) on the \
                      property assessment, property tax notice, or real estate transaction.'"
                  ><i class="fa fa-question fa-lg"></i></b-badge>
              </label>
              </form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="id_owner"
                group-class="font-weight-bold"
                label="Owner Name"
                v-model="searchParams.owner_full_name"
              ></form-input>
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
import ApiService from '@/common/services/ApiService.js'
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
          return [well.latitude, well.longitude, well.well_tag_number]
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
      this.searchParams = {
        well: '',
        street_address: '',
        lot_search: '',
        owner_full_name: ''
      }
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
    }
  },
  created () {
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
