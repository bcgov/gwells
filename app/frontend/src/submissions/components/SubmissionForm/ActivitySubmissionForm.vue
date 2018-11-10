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
  <div>
    <h1 class="card-title">
      <b-row>
        <b-col cols="12">
          <div v-if="isStaffEdit" id="top">Well Edit Page</div>
          <div v-else>Well Activity Submission</div>
          <b-form-group v-if="activityType !== 'STAFF_EDIT'">
            <b-form-radio-group button-variant="outline-primary" size="sm" buttons v-model="formIsFlatInput" label="Form layout" class="float-right">
              <b-form-radio v-bind:value="true" id="singleSubmissionPage">Single page</b-form-radio>
              <b-form-radio v-bind:value="false" id="multiSubmissionPage">Multi page</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
      </b-row>
    </h1>
    <b-row v-if="isStaffEdit">
        <b-col lg="3" v-for="step in formSteps[activityType]" :key='step'>
          <a :href="'#' + step">{{formStepDescriptions[step] ? formStepDescriptions[step] : step}}</a>
        </b-col>
      </b-row>
    <p v-if="!isStaffEdit">Submit activity on a well. <a href="/gwells/">Try a search</a> to see if the well exists in the system before submitting a report.</p>

    <!-- Form load/save -->
    <b-row v-if="!isStaffEdit">
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
      v-if="showSection('activityType')"
      id="activityType"
      :wellActivityType.sync="activityTypeInput"
    />

    <!-- Type of well -->
    <well-type class="my-3"
      v-if="showSection('wellType')"
      id="wellType"
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
      v-if="showSection('personResponsible')"
      id="personResponsible"
      :drillerName.sync="form.driller_name"
      :consultantName.sync="form.consultant_name"
      :consultantCompany.sync="form.consultant_company"
      :personResponsible.sync="form.driller_responsible"
      :drillerSameAsPersonResponsible.sync="form.meta.drillerSameAsPersonResponsible"
      :errors="errors"
      :fieldsLoaded="fieldsLoaded"
      :isStaffEdit="isStaffEdit"
      :saveDisabled="editSaveDisabled"
      v-on:save="$emit('submit_edit')"
    />

    <!-- Owner information -->
    <owner class="my-3"
      v-if="showSection('wellOwner')"
      id="wellOwner"
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
      v-if="showSection('wellLocation')"
      id="wellLocation"
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
      v-if="showSection('wellCoords')"
      id="wellCoords"
      :latitude.sync="form.latitude"
      :longitude.sync="form.longitude"
    />

    <!-- Method of Drilling -->
    <method-of-drilling class="my-3"
      v-if="showSection('method')"
      id="method"
      :groundElevation.sync="form.ground_elevation"
      :groundElevationMethod.sync="form.ground_elevation_method"
      :drillingMethod.sync="form.drilling_method"
      :otherDrillingMethod.sync="form.other_drilling_method"
      :wellOrientation.sync="form.well_orientation"
    />

    <!-- Closure/Decommission Description -->
    <closure-description class="my-3"
      v-if="showSection('closureDescription')"
      id="closureDescription"
      :closureDescriptionSet.sync="form.decommission_description_set">

    </closure-description>

    <!-- Lithology -->
    <lithology class="my-3"
      v-if="showSection('lithology')"
      id="lithology"
      :lithology.sync="form.lithologydescription_set"
    />

    <!-- Casings -->
    <casings class="my-3"
      :key="`casingsComponent${componentUpdateTrigger}`"
      v-if="showSection('casings')"
      id="casings"
      :casings.sync="form.casing_set"
      :errors="errors"
      :fieldsLoaded="fieldsLoaded"
    />

    <!-- Surface Seal / Backfill Material -->
    <backfill class="my-3"
      v-if="showSection('backfill')"
      id="backfill"
      :surfaceSealMaterial.sync="form.surface_seal_material"
      :surfaceSealDepth.sync="form.surface_seal_depth"
      :surfaceSealThickness.sync="form.surface_seal_thickness"
      :surfaceSealMethod.sync="form.surface_seal_method"
      :backfillAboveSurfaceSeal.sync="form.backfill_above_surface_seal"
      :backfillDepth.sync="form.backfill_above_surface_seal_depth"
    />

    <!-- Liner Information -->
    <liner class="my-3"
      :key="`linerComponent${componentUpdateTrigger}`"
      v-if="showSection('liner')"
      id="liner"
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
      :key="`screensComponent${componentUpdateTrigger}`"
      v-if="showSection('screens' )"
      id="screens"
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
      v-if="showSection('filterPack')"
      id="filterPack"
      :filterPackFrom.sync="form.filter_pack_from"
      :filterPackTo.sync="form.filter_pack_to"
      :filterPackThickness.sync="form.filter_pack_thickness"
      :filterPackMaterial.sync="form.filter_pack_material"
      :filterPackMaterialSize.sync="form.filter_pack_material_size"
    />

    <!-- Well Development -->
    <development class="my-3"
      v-if="showSection('wellDevelopment')"
      id="wellDevelopment"
      :developmentMethod.sync="form.development_method"
      :developmentHours.sync="form.development_hours"
      :developmentNotes.sync="form.development_notes"
    />

    <!-- Yield (Production Data) -->
    <yield class="my-3"
      v-if="showSection('wellYield')"
      id="wellYield"
      :productionData.sync="form.production_data_set"
    />

    <!-- Water Quality -->
    <water-quality class="my-3"
      v-if="showSection('waterQuality')"
      id="waterQuality"
      :waterQualityCharacteristics.sync="form.water_quality_characteristics"
      :waterQualityColour.sync="form.water_quality_colour"
      :waterQualityOdour.sync="form.water_quality_odour"
      :emsID.sync="form.ems_id"
    />

      <!-- Well Completion Data -->
    <completion class="my-3"
      v-if="showSection('wellCompletion')"
      id="wellCompletion"
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
      v-if="showSection('decommissionInformation')"
      id="decommissionInformation"
      :finishedWellDepth.sync="form.finished_well_depth"
      :decommissionReason.sync="form.decommission_reason"
      :decommissionMethod.sync="form.decommission_method"
      :sealantMaterial.sync="form.sealant_material"
      :backfillMaterial.sync="form.backfill_material"
      :decommissionDetails.sync="form.decommission_details"
    />

    <!-- Comments -->
    <comments class="my-3"
      v-if="showSection('comments')"
      id="comments"
      :comments.sync="form.comments"
      :alternativeSpecsSubmitted.sync="form.alternative_specs_submitted"
    />

    <!-- Back / Next / Submit controls -->
    <b-row v-if="isStaffEdit" class="mt-5">
      <b-col class="pr-4 text-right">
        <b-btn variant="primary" @click="$emit('submit_edit')" :disabled="editSaveDisabled">Save</b-btn>
      </b-col>
    </b-row>
    <b-row v-else class="mt-5">
      <b-col v-if="!formIsFlat">
        <b-btn v-if="step > 1 && !formIsFlat" @click="step > 1 ? step-- : null" variant="primary">Back</b-btn>
      </b-col>
      <b-col class="pr-4 text-right">
        <b-btn v-if="step < maxSteps && !formIsFlat" @click="step++" variant="primary" id="nextSubmissionStep">Next</b-btn>
        <span v-else>
          <b-btn variant="primary" @click="$emit('preview')" id="formPreviewButton">Preview &amp; Submit</b-btn>
        </span>
      </b-col>
    </b-row>

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
</template>

