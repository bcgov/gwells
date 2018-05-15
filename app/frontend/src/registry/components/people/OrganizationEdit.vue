<template>
  <b-container>
    <b-card title="Manage Organizations">

      <!-- Add company button (opens 'add company' modal) and success feedback -->
      <b-row>
        <b-col>
          <b-button
              type="button"
              v-b-modal.orgModal
              variant="light"
              size="sm"
              class="mb-3">
            <i class="fa fa-plus-square-o"></i> Add a company</b-button>
          <organization-add @newOrgAdded="newOrgHandler"></organization-add>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-alert variant="success" :show="companyAddSuccess" dismissible @dismissed="companyAddSuccess=false">Company added.</b-alert>
        </b-col>
      </b-row>

      <!-- Company selector (used to select company to edit) -->
      <b-row>
        <b-col cols="12" md="7">
          <b-form-group label="Select a company:" label-for="manageCompanySelect">
            <v-select
                id="manageCompanySelect"
                :options="companies"
                label="org_verbose_name"
                v-model="selectedCompany"
                placeholder="Begin typing a company name"
                ></v-select>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="5">
          <b-alert variant="warning" :show="!!companyListError" dismissible @dismissed="companyListError=false">
            Error retrieving list of companies. Please try again later.
          </b-alert>
        </b-col>
      </b-row>

      <!-- Selected company details -->
      <b-card>
        <b-form @submit.prevent="console.log('submitted')">
          <b-row>
            <b-col cols="12" md="5">
                <b-form-group
                  id="companyNameInputGroup"
                  label="Company name:"
                  label-for="companyNameInput">
                  <b-form-input
                    id="companyNameInput"
                    type="text"
                    v-model="companyForm.name"/>
                </b-form-group>
            </b-col>
              <b-col cols="12" md="5" offset-md="1">
                <b-form-group
                  id="companyAddressInputGroup"
                  label="Street address:"
                  label-for="companyAddressInput">
                  <b-form-input
                    id="companyAddressInput"
                    type="text"
                    v-model="companyForm.street_address"/>
                </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="5">
                <b-form-group
                  id="companyCityInputGroup"
                  label="City:"
                  label-for="companyCityInput">
                  <b-form-input
                    id="companyCityInput"
                    type="text"
                    v-model="companyForm.city"/>
                </b-form-group>
            </b-col>
              <b-col cols="12" md="5" offset-md="1">
                <b-form-group
                  id="companyProvinceInputGroup"
                  label="Province:"
                  label-for="companyProvinceInput">
                  <b-form-select
                    id="companyProvinceInput"
                    :options="provCodes"
                    v-model="companyForm.province_state">
                    <option value="" disabled>Select a province</option>
                  </b-form-select>
                </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="5">
                <b-form-group
                  id="postalCodeInputGroup"
                  label="Postal code:"
                  label-for="postalCodeInput">
                  <b-form-input
                    id="postalCodeInput"
                    type="text"
                    v-model="companyForm.postal_code"/>
                </b-form-group>
            </b-col>
              <b-col cols="12" md="5" offset-md="1">
                <b-form-group
                  id="companyTelInputGroup"
                  label="Office number:"
                  label-for="companyTelInput">
                  <b-form-input
                    id="companyTelInput"
                    type="text"
                    v-model="companyForm.main_tel"/>
                </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="5">
                <b-form-group
                  id="companyFaxInputGroup"
                  label="Fax number:"
                  label-for="companyFaxInput">
                  <b-form-input
                    id="companyFaxInput"
                    type="text"
                    v-model="companyForm.fax_tel"/>
                </b-form-group>
            </b-col>
              <b-col cols="12" md="5" offset-md="1">
                <b-form-group
                  id="companyWebsiteInputGroup"
                  label="Website:"
                  label-for="companyWebsiteInput">
                  <b-form-input
                    id="companyWebsiteInput"
                    type="text"
                    v-model="companyForm.website_url"/>
                </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="11">
                <b-form-group
                  id="companyNotesInputGroup"
                  label="Notes:"
                  label-for="companyNotesInput">
                  <b-form-textarea
                    id="companyNotesInput"
                    :rows="3"
                    :max-rows="6"
                    v-model="companyNotesForm"/>
                </b-form-group>
            </b-col>
          </b-row>
        </b-form>
      </b-card>
    </b-card>
  </b-container>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'

export default {
  name: 'OrganizationEdit',
  components: {
    OrganizationAdd
  },
  data () {
    return {
      // companies list from API
      companies: [{ name: '', org_guid: '' }],
      selectedCompany: null,
      provCodes: [
        'BC', 'AB'
      ],

      // company form fields
      companyForm: {
        name: '',
        street_address: '',
        city: '',
        province_state: '',
        postal_code: '',
        main_tel: '',
        fax_tel: '',
        website_url: ''
      },
      companyNotesForm: '',

      // add company success message
      companyAddSuccess: false,
      companyListError: false
    }
  },
  watch: {
    selectedCompany () {
      this.companyForm.name = this.selectedCompany.name || ''
      this.companyForm.street_address = this.selectedCompany.street_address || ''
      this.companyForm.city = this.selectedCompany.city || ''
      this.companyForm.province_state = this.selectedCompany.province_state || ''
      this.companyForm.postal_code = this.selectedCompany.postal_code || ''
      this.companyForm.main_tel = this.selectedCompany.main_tel || ''
      this.companyForm.fax_tel = this.selectedCompany.fax_tel || ''
      this.companyForm.website_url = this.selectedCompany.website_url || ''
    }
  },
  methods: {
    newOrgHandler (orgGuid) {
      this.companyAddSuccess = true
      ApiService.query('organizations/').then((response) => {
        this.companies = response.data
        this.selectedCompany = this.companies.find((company) => company.org_guid === orgGuid)
      }).catch((e) => {
        this.companyListError = e.response
      })
    }
  },
  created () {
    ApiService.query('organizations/').then((response) => {
      this.companies = response.data
    }).catch((e) => {
      this.companyListError = e.response
    })
  }
}
</script>

<style>

</style>
