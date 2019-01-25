<template>
  <b-card class="container container-wide p-1">
    <h1 class="card-title">Groundwater Well Search</h1>

    <b-row class="mt-3">
      <b-col cols="12" lg="6" xl="5">
        <b-form @submit.prevent="wellSearch(); locationSearch()" @reset.prevent="resetButtonHandler(); locationSearch()">
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
            <b-col cols="6">
              <form-input
                id="wellTagSearchBox"
                group-class="font-weight-bold"
                label="Well Tag Number"
                v-model="searchParams.well_tag_number"
              ></form-input>
            </b-col>
            <b-col cols="6">
              <form-input
                id="wellPlateSearchBox"
                group-class="font-weight-bold"
                label="Well Identification Plate Number"
                v-model="searchParams.identification_plate_number"
              ></form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="streetAddressSearchBox"
                group-class="font-weight-bold"
                label="Street Address"
                v-model="searchParams.street_address"
              ></form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="lotNumberSearchBox"
                group-class="font-weight-bold"
                label="Legal Plan"
                v-model="searchParams.legal_plan"
              ></form-input>
            </b-col>
            <b-col>
              <form-input
                id="legalPlanSearchBox"
                group-class="font-weight-bold"
                v-model="searchParams.legal_lot"
                label="Lot Number"
              ></form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="ownerNameSearchBox"
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
    <!-- <b-row class="my-5">
      <b-col>
        <b-table
          show-empty
          ref="wellSearchTable"
          id="wellSearchTable"
          :busy.sync="isBusy"
          :fields="['well_tag_number', 'identification_plate_number', 'owner_full_name', 'street_address', 'legal_lot', 'legal_plan', 'legal_district_lot', 'land_district', 'legal_pid', 'diameter', 'finished_well_depth']"
          :items="wellSearch"
          :per-page="perPage"
          :current-page="currentPage"
        >
          <template slot="well_tag_number" slot-scope="data">
            <router-link :to="{ name: 'wells-detail', params: { id: data.item.well_tag_number} }">{{ data.item.well_tag_number }}</router-link>
          </template>
        </b-table>
      </b-col>
    </b-row> -->
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

const Tabulator = require('tabulator-tables')

export default {
  name: 'WellSearch',
  components: {
    'search-map': SearchMap
  },
  data () {
    return {
      isBusy: false,
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
    wellSearch (ctx = { perPage: this.perPage, currentPage: this.currentPage }) {
      /**
      * wellSearch() is a table items provider function
      * https://bootstrap-vue.js.org/docs/components/table/
      *
      * it takes a context/config object that contains properties that come
      * from the table attributes (e.g. perPage, currentPage), makes an API request
      * with query strings based on the context, and returns a promise.
      * The promise must always return an array.
      *
      * this function is handled by the table but a refresh can be triggered by
      * calling this.$root.$emit('bv::refresh::table', 'wellSearchTable')
      */

      const params = {
        limit: ctx.perPage,
        offset: ctx.perPage * (ctx.currentPage - 1)
      }

      // add other search parameters into the params object.
      // these will be urlencoded and the API will filter on these values.
      Object.assign(params, this.searchParams)

      return ApiService.query('wells/', params).then((response) => {
        this.numberOfRecords = response.data.count
        this.tableData = response.data.results
        this.tabulator.clearData()
        this.tabulator.replaceData(this.tableData)

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
        console.log('bounds', sw, ne)
        const boundBox = {

          sw_lat: sw.lat,
          sw_long: sw.lng,
          ne_lat: ne.lat,
          ne_long: ne.lng

        }
        params = Object.assign(params, boundBox)
      }
      ApiService.query('wells/locations/', params).then((response) => {
        this.locations = response.data.map((well) => {
          return [well.latitude, well.longitude, well.well_tag_number]
        })
      })
    },
    resetButtonHandler () {
      this.searchParamsReset()
      this.$root.$emit('bv::refresh::table', 'wellSearchTable')
    },
    searchParamsReset () {
      this.searchParams = {
        owner_full_name: '',
        well_tag_number: ''
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
    }
  },
  created () {
    this.searchParamsReset()
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
