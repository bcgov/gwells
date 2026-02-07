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
          <div v-if="isStaffEdit" id="top">Update Well Information</div>
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

    <div v-if="loading">
      <b-row>
        <b-col cols="12">
          <div class="fa-2x text-center">
            Loading...
          </div>
          <div class="fa-2x text-center">
            <i class="fa fa-circle-o-notch fa-spin"></i>
          </div>
        </b-col>
      </b-row>
    </div>
    <div v-else>
      <b-alert show v-if="isStaffEdit && isUnpublished" variant="info">
        This well is unpublished and will be hidden from DataBC, iMapBC, GWELLS Well Search, and the CSV/XLS export.
      </b-alert>
      <b-row v-if="isStaffEdit">
          <b-col lg="3" v-for="step in stepCodes" :key='step'>
            <a :href="`#${step}`" @click.prevent="anchorLinkHandler(step)">{{formStepDescriptions[step] ? formStepDescriptions[step] : step}}</a>
          </b-col>
        </b-row>
      <p v-if="!isStaffEdit">Submit activity on a well. <a href="/gwells/" target="_blank">Try a search</a> to see if the well exists in the system before submitting a report.</p>
      <p class="bg-warning p-2">All form fields marked with a trailing asterisk are mandatory fields.</p>

      <!-- Form load/save -->
      <b-row v-if="!isStaffEdit">
        <b-col class="text-right">
          <b-btn size="sm" variant="outline-primary" class="mr-2" @click="saveForm">
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
      <activity-type class="my-5"
        v-if="showSection('activityType')"
        id="activityType"
        v-model:wellActivityType="activityTypeInput"
      />

    <submission-history
      v-if="showSection('submissionHistory')"
      id="submissionHistory"
      :submissionsHistory="submissionsHistory"
      :isStaffEdit="isStaffEdit"
    ></submission-history>

    <!-- Publication Status of well -->
    <publication-status class="my-5"
      v-if="showSection('wellPublicationStatus')"
      id="wellPublicationStatus"
      v-model:wellPublicationStatusCode="form.well_publication_status"
      :errors="errors"
      :fieldsLoaded="fieldsLoaded"
      :isStaffEdit="isStaffEdit"
      :saveDisabled="editSaveDisabled"
      v-on:save="$emit('submit_edit')"
    />

    <!-- Type of well -->
    <well-type class="my-5"
      v-if="showSection('wellType')"
      id="wellType"
      :startDateOfWorkLabel.sync="this.startDateOfWorkLabel"
      :endDateOfWorkLabel.sync="this.endDateOfWorkLabel"
      :wellIdentificationPlateNumberLabel.sync="this.wellIdentificationPlateNumberLabel"
      :wellIdentificationPlateAttachedLabel.sync="this.wellIdentificationPlateAttachedLabel"
      :wellTagNumber.sync="form.well"
      :wellStatusCode.sync="form.well_status"
      :wellActivityType="activityType"
      @update:wellActivityType="$emit('update:activityType', $event)"
      :wellClass.sync="form.well_class"
      :wellSubclass.sync="form.well_subclass"
      :intendedWaterUse.sync="form.intended_water_use"
      :units.sync="units"
      :idPlateNumber.sync="form.identification_plate_number"
      :wellPlateAttached.sync="form.well_identification_plate_attached"
      :idPlateAttachedBy.sync="form.id_plate_attached_by"
      :waterSupplySystem.sync="form.water_supply_system_name"
      :waterSupplyWell.sync="form.water_supply_system_well_name"
      :workStartDate.sync="form.work_start_date"
      :workEndDate.sync="form.work_end_date"
      :errors="errors"
      :fieldsLoaded="fieldsLoaded"
      :isStaffEdit="isStaffEdit"
      :saveDisabled="editSaveDisabled"
      v-on:save="$emit('submit_edit')"
      :handleDateInput="handleDateInput"
    />

      <!-- Type of well -->
      <work-dates class="my-5"
       v-if="showSection('workDates')"
       id="workDates"
       v-model:constructionStartDate="form.construction_start_date"
       v-model:constructionEndDate="form.construction_end_date"
       v-model:alterationStartDate="form.alteration_start_date"
       v-model:alterationEndDate="form.alteration_end_date"
       v-model:decommissionStartDate="form.decommission_start_date"
       v-model:decommissionEndDate="form.decommission_end_date"
       v-model:workStartDate="form.work_start_date"
       v-model:workEndDate="form.work_end_date"
       :errors="errors"
       :fieldsLoaded="fieldsLoaded"
       :isStaffEdit="isStaffEdit"
       :saveDisabled="editSaveDisabled"
       v-on:save="$emit('submit_edit')"
      />

      <!-- Person responsible for work -->
      <person-responsible class="my-5"
        v-if="showSection('personResponsible')"
        id="personResponsible"
        v-model:drillerName="form.driller_name"
        v-model:consultantName="form.consultant_name"
        v-model:consultantCompany="form.consultant_company"
        v-model:personResponsible="form.person_responsible"
        v-model:companyOfPersonResponsible="form.company_of_person_responsible"
        v-model:drillerSameAsPersonResponsible="form.meta.drillerSameAsPersonResponsible"
        :errors="errors"
        :fieldsLoaded="fieldsLoaded"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Owner information -->
      <owner class="my-5"
        v-if="showSection('wellOwner')"
        id="wellOwner"
        v-model:ownerFullName="form.owner_full_name"
        v-model:ownerMailingAddress="form.owner_mailing_address"
        v-model:ownerProvinceState="form.owner_province_state"
        v-model:ownerCity="form.owner_city"
        v-model:ownerPostalCode="form.owner_postal_code"
        v-model:ownerEmail="form.owner_email"
        v-model:ownerTel="form.owner_tel"
        :errors="errors"
        :fieldsLoaded="fieldsLoaded"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Well location -->
      <location class="my-5"
        v-if="showSection('wellLocation')"
        id="wellLocation"
        v-model:ownerMailingAddress="form.owner_mailing_address"
        v-model:ownerProvinceState="form.owner_province_state"
        v-model:ownerCity="form.owner_city"
        v-model:ownerPostalCode="form.owner_postal_code"
        v-model:streetAddress="form.street_address"
        v-model:city="form.city"
        v-model:legalLot="form.legal_lot"
        v-model:legalPlan="form.legal_plan"
        v-model:legalDistrictLot="form.legal_district_lot"
        v-model:legalBlock="form.legal_block"
        v-model:legalSection="form.legal_section"
        v-model:legalTownship="form.legal_township"
        v-model:legalRange="form.legal_range"
        v-model:landDistrict="form.land_district"
        v-model:legalPID="form.legal_pid"
        v-model:wellLocationDescription="form.well_location_description"
        :errors="errors"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Coords -->
      <coords class="my-5"
        v-if="showSection('wellCoords')"
        id="wellCoords"
        ref="wellCoords"
        v-model:latitude="form.latitude"
        v-model:longitude="form.longitude"
        :drinking_water="form.drinking_water_protection_area_ind"
        v-model:coordinateAcquisitionCode="form.coordinate_acquisition_code"
        :isStaffEdit="isStaffEdit"
        :errors="errors"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
        v-on:editWater="editWater"
      />

      <!-- Method of Drilling -->
      <method-of-drilling class="my-5"
        v-if="showSection('method')"
        id="method"
        v-model:drillingMethodsLabel="this.drillingMethodsLabel"
        v-model:groundElevation="form.ground_elevation"
        v-model:groundElevationMethod="form.ground_elevation_method"
        v-model:drillingMethod="form.drilling_methods"
        v-model:wellOrientationStatus="form.well_orientation_status"
        :errors="errors"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Lithology -->
      <lithology class="my-5"
        v-if="showSection('lithology')"
        id="lithology"
        :errors="errors"
        v-model:lithology="form.lithologydescription_set"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Casings -->
      <casings class="my-5"
        :key="`casingsComponent${componentUpdateTrigger}`"
        v-if="showSection('casings')"
        id="casings"
        v-model:casings="form.casing_set"
        :errors="errors"
        :fieldsLoaded="fieldsLoaded"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Surface Seal / Backfill Material -->
      <backfill class="my-5"
        v-if="showSection('backfill')"
        id="backfill"
        :errors="errors"
        v-model:surfaceSealMaterial="form.surface_seal_material"
        v-model:surfaceSealDepth="form.surface_seal_depth"
        v-model:surfaceSealThickness="form.surface_seal_thickness"
        v-model:surfaceSealMethod="form.surface_seal_method"
        v-model:backfillAboveSurfaceSeal="form.backfill_type"
        v-model:backfillDepth="form.backfill_depth"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Liner Information -->
      <liner class="my-5"
        :key="`linerComponent${componentUpdateTrigger}`"
        v-if="showSection('liner')"
        id="liner"
        v-model:linerMaterial="form.liner_material"
        v-model:linerDiameter="form.liner_diameter"
        v-model:linerThickness="form.liner_thickness"
        v-model:linerFrom="form.liner_from"
        v-model:linerTo="form.liner_to"
        v-model:linerPerforations="form.linerperforation_set"
        :errors="errors"
        :fieldsLoaded="fieldsLoaded"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Screens -->
      <screens class="my-5"
        :key="`screensComponent${componentUpdateTrigger}`"
        v-if="showSection('screens')"
        id="screens"
        v-model:screenIntakeMethod="form.screen_intake_method"
        v-model:screenType="form.screen_type"
        v-model:screenMaterial="form.screen_material"
        v-model:otherScreenMaterial="form.other_screen_material"
        v-model:screenOpening="form.screen_opening"
        v-model:screenBottom="form.screen_bottom"
        v-model:screens="form.screen_set"
        v-model:screenInformation="form.screen_information"
        :errors="errors"
        :fieldsLoaded="fieldsLoaded"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Filter Pack -->
      <filterPack class="my-5"
        v-if="showSection('filterPack')"
        id="filterPack"
        :errors="errors"
        v-model:filterPackFrom="form.filter_pack_from"
        v-model:filterPackTo="form.filter_pack_to"
        v-model:filterPackThickness="form.filter_pack_thickness"
        v-model:filterPackMaterial="form.filter_pack_material"
        v-model:filterPackMaterialSize="form.filter_pack_material_size"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Well Development -->
      <development class="my-5"
        v-if="showSection('wellDevelopment')"
        id="wellDevelopment"
        :errors="errors"
        v-model:developmentMethod="form.development_methods"
        v-model:developmentHours="form.development_hours"
        v-model:developmentNotes="form.development_notes"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Yield (Production Data) -->
      <yield class="my-5"
        v-if="showSection('wellYield')"
        id="wellYield"
        :errors="errors"
        v-model:yieldEstimationMethod="form.yield_estimation_method"
        v-model:yieldEstimationRate="form.yield_estimation_rate"
        v-model:yieldEstimationDuration="form.yield_estimation_duration"
        v-model:staticLevel="form.static_level_before_test"
        v-model:drawdown="form.drawdown"
        v-model:hydroFracturingPerformed="form.hydro_fracturing_performed"
        v-model:hydroFracturingYieldIncrease="form.hydro_fracturing_yield_increase"
        v-model:recommendedPumpDepth="form.recommended_pump_depth"
        v-model:recommendedPumpRate="form.recommended_pump_rate"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Water Quality -->
      <water-quality class="my-5"
        v-if="showSection('waterQuality')"
        id="waterQuality"
        v-model:waterQualityCharacteristics="form.water_quality_characteristics"
        v-model:waterQualityColour="form.water_quality_colour"
        v-model:waterQualityOdour="form.water_quality_odour"
        v-model:emsID="form.ems"
        :errors="errors"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

        <!-- Well Completion Data -->
      <completion class="my-5"
        v-if="showSection('wellCompletion')"
        id="wellCompletion"
        v-model:totalDepthDrilledLabel="this.totalDepthDrilledLabel"
        v-model:finishedWellDepthLabel="this.finishedWellDepthLabel"
        v-model:totalDepthDrilled="form.total_depth_drilled"
        v-model:finishedWellDepth="form.finished_well_depth"
        v-model:finalCasingStickUp="form.final_casing_stick_up"
        v-model:bedrockDepth="form.bedrock_depth"
        v-model:staticWaterLevel="form.static_water_level"
        v-model:wellYield="form.well_yield"
        v-model:artesianConditions="form.artesian_conditions"
        v-model:artesianFlow="form.artesian_flow"
        v-model:artesianPressureHead="form.artesian_pressure_head"
        v-model:artesianPressurePSI="form.artesian_pressure"
        v-model:wellCapType="form.well_cap_type"
        v-model:wellDisinfected="form.well_disinfected_status"
        :errors="errors"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Aquifer Data -->
      <aquifer-data class="my-5"
        v-if="showSection('aquiferData')"
        id="aquiferData"
        v-model:aquifer="form.aquifer"
        v-model:aquiferLithology="form.aquifer_lithology"
        :errors="errors"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Observation well info -->
      <observation-well-info class="my-5"
        v-if="showSection('observationWellInfo')"
        id='observationWellInfo'
        v-model:obsWellNumber="form.observation_well_number"
        v-model:obsWellStatus="form.observation_well_status"
        :errors="errors"
        :fieldsLoaded="fieldsLoaded"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Decommission Information -->
      <decommission-information class="my-5"
        v-if="showSection('decommissionInformation')"
        id="decommissionInformation"
        v-model:finishedWellDepth="form.finished_well_depth"
        v-model:decommissionReason="form.decommission_reason"
        v-model:decommissionMethod="form.decommission_method"
        v-model:sealantMaterial="form.decommission_sealant_material"
        v-model:backfillMaterial="form.decommission_backfill_material"
        v-model:decommissionDetails="form.decommission_details"
        :errors="errors"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <!-- Closure/Decommission Description -->
      <closure-description class="my-5"
         v-if="showSection('closureDescription')"
         id="closureDescription"
         :errors="errors"
         :isStaffEdit="isStaffEdit"
         :saveDisabled="editSaveDisabled"
         v-on:save="$emit('submit_edit')"
         v-model:closureDescriptionSet="form.decommission_description_set">
      </closure-description>

      <!-- Comments -->
      <comments class="my-5"
        v-if="showSection('comments')"
        id="comments"
        v-model:comments="form.comments"
        v-model:internalComments="form.internal_comments"
        v-model:alternativeSpecsSubmitted="form.alternative_specs_submitted"
        v-model:technicalReport="form.technical_report"
        v-model:drinkingWaterProtectionArea="form.drinking_water_protection_area_ind"
        :errors="errors"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
        v-on:setFormValueChanged="setFormValueChanged"
      />

      <!-- Documents -->
      <documents class="my-5"
        v-if="showSection('documents')"
        id="documents"
        :wellTagNumber="wellTagNumber"
        :uploadedFiles="uploadedFiles"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        :showDocuments="form.well !== null"
        :form="form"
        v-on:save="$emit('submit_edit')"
        v-on:setFormValueChanged="setFormValueChanged"
        v-on:fetchFiles="fetchFiles"
      />

      <!-- Aquifer Parameters -->
      <aquifer-parameters class="my-5"
        :key="`aquiferParametersComponent${componentUpdateTrigger}`"
        v-if="showSection('aquiferParameters')"
        id="aquiferParameters"
        v-model:aquiferParameters="form.aquifer_parameters_set"
        :errors="errors"
        :fieldsLoaded="fieldsLoaded"
        :isStaffEdit="isStaffEdit"
        :saveDisabled="editSaveDisabled"
        v-on:save="$emit('submit_edit')"
      />

      <vertical-aquifer-extents class="my-5"
        v-if="showSection('aquiferParameters')"
        id="vertical-aquifer-extents"
        :wellTagNumber="wellTagNumber"
      />

      <edit-history class="my-5"
        v-if="showSection('editHistory')"
        id="editHistory"
        :well-tag-number="wellTagNumber"
        :events="events"
      ></edit-history>

      <!-- Back / Next / Submit controls -->
      <b-row v-else class="mt-5">
        <b-col v-if="!formIsFlat">
          <b-btn v-if="step > 1 && !formIsFlat" @click="gotoPrevStep" variant="primary">Back</b-btn>
        </b-col>
        <b-col class="pr-4 text-right">
          <b-btn v-if="step < maxSteps && !formIsFlat" @click="gotoNextStep" variant="primary" id="nextSubmissionStep">Next</b-btn>
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
  </div>
