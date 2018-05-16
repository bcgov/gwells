<template>
  <b-container>
    <b-card no-body class="mb-3">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <b-card title="Manage Companies">

      <!-- Add company button (opens 'add company' modal) and success feedback -->
      <b-row>
        <b-col>
          <b-button
              id="addNewOrgButton"
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
        <b-form @submit.prevent="submitConfirm" @reset.prevent="cancelConfirm">
          <b-row>
            <b-col cols="12" md="5">
                <b-form-group
                  id="companyNameInputGroup"
                  label="Company name:"
                  label-for="companyNameInput">
                  <b-form-input
                    :disabled="!selectedCompany"
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
                    :disabled="!selectedCompany"
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
                    :disabled="!selectedCompany"
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
                    :disabled="!selectedCompany"
                    id="companyProvinceInput"
                    :state="validation.province_state"
                    :options="provCodes"
                    aria-describedby="provInputFeedback"
                    v-model="companyForm.province_state">
                    <option value="" disabled>Select a province</option>
                  </b-form-select>
                  <b-form-invalid-feedback id="provInputFeedback">
                    <div v-for="(error, index) in fieldErrors.province_state" :key="`provInput error ${index}`">
                      {{ error }}
                    </div>
                  </b-form-invalid-feedback>
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
                    :disabled="!selectedCompany"
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
                    :disabled="!selectedCompany"
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
                    :disabled="!selectedCompany"
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
                    :disabled="!selectedCompany"
                    id="companyWebsiteInput"
                    :state="validation.website_url"
                    aria-describedby="websiteInputFeedback"
                    type="text"
                    v-model="companyForm.website_url"/>
                  <b-form-invalid-feedback id="websiteInputFeedback">
                      <div v-for="(error, index) in fieldErrors.website_url" :key="`websiteInput error ${index}`">
                        {{ error }}
                      </div>
                  </b-form-invalid-feedback>
                </b-form-group>
            </b-col>
          </b-row>
          <!-- <b-row>
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
          </b-row> -->
          <b-row>
            <b-col>
              <button type="submit" class="btn btn-primary" ref="orgUpdateSaveBtn" :disabled="!selectedCompany || !formChanged">Update</button>
              <button type="reset" class="btn btn-light" ref="orgUpdateCancelBtn" :disabled="!selectedCompany || !formChanged">Cancel</button>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col>
              <b-alert variant="success" :show="companyUpdateSuccess" dismissible @dismissed="companyUpdateSuccess=false">
                Successfully updated company information.
              </b-alert>
            </b-col>
          </b-row>
          <b-modal
              v-model="confirmSubmitModal"
              centered
              title="Confirm save"
              @shown="focusSubmitModal"
              :return-focus="$refs.orgUpdateSaveBtn">
            Are you sure you want to save these changes?
            <div slot="modal-footer">
              <b-btn variant="primary" @click="confirmSubmitModal=false;submitForm()" ref="confirmSubmitConfirmBtn">
                Save
              </b-btn>
              <b-btn variant="light" @click="confirmSubmitModal=false">
                Cancel
              </b-btn>
            </div>
          </b-modal>
          <b-modal
              v-model="confirmCancelModal"
              centered
              title="Confirm cancel"
              @shown="focusCancelModal"
              :return-focus="$refs.orgUpdateCancelBtn">
            Are you sure you want to discard your changes?
            <div slot="modal-footer">
              <b-btn variant="secondary" @click="confirmCancelModal=false" ref="cancelSubmitCancelBtn">
                Cancel
              </b-btn>
              <b-btn variant="danger" @click="confirmCancelModal=false;formReset()">
                Discard
              </b-btn>
            </div>
          </b-modal>
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
      breadcrumbs: [
        {
          text: 'Registry',
          to: { name: 'SearchHome' }
        },
        {
          text: 'Manage Companies',
          active: true
        }
      ],

      // companies list from API
      companies: [{ name: '', org_guid: '', org_verbose_name: '' }],
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

      // add/update company success messages
      companyAddSuccess: false,
      companyUpdateSuccess: false,
      companyListError: false,
      fieldErrors: {},

      // confirm popups
      confirmSubmitModal: false,
      confirmCancelModal: false
    }
  },
  computed: {
    validation () {
      return {
        website_url: (this.fieldErrors.website_url && this.fieldErrors.website_url.length) ? false : null,
        province_state: (this.fieldErrors.province_state && this.fieldErrors.province_state.length) ? false : null
      }
    },
    fieldsChanged () {
      const fields = {}
      if (this.selectedCompany) {
        Object.keys(this.companyForm).forEach((key) => {
          // sets a field as true if it has changed
          // need to convert empty strings to null to compare to null/blank values from API
          fields[key] = ((this.companyForm[key] ? this.companyForm[key] : null) !== this.selectedCompany[key])
        })
      }
      return fields
    },
    formChanged () {
      return (Object.keys(this.fieldsChanged).map(x => this.fieldsChanged[x]).includes(true))
    }
  },
  watch: {
    selectedCompany () {
      // reset form whenever selectedCompany (dropdown)
      this.formReset()
    }
  },
  methods: {
    newOrgHandler (orgGuid) {
      // called when a new company created
      // shows a success message and sets currently selected company to the new one
      this.companyUpdateSuccess = false
      this.companyAddSuccess = true
      this.loadCompanies().then(() => {
        this.selectedCompany = this.companies.find((company) => company.org_guid === orgGuid)
        this.companyAddSuccess = true
      })
    },
    submitConfirm () {
      // popup confirmation for form submit
      // also clear 'company add' success message if it is still active
      this.companyAddSuccess = false
      this.companyUpdateSuccess = false
      this.confirmSubmitModal = true
    },
    submitForm () {
      const data = {}

      // remove null & empty string values, and the guid (not needed in data object)
      Object.keys(this.companyForm).forEach((key) => {
        if (this.companyForm[key] && this.companyForm[key] !== '' && key !== 'org_guid') {
          data[key] = this.companyForm[key]
        }
      })
      ApiService.patch('organizations', this.selectedCompany.org_guid, data).then((response) => {
        this.loadCompanies().then((response) => {
          this.selectedCompany = this.companies.find((company) => company.org_guid === this.selectedCompany.org_guid)
          this.companyUpdateSuccess = true
          this.resetFieldErrors()
        })
      }).catch((error) => {
        this.fieldErrors = error.response.data
      })
    },
    cancelConfirm () {
      // also clear 'company add' success message if it is still active
      this.companyAddSuccess = false
      this.companyUpdateSuccess = false
      this.confirmCancelModal = true
    },
    focusSubmitModal () {
      // focus the "submit" button in the confirm save note popup
      this.$refs.confirmSubmitConfirmBtn.focus()
    },
    focusCancelModal () {
      // focus the "cancel" button in the confirm discard popup
      this.$refs.cancelSubmitCancelBtn.focus()
    },
    formReset () {
      const company = this.selectedCompany || {}
      this.companyForm.name = company.name || ''
      this.companyForm.street_address = company.street_address || ''
      this.companyForm.city = company.city || ''
      this.companyForm.province_state = company.province_state || ''
      this.companyForm.postal_code = company.postal_code || ''
      this.companyForm.main_tel = company.main_tel || ''
      this.companyForm.fax_tel = company.fax_tel || ''
      this.companyForm.website_url = company.website_url || ''
      this.resetFieldErrors()
    },
    resetFieldErrors () {
      this.fieldErrors = {}
    },
    loadCompanies () {
      // load full list of companies when page loads (for dropdown picker)
      return ApiService.query('organizations/').then((response) => {
        this.companies = response.data
      }).catch((e) => {
        this.companyListError = e.response
      })
    }
  },
  created () {
    this.loadCompanies()
  }
}
</script>

<style>

</style>
