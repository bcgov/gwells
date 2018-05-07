<template>
  <div>
    <div v-if="section === 'company' && !!record">
      <b-form @submit.prevent="submitCompanyForm">
        <b-form-group
          id="companyInputGroup"
          :label="`${record.activity_description} company:`"
          label-for="companyInput"
          >
          <v-select
            id="companyInput"
            v-model="registrationCompanyForm.organization"
            :options="companies"
            placeholder="Begin typing a company name"
            label="name"
            />
        </b-form-group>
        <button type="submit" class="btn btn-primary">Submit</button>
        <button type="button" class="btn btn-light" @click="$emit('canceled')">Cancel</button>
      </b-form>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'

export default {
  name: 'PersonDetailEdit',
  components: {
    'api-error': APIErrorMessage
  },
  props: ['section', 'record'],
  data () {
    return {
      personalInfoForm: {},
      contactInfoForm: {},
      registrationCompanyForm: {},
      companies: []
    }
  },
  computed: {
    ...mapGetters([
      'error',
      'currentDriller'
    ])
  },
  methods: {
    formReset () {
      /**
       * populate form fields from the currentDriller object in store
       * fields are split up into 3 groups (personal info, contact info and affiliated companies).
       */

      // copy current person object from store
      const personData = JSON.parse(JSON.stringify(this.currentDriller))

      this.personalInfoForm = {}
      this.contactInfoForm = {}
      this.registrationCompanyForm = {
        organization: null
      }

      this.personalInfoForm.first_name = personData.first_name
      this.personalInfoForm.surname = personData.surname

      // add contact info
      if (personData.contact_info) {
        this.contactInfoForm = personData.contact_info
      }

      // add company info (for the registration record defined by prop 'record' only)
      if (this.record && this.record.organization) {
        this.registrationCompanyForm.organization = {
          name: this.record.organization.name,
          org_guid: this.record.organization.org_guid
        }
      }
    },
    submitCompanyForm () {
      const regGuid = this.record.register_guid
      const data = { organization: this.registrationCompanyForm.organization.org_guid }
      ApiService.patch('registrations', regGuid, data).then(() => {
        this.$emit('updated', true)
      })
    }
  },
  created () {
    this.formReset()
    if (this.section === 'company') {
      ApiService.query('organizations/names/').then((response) => {
        this.companies = response.data
      }).catch(() => {
        this.orgListError = 'Unable to retrieve organization list.'
      })
    }
  }
}
</script>

<style>
</style>
