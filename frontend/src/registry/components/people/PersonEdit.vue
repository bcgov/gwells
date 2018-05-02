<template>
  <div>
    <div v-if="section === 'person' || section === 'all'">
      <b-form @submit.prevent="submitPersonForm">
        <b-row>
          <b-col cols="12" md="5">
            <b-form-group
              id="surnameInputGroup"
              label="Surname:"
              label-for="surnameInput">
              <b-form-input
                id="surnameInput"
                type="text"
                v-model="personalInfoForm.surname"
                required
                placeholder="Enter surname"/>
            </b-form-group>
          </b-col>
          <b-col cols="12" md="5" offset-md="1">
            <b-form-group
              id="firstnameInputGroup"
              label="First name:"
              label-for="firstnameInput">
              <b-form-input
                id="firstnameInput"
                type="text"
                v-model="personalInfoForm.first_name"
                required
                placeholder="Enter first name"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" md="5">
            <b-form-group
              id="drillOrcsInputGroup"
              label="Well Driller ORCS:"
              label-for="drillORCSInput">
              <b-form-input
                id="drillORCSInput"
                type="text"
                v-model="personalInfoForm.well_driller_orcs_no"
                placeholder="Enter well driller ORCS"/>
            </b-form-group>
          </b-col>
          <b-col cols="12" md="5" offset-md="1">
            <b-form-group
              id="pumpORCSInputGroup"
              label="Pump installer ORCS:"
              label-for="pumpORCSInput">
              <b-form-input
                id="pumpORCSInput"
                type="text"
                v-model="personalInfoForm.pump_installer_orcs_no"
                placeholder="Enter pump installer ORCS"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <button type="submit" class="btn btn-primary">Submit</button>
            <button type="button" class="btn btn-light" @click="$emit('canceled')">Cancel</button>
          </b-col>
        </b-row>
      </b-form>
    </div>
    <div v-if="(section === 'contact' || section === 'all')">
      <b-form @submit.prevent="submitContactForm">
        <b-row
            v-for="(contact, contactIndex) in contactInfoForm"
            :key="`contact set ${contactIndex}`">
          <b-col cols="12" md="5">
            <b-form-group
              :id="`emailInputGroup${contactIndex}`"
              label="Email address:"
              :label-for="`emailInput${contactIndex}`">
              <b-form-input
                :id="`emailInput${contactIndex}`"
                type="text"
                v-model="contactInfoForm[contactIndex].contact_email"
                placeholder="Enter email"/>
            </b-form-group>
          </b-col>
          <b-col cols="12" md="5" offset-md="1">
            <b-form-group
              :id="`telInputGroup${contactIndex}`"
              label="Telephone:"
              :label-for="`telInput${contactIndex}`">
              <b-form-input
                :id="`telInput${contactIndex}`"
                type="text"
                v-model="contactInfoForm[contactIndex].contact_tel"
                placeholder="Enter telephone number"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
          <button
              class="btn btn-light btn-sm registries-edit-btn mb-3"
              type="button"
              @click="addContactSet">
            <i class="fa fa-plus-square-o"></i> Add more contact info</button>
          </b-col>
        </b-row>
      </b-form>
      <b-row>
        <b-col>
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" class="btn btn-light" @click="$emit('canceled')">Cancel</button>
        </b-col>
      </b-row>
    </div>
    <div v-if="(section === 'company' || section === 'all') && !!record">
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
      personalInfoForm: {},
      contactInfoForm: [],
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
      this.contactInfoForm = []
      this.registrationCompanyForm = {
        organization: null
      }

      this.personalInfoForm.first_name = personData.first_name
      this.personalInfoForm.surname = personData.surname
      this.personalInfoForm.pump_installer_orcs_no = personData.pump_installer_orcs_no
      this.personalInfoForm.well_driller_orcs_no = personData.well_driller_orcs_no

      // add contact info
      if (personData.contact_info) {
        for (let i = 0; i < personData.contact_info.length; i++) {
          this.contactInfoForm.push({
            contact_tel: personData.contact_info[i].contact_tel,
            contact_email: personData.contact_info[i].contact_email,
            contact_cell: personData.contact_info[i].contact_cell,
            contact_detail_guid: personData.contact_info[i].contact_detail_guid,
            new: false
          })
        }
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
    },
    submitPersonForm () {
      const data = this.personalInfoForm
      ApiService.patch('drillers', this.record, data).then(() => {
        this.$emit('updated')
      })
    },
    addContactSet () {
      this.contactInfoForm.push({
        contact_tel: null,
        contact_email: null,
        contact_cell: null,
        new: true
      })
    },
    submitContactForm () {
      console.log('clicked')
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
