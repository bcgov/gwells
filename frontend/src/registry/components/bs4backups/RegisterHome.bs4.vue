<template>
  <b-container>
      <b-row>
        <b-col cols="12" md="8">
          <a id="main-content-anchor"></a>
          <h2>Register of Well Drillers and Well Pump Installers</h2>
            <p><a href="#">Learn more about registering as a well driller or well pump installer in B.C.</a></p>
        </b-col>
        <b-col>
          <b-button v-b-toggle.gw-admin-collapse class="m-1" variant="outline-primary">GWELLS Administrator options</b-button>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-collapse id="gw-admin-collapse" class="mt-2">
            <b-card>
              <p class="card-text">
                <b-button class="m-1" variant="outline-primary">Add new entry</b-button>
                <b-button class="m-1" variant="outline-primary">Manage companies</b-button>
              </p>
            </b-card>
          </b-collapse>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-card class="mt-2 mb-2" title="Search for a Well Driller or Well Installer">
          <b-form @submit="drillerSearch" @reset="drillerSearchReset">
            <b-container fluid>
              <b-form-row align-h="start">
                <b-col>
                  <b-form-group label="Choose a professional type:">
                    <b-form-radio-group v-model="regType">
                      <b-form-radio value="driller" style="padding-top:4px">Well Driller</b-form-radio>
                      <b-form-radio value="installer" style="padding-top:4px">Well Pump Installer</b-form-radio>
                    </b-form-radio-group>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row align-h="start">
                <b-col sm="12" md="6">
                  <b-form-group label="Community">
                    <b-form-select v-model="community" :options="cities" size="sm" style="font-size:14px"/>
                  </b-form-group>
                </b-col>
                <b-col sm="12" md="6">
                  <b-form-group label="Registration status">
                    <b-form-select v-model="regStatus" :options="regStatusOptions" size="sm" style="font-size:14px"/>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row align-h="start">
                <b-col>
                  <b-form-group label="Individual, company, or registration number">
                    <b-form-input v-model="searchParams.searchString" type="text" placeholder="Search" size="sm" style="font-size:14px"/>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row align-h="start">
                <b-col>
                  <b-button type="submit" variant="primary">Search</b-button>
                  <b-button type="reset" variant="secondary">Reset</b-button>
                </b-col>
              </b-form-row>
            </b-container>
          </b-form>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <register-table :items="drillers"/>
        </b-col>
      </b-row>
  </b-container>
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
    this.$store.dispatch(FETCH_DRILLER_LIST, { search: '' })
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
      'error',
      'drillers'
    ])
  },
  data () {
    return {
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
        searchString: ''
      }
    }
  },
  methods: {
    drillerSearch (e) {
      e.preventDefault()
      this.$store.dispatch(FETCH_DRILLER_LIST, { search: this.searchParams.searchString })
    },
    drillerSearchReset (e) {
      e.preventDefault()
      this.regType = 'driller'
      this.searchParams.searchString = ''
      this.regStatus = 'all'
    }
  }
}
</script>

<style>
.btn {
  margin-top: 5px;
}
</style>
