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
  <div class="container p-1">
    <div v-if="loading" class="mt-3">
      <div class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"></i>
      </div>
    </div>
    <div v-else>
      <b-card v-if="breadcrumbs && breadcrumbs.length" no-body class="mb-3 d-print-none">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
      </b-card>
      <div class="card" v-if="userRoles.wells.edit || userRoles.submissions.edit">
        <div class="card-body">

          <b-alert
              show
              variant="info"
              class="mb-3"
              v-for="(survey, index) in surveys[isStaffEdit ? 'edit' : 'submissions']"
              :key="`survey ${index}`">
            <p class="m-0">
              <a :href="survey.survey_link" target="_blank">
                {{ survey.survey_introduction_text }}
              </a>
            </p>
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
              v-on:fetchFiles="fetchFiles"
              />
            <!-- if preview === false : Activity submission form -->
            <div v-else>
              <div v-if="isStaffEdit && errorWellNotFound">
                <h1>Not Found</h1>
                <p>The page you are looking for was not found.</p>
              </div>
              <activity-submission-form
                v-else
                :form="form"
                :events="events"
                :submissionsHistory="submissionsHistory"
                :isPublished="isPublished"
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
                :formChanges="formChanges"
                v-on:preview="handlePreviewButton"
                v-on:submit_edit="formSubmit"
                v-on:resetForm="resetForm"
                v-on:fetchFiles="fetchFiles"
                />
            </div>

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
      <div class="card" v-else-if="!$keycloak.authenticated">
        <div class="card-body">
          <p>Please log in to continue.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapGetters, mapState } from 'vuex'
import { diff } from 'deep-diff'
import { camelCase } from 'lodash'
import smoothScroll from 'smoothscroll'

import ApiService from '@/common/services/ApiService.js'
import { FETCH_CODES, FETCH_WELL_TAGS } from '../store/actions.types.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'
import SubmissionPreview from '@/submissions/components/SubmissionPreview/SubmissionPreview.vue'
import filterBlankRows from '@/common/filterBlankRows.js'
import ActivitySubmissionForm from '@/submissions/components/SubmissionForm/ActivitySubmissionForm.vue'
import parseErrors from '@/common/helpers/parseErrors.js'
import { RESET_WELL_DATA } from '@/wells/store/actions.types.js'

