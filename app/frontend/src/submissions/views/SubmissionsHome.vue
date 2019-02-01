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
  <div class="card" v-if="userRoles.wells.edit || userRoles.submissions.edit">
    <div class="card-body">

      <!-- Form submission success message -->
      <b-alert
          id="submissionSuccessAlert"
          :show="formSubmitSuccess"
          variant="success"
          class="mt-3">
        <i class="fa fa-2x fa-check-circle text-success mr-2 alert-icon" aria-hidden="true"></i>
        <div v-if="isStaffEdit" class="alert-message">
          Changes saved.
        </div>
        <div v-else class="alert-message">
          Your well record was successfully submitted.
        </div>
      </b-alert>

      <!-- Document Uploading alerts -->
      <b-alert show v-if="files_uploading">File Upload In Progress...</b-alert>
      <b-alert show v-if="!files_uploading && file_upload_error" variant="warning" >{{file_upload_error}}</b-alert>
      <b-alert show v-if="!files_uploading && file_upload_success" variant="success" >Successfully uploaded all files</b-alert>

      <!-- Form submission error message -->
      <b-alert
          :show="formSubmitError"
          dismissible
          @dismissed="formSubmitError=false"
          variant="danger"
          class="mt-3">

        <i class="fa fa-2x fa-exclamation-circle text-danger mr-2 alert-icon" aria-hidden="true"></i>
        <div class="alert-message">
          <div v-if="isStaffEdit">
            Your changes were not saved.
          </div>
          <div v-else>
            Your well record was not submitted.
          </div>
          <span v-if="errors && errors.detail">
            {{ errors.detail }}
          </span>
          <div v-if="errors && errors != {}">
            <div v-for="(field, i) in Object.keys(errors)" :key="`submissionError${i}`">
              {{field | readable}} : <span v-for="(e, j) in errors[field]" :key="`submissionError${i}-${j}`">{{ e }}</span>
            </div>
          </div>
        </div>
      </b-alert>

      <b-form @submit.prevent="confirmSubmit">
        <!-- if preview === true : Preview -->
        <submission-preview
          v-if="preview"
          :form="form"
          :activity="activityType"
          :sections="displayFormSection"
          :errors="errors"
          :reportSubmitted="formSubmitSuccess"
          :formSubmitLoading="formSubmitLoading"
          :uploadedFiles="uploadedFiles"
          v-on:back="handlePreviewBackButton"
          v-on:startNewReport="handleExitPreviewAfterSubmit"
          />
        <!-- if preview === false : Activity submission form -->
        <activity-submission-form
          v-else
          :form="form"
          :activityType.sync="activityType"
          :sections="displayFormSection"
          :formSteps="formSteps"
          :errors="errors"
          :formIsFlat.sync="formIsFlat"
          :trackValueChanges="trackValueChanges"
          :formSubmitLoading="formSubmitLoading"
          :isStaffEdit="isStaffEdit"
          :loading="loading"
          :uploadedFiles="uploadedFiles"
          v-on:preview="handlePreviewButton"
          v-on:submit_edit="formSubmit"
          v-on:resetForm="resetForm"
          v-on:fetchFiles="fetchFiles"
          />

        <!-- Form submission confirmation -->
        <b-modal
            v-model="confirmSubmitModal"
            id="confirmSubmitModal"
            centered
            title="Confirm submission"
            @shown="$refs.confirmSubmitConfirmBtn.focus()"
            :return-focus="$refs.activitySubmitBtn">
          Are you sure you want to submit this activity report?
          <div slot="modal-footer">
            <b-btn variant="primary" @click="confirmSubmitModal=false;formSubmit()" ref="confirmSubmitConfirmBtn">
              Save
            </b-btn>
            <b-btn variant="light" @click="confirmSubmitModal=false">
              Cancel
            </b-btn>
          </div>
        </b-modal>
      </b-form>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import { FETCH_CODES, FETCH_WELLS } from '../store/actions.types.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'
