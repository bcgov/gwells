<template>
  <div class="container-fluid">
    <div class="row" v-if="currentDriller != {}">
      <div class="col-xs-12 col-sm-8">
        <h2>{{ currentDriller.first_name }} {{ currentDriller.surname }}</h2>
      </div>
      <div class="col-xs-12" v-if="error">
        <api-error :error="error" resetter="setError"></api-error>
      </div>
    </div>
    <div>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <th class="col-xs-2">Classification</th>
            <th class="col-xs-2">Register Status</th>
            <th class="col-xs-2">Date Registered</th>
          </thead>
          <tbody>
            <tr v-if="classifications && classifications.length" v-for="(item, index) in classifications" :key="`classification ${index}`">
              <td>{{ item.description }}</td>
              <td>{{ item.status }}</td>
              <td>{{ item.date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <fieldset class="registry-section">
      <legend>Personal Information</legend>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Last name: {{ currentDriller.surname }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          First name: {{ currentDriller.first_name }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <r-checkbox :checked="drillerOver19"></r-checkbox> Confirmed applicant is 19 or older
        </div>
      </div>
    </fieldset>
    <fieldset class="registry-section">
      <legend>Current Company Information</legend>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Company name: {{ company.organization_name }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Street address: {{ company.street_address }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          City: {{ company.city }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Province: {{ company.province_state }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Postal Code: {{ company.postal_code }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Telephone: {{ company.contact_tel }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Email address: {{ company.contact_email }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Website: {{ company.contact_email }}
        </div>
      </div>
    </fieldset>
    <div v-if="drillerApplicationNotes && drillerApplicationNotes.length">
      <div class="row">
        <div class="col-xs-12">
          <h4>Notes</h4>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12">
          <p v-for="note in drillerApplicationNotes" :key="note.appKey">{{ note.note }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage'
import QualCheckbox from '@/common/components/QualCheckbox'
import { mapGetters } from 'vuex'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER } from '@/registry/store/actions.types'

export default {
  name: 'person-detail',
  components: {
    'api-error': APIErrorMessage,
    'r-checkbox': QualCheckbox
  },
  data () {
    return {
      person: {
        name: 'John Bobert',
        certNumber: 'CGWA930209',
        certAuthority: 'Canadian Groundwater Association',
        qualificationCode: 'DRILL',
        activityDescription: 'Well Driller'
      },
      qualType: 'DRILL',
      wellQualifications: {
        supply: true,
        monitoring: true,
        recharge: true,
        injection: true,
        dewatering: false,
        remediation: false,
        geotechnical: true,
        geoexchange: false
      }
    }
  },
  computed: {
    company () {
      if (this.currentDriller && this.currentDriller.companies && this.currentDriller.companies.length) {
        return this.currentDriller.companies[0]
      }
      return {}
    },
    drillerOver19 () {
      if (this.currentDriller.applications && this.currentDriller.applications.length) {
        return ~this.currentDriller.applications.findIndex((app) => {
          return app.over19_ind === true
        })
      }
      return false
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
          console.log('checking application')
          console.log(app)
          let status = null
          let date = null

          // set date for this application- it will apply to all qualifications/classifications associated
          // with this application.

          // priority of status codes from lowest to highest
          const statusPriority = ['P', 'A']

          if (app.registriesapplicationstatus_set && app.registriesapplicationstatus_set.length) {
            statusPriority.forEach((code) => {
              console.log('checking for status code', code)
              const statusLevel = app.registriesapplicationstatus_set.findIndex((item) => {
                return item.status_code === code
              })

              if (~statusLevel) {
                console.log('found a status', code)
                status = app.registriesapplicationstatus_set[statusLevel].status
                date = app.registriesapplicationstatus_set[statusLevel].effective_date
              }
            })
          }
          console.log(status, date)

          // now iterate through classifications that the person has applied for and push onto an array
          if (app.classificationappliedfor_set &&
            app.classificationappliedfor_set.length) {
            app.classificationappliedfor_set.forEach((classification) => {
              console.log('checking classification')
              console.log(classification)
              if (
                classification.registries_subactivity &&
                classification.registries_subactivity.description &&
                classification.registries_subactivity.description
              ) {
                classifications.push({
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
      console.log(this.currentDriller.applications)
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
  created () {
    this.$store.commit(SET_DRILLER, {})
    if (this.drillers && this.drillers.results && this.drillers.results.length) {
      const driller = this.drillers.results.find((item) => {
        return item.person_guid === this.$route.params.person_guid
      })
      if (driller) {
        this.$store.commit(SET_DRILLER, driller)
      }
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
.registry-disabled-item {
  color: #808080;
  cursor: auto!important;
}
.qualification-item {
  margin-bottom: 5px;
}
</style>
