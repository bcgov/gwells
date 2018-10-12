<template>
  <b-modal id="orgAddModal" title="Add a Company" hide-footer @shown="focusInput()">
    <div class="col-xs-12" v-if="error">
      <api-error :error="error" resetter="SET_ERROR"></api-error>
    </div>
    <div class="container">
        <b-form autocomplete="off" @submit.prevent="onFormSubmit()" @reset.prevent="onFormReset()">
          <b-row>
            <b-col cols="12">
              <b-form-group
                label="Company name:"
                label-for="orgAddNameInput">
                <b-form-input
                    id="orgAddNameInput"
                    type="text"
                    v-model="orgForm.name"
                    required
                    ref="orgAddNameInput"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col cols="12">
              <b-form-group
                label="Street address:"
                label-for="orgAddAddressInput">
                <b-form-input
                    id="orgAddAddressInput"
                    type="text"
                    v-model="orgForm.street_address"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="6">
              <b-form-group
                label="City:"
                label-for="orgAddCityInput">
                <b-form-input
                    id="orgAddCityInput"
                    type="text"
                    v-model="orgForm.city"/>
              </b-form-group>
            </b-col>
            <b-col cols="12" md="6">
              <b-form-group
                label="Province/State:"
                label-for="orgAddProvinceInput">
                <b-form-select
                  id="orgAddProvinceInput"
                  :options="provinceStateOptions"
                  v-model="orgForm.province_state"
                  :state="validation.province_state"
                  required>
                  <template slot="first">
                    <option :value="''" disabled>Select a province</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback id="orgAddProvinceFeedback">
                  <div v-for="(error, index) in fieldErrors.province_state" :key="`urlInput error ${index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="6">
              <b-form-group
                label="Postal code:"
                label-for="orgAddPostalInput">
                <b-form-input
                    id="orgAddPostalInput"
                    type="text"
                    v-model="orgForm.postal_code"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col cols="12" md="6">
              <b-form-group
                label="Telephone:"
                label-for="orgAddPhoneInput">
                <b-form-input
                    id="orgAddPhoneInput"
                    type="text"
                    :formatter="formatTel"
                    lazy-formatter
                    v-model="orgForm.main_tel"/>
              </b-form-group>
            </b-col>
            <b-col cols="12" md="6">
              <b-form-group
                label="Fax number:"
                label-for="orgAddFaxInput">
                <b-form-input
                    id="orgAddFaxInput"
                    type="text"
                    :formatter="formatTel"
                    lazy-formatter
                    v-model="orgForm.fax_tel"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="6">
              <b-form-group
                label="Email:"
                label-for="orgAddEmailInput">
                <b-form-input
                    id="orgAddEmailInput"
                    type="text"
                    :state="validation.email"
                    aria-describedby="orgAddEmailFeedback"
                    v-model="orgForm.email"/>
                <b-form-invalid-feedback>
                  <div v-for="(error, index) in fieldErrors.email" :key="`urlInput error ${index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col cols="12" md="6">
              <b-form-group
                label="Website:"
                label-for="orgAddWebsiteInput">
                <b-form-input
                    id="orgAddWebsiteInput"
                    type="text"
                    :state="validation.website_url"
                    aria-describedby="orgAddWebsiteFeedback websiteInputHelp"
                    v-model="orgForm.website_url"
                    placeholder="e.g.: http://www.example.com"/>
                <b-form-invalid-feedback>
                  <div v-for="(error, index) in fieldErrors.website_url" :key="`urlInput error ${index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
                <b-form-text>
                  Use a full website address, including http://
                </b-form-text>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="my-3">
            <b-col>
              <b-button type="submit" class="mr-2" variant="primary" :disabled="orgSubmitLoading">Save</b-button>
              <b-button type="reset" variant="light" id="orgAddFormResetButton">Cancel</b-button>
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
import inputFormatMixin from '@/common/inputFormatMixin.js'
import { FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'

export default {
  name: 'OrganizationAdd',
  mixins: [inputFormatMixin],
  data () {
    return {
      orgForm: {
        name: '',
        street_address: '',
        city: '',
        province_state: '',
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
    ...mapGetters(['error', 'provinceStateOptions'])
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
        province_state: '',
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
    }
  },
  created () {
    this.resetFieldErrors()
    this.$store.dispatch(FETCH_DRILLER_OPTIONS)
  }
}
</script>

<style>

</style>
