<template>
  <div>
    <b-card v-if="userIsAdmin" no-body class="container p-1 mb-3">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-btn block href="#" v-b-toggle.adminPanel variant="light" class="text-left">Administrator options</b-btn>
      </b-card-header>
      <b-collapse id="adminPanel">
        <b-card-body class="pb-1">
          <b-button
            class="mb-2"
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
            :to="{ name: 'OrganizationAdd' }"
          >
            Manage companies
          </b-button>
        </b-card-body>
      </b-collapse>
    </b-card>
    <b-card class="container p-1" title="Register of Well Drillers and Well Pump Installers">
      To update contact information or for general enquiries email <a href="mailto:Groundwater@gov.bc.ca">groundwater@gov.bc.ca</a>.
      <p class="mt-1">
        <a href="https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/groundwater-wells/information-for-well-drillers-well-pump-installers/what-you-need-to-practice-in-bc">
        Learn more about registering as a well driller or well pump installer in B.C.
        </a>
      </p>
      <b-card no-body class="p-3 mb-4">
        <h5>Search for a Well Driller or Well Pump Installer</h5>
        <b-form @submit.prevent="drillerSearch" @reset.prevent="drillerSearchReset({clearDrillers: true})" id="drillerSearchForm">
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
            <b-col cols="12" md="6" class="pr-md-5">
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
            <b-col cols="12" md="6" v-if="userIsAdmin">
              <b-form-group label="Registration status" label-for="registrationStatusSelect">
                <b-form-select
                    v-model="searchParams.status"
                    id="registrationStatusSelect"
                    name="registryStatuses">
                  <option value="">All</option>
                  <option value="PENDING">Pending</option>
                  <option value="INACTIVE">Not registered</option>
                  <option value="ACTIVE">Registered</option>
                  <option value="REMOVED">Removed</option>
                </b-form-select>
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
            <b-col>
              <b-form-group>
                  <button
                    type="submit"
                    class="btn btn-primary registries-search-btn mr-md-1"
                    id="personSearchSubmit"
                    :disabled="searchLoading">
                    <span>Search</span>
                  </button>
                  <button type="reset" class="btn btn-default" id="personSearchReset">Reset</button>
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-form>
      </b-card>
      <div ref="registryTableResults">
        <template v-if="!searchLoading">
          <b-row>
            <b-col cols="12" v-if="drillers.results && !drillers.results.length">
              No results were found.
            </b-col>
            <b-col cols="12" v-if="listError">
              <api-error :error="listError" resetter="SET_LIST_ERROR"></api-error>
            </b-col>
          </b-row>
          <b-row v-if="drillers.results && drillers.results.length">
            <div class="col-xs-12 col-sm-4">
              <h3>{{ activityTitle }} Results</h3>
            </div>
            <b-col cols="12">
              To update contact information email <a href="mailto:Groundwater@gov.bc.ca">groundwater@gov.bc.ca</a>.
            </b-col>
            <b-col cols="12" class="mt-2">
              <registry-table @sort="sortTable" :activity="lastSearchedActivity"/>
            </b-col>
          </b-row>
          <b-row v-if="drillers.results && drillers.results.length" class="mt-5">
            <b-col cols="12">
              <register-legal-text class="register-legal" :activity="lastSearchedActivity"/>
            </b-col>
          </b-row>
        </template>
      </div>
    </b-card>
  </div>
</template>

<script>
import SearchTable from '@/registry/components/search/SearchTable.vue'
import LegalText from '@/registry/components/Legal.vue'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import { mapGetters } from 'vuex'
import { FETCH_CITY_LIST, FETCH_DRILLER_LIST } from '@/registry/store/actions.types'
import { SET_DRILLER_LIST } from '@/registry/store/mutations.types'

export default {
  components: {
    'registry-table': SearchTable,
    'api-error': APIErrorMessage,
    'register-legal-text': LegalText
  },
  data () {
    return {
      adminPanelToggle: false,
      loginPanelToggle: false,
      lastSearchedActivity: 'DRILL',
      regStatusOptions: [
        { value: '', text: 'All', public: false },
        { value: 'PENDING', text: 'Pending', public: false },
        { value: 'INACTIVE', text: 'Not registered', public: true },
        { value: 'ACTIVE', text: 'Registered', public: true },
        { value: 'REMOVED', text: 'Removed', public: false }
      ],
      credentials: {
        username: null,
        password: null
      },
      searchParams: {
        search: '',
        city: [''],
        activity: 'DRILL',
        status: 'ACTIVE',
        limit: '10',
        ordering: ''
      },
      searchLoading: false,
      lastSearchedParams: {}
    }
  },
  computed: {
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
      if (activityMap[this.lastSearchedActivity]) {
        return activityMap[this.lastSearchedActivity]
      }
      return ''
    },
    APISearchParams () {
      // bundles searchParams into fields compatible with API
      return {
        search: this.searchParams.search,
        // prov: this.searchParams.city.split(',')[1],
        city: this.searchParams.city.join(),
        status: this.searchParams.status,
        limit: this.searchParams.limit,
        activity: this.searchParams.activity,
        ordering: this.searchParams.ordering
      }
    },
    ...mapGetters([
      'userIsAdmin',
      'loading',
      'listError',
      'cityList',
      'drillers'
    ])
  },
  watch: {
    'searchParams.activity': function () {
      // get new city list when user changes activity (well driller or well pump installer)
      this.searchParams.city = ['']
      this.$store.dispatch(FETCH_CITY_LIST, this.formatActivityForCityList)
    },
    user: function () {
      // reset search when user changes (this happens every login or logout)
      this.drillerSearchReset()
    }
  },
  methods: {
    drillerSearch () {
      const table = this.$refs.registryTableResults
      const params = this.APISearchParams
      this.lastSearchedActivity = this.searchParams.activity || 'DRILL'
      this.searchLoading = true
      this.$store.dispatch(FETCH_DRILLER_LIST, params).then(() => {
        this.$SmoothScroll(table, 100)
        this.drillerSearchReset({keepActivity: true, keepLimit: true})
        this.searchLoading = false
        this.lastSearchedParams = Object.assign({}, params)
      }).catch(() => {
        this.searchLoading = false
      })
    },
    drillerSearchReset (options = {}) {
      this.searchParams.search = ''
      this.searchParams.city = ['']
      this.searchParams.status = 'ACTIVE'
      this.searchParams.ordering = ''
      if (options.clearDrillers) {
        this.$store.commit(SET_DRILLER_LIST, [])
      }
      if (!options.keepActivity) {
        this.searchParams.activity = 'DRILL'
      }
      if (!options.keepLimit) {
        this.searchParams.limit = '10'
      }
    },
    sortTable (sortCode) {
      if (this.lastSearchedParams.ordering[0] !== '-') {
        this.lastSearchedParams['ordering'] = `-${sortCode}`
      } else {
        this.lastSearchedParams['ordering'] = `${sortCode}`
      }
      this.$store.dispatch(FETCH_DRILLER_LIST, this.lastSearchedParams)
    }
  },
  created () {
    // send request for city list when app is loaded
    this.$store.dispatch(FETCH_CITY_LIST, this.formatActivityForCityList)
  }
}
</script>

<style>
.registries-search-btn {
  min-width: 70px;
}
</style>
