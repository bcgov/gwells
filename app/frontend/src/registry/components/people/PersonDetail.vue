<template>
  <div class="rounded-lg ml-20 mr-20 bg-white mb-4 px-12">
    <Breadcrumb :model="breadcrumbs"></Breadcrumb>
  </div>
  <div v-if="showSpinner" class="rounded-lg ml-20 mr-20 bg-white mb-4 px-12">
    <div class="fa-2x text-center">
      <i class="fa fa-circle-o-notch fa-spin"></i>
    </div>
  </div>
  <Card v-else class="rounded-lg ml-20 mr-20 bg-white">
    <template #header>
      <div class="col-12" v-if="commonStore.filesUploading">
        <Message severity="info" show>File Upload In Progress...</Message>
      </div>
      <div class="col-12" v-if="!commonStore.filesUploading && commonStore.fileUploadError">
        <Message show severity="warn" >File Upload Errors: {{commonStore.fileUploadErrors.map((e) => e.response.statusText)}}</Message>
      </div>
      <div class="col-12" v-if="!commonStore.filesUploading && commonStore.fileUploadSuccess">
        <Message show severity="success" >Successfully uploaded all files</Message>
      </div>
    </template>
    <template #content>
      <div v-if="currentDriller != {}">
        <div class="row">
          <div class="col-12">
            <h4 class="card-title">{{ currentDriller.first_name }} {{ currentDriller.surname }}</h4>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-12" v-if="error">
          <api-error :error="error" :on-clear="() => registryStore.setError(null)"></api-error>
        </div>
      </div>

      <!-- Personal information -->
      <div class="mb-4">
        <div class="p-2 p-md-3">
          <div class="grid grid-cols-12">
            <div class="col-9">
              <h5 class="card-title mb-4">Personal Information</h5>
            </div>
            <div class="col-3 text-right">
              <button
                class="btn btn-light btn-sm registries-edit-btn"
                type="button"
                @click="editPerson = !editPerson"
                v-if="currentDriller.person_guid && commonStore.userRoles.registry.edit"><i class="fa fa-edit"></i> Edit</button>
            </div>
          </div>
          <person-edit
            section="person"
            v-if="editPerson && commonStore.userRoles.registry.edit"
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

      <!-- Registrations -->
      <div class="card mb-4"
          v-for="(registration, index) in currentDriller.registrations"
          :key="`registration ${index}`">
        <div class="card-body p-2 p-md-3">
          <h5 class="card-title">{{ registration.activity_description }} Registration</h5>

          <!-- Classifications -->
          <h6>Classifications</h6>
          <div class="mb-4">
            <div class="table-responsive">
              <table id="classification-table" class="table">
                <thead>
                  <tr>
                    <th>Classification</th>
                    <th>Register Status</th>
                    <th>Date Registered</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                      v-for="(item, index_c) in classifications.filter((item) => {
                        return item.activity === registration.registries_activity
                      })" :key="`reg ${index} class ${index_c}`">
                    <td><router-link :to="{
                      name: 'ApplicationDetail',
                      params: { person_guid: currentDriller.person_guid, registration_guid: item.registration_guid, application_guid: item.application_guid } }">
                    {{ item.description }}</router-link></td>
                    <td>{{ item.status }}</td>
                    <td>{{ item.date }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="show(registration.registries_activity)">
              <Form @submit.prevent="saveApplication(registration.registries_activity)">
                <application-add
                    class="mb-4"
                    v-on:close="closeApplication(registration.registries_activity)"
                    :modelValue="getApplication(registration.registries_activity)"
                    :activity="registration.registries_activity"
                    mode="edit">
                    <button type="submit" class="btn btn-primary" variant="primary">Save</button>
                    <button type="button" class="btn btn-light" @click="closeApplication(registration.registries_activity)">Cancel</button>
                </application-add>
              </Form>
            </div>
            <div v-else>
              <Button
                v-if="commonStore.userRoles.registry.edit"
                label="Add classification"
                size="small"
                v-on:click="addApplication(registration)"
                class="mb-4 registries-action-button" />
            </div>
          </div>

          <!-- Registration information -->
          <div class="row">
            <div class="col">
              <h6 class="card-title mb-4">{{ registration.activity_description }} Registration Details</h6>
            </div>
            <div class="col text-right">
              <button
                class="btn btn-light btn-sm registries-edit-btn"
                type="button"
                @click="editRegistration = (editRegistration === (index + 1) ? 0 : (index + 1))"
                v-if="commonStore.userRoles.registry.edit">
                <span><i class="fa fa-edit"></i> Edit</span>
                </button>
            </div>
          </div>
          <person-edit
            class="mb-6"
            section="registration"
            :record="registration"
            v-if="editRegistration === (index + 1) && commonStore.userRoles.registry.edit"
            @updated="editRegistration = 0; updateRecord()"
            @canceled="editRegistration = 0"></person-edit>
          <div v-if="editRegistration !== (index + 1)">
            <div class="row mb-6">
              <div class="col-5 col-md-2">
                Registration number:
              </div>
              <div class="col-7 col-md-4">
                {{ registration.registration_no }}
              </div>
            </div>
          </div>

          <!-- Company information -->
          <div class="row">
            <div class="col">
              <h6 class="card-title mb-4">{{ registration.activity_description }} Company Information</h6>
            </div>
            <div class="col text-right">
              <button
                class="btn btn-light btn-sm registries-edit-btn"
                type="button"
                @click="editCompany = (editCompany === (index + 1) ? 0 : (index + 1))"
                v-if="currentDriller.person_guid && commonStore.userRoles.registry.edit">
                <span v-if="!registration.organization"><i class="fa fa-plus"></i> Add company</span>
                <span v-else><i class="fa fa-refresh"></i> Change company</span>
                </button>
            </div>
          </div>
          <person-edit
            section="company"
            :record="registration"
            v-if="editCompany === (index + 1) && commonStore.userRoles.registry.edit"
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
                Email Address:
              </div>
              <div class="col-7 col-md-4">
                {{ registration.organization.email }}
              </div>
              <div class="col-5 col-md-2">
                Fax number:
              </div>
              <div class="col-7 col-md-4">
                {{ registration.organization.fax_tel }}
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-5 col-md-2">
                Website:
              </div>
              <div class="col-7 col-md-4">
                {{ registration.organization.website_url }}
              </div>
            </div>
          </div>
          <div v-else-if="!registration.organization && editCompany !== (index + 1)">
            No {{ registration.activity_description }} company.
          </div>
        </div>
      </div>

      <!-- new registrations -->
      <div class="card mb-4" v-if="commonStore.userRoles.registry.edit && (!currentDriller.registrations || currentDriller.registrations.length !== 2)">
        <div class="card-body p-2 p-md-3">
          <div
            v-for="(item, index) in registrationOptions.filter((item) => {
                return !currentDriller.registrations.some(reg => reg.registries_activity === item.code)
              })"
            :key="`unregistered activity ${index}`">
            <Button
              label="Register as a {{ item.desc }}"
              variant="primary"
              class="my-1 registries-action-button"
              :ref="`registerButton${item.code}`"
              @click="confirmRegisterModal[item.code]=true"
            />
            <Dialog
                v-model="confirmRegisterModal[item.code]"
                v-model:visible="visible"
                centered
                modal
                header="`Confirm register as ${item.desc}`"
                @shown="$refs[`confirmRegisterConfirmBtn${item.code}`][0].focus()"
                :return-focus="$refs[`registerButton${item.code}`]">
              Are you sure you want to register {{ currentDriller.first_name }} {{ currentDriller.surname }} as a {{ item.desc }}?
              <div slot="modal-footer">
                <Button
                  label="Confirm"
                  variant="primary"
                  @click="confirmRegisterModal[item.code]=false;submitRegistration(item.code)"
                  :ref="`confirmRegisterConfirmBtn${item.code}`"
                  id="register-confirm"/>
                <Button label="Cancel" variant="light" @click="confirmRegisterModal[item.code]=false" id="register-cancel"/>
              </div>
            </Dialog>
          </div>
        </div>
      </div>

      <!-- Contact Information -->
      <div class="card mb-4">
        <div class="card-body p-2 p-md-3">
          <div class="row">
            <div class="col-9">
              <h6 class="card-title mb-4">Contact Information at Company</h6>
            </div>
            <div class="col-3 text-right">
              <button
                class="btn btn-light btn-sm registries-edit-btn"
                type="button"
                @click="editContact = !editContact"
                v-if="currentDriller.person_guid && commonStore.userRoles.registry.edit"><i class="fa fa-edit"></i> Edit</button>
            </div>
          </div>
          <person-edit
            section="contact"
            :record="currentDriller.person_guid"
            v-if="editContact && commonStore.userRoles.registry.edit"
            @updated="editContact = false; updateRecord()"
            @canceled="editContact = false"></person-edit>
          <div v-if="!editContact">
            <div class="row mb-2">
              <div class="col-12 col-md-4">
                <span class="contact-label">Email address: </span><a :href="`mailto:${currentDriller.contact_email}`">{{ currentDriller.contact_email }}</a>
              </div>
              <div class="col-12 col-md-4">
                <span class="contact-label">Telephone: </span>{{ currentDriller.contact_tel }}
              </div>
              <div class="col-12 col-md-4">
                <span class="contact-label">Cell: </span>{{ currentDriller.contact_cell }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Notes -->
      <person-notes @updated="updateRecord"></person-notes>

      <div class="card mb-4">
        <div class="card-body p-2 p-md-3">
          <div class="row">
            <div class="col-9">
              <h5 class="card-title mb-4">Attachments</h5>
            </div>
          </div>
          <div class="mt-4">
            <label>Upload Documents
              <FileUpload
                v-model="files"
                multiple
                plain/>
              <div class="mt-4" v-if="commonStore.uploadFiles.length > 0">
                <ul>
                  <li v-for="(f, index) in uploadFiles" :key="index">{{f.name}}</li>
                </ul>
              </div>
            </label>
          </div>
          <div class="mt-4">
            <person-documents :files="person_files"
              v-on:fetchFiles="fetchFiles"
              :guid="currentDriller.person_guid"></person-documents>
          </div>
          <div slot="modal-footer">
            <Button label="Save" variant="primary" @click="uploadAttachments()" :disabled="variant.uploadFiles.length === 0" />
            <Button label="Cancel" variant="light" @click="cancelUploadAttachments" />
          </div>
        </div>
      </div>

      <!-- Change history for this record -->
      <change-history
        ref="changeHistory"
        class="my-4"
        v-if="!!currentDriller"
        resource="person"
        :id="currentDriller.person_guid"></change-history>
    </template>
  </Card>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import PersonEdit from '@/registry/components/people/PersonEdit.vue'
import PersonNotes from '@/registry/components/people/PersonNotes.vue'
import ChangeHistory from '@/common/components/ChangeHistory.vue'
import ApplicationAddEdit from '@/registry/components/people/ApplicationAddEdit.vue'
import ApiService from '@/common/services/ApiService.js'
import { useRegistryStore } from '@/stores/registry.js'
import PersonDocuments from './PersonDocuments.vue'

export default {
  name: 'person-detail',
  components: {
    'person-documents': PersonDocuments,
    'api-error': APIErrorMessage,
    'person-edit': PersonEdit,
    'application-add': ApplicationAddEdit,
    ChangeHistory,
    PersonNotes
  },
  data () {
    return {
      drillApplication: null,
      pumpApplication: null,
      breadcrumbs: [
        { label: 'Registry', url: '/registries' },
        { label: 'Person Profile' }
      ],
      editCompany: 0,
      editRegistration: 0,
      editPerson: false,
      editContact: false,
      savingApplication: false,
      registrationOptions: [
        {
          code: 'DRILL',
          desc: 'Well Driller'
        },
        {
          code: 'PUMP',
          desc: 'Well Pump Installer'
        }
      ],
      confirmRegisterModal: {
        DRILL: false,
        PUMP: false
      },
      person_files: {},
      registryStore: useRegistryStore()
    }
  },
  computed: {
    error () { return this.registryStore.error },
    currentDriller () { return this.registryStore.currentDriller },
    searchResponse () { return this.registryStore.searchResponse },
    loading () { return this.registryStore.loading },
    files: {
      get: function () {
        return this.uploadFiles
      },
      set: function (value) {
        this.commonStore.setFiles(value)
      }
    },
    showSpinner () {
      return this.currentDriller == null || this.loading || this.savingApplication
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
            let status = null
            if (app.removal_date) {
              status = 'Removed'
            } else if (app.current_status) {
              status = app.current_status.description
            }
            classifications.push({
              code: app.subactivity.registries_subactivity_code,
              description: app.subactivity.description,
              status: status,
              date: app.application_outcome_date,
              registration_guid: reg.register_guid,
              application_guid: app.application_guid,
              activity: reg.registries_activity
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
    commonStore () { return useCommonStore() },
  },
  methods: {
    show (key) {
      return ((key === 'PUMP' && this.pumpApplication) || (key === 'DRILL' && this.drillApplication))
    },
    getApplication (key) {
      if (key === 'PUMP') {
        return this.pumpApplication
      } else if (key === 'DRILL') {
        return this.drillApplication
      }
      return null
    },
    updateRecord () {
      this.registryStore.fetchDriller(this.$route.params.person_guid)
      // update changeHistory when company is updated
      if (this.currentDriller && this.$refs.changeHistory) {
        this.$refs.changeHistory.update()
      }
      this.fetchFiles()
    },
    addApplication (registration) {
      const newClassification = {
        registration: registration.register_guid
      }
      if (registration.registries_activity === 'PUMP') {
        this.pumpApplication = newClassification
      } else if (registration.registries_activity === 'DRILL') {
        this.drillApplication = newClassification
      }
    },
    closeApplication (key) {
      if (key === 'PUMP') {
        this.pumpApplication = null
      } else if (key === 'DRILL') {
        this.drillApplication = null
      }
    },
    saveApplication (key) {
      let application = this.getApplication(key)
      this.savingApplication = true
      ApiService.post('applications', application).then(() => {
        this.closeApplication(key)
        this.savingApplication = false
        this.updateRecord()
      }).catch(() => {
        this.savingApplication = false
      })
    },
    submitRegistration (activity) {
      const data = {
        person: this.currentDriller.person_guid,
        registries_activity: activity
      }
      ApiService.post('registrations', data).then(() => {
        this.updateRecord()
      })
    },
    cancelUploadAttachments () {
      this.commonStore.setFiles([])
    },
    uploadAttachments () {
      if (this.commonStore.uploadFiles.length > 0) {
        this.commonStore.uploadTheFiles({
          documentType: 'drillers',
          recordId: this.currentDriller.person_guid
        }).then(() => {
          this.commonStore.fileUploadSucceeded()
          this.fetchFiles()
          window.scrollTo(0, 0)
        }).catch((error) => {
          this.commonStore.fileUploadFail()
          console.error(error)
          window.scrollTo(0, 0)
        })
      }
    },
    fetchFiles () {
      ApiService.query(`drillers/${this.$route.params.person_guid}/files`)
        .then((response) => {
          this.person_files = response.data
        })
    }
  },
  created () {
    if (this.currentDriller.person_guid !== this.$route.params.person_guid) {
      this.registryStore.setDriller({})
      if (this.searchResponse && this.searchResponse.results && this.searchResponse.results.length) {
        const driller = this.searchResponse.results.find((item) => {
          return item.person_guid === this.$route.params.person_guid
        })
        if (driller) {
          this.registryStore.setDriller(driller)
        }
      }
    }
    this.updateRecord()
    this.registryStore.fetchDrillerOptions()
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
.contact-label {
  margin-right: 1rem;
}
</style>
