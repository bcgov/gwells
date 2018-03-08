<template>
  <div class="container-fluid">
    <div class="row" v-if="currentDriller != {}">
      <div class="col-xs-12 col-sm-7">
        <h2>{{ currentDriller.first_name }} {{ currentDriller.surname }}</h2>
      </div>
      <div class="col-xs-12 col-sm-5 text-center">
        <router-link :to="{ name: 'PersonDetail', params: { person_guid: currentDriller.person_guid } }" tag="button" class="btn btn-secondary">Cancel editing person</router-link>
      </div>
      <div class="col-xs-12" v-if="error">
        <api-error :error="error" resetter="setError"></api-error>
      </div>
    </div>
    <div class="panel" v-if="editDriller != {}">
      <div class="panel-body">
        <div class="container-fluid">
          <div class="table-responsive">
            <table class="table">
              <thead>
                <th class="col-xs-2">Classification</th>
                <th class="col-xs-2">Register Status</th>
                <th class="col-xs-2">Date Registered</th>
              </thead>
              <tbody>
                <tr v-if="classifications && classifications.length" v-for="(classification, index) in classifications" :key="`classification ${index}`">
                  <td>{{ classification.description }}</td>
                  <td>{{ classification.status }}</td>
                  <td>{{ classification.date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="row">
            <p class="col-xs-12">
              <button type="button" class="btn btn-secondary" @click="addClassificationToggle = !addClassificationToggle">
                <span v-if="!addClassificationToggle"><i class="fa fa-plus-square-o"></i> Add classification</span>
                <span v-if="addClassificationToggle"><i class="fa fa-minus-square-o"></i> Cancel</span>
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="panel" v-if="addClassificationToggle" style="border-color: #1a5a96">
      <div class="panel-body">
        <add-classification/>
          <button type="button" class="btn btn-primary" @click="addClassificationToggle = !addClassificationToggle">Save</button>
          <button type="button" class="btn btn-secondary" @click="addClassificationToggle = !addClassificationToggle">
            <span v-if="addClassificationToggle">Cancel</span>
          </button>
      </div>
    </div>
    <div class="panel" v-if="editDriller != {}">
      <div class="panel-body">
        <div class="container-fluid">
          <h3>Personal Information</h3>
          <form class="form-horizontal">
            <div class="form-group">
              <label class="col-xs-12 col-md-2 registry-form-label" for="personLastName">Last name:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="personLastName" placeholder="Surname" v-model="editDriller.surname">
              </div>
              <label class="col-xs-12 col-md-2 registry-form-label" for="personFirstName">First name:</label>
              <div class="col-xs-12 col-md-3">
                <input type="text" id="personFirstName" placeholder="First name" v-model="editDriller.first_name">
              </div>
            </div>
            <div class="form-group">
              <div class="checkbox col-xs-12 col-sm-5">
                <label class="form-spacing">
                  <input type="checkbox" v-model="drillerOver19.value"  style="margin-top: 0px"> <strong>Confirmed applicant is 19 or older</strong>
                </label>
              </div>
              <label class="col-xs-12 col-md-2 registry-form-label" for="identificationSelect">Proof of age: </label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <select class="form-control" v-model="drillerOver19.proof" id="identificationSelect">
                  <option value="">Select identification type</option>
                  <option v-for="(item, index) in proofOfAgeChoices" :key="`ident ${index}`" :value="item">{{ item }}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-xs-12 col-md-2" for="drillRegNo">Driller registration number:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="drillRegNo" placeholder="Enter registration number" v-model="editDrillerReg.drillRegNo">
              </div>
              <label class="col-xs-12 col-md-2" for="pumpRegNo">Pump installer registration number:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="pumpRegNo" placeholder="Enter registration number" v-model="editDrillerReg.pumpRegNo">
              </div>
            </div>
            <div class="form-group">
              <label class="col-xs-12 col-md-2" for="drillORCSNo">Driller ORCS number:</label>
              <div class="col-xs-12 col-md-3">
                <input type="text" id="drillORCSNo" placeholder="Enter ORCS number" v-model="editDrillerReg.drillORCSNo">
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="panel" v-if="editDriller != {}">
      <div class="panel-body">
        <div class="container-fluid">
          <h3>Company Information</h3>
          <form class="form-horizontal">
            <div class="form-group">
              <label class="col-xs-12 col-md-2" for="orgName">Company name:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <select id="orgName" v-model="editCompany.organization_name">
                  <option value="">Select company</option>
                  <option>{{company.organization_name}}</option>
                </select>
              </div>
              <label class="col-xs-12 col-md-2" for="orgAddress">Company address:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgAddress" placeholder="Enter organization address" v-model="editCompany.street_address">
              </div>
            </div>
            <div class="form-group">
              <label class="col-xs-12 col-md-2" for="orgCity">City:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgCity" placeholder="Enter city" v-model="editCompany.city">
              </div>
              <label class="col-xs-12 col-md-2" for="orgProvince">Province:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgProvince" placeholder="Enter organization Province" v-model="editCompany.province_state">
              </div>
            </div>
            <div class="form-group">
              <label class="col-xs-12 col-md-2" for="orgPostalCode">Postal code:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgPostalCode" placeholder="Enter postal code" v-model="editCompany.postal_code">
              </div>
              <label class="col-xs-12 col-md-2" for="orgPhone">Office number:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgPhone" placeholder="Enter phone number" v-model="editCompany.contact_tel">
              </div>
            </div>
            <div class="form-group">
              <label class="col-xs-12 col-md-2" for="orgCell">Cell number:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgCell" placeholder="Enter cell number">
              </div>
              <label class="col-xs-12 col-md-2" for="orgFax">Fax number:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgFax" placeholder="Enter fax number">
              </div>
            </div>
            <div class="form-group">
              <label class="col-xs-12 col-md-2" for="orgEmail">Email:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgEmail" placeholder="Enter email address" v-model="editCompany.contact_email">
              </div>
              <label class="col-xs-12 col-md-2" for="orgWebsite">Website:</label>
              <div class="col-xs-12 col-md-3 form-spacing">
                <input type="text" id="orgWebsite" placeholder="Enter website address" v-model="editCompany.website_url">
              </div>
            </div>
            <div class="form-group">
              <div class="col-xs-12">
                <button class="btn btn-secondary" type="button">Add new company</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="panel" v-if="editDriller != {}">
      <div class="panel-body">
        <div class="container-fluid">
          <div class="row registry-item">
            <div class="col-xs-12">
              <label for="drillerNotes">Notes:</label>
              <textarea class="form-control" rows="3" id="drillerNotes" v-model="drillerNote"></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="panel" v-if="editDriller != {}">
      <div class="panel-body">
        <div class="container-fluid">
          <div class="row registry-item">
            <div class="col-xs-12">
              <button type="button" class="btn btn-primary">Save</button>
              <router-link :to="{ name: 'PersonDetail', params: { person_guid: currentDriller.person_guid } }" tag="button" class="btn btn-secondary">Cancel</router-link>
            </div>
          </div>
          <div class="row registry-item">
            <div class="col-xs-12">
              <button type="button" class="btn btn-secondary">View record change history</button>
            </div>
          </div>
          <div class="row registry-item">
            <div class="col-xs-12">
              <button type="button" class="btn btn-secondary">Upload attachments</button> <span class="attachment-icon"> <i class="fa fa-paperclip"></i></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage'
import QualCheckbox from '@/common/components/QualCheckbox'
import ClassificationAdd from '@/registry/components/ClassificationAdd'
import { mapGetters } from 'vuex'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER } from '@/registry/store/actions.types'

export default {
  name: 'PersonDetailEdit',
  components: {
    'api-error': APIErrorMessage,
    'r-checkbox': QualCheckbox,
    'add-classification': ClassificationAdd
  },
  data () {
    return {
      addClassificationToggle: false,
      editDriller: {},
      editDrillerReg: {
        drillRegNo: '',
        pumpRegNo: '',
        drillORCSNo: ''
      },
      drillerNote: '',
      editCompany: {},
      drillerOver19: {
        value: true,
        app: 'well',
        proof: ''
      },
      proofOfAgeChoices: [
        'Driver\'s license',
        'Passport',
        'Birth certificate'
      ]
    }
  },
  computed: {
    company () {
      if (this.currentDriller && this.currentDriller.companies && this.currentDriller.companies.length) {
        return this.currentDriller.companies[0]
      }
      return {}
    },
    classifications () {
      const classifications = []

      // classifications are contained within arrays pulled from the application table
      if (
        this.currentDriller.applications &&
        this.currentDriller.applications.length
      ) {
        // since each person can have multiple applications, and each application can have multiple
        // classifications, we need to iterate through several arrays.
        this.currentDriller.applications.forEach((app) => {
          let status = null
          let date = null

          // set date for this application- it will apply to all qualifications/classifications associated
          // with this application.

          // priority of status codes from lowest to highest
          const statusPriority = ['P', 'A']

          if (app.registriesapplicationstatus_set && app.registriesapplicationstatus_set.length) {
            statusPriority.forEach((code) => {
              const statusLevel = app.registriesapplicationstatus_set.findIndex((item) => {
                return item.status_code === code
              })

              if (~statusLevel) {
                status = app.registriesapplicationstatus_set[statusLevel].status
                date = app.registriesapplicationstatus_set[statusLevel].effective_date
              }
            })
          }

          // now iterate through classifications that the person has applied for and push onto an array
          if (app.classificationappliedfor_set &&
            app.classificationappliedfor_set.length) {
            app.classificationappliedfor_set.forEach((classification) => {
              if (
                classification.registries_subactivity
              ) {
                classifications.push({
                  code: classification.registries_subactivity.code.toLowerCase(),
                  description: classification.registries_subactivity.description,
                  status: status,
                  date: date
                })
              }
            })
          }
        })
      }
      return classifications
    },
    drillerApplicationNotes () {
      const notes = []
      if (this.currentDriller.applications && this.currentDriller.applications.length) {
        this.currentDriller.applications.forEach((app) => {
          if (app.registrar_notes) {
            notes.push({
              note: app.registrar_notes,
              appKey: `notes ${app.application_guid}`
            })
          }
        })
      }
      return notes
    },
    ...mapGetters([
      'loading',
      'error',
      'currentDriller',
      'drillers'
    ])
  },
  watch: {
    currentDriller: function () {
      this.editDriller = JSON.parse(JSON.stringify(this.currentDriller))
    },
    company: function () {
      this.editCompany = JSON.parse(JSON.stringify(this.company))
    }
  },
  created () {
    if (this.currentDriller.person_guid !== this.$route.params.person_guid) {
      this.$store.commit(SET_DRILLER, {})
    }
    this.$store.dispatch(FETCH_DRILLER, this.$route.params.person_guid)
  }
}
</script>

<style>
.registry-section {
  margin-top: 25px;
  margin-bottom: 20px;
}
.registry-item {
  margin-bottom: 20px;
}
.registry-label {
  font-weight: bold;
}
.registry-disabled-item {
  color: #808080;
  cursor: auto!important;
}
.qualification-item {
  margin-bottom: 5px;
}
.attachment-icon {
  font-size: 2rem;
  margin-left: 10px;
  margin-top: 5px;
}
.registry-form-label {
  padding-top: 5px;
}
</style>
