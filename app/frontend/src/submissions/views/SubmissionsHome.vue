<template>
  <div class="card" v-if="userRoles.wells.edit || userRoles.submissions.edit">
    <div class="card-body">
      <h4 class="card-title">
        <b-row>
          <b-col lg="12" >Well Activity Submission
            <b-form-group>
              <b-form-radio-group button-variant="outline-primary" size="sm" buttons v-model="formIsFlat" label="Form layout" class="float-right">
                <b-form-radio v-bind:value="true" id="flat">Single page</b-form-radio>
                <b-form-radio v-bind:value="false">Multi page</b-form-radio>
              </b-form-radio-group>
            </b-form-group>
          </b-col>
        </b-row>
      </h4>
      <p>Submit activity on a well. <a href="/gwells/">Try a search</a> to see if the well exists in the system before submitting a report.</p>

      <!-- Activity submission form -->
      <b-form @submit.prevent="confirmSubmit">

        <!-- Form load/save -->
        <b-row>
          <b-col class="text-right">
            <b-btn size="sm" variant="outline-primary" @click="saveForm">
              Save report progress
              <transition name="bounce" mode="out-in">
                  <i v-show="saveFormSuccess" class="fa fa-check text-success"></i>
              </transition>
            </b-btn>
            <b-btn size="sm" variant="outline-primary" @click="loadConfirmation" ref="confirmLoadBtn" :disabled="isLoadFormDisabled">
              Load saved report
              <transition name="bounce">
                  <i v-show="loadFormSuccess" class="fa fa-check text-success"></i>
              </transition>
            </b-btn>
          </b-col>
        </b-row>

        <!-- Type of work performed -->
        <activity-type class="my-3"
          v-if="currentStep === 'activityType' || (formIsFlat && flatForm.activityType)"
          :wellActivityType.sync="activityType"
        />

        <!-- Type of well -->
        <well-type class="my-3"
          v-if="currentStep === 'wellType' || (formIsFlat && flatForm.wellType)"
          :wellTagNumber.sync="form.well"
          :wellActivityType.sync="activityType"
          :wellClass.sync="form.well_class"
          :wellSubclass.sync="form.well_subclass"
          :intendedWaterUse.sync="form.intended_water_use"
          :units.sync="units"
          :idPlateNumber.sync="form.identification_plate_number"
          :wellPlateAttached.sync="form.well_plate_attached"
          :workStartDate.sync="form.work_start_date"
          :workEndDate.sync="form.work_end_date"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        />

        <!-- Person responsible for work -->
        <person-responsible class="my-3"
          v-if="formStep === 'personResponsible' || (formIsFlat && flatForm.personResponsible)"
          :drillerName.sync="form.driller_name"
          :consultantName.sync="form.consultant_name"
          :consultantCompany.sync="form.consultant_company"
          :personResponsible.sync="form.driller_responsible"
          :drillerSameAsPersonResponsible.sync="form.meta.drillerSameAsPersonResponsible"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        />

        <!-- Owner information -->
        <owner class="my-3"
          v-if="currentStep === 'wellOwner' || (formIsFlat && flatForm.wellOwner)"
          :ownerFullName.sync="form.owner_full_name"
          :ownerMailingAddress.sync="form.owner_mailing_address"
          :ownerProvinceState.sync="form.owner_province_state"
          :ownerCity.sync="form.owner_city"
          :ownerPostalCode.sync="form.owner_postal_code"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        />

        <!-- Well location -->
        <location class="my-3"
          v-if="currentStep === 'wellLocation' || (formIsFlat && flatForm.wellLocation)"
          :ownerMailingAddress.sync="form.owner_mailing_address"
          :ownerProvinceState.sync="form.owner_province_state"
          :ownerCity.sync="form.owner_city"
          :ownerPostalCode.sync="form.owner_postal_code"
          :streetAddress.sync="form.street_address"
          :city.sync="form.city"
          :legalLot.sync="form.legal_lot"
          :legalPlan.sync="form.legal_plan"
          :legalDistrictLot.sync="form.legal_district_lot"
          :legalBlock.sync="form.legal_block"
          :legalSection.sync="form.legal_section"
          :legalTownship.sync="form.legal_township"
          :legalRange.sync="form.legal_range"
          :landDistrict.sync="form.land_district"
          :legalPID.sync="form.legal_pid"
          :wellLocationDescription.sync="form.well_location_description"
        />

        <!-- Coords -->
        <coords class="my-3"
          v-if="currentStep === 'wellCoords' || (formIsFlat && flatForm.wellCoords)"
          :latitude.sync="form.latitude"
          :longitude.sync="form.longitude"
        />

        <!-- Method of Drilling -->
        <method-of-drilling class="my-3"
          v-if="currentStep === 'method' || (formIsFlat && flatForm.method)"

          :groundElevation.sync="form.ground_elevation"
          :groundElevationMethod.sync="form.ground_elevation_method"
          :drillingMethod.sync="form.drilling_method"
          :otherDrillingMethod.sync="form.other_drilling_method"
          :wellOrientation.sync="form.well_orientation"
        />

        <!-- Closure/Decommission Description -->
        <closure-description class="my-3"
          v-if="currentStep === 'closureDescription' || (formIsFlat && flatForm.closureDescription)"
          :closureDescriptionSet.sync="form.decommission_description_set">

        </closure-description>

        <!-- Lithology -->
        <lithology class="my-3"
          v-if="currentStep === 'lithology' || (formIsFlat && flatForm.lithology)"
          :lithology.sync="form.lithologydescription_set"
        />

        <!-- Casings -->
        <casings class="my-3"
          :key="`casingsComponent${componentUpdateTrigger}`"
          v-if="currentStep === 'casings' || (formIsFlat && flatForm.casings)"
          :casings.sync="form.casing_set"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        />

        <!-- Surface Seal / Backfill Material -->
        <backfill class="my-3"
          v-if="currentStep === 'backfill' || (formIsFlat && flatForm.backfill)"
          :surfaceSealMaterial.sync="form.surface_seal_material"
          :surfaceSealDepth.sync="form.surface_seal_depth"
          :surfaceSealThickness.sync="form.surface_seal_thickness"
          :surfaceSealMethod.sync="form.surface_seal_method"
          :backfillAboveSurfaceSeal.sync="form.backfill_above_surface_seal"
          :backfillDepth.sync="form.backfill_above_surface_seal_depth"
        />

        <!-- Liner Information -->
        <liner class="my-3"
          v-if="currentStep === 'liner' || (formIsFlat && flatForm.liner)"
          :linerMaterial.sync="form.liner_material"
          :linerDiameter.sync="form.liner_diameter"
          :linerThickness.sync="form.liner_thickness"
          :linerFrom.sync="form.liner_from"
          :linerTo.sync="form.liner_to"
          :linerPerforations.sync="form.linerperforation_set"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        />

        <!-- Screens -->
        <screens class="my-3"
          v-if="currentStep === 'screens' || (formIsFlat && flatForm.screens)"
          :screenIntakeMethod.sync="form.screen_intake_method"
          :screenType.sync="form.screen_type"
          :screenMaterial.sync="form.screen_material"
          :otherScreenMaterial.sync="form.other_screen_material"
          :screenOpening.sync="form.screen_opening"
          :screenBottom.sync="form.screen_bottom"
          :screens.sync="form.screen_set"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        />

        <!-- Filter Pack -->
        <filterPack class="my-3"
          v-if="currentStep === 'filterPack' || (formIsFlat && flatForm.filterPack)"
          :filterPackFrom.sync="form.filter_pack_from"
          :filterPackTo.sync="form.filter_pack_to"
          :filterPackThickness.sync="form.filter_pack_thickness"
          :filterPackMaterial.sync="form.filter_pack_material"
          :filterPackMaterialSize.sync="form.filter_pack_material_size"
        />

        <!-- Well Development -->
        <development class="my-3"
          v-if="currentStep === 'wellDevelopment' || (formIsFlat && flatForm.wellDevelopment)"
          :developmentMethod.sync="form.development_method"
          :developmentHours.sync="form.development_hours"
          :developmentNotes.sync="form.development_notes"
        />

        <!-- Yield (Production Data) -->
        <yield class="my-3"
          v-if="currentStep === 'wellYield' || (formIsFlat && flatForm.wellYield)"
          :productionData.sync="form.production_data_set"
        />

        <!-- Water Quality -->
        <water-quality class="my-3"
          v-if="currentStep === 'waterQuality' || (formIsFlat && flatForm.waterQuality)"
          :waterQualityCharacteristics.sync="form.water_quality_characteristics"
          :waterQualityColour.sync="form.water_quality_colour"
          :waterQualityOdour.sync="form.water_quality_odour"
          :emsID.sync="form.ems_id"
        />

        <!-- Well Completion Data -->
        <completion class="my-3"
          v-if="currentStep === 'wellCompletion' || (formIsFlat && flatForm.wellCompletion)"
          :totalDepthDrilled.sync="form.total_depth_drilled"
          :finishedWellDepth.sync="form.finished_well_depth"
          :finalCasingStickUp.sync="form.final_casing_stick_up"
          :bedrockDepth.sync="form.bedrock_depth"
          :staticWaterLevel.sync="form.static_water_level"
          :wellYield.sync="form.well_yield"
          :artesianFlow.sync="form.artesian_flow"
          :artesianPressure.sync="form.artesian_pressure"
          :wellCapType.sync="form.well_cap_type"
          :wellDisinfected.sync="form.well_disinfected"
        />

        <decommission-information class="my-3"
          v-if="currentStep === 'decommissionInformation' || (formIsFlat && flatForm.decommissionInformation)"
          :finishedWellDepth.sync="form.finished_well_depth"
          :decommissionReason.sync="form.decommission_reason"
          :decommissionMethod.sync="form.decommission_method"
          :sealantMaterial.sync="form.sealant_material"
          :backfillMaterial.sync="form.backfill_material"
          :decommissionDetails.sync="form.decommission_details"
        />

        <!-- Comments -->
        <comments class="my-3"
          v-if="currentStep === 'comments' || (formIsFlat && flatForm.comments)"
          :comments.sync="form.comments"
          :alternativeSpecsSubmitted.sync="form.alternative_specs_submitted"
        />

        <!-- Back / Next / Submit controls -->
        <b-row class="mt-5">
          <b-col v-if="!formIsFlat">
            <b-btn v-if="step > 1" @click="step > 1 ? step-- : null" variant="primary">Back</b-btn>
          </b-col>
          <b-col :class="`pr-4 ${formIsFlat ? '':'text-right'}`">
            <b-btn v-if="step < maxSteps && !formIsFlat" @click="step++" variant="primary">Next</b-btn>
            <b-btn v-else id="formSubmitButton" type="submit" variant="primary" ref="activitySubmitBtn">Submit</b-btn>
          </b-col>
        </b-row>
      </b-form>

      <!-- Form submission success message -->
      <b-alert
          :show="formSubmitSuccess"
          dismissible
          @dismissed="formSubmitSuccess=false"
          variant="success"
          class="mt-3">Report submitted!</b-alert>

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

      <!-- Form reload (load from save) confirmation -->
      <b-modal
          v-model="confirmLoadModal"
          centered
          title="Confirm load submission data"
          @shown="$refs.confirmLoadConfirmBtn.focus()"
          :return-focus="$refs.loadFormBtn">
        Are you sure you want to load the previously saved activity report? Your current report will be overwritten.
        <div slot="modal-footer">
          <b-btn variant="primary" @click="confirmLoadModal=false;loadForm()" ref="confirmLoadConfirmBtn">
            Load
          </b-btn>
          <b-btn variant="light" @click="confirmLoadModal=false">
            Cancel
          </b-btn>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import { FETCH_CODES } from '../store/actions.types.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'
