<template>
  <div class="container p-1 p-md-3">
    <b-card no-body class="mb-3">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <div class="card">
      <div class="card-body p-2 p-md-3">
        <div v-if="currentDriller != {}">
          <div class="row">
            <div class="col-12">
              <h5 class="card-title">{{ currentDriller.first_name }} {{ currentDriller.surname }}</h5>
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
        <router-link
          class="btn btn-light btn-sm registries-edit-btn mb-3"
          tag="button"
          to="#"
          v-if="currentDriller.person_guid"><i class="fa fa-plus-square-o"></i> Add application</router-link>
        <div class="card mb-3">
          <div class="card-body p-2 p-md-3">
            <div class="row">
              <div class="col-9">
                <h6 class="card-title mb-3">Personal Information</h6>
              </div>
              <div class="col-3 text-right">
                <button
                  class="btn btn-light btn-sm registries-edit-btn"
                  type="button"
                  @click="editPerson = !editPerson"
                  v-if="currentDriller.person_guid"><i class="fa fa-edit"></i> Edit</button>
              </div>
            </div>
            <person-edit
                  section="person"
                  v-if="editPerson"
                  :record="currentDriller.person_guid"
                  @updated="editPerson = false; updateRecord()"
                  @canceled="editPerson = false"></person-edit>
            <div v-if="!editPerson">
              <div class="row mb-2">
                <div class="col-5 col-md-2 mb-1 mb-sm-0">
                  Surname:
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
                <div class="col-5 col-md-2">
                  Well Driller ORCS:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.well_driller_orcs_no }}
                </div>
                <div class="col-5 col-md-2">
                  Pump Installer ORCS:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.pump_installer_orcs_no }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card mb-3">
          <div class="card-body p-2 p-md-3">
            <div class="row">
              <div class="col-9">
                <h6 class="card-title mb-3">Contact Information</h6>
              </div>
              <div class="col-3 text-right">
                <button
                  class="btn btn-light btn-sm registries-edit-btn"
                  type="button"
                  @click="editContact = !editContact"
                  v-if="currentDriller.person_guid"><i class="fa fa-edit"></i> Edit</button>
              </div>
            </div>
            <person-edit
              section="contact"
              :record="currentDriller.person_guid"
              v-if="editContact"
              @updated="editContact = false; updateRecord()"
              @canceled="editContact = false"></person-edit>
            <div v-if="!editContact">
              <div class="row mb-2">
                <div class="col-5 col-md-2">
                  Email address:
                </div>
                <div class="col-7 col-md-4">
                  <a :href="`mailto:${currentDriller.contact_email}`">{{ currentDriller.contact_email }}</a>
                </div>
                <div class="col-5 col-md-2">
                  Telephone:
                </div>
                <div class="col-7 col-md-4">
                  {{ currentDriller.contact_tel }}
                </div>
              </div>
            </div>
            <div v-if="personTel.length || personEmail.length">
              <div class="row mb-2 mt-5">
                <div class="col-12">
                  <h6 class="card-title mb-3">Additional (Legacy) Contact Information</h6>
                </div>
                <div class="col-5 col-md-2">
                  Email address:
                </div>
                <div class="col-7 col-md-4">
                  <div v-for="(email, index) in personEmail" :key="`person email ${index}`">
                    <a :href="`mailto:${email}`">{{ email }}</a>
                  </div>
                </div>
                <div class="col-5 col-md-2">
                  Telephone:
                </div>
                <div class="col-7 col-md-4">
                  <div v-for="(tel, index) in personTel" :key="`person tel ${index}`">
                    {{ tel }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card mb-3">
          <div class="card-body p-2 p-md-3">
            <div>
              <div v-if="currentDriller.registrations && !currentDriller.registrations.length">
                <h6 class="card-title my-3">Applicant has not yet been added to the register. Submit or approve an application to view or add company information.</h6>
              </div>
              <div v-for="(registration, index) in currentDriller.registrations"
                :key="`company information row ${index}`"
                :class="index > 0 ? 'mt-5' : 'mt-2'">
                  <div class="row">
                  <div class="col">
                    <h6 class="card-title mb-3">{{ registration.activity_description }} Company Information</h6>
                  </div>
                  <div class="col text-right">
                    <button
                      class="btn btn-light btn-sm registries-edit-btn"
                      type="button"
                      @click="editCompany = (editCompany === (index + 1) ? 0 : (index + 1))"
                      v-if="currentDriller.person_guid"><i class="fa fa-refresh"></i> Add/Change</button>
                  </div>
                </div>
                <person-edit
                  section="company"
                  :record="registration"
                  v-if="editCompany === (index + 1)"
                  @updated="editCompany = 0; updateRecord()"
                  @canceled="editCompany = 0"></person-edit>
                <div v-if="registration.organization && editCompany !== (index + 1)">
                  <div class="row mb-2">
                    <div class="col-5 col-md-2 mb-1 mb-sm-0">
                      Company name:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.name }}
                    </div>
                    <div class="col-5 col-md-2">
                      Street address:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.street_address }}
                    </div>
                  </div>
                  <div class="row mb-2">
                    <div class="col-5 col-md-2 mb-1 mb-sm-0">
                      City:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.city }}
                    </div>
                    <div class="col-5 col-md-2">
                      Province:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.province_state }}
                    </div>
                  </div>
                  <div class="row mb-2">
                    <div class="col-5 col-md-2 mb-1 mb-sm-0">
                      Postal Code:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.postal_code }}
                    </div>
                    <div class="col-5 col-md-2">
                      Office number:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.main_tel }}
                    </div>
                  </div>
                  <div class="row mb-2">
                    <div class="col-5 col-md-2 mb-1 mb-sm-0">
                      Cell number:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.surname }}
                    </div>
                    <div class="col-5 col-md-2">
                      Fax number:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.fax_tel }}
                    </div>
                  </div>
                  <div class="row mb-2">
                    <div class="col-5 col-md-2 mb-1 mb-sm-0">
                      Email address:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.contact_email }}
                    </div>
                    <div class="col-5 col-md-2">
                      Website:
                    </div>
                    <div class="col-7 col-md-4">
                      {{ registration.organization.website_url }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <person-notes @updated="updateRecord"></person-notes>
      </div>
    </div>
  </div>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage'
import PersonEdit from '@/registry/components/people/PersonEdit.vue'
import PersonNotes from '@/registry/components/people/PersonNotes.vue'
import { mapGetters } from 'vuex'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER } from '@/registry/store/actions.types'

