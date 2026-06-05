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
    <form-subsection title="Well Class" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
      <responsive-grid v-if="isStaffEdit" :cols="12" :md="[3, 4]" :xl="[2, undefined]">
        <form-input
          id="wellTagNumberStaff"
          label="Well Tag Number"
          type="text"
          :value="$route.params.id"
          disabled/>
        <form-input
          select
          v-model="wellStatusCodeInput"
          :options="codes?.well_status_codes"
          value-field="well_status_code"
          text-field="description"
          label="Well Status"
          placeholder="Select status"
          :errors="errors['well_status']"
          :loaded="fieldsLoaded['well_status']"
          id="wellStatusCodeInput"/>
      </responsive-grid>
      <responsive-grid :cols="12" :md="4">
        <div class="flex flex-col form-group" aria-describedby="wellClassInvalidFeedback">
          <label for="wellClass">Class of Well *</label>
          <Select
            id="wellClass"
            v-model="wellClassInput"
            :options="codes?.well_classes"
            optionValue="well_class_code"
            optionLabel="description"
            :invalid="errors['well_class'] ? true : false"
            placeholder="Select class"/>
          <div id="wellClassInvalidFeedback">
            <div v-for="(error, index) in errors['well_class']" class="mt-1 text-sm text-red-600" :key="`wellClass error ${index}`">
              {{ error }}
            </div>
          </div>
        </div>
        <div class="flex flex-col form-group" aria-describedby="wellSubclassInvalidFeedback">
          <label for="wellSubclass">Well Subclass</label>
          <Select
            id="wellSubclass"
            v-model="wellSubclassInput"
            :options="subclasses"
            optionValue="well_subclass_guid"
            optionLabel="description"
            :disabled="wellSubclassDisabled"
            :invalid="errors['well_subclass'] ? true : false"
            placeholder="Select subclass"/>
          <div id="wellSubclassInvalidFeedback">
            <div v-for="(error, index) in errors['well_subclass']" class="mt-1 text-sm text-red-600" :key="`wellSubclass error ${index}`">
              {{ error }}
            </div>
          </div>
        </div>
        <form-input
          select
          v-model="intendedWaterUseInput"
          :options="intendedWaterUseOptions"
          value-field="intended_water_use_code"
          text-field="description"
          label="Intended Water Use *"
          placeholder="Select intended use"
          :errors="errors['intended_water_use']"
          :loaded="fieldsLoaded['intended_water_use']"
          :disabled="intendedWaterUseDisabled"
          id="intendedWaterUse"/>
      </responsive-grid>
      <div class="grid grid-cols-12">
        <div class="col-span-12 md:col-span-4" v-if="!isStaffEdit && wellActivityType !== 'CON'">
          <div class="flex flex-col form-group">
            <label for="wellTagNumberSelect">Well Tag Number (if known)</label>
            <v-select
              v-model="wellTagNumberInput"
              :disabled="wells === null"
              id="wellTagNumberSelect"
              :filterable="false"
              label="well_tag_number"
              :options="wellTagOptions"
              @search="onWellTagSearch"
              ref="wellTagNumber"
              @search:blur="handleSearchBlur">
              <template v-slot:no-options>
                  Search by well tag number or owner name
              </template>
              <template v-slot:cell(option)="option">
                <div>
                  {{ option.well_tag_number }} ({{ option.owner_full_name }})
                </div>
              </template>
              <template v-slot:cell(selected-option)="option">
                <div>
                  {{ option.well_tag_number }}
                </div>
              </template>
            </v-select>
            <small id="wellTagNumberSelectHint" class="form-text text-muted">
              *displays a maximum of {{MAX_RESULTS}} results
            </small>
          </div>
        </div>
        <div class="col-span-12 md:col-span-4">
          <form-input
            id="idPlateNumber"
            :label="wellIdentificationPlateNumberLabel"
            type="number"
            v-model="idPlateNumberInput"
            :errors="errors['identification_plate_number']"
            :loaded="fieldsLoaded['identification_plate_number']"/>
        </div>
        <div class="col-span-12 md:col-span-4">
          <form-input
            id="wellPlateAttached"
            :label="wellIdentificationPlateAttachedLabel"
            type="text"
            v-model="wellPlateAttachedInput"
            :errors="errors['well_identification_plate_attached']"
            :loaded="fieldsLoaded['well_identification_plate_attached']"/>
        </div>
        <div class="col-span-12 md:col-span-4" v-if="isStaffEdit">
          <form-input
            id="wellPlateAttachedBy"
            label="Identification Plate Attached By"
            type="text"
            v-model="idPlateAttachedByInput"
            :errors="errors['id_plate_attached_by']"
            :loaded="fieldsLoaded['id_plate_attached_by']"/>
        </div>
      </div>
      <responsive-grid v-if="isStaffEdit" :cols="12" :md="4">
        <form-input
          id="waterSupplySystem"
          label="Water Supply System Name"
          type="text"
          v-model="waterSupplySystemInput"
          :errors="errors['water_supply_system_name']"
          :loaded="fieldsLoaded['water_supply_system_name']"/>
        <form-input
          id="waterSupplyWell"
          label="Water Supply Well Name"
          type="text"
          v-model="waterSupplyWellInput"
          :errors="errors['water_supply_system_well_name']"
          :loaded="fieldsLoaded['water_supply_system_well_name']"/>
      </responsive-grid>
      <responsive-grid v-if="!isStaffEdit" :cols="12" :md="6">
        <form-input
          id="workStartDateInput"
          type="date"
          :label="startDateOfWorkLabel"
          placeholder="YYYY-MM-DD"
          v-model="workStartDateInput"
          :errors="errors.work_start_date"
          :loaded="fieldsLoaded['work_start_date']"
          @input="handleDateInput($event, 'workStartDate')"/>
        <form-input
          id="workEndDateInput"
          type="date"
          :label="endDateOfWorkLabel"
          placeholder="YYYY-MM-DD"
          v-model="workEndDateInput"
          :errors="errors.work_end_date"
          :loaded="fieldsLoaded['work_end_date']"
          @input="handleDateInput($event, 'workEndDate')"/>
      </responsive-grid>
    </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'
