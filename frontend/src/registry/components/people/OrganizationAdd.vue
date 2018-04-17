<template>
  <b-container>
    <b-card no-body class="mb-3">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <div class="col-xs-12" v-if="error">
      <api-error :error="error" resetter="SET_ERROR"></api-error>
    </div>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Add an Organization</h5>
        <b-form @submit.prevent="onFormSubmit()" @reset.prevent="onFormReset()">
          <b-row>
            <b-col cols="12" md="5">
              <b-form-group
                id="orgNameInputGroup"
                label="Organization name:"
                label-for="orgNameInput">
                <b-form-input
                    id="orgNameInput"
                    type="text"
                    v-model="orgForm.name"
                    required
                    placeholder="Enter organization name"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col cols="12" md="5">
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
            <b-col cols="12" md="5">
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
          </b-row>
          <b-row>
            <b-col cols="12" md="5">
              <b-form-group
                id="provInputGroup"
                label="Province/State:"
                label-for="provInput">
                <v-select :options="provOptions" v-model="orgForm.province_state" placeholder="Select a province or state"/>
              </b-form-group>
            </b-col>
            <b-col cols="12" md="5">
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
            <b-col cols="12" md="5">
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
            <b-col cols="12" md="5">
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
            <b-col cols="12" md="5">
              <b-form-group
                id="websiteInputGroup"
                label="Website:"
                label-for="websiteInput">
                <b-form-input
                    id="websiteInput"
                    type="text"
                    v-model="orgForm.website_url"
                    placeholder="Enter website address"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col>
              <b-button type="submit" class="mr-2" variant="primary">Submit</b-button>
              <b-button type="reset" variant="light">Reset</b-button>
            </b-col>
          </b-row>
        </b-form>
      </div>
    </div>
  </b-container>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'OrganizationAdd',
  components: {
    'api-error': APIErrorMessage
  },
  data () {
    return {
      breadcrumbs: [
        {
          text: 'Registry Search',
          to: { name: 'SearchHome' }
        },
        {
          text: 'Add an Organization',
          active: true
        }
      ],
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
      provOptions: ['BC', 'AB']
    }
  },
  computed: {
    ...mapGetters(['error'])
  },
  methods: {
    onFormSubmit () {
      const org = {}

      // build 'org' object out of orgForm, skipping empty strings
      for (let prop in this.orgForm) {
        if (this.orgForm[prop] !== '') {
          org[prop] = this.orgForm[prop]
        }
      }
      ApiService.post('organizations', org)
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
    }
  }
}
</script>

<style>

</style>
