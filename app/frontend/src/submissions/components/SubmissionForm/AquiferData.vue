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
        <legend :id="id">Well Testing and Aquifer Details</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12" md="6" xl="3">
        <b-form-group label="Associated aquifer">
          <v-select
            v-model="aquiferInput"
            id="aquiferSelect"
            :filterable="false"
            :options="aquiferList"
            :reduce="aquifer => aquifer.aquifer_id"
            label="description"
            index="aquifer_id"
            @search="onAquiferSearch">
            <template slot="no-options">
                Search for an aquifer by name or id number
            </template>
            <template slot="option" slot-scope="option">
              <div>
                {{ option.description }}
              </div>
            </template>
            <template slot="selected-option" slot-scope="option">
              <div>
                {{ option.description }}
              </div>
            </template>
          </v-select>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4">
        <form-input
            id="aquiferVulnerabilityIndexInput"
            label="AVI"
            hint="years"
            type="number"
            v-model="aquiferVulnerabilityIndexInput"
            :errors="errors['aquifer_vulnerability_index']"
            :loaded="fieldsLoaded['aquifer_vulnerability_index']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="storativityInput"
            label="Storativity"
            type="number"
            v-model="storativityInput"
            :errors="errors['storativity']"
            :loaded="fieldsLoaded['storativity']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="transmissivityInput"
            label="Transmissivity"
            hint="m²/s"
            type="number"
            v-model="transmissivityInput"
            :errors="errors['transmissivity']"
            :loaded="fieldsLoaded['transmissivity']"
        ></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4">
        <form-input
            id="hydraulicConductivityInput"
            label="Hydraulic Conductivity"
            hint="m/s"
            type="text"
            v-model="hydraulicConductivityInput"
            :errors="errors['hydraulic_conductivity']"
            :loaded="fieldsLoaded['hydraulic_conductivity']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="specificStorageInput"
            label="Specific storage"
            hint="1/m"
            type="text"
            v-model="specificStorageInput"
            :errors="errors['specific_storage']"
            :loaded="fieldsLoaded['specific_storage']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="specificYieldInput"
            label="Specific yield"
            type="number"
            v-model="specificYieldInput"
            :errors="errors['specific_yield']"
            :loaded="fieldsLoaded['specific_yield']"
        ></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4">
        <form-input
            id="testingMethodInput"
            label="Testing method"
            type="text"
            v-model="testingMethodInput"
            :errors="errors['test_method']"
            :loaded="fieldsLoaded['test_method']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="testingDuration"
            label="Testing duration"
            hint="hours"
            type="number"
            v-model="testingDurationInput"
            :errors="errors['testing_duration']"
            :loaded="fieldsLoaded['testing_duration']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="analyticSolution"
            label="Analytic solution"
            type="number"
            v-model="analyticSolutionInput"
            :errors="errors['analytic_solution_type']"
            :loaded="fieldsLoaded['analytic_solution_type']"
        ></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4">
        <form-input
          label="Boundary effect"
          id="boundaryEffect"
          select
          v-model="boundaryEffectInput"
          :options="codes.boundary_effect_codes"
          placeholder="Select Boundary effect"
          text-field="description"
          value-field="boundary_effect_code"
          :errors="errors['boundary_effect']"
          :loaded="fieldsLoaded['boundary_effect']"/>
      </b-col>
      <b-col cols="12" md="4">
        <b-form-group
          id="aquiferLithology"
          label="Aquifer Lithology">
          <b-form-select
            v-model="aquiferLithologyInput"
            value-field="aquifer_lithology_code"
            :options="codes.aquifer_lithology_codes"
            :errors="errors['aquifer_lithology']"
            :loaded="fieldsLoaded['aquifer_lithology']"
            text-field="description">
            <template slot="first">
              <option :value="null" disabled>Select Lithology</option>
            </template>
          </b-form-select>
        </b-form-group>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { debounce } from 'lodash'
import { mapGetters } from 'vuex'

import ApiService from '@/common/services/ApiService.js'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'

import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  mixins: [inputBindingsMixin, inputFormatMixin],
  components: {
    BackToTopLink
  },
  props: {
    aquifer: null,
    aquiferVulnerabilityIndex: null,
    storativity: null,
    transmissivity: null,
    hydraulicConductivity: null,
    specificStorage: null,
    specificYield: null,
    testingMethod: null,
    testingDuration: null,
    analyticSolutionType: null,
    boundaryEffect: null,
    aquiferLithology: null,
    id: {
      type: String,
      isInput: false
    },
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
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
  fields: {
    aquiferInput: 'aquifer',
    aquiferVulnerabilityIndexInput: 'aquiferVulnerabilityIndex',
    storativityInput: 'storativity',
    transmissivityInput: 'transmissivity',
    hydraulicConductivityInput: 'hydraulicConductivity',
    specificStorageInput: 'specificStorage',
    specificYieldInput: 'specificYield',
    testingMethodInput: 'testingMethod',
    testingDurationInput: 'testingDuration',
    analyticSolutionInput: 'analyticSolutionType',
    boundaryEffectInput: 'boundaryEffect',
    aquiferLithologyInput: 'aquiferLithology'
  },
  data () {
    return {
      aquiferList: []
    }
  },
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    aquiferSearch: debounce((loading, search, vm) => {
      ApiService.query(`aquifers/names?search=${escape(search)}`).then((response) => {
        vm.aquiferList = response.data
        loading(false)
      }).catch(() => {
        loading(false)
      })
    }, 500),
    onAquiferSearch (search, loading) {
      loading(true)
      this.aquiferSearch(loading, search, this)
    }
  }
}
</script>

<style>

</style>
