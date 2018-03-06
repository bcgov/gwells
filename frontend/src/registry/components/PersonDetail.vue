<template>
  <div class="container-fluid">
    <div class="row" v-if="currentDriller != {}">
      <div class="col-xs-12 col-sm-7">
        <h2>{{ currentDriller.first_name }} {{ currentDriller.surname }}</h2>
      </div>
      <div class="col-xs-12 col-sm-5 text-center">
        <router-link
          class="btn btn-secondary"
          tag="button"
          :to="{
            name: 'PersonDetailEdit',
            params: {
              person_guid: currentDriller.person_guid
            }
          }"
          v-if="currentDriller.person_guid"><i class="fa fa-edit"></i>Edit</router-link>
      </div>
    </div>
    <div class="row">
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
              <td><router-link :to="{
                name: 'PersonApplicationDetail',
                params: {
                  person_guid: currentDriller.person_guid,
                  classCode: item.code
                }
              }">{{ item.description }}</router-link></td>
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
          <span class="registry-label">Last name:</span> {{ currentDriller.surname }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          <span class="registry-label">First name:</span> {{ currentDriller.first_name }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <r-checkbox :checked="drillerOver19"></r-checkbox> <span class="registry-label">Confirmed applicant is 19 or older</span>
        </div>
      </div>
    </fieldset>
    <fieldset class="registry-section">
      <legend>Current Company Information</legend>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Company name:</span> {{ company.organization_name }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          <span class="registry-label">Street address:</span> {{ company.street_address }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">City:</span> {{ company.city }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          <span class="registry-label">Province:</span> {{ company.province_state }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Postal Code:</span> {{ company.postal_code }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          <span class="registry-label">Telephone:</span> {{ company.contact_tel }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-12 registry-item">
          <span class="registry-label">Email address:</span> {{ company.contact_email }}
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
import { FETCH_DRILLER, LOGOUT } from '@/registry/store/actions.types'

export default {
  name: 'person-detail',
  components: {
    'api-error': APIErrorMessage,
    'r-checkbox': QualCheckbox
  },
  data () {
    return {}
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
      'user',
      'error',
      'currentDriller',
      'drillers'
    ])
  },
  methods: {
    logout () {
      this.$store.dispatch(LOGOUT)
    }
  },
  created () {
    if (this.currentDriller.person_guid !== this.$route.params.person_guid) {
      this.$store.commit(SET_DRILLER, {})
      if (this.drillers && this.drillers.results && this.drillers.results.length) {
        const driller = this.drillers.results.find((item) => {
          return item.person_guid === this.$route.params.person_guid
        })
        if (driller) {
          this.$store.commit(SET_DRILLER, driller)
        }
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
</style>
