<template>
  <div class="p-1 p-md-3">
    <Card no-body class="mb-3">
      <Breadcrumb :model="breadcrumbs" class="py-0 my-2"></Breadcrumb>
    </Card>
    <Card title="Manage Companies">

      <!-- Company selector (used to select company to edit) -->
      <tr>
        <td cols="12" md="7">
          <label for="orgEditSelectDropdown">Select a company:
            <v-select
                id="orgEditSelectDropdown"
                :options="companies"
                label="org_verbose_name"
                v-model="selectedCompany"
                placeholder="Begin typing a company name"
                ></v-select>
          </label>
        </td>
        <td cols="12" md="5">
          <Message variant="warning" :show="!!companyListError" @dismissed="companyListError=false" severity="warn">
            Error retrieving list of companies. Please try again later.
          </Message>
        </td>
      </tr>

      <!-- Add company button (opens 'add company' modal) and success feedback -->
      <tr>
        <td>
          <Button
            id="orgAddNewButton"
            type="button"
            label="Add new company"
            v-b-modal.orgAddModal
            size="sm"
            class="mb-5"
          />
          <organization-add @newOrgAdded="newOrgHandler"></organization-add>
        </td>
      </tr>
      <tr>
        <td>
          <Message variant="success" severity="success" id="orgAddSuccessAlert" :show="companyAddSuccess" dismissible @dismissed="companyAddSuccess=false">Company added.</Message>
        </td>
      </tr>

      <!-- Selected company details and edit form fields -->
      <Card no-body class="p-2 p-md-3" v-if="!!selectedCompany">
        <h6 class="card-subtitle mb-3">Company Information</h6>
        <Form @submit.prevent="submitConfirm" @reset.prevent="cancelConfirm">
          <tr>
            <td cols="12" md="5">
                <label for="orgEditNameInput">Company name:
                  <InputText
                    type="text"
                    :disabled="!selectedCompany"
                    id="orgEditNameInput"
                    v-model="companyForm.name"/>
                </label>
            </td>
            <td cols="12" md="5" offset-md="1">
              <label for="orgEditAddressInput">Street address:
                <InputText
                  :disabled="!selectedCompany"
                  id="orgEditAddressInput"
                  type="text"
                  v-model="companyForm.street_address"/>
              </label>
            </td>
          </tr>
          <tr>
            <td cols="12" md="5">
                <label for="orgEditCityInput">City:
                  <InputText
                    :disabled="!selectedCompany"
                    id="orgEditCityInput"
                    type="text"
                    v-model="companyForm.city"/>
                </label>
            </td>
            <td cols="12" md="5" offset-md="1">
              <label for="orgEditProvinceInput">Province:
                <Select
                  :disabled="!selectedCompany"
                  id="orgEditProvinceInput"
                  :state="validation.province_state"
                  :options="provinceStateOptions"
                  aria-describedby="provInputFeedback"
                  v-model="companyForm.province_state">
                </Select>
                <Message id="provInputFeedback" severity="error" v-for="(error, index) in fieldErrors.province_state" :key="`provInput error ${index}`">
                  {{ error }}
                </Message>
              </label>
            </td>
          </tr>
          <tr>
            <td cols="12" md="5">
              <label for="orgEditPostalInput">Postal code:
                <InputText
                  :disabled="!selectedCompany"
                  id="orgEditPostalInput"
                  v-model="companyForm.postal_code"/>
              </label>
            </td>
          </tr>
          <tr class="mt-4">
            <td cols="12" md="5">
              <label for="orgEditPhoneInput">Office telephone number:
                <InputMask
                  :disabled="!selectedCompany"
                  id="orgEditPhoneInput"
                  mask="(999) 999-9999"
                  v-model="companyForm.main_tel"/>
              </label>
            </td>
            <td cols="12" md="5" offset-md="1">
              <label for="orgEditFaxInput">Fax number:
                <InputMask
                  :disabled="!selectedCompany"
                  id="orgEditFaxInput"
                  type="text"
                  mask="(999) 999-9999"
                  v-model="companyForm.fax_tel"/>
              </label>
            </td>
          </tr>
          <tr>
            <td cols="12" md="5">
              <label for="orgEditEmailInput">Email:
                <InputText
                    id="orgEditEmailInput"
                    type="text"
                    :state="validation.email"
                    :disabled="!selectedCompany"
                    aria-describedby="orgEditEmailFeedback"
                    v-model="companyForm.email"/>
                <Message id="orgEditEmailFeedback" severity="error" v-for="(error, index) in fieldErrors.email" :key="`urlInput error ${index}`">
                  {{ error }}
                </Message>
              </label>
            </td>
            <td cols="12" md="5" offset-md="1">
              <label for="orgEditWebsiteInput">Website:
                <InputText
                  :disabled="!selectedCompany"
                  id="orgEditWebsiteInput"
                  :state="validation.website_url"
                  aria-describedby="orgEditWebsiteFeedback"
                  placeholder="eg. http://www.example.com"
                  type="text"
                  v-model="companyForm.website_url"/>
                <Message id="orgEditWebsiteFeedback" severity="error" v-for="(error, index) in fieldErrors.website_url" :key="`websiteInput error ${index}`">
                  {{ error }}
                </Message>
                <div id="orgEditEmailInput">
                  Use a full website address, including http://
                </div>
              </label>
            </td>
            <td cols="12" md="12">
              <label for="regionOptions">Region:
                <MultiSelect
                  name="regionOptions"
                  v-model="companyForm.regional_areas"
                  :options="regionOptions"
                  optionLabel="regionOptions"
                  optionValue="regional_area_guid"
                  filter
                  class="mb-3" />
              </label>
            </td>
          </tr>
          <tr class="mt-3">
            <td>
              <Button label="Update" type="submit" class="btn btn-primary" ref="orgUpdateSaveBtn" :disabled="!selectedCompany || !formChanged" />
              <Button label="Cancel" type="reset" class="btn btn-light" severity="danger" ref="orgUpdateCancelBtn" :disabled="!selectedCompany || !formChanged" />
            </td>
          </tr>
          <tr>
            <td>
              <Message class="mt-3" variant="success" severity="success" id="orgUpdateSuccessAlert" :show="companyUpdateSuccess" dismissible @dismissed="companyUpdateSuccess=false">
                Successfully updated company information.
              </Message>
            </td>
          </tr>

          <!-- Modals for confirming update/cancel editing -->
           <Dialog
              id="orgUpdateModal"
              v-model="confirmSubmitModal"
              v-model:visible="visible"
              centered
              modal
              header="Confirm update"
              @shown="focusSubmitModal"
              :return-focus="$refs.orgUpdateSaveBtn">
            Are you sure you want to save these changes?
            <div slot="modal-footer">
              <Button label="Save" variant="primary" @click="confirmSubmitModal=false;submitForm()" ref="confirmSubmitConfirmBtn" />
              <Button label="Cancel" severity="Danger" variant="light" @click="confirmSubmitModal=false" />
            </div>
          </Dialog>
          <Dialog
              v-model="confirmCancelModal"
              v-model:visible="visible"
              centered
              modal
              header="Confirm cancel"
              @shown="focusCancelModal"
              :return-focus="$refs.orgUpdateCancelBtn">
            Are you sure you want to discard your changes?
            <div slot="modal-footer">
              <Button label="Cancel" variant="secondary" severity="secondary" @click="confirmCancelModal=false" ref="cancelSubmitCancelBtn" />
              <Button label="Discard" variant="danger" severity="danger" @click="confirmCancelModal=false;formReset()" />
            </div>
          </Dialog>
        </Form>
      </Card>

      <!-- Company notes -->
      <notes
          class="mt-3"
          v-if="!!companyDetails"
          type="organization"
          @updated="loadCompanyDetails()"
          :guid="companyDetails.org_guid"
          :record="companyDetails"></notes>

      <!-- Change history for this record -->
      <change-history
          ref="changeHistory"
          class="my-3"
          v-if="!!selectedCompany"
          resource="organization"
          :id="selectedCompany.org_guid"></change-history>

      <!-- Delete company button and confirmation modals -->
      <div v-if="!!companyDetails">
        <p class="mt-3">
          There {{ companyDetails.registrations_count === 1 ? 'is': 'are' }}
          <span class="font-weight-bold">{{ companyDetails.registrations_count }}</span>
          {{ companyDetails.registrations_count === 1 ? 'registrant': 'registrants' }}
          listed under
          {{ selectedCompany.name }}{{ selectedCompany.name.slice(-1) === '.' ? '' : '.' }}
        </p>
        <DataTable
          v-if="companyRegistrants.length > 0"
          id="registrants"
          stripedRows
          rowhover
          size="small"
          :value="companyRegistrants"
          tableStyle="min-width: 50rem"
        >
          <Column field="name" header="Name">
            <template>
              <router-link :to="{ name: 'PersonDetail', params: { person_guid: row.item.person_guid }}">{{ row.item.surname }}, {{ row.item.first_name }}</router-link>
          </template>
          </Column>
          <Column field="contact_tel" header="contact_tel"></Column>
          <Column field="contact_email" header="contact_email"></Column>
        </DataTable>
        <Button
          label="Delete this company"
          variant="danger"
          severity="danger"
          :disabled="companyDetails.registrations_count > 0"
          @click="companyDeleteConfirm()"
        />
        <p v-if="companyDetails.registrations_count > 0" class="delete-company">You must remove all registrants from this company before deleting.</p>
      </div>
      <Dialog
          id="orgDeleteModal"
          v-model="companyDeleteModal"
          v-model:visible="visible"
          centered
          modal
          header="Confirm delete"
          @shown="focusDeleteModal"
          :return-focus="$refs.orgDeleteBtn">
        Are you sure you want to delete this company?
        <div slot="modal-footer">
          <Button label="Cancel" severity="secondary" @click="companyDeleteModal=false" ref="companyDeleteCancelBtn" />
          <Button label="Delete" severity="danger" @click="companyDeleteModal=false;companyDelete()" />
        </div>
      </Dialog>
      <Message severity="success" class="mt-3" id="orgDeleteSuccessAlert" :show="!!companyDeleted" dismissible @dismissed="companyDeleted=false">
          {{ companyDeleted }} removed.
      </Message>
    </Card>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'
