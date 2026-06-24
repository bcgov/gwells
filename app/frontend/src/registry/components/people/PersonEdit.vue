<template>
  <div>

    <!-- Person details -->
    <div v-if="section === 'person' || section === 'all'">
      <Form @submit="submitPersonForm" @reset="formReset">
        <responsive-grid :cols="6" gap="6" class="mb-4">
          <label
            id="surnameInputGroup"
            for="surnameInput">Surname:
            <InputText
              id="surnameInput"
              v-model="personalInfoForm.surname"
              required/>
          </label>
          <label
            id="firstnameInputGroup"
            for="firstnameInput">First name:
            <InputText
              id="firstnameInput"
              v-model="personalInfoForm.first_name"
              required/>
          </label>
        </responsive-grid>
        <responsive-grid :cols="6" gap="6" class="mb-4">
          <label
            id="drillOrcsInputGroup"
            for="drillORCSInput">Well Driller ORCS:
            <InputText
              id="drillORCSInput"
              v-model="personalInfoForm.well_driller_orcs_no"/>
            <div id="drillerORCSExample" class="text-sm">
              ORCS format: 38000-25/DRI XXXX X
            </div>
          </label>
          <label
            id="pumpORCSInputGroup"
            for="pumpORCSInput">Pump installer ORCS:
            <InputText
              id="pumpORCSInput"
              v-model="personalInfoForm.pump_installer_orcs_no"/>
            <div id="pumpORCSExample" class="text-sm">
              ORCS format: 38000-25/PUMP XXXX X
            </div>
          </label>
        </responsive-grid>
        <div class="mt-4 flex gap-2">
          <Button label="Save" type="submit"/>
          <Button label="Cancel" type="button" severity="secondary" @click="$emit('canceled')" />
        </div>
      </Form>
    </div>

    <!-- Contact information -->
    <div v-if="(section === 'contact' || section === 'all')">
      <Form @submit="submitContactForm">
        <responsive-grid :cols="4" gap="6" class="mb-4">
          <label
            id="emailInputGroup"
            for="emailInput">Email Address:
            <InputText
              id="emailInput"
              type="email"
              :state="validation.contact_email"
              aria-describedby="emailInputFeedback"
              v-model="contactInfoForm.contact_email"/>
            <Message severity="error" id="emailInputFeedback" v-for="(error, index) in fieldErrors.contact_email" :key="`emailInput error ${index}`">
              {{ error }}
            </Message>
          </label>
          <label
            id="telInputGroup"
            for="telInput">Telephone:
            <InputMask
              id="telInput"
              type="tel"
              mask="(999) 999-9999"
              v-model="contactInfoForm.contact_tel"/>
          </label>
          <label
            id="cellInputGroup"
            for="cellInput">Cell:
            <InputMask
              id="cellInput"
              type="tel"
              mask="(999) 999-9999"
              v-model="contactInfoForm.contact_cell"/>
          </label>
        </responsive-grid>
        <div class="mt-4 flex gap-2">
          <Button label="Save" type="submit"/>
          <Button label="Cancel" type="button" severity="secondary" @click="$emit('canceled')" />
        </div>
      </Form>
    </div>

    <!-- Company -->
    <div v-if="(section === 'company' || section === 'all') && !!record">
      <Form @submit="submitCompanyForm">
        <label id="companyInputGroup" for="companyInput">{{record.activity_description}} company:
          <Select
            id="companyInput"
            v-model="registrationCompanyForm.organization"
            :options="companies"
            optionLabel="org_verbose_name"
            optionValue="name"
            placeholder="Begin typing a company name"/>
        </label>
        <div class="mt-4 flex gap-2">
          <Button label="Save" type="submit"/>
          <Button label="Cancel" type="button" severity="secondary" @click="$emit('canceled')" />
        </div>
      </Form>
    </div>

    <!-- Registration -->
    <div v-if="(section === 'registration' || section === 'all') && !!record">
      <Form @submit="submitRegistrationForm">
        <label
          id="registrationInputGroup"
          for="registrationInput"
          >Registration number:
          <InputText
            v-model="registrationForm.registration_no"
            id="registrationInput"
          />
        </label>
        <div class="mt-4 flex gap-2">
          <Button label="Save" type="submit"/>
          <Button label="Cancel" type="button" severity="secondary" @click="$emit('canceled')" />
        </div>
      </Form>
    </div>

  </div>