import SubmissionPreview from '@/submissions/components/SubmissionPreview/SubmissionPreview.vue'
import filterBlankRows from '@/common/filterBlankRows.js'
import ActivitySubmissionForm from '@/submissions/components/SubmissionForm/ActivitySubmissionForm.vue'
export default {
  name: 'SubmissionsHome',
  mixins: [inputFormatMixin, filterBlankRows],
  components: {
    ActivitySubmissionForm,
    SubmissionPreview
  },
  data () {
    return {
      activityType: 'CON',
      formIsFlat: false,
      preview: false,
      loading: false,
      confirmSubmitModal: false,
      formSubmitSuccess: false,
      formSubmitSuccessWellTag: null,
      formSubmitError: false,
      formSubmitLoading: false,
      sliding: null,
      trackValueChanges: false,
      errors: {},
      form: {},
      formOptions: {},
      uploadedFiles: {},
      formSteps: {
        CON: [
          'activityType',
          'wellType',
          'wellOwner',
          'personResponsible',
          'wellLocation',
          'wellCoords',
          'method',
          'casings',
          'backfill',
          'lithology',
          'liner',
          'screens',
          'filterPack',
          'wellDevelopment',
          'wellYield',
          'waterQuality',
          'wellCompletion',
          'comments',
          'documents'
        ],
        ALT: [
          'activityType',
          'wellType',
          'wellOwner',
          'personResponsible',
          'wellLocation',
          'wellCoords',
          'method',
          'casings',
          'backfill',
          'lithology',
          'liner',
          'screens',
          'filterPack',
          'wellDevelopment',
          'wellYield',
          'waterQuality',
          'wellCompletion',
          'comments',
          'documents'
        ],
        DEC: [
          'activityType',
          'wellType',
          'wellOwner',
          'personResponsible',
          'wellLocation',
          'wellCoords',
          'method',
          'closureDescription',
          'casings',
          'decommissionInformation',
          'comments',
          'documents'
        ],
        STAFF_EDIT: [
          'wellType',
          'wellOwner',
          'personResponsible',
          'wellLocation',
          'wellCoords',
          'method',
          'casings',
          'backfill',
          'lithology',
          'liner',
          'screens',
          'filterPack',
          'wellDevelopment',
          'wellYield',
          'waterQuality',
          'wellCompletion',
          'observationWellInfo',
          'closureDescription',
          'decommissionInformation',
          'comments',
          'documents',
          'aquiferData'
        ]
      }
    }
  },
  computed: {
    displayFormSection () {
      // returns an object describing which components should be displayed
      // when in "flat form" mode

      const activityType = this.activityType
      const components = {}

      this.formSteps[activityType].forEach((step) => {
        components[step] = true
      })
      return components
    },
    isStaffEdit () {
      return this.activityType === 'STAFF_EDIT'
    },
    ...mapGetters(['codes', 'userRoles', 'well', 'keycloak']),
    ...mapState('documentState', [
      'files_uploading',
      'file_upload_error',
      'file_upload_success',
      'upload_files'
    ])
  },
  methods: {
    ...mapActions('documentState', [
      'uploadFiles',
      'fileUploadSuccess'
    ]),
    formSubmit () {
      const data = Object.assign({}, this.form)
      const meta = data.meta

      if (this.isStaffEdit) {
        // Remove any fields that aren't changed
        Object.keys(data).forEach((key) => {
          if (key !== 'well' && !(key in meta.valueChanged)) {
            delete data[key]
          }
        })
      }

      // delete "meta" data (form input that need not be submitted) stored within form object
      delete data.meta

      // replace the "person responsible" object with the person's guid
      if (data.person_responsible && data.person_responsible.person_guid) {
        data.person_responsible = data.person_responsible.person_guid
      }
      // replace the "company of person responsible" object with the company's guid
      if (data.company_of_person_responsible && data.company_of_person_responsible.org_guid) {
        data.company_of_person_responsible = data.company_of_person_responsible.org_guid
      }

      if (data.well && data.well.well_tag_number) {
        data.well = data.well.well_tag_number
      }

      if (!this.isStaffEdit) {
        // We don't strip blank strings on an edit, someone may be trying to replace a value with a blank value.
        this.stripBlankStrings(data)
      }

      const sets = ['linerperforation_set', 'lithologydescription_set', 'screen_set', 'casing_set', 'decommission_description_set']
      sets.forEach((key) => {
        if (key in data) {
          data[key] = this.filterBlankRows(data[key])
        }
      })

      this.formSubmitLoading = true
      this.formSubmitSuccess = false
      this.formSubmitError = false
      this.formSubmitSuccessWellTag = null
      this.errors = {}
      // Depending on the type of submission (construction/decommission/alteration/edit) we post to
      // different endpoints.
      const PATH = this.codes.activity_types.find((item) => item.code === this.activityType).path
      ApiService.post(PATH, data).then((response) => {
        this.formSubmitSuccess = true
        this.formSubmitSuccessWellTag = response.data.well

        this.$emit('formSaved')

        if (!this.form.well_tag_number) {
          this.setWellTagNumber(response.data.well)
        }

        this.$nextTick(function () {
          window.scrollTo(0, 0)
        })

        if (this.upload_files.length > 0) {
          if (response.data.filing_number) {
            this.uploadFiles({
              documentType: 'submissions',
              recordId: response.data.filing_number
            }).then(() => {
              this.fileUploadSuccess()
              this.fetchFiles()
            }).catch((error) => {
              console.log(error)
            })
          } else {
            this.uploadFiles({
              documentType: 'wells',
              recordId: response.data.well
            }).then(() => {
              this.fileUploadSuccess()
              this.fetchFiles()
            }).catch((error) => {
              console.log(error)
            })
          }
        }
      }).catch((error) => {
        if (error.response.status === 400) {
          // Bad request, the response.data will contain information relating to why the request was bad.
          this.errors = error.response.data
        } else {
          // Some other kind of server error. If for example, it's a 500, the response data is not of
          // much use, so we just grab the status text.
          this.errors = { 'Server Error': error.response.statusText }
        }
        this.formSubmitError = true
        this.$nextTick(function () {
          window.scrollTo(0, 0)
        })
      }).finally((response) => {
        this.formSubmitLoading = false
      })
    },
    confirmSubmit () {
      this.confirmSubmitModal = true
    },
    resetForm () {
      this.form = {
        well: null,
        well_status: '',
        well_class: '',
        well_subclass: '',
        intended_water_use: '',
        identification_plate_number: null,
        well_identification_plate_attached: '',
        id_plate_attached_by: '',
        water_supply_system_well_name: '',
        water_supply_system_name: '',
        person_responsible: null,
        company_of_person_responsible: null,
        driller_name: '',
        consultant_name: '',
        consultant_company: '',
        work_start_date: '',
        work_end_date: '',
        owner_full_name: '',
        owner_mailing_address: '',
        owner_city: '',
        owner_province_state: '',
        owner_postal_code: '',
        owner_email: '',
        owner_tel: '',
        street_address: '', // this is the street address of the well location
        city: '', // well location city
        legal_lot: '',
        legal_plan: '',
        legal_district_lot: '',
        legal_block: '',
        legal_section: '',
        legal_township: '',
        legal_range: '',
        land_district: '',
        legal_pid: '',
        liner_material: null,
        liner_diameter: null,
        liner_thickness: null,
        liner_from: null,
        liner_to: null,
        linerperforation_set: [],
        well_location_description: '',
        latitude: null,
        longitude: null,
        coordinate_acquisition_code: null,
        ground_elevation: null,
        ground_elevation_method: '',
        drilling_method: '',
        other_drilling_method: '',
        well_orientation: true,
        lithologydescription_set: [],
        surface_seal_material: '',
        surface_seal_depth: '',
        surface_seal_thickness: '',
        surface_seal_method: '',
        backfill_type: '',
        backfill_depth: '',
        casing_set: [],
        screen_intake_method: '',
        screen_type: '',
        screen_material: '',
        other_screen_material: '',
        screen_opening: '',
        screen_bottom: '',
        screen_set: [],
        screen_information: '',
        development_method: '',
        development_hours: '',
        development_notes: '',
        yield_estimation_method: '',
        yield_estimation_rate: '',
        yield_estimation_duration: '',
        well_yield_unit: '',
        static_level_before_test: '',
        drawdown: '',
        hydro_fracturing_performed: false,
        hydro_fracturing_yield_increase: '',
        recommended_pump_depth: '',
        recommended_pump_rate: '',
        filter_pack_from: '',
        filter_pack_to: '',
        filter_pack_thickness: '',
        filter_pack_material: '',
        filter_pack_material_size: '',
        water_quality_characteristics: [],
        water_quality_colour: '',
        water_quality_odour: '',
        ems_id: '',
        aquifer: '',
        total_depth_drilled: '',
        finished_well_depth: '',
        final_casing_stick_up: '',
        bedrock_depth: '',
        static_water_level: '',
        well_yield: '',
        artesian_flow: '',
        artesian_pressure: '',
        well_cap_type: '',
        well_disinfected: 'False',
        comments: '',
        internal_comments: '',
        alternative_specs_submitted: 'False',
        decommission_description_set: [],
        decommission_reason: '',
        decommission_method: '',
        sealant_material: '',
        backfill_material: '',
        decommission_details: '',
        observation_well_number: '',
        observation_well_status: '',
        aquifer_vulnerability_index: '',
        storativity: '',
        transmissivity: '',
        hydraulic_conductivity: '',
        specific_storage: '',
        specific_yield: '',
        testing_method: '',
        testing_duration: '',
        analytic_solution_type: '',
        boundary_effect: '',

        // non-form fields that should be saved with form
        meta: {
          drillerSameAsPersonResponsible: false
        }
      }
      this.componentUpdateTrigger = Date.now()
    },

    setWellTagNumber (well) {
      // setWellTagNumber is used to link an activity report to a well other than through the dropdown menu.
      // the dropdown menu returns an object so this method also does.
      this.form.well = { well_tag_number: well }
    },
    stripBlankStrings (formObject) {
      // strips blank strings from a form object

      Object.keys(formObject).forEach((key) => {
        if (typeof formObject[key] === 'object' && formObject[key] !== null) {
          // descend into nested objects
          this.stripBlankStrings(formObject[key])
        }

        if (formObject[key] === '') {
          delete formObject[key]
        }
      })
    },
    handlePreviewButton () {
      this.preview = true

      // clear the error alert (otherwise it looks like there are new errors after clicking preview)
      this.formSubmitError = false

      this.$nextTick(function () {
        window.scrollTo(0, 0)
      })
    },
    handlePreviewBackButton () {
      this.preview = false
      this.$nextTick(function () {
        window.scrollTo(0, 0)
      })
    },
    handleExitPreviewAfterSubmit () {
      this.formSubmitSuccess = false
      this.resetForm()
      this.preview = false
      this.step = 1
      this.$nextTick(function () {
        window.scrollTo(0, 0)
      })
    },
    fetchFiles () {
      // this.form.well is sometimes the tag number, and sometimes an object. This detects which is which
      console.log(this.form.well && isNaN(this.form.well))
      let tag = this.form.well && isNaN(this.form.well) ? this.form.well.well_tag_number : this.form.well

      if (tag) {
        ApiService.query(`wells/${tag}/files`)
          .then((response) => {
            this.uploadedFiles = response.data
          })
      }
    }
  },
  watch: {
    activityType () {
      this.resetForm()
    }
  },
  created () {
    this.resetForm()
    this.$store.dispatch(FETCH_CODES)

    if (this.$route.params.id) {
      this.setWellTagNumber(this.$route.params.id)
    }
    if (this.$route.name === 'SubmissionsEdit') {
      this.activityType = 'STAFF_EDIT'
      this.formIsFlat = true

      this.loading = true

      ApiService.query(`wells/${this.$route.params.id}`).then((res) => {
        Object.keys(res.data).forEach((key) => {
          if (key in this.form) {
            this.form[key] = res.data[key]
          }
        })
        if (this.form.person_responsible && this.form.person_responsible.name === this.form.driller_name) {
          this.form.meta.drillerSameAsPersonResponsible = true
        }
        // Wait for the form update we just did to fire off change events.
        this.$nextTick(() => {
          this.form.meta.valueChanged = {}
          this.loading = false
          this.$nextTick(() => {
            // We have to allow the UI to render all the components after the 'loading = false' setting,
            // so we only start tracking changes after that.
            this.trackValueChanges = true
          })
        })
      }).catch((e) => {
        console.error(e)
      })
    } else {
      // Some of our child components need the well data, we dispatch the request here, in hopes
      // that the data will be available by the time those components render.
      this.$store.dispatch(FETCH_WELLS)
    }

    this.fetchFiles()
  }
}
</script>

<style lang="scss">
.slide-leave-active,
.slide-enter-active {
  transition: 1s;
}
.slide-enter {
  transform: translate(100%, 0);
}
.slide-leave-to {
  transform: translate(-100%, 0);
}
.bounce-enter-active {
  animation: bounce-in .5s;
}
.bounce-leave-active {
  animation: bounce-out .2s;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes bounce-out {
  100% {
    transform: scale(0)
  }
}
.input-width-small {
  max-width: 3rem;
}
.input-width-medium {
  max-width: 6rem;
}
</style>
