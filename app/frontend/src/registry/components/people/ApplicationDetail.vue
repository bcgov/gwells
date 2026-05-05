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
    <Card no-body class="mb-4">
      <Breadcrumb :model="breadcrumbs" class="py-0 my-2"></Breadcrumb>
    </Card>
    <div class="card">
      <div class="card-body">
        <!-- Display loading spinner if application is null -->
        <div v-if="applicationLoading">
          <div class="fa-2x text-center">
            <i class="fa fa-circle-o-notch fa-spin"></i>
          </div>
        </div>
        <!-- Display application detail once loaded -->
        <div v-else>
          <div v-if="currentDriller != {} && registration != null">
            <h5 class="card-title" id="titlePersonName">{{ titlePersonName }}</h5>
            <div class="pl-0" v-if="classification">
              <h5>Certification - {{ classification }}</h5>
            </div>
          </div>
          <div v-if="editClassification">
            <Form @submit.prevent="saveApplication()" @reset.prevent="applicationReset()">
              <Dialog
                  v-model="confirmCancelModal"
                  v-model:visible="visible"
                  centered
                  modal
                  header="Confirm cancel"
                  @shown="focusCancelModal"
                  :return-focus="$refs.cancelClassification">
                Your changes are not saved. Are you sure you want to discard your changes?
                <template #footer>
                  <Button severity="secondary" id="confirmCancel" @click="confirmCancelModal=false" ref="cancelSubmitCancelBtn">
                    Cancel
                  </Button>
                  <Button severity="danger" id="discardChanges" @click="confirmCancelModal=false;editClassification=false;applicationReset();">
                    Discard
                  </Button>
                </template>
              </Dialog>
              <div>
                <application-edit
                  :activity="activity"
                  v-model="applicationFormValue"
                  mode="edit"
                  v-on:isValid="onApplicationIsValid"
                  v-on:close="confirmCancelModal=true"/>
              </div>
              <div class="mt-4">
                  <button type="submit" class="btn btn-primary" id="saveClassification">Save</button>
                  <button type="button" class="btn btn-primary" id="cancelClassification" v-on:click="confirmCancelModal=true">Cancel</button>
              </div>
            </Form>
          </div>
          <div v-else>
            <div class="card mb-4">
              <div class="card-body">
                <div>
                  <h5>Classification &amp; Qualifications</h5>
                  <div class="text-right">
                    <button
                      class="btn btn-light btn-sm registries-edit-btn"
                      type="button"
                      @click="editClassification = !editClassification"
                      id="editClassification"
                      v-if="commonStore.userRoles.registry.edit"><i class="fa fa-edit" id="editClassification"></i> Edit</button>
                  </div>
                </div>
                <div class="row" v-if="classification && classification.registries_subactivity">
                  <div class="registry-item">
                    <h4>Qualification: {{ classification.registries_subactivity.description }}&nbsp;
                    <span class="registry-subtle">
                      (<router-link :to="{ name: 'PersonDetail', params: { person_guid: currentDriller.person_guid }}">change</router-link>)
                    </span>
                    </h4>
                  </div>
                </div>
                <div>
                  <div><span class="registry-label">Issued by:</span></div>
                  <div>{{ primaryCertificateName }} ({{ primaryCertificateAuth }})</div>
                  <div><span class="registry-label">Certificate number:</span></div>
                  <div>{{ application.primary_certificate_no }}</div>
                </div>
                <div>
                  <div class="pl-4 pt-4">
                      <label for="qualifications" class="font-weight-bold">
                        {{ `Qualified ${activity === 'DRILL' ? 'to drill ' : ''}under this classification` }}
                          <div class="col-12">
                            <CheckboxGroup v-model="qualifications">
                              <div v-for="q in qualificationOptions" :key="q.value">
                                <Checkbox
                                  inputId="qualifications"
                                  name="qualifications"
                                  value="q.value"
                                  class="fixed-width font-weight-normal"
                                  disabled
                                  />
                                <label :for="q.value">{{ q.text }}</label>
                              </div>
                            </CheckboxGroup>
                          </div>
                    </label>
                  </div>
                </div>
                <div>
                  <h5>Adjudication</h5>
                </div>
                <div>
                  <div>
                    Confirmed applicant is 19 years of age or older by reviewing: {{ proofOfAge }}
                  </div>
                </div>
                <div>
                  <div class="registry-item pr-0">
                    <span class="registry-label">Date application received:</span>
                  </div>
                  <div v-if="application && application.application_recieved_date">
                      {{ application.application_recieved_date }}
                  </div>
                  <div v-else>Unknown</div>
                </div>
                <div>
                  <div class="registry-item">
                    <span class="registry-label">Approval outcome date:</span>
                  </div>
                  <div v-if="application && application.application_outcome_date">
                    {{ application.application_outcome_date }}
                  </div>
                  <div v-else>Unknown</div>
                  <div class="registry-item">
                    <span class="registry-label">Approval outcome:</span>
                  </div>
                  <div v-if="application && application.current_status">
                    {{ application.current_status.description }}
                  </div>
                  <div v-else>Unknown</div>
                  <div v-if="application && application.current_status && application.current_status.code === 'NA'" class="registry-item">
                    <span class="registry-label">Reason denied:</span>
                  </div>
                  <div v-if="application && application.current_status && application.current_status.code === 'NA'">
                    <span v-if="application.reason_denied">
                      {{ application.reason_denied }}
                    </span>
                    <span v-else>
                      Unknown
                    </span>
                  </div>
                </div>
                <div>
                  <div class="registry-item">
                    <span class="registry-label">Notification date:</span>
                  </div>
                  <div v-if="application && application.application_outcome_notification_date">
                    {{ application.application_outcome_notification_date }}
                  </div>
                  <div v-else>Unknown</div>
                </div>
                <div v-if="removalDate || removalReason">
                  <div class="pt-4"><h6>Removal of classification from register</h6></div>
                </div>
                <div v-if="removalDate || removalReason">
                  <div><span class="registry-label">Removal date:</span></div>
                  <div>{{removalDate}}</div>
                  <div><span class="registry-label">Removal reason:</span></div>
                  <div v-if="removalReason">{{removalReason.description}}</div>
                  <div v-else>Unknown</div>
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
import { useCommonStore } from '@/stores/common.js'
import { useRegistryStore } from '@/stores/registry.js'
import ApplicationAddEdit from '@/registry/components/people/ApplicationAddEdit.vue'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'PersonApplicationDetail',
  components: {
    'application-edit': ApplicationAddEdit
  },
  data () {
    return {
      registryStore: useRegistryStore(),
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
      registration: null,
      applicationFormValue: null,
      editClassification: false,
      confirmCancelModal: false,
      applicationSaving: false,
      formValid: true
    }
  },
  methods: {
    applicationReset () {
      this.registration = null
      this.applicationFormValue = null
      this.formValid = true
      // We fetch the entire registration with all applications because we need a reference to the registration
      // activity.
      ApiService.get('registrations', this.$route.params.registration_guid)
        .then((response) => {
          this.registration = response.data
          if (this.registration) {
            let application = this.registration.applications.find((item) => item.application_guid === this.$route.params.application_guid)
            this.applicationFormValue = {
              subactivity: {
                registries_subactivity_code: application.subactivity.registries_subactivity_code
              },
              primary_certificate_no: application.primary_certificate_no,
              primary_certificate: {
                acc_cert_guid: application.primary_certificate.acc_cert_guid
              },
              current_status: application.current_status,
              qualifications: application.qualifications,
              proof_of_age: application.proof_of_age ? application.proof_of_age : {},
              reason_denied: application.reason_denied,
              application_outcome_date: application.application_outcome_date,
              application_outcome_notification_date: application.application_outcome_notification_date,
              application_recieved_date: application.application_recieved_date,
              removal_reason: application.removal_reason,
              removal_date: application.removal_date
            }
          }
        })
        .catch((error) => {
          this.registryStore.setError(error.response)
        })
    },
    focusCancelModal () {
      // focus the "cancel" button in the confirm discard popup
      this.$refs.cancelSubmitCancelBtn.focus()
    },
    saveApplication () {
      if (this.formValid) {
        this.applicationSaving = true
        const copy = Object.assign({}, this.applicationFormValue)
        delete copy['qualifications'] // This section is read-only. No point pushing it to server.
        ApiService.patch('applications', this.$route.params.application_guid, copy).then(() => {
          this.editClassification = false
          this.applicationSaving = false
          this.applicationReset()
        }).catch((error) => {
          this.applicationSaving = false
          this.registryStore.setError({ status: 'Error saving application' })
          console.error(error)
        })
      }
    },
    onApplicationIsValid (event) {
      this.formValid = event
    }
  },
  computed: {
    classification () {
      let description = null
      if (this.application && this.application.subactivity) {
        description = this.application.subactivity.description
      }
      return description
    },
    activity () {
      return this.registration ? this.registration.registries_activity : null
    },
    qualificationOptions () {
      if (this.drillerOptions && this.activity in this.drillerOptions) {
        return this.drillerOptions[this.activity].well_class_codes.map((item) => { return { 'text': item.description, 'value': item.registries_well_class_code } })
      }
      return []
    },
    qualifications () {
      console.log(this.application.qualifications)
      if (this.application) {
        return this.application.qualifications
      }
      return []
    },
    application () {
      return this.registration ? this.registration.applications.find((item) => item.application_guid === this.$route.params.application_guid) : null
    },
    applicationLoading () {
      return this.loading || this.drillerOptions === null || this.registration === null || this.application === null || this.applicationSaving === true
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
    proofOfAge () {
      let description = null
      if (this.application && this.application.proof_of_age) {
        description = this.application.proof_of_age.description
      }
      return description
    },
    removalDate () {
      return this.application ? this.application.removal_date : null
    },
    removalReason () {
      return this.application ? this.application.removal_reason : null
    },
    commonStore () { return useCommonStore() },
    loading () { return this.registryStore.loading },
    error () { return this.registryStore.error },
    currentDriller () { return this.registryStore.currentDriller },
    drillerOptions () { return this.registryStore.drillerOptions }
  },
  created () {
    this.registryStore.fetchDrillerOptions()
    this.applicationReset()
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