import ActivityType from '@/submissions/components/SubmissionForm/ActivityType.vue'
import WellType from '@/submissions/components/SubmissionForm/WellType.vue'
import PersonResponsible from '@/submissions/components/SubmissionForm/PersonResponsible.vue'
import Owner from '@/submissions/components/SubmissionForm/Owner.vue'
import Location from '@/submissions/components/SubmissionForm/Location.vue'
import Coords from '@/submissions/components/SubmissionForm/Coords.vue'
import MethodOfDrilling from '@/submissions/components/SubmissionForm/MethodOfDrilling.vue'
import Lithology from '@/submissions/components/SubmissionForm/Lithology.vue'
import Casings from '@/submissions/components/SubmissionForm/Casings.vue'
import Backfill from '@/submissions/components/SubmissionForm/Backfill.vue'
import Liner from '@/submissions/components/SubmissionForm/Liner.vue'
import Screens from '@/submissions/components/SubmissionForm/Screens.vue'
import FilterPack from '@/submissions/components/SubmissionForm/FilterPack.vue'
import Development from '@/submissions/components/SubmissionForm/Development.vue'
import Yield from '@/submissions/components/SubmissionForm/Yield.vue'
import WaterQuality from '@/submissions/components/SubmissionForm/WaterQuality.vue'
import Completion from '@/submissions/components/SubmissionForm/Completion.vue'
import Comments from '@/submissions/components/SubmissionForm/Comments.vue'
import ClosureDescription from '@/submissions/components/SubmissionForm/ClosureDescription.vue'
import DecommissionInformation from '@/submissions/components/SubmissionForm/DecommissionInformation.vue'
export default {
  name: 'SubmissionsHome',
  mixins: [inputFormatMixin],
  components: {
    ActivityType,
    WellType,
    PersonResponsible,
    Owner,
    Location,
    Coords,
    MethodOfDrilling,
    Lithology,
    Casings,
    Backfill,
    Liner,
    Screens,
    FilterPack,
    Development,
    Yield,
    WaterQuality,
    Completion,
    Comments,
    ClosureDescription,
    DecommissionInformation
  },
  data () {
    return {
      activityType: 'CON',
      formIsFlat: false,
      units: 'imperial',
      confirmSubmitModal: false,
      formSubmitLoading: false,
      formSubmitSuccess: false,
      formSubmitError: false,
      saveFormSuccess: false,
      hasHadSaveFormSuccess: false,
      loadFormSuccess: false,
      confirmLoadModal: false,
      // componentUpdateTrigger can be appended to a component's key. Changing this value will cause
      // these components to be re-created, allowing the created() and mounted() hooks to re-run.
      componentUpdateTrigger: 0,
      step: 1,
      sliding: null,
      errors: {},
      fieldsLoaded: {},
      form: {},
      formOptions: {},
      formSteps: {
        CON: [
          'activityType',
          'wellType',
          'wellOwner',
          'wellLocation',
          'wellCoords',
          'method',
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
          'comments'
        ],
        ALT: [
          'activityType',
          'wellType',
          'wellOwner',
          'wellLocation',
          'wellCoords',
          'method',
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
          'comments'
        ],
        DEC: [
          'activityType',
          'wellType',
          'wellOwner',
          'wellLocation',
          'wellCoords',
          'method',
          'closureDescription',
          'casings',
          'decommissionInformation',
          'comments'
        ],
        STAFF_EDIT: [
          'activityType'
        ]
      }
    }
  },
  computed: {
    formStep () {
      // the numbered step that the user is on
      // this value is bound by the length of the list of steps for the
      // current type of submission
      return (this.step % (this.maxSteps + 1))
    },
    maxSteps () {
      return this.formSteps[this.activityType].length
    },
    currentStep () {
      // the string name of the step corresponding to formStep
      // this will determine which step is currently displayed
      return this.formSteps[this.activityType][this.formStep - 1]
    },
    flatForm () {
      // returns an object describing which components should be displayed
      // when in "flat form" mode

      const activityType = this.activityType
      const components = {}

      this.formSteps[activityType].forEach((step) => {
        components[step] = true
      })

      return components
    },
    isLoadFormDisabled () {
      // During unit tests, the localStorage object might not exist, so we have to check it's existence.
      return !window.localStorage || (window.localStorage.getItem('savedFormData') === null && !this.hasHadSaveFormSuccess)
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

      this.formSubmitLoading = true
      this.formSubmitSuccess = false
      this.formSubmitError = false
      this.errors = {}
      // Depending on the type of submission (construction/decommission/alteration/edit) we post to
      // different endpoints.
      const PATH = this.codes.activity_types.find((item) => item.code === this.activityType).path
      ApiService.post(PATH, data).then(() => {
        this.formSubmitSuccess = true
        this.resetForm()
      }).catch((error) => {
        this.errors = error.response.data
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
        latitude: '',
        longitude: '',
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
    saveForm () {
      // saves a copy of form data locally
      this.saveStatusReset()
      const data = JSON.stringify(this.form)
      localStorage.setItem('savedFormData', data)
      setTimeout(() => { this.saveFormSuccess = true }, 10)
      setTimeout(() => { this.saveFormSuccess = false; this.hasHadSaveFormSuccess = true }, 1000)
    },
    loadForm () {
      this.saveStatusReset()
      const storedData = localStorage.getItem('savedFormData')
      if (storedData) {
        this.resetForm()

        // some form features depend on watching form field values.
        // setTimeout pushes rendering new data down execution queue
        // to give watchers a chance to act on each set of changes
        // (e.g. form reset, form population)
        setTimeout(() => {
          const parsedData = JSON.parse(storedData)
          this.form = Object.assign(this.form, parsedData)
          this.fieldsLoaded = Object.assign(this.fieldsLoaded, parsedData)
          setTimeout(() => { this.loadFormSuccess = true }, 0)
          setTimeout(() => { this.fieldsLoaded = {} }, 0)
          setTimeout(() => { this.loadFormSuccess = false }, 1000)
        }, 0)
      }
    },
    loadConfirmation () {
      this.confirmLoadModal = true
    },
    saveStatusReset () {
      this.saveFormSuccess = false
      this.loadFormSuccess = false
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
