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
            </b-form-radio-group>
          </b-form-group>
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
          <b-form-group
              label="Person Responsible for Drilling *"
              aria-describedby="personResponsibleInvalidFeedback"
              :state="false">
            <v-select
                :class="errors.driller_responsible?'border border-danger dropdown-error-border':''"
                id="personResponsibleSelect"
                :filterable="false"
                :options="personOptions"
                v-model="personResponsibleInput"
                @search="onPersonSearch">
              <template slot="no-options">
                  Type to search registry...
              </template>
              <template slot="option" slot-scope="option">
                <div>
                  {{ option.name }}
                  </div>
              </template>
              <template slot="selected-option" slot-scope="option">
                <div>
                  {{ option.name }}
                </div>
              </template>
            </v-select>
            <b-form-text id="personResponsibleInvalidFeedback" v-if="errors.driller_responsible">
              <div v-for="(error, index) in errors.driller_responsible" :key="`personResponsible error ${index}`" class="text-danger">
                {{ error }}
              </div>
            </b-form-text>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input
              id="consultantName"
              label="Consultant Name"
              type="text"
              v-model="consultantNameInput"
              :errors="errors['consultant_name']"
              :loaded="fieldsLoaded['consultant_name']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input
              id="consultantCompany"
              label="Consultant Company"
              type="text"
              v-model="consultantCompanyInput"
              :errors="errors['consultant_company']"
              :loaded="fieldsLoaded['consultant_company']"
          ></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input id="workStartDateInput" type="date" label="Start Date of Work *" v-model="workStartDateInput" :errors="errors.work_start_date" :loaded="fieldsLoaded['work_start_date']">
          </form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input id="workEndDateInput" type="date" label="End Date of Work *" v-model="workEndDateInput" :errors="errors.work_end_date" :loaded="fieldsLoaded['work_end_date']">
          </form-input>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import debounce from 'lodash.debounce'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'Step01Type',
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
    consultantName: String,
    consultantCompany: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    }
  },
  fields: {
    unitsInput: 'units',
    workStartDateInput: 'workStartDate',
    workEndDateInput: 'workEndDate',
    wellActivityTypeInput: 'wellActivityType',
    personResponsibleInput: 'personResponsible',
    wellTagNumberInput: 'wellTagNumber',
    drillerNameInput: 'drillerName',
    idPlateNumberInput: 'idPlateNumber',
    wellPlateAttachedInput: 'wellPlateAttached',
    consultantNameInput: 'consultantName',
    consultantCompanyInput: 'consultantCompany'
  },
  data () {
    return {
      personOptions: [],
      wellTagOptions: []
    }
  },
  computed: {},
  methods: {
    onPersonSearch (search, loading) {
      loading(true)
      this.drillerSearch(loading, search, this)
    },
    drillerSearch: debounce((loading, search, vm) => {
      ApiService.query(`drillers/names/?search=${escape(search)}`).then((response) => {
        vm.personOptions = response.data
        loading(false)
      })
    }, 500),
    onWellTagSearch (search, loading) {
      loading(true)
      this.wellTagSearch(loading, search, this)
    },
    wellTagSearch: debounce((loading, search, vm) => {
      ApiService.query(`wells/tags/?search=${escape(search)}`).then((response) => {
        vm.wellTagOptions = response.data
        loading(false)
      })
    }, 500)
  },
  watch: {
    personResponsibleInput (val) {
      // reset list of people when user finished selecting a person
      this.personOptions = []
    },
    wellTagNumberInput (val) {
      // reset list of people when user finished selecting a person
      this.wellTagOptions = []
    }
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
</style>
