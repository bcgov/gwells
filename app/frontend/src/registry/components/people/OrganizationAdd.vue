<template>
  <Dialog id="orgAddModal" v-model:visible="visible" modal header="Add a Company" hide-footer @shown="focusInput()">
    <div class="col-xs-12" v-if="error">
      <api-error :error="error" :on-clear="() => registryStore.setError(null)"></api-error>
    </div>
    <div class="container">
        <Form @submit.prevent="onFormSubmit()" @reset.prevent="onFormReset()">
          <tr>
            <td cols="12">
              <label
                for="orgAddNameInput">Company name:
                <InputText
                    type="text"
                    id="orgAddNameInput"
                    v-model="orgForm.name"
                    required
                    ref="orgAddNameInput"/>
              </label>
            </td>
          </tr>
          <tr class="mt-3">
            <td cols="12">
              <label for="orgAddAddressInput">Street address:
                <InputText
                    type="text"
                    id="orgAddAddressInput"
                    v-model="orgForm.street_address"/>
              </label>
            </td>
          </tr>
          <tr>
            <td cols="12" md="6">
              <label for="orgAddCityInput">City:
                <InputText
                    type="text"
                    id="orgAddCityInput"
                    v-model="orgForm.city"/>
              </label>
            </td>
            <td cols="12" md="6">
              <label for="orgAddProvinceInput">Province:
                <Select
                  id="orgAddProvinceInput"
                  :options="provinceStateOptions"
                  v-model="orgForm.province_state"
                  :state="validation.province_state"
                  :class="{ 'p-invalid': fieldErrors.province_state }"
                  required>
                  <template v-slot:first>
                    <option :value="null" disabled>Select a province</option>
                  </template>
                </Select>
                <Message id="orgAddProvinceFeedback" class="p-error" v-if="fieldErrors.province_state">
                  <div v-for="(error, index) in fieldErrors.province_state" :key="`urlInput error ${index}`">
                    {{ error }}
                  </div>
                </Message>
              </label>
            </td>
          </tr>
          <tr>
            <td cols="12" md="6">
              <label for="orgAddPostalInput">Postal code:
                <InputText
                  type="text"
                  id="orgAddPostalInput"
                  v-model="orgForm.postal_code"/>
              </label>
            </td>
          </tr>
          <tr class="mt-3">
            <td cols="12" md="6">
              <label for="orgAddPhoneInput">Office telephone number:
                <InputMask
                    type="text"
                    id="orgAddPhoneInput"
                    mask="(999) 999-9999"
                    v-model="orgForm.main_tel"/>
              </label>
            </td>
            <td cols="12" md="6">
              <label for="orgAddFaxInput">Fax number:
                <InputMask
                    type="text"
                    id="orgAddFaxInput"
                    mask="(999) 999-9999"
                    v-model="orgForm.fax_tel"/>
              </label>
            </td>
          </tr>
          <tr>
            <td cols="12" md="6">
              <label for="orgAddEmailInput">Email:
                <InputText
                    id="orgAddEmailInput"
                    type="text"
                    :state="validation.email"
                    aria-describedby="orgAddEmailFeedback"
                    v-model="orgForm.email"/>
                  <Message v-for="(error, index) in fieldErrors.email" :key="`urlInput error ${index}`" severity="error">
                    {{ error }}
                  </Message>
              </label>
            </td>
            <td cols="12" md="6">
              <label for="orgAddWebsiteInput">Website:
                <InputText
                    id="orgAddWebsiteInput"
                    type="text"
                    :state="validation.website_url"
                    aria-describedby="orgAddWebsiteFeedback websiteInputHelp"
                    v-model="orgForm.website_url"
                    placeholder="e.g.: http://www.example.com"/>
                  <Message v-for="(error, index) in fieldErrors.website_url" :key="`urlInput error ${index}`" severity="error">
                    {{ error }}
                  </Message>
                <div>
                  Use a full website address, including http://
                </div>
              </label>
            </td>
          </tr>
          <tr class="my-3">
            <td>
              <Button label="save" type="submit" class="mr-2" severity="primary" :disabled="orgSubmitLoading" />
              <Button label="cancel" type="reset" id="orgAddFormResetButton" />
            </td>
          </tr>
        </Form>
        <Message v-if="!!orgSubmitError" variant="warning" severity="warn">
          Error creating a new company.
          <div v-for="(value, key, index) in orgSubmitError.data" :key="`submit error ${index}`">
              <span class="text-capitalize">{{ key }}</span>:
              <span
                v-for="(msg, msgIndex) in value"
                :key="`submit error msg ${index} ${msgIndex}`">{{ msg }} </span>
            </div>
        </Message>
    </div>
  </Dialog>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { useRegistryStore } from '@/stores/registry.js'

export default {
  name: 'OrganizationAdd',
  data () {
    return {
      registryStore: useRegistryStore(),
      orgForm: {
        name: '',
        street_address: '',
        city: '',
        province_state: null,
        postal_code: '',
        email: '',
        main_tel: '',
        fax_tel: '',
        website_url: ''
      },
      orgSubmitLoading: false,
      orgSubmitError: null,
      fieldErrors: {
        province_state: [],
        website_url: []
      }
    }
  },
  computed: {
    validation () {
      return {
        province_state: (this.fieldErrors.province_state && this.fieldErrors.province_state.length) ? false : null,
        website_url: (this.fieldErrors.website_url && this.fieldErrors.website_url.length) ? false : null,
        email: (this.fieldErrors.email && this.fieldErrors.email.length) ? false : null
      }
    },
    error () { return this.registryStore.error },
    provinceStateOptions () { return this.registryStore.provinceStateOptions }
  },
  methods: {
    onFormSubmit () {
      this.resetFieldErrors()
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
        this.$root.$emit('bv::hide::modal', 'orgAddModal')
        this.$emit('newOrgAdded', response.data.org_guid)
      }).catch((e) => {
        this.orgSubmitLoading = false
        const errors = e.response.data

        for (const field in errors) {
          this.fieldErrors[field] = errors[field]
        }
      })
    },
    onFormReset () {
      this.orgForm = Object.assign({}, {
        name: '',
        street_address: '',
        city: '',
        province_state: null,
        postal_code: '',
        email: '',
        main_tel: '',
        fax_tel: '',
        website_url: ''
      })
      this.$root.$emit('bv::hide::modal', 'orgAddModal')
    },
    focusInput () {
      this.$refs.orgAddNameInput.focus()
    },
    resetFieldErrors () {
      this.fieldErrors = {
        contact_email: [],
        province_state: [],
        website_url: [],
        email: []
      }
    },
  },
  created () {
    this.resetFieldErrors()
    this.registryStore.fetchDrillerOptions()
  }
}
</script>

<style>

</style>
