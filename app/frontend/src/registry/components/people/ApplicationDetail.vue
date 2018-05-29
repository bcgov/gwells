/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
  <div class="container">
    <b-card no-body class="mb-3">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <div class="card">
      <div class="card-body">
        <!-- Display loading spinner if application is null -->
        <div v-if="applicationLoading">
          <b-row>
            <b-col md="12">
              <div class="fa-2x text-center">
                <i class="fa fa-circle-o-notch fa-spin"></i>
              </div>
            </b-col>
          </b-row>
        </div>
        <!-- Display application detail once loaded -->
        <div v-else>
          <div v-if="currentDriller != {} && registration != null">
              <h5 class="card-title" id="titlePersonName">{{ titlePersonName }}</h5>
            <div class="col-12" v-if="error">
              <api-error :error="error" resetter="SET_ERROR"></api-error>
            </div>
            <b-col md="12" class="pl-0" v-if="classification">
              <h5>Certification - {{ classification }}</h5>
            </b-col>
          </div>
          <application-edit v-if="editClassification" :activity="activity"/>
          <div v-else>
            <div class="card">
              <div class="card-body">
                <b-row>
                  <b-col md="9">
                    <h5>Classification &amp; Qualifications</h5>
                  </b-col>
                  <b-col md="3" class="text-right">
                    <button
                      class="btn btn-light btn-sm registries-edit-btn"
                      type="button"
                      @click="editClassification = !editClassification"
                      id="editClassification"
                      v-if="userIsAdmin"><i class="fa fa-edit"></i> Edit</button>
                  </b-col>
                </b-row>
                <b-row class="row" v-if="classification && classification.registries_subactivity">
                  <b-col md="12" class="registry-item">
                    <h4>Qualification: {{ classification.registries_subactivity.description }}&nbsp;
                    <span class="registry-subtle">
                      (<router-link :to="{ name: 'PersonDetail', params: { person_guid: currentDriller.person_guid }}">change</router-link>)
                    </span></h4>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col md="2"><span class="registry-label">Issued by:</span></b-col>
                  <b-col md="3">{{ primaryCertificateName }} ({{ primaryCertificateAuth }})</b-col>
                  <b-col md="2"><span class="registry-label">Certificate number:</span></b-col>
                  <b-col md="3">{{ application.primary_certificate_no }}</b-col>
                </b-row>
                <b-row>
                  <b-col md="8" class="pl-3 pt-3">
                    <b-form-group label="Qualified to drill under this classification" label-for="qualifications" class="font-weight-bold">
                      <b-form-checkbox-group id="qualifications" class="fixed-width font-weight-normal" :options="qualificationOptions" v-model="qualifications" disabled>
                      </b-form-checkbox-group>
                    </b-form-group>
                  </b-col>
                </b-row>
              </div>
            </div>
            <div class="card">
              <div class="card-body">
                <h5>Adjudication</h5>
                <div class="row">
                  <div class="col-12 registry-item">
                    <span class="registry-label">Date application received:</span>
                  </div>
                </div>
                <div class="row">
                  <div class="col-12 col-sm-4 registry-item">
                    <span class="registry-label">Approval outcome date:</span>
                  </div>
                  <div class="col-12 col-sm-4 registry-item">
                    <span class="registry-label">Approval outcome:</span>
                  </div>
                  <div class="col-12 col-sm-4 registry-item">
                    <span class="registry-label">Reason not approved:</span>
                  </div>
                </div>
                <div class="row">
                  <div class="col-12 col-sm-4 registry-item">
                    <span class="registry-label">Register removal date:</span>
                  </div>
                </div>
                <!-- <div class="row">
                  <div class="col-12 registry-item">
                    <div class="checkbox form-inline">
                      <label>
                        <input type="checkbox" style="margin-top:-4px;" class="registry-disabled-item" disabled><span style="color: #808080">As Deputy Comptroller, I confirm I have reviewed the application or action and approved this registry update.</span>
                      </label>
                    </div>
                  </div>
                </div> -->
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
import { mapGetters, mapActions } from 'vuex'
import { SET_DRILLER, SET_ERROR } from '@/registry/store/mutations.types'
import { FETCH_DRILLER, FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import ApplicationAdd from '@/registry/components/people/ApplicationAdd.vue'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'PersonApplicationDetail',
  components: {
    'api-error': APIErrorMessage,
    'r-checkbox': QualCheckbox,
    'application-edit': ApplicationAdd
  },
  data () {
    return {
      breadcrumbs: [
        {
          text: 'Registry',
          to: { name: 'SearchHome' }
        },
        {
          text: 'Profile',
          to: { name: 'PersonDetail', params: { person_guid: this.$route.params.person_guid } }
        },
        {
          text: `Classification`,
          active: true
        }
      ],
      editClassification: false,
      registration: null
    }
  },
  methods: {
    ...mapActions([
      FETCH_DRILLER_OPTIONS
    ])
  },
  computed: {
    classification () {
      return this.application ? this.application.subactivity.description : null
    },
    application () {
      return this.registration ? this.registration.applications.find((item) => item.application_guid === this.$route.params.application_guid) : null
    },
    activity () {
      return this.registration ? this.registration.registries_activity : null
    },
    qualificationOptions () {
      if (this.drillerOptions && this.activity in this.drillerOptions) {
        return this.drillerOptions[this.activity].WellClassCode.map((item) => { return {'text': item.description, 'value': item.registries_well_class_code} })
      }
      return []
    },
    qualifications () {
      if (this.application) {
        return this.application.qualifications
      }
      return []
    },
    applicationLoading () {
      return this.loading || this.drillerOptions === null || this.registration === null || this.application === null
    },
    primaryCertificateName () {
      return this.application && this.application.primary_certificate ? this.application.primary_certificate.name : null
    },
    primaryCertificateAuth () {
      return this.application && this.application.primary_certificate ? this.application.primary_certificate.cert_auth : null
    },
    titlePersonName () {
      let title = `${this.currentDriller.first_name} ${this.currentDriller.surname}`
      if (this.registration.registration_no) {
        title += ` - ${this.registration.registration_no}`
      }
      return title
    },
    ...mapGetters([
      'loading',
      'error',
      'currentDriller',
      'userIsAdmin',
      'drillerOptions'
    ])
  },
  created () {
    // if (this.currentDriller.person_guid !== this.$route.params.person_guid) {
    //   this.$store.commit(SET_DRILLER, {})
    // }
    // this.$store.dispatch(FETCH_DRILLER, this.$route.params.person_guid)

    this.FETCH_DRILLER_OPTIONS()

    // We fetch the entire registration with all applications because we need a reference to the registration
    // activity.
    ApiService.get('registrations', this.$route.params.registration_guid)
      .then((response) => {
        this.registration = response.data
      })
      .catch((error) => {
        this.$store.commit(SET_ERROR, error.response)
      })
  }
}
</script>

<style>
.registry-section {
  margin-top: 25px;
  margin-bottom: 20px;
}
.registry-disabled-item {
  color: #808080;
  cursor: auto!important;
}
.qualification-item {
  margin-bottom: 5px;
}
.registry-subtle {
  font-size: 0.9rem;
}
.fixed-width .custom-control-label {
  width: 220px;
}
</style>
