<template>
  <div class="rounded-lg ml-20 mr-20 bg-white mb-3 px-5">
    <Breadcrumb :model="breadcrumbs"/>
  </div>
  <Card class="rounded-lg ml-20 mr-20 bg-white">
    <template #title>Manage Companies</template>
    <template #content>

      <!-- Company selector (used to select company to edit) -->
      <div class="grid grid-cols-3 gap-4 mb-4">
          <label for="orgEditSelectDropdown">Select a company:
            <v-select
                id="orgEditSelectDropdown"
                :options="companies"
                label="org_verbose_name"
                v-model="selectedCompany"
                placeholder="Begin typing a company name"
                class="mt-2 col-span-3"
                ></v-select>
          </label>
        <Message
          v-if="!!companyListError"
          @close="companyListError=false"
          severity="warn">
          Error retrieving list of companies. Please try again later.
        </Message>
      </div>

      <!-- Add company button (opens 'add company' modal) and success feedback -->
      <div class="flex flex-col mb-5">
        <div>
          <Button
            id="orgAddNewButton"
            @click="showAddModal = true"
            type="button"
            size="small"
            class="mb-5">
          <i class="fa fa-plus-square-o"></i> Add new company</Button>
        <organization-add v-model:visible="showAddModal"  @newOrgAdded="newOrgHandler"></organization-add>
        </div>
      </div>
      <div class="grid grid-flow-col">
        <div class="col-span-12">
          <Message
            severity="success"
            id="orgAddSuccessAlert"
            v-if="companyAddSuccess"
            :closable="true"
            @close="companyAddSuccess=false">
            Company added.
          </Message>
        </div>
      </div>

      <!-- Selected company details and edit form fields -->
      <div class="grid grid-cols-1 gap-4 mb-4">
        <Card class="rounded-lg" v-if="!!selectedCompany">
          <template #content>
            <Form @submit="submitConfirm" @reset="cancelConfirm">
              <h6 class="text-xl font-bold mb-4">Company Information</h6>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="flex flex-col gap-2">
                  <label for="orgEditNameInput">Company name:</label>
                  <InputText
                    type="text"
                    :disabled="!selectedCompany"
                    id="orgEditNameInput"
                    class="w-full md:w-80"
                    v-model="companyForm.name"/>
                </div>
                <div class="flex flex-col gap-2">
                  <label for="orgEditAddressInput">Street address:</label>
                  <InputText
                    type="text"
                    :disabled="!selectedCompany"
                    id="orgEditAddressInput"
                    class="w-full md:w-80"
                    v-model="companyForm.street_address"/>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="flex flex-col gap-2">
                  <label for="orgEditCityInput">City:</label>
                  <InputText
                    :disabled="!selectedCompany"
                    id="orgEditCityInput"
                    type="text"
                    class="w-full md:w-80"
                    v-model="companyForm.city"/>
                </div>
                <div class="flex flex-col gap-2">
                  <label for="orgEditProvinceInput">Province:</label>
                  <Select
                    :disabled="!selectedCompany"
                    id="orgEditProvinceInput"
                    :state="validation.province_state"
                    :options="provinceStateOptions"
                    class="w-full md:w-80"
                    aria-describedby="provInputFeedback"
                    v-model="companyForm.province_state">
                  </Select>
                  <Message id="provInputFeedback" severity="error" v-for="(error, index) in fieldErrors.province_state" :key="`provInput error ${index}`">
                    {{ error }}
                  </Message>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="flex flex-col gap-2">
                  <label for="orgEditPostalInput">Postal code:</label>
                  <InputText
                    :disabled="!selectedCompany"
                    id="orgEditPostalInput"
                    class="w-full md:w-80"
                    v-model="companyForm.postal_code"/>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="flex flex-col gap-2">
                  <label for="orgEditPhoneInput">Office telephone number:</label>
                  <InputMask
                    :disabled="!selectedCompany"
                    id="orgEditPhoneInput"
                    class="w-full md:w-80"
                    mask="(999) 999-9999"
                    v-model="companyForm.main_tel"/>
                </div>
                <div class="flex flex-col gap-2" offset-md="1">
                  <label for="orgEditFaxInput">Fax number:</label>
                  <InputMask
                    :disabled="!selectedCompany"
                    id="orgEditFaxInput"
                    type="text"
                    class="w-full md:w-80"
                    mask="(999) 999-9999"
                    v-model="companyForm.fax_tel"/>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="flex flex-col gap-2">
                  <label for="orgEditEmailInput">Email:</label>
                  <InputText
                      id="orgEditEmailInput"
                      type="text"
                      :state="validation.email"
                      :disabled="!selectedCompany"
                      aria-describedby="orgEditEmailFeedback"
                      class="w-full md:w-80"
                      v-model="companyForm.email"/>
                  <Message id="orgEditEmailFeedback" severity="error" v-for="(error, index) in fieldErrors.email" :key="`urlInput error ${index}`">
                    {{ error }}
                  </Message>
                </div>
                <div class="flex flex-col gap-2" offset-md="1">
                  <label for="orgEditWebsiteInput">Website:</label>
                  <InputText
                    :disabled="!selectedCompany"
                    id="orgEditWebsiteInput"
                    :state="validation.website_url"
                    aria-describedby="orgEditWebsiteFeedback"
                    class="w-full md:w-80"
                    placeholder="eg. http://www.example.com"
                    type="text"
                    v-model="companyForm.website_url"/>
                  <Message id="orgEditWebsiteFeedback" severity="error" v-for="(error, index) in fieldErrors.website_url" :key="`websiteInput error ${index}`">
                    {{ error }}
                  </Message>
                  <div id="orgEditEmailInput">
                    Use a full website address, including http://
                  </div>
                </div>
                <div class="flex flex-col gap-2">
                  <label for="regionOptions">Region:</label>
                  <MultiSelect
                    id="regionOptions"
                    v-model="companyForm.regional_areas"
                    display="chip"
                    :options="regionOptions"
                    optionLabel="name"
                    optionValue="regional_area_guid"
                    filter
                    placeholder="Select Regions"
                    class="w-full md:w-80" />
                </div>
              </div>
              <div class="grid gap-4 grid-cols-2 mb-4">
                <div class="col-span-1">
                  <Button label="Update" type="submit" class="btn btn-primary mr-2" ref="orgUpdateSaveBtn" :disabled="!selectedCompany || !formChanged" />
                  <Button label="Cancel" type="reset" class="btn btn-light" severity="danger" ref="orgUpdateCancelBtn" :disabled="!selectedCompany || !formChanged" />
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <Message class="mt-3" severity="success" id="orgUpdateSuccessAlert" v-if="companyUpdateSuccess" :closable="true" @close="companyUpdateSuccess=false">
                  Successfully updated company information.
                </Message>
              </div>

              <!-- Modals for confirming update/cancel editing -->
                <Dialog
                  id="orgUpdateModal"
                  v-model="confirmSubmitModal"
                  modal
                  header="Confirm update"
                  @shown="focusSubmitModal">
                Are you sure you want to save these changes?
                <template #footer>
                  <Button label="Save" @click="confirmSubmitModal=false;submitForm()" ref="confirmSubmitConfirmBtn" />
                  <Button label="Cancel" severity="Danger" @click="confirmSubmitModal=false" />
                </template>
              </Dialog>
              <Dialog
                  v-model="confirmCancelModal"
                  modal
                  header="Confirm cancel"
                  @shown="focusCancelModal">
                Are you sure you want to discard your changes?
                <template #footer>
                  <Button label="Cancel" severity="secondary" @click="confirmCancelModal=false" ref="cancelSubmitCancelBtn" />
                  <Button label="Discard" severity="danger" @click="confirmCancelModal=false;formReset()" />
                </template>
              </Dialog>
            </Form>
          </template>
        </Card>

        <!-- Company notes -->
        <Card class="rounded-lg" v-if="!!companyDetails">
          <template #content>
            <notes
              ref="notes"
              class="my-3"
              v-if="!!companyDetails"
              type="organization"
              @updated="loadCompanyDetails()"
              :guid="companyDetails.org_guid"
              :record="companyDetails"></notes>
          </template>
        </Card>

        <!-- Change history for this record -->
        <Card class="rounded-lg" v-if="!!selectedCompany">
          <template #content>
            <change-history
              ref="changeHistory"
              class="my-3"
              v-if="!!selectedCompany"
              resource="organization"
              :id="selectedCompany.org_guid"></change-history>
          </template>
        </Card>
      </div>

      <!-- Delete company button and confirmation modals -->
      <div v-if="!!companyDetails">
        <p class="mt-3">
          There {{ companyDetails.registrations_count === 1 ? 'is': 'are' }}
          <span class="font-bold">{{ companyDetails.registrations_count }}</span>
          {{ companyDetails.registrations_count === 1 ? 'registrant': 'registrants' }}
          listed under
          {{ selectedCompany.name }}{{ selectedCompany.name.slice(-1) === '.' ? '' : '.' }}
        </p>
        <DataTable
          v-if="companyRegistrants.length > 0"
          :value="companyRegistrants"
          id="registrants"
          stripedRows
          rowHover
          size="small"
          v-model="companyRegistrants"
          tableStyle="min-width: 50rem"
        >
          <Column field="name" header="Name">
            <template #body="slotProps">
              <router-link :to="{ name: 'PersonDetail', params: { person_guid: slotProps.data.person_guid }}">
                {{ slotProps.data.surname }}, {{ slotProps.data.first_name }}
              </router-link>
            </template>
          </Column>
          <Column field="contact_tel" header="Phone"></Column>
          <Column field="contact_email" header="Email"></Column>
        </DataTable>
        <Button
          label="Delete this company"
          variant="danger"
          severity="danger"
          class="mt-4 mb-4"
          :disabled="companyDetails.registrations_count > 0"
          @click="companyDeleteConfirm()"
        />
        <p v-if="companyDetails.registrations_count > 0" class="delete-company">You must remove all registrants from this company before deleting.</p>
      </div>
      <Dialog
          id="orgDeleteModal"
          v-model="companyDeleteModal"
          modal
          header="Confirm delete"
          @shown="focusDeleteModal">
        Are you sure you want to delete this company?
        <template #footer>
          <Button label="Cancel" severity="secondary" @click="companyDeleteModal=false" ref="companyDeleteCancelBtn" />
          <Button label="Delete" severity="danger" @click="companyDeleteModal=false;companyDelete()" />
        </template>
      </Dialog>
      <Message
        severity="success"
        class="mt-3"
        id="orgDeleteSuccessAlert"
        v-if="!!companyDeleted"
        :closable="true"
        @close="companyDeleted=false">
        {{ companyDeleted }} removed.
      </Message>

    </template>
  </Card>
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
        { label: 'Registry', url: '/registries/' },
        { label: 'Manage Companies' }
      ],

      // to show organizationAdd.vue on button click
      showAddModal: false,

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
