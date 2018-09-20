<template>
    <fieldset>
      <legend>Type of Work and Well Class</legend>
      <b-row>
        <b-col cols="12" md="6">
          <b-form-group label="Type of Work *">
            <b-form-radio-group v-model="wellActivityTypeInput"
                                stacked
                                name="submissionTypeRadio">
              <b-form-radio value="CON">Construction</b-form-radio>
              <b-form-radio value="ALT">Alteration</b-form-radio>
              <b-form-radio value="DEC">Decommissioning</b-form-radio>
              <b-form-radio value="STAFF_EDIT" v-if="userRoles.wells.edit">Staff edit</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="4">
          <b-form-group
              id="wellClass"
              label="Class of Well"
              aria-describedby="wellClassInvalidFeedback">
            <b-form-select
                v-model="wellClassInput"
                :options="codes.well_classes"
                value-field="well_class_code"
                text-field="description"
                :state="errors['well_class'] ? false : null">
              <template slot="first">
                <option value="" disabled>Select class</option>
              </template>
            </b-form-select>
            <b-form-invalid-feedback id="wellClassInvalidFeedback">
              <div v-for="(error, index) in errors['well_class']" :key="`wellClass error ${index}`">
                {{ error }}
              </div>
            </b-form-invalid-feedback>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="4">
          <b-form-group
              id="wellSubclass"
              label="Well Subclass"
              aria-describedby="wellSubclassInvalidFeedback">
            <b-form-select
                v-model="wellSubclassInput"
                :options="subclasses"
                value-field="well_subclass_code"
                text-field="description"
                :disabled="!subclasses.length"
                :state="errors['well_subclass'] ? false : null">
              <template slot="first">
                <option value="" disabled>Select subclass</option>
              </template>
            </b-form-select>
            <b-form-invalid-feedback id="wellSubclassInvalidFeedback">
              <div v-for="(error, index) in errors['well_subclass']" :key="`wellSubclass error ${index}`">
                {{ error }}
              </div>
            </b-form-invalid-feedback>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
            select
            v-model="intendedWaterUseInput"
            :options="codes.intended_water_uses"
            value-field="intended_water_use_code"
            text-field="description"
            label="Intended Water Use"
            placeholder="Select intended use"
            :errors="errors['intended_water_use']"
            :loaded="fieldsLoaded['intended_water_use']"
            id="intendedWaterUse"></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="4">
          <b-form-group label="Well Tag Number (if known)">
            <v-select
              v-model="wellTagNumberInput"
              id="wellTagNumberSelect"
              :filterable="false"
              :options="wellTagOptions"
              @search="onWellTagSearch">
              <template slot="no-options">
                  Search by well tag number or owner name
              </template>
              <template slot="option" slot-scope="option">
                <div>
                  {{ option.well_tag_number }} ({{ option.owner_full_name }})
                </div>
              </template>
              <template slot="selected-option" slot-scope="option">
                <div>
                  {{ option.well_tag_number }}
                </div>
              </template>
            </v-select>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
              id="idPlateNumber"
              label="Well Identification Plate Number"
              type="text"
              v-model="idPlateNumberInput"
              :errors="errors['identification_plate_number']"
              :loaded="fieldsLoaded['identification_plate_number']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="4">
          <form-input
              id="wellPlateAttached"
              label="Where Identification Plate Attached"
              type="text"
              v-model="wellPlateAttachedInput"
              :errors="errors['well_identification_plate_attached']"
              :loaded="fieldsLoaded['well_identification_plate_attached']"
          ></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input
              id="workStartDateInput"
              type="date"
              label="Start Date of Work *"
              hint="Enter date as YYYY/MM/DD"
              v-model="workStartDateInput"
              :errors="errors.work_start_date"
              :loaded="fieldsLoaded['work_start_date']">
          </form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input
              id="workEndDateInput"
              type="date"
              label="End Date of Work *"
              hint="Enter date as YYYY/MM/DD"
              v-model="workEndDateInput"
              :errors="errors.work_end_date"
              :loaded="fieldsLoaded['work_end_date']">
          </form-input>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import debounce from 'lodash.debounce'
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ApiService from '@/common/services/ApiService.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    units: String,
    wellTagNumber: Object,
    workStartDate: String,
    workEndDate: String,
    wellActivityType: String,
    personResponsible: Object,
    drillerName: String,
    idPlateNumber: String,
    wellPlateAttached: String,
    wellClass: String,
    intendedWaterUse: String,
    wellSubclass: String,
    drillerSameAsPersonResponsible: Boolean,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      wellTagOptions: []
    }
  },
  computed: {
    subclasses () {
      if (this.codes && this.codes.well_classes && this.wellClass) {
        return this.codes.well_classes.find(x => x.well_class_code === this.wellClass).wellsubclasscode_set
      } else {
        return []
      }
    },
    ...mapGetters(['codes', 'userRoles'])
  },
  methods: {
    wellTagSearch: debounce((loading, search, vm) => {
      ApiService.query(`wells/tags/?search=${escape(search)}`).then((response) => {
        vm.wellTagOptions = response.data
        loading(false)
      })
    }, 500),
    onWellTagSearch (search, loading) {
      loading(true)
      this.wellTagSearch(loading, search, this)
    }
  },
  watch: {
    wellTagNumber (val) {
      // reset list of people when user finished selecting a person
      this.wellTagOptions = []
    },
    wellClass (val, prev) {
      if (prev !== '') {
        this.wellSubclassInput = ''
      }
    }
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
</style>
