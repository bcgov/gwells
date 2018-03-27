<template>
  <div class="container-fluid no-pad">
    <div class="row form-spacing no-pad">
      <div class="col-xs-12 col-sm-7">
          <p><a href="https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/groundwater-wells/information-for-well-drillers-well-pump-installers/what-you-need-to-practice-in-bc">Learn more about registering as a well driller or well pump installer in B.C.</a></p>
      </div>
      <div class="col-xs-12 col-sm-5 text-right">
        <button v-if="!user" type="button" class="btn btn-primary" @click="loginPanelToggle = !loginPanelToggle">Log in</button>
        <button v-if="user" type="button" class="btn btn-secondary" @click="logout" id="logoutButton">Log out</button>
      </div>
    </div>
    <div class="row no-pad" v-if="!user && loginPanelToggle">
      <div class="col-xs-12">
        <div class="well well-sm">
          <div class="container">
            <form @submit.prevent="login" id="registryLoginForm">
              <div class="form-group">
                <div class="col-xs-12 col-sm-2">
                  <label for="loginUser">Username</label>
                  <input type="text" class="form-control" id="loginUser" placeholder="Search" v-model="credentials.username">
                </div>
                <div class="col-xs-12 col-sm-2">
                  <label for="loginPassword">Password</label>
                  <input type="password" class="form-control" id="loginPassword" placeholder="Password" v-model="credentials.password">
                </div>
              </div>
              <div class="form-group">
                <div class="col-xs-12">
                  <button id="loginButton" type="submit" class="btn btn-primary">Login</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="row no-pad" v-if="user">
      <div class="col-xs-12">
          <div class="well well-sm">
            <div v-if="user">
              <div>Logged in as {{ user.username }}</div>
              <div>
                <button type="button" class="btn btn-primary" id="addNewEntryButton">Add new entry</button>
                <button type="button" class="btn btn-primary" id="manageCompaniesButton">Manage companies</button>
              </div>
            </div>
          </div>
      </div>
    </div>
    <div class="row no-pad">
      <div class="col-xs-12">
        <div class="panel no-pad">
          <div class="panel-body no-pad">
            <h3 class="registry-panel-title">Search for a Well Driller or Well Installer</h3>
            <form @submit.prevent="drillerSearch" @reset.prevent="drillerSearchReset" id="drillerSearchForm">
              <div class="row no-pad">
                <div class="col-xs-12">
                  <div class="form-group">
                    <div class="col-xs-12">
                      <label>Choose professional type: &nbsp;</label>
                    </div>
                    <div class="col-xs-12 form-spacing">
                      <label class="radio-inline">
                        <input type="radio" name="activitySelector" id="activityDriller" v-model="searchParams.activity" value="DRILL" style="margin-top: 0px"> Well Driller
                      </label>
                      <label class="radio-inline">
                        <input type="radio" name="activitySelector" id="activityInstaller" v-model="searchParams.activity" value="PUMP" style="margin-top: 0px"> Pump Installer
                      </label>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row no-pad">
                <div class="col-xs-12">
                  <div class="form-group">
                    <div class="col-xs-12 col-sm-6 form-spacing">
                      <label for="cityOptions">Community</label>
                      <div>To search more than one community, hold down the Ctrl key and select.</div>
                      <select id="cityOptions" class="form-control" v-model="searchParams.city" multiple="multiple" style="min-height: 5.8rem">
                        <option value="">All</option>
                        <optgroup
                          v-for="prov in cityList[formatActivityForCityList]"
                          v-if="prov.cities && prov.cities.length"
                          :key="prov.prov"
                          :label="`${prov.prov} (${prov.cities.length})`"
                        >
                          <option v-for="city in prov.cities" :key="`${city} ${prov.prov}`" :value="city">{{ city }}</option>
                        </optgroup>
                        <!-- <option v-for="city in cityList[formatActivityForCityList]" :key="city.city + city.province" :value="city.city">{{city.city}}</option> -->
                      </select>
                    </div>
                  </div>
                  <div class="form-group" v-if="user">
                    <div class="col-xs-12 col-sm-6 form-spacing">
                      <label for="registrationStatusSelect">Registration status</label>
                      <select v-model="searchParams.status" class="form-control" id="registrationStatusSelect">
                        <option value="">All</option>
                        <option value="PENDING">Pending</option>
                        <option value="INACTIVE">Not registered</option>
                        <option value="ACTIVE">Registered</option>
                        <option value="REMOVED">Removed</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row no-pad">
                <div class="col-xs-12">
                  <div class="form-group">
                    <div class="col-xs-12 col-sm-6 form-spacing">
                      <label for="regTypeInput">Individual, company, or registration number</label>
                      <input type="text" class="form-control" id="regTypeInput" placeholder="Search" v-model="searchParams.search">
                    </div>
                  </div>
                </div>
              </div>
              <div class="row no-pad">
                <div class="col-xs-12">
                  <div class="form-group">
                    <div class="col-xs-6 col-sm-2 form-spacing">
                      <label for="registriesResultsNumberSelect">Entries</label>
                      <select class="form-control input-sm" v-model="searchParams.limit" id="registriesResultsNumberSelect"><option>10</option><option>25</option></select>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row no-pad">
                <div class="col-xs-12">
                  <div class="form-group">
                    <div class="col-xs-12">
                      <button type="submit" class="btn btn-primary" id="personSearchSubmit">Submit</button>
                      <button type="reset" class="btn btn-secondary" id="personSearchReset">Reset</button>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="row no-pad">
      <div class="col-xs-12 col-sm-4">
        <h3>{{ activityTitle }} Results</h3>
      </div>
      <div v-if="listError" class="col-xs-12 col-sm-7">
        <api-error :error="listError" resetter="setListError"></api-error>
      </div>
      <div class="col-xs-12">
        <register-table @sort="sortTable" :activity="lastSearchedActivity"/>
      </div>
    </div>
    <div class="row no-pad" v-if="drillers.results && drillers.results.length">
      <div class="col-xs-12">
        <register-legal-text class="register-legal" :activity="lastSearchedActivity"/>
      </div>
    </div>
  </div>
