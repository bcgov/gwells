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
        <legend :id="id">Well Owner</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12" md="6">
        <form-input 
          id="ownerFullName" 
          label="Well Owner Name *" 
          v-model="ownerFullNameInput" 
          :errors="errors['owner_full_name']" 
          :loaded="fieldsLoaded['owner_full_name']"
        ></form-input>       
      </b-col>
      <b-col cols="12" md="6">
        <form-input 
          id="ownerMailingAddress" 
          label="Owner Mailing Address *" 
          v-model="ownerAddressInput" 
          @input="fetchAddressSuggestions" 
          v-on:focus="showList(true)" 
          v-on:blur="showList(false)" 
          :errors="errors['owner_mailing_address']" 
          :loaded="fieldsLoaded['owner_mailing_address']">
        </form-input>
        <!-- Display the address suggestions -->
        <div v-if="addressSuggestions.length > 0" class="address-suggestions list-group list-group-flush border" id="owner-address-suggestions-list">
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
      <b-col cols="12" md="4">
        <form-input id="ownerCity" label="City *" v-model="ownerCityInput" :errors="errors['owner_city']" :loaded="fieldsLoaded['owner_city']" required></form-input>
      </b-col>
      <b-col cols="6" md="4">
        <b-form-group
            id="ownerProvince"
            label="Province or State *"
            aria-describedby="ownerProvinceInvalidFeedback">
          <b-form-select
              v-model="ownerProvinceInput"
              :options="codes.province_codes"
              value-field="province_state_code"
              text-field="description"
              :state="errors['owner_province_state'] ? false : null">
            <template slot="first">
              <option :value="null" disabled>Select a province</option>
            </template>
          </b-form-select>
          <b-form-invalid-feedback id="ownerProvinceInvalidFeedback">
            <div v-for="(error, index) in errors['owner_province_state']" :key="`ProvinceInput error ${index}`">
              {{ error }}
            </div>
          </b-form-invalid-feedback>
        </b-form-group>
      </b-col>
      <b-col cols="6" md="4" xl="3">
        <form-input id="ownerPostalCode" label="Postal Code *" v-model="ownerPostalCodeInput" :errors="errors['owner_postal_code']" :loaded="fieldsLoaded['owner_postal_code']"></form-input>
      </b-col>
    </b-row>
    <b-row v-if="isStaffEdit">
      <b-col cols="12" md="6" lg="4" xl="4">
        <form-input id="ownerEmail" label="Email Address" v-model="ownerEmailInput" :errors="errors['owner_email']" :loaded="fieldsLoaded['owner_email']"></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4" xl="3">
        <form-input
            id="ownerTel"
            label="Telephone"
            v-model="ownerTelInput"
            :errors="errors['owner_tel']"
            :loaded="fieldsLoaded['owner_tel']"
            :formatter="formatTel"
            lazy-formatter
            >
        </form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'
import BackToTopLink from '@/common/components/BackToTopLink.vue'
import ApiService from '../../../common/services/ApiService'

export default {
  mixins: [inputBindingsMixin, inputFormatMixin],
  components: {
    BackToTopLink
  },
  props: {
    ownerFullName: String,
    ownerMailingAddress: String,
    ownerCity: String,
    ownerProvinceState: String,
    ownerPostalCode: String,
    ownerEmail: String,
    ownerTel: String,
    id: {
      type: String,
      isInput: false
    },
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  fields: {
    ownerFullNameInput: 'ownerFullName',
    ownerAddressInput: 'ownerMailingAddress',
    ownerCityInput: 'ownerCity',
    ownerProvinceInput: 'ownerProvinceState',
    ownerPostalCodeInput: 'ownerPostalCode',
    ownerEmailInput: 'ownerEmail',
    ownerTelInput: 'ownerTel'
  },
  data () {
    return {
      addressSuggestions: [],
      isLoadingSuggestions: false
    }
  },
  computed: {
    ...mapGetters(['codes'])
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
      if (!this.ownerAddressInput || this.ownerAddressInput.length < MIN_QUERY_LENGTH) {
        this.addressSuggestions = [];
        return;
      } 
        this.isLoadingSuggestions = true;
        const params = {
          minScore: 50, //accuracy score of results compared to input
          maxResults: 5,
          echo: 'false',
          brief: true,
          autoComplete: true,
          matchPrecision: 'CIVIC_NUMBER', //forced minimum level of specificity for return values. will only return addresses that contain at least contain a street number
          addressString: this.ownerAddressInput
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
      }
      )
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
      const ownerAddressArray = suggestion.split(',');
      const PROV_ARRAY_INDEX = 2;
      const CITY_ARRAY_INDEX = 1;
      const STREET_ARRAY_INDEX = 0;
      let province = ownerAddressArray[PROV_ARRAY_INDEX].toUpperCase().trim();
      if(province === 'BC' || province === 'BRITISH COLUMBIA'){
        this.ownerProvinceInput = this.codes.province_codes[0].province_state_code;
      }
      else {
      this.ownerProvinceInput = "";
      }
      this.ownerCityInput = ownerAddressArray[CITY_ARRAY_INDEX].trim();
      this.ownerAddressInput = ownerAddressArray[STREET_ARRAY_INDEX];
    
    this.clearAddressSuggestions();
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
      if(document.getElementById('owner-address-suggestions-list')){
        document.getElementById('owner-address-suggestions-list').style.display =  show? 'block' : 'none';
      }
    }        
  }
}
</script>

<style>
  .address-suggestions {
    list-style-type: none;
    position: absolute;
    z-index: 10;
  }
</style>