import { useCommonStore } from '@/stores/common'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  mixins: [inputBindingsMixin],
  props: {
    wellActivityType: String,
    units: String,
    wellTagNumber: null,
    wellStatusCode: String,
    workStartDate: String,
    workEndDate: String,
    personResponsible: Object,
    drillerName: String,
    idPlateNumber: null,
    wellPlateAttached: String,
    idPlateAttachedBy: String,
    wellClass: String,
    intendedWaterUse: String,
    wellSubclass: String,
    drillerSameAsPersonResponsible: Boolean,
    waterSupplySystem: String,
    waterSupplyWell: String,
    handleDateInput: Function,
    startDateOfWorkLabel: String,
    endDateOfWorkLabel: String,
    wellIdentificationPlateNumberLabel: String,
    wellIdentificationPlateAttachedLabel: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    id: {
      type: String,
      isInput: false
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  components: {
    FormSubsection,
    ResponsiveGrid
  },
  data () {
    return {
      submissionStore: null,
      wellTagOptions: [],
      MAX_RESULTS: 50
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
  },
  computed: {
    subclasses () {
      if (this.codes && this.codes.well_classes && this.wellClass) {
        return this.codes.well_classes.find(x => x.well_class_code === this.wellClass).wellsubclasscode_set
      } else {
        return []
      }
    },
    intendedWaterUseDisabled () {
      // Disable intended water use dropdown whenever the well class is not Water Supply. There is
      // an exception to this rule for wells that do not have well class set to Water Supply and
      // have a intended water use code set to something other then NA. Then the dropdown is enabled
      // so the user can pick the NA option. If they pick anything other then NA then the validation
      // rules in SubmissionHome.isFormValid() will notify the user that they _have_ to pick NA or
      // change the well class.
      return this.wellClass !== 'WATR_SPPLY' && this.intendedWaterUseInput === 'NA'
    },
    intendedWaterUseOptions () {
      if (this.wellClass === 'WATR_SPPLY' && this.codes.intended_water_uses) {
        // Do not allow user to pick "Not Applicable" when well_class_code is WATR_SPPLY
        return this.codes.intended_water_uses.filter((code) => {
          return code.intended_water_use_code !== 'NA'
        })
      }
      return this.codes.intended_water_uses
    },
    wellSubclassDisabled () {
      // WATER-1589, we disable the subclass dropdown for well classes of WATR_SPPLY and CLS_LP_GEO
      return this.subclasses && (this.wellClass === 'WATR_SPPLY' || this.wellClass === 'CLS_LP_GEO')
    },
    commonStore () { return useCommonStore() },
    submissionStore () { return useSubmissionStore() },
    codes () {
      return this.submissionStore.codes
    }
  },
  methods: {
    match (item, search) {
      // On some browsers indexOf is faster than contains and vice versa. The trends seems to be that indexOf is faster
      return (item.owner_full_name != null && item.owner_full_name.toUpperCase().indexOf(search) !== -1) || String(item.well_tag_number).indexOf(search) !== -1
    },
    onWellTagSearch (search, loading) {
      // Only do search if something has been typed.
      this.wellTagOptions = []
      if (search && search.length >= 1 && this.submissionStore.wells) {
        // Save time, by converting to uppercase for search only once.
        search = search.toUpperCase()
        // We iterate manually instead of using .filter in order that we can limit the number
        // of search results, and run faster.
        for (let i = 0; i < this.submissionStore.wells.length && this.wellTagOptions.length < this.MAX_RESULTS; ++i) {
          if (this.match(this.submissionStore.wells[i], search)) {
            this.wellTagOptions.push(this.submissionStore.wells[i])
          }
        }
      }
    },
    handleSearchBlur () {
      if (this.wellTagOptions && this.$refs.wellTagNumber.typeAheadPointer < this.wellTagOptions.length) {
        const target = this.wellTagOptions[this.$refs.wellTagNumber.typeAheadPointer]
        if (target) {
          this.wellTagNumberInput = target.well_tag_number
        }
      }
    }
  },
  watch: {
    wellTagNumber (val) {
      // reset list of people when user finished selecting a person
      this.wellTagOptions = []
    },
    wellClass (val, prev) {
      // WATER-1589, now that watr_spply and cls lp geo only have retired subclass codes we always default to NA
      if (val !== null && (val === 'WATR_SPPLY' || val === 'CLS_LP_GEO')) {
        this.wellSubclassInput = this.subclasses.find(c => c.well_subclass_code === 'NA').well_subclass_guid
      } else {
        // reset wellSubClass when wellClass changes
        this.wellSubclassInput = null
      }

      if (val !== null && val !== 'WATR_SPPLY') {
        this.intendedWaterUseInput = 'NA'
      } else if (this.intendedWaterUse === 'NA') {
        // When the well class is changed to WATR_SPPLY then set the intendedWaterUseInput to `null`
        // only if the current value of intended water use code is 'NA'
        this.intendedWaterUseInput = null
      }
    }
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
.v-select i.open-indicator {
  width: 0px;
  visibility: hidden;
}
</style>
