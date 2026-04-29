<template>
  <Dialog id="orgAddModal" :visible="visible" modal header="Add a Company" @update:visible="$emit('update:visible', $event)" @shown="focusInput()" :style="{ width: '50rem' }">
    <div class="col-span-12" v-if="error">
      <api-error :error="error" :on-clear="() => registryStore.setError(null)"></api-error>
    </div>

    <!-- form body and inputs -->
    <Form @submit="onFormSubmit()" @reset="onFormReset()">
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label for="orgAddNameInput">Company name:</label>
          <InputText
            type="text"
            id="orgAddNameInput"
            v-model="orgForm.name"
            required
            class="w-full md:w-80"
            ref="orgAddNameInput"/>
        </div>
        <div class="flex flex-col gap-2">
          <label for="orgAddAddressInput">Street address:</label>
          <InputText
            type="text"
            id="orgAddAddressInput"
            class="w-full md:w-80"
            v-model="orgForm.street_address"/>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4 mb-4">
        <div class="flex flex-col">
          <label for="orgAddCityInput">City:</label>
          <InputText
            type="text"
            id="orgAddCityInput"
            class="w-full md:w-80"
            v-model="orgForm.city"/>
        </div>
        <div>
          <label for="orgAddProvinceInput">Province:</label>
          <div class="w-full md:w-80">
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
            <Message id="orgAddProvinceFeedback" class="p-error" v-for="(error, index) in fieldErrors.province_state" :key="`urlInput error ${index}`" severity="error">
              {{ error }}
            </Message>
          </div>
        </div>
        <div>
          <label for="orgAddPostalInput">Postal code:</label>
          <InputText
            type="text"
            id="orgAddPostalInput"
            class="w-full md:w-80"
            v-model="orgForm.postal_code"/>
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label for="orgAddPhoneInput">Office telephone number:</label>
          <InputMask
            type="text"
            id="orgAddPhoneInput"
            class="w-full md:w-80"
            mask="(999) 999-9999"
            v-model="orgForm.main_tel"/>
        </div>
        <div>
          <label for="orgAddFaxInput">Fax number:</label>
          <InputMask
            type="text"
            id="orgAddFaxInput"
            class="w-full md:w-80"
            mask="(999) 999-9999"
            v-model="orgForm.fax_tel"/>
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div class="flex flex-col">
          <label for="orgAddEmailInput">Email:</label>
          <InputText
            id="orgAddEmailInput"
            type="text"
            :state="validation.email"
            aria-describedby="orgAddEmailFeedback"
            class="w-full md:w-80"
            v-model="orgForm.email"/>
            <Message v-for="(error, index) in fieldErrors.email" :key="`urlInput error ${index}`" severity="error">
              {{ error }}
            </Message>
        </div>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label for="orgAddWebsiteInput">Website:</label>
            <InputText
                id="orgAddWebsiteInput"
                type="text"
                :state="validation.website_url"
                aria-describedby="orgAddWebsiteFeedback websiteInputHelp"
                class="w-full md:w-80"
                v-model="orgForm.website_url"
                placeholder="e.g.: http://www.example.com"/>
              <Message v-for="(error, index) in fieldErrors.website_url" :key="`urlInput error ${index}`" severity="error">
                {{ error }}
              </Message>
            <p class="w-full md:w-80 text-sm">
              Use a full website address, including http://
            </p>
          </div>
        </div>
      </div>
      <div class="mt-3 grid grid-cols-12 gap-4">
        <div class="col-span-12">
          <Button label="save" type="submit" class="mr-2" :disabled="orgSubmitLoading" />
          <Button label="cancel" type="button" severity="secondary" id="orgAddFormResetButton" @click="cancelConfirm"/>
        </div>
      </div>
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
  </Dialog>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { useRegistryStore } from '@/stores/registry.js'

export default {
  name: 'OrganizationAdd',
  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:visible', 'newOrgAdded'],
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
        this.$emit('update:visible', false)
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
      this.orgForm = {
        name: '',
        street_address: '',
        city: '',
        province_state: null,
        postal_code: '',
        email: '',
        main_tel: '',
        fax_tel: '',
        website_url: ''
      }
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
    cancelConfirm () {
      this.resetFieldErrors()
      this.onFormReset()
      this.$emit('update:visible', false)
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