</template>

<script>
import RegisterTable from '@/registry/components/RegisterTable'
import LegalText from '@/registry/components/Legal'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { mapGetters } from 'vuex'
import { LOGIN, LOGOUT, FETCH_CITY_LIST, FETCH_DRILLER_LIST } from '@/registry/store/actions.types'
import { SET_DRILLER_LIST } from '@/registry/store/mutations.types'

export default {
  components: {
    'register-table': RegisterTable,
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
        city: [],
        activity: 'DRILL',
        status: 'ACTIVE',
        limit: '10',
        ordering: ''
      }
    }
  },
  computed: {
    cities () {
      const list = []
      list.push({
        value: null,
        text: 'Select a city'
      })
      return list
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
        PUMP: 'Pump Installer'
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
      'user',
      'loading',
      'listError',
      'cityList',
      'drillers'
    ])
  },
  watch: {
    'searchParams.activity': function () {
      this.searchParams.city = []
      this.$store.dispatch(FETCH_CITY_LIST, this.formatActivityForCityList)
    },
    user: function () {
      this.drillerSearchReset()
    }
  },
  methods: {
    drillerSearch () {
      const params = this.APISearchParams
      this.lastSearchedActivity = this.searchParams.activity || 'DRILL'
      this.$store.dispatch(FETCH_DRILLER_LIST, params)
    },
    drillerSearchReset () {
      this.searchParams.search = ''
      this.searchParams.city = []
      this.searchParams.activity = 'DRILL'
      this.searchParams.status = 'ACTIVE'
      this.searchParams.limit = '10'
      this.searchParams.ordering = ''
      this.$store.commit(SET_DRILLER_LIST, [])
    },
    sortTable (sortCode) {
      if (this.searchParams.ordering && this.searchParams.ordering.length && this.searchParams.ordering[0] !== '-') {
        this.searchParams['ordering'] = `-${sortCode}`
      } else {
        this.searchParams['ordering'] = `${sortCode}`
      }
      this.$store.dispatch(FETCH_DRILLER_LIST, this.APISearchParams)
    },
    login () {
      this.$store.dispatch(LOGIN, this.credentials)
      this.loginPanelToggle = false
    },
    logout () {
      this.$store.dispatch(LOGOUT)
    }
  },
  created () {
    this.$store.dispatch(FETCH_CITY_LIST, this.formatActivityForCityList)
    // if (!this.drillers || !this.drillers.results || !this.drillers.results.length) {
    //   this.drillerSearch()
    // }
  }
}
</script>

<style>
.row.no-pad {
  margin-right:0;
  margin-left:0;
}
.row.no-pad > [class*='col-'] {
  padding-right:0;
  padding-left:0;
}
.panel.no-pad {
  margin-right:0;
  margin-left:0;
  padding-right:0;
  padding-left:0;
  margin-top:0;
  padding-top:0;
}
.panel.no-pad > .panel-body {
  margin-right:0;
  margin-left:0;
  padding-right:0;
  padding-left:0;
  margin-top:0;
  padding-top:0;
}
.container-fluid.no-pad {
  margin-right:0;
  margin-left:0;
  padding-right:0;
  padding-left:0;
}
.registry-panel-title {
  margin-left: 10px;
  margin-top: 0px;
  padding-top:0px;
}
.btn {
  margin-top: 5px;
}
.form-spacing {
  margin-bottom: 15px;
}
.registry-disabled-item {
  color: #808080;
  cursor: auto!important;
}
.register-legal {
  margin-top: 25px;
}
</style>