<script>
import ActivityType from './ActivityType.vue'
import WellType from './WellType.vue'
import PersonResponsible from './PersonResponsible.vue'
import Owner from './Owner.vue'
import Location from './Location.vue'
import Coords from './Coords.vue'
import MethodOfDrilling from './MethodOfDrilling.vue'
import Lithology from './Lithology.vue'
import Casings from './Casings.vue'
import Backfill from './Backfill.vue'
import Liner from './Liner.vue'
import Screens from './Screens.vue'
import FilterPack from './FilterPack.vue'
import Development from './Development.vue'
import Yield from './Yield.vue'
import WaterQuality from './WaterQuality.vue'
import Completion from './Completion.vue'
import Comments from './Comments.vue'
import ClosureDescription from './ClosureDescription.vue'
import DecommissionInformation from './DecommissionInformation.vue'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'SubmissionsForm',
  mixins: [inputBindingsMixin],
  props: {
    form: {
      type: Object,
      isInput: false
    },
    sections: {
      type: Object,
      isInput: false
    },
    activityType: {
      type: String
    },
    formIsFlat: {
      type: Boolean
    },
    formSteps: {
      type: Object,
      isInput: false
    },
    errors: {
      type: Object,
      isInput: false
    },
    trackValueChanges: {
      type: Boolean,
      isInput: false
    },
    formSubmitLoading: {
      type: Boolean,
      isInput: false
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    }
  },
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
      units: 'imperial',
      saveFormSuccess: false,
      hasHadSaveFormSuccess: false,
      loadFormSuccess: false,
      confirmLoadModal: false,
      formValueChanged: false,
      // componentUpdateTrigger can be appended to a component's key. Changing this value will cause
      // these components to be re-created, allowing the created() and mounted() hooks to re-run.
      componentUpdateTrigger: 0,
      step: 1,
      fieldsLoaded: {},
      formStepDescriptions: {
        'activityType': 'Type of work',
        'wellType': 'Well class',
        'wellOwner': 'Well owner',
        'wellLocation': 'Well location',
        'wellCoords': 'Geographic coordinates',
        'method': 'Method of drilling',
        'closureDescription': 'Decommission description',
        'lithology': 'Lithology',
        'casings': 'Casing details',
        'backfill': 'Surface seal and backfill information',
        'liner': 'Liner information',
        'screens': 'Screen information',
        'filterPack': 'Filter pack',
        'wellDevelopment': 'Well development',
        'wellYield': 'Well yield estimation',
        'waterQuality': 'Water quality',
        'wellCompletion': 'Well completion data',
        'decommissionInformation': 'Well decommission information',
        'comments': 'Comments',
        'personResponsible': 'Person Responsible for Work'
      }
    }
  },
  watch: {
    // we need this empty watch section for the code in beforeCreate
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
    isLoadFormDisabled () {
      // During unit tests, the localStorage object might not exist, so we have to check it's existence.
      return !window.localStorage || (window.localStorage.getItem('savedFormData') === null && !this.hasHadSaveFormSuccess)
    },
    editSaveDisabled () {
      return this.formSubmitLoading || !this.formValueChanged
    }
  },
  methods: {
    showSection (stepName) {
      return this.currentStep === stepName || (this.formIsFlat && stepName in this.sections)
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
        this.$emit('resetForm')

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
    }
  },
  created () {
    // When the form is saved, reset the formValueChanged variable.
    this.$parent.$on('formSaved', () => { this.formValueChanged = false })
  },
  beforeCreate () {
    // We know right from the start if this is going to be a SubmissionsEdit, and then we add watches
    // on all the form fields.
    // Unfortunately watches aren't very fast, and there will be a lot of code bloat if we instead
    // switch to using computed properties, which would be faster. We'd have to add a getter and setter
    // for every single form field!
    if (this.$route.name === 'SubmissionsEdit') {
      Object.keys(this.$options.propsData.form).forEach((key) => {
        // We have to add the watches in beforeCreate.
        this.$options.watch[`form.${key}`] = {
          handler (newValue, oldValue) {
            if (this.trackValueChanges) {
              this.formValueChanged = true
              this.form.meta.valueChanged[key] = true
            }
          }
        }
      })
    }
  }
}
</script>

<style lang="css">

</style>