export default {
  name: 'SubmissionsHome',
  mixins: [inputFormatMixin, filterBlankRows],
  components: {
    ActivitySubmissionForm,
    SubmissionPreview
  },
  data () {
    return {
      compareForm: {},
      // event bus; use by emitting events on the events instance eg. this.events.$emit('updated')
      events: new Vue(),
      ...initialState()
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
      return this.activityType === 'STAFF_EDIT' && this.userRoles.wells.edit
    },
    breadcrumbs () {
      const breadcrumbs = []

      if (this.errorWellNotFound) {
        breadcrumbs.push({
          text: `Well Search`,
          to: { name: 'wells-home' }
        },
        {
          text: `Not found`,
          active: true
        })
        return breadcrumbs
      }

      if (this.isStaffEdit) {
        breadcrumbs.push(
          {
            text: `Well Search`,
            to: { name: 'wells-home' }
          },
          {
            text: `Well ${this.$route.params.id} Summary`,
            to: { name: 'wells-detail', params: { id: this.$route.params.id } }
          },
          {
            text: `Edit Well`,
            to: { name: 'SubmissionsEdit', params: { id: this.$route.params.id } }
          }
        )
      }
      return breadcrumbs
    },
    errorWellNotFound () {
      return this.wellFetchError && this.wellFetchError.status === 404
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
      'fileUploadSuccess',
      'fileUploadFail',
      'resetUploadFiles'
    ]),
    ...mapActions([ RESET_WELL_DATA ]),
    formSubmit () {
      const data = Object.assign({}, this.form)
      const meta = data.meta

      if (this.isStaffEdit) {
        // These skip variables will include both mutually required fields if one of them changes
        // We have to include both lat and lon for geom updates and ground_elevation and method together
        // TODO optimize the mutual requirement flow
        let skipLatLon = 'latitude' in meta.valueChanged || 'longitude' in meta.valueChanged
        let skipWorkDates = 'work_start_date' in meta.valueChanged || 'work_end_date' in meta.valueChanged
        let skipConDates = 'construction_start_date' in meta.valueChanged || 'construction_end_date' in meta.valueChanged
        let skipAltDates = 'alteration_start_date' in meta.valueChanged || 'alteration_end_date' in meta.valueChanged
        let skipDecDates = 'decommission_start_date' in meta.valueChanged || 'decommission_end_date' in meta.valueChanged
        let skipGroundElevation = 'ground_elevation' in meta.valueChanged || 'ground_elevation_method' in meta.valueChanged
        Object.keys(data).forEach((key) => {
          // Skip lat lon if one of them has changed
          if ((key === 'latitude' || key === 'longitude') && skipLatLon) { return }
          if ((key === 'ground_elevation' || key === 'ground_elevation_method') && skipGroundElevation) { return }
          if ((key === 'work_start_date' || key === 'work_end_date') && skipWorkDates) {
            if (data[key] === '') { data[key] = null } return
          }
          if ((key === 'construction_start_date' || key === 'construction_end_date') && skipConDates) {
            if (data[key] === '') { data[key] = null } return
          }
          if ((key === 'alteration_start_date' || key === 'alteration_end_date') && skipAltDates) {
            if (data[key] === '') { data[key] = null } return
          }
          if ((key === 'decommission_start_date' || key === 'decommission_end_date') && skipDecDates) {
            if (data[key] === '') { data[key] = null } return
          }
          // Remove any fields that aren't changed
          if (key !== 'well' && !(key in meta.valueChanged)) { delete data[key] }
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
        let skipKeys = []
        // we need both ground elevation and its method to be sent for validation on submission
        if (data.ground_elevation_method || data.ground_elevation) {
          skipKeys.push('ground_elevation_method', 'ground_elevation')
        }
        // We don't strip blank strings on an edit, someone may be trying to replace a value with a blank value.
        this.stripBlankStrings(data, skipKeys)
      }

      const sets = ['linerperforation_set', 'lithologydescription_set', 'screen_set', 'casing_set', 'decommission_description_set']
      sets.forEach((key) => {
        if (key in data) {
          data[key] = this.filterBlankRows(data[key])
        }
      })

      // Check to see if we are currently saving this form. If so - don't try to POST again
      if (this.formSubmitLoading) { return }

      if (!this.isFormValid()) {
        this.showErrorMessages()
        return
      }

      this.formSubmitLoading = true
      this.formSubmitSuccess = false
      this.formSubmitError = false
      this.formSubmitSuccessWellTag = null
      this.errors = {}
      // Save notification
      const savingNotification = this.$noty.info('<div class="loader"></div><div class="notifyText">Saving...</div>', { timeout: false })

      // Depending on the type of submission (construction/decommission/alteration/edit) we post to
      // different endpoints.
      const PATH = this.codes.activity_types.find((item) => item.code === this.activityType).path
      ApiService.post(PATH, data).then((response) => {
        this.formSubmitSuccess = true
        this.formSubmitSuccessWellTag = response.data.well

        this.$emit('formSaved')
        // Save completed notification

        if (this.isStaffEdit) {
          this.$nextTick(() => {
            this.$noty.success('<div class="notifyText">Changes saved.</div>', { killer: true })
          })
          this.events.$emit('well-edited', true)
          this.fetchWellDataForStaffEdit({ reloadPage: false })
          this[RESET_WELL_DATA]()
        } else {
          this.$nextTick(() => {
            this.$noty.success('<div aria-label="Close" class="closeBtn">x</div><div class="notifyText">Well report submitted.</div>', { killer: true })
          })

          this.$nextTick(function () {
            window.scrollTo(0, 0)
          })
        }

        if (!this.form.well_tag_number) {
          this.form.well = response.data.well
        }

        // Reloads only altered data in form for re-rendering
        Object.keys(response.data).forEach((key) => {
          if (meta.valueChanged && key in meta.valueChanged) {
            this.form[key] = response.data[key]
          }
        })

        this.form.meta.valueChanged = {}
        // Set initial form fields for comparison with user input changes
        Object.assign(this.compareForm, this.form)

        if (this.upload_files.length > 0) {
          if (response.data.filing_number) {
            this.$noty.info('<div class="loader"></div><div class="notifyText">File upload in progress...</div>', { timeout: false })
            this.uploadFiles({
              documentType: 'submissions',
              recordId: response.data.filing_number
            }).then(() => {
              this.fileUploadSuccess()
              this.fetchFiles()
              this.$noty.success('<div class="notifyText">Successfully uploaded all files.</div>', { killer: true })
            }).catch((error) => {
              this.fileUploadFail()
              console.error(error)
              this.$noty.error('<div class="notifyText">Error uploading files.</div>', { killer: true })
            })
          } else {
            this.$noty.info('<div class="loader"></div><div class="notifyText">File upload in progress...</div>', { timeout: false })
            this.uploadFiles({
              documentType: 'wells',
              recordId: response.data.well
            }).then(() => {
              this.$noty.success('<div class="notifyText">Successfully uploaded all files.</div>', { killer: true })
              this.fileUploadSuccess()
              this.fetchFiles()
            }).catch((error) => {
              this.fileUploadFail()
              console.error(error)
              this.$noty.error('<div class="notifyText">Error uploading files.</div>', { killer: true })
            })
          }
        }
      }).catch((error) => {
        if (error.response) {
          if (error.response.status === 400) {
            // Bad request, the response.data will contain information relating to why the request was bad.
            this.errors = error.response.data
          } else {
            // Some other kind of server error. If for example, it's a 500, the response data is not of
            // much use, so we just grab the status text.
            this.errors = { 'Server error': error.response.statusText }
          }
        } else {
          // This is a generic js error, so just log it
          console.log(error)
        }

        this.formSubmitError = true

        this.showErrorMessages()
      }).finally((response) => {
        this.formSubmitLoading = false

        // sometimes the save success notification doesn't close the "saving..." one.
        // if the in-progress status message is still shown after the request completes,
        // close it immediately.
        if (savingNotification && !savingNotification.closed) {
          savingNotification.close()
        }
      })
    },
    showErrorMessages () {
      let cleanErrors = parseErrors(this.errors)
      let errTxt = cleanErrors.length > 1 ? 'Input errors.' : 'Input error.'
      // Error notifications
      this.$noty.error('<div class="errorTitle">' + errTxt + '</div>', { timeout: 2000, killer: true })
      cleanErrors.forEach(e => {
        this.$noty.error('<div aria-label="Close" class="closeBtn">x</div><div class="errorText"><b>Error: </b>' + e + '</div>', { timeout: false })
      })
    },
    formChanges () {
      let differences = diff(this.compareForm, this.form)
      return !!differences
    },
    confirmSubmit () {
      this.confirmSubmitModal = true
    },
    resetForm () {
      this.form = {
        well: null,
        well_status: '',
        well_publication_status: '',
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
        construction_start_date: '',
        construction_end_date: '',
        alteration_start_date: '',
        alteration_end_date: '',
        decommission_start_date: '',
        decommission_end_date: '',
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
        well_orientation_status: '',
        drilling_methods: [],
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
        development_methods: [],
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
        ems: '',
        aquifer: '',
        total_depth_drilled: '',
        finished_well_depth: '',
        final_casing_stick_up: '',
        bedrock_depth: '',
        static_water_level: '',
        well_yield: '',
        artesian_flow: '',
        artesian_pressure: '',
        artesian_pressure_head: '',
        artesian_conditions: false,
        well_cap_type: '',
        well_disinfected_status: '',
        comments: '',
        internal_comments: '',
        alternative_specs_submitted: false,
        decommission_description_set: [],
        decommission_reason: '',
        decommission_method: '',
        decommission_sealant_material: '',
        decommission_backfill_material: '',
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
        aquifer_lithology: '',

        // non-form fields that should be saved with form
        meta: {
          drillerSameAsPersonResponsible: false
        }
      }
      this.componentUpdateTrigger = Date.now()
    },
    isFormValid () {
      const errors = {}

      let validateWellClassAndIntendedWaterUse = true
      if ((this.activityType === 'ALT' || this.activityType === 'DEC') && this.form.well) {
        validateWellClassAndIntendedWaterUse = false
      }

      // Always validate well_class and intended_water_use except for ALT or DEC submissions with a
      // well_tag_number specified
      if (validateWellClassAndIntendedWaterUse) {
        if (!this.form.intended_water_use) {
          errors.intended_water_use = [ 'Intended water use is required.' ]
        }

        if (!this.form.well_class) {
          errors.well_class = [ 'Well class is required.' ]
        } else if (this.form.well_class === 'WATR_SPPLY') {
          if (!this.form.intended_water_use || this.form.intended_water_use === 'NA') {
            errors.intended_water_use = [ 'Intended water use is required when the well class is Water Supply.' ]
          }
        } else { // all other well_class_codes
          if (this.form.intended_water_use && this.form.intended_water_use !== 'NA') {
            errors.intended_water_use = [ 'Intended water use only valid for a well class of Water Supply.' ]
          }
        }
      }

      // Validate the Artesian Well radio button, if flow, pressure head or pressure psi has a value then we
      //  ask the user to set the value of Artesian Well to Yes
      if (!this.form.artesian_conditions && (this.form.artesian_flow > 0 || this.form.artesian_pressure > 0 || this.form.artesian_pressure_head > 0)) {
        errors.artesian_conditions = [ 'Set Artesian Well to Yes for positive flow or pressure.' ]
      }

      this.errors = errors
      return Object.keys(errors).length === 0
    },
    setWellTagNumber (well) {
      // setWellTagNumber is used to link an activity report to a well other than through the dropdown menu.
      // the dropdown menu returns an object so this method also does.
      this.form.well = { well_tag_number: well }
    },
    stripBlankStrings (formObject, skipKeys = []) {
      // strips blank strings from a form object
      Object.keys(formObject).forEach((key) => {
        if (skipKeys.includes(key)) {
          return
        }
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
      if (!this.formChanges()) {
        this.$noty.info('<div class="errorTitle">Please add some data to your submission.</div>', { killer: true })
        return
      }

      if (!this.isFormValid()) {
        this.showErrorMessages()
        const firstField = Object.keys(this.errors)[0] || 'no-field-name'
        const el = this.$el.querySelector(`#${camelCase(firstField)}`) || null
        if (el) { smoothScroll(el, 500) }
        return
      }

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
      this.uploadedFiles = {}

      // this.form.well is sometimes the tag number, and sometimes an object. This detects which is which
      let tag = this.form.well && isNaN(this.form.well) ? this.form.well.well_tag_number : this.form.well

      if (tag) {
        ApiService.query(`wells/${tag}/files`)
          .then((response) => {
            this.uploadedFiles = response.data
          })
      }
    },
    setupPage () {
      Object.assign(this.$data, initialState())
      this.resetForm()
      this.$store.dispatch(FETCH_CODES)
      this.resetUploadFiles()
      if (this.$route.params.id) {
        this.setWellTagNumber(this.$route.params.id)
      }
      if (this.$route.name === 'SubmissionsEdit') {
        this.activityType = 'STAFF_EDIT'
        this.formIsFlat = true
        this.fetchWellDataForStaffEdit()
      } else {
        // Some of our child components need the well tags, we dispatch the request here, in hopes
        // that the data will be available by the time those components render.
        this.$store.dispatch(FETCH_WELL_TAGS)
        this.activityType = 'CON'
        this.formIsFlat = false
      }
      this.fetchFiles()
      // Set initial form fields for comparison with user input changes
      Object.assign(this.compareForm, this.form)
    },
    fetchSurveys () {
      // Fetch current surveys and add applicable surveys (if any) to this.surveys to be displayed
      ApiService.query('surveys').then((response) => {
        if (response.data) {
          response.data.forEach((survey) => {
            if (survey.survey_page === 'u' && survey.survey_enabled) {
              this.surveys.submissions.push(survey)
            }

            if (survey.survey_page === 'e' && survey.survey_enabled) {
              this.surveys.edit.push(survey)
            }
          })
        }
      }).catch((e) => {
        console.error(e)
      })
    },
    fetchWellDataForStaffEdit (options = {}) {
      const { reloadPage = true } = options
      if (reloadPage) {
        this.loading = true
      }
      ApiService.query(`wells/${this.$route.params.id}/edit`).then((res) => {
        Object.keys(res.data).forEach((key) => {
          if (key in this.form) {
            this.form[key] = res.data[key]
          }
        })
        if (this.form.person_responsible && this.form.person_responsible.name === this.form.driller_name) {
          this.form.meta.drillerSameAsPersonResponsible = true
        }

        // store the number of submissions already associated with this well
        this.submissionsHistory = res.data.submission_reports || []

        // store the is published flag for this well
        this.isPublished = res.data.is_published

        // Wait for the form update we just did to fire off change events.
        this.$nextTick(() => {
          this.form.meta.valueChanged = {}
          this.$nextTick(() => {
            // We have to allow the UI to render all the components after the 'loading = false' setting,
            // so we only start tracking changes after that.
            this.trackValueChanges = true
          })
        })
        // Set initial form fields for comparison with user input changes
        Object.assign(this.compareForm, this.form)
      }).catch((e) => {
        this.wellFetchError = e.response
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    },
    confirmLeavePage () {
      // prompt the user to confirm whether they want to leave the page or not
      return window.confirm('Your changes are not saved!\nAre you sure you want to discard your changes?')
    },
    confirmStayOnPage () {
      return this.formChanges() && !this.confirmLeavePage()
    },
    beforeWindowUnload (e) {
      // should we allow the browser to navigate us away?
      if (this.confirmStayOnPage()) {
        // cancel the event
        e.preventDefault()
        // some browsers want returnValue to be set
        e.returnValue = ''
      }
    }
  },
  watch: {
    activityType () {
      this.resetForm()
    },
    // This watches for a route change between Submission and Well Edit and resets the page data
    '$route' (to, from) {
      if (to.path !== from.path) {
        this.setupPage()
      }
    }
  },
  created () {
    this.setupPage()
    this.fetchSurveys()
    // connect our before window unload event listener
    window.addEventListener('beforeunload', this.beforeWindowUnload)
  },
  beforeRouteLeave (to, from, next) {
    // should we allow the router to navigate us away?
    if (this.confirmStayOnPage()) {
      // don't navigate away
      next(false)
    } else {
      // allow navigation
      next()
    }
  },
  beforeDestroy () {
    // disconnect our before window unload event listener
    window.removeEventListener('beforeunload', this.beforeWindowUnload)
  }
}

function initialState () {
  return {
    activityType: 'CON',
    formIsFlat: false,
    preview: false,
    loading: false,
    wellFetchError: null,
    confirmSubmitModal: false,
    formSubmitSuccess: false,
    formSubmitSuccessWellTag: null,
    formSubmitError: false,
    formSubmitLoading: false,
    sliding: null,
    trackValueChanges: false,
    errors: {},
    form: {},
    submissionsHistory: [], // historical submissions for each well (comes into play for staff edits)
    isPublished: false,
    formOptions: {},
    surveys: {
      submissions: [],
      edit: []
    },
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
        'submissionHistory',
        'wellPublicationStatus',
        'wellType',
        'wellOwner',
        'workDates',
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
        'aquiferData',
        'editHistory'
      ]
    }
  }
}
</script>

<style lang="scss">
@import '~vuejs-noty/dist/vuejs-noty.css';

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
    max-width: 4rem;
  }
  .input-width-medium {
    max-width: 6rem;
  }
  .loader {
    border: 5px solid #f3f3f3;
    border-top: 5px solid #5b7b9c;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: inline-block;
    text-align: center;
    vertical-align: middle;
    animation: spin 2s linear infinite;
  }
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  .notifyText {
    font-size: 18px;
    display: inline-block;
    text-align: center;
    vertical-align: middle;
    margin-left: 20px;
    padding-top: 3px;
  }
  .errorTitle {
    font-size: 18px;
  }
  .errorText {
    font-size: 18px;
    padding-right: 20px;
  }
  .closeBtn {
    position: absolute;
    right: 10px;
    top: 5px;
  }
</style>
