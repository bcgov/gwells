<template>
  <div class="container-fluid">
      <div class="row">
        <div class="col-xs-8">
          <a id="main-content-anchor"></a>
          <h2>Register of Well Drillers and Well Pump Installers</h2>
            <p><a href="#">Learn more about registering as a well driller or well pump installer in B.C.</a></p>
        </div>
        <div class="col-xs-4">
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
                <form @submit.prevent="drillerSearch">
                  <div class="form-group">
                    <div class="col-xs-12">
                      <label>Choose professional type: &nbsp;</label>
                    </div>
                    <div class="col-xs-12 form-spacing">
                      <label class="radio-inline">
                        <input type="radio" name="regTypeSelector" id="regTypeDriller" value="driller" style="margin-top: 0px"> Well Driller
                      </label>
                      <label class="radio-inline">
                        <input type="radio" name="regTypeSelector" id="regTypeInstaller" value="installer" style="margin-top: 0px"> Pump Installer
                      </label>
                    </div>
                  </div>
                  <div class="row">
                    <div class="form-group">
                      <div class="col-xs-12 col-sm-6 form-spacing">
                        <label>Community</label>
                        <select class="form-control">
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
                        <select class="form-control">
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
        <div class="col-xs-12">
          <h3>Well Driller Results</h3>
        </div>
        <div class="col-xs-12 form-inline">
          <div class="form-group col-xs-4">
            <select class="form-control" v-model="searchParams.limit"><option>10</option><option>25</option></select> entries
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
import { mapGetters } from 'vuex'
import { FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

export default {
  components: {
    'register-table': RegisterTable
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
      'error'
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
        communities: '',
        regType: '',
        regStatus: '',
        limit: '10'
      }
    }
  },
  methods: {
    drillerSearch () {
      this.$store.dispatch(FETCH_DRILLER_LIST, this.searchParams)
    },
    drillerSearchReset () {
      this.searchParams.regType = 'driller'
      this.searchParams.search = ''
      this.searchParams.regType = ''
      this.searchParams.regStatus = 'all'
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
