<template>
  <div class="container">
    <b-card no-body class="mb-3">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <div class="card">
      <div class="card-body">
        <div v-if="currentDriller != {}">
          <div class="row">
            <div class="col-9">
              <h5 class="card-title">{{ currentDriller.first_name }} {{ currentDriller.surname }}</h5>
            </div>
            <div class="col-3 text-right">
              <router-link
                class="btn btn-default registries-edit-btn"
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
          <div class="col-12" v-if="error">
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
                  name: 'ApplicationDetail',
                  params: { person_guid: currentDriller.person_guid, classCode: item.code } }">
                {{ item.description }}</router-link></td>
                <td>{{ item.status }}</td>
                <td>{{ item.date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title mb-3">Personal Information</h5>
            <div class="row mb-2">
              <div class="col-5 col-md-2 mb-1 mb-sm-0">
                Last name:
              </div>
              <div class="col-7 col-md-4">
                {{ currentDriller.surname }}
              </div>
              <div class="col-5 col-md-2">
                First name:
              </div>
              <div class="col-7 col-md-4">
                {{ currentDriller.first_name }}
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-12 col-md-6 mb-1">
                <i class="fa fa-check-square"></i>
                Confirmed applicant is 19 or older
              </div>
              <div class="col-5 col-md-2">
                Proof of age:
              </div>
              <div class="col-7 col-md-4">
                Driver's license
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-5 col-md-2">
                ORCS number:
              </div>
              <div class="col-7 col-md-10">
                JOB020180608
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-5 col-md-2">
                Email address:
              </div>
              <div class="col-7 col-md-4">
                <div v-for="(email, index) in personEmail" :key="`person email ${index}`">
                  {{ email }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <h5 class="card-title mb-3">Current Company Information</h5>
            <div v-if="currentDriller.organization">
              <div class="row mb-2">
                <div class="col-5 col-md-2 mb-1 mb-sm-0">
                  Company name:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.name }}
                </div>
                <div class="col-5 col-md-2">
                  Street address:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.street_address }}
                </div>
              </div>
              <div class="row mb-2">
                <div class="col-5 col-md-2 mb-1 mb-sm-0">
                  City:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.city }}
                </div>
                <div class="col-5 col-md-2">
                  Province:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.province_state }}
                </div>
              </div>
              <div class="row mb-2">
                <div class="col-5 col-md-2 mb-1 mb-sm-0">
                  Postal Code:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.postal_code }}
                </div>
                <div class="col-5 col-md-2">
                  Office number:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.main_tel }}
                </div>
              </div>
              <div class="row mb-2">
                <div class="col-5 col-md-2 mb-1 mb-sm-0">
                  Cell number:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.surname }}
                </div>
                <div class="col-5 col-md-2">
                  Fax number:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.fax_tel }}
                </div>
              </div>
              <div class="row mb-2">
                <div class="col-5 col-md-2 mb-1 mb-sm-0">
                  Email address:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.contact_email }}
                </div>
                <div class="col-5 col-md-2">
                  Website:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.organization.website_url }}
                </div>
              </div>
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
      breadcrumbs: [
        {
          text: 'Registry Search',
          to: { name: 'SearchHome' }
        },
        {
          text: 'Person Profile',
          active: true
        }
      ]
    }
  },
  computed: {
    personEmail () {
      // sort a person's contact info into a list of emails
      const email = []
      this.currentDriller.contact_info.forEach((item) => {
        if (item.contact_email) {
          email.push(item.contact_email)
        }
      })
      return email
    },
    personTel () {
      const tel = []
      this.currentDriller.contact_info.forEach((item) => {
        if (item.contact_tel) {
          tel.push(item.contact_tel)
        }
      })
      return tel
    },
    company () {
      if (this.currentDriller && this.currentDriller.companies && this.currentDriller.companies.length) {
        return this.currentDriller.companies[0]
      }
      return {}
    },
    drillerOver19 () {
      if (this.currentDriller.applications && this.currentDriller.applications.length) {
        return this.currentDriller.applications.some((app) => {
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
                  return item.status === code
                })

                // check if statusLevel is a valid array index (e.g. not -1)
                // note: ~(-1) evaluates to 0, but is truthy for valid array indices
                if (~statusLevel) {
                  status = app.status_set[statusLevel].description
                  date = app.status_set[statusLevel].effective_date
                }
              })
            }

            // now iterate through classifications that the person has applied for and push onto an array

            classifications.push({
              code: app.subactivity,
              description: app.subactivity,
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
.registries-edit-btn {
  margin-top: -5px;
}
</style>