</template>

<script>
import { useRegistryStore } from '@/stores/registry.js'
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

export default {
  name: 'PersonDetailEdit',
  components: {
    'api-error': APIErrorMessage,
    ResponsiveGrid
  },

  /**
   * This component accepts two props: section and record.
   * section:
   *   'section' determines which section should be displayed for editing (e.g., personal details)
   *   this allows another component to reuse this component for editing one section at a time.
   *   options: 'company', 'person', 'all'
   * record:
   *   'record' determines the specific record that the edit form should act on.
   */
  props: ['section', 'record'],

  data () {
    return {
      registryStore: useRegistryStore(),
      personalInfoForm: {},
      contactInfoForm: {},
      registrationCompanyForm: {},
      registrationForm: {},
      companies: [],
      submitError: null,
      fieldErrors: {
        contact_email: []
      }
    }
  },
  computed: {
    error () { return this.registryStore.error },
    currentDriller () { return this.registryStore.currentDriller },
    validation () {
      return {
        contact_email: (this.fieldErrors.contact_email && this.fieldErrors.contact_email.length) ? false : null
      }
    }
  },
  methods: {
    formReset () {
      /**
       * populate form fields from the currentDriller object in store
       * fields are split up into 3 groups (personal info, contact info and affiliated companies).
       */

      // copy current person object from store
      const personData = JSON.parse(JSON.stringify(this.currentDriller))

      this.resetFieldErrors()
      this.personalInfoForm = {}
      this.registrationCompanyForm = {
        organization: null
      }

      this.personalInfoForm.first_name = personData.first_name
      this.personalInfoForm.surname = personData.surname
      this.personalInfoForm.pump_installer_orcs_no = personData.pump_installer_orcs_no
      this.personalInfoForm.well_driller_orcs_no = personData.well_driller_orcs_no

      // add contact info
      this.contactInfoForm = {
        contact_tel: personData.contact_tel,
        contact_email: personData.contact_email,
        contact_cell: personData.contact_cell
      }

      // add company info (for the registration record defined by prop 'record' only)
      if (this.record && this.record.organization) {
        this.registrationCompanyForm.organization = {
          name: this.record.organization.name,
          org_guid: this.record.organization.org_guid,
          org_verbose_name: this.record.organization.org_verbose_name
        }
      }

      if (this.record) {
        this.registrationForm = {
          registration_no: this.record.registration_no
        }
      }
    },
    submitCompanyForm () {
      const regGuid = this.record.register_guid
      const data = { organization: this.registrationCompanyForm.organization
        ? this.registrationCompanyForm.organization.org_guid : null }
      ApiService.patch('registrations', regGuid, data).then(() => {
        this.$emit('updated', true)
      })
    },
    submitPersonForm () {
      const data = this.personalInfoForm
      ApiService.patch('drillers', this.record, data).then(() => {
        this.$emit('updated')
      })
    },
    submitContactForm () {
      const data = this.contactInfoForm
      ApiService.patch('drillers', this.record, data).then(() => {
        this.$emit('updated')
      }).catch((e) => {
        const errors = e.response.data
        for (const field in errors) {
          // errors is an object containing keys corresponding to fields. For each field,
          // our API generally returns an array of strings
          this.fieldErrors[field] = errors[field]
        }
      })
    },
    submitRegistrationForm () {
      const data = this.registrationForm
      ApiService.patch('registrations', this.record.register_guid, data).then(() => {
        this.$emit('updated')
      }).catch((e) => {
        const errors = e.response.data
        for (const field in errors) {
          // errors is an object containing keys corresponding to fields. For each field,
          // our API generally returns an array of strings
          this.fieldErrors[field] = errors[field]
        }
      })
    },
    resetFieldErrors () {
      this.fieldErrors = {
        contact_email: []
      }
    }
  },
  created () {
    this.formReset()
    this.resetFieldErrors()
    if (this.section === 'company') {
      ApiService.query('organizations/names').then((response) => {
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
