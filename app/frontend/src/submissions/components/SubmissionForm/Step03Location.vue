<template>
    <fieldset>
      <legend>Step 3: Well Location</legend>
      <b-row>
        <b-col>
          <p>Please provide as much information as possible. A minimum of one type of well location information is required below:</p>
          <p>1) Well location address</p>
        </b-col>
      </b-row>
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
            </v-select>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="5">
          <form-input
              id="wellCity"
              label="City"
              type="text"
              v-model="wellCityInput"
              :errors="errors['city']"
              :loaded="fieldsLoaded['city']"
              >
          </form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <p class="mb-1">OR</p>
          <p>2) Legal description</p>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalLot"
              label="Lot"
              type="text"
              v-model="legalLotInput"
              :errors="errors['legal_lot']"
              :loaded="fieldsLoaded['legal_lot']"
              >
          </form-input>
        </b-col>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalPlan"
              label="Plan"
              type="text"
              v-model="legalPlanInput"
              :errors="errors['legal_plan']"
              :loaded="fieldsLoaded['legal_plan']"
              >
          </form-input>
        </b-col>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalDistrictLot"
              label="District Lot"
              type="text"
              v-model="legalDistrictLotInput"
              :errors="errors['legal_district_lot']"
              :loaded="fieldsLoaded['legal_district_lot']"
              >
          </form-input>
        </b-col>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalBlock"
              label="Block"
              type="text"
              v-model="legalBlockInput"
              :errors="errors['legal_block']"
              :loaded="fieldsLoaded['legal_block']"
              >
          </form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalSection"
              label="Section"
              type="text"
              v-model="legalSectionInput"
              :errors="errors['legal_section']"
              :loaded="fieldsLoaded['legal_section']"
              >
          </form-input>
        </b-col>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalTownship"
              label="Township"
              type="text"
              v-model="legalTownshipInput"
              :errors="errors['legal_township']"
              :loaded="fieldsLoaded['legal_township']"
              >
          </form-input>
        </b-col>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalRange"
              label="Range"
              type="text"
              v-model="legalRangeInput"
              :errors="errors['legal_range']"
              :loaded="fieldsLoaded['legal_range']"
              >
          </form-input>
        </b-col>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="landDistrict"
              label="Land District"
              select
              :options="districtCodes"
              text-field="name"
              value-field="land_district_code"
              v-model="landDistrictInput"
              :errors="errors['land_district']"
              :loaded="fieldsLoaded['land_district']"
              >
          </form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <p class="mb-1">OR</p>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6" lg="3">
          <form-input
              id="legalPID"
              label="3) Parcel Identifier"
              type="text"
              v-model="legalPIDInput"
              :errors="errors['legal_pid']"
              :loaded="fieldsLoaded['legal_pid']"
              >
          </form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="8">
          <form-input
              id="wellLocationDescription"
              label="Description of Well Location"
              type="text"
              v-model="wellLocationDescriptionInput"
              :errors="errors['well_location_description']"
              :loaded="fieldsLoaded['well_location_description']"
              >
          </form-input>
        </b-col>
      </b-row>

      <!-- Error message when location not given -->
      <b-alert class="mt-3" variant="danger" :show="errorWellLocationNotProvided">
        Must provide well location as either an address, legal description, or parcel identifier.
      </b-alert>

    </fieldset>
</template>
<script>
import debounce from 'lodash.debounce'
import axios from 'axios'
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'Step03Location',
  mixins: [inputBindingsMixin],
  props: {
    city: String,
    streetAddress: String,
    legalLot: String,
    legalPlan: String,
    legalDistrictLot: String,
    legalBlock: String,
    legalSection: String,
    legalTownship: String,
    legalRange: String,
    landDistrict: String,
    legalPID: String,
    wellLocationDescription: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    errorWellLocationNotProvided: Boolean
  },
  fields: {
    wellAddressInput: 'streetAddress',
    wellCityInput: 'city',
    legalLotInput: 'legalLot',
    legalPlanInput: 'legalPlan',
    legalDistrictLotInput: 'legalDistrictLot',
    legalBlockInput: 'legalBlock',
    legalSectionInput: 'legalSection',
    legalTownshipInput: 'legalTownship',
    legalRangeInput: 'legalRange',
    landDistrictInput: 'landDistrict',
    legalPIDInput: 'legalPID',
    wellLocationDescriptionInput: 'wellLocationDescription'
  },
  data () {
    return {
      wellAddressHints: []
    }
  },
  computed: {
    districtCodes () {
      const initial = [{
        land_district_code: '',
        name: 'Select district'
      }]
      return initial.concat(this.codes.land_district_codes)
    },
    ...mapGetters(['codes'])
  },
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
