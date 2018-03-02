<template>
  <div class="container-fluid">
      <div class="row form-spacing">
        <div class="col-xs-12 col-sm-8">
          <a id="main-content-anchor"></a>
          <h2 id="registry-title">Register of Well Drillers and Well Pump Installers</h2>
            <p><a href="#">Learn more about registering as a well driller or well pump installer in B.C.</a></p>
        </div>
        <div class="col-xs-12 col-sm-4 text-center">
          <button type="button" class="btn btn-primary" @click="adminPanelToggle=!adminPanelToggle">GWELLS Administrator options</button>
        </div>
      </div>
      <div class="row" v-if="adminPanelToggle">
        <div class="col-xs-12">
            <div class="well well-sm">
              <div v-if="!user">
                <button type="button" class="btn btn-primary" @click="login">Log in</button>
              </div>
              <div v-if="user">
                <div>Logged in as {{ user.username }}</div>
                <div>
                  <button type="button" class="btn btn-primary">Add new entry</button>
                  <button type="button" class="btn btn-primary">Manage companies</button>
                </div>
                <div><button type="button" class="btn btn-secondary" @click="logout">Log out</button></div>
              </div>
            </div>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12">
          <div class="panel">
            <div class="panel-body">
              <div class="container-fluid">
                <h3>Search for a Well Driller or Well Installer</h3>
                <form @submit.prevent="drillerSearch" @reset.prevent="drillerSearchReset">
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
                  <div class="row">
                    <div class="form-group">
                      <div class="col-xs-12 col-sm-6 form-spacing">
                        <label>Community</label>
                        <select class="form-control" v-model="searchParams.city">
                          <option value="">All</option>
                          <option v-for="city in cityList" :key="city.city + city.province" :value="city.city + ',' + city.province_state">{{city.city}}<span v-if="city.province_state">, {{city.province_state}}</span></option>
                        </select>
                      </div>
                    </div>
                    <div class="form-group">
                      <div class="col-xs-12 col-sm-6 form-spacing">
                        <label>Registration status</label>
                        <select v-model="searchParams.status" class="form-control">
                          <option value="" disabled>All</option>
                          <option value="PENDING" disabled>Pending</option>
                          <option value="INACTIVE" disabled>Not registered</option>
                          <option value="ACTIVE">Registered</option>
                          <option value="REMOVED" disabled>Removed</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="col-xs-12 col-sm-6 form-spacing">
                      <label for="regTypeInput">Individual, company, or registration number</label>
                      <input type="text" class="form-control" id="regTypeInput" placeholder="Search" v-model="searchParams.search">
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="col-xs-12 form-inline form-spacing">
                        <select class="form-control input-sm" v-model="searchParams.limit"><option>10</option><option>25</option></select> entries
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="col-xs-12">
                      <button type="submit" class="btn btn-primary">Submit</button>
                      <button type="reset" class="btn btn-secondary">Reset</button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4">
          <h3>Well Driller Results</h3>
        </div>
        <div v-if="listError" class="col-xs-12 col-sm-7">
          <api-error :error="listError" resetter="setListError"></api-error>
        </div>
        <div class="col-xs-12">
          <register-table/>
        </div>
      </div>
  </div>
</template>

<script>
import RegisterTable from '@/registry/components/RegisterTable'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { mapGetters } from 'vuex'
import { SET_USER } from '@/registry/store/mutations.types'
import { FETCH_CITY_LIST, FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

export default {
  components: {
    'register-table': RegisterTable,
    'api-error': APIErrorMessage
  },
  data () {
    return {
      adminPanelToggle: false,
      regStatusOptions: [
        { value: '', text: 'All', public: false },
        { value: 'PENDING', text: 'Pending', public: false },
        { value: 'INACTIVE', text: 'Not registered', public: true },
        { value: 'ACTIVE', text: 'Registered', public: true },
        { value: 'REMOVED', text: 'Removed', public: false }
      ],
      searchParams: {
        search: '',
        city: '',
        activity: 'DRILL',
        status: 'ACTIVE',
        limit: '10'
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
    ...mapGetters([
      'user',
      'loading',
      'listError',
      'cityList'
    ])
  },
  watch: {
    'searchParams.activity': function () {
      this.searchParams.city = ''
      this.$store.dispatch(FETCH_CITY_LIST, this.formatActivityForCityList)
    }
  },
  methods: {
    drillerSearch () {
      const params = {
        search: this.searchParams.search,
        prov: this.searchParams.city.split(',')[1],
        city: this.searchParams.city.split(',')[0],
        status: this.searchParams.status,
        limit: this.searchParams.limit,
        activity: this.searchParams.activity
      }
      this.$store.dispatch(FETCH_DRILLER_LIST, params)
    },
    drillerSearchReset () {
      this.searchParams.search = ''
      this.searchParams.city = ''
      this.searchParams.activity = 'DRILL'
      this.searchParams.status = 'ACTIVE'
      this.searchParams.limit = '10'
    },
    login () {
      this.$store.commit(SET_USER, { username: 'admin' })
    },
    logout () {
      this.$store.commit(SET_USER, null)
    }
  },
  created () {
    this.$store.dispatch(FETCH_CITY_LIST, this.formatActivityForCityList)
    this.drillerSearch()
  }
}
</script>

<style>
.btn {
  margin-top: 5px;
}
.form-spacing {
  margin-bottom: 15px
}
.registry-disabled-item {
  color: #808080;
  cursor: auto!important;
}
</style>
