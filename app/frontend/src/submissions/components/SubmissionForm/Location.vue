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
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <p>Please provide as much information as possible. A minimum of one type of well location information is required below:</p>
          <p class="d-inline">1) Well location address</p>
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
            :errors="errors['street_address']"
            :loaded="fieldsLoaded['street_address']"
            :disabled="sameAsOwnerAddress"
          ></form-input>
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
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'Location',
  mixins: [inputBindingsMixin],
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
      sameAsOwnerAddress: false
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
    sameAsOwnerAddress (val) {
      this.streetAddressInput = String(this.ownerMailingAddress)
      this.cityInput = String(this.ownerCity)
    }
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
</style>
