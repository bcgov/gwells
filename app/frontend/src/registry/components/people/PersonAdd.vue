<template>
  <div class="rounded-lg ml-20 mr-20 bg-white mb-3 px-5">
    <Breadcrumb :model="breadcrumbs"></Breadcrumb>
  </div>
  <div class="rounded-lg ml-20 mr-20 bg-white mb-3 px-5" v-if="error">
    <api-error :error="error" :on-clear="() => registryStore.setError(null)"></api-error>
  </div>
  <Card class="rounded-lg ml-20 mr-20 bg-white">
    <template #title>Add new applicant</template>
    <template #content>
      <Form @submit.prevent="onFormSubmit()" @reset.prevent="onFormReset()">
        <h6 class="font-weight-bold mb-2">Personal Information</h6>
        <div class="mb-3 grid md:grid-cols-2 gap-3">
          <div class="grid grid-flow-col grid-rows-3">
            <label for="surnameInput">Surname:</label>
            <InputText
              id="surnameInput"
              type="text"
              class="mr-100"
              v-model="drillerForm.person.surname"
              required/>
          </div>
          <div class="grid grid-flow-col grid-rows-3">
            <label for="firstnameInput">First name:</label>
            <InputText
              id="firstnameInput"
              type="text"
              class="mr-100"
              v-model="drillerForm.person.first_name"
              required/>
          </div>
        </div>
        <div class="mt-3">
          <h6 class="font-weight-bold mb-2">Contact Information at Company</h6>
          <div class="mb-3 grid md:grid-cols-2 gap-3">
            <div class="grid grid-flow-col grid-rows-3">
              <label for="contactTelInput" aria-describedby="drillerTelExample">Telephone number:</label>
              <InputMask
                  id="contactTelInput"
                  type="tel"
                  mask="(999) 999-9999"
                  class="mr-100"
                  v-model="drillerForm.person.contact_tel"/>
              <small id="drillerTelExample" class="form-text text-muted">
                Example: (250) 555-1234
              </small>
            </div>
            <div class="grid grid-flow-col grid-rows-3">
              <label for="contactEmailInput">Email:</label>
              <InputText
                id="contactEmailInput"
                type="email"
                class="mr-100"
                :state="validation.contact_email"
                aria-describedby="contactEmailFeedback"
                v-model="drillerForm.person.contact_email"/>
              <div id="contactEmailFeedback" class="invalid-feedback">
                <div v-for="(error, index) in fieldErrors.contact_email" :key="`emailInput error ${index}`">
                  {{ error }}
                </div>
              </div>
            </div>
          </div>

        </div>
        <div class="mt-3">
          <h6 class="font-weight-bold mb-2">ORCS File Number</h6>
          <div class="mb-3 grid md:grid-cols-2 gap-3">
            <div class="grid grid-flow-col grid-rows-3">
              <label for="drillerORCSInput" aria-describedby="drillerORCSExample">Well Driller ORCS Number:</label>
              <InputText
                id="drillerORCSInput"
                type="text"
                class="mr-100"
                v-model="drillerForm.person.well_driller_orcs_no"/>
              <small id="drillerORCSExample">
                ORCS format: 38000-25/DRI XXXX X
              </small>
            </div>
            <div class="grid grid-flow-col grid-rows-3">
              <label for="pumpORCSInput" aria-describedby="pumpORCSExample">Pump Installer ORCS Number:</label>
              <InputText
                id="pumpORCSInput"
                type="text"
                class="mr-100"
                v-model="drillerForm.person.pump_installer_orcs_no"/>
              <small id="pumpORCSExample">
                ORCS format: 38000-25/PUMP XXXX X
              </small>
            </div>
          </div>
        </div>
        <div class="grid grid-flow-col grid-rows-3">
          <label for="registrationTypeInput">Register as: </label>
          <CheckboxGroup id="registrationTypeInput" name="registrationType" v-model="drillerForm.regType" class="flex flex-row gap-3">
            <Checkbox inputId="registrationTypeInputDrill"
                value="DRILL"
                v-model="drillerForm.regType"/>
              <label for="registrationTypeInputDrill">Well Driller</label>
              <Checkbox inputId="registrationTypeInputPump"
                value="PUMP"
                v-model="drillerForm.regType"/>
              <label for="registrationTypeInputPump">Well Pump Installer</label>
            </CheckboxGroup>
        </div>
        <div class="mt-3">
          <h6 class="font-weight-bold mb-2">Attachments</h6>
          <FileUpload ref="fileupload" name="files[]" url="/api/files/upload" :auto="true" :multiple="true" :customUpload="true" @upload="onFormSubmit" v-model="files"/>
          <div class="mt-3" v-if="commonStore.uploadFiles.length > 0">
            <Listbox v-for="(f, index) in commonStore.uploadFiles" :key="index">{{f.name}}</Listbox>
          </div>
        </div>
        <Card no-body class="mb-3 p-1 p-md-3" v-if="drillerForm.regType.some(x => x === 'DRILL' || x === 'PUMP')">
          <div>
            <Message :show="newOrgSuccess"
                    dismissible
                    variant="success"
                    severity="success"
                    @dismissed="newOrgSuccess=false"
                    class="mb-3">
              Company added.
            </Message>
            <div class="text-right">
              <Button
                type="button"
                v-b-modal.orgModal
                variant="primary"
                size="sm"
                class="py-0">
                <i class="fa fa-plus-square-o"></i>
                Add a company
              </Button>
            </div>
          </div>
          <organization-add @newOrgAdded="newOrgHandler"></organization-add>
          <div v-if="drillerForm.regType.some(x => x === 'DRILL')" :class="drillerForm.regType.some(x => x === 'PUMP') ? 'mb-5' : 'mb-1' ">
            <h5>Well Driller Registration</h5>
            <div class="mb-3">
              <label for="companyInput">Well drilling company:</label>
              <Select
                v-model="drillerForm.organizations.drill"
                :options="companies"
                placeholder="Begin typing a company name"
                label="org_verbose_name">
              </Select>
            </div>
            <div class="mb-3">
              <h6 class="font-weight-normal">Well Driller Classifications</h6>
              <application-add
                class="mb-3"
                v-for="item in drillApplications"
                v-bind:item="item"
                v-bind:key="item.id"
                v-on:close="closeApplication (drillApplications, item.id)"
                v-model="item.data"
                activity="DRILL"
                mode="add"/>
            </div>
            <div>
              <Button
                type="button"
                variant="primary"
                size="sm"
                v-on:click="addApplication (drillApplications)"
                class="mb-3">
                <i class="fa fa-plus-square-o"></i>
                Add new well driller classification
              </Button>
            </div>
          </div>
          <div v-if="drillerForm.regType.some(x => x === 'PUMP')" class="my-2">
            <h5>Well Pump Installer Registration</h5>
            <div class="mb-3">
              <label
                id="companyInputGroup"
                label="Well pump installation company:"
                label-for="companyInput">
                <v-select
                  v-model="drillerForm.organizations.pump"
                  :options="companies"
                  placeholder="Begin typing a company name"
                  label="org_verbose_name">
                </v-select>
              </label>
            </div>
            <div class="mb-3">
              <h6 class="font-weight-normal">Well Pump Installer Classifications</h6>
              <application-add
                class="mb-3"
                v-for="item in pumpApplications"
                v-bind:item="item"
                v-bind:key="item.id"
                v-on:close="closeApplication (pumpApplications, item.id)"
                v-model="item.data"
                activity="PUMP"
                mode="add"/>
            </div>
            <div class="mb-3">
              <Button
                type="button"
                variant="primary"
                size="sm"
                v-on:click="addApplication(pumpApplications)"
                class="mb-3"><i class="fa fa-plus-square-o"></i> Add new pump installer classification</Button>
            </div>
          </div>
        </Card>
        <div class="mt-3">
          <Button type="submit" class="mr-2">Save</Button>
          <Button type="reset" severity="secondary">Reset</Button>
        </div>
        <div class="mt-3">
          <Message
            v-if="submitSuccess"
            :closable="true"
            severity="success"
            @close="submitSuccess=false">
            Successfully created a new person!
          </Message>
          <Message
            v-if="submitError"
            :closable="true"
            severity="warn"
            @close="submitError=false">
            Error creating a new person.
            <div v-for="(value, key, index) in submitError.data" :key="`submit error ${index}`">
              <span class="text-capitalize">{{ key }}</span>:
              <span
                v-for="(msg, msgIndex) in value"
              :key="`submit error msg ${index} ${msgIndex}`">{{ msg }}
              </span>
            </div>
          </Message>
        </div>
      </Form>
    </template>
  </Card>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import ApiService from '@/common/services/ApiService.js'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'
