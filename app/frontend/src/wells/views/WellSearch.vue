<template>
  <b-card class="container container-wide p-1">
    <h1 class="card-title">Well Search</h1>
    <p>
      Not all groundwater wells are registered with the province, as registration was voluntary until February 29, 2016. Data quality issues may impact search results.
    </p>
    <p>
      Search by one of the fields below, or zoom to a location on the map and select the "Search Wells in this Area" button.
    </p>
    <b-row class="mt-5">
      <b-col cols="12" lg="6">
        <b-form @submit.prevent="$root.$emit('bv::refresh::table', 'wellSearchTable')" @reset.prevent="resetButtonHandler">
          <b-row>
            <b-col>
              <form-input
                id="wellTagSearchBox"
                group-class="font-weight-bold"
                label="Well Tag Number or Well Identification Plate Number"
                v-model="searchParams.well_tag_number"
              ></form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="streetAddressSearchBox"
                group-class="font-weight-bold"
                label="Street Address"
              ></form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <form-input
                id="lotNumberSearchBox"
                group-class="font-weight-bold"
                label="Legal Plan or Lot Number"
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
      <b-col cols="12" lg="6">
        This is a map.
      </b-col>
    </b-row>
    <b-row class="my-5">
      <b-col>
        <b-table
          show-empty
          ref="wellSearchTable"
          id="wellSearchTable"
          :busy.sync="isBusy"
          :fields="['well_tag_number', 'identification_plate_number', 'owner_full_name', 'street_address', 'lot', 'plan', 'district_lot', 'land_district', 'PID', 'diameter', 'finished_well_depth']"
          :items="wellSearch"
          :per-page="perPage"
          :current-page="currentPage"
        >
          <template slot="well_tag_number" slot-scope="data">
            <router-link :to="{ name: 'wells-detail', params: { id: data.item.well_tag_number} }">{{ data.item.well_tag_number }}</router-link>
          </template>
        </b-table>
        <b-pagination :disabled="isBusy" size="md" :total-rows="numberOfRecords" v-model="currentPage" :per-page="perPage">
    </b-pagination>
      </b-col>
    </b-row>
  </b-card>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'WellSearch',
  data () {
    return {
      isBusy: false,
      currentPage: 1,
      perPage: 10,
      numberOfRecords: 0,

      // searchParams will be set by searchParamsReset()
      searchParams: {}
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
        return response.data.results || []
      }).catch((e) => {
        return []
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
    }
  },
  created () {
    this.searchParamsReset()
  }
}
</script>

<style>

</style>
