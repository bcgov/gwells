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
    <legend :id="id">Well Owner</legend>
    <b-row>
      <b-col cols="12" md="6">
        <form-input id="ownerFullName" label="Well Owner Name *" v-model="ownerFullNameInput" :errors="errors['owner_full_name']" :loaded="fieldsLoaded['owner_full_name']"></form-input>
      </b-col>
      <b-col cols="12" md="6">
        <form-input id="ownerMailingAddress" label="Owner Mailing Address *" v-model="ownerAddressInput" :errors="errors['owner_mailing_address']" :loaded="fieldsLoaded['owner_mailing_address']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4">
        <form-input id="ownerCity" label="City *" v-model="ownerCityInput" :errors="errors['owner_city']" :loaded="fieldsLoaded['owner_city']"></form-input>
      </b-col>
      <b-col cols="6" md="4">
        <b-form-group
            id="ownerProvince"
            label="Province *"
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
      <b-col cols="6" md="4">
        <form-input id="ownerPostalCode" label="Postal Code *" v-model="ownerPostalCodeInput" :errors="errors['owner_postal_code']" :loaded="fieldsLoaded['owner_postal_code']"></form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    ownerFullName: String,
    ownerMailingAddress: String,
    ownerCity: String,
    ownerProvinceState: String,
    ownerPostalCode: String,
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
    }
  },
  fields: {
    ownerFullNameInput: 'ownerFullName',
    ownerAddressInput: 'ownerMailingAddress',
    ownerCityInput: 'ownerCity',
    ownerProvinceInput: 'ownerProvinceState',
    ownerPostalCodeInput: 'ownerPostalCode'
  },
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