import ApplicationAddEdit from '@/registry/components/people/ApplicationAddEdit.vue'
import { useCommonStore } from '@/stores/common.js'
import { useRegistryStore } from '@/stores/registry.js'

export default {
  name: 'PersonDetailEdit',
  components: {
    'api-error': APIErrorMessage,
    'organization-add': OrganizationAdd,
    'application-add': ApplicationAddEdit
  },
  data () {
    return {
      registryStore: useRegistryStore(),
      commonStore: useCommonStore(),
      breadcrumbs: [
        { label: 'Registry', url: '/registries/'},
        { label: 'Add a Person'}
      ],
      drillerForm: {
        person: {
          surname: '',
          first_name: '',
          contact_tel: '',
          contact_email: '',
          contact_cell: '',
          well_driller_orcs_no: '',
          pump_installer_orcs_no: ''
        },
        regType: [],
        registrations: {
          drill: {
            registries_activity: 'DRILL',
            status: 'ACTIVE',
            registration_no: '',
            organization: ''
          },
          pump: {
            registries_activity: 'PUMP',
            status: 'ACTIVE',
            registration_no: '',
            organization: ''
          }
        },
        organizations: {
          drill: null,
          pump: null
        }
      },
      companies: [
        { org_guid: '', name: '' }
      ],
      drillApplications: [],
      pumpApplications: [],
      submitSuccess: false,
      submitError: false,
      newOrgSuccess: false,
      fieldErrors: {
        contact_email: []
      }
    }
  },
  computed: {
    validation () {
      return {
        contact_email: (this.fieldErrors.contact_email && this.fieldErrors.contact_email.length) ? false : null
      }
    },
    files: {
      get: function () {
        return this.commonStore.uploadFiles
      },
      set: function (value) {
        this.commonStore.setFiles(value)
      }
    },
    privateDocument: {
      get: function () {
        return this.commonStore.isPrivate
      },
      set: function (value) {
        this.commonStore.setPrivate(value)
      }
    },
    loading () { return this.registryStore.loading },
    error () { return this.registryStore.error }
  },
  methods: {
    clearFieldErrors () {
      this.fieldErrors = {
        contact_email: []
      }
    },
    onFormSubmit () {
      /**
       * Submitting a new person record also creates corresponding registration records
       * for that each activity (driller or pump installer).
       *
       * This method collects data from the template's form fields and bundles it for the GWELLS API.
       * Data for an activity (driller etc.) is only included if the corresponding registration checkbox
       * is checked (checking a box adds the activity to this.regType).
       */
      const registrations = []
      const personData = Object.assign({}, this.drillerForm.person)
      this.submitSuccess = false
      this.submitError = false

      // strip empty strings
      Object.keys(personData).forEach((key) => {
        if (personData[key] === '' || personData[key] === null) {
          delete personData[key]
        }
      })

      // Set organizations for each activity to the GUID of the organization selected in the form
      if (this.drillerForm.organizations.drill) {
        this.drillerForm.registrations['drill'].organization = this.drillerForm.organizations.drill.org_guid
      }
      if (this.drillerForm.organizations.pump) {
        this.drillerForm.registrations['pump'].organization = this.drillerForm.organizations.pump.org_guid
      }

      // Map applications to registrions
      this.drillerForm.registrations['drill'].applications = this.drillApplications.map((application) => application.data)
      this.drillerForm.registrations['pump'].applications = this.pumpApplications.map((application) => application.data)

      // add registration data for activities checked off on form
      this.drillerForm.regType.forEach((item) => {
        registrations.push(this.drillerForm.registrations[item.toLowerCase()])
      })

      personData['registrations'] = registrations

      ApiService.post('drillers', personData).then((response) => {
        if (this.commonStore.uploadFiles.length > 0) {
          this.commonStore.uploadTheFiles({
            documentType: 'drillers',
            recordId: response.data.person_guid
          }).then(() => {
            this.commonStore.fileUploadSucceeded()
            this.$router.push({ name: 'PersonDetail', params: { person_guid: response.data.person_guid } })
          }).catch((error) => {
            this.commonStore.fileUploadFail()
            console.error(error)
          })
        } else {
          this.$router.push({ name: 'PersonDetail', params: { person_guid: response.data.person_guid } })
        }
        this.onFormReset()
      })
        .catch((e) => {
          const errors = e.response.data
          for (const field in errors) {
            this.fieldErrors[field] = errors[field]
          }
        })
    },
    onFormReset () {
      this.clearFieldErrors()
      this.drillerForm = Object.assign({}, {
        person: {
          surname: '',
          first_name: '',
          contact_tel: '',
          contact_email: '',
          contact_cell: ''
        },
        organizations: {
          drill: null,
          pump: null
        },
        regType: [],
        registrations: {
          drill: {
            registries_activity: 'DRILL',
            status: 'ACTIVE',
            registration_no: '',
            organization: null
          },
          pump: {
            registries_activity: 'PUMP',
            status: 'ACTIVE',
            registration_no: '',
            organization: null
          }
        }
      })
    },
    newOrgHandler (orgGuid) {
      ApiService.query('organizations/names').then((response) => {
        this.companies = response.data

        // Find the new company with the "emitted" organization record UUID
        if (this.drillerForm.regType && this.drillerForm.regType.length === 1) {
          this.drillerForm.organizations[[this.drillerForm.regType[0].toLowerCase()]] =
            this.companies.find((company) => company.org_guid === orgGuid)
        }
        this.newOrgSuccess = true
      }).catch(() => {
        this.orgListError = 'Unable to retrieve organization list.'
      })
    },
    addApplication (collection) {
      collection.push({ id: new Date().getUTCMilliseconds(), data: null })
    },
    closeApplication (collection, id) {
      collection.splice(collection.findIndex((item) => item.id === id))
    }
  },
  created () {
    ApiService.query('organizations/names').then((response) => {
      this.companies = response.data
    }).catch(() => {
      this.orgListError = 'Unable to retrieve organization list.'
    })
  }
}
</script>

<style>
</style>
