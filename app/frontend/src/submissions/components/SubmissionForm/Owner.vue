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
        <form-input id="ownerFullName" label="Well Owner Name" v-model="ownerFullNameInput" :errors="errors['owner_full_name']" :loaded="fieldsLoaded['owner_full_name']"></form-input>
      </b-col>
      <b-col cols="12" md="6">
        <form-input id="ownerMailingAddress" label="Owner Mailing Address" v-model="ownerAddressInput" :errors="errors['owner_mailing_address']" :loaded="fieldsLoaded['owner_mailing_address']"></form-input>
        <!-- Display the address suggestions -->
        <ul v-if="addressSuggestions.length > 0" class="address-suggestions">
          <li v-for="(suggestion, index) in addressSuggestions" :key="index">
            <button @click="selectAddressSuggestion(suggestion)">{{ suggestion }}</button>
          </li>
        </ul>
        <!-- Display a loading indicator while fetching suggestions -->
        <div v-if="isLoadingSuggestions" class="loading-indicator">
          Loading...
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4">
        <form-input id="ownerCity" label="City*" v-model="ownerCityInput" :errors="errors['owner_city']" :loaded="fieldsLoaded['owner_city']" required></form-input>
      </b-col>
      <b-col cols="6" md="4">
        <b-form-group
            id="ownerProvince"
            label="Province"
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
        <form-input id="ownerPostalCode" label="Postal Code" v-model="ownerPostalCodeInput" :errors="errors['owner_postal_code']" :loaded="fieldsLoaded['owner_postal_code']"></form-input>
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
    async fetchAddressSuggestions() {

      if (!this.ownerAddressInput) {
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
        addressString: this.ownerAddressInput
      };

      const querystring = require('querystring');
      const searchParams = querystring.stringify(params);
      try {
        const response = await fetch(`https://geocoder.api.gov.bc.ca/addresses.json?q=${searchParams}`);
        console.log(encodeURIComponent(params));
        console.log(searchParams);
        const data = await response.json();
        console.log(data);
        if (data && data.features) {
          
          this.addressSuggestions = data.features.map(item => item.properties.fullAddress);
        } else {
          this.addressSuggestions = [];
        }
      } catch (error) {
        console.error(error);
        this.addressSuggestions = [];
      } finally {
        this.isLoadingSuggestions = false;
      }
    },
    selectAddressSuggestion(suggestion) {
      this.ownerAddressInput = suggestion;
      this.addressSuggestions = [];
    }
  },
  watch: {
    ownerAddressInput() {
      this.fetchAddressSuggestions();
    }
  }
}
</script>

<style>

</style>
