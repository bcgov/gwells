<template>
  <div class="card" v-if="userRoles.wells.edit || userRoles.submissions.edit">
    <div class="card-body">

      <b-form @submit.prevent="confirmSubmit">
        <!-- if preview === true : Preview -->
        <submission-preview
          v-if="preview"
          :form="form"
          :activity="activityType"
          :sections="displayFormSection"
          :errors="errors"
          v-on:back="handlePreviewBackButton"
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
          v-on:preview="handlePreviewButton"
          v-on:resetForm="resetForm"
          />

        <!-- Form submission success message -->
        <b-alert
            :show="formSubmitSuccess"
            dismissible
            @dismissed="formSubmitSuccess=false"
            variant="success"
            class="mt-3">Report submitted!
          <a v-if="formSubmitSuccessWellTag" :href="`/gwells/well/${formSubmitSuccessWellTag}`">
            View well details for well {{formSubmitSuccessWellTag}}
          </a>
        </b-alert>

        <!-- Form submission error message -->
        <b-alert
            :show="formSubmitError"
            dismissible
            @dismissed="formSubmitError=false"
            variant="danger"
            class="mt-3">
          <span v-if="errors && errors.detail">
            {{ errors.detail }}
          </span>
          <div v-if="errors && errors != {}">
            <div v-for="(field, i) in Object.keys(errors)" :key="`submissionError${i}`">
              {{field | readable}} : <span v-for="(e, j) in errors[field]" :key="`submissionError${i}-${j}`">{{ e }}</span>
            </div>
          </div>
        </b-alert>

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
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import { FETCH_CODES } from '../store/actions.types.js'
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
      confirmSubmitModal: false,
      formSubmitSuccess: false,
      formSubmitSuccessWellTag: null,
      formSubmitError: false,
      sliding: null,
      errors: {},
      form: {},
      formOptions: {},
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
          'liner',
          'screens',
          'filterPack',
          'wellDevelopment',
          'wellYield',
          'waterQuality',
          'wellCompletion',
          'comments'
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
          'liner',
          'screens',
          'filterPack',
          'wellDevelopment',
          'wellYield',
          'waterQuality',
          'wellCompletion',
          'comments'
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
          'comments'
        ],
        STAFF_EDIT: [
          'wellType',
          'personResponsible',
          'wellOwner',
          'wellLocation',
          'wellCoords',
          'method',
          'closureDescription',
          'lithology',
          'casings',
          'backfill',
          'liner',
          'screens',
          'filterPack',
          'wellDevelopment',
          'wellYield',
          'waterQuality',
          'wellCompletion',
          'decommissionInformation',
          'comments'
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
    ...mapGetters(['codes', 'userRoles'])
  },
  methods: {
    formSubmit () {
      const data = Object.assign({}, this.form)

      // delete "meta" data (form input that need not be submitted) stored within form object
      delete data.meta

      // replace the "person responsible" object with the person's guid
      if (data.driller_responsible && data.driller_responsible.person_guid) {
        data.driller_responsible = data.driller_responsible.person_guid
      }

      if (data.well && data.well.well_tag_number) {
        data.well = data.well.well_tag_number
      }

      this.stripBlankStrings(data)

      data.linerperforation_set = this.filterBlankRows(data.linerperforation_set)
      data.lithologydescription_set = this.filterBlankRows(data.lithologydescription_set)
      data.production_data_set = this.filterBlankRows(data.production_data_set)
      data.screen_set = this.filterBlankRows(data.screen_set)
      data.casing_set = this.filterBlankRows(data.casing_set)
      data.decommission_description_set = this.filterBlankRows(data.decommission_description_set)

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
        this.resetForm()
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
      }).finally(() => {
        this.formSubmitLoading = false
      })
    },
    confirmSubmit () {
      this.confirmSubmitModal = true
    },
    resetForm () {
      this.form = {
        well: null,
        well_class: '',
        well_subclass: '',
        intended_water_use: '',
        identification_plate_number: null,
        well_plate_attached: '',
        driller_responsible: null,
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
        ground_elevation: null,
        ground_elevation_method: '',
        drilling_method: '',
        well_orientation: '',
        lithologydescription_set: [],
        surface_seal_material: '',
        surface_seal_depth: '',
        surface_seal_thickness: '',
        surface_seal_method: '',
        backfill_above_surface_seal: '',
        backfill_above_surface_seal_depth: '',
        casing_set: [],
        screen_intake_method: '',
        screen_type: '',
        screen_material: '',
        other_screen_material: '',
        screen_opening: '',
        screen_bottom: '',
        screen_set: [],
        development_method: '',
        development_hours: '',
        development_notes: '',
        production_data_set: [],
        filter_pack_from: '',
        filter_pack_to: '',
        filter_pack_thickness: '',
        filter_pack_material: '',
        filter_pack_material_size: '',
        water_quality_characteristics: [],
        water_quality_colour: '',
        water_quality_odour: '',
        ems_id: '',
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
        alternative_specs_submitted: 'False',
        decommission_description_set: [],
        decommission_reason: '',
        decommission_method: '',
        sealant_material: '',
        backfill_material: '',
        decommission_details: '',

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
      this.$nextTick(function () {
        window.scrollTo(0, 0)
      })
    },
    handlePreviewBackButton () {
      this.preview = false
      this.$nextTick(function () {
        window.scrollTo(0, 0)
      })
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
    }
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
  max-width: 5rem;
}
.input-width-medium {
  max-width: 10rem;
}
</style>