export default {
  name: 'person-detail',
  components: {
    'api-error': APIErrorMessage,
    'person-edit': PersonEdit,
    PersonNotes
  },
  data () {
    return {
      breadcrumbs: [
        {
          text: 'Registry',
          to: { name: 'SearchHome' }
        },
        {
          text: 'Person Profile',
          active: true
        }
      ],
      editCompany: 0,
      editPerson: false,
      editContact: false
    }
  },
  computed: {
    personEmail () {
      // sort a person's contact info into a list of emails
      const email = []

      // support for contact_info table (legacy data)
      if (this.currentDriller.contact_info && this.currentDriller.contact_info.length) {
        this.currentDriller.contact_info.forEach((item) => {
          if (item.contact_email) {
            email.push(item.contact_email)
          }
        })
      }

      return email
    },
    personTel () {
      const tel = []
      if (this.currentDriller.contact_info && this.currentDriller.contact_info.length) {
        this.currentDriller.contact_info.forEach((item) => {
          if (item.contact_tel) {
            tel.push(item.contact_tel)
          }
        })
      }

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
              code: app.subactivity.registries_subactivity_code,
              description: app.subactivity.description,
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
  methods: {
    updateRecord () {
      this.$store.dispatch(FETCH_DRILLER, this.$route.params.person_guid)
    }
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
    this.updateRecord()
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
