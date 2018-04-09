<template>
  <div class="container">
    <div class="card">
      <div class="card-body">
        <div v-if="currentDriller != {}">
          <div class="row">
            <div class="col-xs-12 col-sm-7">
              <h5 class="card-title">{{ currentDriller.first_name }} {{ currentDriller.surname }}</h5>
            </div>
            <div class="col-xs-12 col-sm-5 text-right">
              <router-link
                class="btn btn-default"
                :to="{
                  name: 'PersonDetailEdit',
                  params: {
                    person_guid: currentDriller.person_guid
                  }
                }"
                v-if="currentDriller.person_guid"><i class="fa fa-edit"></i>Edit</router-link>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12" v-if="error">
            <api-error :error="error" resetter="SET_ERROR"></api-error>
          </div>
        </div>
        <div class="table-responsive">
          <table id="classification-table" class="table">
            <thead>
              <th>Classification</th>
              <th>Register Status</th>
              <th>Date Registered</th>
            </thead>
            <tbody>
              <tr v-if="classifications && classifications.length" v-for="(item, index) in classifications" :key="`classification ${index}`">
                <td><router-link :to="{
                  name: 'PersonApplicationDetail',
                  params: { person_guid: currentDriller.person_guid, classCode: item.code } }">
                {{ item.description }}</router-link></td>
                <td>{{ item.status }}</td>
                <td>{{ item.date }}</td>
              </tr>
            </tbody>
          </table>
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
        this.currentDriller.registrations &&
        this.currentDriller.registrations.length
      ) {
        // since each person can have multiple registrations, and each application can have multiple
        // classifications, we need to iterate through several arrays.
        this.currentDriller.registrations.forEach((reg) => {
          reg.applications.forEach((app) => {
            let status
            let date

            // set date for this application- it will apply to all qualifications/classifications associated
            // with this application.

            // priority of status codes from lowest to highest
            const statusPriority = ['P', 'A']

            if (app.status_set && app.status_set.length) {
              statusPriority.forEach((code) => {
                const statusLevel = app.status_set.findIndex((item) => {
                  return item.status_code === code
                })

                if (~statusLevel) {
                  status = app.status_set[statusLevel].description
                  date = app.status_set[statusLevel].effective_date
                }
              })
            }

            // now iterate through classifications that the person has applied for and push onto an array

            classifications.push({
              code: app.subactivity,
              description: app.subactivity_description,
              status: status,
              date: date
            })
          })
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
  created () {
    if (this.currentDriller.person_guid !== this.$route.params.person_guid) {
      // reset the currentDriller object if another driller was previously loaded
      this.$store.commit(SET_DRILLER, {})
      if (this.drillers && this.drillers.results && this.drillers.results.length) {
        // use basic info (name etc) from driller list while complete record is being fetched from API
        const driller = this.drillers.results.find((item) => {
          return item.person_guid === this.$route.params.person_guid
        })
        if (driller) {
          this.$store.commit(SET_DRILLER, driller)
        }
      }
    }
    // always fetch up to date record from API when page loads
    this.$store.dispatch(FETCH_DRILLER, this.$route.params.person_guid)
  }
}
</script>

<style>
#classification-table th {
  font-weight: 400!important;
}
</style>
