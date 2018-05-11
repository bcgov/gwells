<template>
  <div class="container">
    <b-card no-body class="mb-3">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <div class="col-xs-12" v-if="error">
      <api-error :error="error" resetter="SET_ERROR"></api-error>
    </div>
    <div class="card">
      <div class="card-body">
          <h5 class="card-title">Add new applicant</h5>
          <b-form @submit.prevent="onFormSubmit()" @reset.prevent="onFormReset()">
            <b-row><b-col><h6 class="font-weight-bold">Personal Information</h6></b-col></b-row>
            <b-row>
              <b-col cols="12" md="5">
                <b-form-group
                  id="surnameInputGroup"
                  label="Surname:"
                  label-for="surnameInput">
                  <b-form-input
                    id="surnameInput"
                    type="text"
                    v-model="drillerForm.person.surname"
                    required/>
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
                    v-model="drillerForm.person.first_name"
                    required/>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row class="mt-3"><b-col><h6 class="font-weight-bold">Contact Information</h6></b-col></b-row>
            <b-row>
              <b-col cols="12" md="5">
                <b-form-group
                  id="contactTelInputGroup"
                  label="Telephone number:"
                  label-for="contactTelInput">
                  <b-form-input
                    id="contactTelInput"
                    type="text"
                    v-model="drillerForm.person.contact_tel"/>
                </b-form-group>
              </b-col>
              <b-col cols="12" md="5" offset-md="1">
                <b-form-group
                  id="contactEmailInputGroup"
                  label="Email:"
                  label-for="contactEmailInput">
                  <b-form-input
                    id="contactEmailInput"
                    type="text"
                    :state="validation.contact_email"
                    aria-describedby="contactEmailFeedback"
                    v-model="drillerForm.person.contact_email"/>
                  <b-form-invalid-feedback id="contactEmailFeedback">
                    <div v-for="(error, index) in fieldErrors.contact_email" :key="`emailInput error ${index}`">
                      {{ error }}
                    </div>
                  </b-form-invalid-feedback>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row class="mt-3"><b-col><h6 class="font-weight-bold">Document Control</h6></b-col></b-row>
            <b-row>
              <b-col>
                <b-form-group
                  id="drillerORCSInputGroup"
                  label="Well Driller ORCS Number:"
                  label-for="drillerORCSInput">
                  <b-form-input
                    id="drillerORCSInput"
                    type="text"
                    v-model="drillerForm.person.well_driller_orcs_no"
                    placeholder="example: 38000-25/DRI SMIT J"/>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                  id="pumpORCSInputGroup"
                  label="Pump Installer ORCS Number:"
                  label-for="pumpORCSInput">
                  <b-form-input
                    id="pumpORCSInput"
                    type="text"
                    v-model="drillerForm.person.pump_installer_orcs_no"
                    placeholder="example: 38000-25/PUMP SMIT J"/>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row class="mt-3">
              <b-col>
                <b-form-group label="Register as: " label-for="registrationTypeInput">
                  <b-form-checkbox-group id="registrationTypeInput" name="registrationType" v-model="drillerForm.regType">
                    <b-form-checkbox value="DRILL">Well Driller</b-form-checkbox>
                    <b-form-checkbox value="PUMP">Well Pump Installer</b-form-checkbox>
                  </b-form-checkbox-group>
                </b-form-group>
              </b-col>
            </b-row>
            <b-card class="mb-3" v-if="drillerForm.regType.some(x => x === 'DRILL' || x === 'PUMP')">
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
                  <b-alert :show="newOrgSuccess"
                        dismissible
                        variant="success"
                        @dismissed="newOrgSuccess=false">
                  Company added.
                  </b-alert>
                </b-col>
              </b-row>
              <div v-if="drillerForm.regType.some(x => x === 'DRILL')">
                <b-row>
                  <b-col cols="12" md="4">
                    <b-form-group
                      id="drillerRegNoInputGroup"
                      label="Well Driller Registration Number:"
                      label-for="drillerRegNoInput">
                      <b-form-input
                        id="drillerRegNoInput"
                        type="text"
                        v-model="drillerForm.registrations.drill.registration_no"/>
                    </b-form-group>
                  </b-col>
                  <b-col md="7" offset-md="1">
                    <b-form-group
                      id="companyInputGroup"
                      label="Well drilling company:"
                      label-for="companyInput">
                      <v-select
                        v-model="drillerForm.organizations.drill"
                        :options="companies"
                        placeholder="Begin typing a company name"
                        label="org_verbose_name">
                      </v-select>
                    </b-form-group>
                  </b-col>
                </b-row>
              </div>
              <div v-if="drillerForm.regType.some(x => x === 'PUMP')">
                <b-row>
                  <b-col cols="12" md="4">
                    <b-form-group
                      id="pumpRegNoInputGroup"
                      label="Well Pump Installer Registration Number:"
                      label-for="pumpRegNoInput">
                      <b-form-input
                        id="pumpRegNoInput"
                        type="text"
                        v-model="drillerForm.registrations.pump.registration_no"/>
                    </b-form-group>
                  </b-col>
                  <b-col md="7" offset-md="1">
                    <b-form-group
                      id="companyInputGroup"
                      label="Well pump installation company:"
                      label-for="companyInput">
                      <v-select
                        v-model="drillerForm.organizations.pump"
                        :options="companies"
                        placeholder="Begin typing a company name"
                        label="org_verbose_name">
                      </v-select>
                    </b-form-group>
                  </b-col>
                </b-row>
              </div>
            </b-card>
            <b-row class="mt-3">
              <b-col>
                <b-button type="submit" class="mr-2" variant="primary">Submit</b-button>
                <b-button type="reset" variant="light">Reset</b-button>
              </b-col>
            </b-row>
            <b-row class="mt-3">
              <b-col>
                <b-alert :show="submitSuccess"
                        dismissible
                        variant="success"
                        @dismissed="submitSuccess=false">
                  Successfully created a new person!
                </b-alert>
                <b-alert :show="!!submitError"
                        dismissible
                        variant="warning"
                        @dismissed="submitError=false">
                  Error creating a new person.
                  <div v-for="(value, key, index) in submitError.data" :key="`submit error ${index}`">
                    <span class="text-capitalize">{{ key }}</span>:
                    <span
                      v-for="(msg, msgIndex) in value"
                      :key="`submit error msg ${index} ${msgIndex}`">{{ msg }} </span>
                  </div>
                </b-alert>
              </b-col>
            </b-row>
          </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'