import Notes from '@/registry/components/people/Notes.vue'
import ChangeHistory from '@/common/components/ChangeHistory.vue'
import { useRegistryStore } from '@/stores/registry.js'

export default {
  name: 'OrganizationEdit',
  components: {
    OrganizationAdd,
    Notes,
    ChangeHistory
  },
  data () {
    return {
      registryStore: useRegistryStore(),
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

      // company details from API (loaded after selecting a company)
      companyDetails: null,
      companyRegistrants: [],
      // company form fields
      companyForm: {
        name: '',
        street_address: '',
        city: '',
        province_state: null,
        postal_code: '',
        email: '',
        main_tel: '',
        fax_tel: '',
        website_url: '',
        regional_areas: []
      },
      companyNotesForm: '',

      // add/update company success messages
      companyAddSuccess: false,
      companyUpdateSuccess: false,
      companyListError: false,
      companyDeleted: false,
      companyDeleteError: false,
      fieldErrors: {},

      // confirm popups
      confirmSubmitModal: false,
      confirmCancelModal: false,
      companyDeleteModal: false
    }
  },
  computed: {
    validation () {
      return {
        website_url: (this.fieldErrors.website_url && this.fieldErrors.website_url.length) ? false : null,
        province_state: (this.fieldErrors.province_state && this.fieldErrors.province_state.length) ? false : null,
        email: (this.fieldErrors.email && this.fieldErrors.email.length) ? false : null
      }
    },
    fieldsChanged () {
      // check if any of the company detail input fields changed (to toggle update/cancel buttons)
      // returns an object containing each field, and true/false if value changed or not

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
      // returns true or false if any of the fields changed. Uses fieldsChanged() method above
      return (Object.keys(this.fieldsChanged).map(x => this.fieldsChanged[x]).includes(true))
    },
    provinceStateOptions () { return this.registryStore.provinceStateOptions },
    regionOptions () { return this.registryStore.regionOptions }
  },
  watch: {
    selectedCompany (val) {
      // reset form whenever selectedCompany (dropdown) changes
      this.formReset()

      // fetch extra company data
      this.companyDetails = null
      if (val) {
        this.loadCompanyDetails()
      }
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
      // submits a PATCH request to API with the updated company details

      const data = {}

      // remove null & empty string values, and the guid (not needed in data object)
      Object.keys(this.companyForm).forEach((key) => {
        if (key !== 'org_guid') {
          data[key] = this.companyForm[key]
        }
      })
      ApiService.patch('organizations', this.selectedCompany.org_guid, data).then((response) => {
        // after successful request, load the company list again
        this.loadCompanies().then((response) => {
          this.selectedCompany = this.companies.find((company) => company.org_guid === this.selectedCompany.org_guid)
          this.companyUpdateSuccess = true
          this.resetFieldErrors()
        })
      }).catch((error) => {
        // if any field errors are returned by the API (e.g. website_url: ['Enter a valid address']), store them
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
    focusDeleteModal () {
      this.$refs.companyDeleteCancelBtn.focus()
    },
    formReset () {
      // reset all company edit form fields (with default values)
      const company = this.selectedCompany || {}
      this.companyForm.name = company.name || ''
      this.companyForm.street_address = company.street_address || ''
      this.companyForm.city = company.city || ''
      this.companyForm.province_state = company.province_state || null
      this.companyForm.postal_code = company.postal_code || ''
      this.companyForm.email = company.email || ''
      this.companyForm.main_tel = company.main_tel || ''
      this.companyForm.fax_tel = company.fax_tel || ''
      this.companyForm.website_url = company.website_url || ''
      this.companyForm.regional_areas = company.regional_areas || []
      this.resetFieldErrors()
    },
    resetFieldErrors () {
      this.fieldErrors = {}
    },
    loadCompanies () {
      // load full list of companies when page loads (for dropdown picker)
      return ApiService.query('organizations').then((response) => {
        this.companies = response.data
      }).catch((e) => {
        this.companyListError = e.response
      })
    },
    loadCompanyDetails () {
      // List of companies only contains basic details. When one is selected, get the full set of details
      // plus all notes for that company
      ApiService.get('organizations', this.selectedCompany.org_guid)
        .then((response) => {
          this.companyRegistrants = []
          this.companyDetails = response.data
          // Fetch data on Registrants
          ApiService.query(`drillers?search=${encodeURIComponent(this.companyDetails.name)}`)
            .then(({ data }) => {
              this.companyRegistrants = data.results
            })
        }).catch((e) => {
          this.companyListError = e.response.data
        })

      // update changeHistory when company is updated
      if (this.$refs.changeHistory) {
        this.$refs.changeHistory.update()
      }
    },
    companyDeleteConfirm () {
      this.companyDeleteModal = true
    },
    companyDelete () {
      // after confirmation received via popup, clear any success messages and send delete request
      return ApiService.delete('organizations', this.selectedCompany.org_guid).then((response) => {
        this.companyDeleted = this.selectedCompany.name
        this.selectedCompany = null
        this.companyUpdateSuccess = false
        this.companyAddSuccess = false
        this.loadCompanies()
      }).catch((e) => {
        this.companyDeleteError = e.response.data
      })
    },
  },
  created () {
    this.loadCompanies()
    this.registryStore.fetchDrillerOptions()
  }
}
</script>

<style>
  .delete-company {
    margin: 0.25em 0;
  }
  button:disabled {
    cursor: not-allowed
  }
</style>
