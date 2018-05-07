<template>
  <b-modal id="orgModal" title="Add a Company" hide-footer @shown="focusInput()">
    <div class="col-xs-12" v-if="error">
      <api-error :error="error" resetter="SET_ERROR"></api-error>
    </div>
    <div class="container">
        <b-form @submit.prevent="onFormSubmit()" @reset.prevent="onFormReset()">
          <b-row>
            <b-col cols="12">
              <b-form-group
                id="orgNameInputGroup"
                label="Company name:"
                label-for="orgNameInput">
                <b-form-input
                    id="orgNameInput"
                    type="text"
                    v-model="orgForm.name"
                    required
                    placeholder="Enter company name"
                    ref="orgNameInput"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col cols="12">
              <b-form-group
                id="orgAddressInputGroup"
                label="Street address:"
                label-for="orgAddressInput">
                <b-form-input
                    id="orgAddressInput"
                    type="text"
                    v-model="orgForm.street_address"
                    placeholder="Enter street address"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="6">
              <b-form-group
                id="orgCityInputGroup"
                label="City:"
                label-for="orgCityInput">
                <b-form-input
                    id="orgCityInput"
                    type="text"
                    v-model="orgForm.city"
                    placeholder="Enter city"/>
              </b-form-group>
            </b-col>
            <b-col cols="12" md="6">
              <b-form-group
                id="provInputGroup"
                label="Province/State:"
                label-for="provInput">
                <v-select :options="provOptions" v-model="orgForm.province_state" placeholder="Select province"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="6">
              <b-form-group
                id="postalCodeInputGroup"
                label="Postal code:"
                label-for="postalCodeInput">
                <b-form-input
                    id="postalCodeInput"
                    type="text"
                    v-model="orgForm.postal_code"
                    placeholder="Enter postal code"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col cols="12" md="6">
              <b-form-group
                id="telInputGroup"
                label="Telephone:"
                label-for="telInput">
                <b-form-input
                    id="telInput"
                    type="text"
                    v-model="orgForm.main_tel"
                    placeholder="Enter telephone number"/>
              </b-form-group>
            </b-col>
            <b-col cols="12" md="6">
              <b-form-group
                id="faxInputGroup"
                label="Fax number:"
                label-for="faxInput">
                <b-form-input
                    id="faxInput"
                    type="text"
                    v-model="orgForm.fax_tel"
                    placeholder="Enter fax number"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12">
              <b-form-group
                id="emailInputGroup"
                label="Email:"
                label-for="emailInput">
                <b-form-input
                    id="emailInput"
                    type="text"
                    v-model="orgForm.email"
                    placeholder="Enter email address"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12">
              <b-form-group
                id="websiteInputGroup"
                label="Website:"
                label-for="websiteInput">
                <b-form-input
                    id="websiteInput"
                    type="text"
                    v-model="orgForm.website_url"
                    placeholder="Enter website address (e.g. http://www.example.com)"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="my-3">
            <b-col>
              <b-button type="submit" class="mr-2" variant="primary" :disabled="orgSubmitLoading">Submit</b-button>
              <b-button type="reset" variant="light" id="orgFormResetButton">Cancel</b-button>
            </b-col>
          </b-row>
        </b-form>
        <b-alert v-if="!!orgSubmitError" show variant="warning" dismissible @dismissed="orgSubmitError=null">
          Error creating a new company.
          <div v-for="(value, key, index) in orgSubmitError.data" :key="`submit error ${index}`">
              <span class="text-capitalize">{{ key }}</span>:
              <span
                v-for="(msg, msgIndex) in value"
                :key="`submit error msg ${index} ${msgIndex}`">{{ msg }} </span>
            </div>
        </b-alert>
    </div>
  </b-modal>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { mapGetters } from 'vuex'

export default {
  name: 'OrganizationAdd',
  data () {
    return {
      orgForm: {
        name: '',
        street_address: '',
        city: '',
        province_state: '',
        postal_code: '',
        main_tel: '',
        fax_tel: '',
        website_url: ''
      },
      provOptions: ['BC', 'AB'],
      orgSubmitLoading: false,
      orgSubmitError: null
    }
  },
  computed: {
    ...mapGetters(['error'])
  },
  methods: {
    onFormSubmit () {
      const org = {}
      this.orgSubmitLoading = true

      // build 'org' object out of orgForm, skipping empty strings
      for (let prop in this.orgForm) {
        if (this.orgForm[prop] !== '' && this.orgForm[prop] !== null) {
          org[prop] = this.orgForm[prop]
        }
      }
      ApiService.post('organizations', org).then((response) => {
        this.orgSubmitLoading = false
        this.$root.$emit('bv::hide::modal', 'orgModal')
        this.$emit('newOrgAdded', response.data.org_guid)
      }).catch((error) => {
        this.orgSubmitLoading = false
        this.orgSubmitError = error.response
      })
    },
    onFormReset () {
      this.orgForm = Object.assign({}, {
        name: '',
        street_address: '',
        city: '',
        province_state: '',
        postal_code: '',
        main_tel: '',
        fax_tel: '',
        website_url: ''
      })
      this.$root.$emit('bv::hide::modal', 'orgModal')
    },
    focusInput () {
      this.$refs.orgNameInput.focus()
    }
  }
}
</script>

<style>

</style>