export default {
  name: 'PersonDetailEdit',
  components: {
    'api-error': APIErrorMessage,
    'organization-add': OrganizationAdd
  },
  data () {
    return {
      breadcrumbs: [
        {
          text: 'Registry',
          to: { name: 'SearchHome' }
        },
        {
          text: 'Add a Person',
          active: true
        }
      ],
      drillerForm: {
        person: {
          surname: '',
          first_name: '',
          contact_tel: '',
          contact_email: '',
          contact_cell: '',
          well_driller_orcs_no: '',
          pump_installer_orcs_no: ''
        },
        regType: [],
        registrations: {
          drill: {
            registries_activity: 'DRILL',
            status: 'ACTIVE',
            registration_no: '',
            organization: ''
          },
          pump: {
            registries_activity: 'PUMP',
            status: 'ACTIVE',
            registration_no: '',
            organization: ''
          }
        },
        organizations: {
          drill: null,
          pump: null
        }
      },
      companies: [
        { org_guid: '', name: '' }
      ],
      submitSuccess: false,
      submitError: false,
      newOrgSuccess: false,
      fieldErrors: {
        contact_email: []
      }
    }
  },
  computed: {
    validation () {
      return {
        contact_email: (this.fieldErrors.contact_email && this.fieldErrors.contact_email.length) ? false : null
      }
    },
    ...mapGetters([
      'loading',
      'error'
    ])
  },
  methods: {
    clearFieldErrors () {
      this.fieldErrors = {
        contact_email: []
      }
    },
    onFormSubmit () {
      /**
       * Submitting a new person record also creates corresponding registration records
       * for that each activity (driller or pump installer).
       *
       * This method collects data from the template's form fields and bundles it for the GWELLS API.
       * Data for an activity (driller etc.) is only included if the corresponding registration checkbox
       * is checked (checking a box adds the activity to this.regType).
       */
      const registrations = []
      const personData = Object.assign({}, this.drillerForm.person)
      this.submitSuccess = false
      this.submitError = false

      // strip empty strings
      Object.keys(personData).forEach((key) => {
        if (personData[key] === '' || personData[key] === null) {
          delete personData[key]
        }
      })

      // Set organizations for each activity to the GUID of the organization selected in the form
      if (this.drillerForm.organizations.drill) {
        this.drillerForm.registrations['drill'].organization = this.drillerForm.organizations.drill.org_guid
      }
      if (this.drillerForm.organizations.pump) {
        this.drillerForm.registrations['pump'].organization = this.drillerForm.organizations.pump.org_guid
      }

      // add registration data for activities checked off on form
      this.drillerForm.regType.forEach((item) => {
        registrations.push(this.drillerForm.registrations[item.toLowerCase()])
      })

      personData['registrations'] = registrations

      ApiService.post('drillers', personData).then((response) => {
        this.onFormReset()
        this.$router.push({ name: 'PersonDetail', params: { person_guid: response.data.person_guid } })
      }).catch((e) => {
        const errors = e.response.data
        for (const field in errors) {
          this.fieldErrors[field] = errors[field]
        }
      })
    },
    onFormReset () {
      this.clearFieldErrors()
      this.drillerForm = Object.assign({}, {
        person: {
          surname: '',
          first_name: '',
          contact_tel: '',
          contact_email: '',
          contact_cell: ''
        },
        organizations: {
          drill: null,
          pump: null
        },
        regType: [],
        registrations: {
          drill: {
            registries_activity: 'DRILL',
            status: 'ACTIVE',
            registration_no: '',
            organization: null
          },
          pump: {
            registries_activity: 'PUMP',
            status: 'ACTIVE',
            registration_no: '',
            organization: null
          }
        }
      })
    },
    newOrgHandler (orgGuid) {
      ApiService.query('organizations/names/').then((response) => {
        this.companies = response.data

        // Find the new company with the "emitted" organization record UUID
        if (this.drillerForm.regType && this.drillerForm.regType.length === 1) {
          this.drillerForm.organizations[[this.drillerForm.regType[0].toLowerCase()]] =
            this.companies.find((company) => company.org_guid === orgGuid)
        }
        this.newOrgSuccess = true
      }).catch(() => {
        this.orgListError = 'Unable to retrieve organization list.'
      })
    }
  },
  created () {
    ApiService.query('organizations/names/').then((response) => {
      this.companies = response.data
    }).catch(() => {
      this.orgListError = 'Unable to retrieve organization list.'
    })
  }
}
</script>

<style>
</style>