</template>

<script>
import Vue from 'vue'
import smoothScroll from 'smoothscroll'

import ActivityType from './ActivityType.vue'
import AquiferData from './AquiferData.vue'
import VerticalAquiferExtents from './VerticalAquiferExtents.vue'
import WellType from './WellType.vue'
import PublicationStatus from './PublicationStatus.vue'
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
import Documents from './Documents.vue'
import ClosureDescription from './ClosureDescription.vue'
import DecommissionInformation from './DecommissionInformation.vue'
import ObservationWellInfo from './ObservationWellInfo.vue'
import SubmissionHistory from './SubmissionHistory.vue'
import EditHistory from './EditHistory.vue'
import WorkDates from './WorkDates.vue'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import AquiferParameters from './AquiferParameters.vue'
import {
  WELL_SUBMISSION_STRINGS,
  MANDATORY_WELL_SUBMISSION_STRINGS,
  DATE_INPUT_TYPE,
  NEW_WELL_CONSTRUCTION_VALIDATION_DATE
} from '@/common/constants.js'

export default {
  name: 'SubmissionsForm',
  mixins: [inputBindingsMixin],
  props: {
    form: {
      type: Object,
      isInput: false
    },
    events: {
      type: Vue
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
    },
    loading: {
      type: Boolean,
      isInput: false
    },
    uploadedFiles: {
      type: Object,
      isInput: false
    },
    formChanges: {
      type: Function
    },
    submissionsHistory: {
      type: Array,
      default: () => ([])
    },
    isPublished: {
      type: Boolean,
      isInput: false
    }
  },
  components: {
    WorkDates,
    ActivityType,
    AquiferData,
    VerticalAquiferExtents,
    WellType,
    PublicationStatus,
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
    Documents,
    ClosureDescription,
    DecommissionInformation,
    ObservationWellInfo,
    SubmissionHistory,
    EditHistory,
    AquiferParameters
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
        'aquiferData': 'Well testing and aquifer details',
        'wellType': 'Well class',
        'wellPublicationStatus': 'Well publication status',
        'wellOwner': 'Well owner',
        'workDates': 'Well work dates',
        'wellLocation': 'Well location',
        'wellCoords': 'Geographic coordinates',
        'method': 'Method of drilling',
        'closureDescription': 'Decommission description',
        'lithology': 'Lithology',
        'casings': 'Casing details',
        'aquiferParameters': 'Pumping Test Information and Aquifer Parameters',
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
        'personResponsible': 'Person responsible for work',
        'observationWellInfo': 'Observation well information',
        'submissionHistory': 'Activity report history',
        'documents': 'Attachments',
        'editHistory': 'Edit history'
      },
      initLong: null,
      initLat: null,
      workStartDate: '',
      workEndDate: '',
      // Labelling "Start Date of Work" and "End Date of Work" as mandatory.
      // To push users to input dates but to allow for empty dates.
      startDateOfWorkLabel: MANDATORY_WELL_SUBMISSION_STRINGS.START_DATE_OF_WORK,
      endDateOfWorkLabel: MANDATORY_WELL_SUBMISSION_STRINGS.END_DATE_OF_WORK,
      wellIdentificationPlateNumberLabel: WELL_SUBMISSION_STRINGS.WELL_IDENTIFICATION_PLATE_NUMBER,
      wellIdentificationPlateAttachedLabel: WELL_SUBMISSION_STRINGS.WELL_IDENTIFICATION_PLATE_ATTACHED,
      totalDepthDrilledLabel: WELL_SUBMISSION_STRINGS.TOTAL_DEPTH_DRILLED,
      finishedWellDepthLabel: WELL_SUBMISSION_STRINGS.FINISHED_WELL_DEPTH,
      drillingMethodsLabel: WELL_SUBMISSION_STRINGS.DRILLING_METHODS
    }
  },
  watch: {
    // we need this empty watch section for the code in beforeCreate
    '$route' (to, from) {
      if (to.hash !== from.hash && !this.formIsFlat) {
        const routeFromUrlHash = to.hash.substr(1)
        if (routeFromUrlHash) {
          const stepNum = this.stepCodes.indexOf(routeFromUrlHash)
          if (stepNum >= 0) {
            this.step = Math.min(stepNum + 1, this.maxSteps)
          }
        } else {
          this.step = 1
        }
      }
    },
    formIsFlat () {
      this.formFlatnessChanged()
    }
  },
  computed: {
    wellTagNumber () {
      return this.form.well
    },
    formStep () {
      // the numbered step that the user is on
      // this value is bound by the length of the list of steps for the
      // current type of submission
      return (this.step % (this.maxSteps + 1))
    },
    stepCodes () {
      return this.formSteps[this.activityType]
    },
    maxSteps () {
      return this.stepCodes.length
    },
    currentStep () {
      // the string name of the step corresponding to formStep
      // this will determine which step is currently displayed
      return this.stepCodes[this.formStep - 1]
    },
    isLoadFormDisabled () {
      // During unit tests, the localStorage object might not exist, so we have to check it's existence.
      return !window.localStorage || (window.localStorage.getItem('savedFormData') === null && !this.hasHadSaveFormSuccess)
    },
    editSaveDisabled () {
      return this.formSubmitLoading || !this.formValueChanged
    },
    isUnpublished () {
      return !this.isPublished
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
      if (window.localStorage) {
        window.localStorage.setItem('savedFormData', data)
      }
      setTimeout(() => { this.saveFormSuccess = true }, 10)
      setTimeout(() => { this.saveFormSuccess = false; this.hasHadSaveFormSuccess = true }, 1000)
    },
    loadForm () {
      this.saveStatusReset()
      const storedData = window.localStorage ? localStorage.getItem('savedFormData') : null
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
    },
    setFormValueChanged () {
      this.formValueChanged = true
    },
    fetchFiles () {
      this.$emit('fetchFiles')
    },
    anchorLinkHandler (step) {
      smoothScroll(this.$el.querySelector(`#${step}`))
      this.$router.replace({ hash: `#${step}` })
    },
    gotoPrevStep () {
      this.step--
      this.changeRouteHash(this.step)
    },
    gotoNextStep () {
      this.step++
      this.changeRouteHash(this.step)
    },
    formFlatnessChanged () {
      this.changeRouteHash(this.step)
    },
    changeRouteHash (step) {
      // Only set the route hash on a multi-step form
      const hash = this.formIsFlat ? '' : `#${this.stepCodes[step - 1]}`
      this.$router.push({ hash })
    },
    editWater (coords) {
      this.$emit('editWater', coords)
    },
    checkNewWellConstructionDates (dateString, dateInputType) {
      const newWellConstructionDate = NEW_WELL_CONSTRUCTION_VALIDATION_DATE

      if (dateString === '' && dateInputType === DATE_INPUT_TYPE.START_DATE) {
        if (this.workEndDate > newWellConstructionDate) {
          return true
        }
      }
      if (dateString === '' && dateInputType === DATE_INPUT_TYPE.END_DATE) {
        if (this.workStartDate > newWellConstructionDate) {
          return true
        }
      }
      if (dateString < newWellConstructionDate && ((this.workStartDate < newWellConstructionDate) && this.workEndDate < newWellConstructionDate)) {
        return false
      }
      return true
    },
    handleNewWellConstruction (isNewWellConstruction) {
      if (isNewWellConstruction === undefined) return
      if (isNewWellConstruction === false) {
        this.wellIdentificationPlateNumberLabel = WELL_SUBMISSION_STRINGS.WELL_IDENTIFICATION_PLATE_NUMBER
        this.wellIdentificationPlateAttachedLabel = WELL_SUBMISSION_STRINGS.WELL_IDENTIFICATION_PLATE_ATTACHED
        this.totalDepthDrilledLabel = WELL_SUBMISSION_STRINGS.TOTAL_DEPTH_DRILLED
        this.finishedWellDepthLabel = WELL_SUBMISSION_STRINGS.FINISHED_WELL_DEPTH
        this.drillingMethodsLabel = WELL_SUBMISSION_STRINGS.DRILLING_METHODS
        return
      }
      this.wellIdentificationPlateNumberLabel = MANDATORY_WELL_SUBMISSION_STRINGS.WELL_IDENTIFICATION_PLATE_NUMBER
      this.wellIdentificationPlateAttachedLabel = MANDATORY_WELL_SUBMISSION_STRINGS.WELL_IDENTIFICATION_PLATE_ATTACHED
      this.totalDepthDrilledLabel = MANDATORY_WELL_SUBMISSION_STRINGS.TOTAL_DEPTH_DRILLED
      this.finishedWellDepthLabel = MANDATORY_WELL_SUBMISSION_STRINGS.FINISHED_WELL_DEPTH
      this.drillingMethodsLabel = MANDATORY_WELL_SUBMISSION_STRINGS.DRILLING_METHODS
    },
    handleDateInput (event, dateInputType) {
      if (dateInputType === DATE_INPUT_TYPE.START_DATE) {
        this.workStartDate = event
      }

      if (dateInputType === DATE_INPUT_TYPE.END_DATE) {
        this.workEndDate = event
      }

      const dateString = event
      const isNewWellConstruction = this.checkNewWellConstructionDates(dateString, dateInputType)
      this.handleNewWellConstruction(isNewWellConstruction)
    }
  },
  created () {
    // When the form is saved, reset the formValueChanged variable.
    this.$parent.$on('formSaved', () => { this.formValueChanged = false })
    if (this.$route.hash) {
      this.step = 1
      this.changeRouteHash(this.step)
    }
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
            if (this.trackValueChanges && !this.loading && !this.formSubmitLoading) {
              if (this.formChanges()) {
                this.formValueChanged = true
                this.form.meta.valueChanged[key] = true
              } else {
                this.formValueChanged = false
                this.form.meta.valueChanged = {}
              }
            }
          },
          deep: true
        }
      })
    }
  }
}
</script>

<style lang="css">

</style>
