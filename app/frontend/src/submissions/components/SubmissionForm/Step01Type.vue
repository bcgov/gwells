<template>
    <fieldset>
      <legend>Type of Work and Well Class</legend>
      <b-row>
        <b-col cols="12" md="6">
          <b-form-group label="Type of Work*">
            <b-form-radio-group v-model="formData.type_of_work"
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
            <b-form-radio-group v-model="units"
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
          <b-form-group label="Start Date of Work*">
            <b-form-input type="date" v-model="formData.work_start_date"/>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="6">
          <b-form-group label="End Date of Work*">
            <b-form-input type="date" v-model="formData.work_end_date"/>
          </b-form-group>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import _ from 'lodash'
import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'Step01Type',
  data () {
    return {
      units: 'metric',
      personOptions: [],
      // form data keys follow naming convention from API for consistency with request/response field names
      formData: {
        type_of_work: 'CON',
        work_start_date: '',
        work_end_date: ''
      }
    }
  },
  methods: {
    onPersonSearch (search, loading) {
      loading(true)
      this.search(loading, search, this)
    },
    search: _.debounce((loading, search, vm) => {
      ApiService.query(`drillers/names/?search=${escape(search)}`).then((response) => {
        vm.personOptions = response.data
        loading(false)
      })
    }, 500)
  }
}
</script>

<style>

</style>
