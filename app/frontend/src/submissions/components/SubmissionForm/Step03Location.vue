<template>
    <fieldset>
      <legend>Well Location</legend>
      <b-row>
        <b-col cols="12" md="6">
          <b-form-group label="Street address">
            <v-select
              v-model="wellAddressInput"
              id="wellAddressSelect"
              :filterable="false"
              taggable
              :options="wellAddressHints"
              @search="onWellAddressSearch">
              <template slot="no-options">
                &nbsp;
              </template>
              <!-- <template slot="option" slot-scope="option">
                <div>
                  {{ option.well_tag_number }} ({{ option.owner_full_name }})
                </div>
              </template>
              <template slot="selected-option" slot-scope="option">
                <div>
                  {{ option.well_tag_number }}
                </div>
              </template> -->
            </v-select>
          </b-form-group>
        </b-col>
      </b-row>
    </fieldset>
</template>
<script>
import debounce from 'lodash.debounce'
import axios from 'axios'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
// import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'Step03Location',
  mixins: [inputBindingsMixin],
  props: {
    streetAddress: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    }
  },
  fields: {
    wellAddressInput: 'streetAddress'
  },
  data () {
    return {
      wellAddressHints: []
    }
  },
  computed: {},
  watch: {
    streetAddress (val) {
      // match against strings that contain two groups of letters/numbers (e.g. "123 Main")
      if (!(/^(\w+ [ \w]+)/.test(val))) {
        this.wellAddressHints = []
      }
    }
  },
  methods: {
    onWellAddressSearch (search, loading) {
      loading(true)
      this.wellAddressSearch(loading, search, this)
    },
    wellAddressSearch: debounce((loading, search, vm) => {
      if (/^(\w+ [ \w]+)/.test(search)) {
        console.log('matched', search)
        axios.get(`https://geocoder.api.gov.bc.ca/addresses.json?addressString=${escape(search)}&autoComplete=true&maxResults=10&brief=true`).then((response) => {
          vm.wellAddressHints = response.data.features.map(x => x.properties.fullAddress)
        })
      }
      loading(false)
    }, 500)
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
</style>
