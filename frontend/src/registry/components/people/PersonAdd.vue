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
          <h5 class="card-title">Add a Well Driller or Well Pump Installer</h5>
          <b-form @submit.prevent="onFormSubmit()" @reset.prevent="onFormReset()">
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
                    v-model="drillerForm.person.first_name"
                    required
                    placeholder="Enter first name"/>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row class="mt-3">
              <b-col cols="12" md="5">
                <b-form-group
                  id="contactTelInputGroup"
                  label="Telephone number:"
                  label-for="contactTelInput">
                  <b-form-input
                    id="contactTelInput"
                    type="text"
                    v-model="drillerForm.contact_info.contact_tel"
                    placeholder="Enter telephone number"/>
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
                    v-model="drillerForm.contact_info.contact_email"
                    placeholder="Enter email address"/>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row class="mt-3">
              <b-col md="5">
                <b-form-group
                  id="companyInputGroup"
                  label="Company:"
                  label-for="companyInput">
                  <v-select
                    v-model="drillerForm.person.organization"
                    :options="companies"
                    placeholder="Begin typing a company name"/>
                </b-form-group>
                <b-button type="button" href="#" variant="light" size="sm" class="mb-3"><i class="fa fa-plus-square-o"></i> Add a company</b-button>
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
              <b-row v-if="drillerForm.regType.some(x => x === 'DRILL')">
                <b-col cols="12" md="5">
                  <b-form-group
                    id="drillerRegNoInputGroup"
                    label="Well Driller Registration Number:"
                    label-for="drillerRegNoInput">
                    <b-form-input
                      id="drillerRegNoInput"
                      type="text"
                      v-model="drillerForm.registrations.drill.registration_no"
                      placeholder="Enter registration number"/>
                  </b-form-group>
                </b-col>
              </b-row>
              <b-row v-if="drillerForm.regType.some(x => x === 'PUMP')">
                <b-col cols="12" md="5">
                  <b-form-group
                    id="pumpRegNoInputGroup"
                    label="Well Pump Installer Registration Number:"
                    label-for="pumpRegNoInput">
                    <b-form-input
                      id="pumpRegNoInput"
                      type="text"
                      v-model="drillerForm.registrations.pump.registration_no"
                      placeholder="Enter registration number"/>
                  </b-form-group>
                </b-col>
              </b-row>
            </b-card>
            <b-row class="mt-3">
              <b-col>
                <b-button type="submit" class="mr-2" variant="primary">Submit</b-button>
                <b-button type="reset" variant="light">Reset</b-button>
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

export default {
  name: 'PersonDetailEdit',
  components: {
    'api-error': APIErrorMessage
  },
  data () {
    return {
      breadcrumbs: [
        {
          text: 'Registry Search',
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
          first_name: ''
        },
        regType: [],
        contact_info: {
          contact_tel: '',
          contact_email: ''
        },
        registrations: {
          drill: {
            registries_activity: 'DRILL',
            status: 'ACTIVE',
            registration_no: ''
          },
          pump: {
            registries_activity: 'PUMP',
            status: 'ACTIVE',
            registration_no: ''
          }
        }
      },
      companies: [
        { value: '123', label: 'Big Time Drilling Co.' },
        { value: '124', label: 'Steve\'s Drilling Inc.' }
      ]
    }
  },
  computed: {
    ...mapGetters([
      'loading',
      'error'
    ])
  },
  methods: {
    onFormSubmit () {
      const registrations = []
      const contactInfo = []
      const personData = Object.assign({}, this.drillerForm.person)

      // add registration data for activities checked off on form
      this.drillerForm.regType.forEach((item) => {
        registrations.push(this.drillerForm.registrations[item.toLowerCase()])
      })

      // add submitted contact info onto collection of person's contact details
      contactInfo.push(this.drillerForm.contact_info)

      personData['registrations'] = registrations
      personData['contact_info'] = contactInfo

      ApiService.post('drillers', personData)
    }
  }
}
</script>

<style>
</style>
