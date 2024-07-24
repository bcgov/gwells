/*
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
    <fieldset>
      <b-row>
        <b-col cols="12" lg="6">
          <legend :id="id">Well Location</legend>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <back-to-top-link v-if="isStaffEdit"/>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <p>Please provide as much information as possible.</p> <p class="bg-warning p-2">A minimum of one type of well location information is required below:</p>
          <p class="d-inline font-weight-bold">1) Well Location Address</p>
          <div class="d-inline pl-2"><b-form-checkbox v-model="sameAsOwnerAddress">Same as owner address</b-form-checkbox></div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input
            v-model="streetAddressInput"
            id="wellStreetAddress"
            type="text"
            label="Street address"
            @input="fetchAddressSuggestions"
            v-on:focus="showList(true)"
            v-on:blur="showList(false)"
            :errors="errors['street_address']"
            :loaded="fieldsLoaded['street_address']"
            :disabled="sameAsOwnerAddress"
          ></form-input>
           <!-- Display the address suggestions -->
        <div v-if="addressSuggestions.length > 0" class="address-suggestions list-group list-group-flush border" id="location-address-suggestions-list">
          <div v-for="(suggestion, index) in addressSuggestions" :key="index">
            <button @mousedown="selectAddressSuggestion(suggestion)" class="list-group-item list-group-item-action border-0">{{ suggestion }}</button>
          </div>
        </div>
        <!-- Display a loading indicator while fetching suggestions -->
        <div v-if="isLoadingSuggestions" class="loading-indicator">
          Loading...
        </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="5">
          <form-input
              id="wellCity"
              label="City"
              type="text"
              v-model="cityInput"
              :errors="errors['city']"
              :loaded="fieldsLoaded['city']"
              :disabled="sameAsOwnerAddress"
              >
          </form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <p class="mb-1">OR</p>
          <p class="font-weight-bold">
            2) Legal Description
            <i id="legal_description_fields" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
            <b-popover
              target="legal_description_fields"
              triggers="hover focus"
              :content="TOOLTIP_TEXT.location_vue.legal_description_fields"
            />
          </p>
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
          <p class="font-weight-bold">3) Parcel Identifier (PID)</p>
          <form-input
              id="legalPID"
              type="text"
              hint="*Input a 9 digit number (including leading zeroes, if necessary)"
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
      <b-alert class="mt-3" variant="danger" :show="errors.well_location_section && errors.well_location_section.length > 0">
        Must provide well location as either an address, legal description, or parcel identifier.
      </b-alert>

    </fieldset>
</template>
<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import BackToTopLink from '@/common/components/BackToTopLink.vue'
import ApiService from '../../../common/services/ApiService'
import { TOOLTIP_TEXT } from '@/common/constants'

export default {
  name: 'Location',
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    id: {
      type: String,
      isInput: false
    },
    ownerMailingAddress: String,
    ownerProvinceState: String,
    ownerCity: String,
    ownerPostalCode: String,
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
    legalPID: null,
    wellLocationDescription: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    errorWellLocationNotProvided: Boolean,
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  data () {
    return {
      wellAddressHints: [],
      sameAsOwnerAddress: false,
      addressSuggestions: [],
      isLoadingSuggestions: false,
      TOOLTIP_TEXT: TOOLTIP_TEXT,
    }
  },
  computed: {
    districtCodes () {
      const initial = [{
        land_district_code: '',
        name: 'Select district'
      }]
      // codes may not be loaded yet, or busy loading, so we have to check if we even have a map
      // function available
      if (!this.codes || !this.codes.land_district_codes || !this.codes.land_district_codes.map) {
        return initial
      }
      return initial.concat(
        this.codes.land_district_codes.map((item) => {
          return {
            land_district_code: item.land_district_code,
            name: `${item.name} (${item.land_district_code})`
          }
        })
      )
    },
    ...mapGetters(['codes'])
  },
  watch: {
    sameAsOwnerAddress (val) {
      this.streetAddressInput = String(this.ownerMailingAddress)
      this.cityInput = String(this.ownerCity)
    }
  },
  methods: {
    /**
     * @desc Asynchronously fetches address suggestions based on the owner's address input.
     * If no input is provided, it clears the current suggestions.
     * On success, it maps the received data to full addresses and updates the addressSuggestions state.
     * On failure, it logs the error and clears the current suggestions.
     * Finally, sets the loading state to false.
     */
    async fetchAddressSuggestions() {
      const MIN_QUERY_LENGTH = 3;
      if (!this.streetAddressInput || this.streetAddressInput.length < MIN_QUERY_LENGTH) {
        this.addressSuggestions = [];
        return;
      }
      this.isLoadingSuggestions = true;
      const params = {
        minScore: 50,
        maxResults: 5,
        echo: 'false',
        brief: true,
        autoComplete: true,
        matchPrecision: 'CIVIC_NUMBER', //forced minimum level of specificity for return values. will only return addresses that contain at least contain a street number
        addressString: this.streetAddressInput
      };

      const querystring = require('querystring');
      const searchParams = querystring.stringify(params);
      try {
        ApiService.getAddresses(searchParams).then((response) => {
        if (response.data) {
          const data = response.data;
          if (data && data.features) {
            this.addressSuggestions = data.features.map(item => item.properties.fullAddress);
          } else {
            this.addressSuggestions = [];
          }
        }
      })
      } catch (error) {
        console.error(error);
        this.addressSuggestions = [];
      } finally {
        this.isLoadingSuggestions = false;
      }
    },

    /**
     * @desc Processes the selected address suggestion.
     * Splits the suggestion into components and updates the owner's province, city, and address inputs accordingly.
     * Clears the address suggestions afterward.
     * @param {string} suggestion - The selected address suggestion. ("1234 Street Rd, Name of City, BC")
     */
    selectAddressSuggestion(suggestion) {
      const CITY_ARRAY_INDEX = 1;
      const STREET_ARRAY_INDEX = 0;
      const wellAddressArray = suggestion.split(',');
      this.streetAddressInput = wellAddressArray[STREET_ARRAY_INDEX];
      this.cityInput = wellAddressArray[CITY_ARRAY_INDEX].trim();
    },

    /**
     * @desc Clears the current list of address suggestions.
     */
    clearAddressSuggestions () {
      this.addressSuggestions = [];
    },
    /**
     * @desc Shows or hides the address suggestions list in the UI.
     * @param {boolean} show - a boolean which indicates whether to show or hide the element
     */
     showList(show) {
      if(document.getElementById('location-address-suggestions-list')){
        document.getElementById('location-address-suggestions-list').style.display =  show? 'block' : 'none';
      }
    }        
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}

/** Corrects how bold font doesn't render in chrome */
p, #legalPID__BV_label_ {
  -webkit-font-smoothing: antialiased;
}

.address-suggestions {
    list-style-type: none;
    position: absolute;
    z-index: 10;
  }
</style>
