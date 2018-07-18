<template>
    <fieldset>
      <legend>Type of Work and Well Class</legend>
      <b-row>
        <b-col cols="12" md="6">
          <b-form-group label="Type of Work*">
            <b-form-radio-group v-model="typeOfWorkInput"
                                stacked
                                name="submissionTypeRadio">
              <b-form-radio value="CON">Construction</b-form-radio>
              <b-form-radio value="ALT">Alteration</b-form-radio>
              <b-form-radio value="DEC">Decommissioning</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="6">
          <b-form-group label="Measurement units for data entry">
            <b-form-radio-group v-model="unitsInput"
                                stacked
                                name="measurementUnitsRadio">
              <b-form-radio value="metric">Metric</b-form-radio>
              <b-form-radio value="imperial">Imperial</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <b-form-group label="Person Responsible for Drilling*">
            <v-select
                :filterable="false"
                :options="personOptions"
                v-model="personResponsibleInput"
                @search="onPersonSearch">
              <template slot="no-options">
                  Type to search Well Driller and Pump Installer Registry...
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
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input id="workStartDateInput" type="date" label="Start Date of Work*" v-model="workStartDateInput" :errors="errors.work_start_date">
          </form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input id="workEndDateInput" type="date" label="End Date of Work*" v-model="workEndDateInput" :errors="errors.work_end_date">
          </form-input>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import debounce from 'lodash.debounce'
import inputBindingsMixin from './inputBindingsMixin.js'
import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'Step01Type',
  mixins: [inputBindingsMixin],
  props: {
    units: String,
    workStartDate: String,
    workEndDate: String,
    typeOfWork: String,
    personResponsible: Object,
    errors: {
      type: Object,
      default: () => ({})
    }
  },
  fields: {
    unitsInput: 'units',
    workStartDateInput: 'workStartDate',
    workEndDateInput: 'workEndDate',
    typeOfWorkInput: 'typeOfWork',
    personResponsibleInput: 'personResponsible'
  },
  data () {
    return {
      personOptions: []
    }
  },
  computed: {},
  methods: {
    onPersonSearch (search, loading) {
      loading(true)
      this.search(loading, search, this)
    },
    search: debounce((loading, search, vm) => {
      ApiService.query(`drillers/names/?search=${escape(search)}`).then((response) => {
        vm.personOptions = response.data
        loading(false)
      })
    }, 500)
  },
  watch: {

  }
}
</script>

<style>

</style>
