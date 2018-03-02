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
              <p>
                <button type="button" class="btn btn-primary">Add new entry</button>
                <button type="button" class="btn btn-primary">Manage companies</button>
              </p>
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
                          <option value="">All</option>
                          <option value="PENDING">Pending</option>
                          <option value="INACTIVE">Not registered</option>
                          <option value="ACTIVE">Registered</option>
                          <option value="REMOVED">Removed</option>
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
        <div class="col-xs-12 form-inline">
          <div class="form-group col-xs-4">
            <select class="form-control input-sm" v-model="searchParams.limit"><option>10</option><option>25</option></select> entries
          </div>
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
import { FETCH_CITY_LIST, FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

export default {
  components: {
    'register-table': RegisterTable,
    'api-error': APIErrorMessage
  },
  created () {
    this.$store.dispatch(FETCH_CITY_LIST)
    this.drillerSearch()
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
    ...mapGetters([
      'loading',
      'listError',
      'cityList'
    ])
  },
  data () {
    return {
      adminPanelToggle: false,
      regTypeOptions: [
        {text: 'Well Driller', value: 'DRILL'},
        {text: 'Well Pump Installer', value: 'PUMP'}
      ],
      regStatusOptions: [
        { value: '', text: 'All' },
        { value: 'PENDING', text: 'Pending' },
        { value: 'INACTIVE', text: 'Not registered' },
        { value: 'ACTIVE', text: 'Registered' },
        { value: 'REMOVED', text: 'Removed' }
      ],
      searchParams: {
        search: '',
        city: '',
        activity: 'DRILL',
        status: '',
        limit: '10'
      }
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
    }
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
</style>
