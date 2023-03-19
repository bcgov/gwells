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
        <legend :id="id">Aquifer Parameters</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <div class="table-responsive" id="aquiferParametersTable">
      <table class="table table-sm">
        <thead>
          <tr>
            <th class="font-weight-normal">Storativity</th>
            <th class="font-weight-normal">Transmissivity</th>
            <th class="font-weight-normal">Hydraulic Conductivity</th>
            <th class="font-weight-normal">Specific Yield</th>
            <th class="font-weight-normal">Analytical Solution Type</th>
            <th class="font-weight-normal">Testing Method</th>
            <th class="font-weight-normal">Testing Duration</th>
            <th class="font-weight-normal">Well Testing comments</th>
            <th class="font-weight-normal">Date of Test</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(aquiferParameter, index) in aquiferParametersData" :key="aquiferParameter.id">
            <td class="input-width-small">
              <form-input
                group-class="mt-1 mb-0"
                :id="'aquiferParameter_storativity_' + index"
                type="number"
                v-model="aquiferParameter.storativity"
                :errors="getAquiferParametersError(index).storativity"
                :loaded="getFieldsLoaded(index).storativity"/>
            </td>
            <td class="input-width-small">
              <form-input
                group-class="mt-1 mb-0"
                :id="'aquiferParameter_transmissivity_' + index"
                type="number"
                v-model="aquiferParameter.transmissivity"
                :errors="getAquiferParametersError(index).transmissivity"
                :loaded="getFieldsLoaded(index).transmissivity"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'aquiferParameter_hydraulicConductivity_' + index"
                type="text"
                v-model="aquiferParameter.hydraulic_conductivity"
                :errors="getAquiferParametersError(index).hydraulic_conductivity"
                :loaded="getFieldsLoaded(index).hydraulic_conductivity"/>
            </td>
            <td class="input-width-small">
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
                :id="'aquiferParameter_analyticSolutionType_' + index"
                type="text"
                v-model="aquiferParameter.analytic_solution_type"
                :errors="getAquiferParametersError(index).analytic_solution_type"
                :loaded="getFieldsLoaded(index).analytic_solution_type"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'aquiferParameter_testingMethod_' + index"
                type="text"
                v-model="aquiferParameter.testing_method"
                :errors="getAquiferParametersError(index).testing_method"
                :loaded="getFieldsLoaded(index).testing_method"/>
            </td>
            <td class="input-width-small">
              <form-input
                group-class="mt-1 mb-0"
                :id="'aquiferParameter_testingDuration_' + index"
                type="number"
                v-model="aquiferParameter.testing_duration"
                :errors="getAquiferParametersError(index).testing_duration"
                :loaded="getFieldsLoaded(index).testing_duration"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'aquiferParameter_testingComments_' + index"
                type="text"
                v-model="aquiferParameter.testing_comments"
                :errors="getAquiferParametersError(index).testing_comments"
                :loaded="getFieldsLoaded(index).testing_comments"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'aquiferParameter_testingDate_' + index"
                type="date"
                placeholder="YYYY-MM-DD"
                v-model="aquiferParameter.testing_date"
                :errors="getAquiferParametersError(index).testing_date"
                :loaded="getFieldsLoaded(index).testing_date"/>
                <b-col cols="6" md="6">
      </b-col>
            </td>
            <td class="pt-1 py-0">
              <b-btn size="sm" variant="primary" :id="`removeAquiferParameterRowBtn${index}`" @click="removeRowIfOk(aquiferParameter)" class="mt-2 float-right"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
            </td>
          </tr>
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
        storativity: null,
        transmissivity: null,
        hydraulic_conductivity: null,
        specific_yield: null,
        analytic_solution_type: null,
        testing_method: null,
        testing_duration: null,
        testing_comments: null,
        testing_date: null
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
      for (let i = 0; i < 3; i++) {
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

</style>
