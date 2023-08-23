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
  <fieldset>
    <b-row>
      <b-col cols="12" lg="6">
        <legend :id="id">Pumping Test Information and Aquifer Parameters</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <div class="table-responsive" id="aquiferParametersTable">
      <table class="table" aria-describedby="aquiferParameters">
        <thead>
        </thead>
        <tbody>
          <template v-for="(aquiferParameter, index) in aquiferParametersData">
            <div class="bordered-table">
              <tr>
                <th class="font-weight-normal top-row-no-border" scope="col">Start Date of Test</th>
                <th class="font-weight-normal top-row-no-border" scope="col">Test Description</th>
                <th class="font-weight-normal top-row-no-border" scope="col">Test Duration (min)</th>
                <th class="font-weight-normal top-row-no-border" scope="col">Boundary Effect</th>
              </tr>
              <tr>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_startDatePumpingTest_' + index"
                    type="date"
                    placeholder="YYYY-MM-DD"
                    v-model="aquiferParameter.start_date_pumping_test"
                    :errors="getAquiferParametersError(index).start_date_pumping_test"
                    :loaded="getFieldsLoaded(index).start_date_pumping_test"/>
                </td>
                <td>
                  <form-input
                    id="testDescription"
                    group-class="mt-1 mb-0"
                    select
                    v-model="aquiferParameter.pumping_test_description"
                    :options="codes.pumping_test_description_codes"
                    placeholder="Select Testing Description"
                    text-field="description"
                    value-field="pumping_test_description_code"
                    :errors="errors['pumping_test_description']"
                    :loaded="fieldsLoaded['pumping_test_description']"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_testDuration_' + index"
                    type="number"
                    v-model="aquiferParameter.test_duration"
                    :errors="getAquiferParametersError(index).test_duration"
                    :loaded="getFieldsLoaded(index).test_duration"
                    :min="1"/>
                </td>
                <td>
                  <form-input
                    id="boundaryEffect"
                    group-class="mt-1 mb-0"
                    select
                    v-model="aquiferParameter.boundary_effect"
                    :options="codes.boundary_effect_codes"
                    placeholder="Select Boundary effect"
                    text-field="description"
                    value-field="boundary_effect_code"
                    :errors="errors['boundary_effect']"
                    :loaded="fieldsLoaded['boundary_effect']"/>
                </td>
              </tr>
              <tr>
                <th class="font-weight-normal" scope="col">Analysis Method</th>
                <th class="font-weight-normal" scope="col">Transmissivity (m²/day)</th>
                <th class="font-weight-normal" scope="col">Conductivity (m/day)</th>
                <th class="font-weight-normal" scope="col">Storativity</th>
                <th class="font-weight-normal" scope="col">Specific Yield</th>
                <th class="font-weight-normal" scope="col">Specific Capacity (L/s/m)</th>
              </tr>
              <tr>
                <td>
                  <form-input
                    id="analysisMethod"
                    group-class="mt-1 mb-0"
                    select
                    v-model="aquiferParameter.analysis_method"
                    :options="codes.analysis_method_codes"
                    placeholder="Select Analysis Method"
                    text-field="description"
                    value-field="analysis_method_code"
                    :errors="errors['analysis_method_code']"
                    :loaded="fieldsLoaded['analysis_method_code']"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_transmissivity_' + index"
                    type="number"
                    :value="removeTrailingZeros(aquiferParameter.transmissivity)"
                    @input="aquiferParameter.transmissivity = $event"
                    :errors="getAquiferParametersError(index).transmissivity"
                    :loaded="getFieldsLoaded(index).transmissivity"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_hydraulicConductivity_' + index"
                    type="number"
                    :value="removeTrailingZeros(aquiferParameter.hydraulic_conductivity)"
                    @input="aquiferParameter.hydraulic_conductivity = $event"
                    :errors="getAquiferParametersError(index).hydraulic_conductivity"
                    :loaded="getFieldsLoaded(index).hydraulic_conductivity"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_storativity_' + index"
                    type="number"
                    :value="removeTrailingZeros(aquiferParameter.storativity)"
                    @input="aquiferParameter.storativity = $event"
                    :errors="getAquiferParametersError(index).storativity"
                    :loaded="getFieldsLoaded(index).storativity"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_specificYield_' + index"
                    type="number"
                    v-model="aquiferParameter.specific_yield"
                    :errors="getAquiferParametersError(index).specific_yield"
                    :loaded="getFieldsLoaded(index).specific_yield"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_specificCapacity_' + index"
                    type="number"
                    v-model="aquiferParameter.specific_capacity"
                    :errors="getAquiferParametersError(index).specific_capacity"
                    :loaded="getFieldsLoaded(index).specific_capacity"/>
                </td>
              </tr>
              <tr>
                <th class="font-weight-normal" scope="col">Comments</th>
                <th scope="col"></th>
              </tr>
              <tr>
                <td colspan="6">
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="'aquiferParameter_comments_' + index"
                    type="text"
                    v-model="aquiferParameter.comments"
                    :errors="getAquiferParametersError(index).comments"
                    :loaded="getFieldsLoaded(index).comments"/>
                </td>
              </tr>
              <tr>
                <td class="pt-2 pb-3">
                  <b-btn size="sm" variant="primary" :id="`removeAquiferParameterRowBtn${index}`" @click="removeRowIfOk(aquiferParameter)" class="mt-2"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
                </td>
              </tr>
            </div>
          </template>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" id="addAquiferParameterRowBtn" variant="primary" @click="addRow"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
    <b-modal
        v-model="confirmRemoveModal"
        centered
        title="Confirm remove"
        @shown="focusRemoveModal">
      Are you sure you want to remove this row?
      <div slot="modal-footer">
        <b-btn variant="secondary" @click="confirmRemoveModal=false;rowIndexToRemove=null" ref="cancelRemoveBtn">
          Cancel
        </b-btn>
        <b-btn variant="danger" @click="confirmRemoveModal=false;removeRowByIndex(rowIndexToRemove)">
          Remove
        </b-btn>
      </div>
    </b-modal>
  </fieldset>
