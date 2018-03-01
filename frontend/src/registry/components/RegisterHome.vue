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
                        <input type="radio" name="regTypeSelector" id="regTypeDriller" v-model="searchParams.regType" value="driller" style="margin-top: 0px"> Well Driller
                      </label>
                      <label class="radio-inline">
                        <input type="radio" name="regTypeSelector" id="regTypeInstaller" v-model="searchParams.regType" value="installer" style="margin-top: 0px"> Pump Installer
                      </label>
                    </div>
                  </div>
                  <div class="row">
                    <div class="form-group">
                      <div class="col-xs-12 col-sm-6 form-spacing">
                        <label>Community</label>
                        <select class="form-control" v-model="searchParams.communities">
                          <option>All</option>
                          <option>Victoria</option>
                          <option>Duncan</option>
                          <option>Nanaimo</option>
                        </select>
                      </div>
                    </div>
                    <div class="form-group">
                      <div class="col-xs-12 col-sm-6 form-spacing">
                        <label>Registration status</label>
                        <select v-model="searchParams.regStatus" class="form-control">
                          <option>All</option>
                          <option>Pending</option>
                          <option>Not registered</option>
                          <option>Registered</option>
                          <option>Removed</option>
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
import { FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

export default {
  components: {
    'register-table': RegisterTable,
    'api-error': APIErrorMessage
  },
  created () {
    this.$store.dispatch(FETCH_DRILLER_LIST, this.searchParams)
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
      'listError'
    ])
  },
  data () {
    return {
      adminPanelToggle: false,
      community: null,
      regType: 'driller',
      regStatus: 'all',
      regTypeOptions: [
        {text: 'Well Driller', value: 'driller'},
        {text: 'Well Pump Installer', value: 'installer'}
      ],
      regStatusOptions: [
        { value: 'all', text: 'All' },
        { value: 'pending', text: 'Pending' },
        { value: 'notRegistered', text: 'Not registered' },
        { value: 'registered', text: 'Registered' },
        { value: 'removed', text: 'Removed' }
      ],
      searchParams: {
        search: '',
        communities: 'All',
        regType: 'driller',
        regStatus: 'All',
        limit: '10'
      }
    }
  },
  methods: {
    drillerSearch () {
      this.$store.dispatch(FETCH_DRILLER_LIST, this.searchParams)
    },
    drillerSearchReset () {
      this.searchParams.search = ''
      this.searchParams.communities = 'All'
      this.searchParams.regType = 'driller'
      this.searchParams.regStatus = 'All'
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