</template>

<script>
import Vue from 'vue'
import { mapGetters } from 'vuex'
import { omit } from 'lodash'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'

import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  name: 'AquiferParameters',
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    aquiferParameters: Array,
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
  data () {
    return {
      confirmRemoveModal: false,
      rowIndexToRemove: null,
      aquiferParametersData: []
    }
  },
  methods: {
    addRow () {
      this.aquiferParametersData.push(this.emptyObject())
    },
    emptyObject () {
      return {
        start_date_pumping_test: null,
        pumping_test_description: null,
        test_duration: null,
        boundary_effect: null,
        storativity: null,
        transmissivity: null,
        hydraulic_conductivity: null,
        specific_yield: null,
        specific_capacity: null,
        analysis_method: null,
        comments: null
      }
    },
    removeRowByIndex (index) {
      this.aquiferParametersData.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (instance) {
      const index = this.aquiferParametersData.findIndex(item => item === instance)
      if (this.rowHasValues(this.aquiferParametersData[index])) {
        this.rowIndexToRemove = index
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(index)
      }
    },
    toggleAquiferParametersLengthRequired (index) {
      const instance = this.aquiferParametersData[index]
      instance.length_required = !instance.length_required
      Vue.set(this.aquiferParametersData, index, instance)
    },
    getAquiferParametersError (index) {
      if (this.errors && 'aquifer_parameters_set' in this.errors && index in this.errors['aquifer_parameters_set']) {
        return this.errors['aquifer_parameters_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'aquifer_parameters_set' in this.fieldsLoaded && index in this.fieldsLoaded['aquifer_parameters_set']) {
        return this.fieldsLoaded['aquifer_parameters_set'][index]
      }
      return {}
    },
    rowHasValues (row) {
      let keys = Object.keys(row)
      if (keys.length === 0) return false
      // Check that all fields are not empty.
      return !this.aquiferParametersIsEmpty(row)
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    aquiferParametersIsEmpty (aquiferParameters) {
      const fieldsToTest = omit(aquiferParameters, 'length_required')
      return Object.values(fieldsToTest).every((x) => !x)
    },
    removeTrailingZeros (value) {
      return parseFloat(value).toString()
    }
  },
  computed: {
    ...mapGetters(['codes']),
    computedAquiferParameters () {
      return [...this.aquiferParametersData]
    }
  },
  watch: {
    computedAquiferParameters: {
      deep: true,
      handler: function (n, o) {
        const aquiferParameters = this.aquiferParametersData.filter((d) => !this.aquiferParametersIsEmpty(d))
        this.$emit('update:aquiferParameters', aquiferParameters)
      }
    }
  },
  created () {
    // When component created, add an initial row of aquiferParameters.
    if (!this.aquiferParameters.length) {
      for (let i = 0; i < 1; i++) {
        this.addRow()
      }
    } else {
      this.aquiferParameters.forEach((parameters) => {
        this.aquiferParametersData.push({ ...parameters })
      })
      this.addRow()
    }
  }
}
</script>

<style>
  .input-width-sm {
    max-width: 50px;
  }
  .input-width-md {
    max-width: 100px;
  }
  .input-width-lg {
    max-width: 200px;
  }
  .bordered-table {
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-top: 4px;
  }
  .top-row-no-border {
    border-top: none !important;
  }
  /* For Firefox */
  input[type='number'] {
    -moz-appearance: textfield;
  }

  /* For Chrome, Safari, Edge, Opera */
  input[type='number']::-webkit-inner-spin-button,
  input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
</style>
