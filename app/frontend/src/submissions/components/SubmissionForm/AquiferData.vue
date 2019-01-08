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
          <a href="#top" v-if="isStaffEdit">Back to top</a>
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
            type="text"
            v-model="aquiferVulnerabilityIndexInput"
            :errors="errors['aquifer_vulnerability_index']"
            :loaded="fieldsLoaded['aquifer_vulnerability_index']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="storativityInput"
            label="Storativity"
            type="text"
            v-model="storativityInput"
            :errors="errors['storativity']"
            :loaded="fieldsLoaded['storativity']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="transmissivityInput"
            label="Transmissivity"
            type="text"
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
            type="text"
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
            type="text"
            v-model="testingDurationInput"
            :errors="errors['testing_duration']"
            :loaded="fieldsLoaded['testing_duration']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="4">
        <form-input
            id="analyticSolution"
            label="Analytic solution"
            type="text"
            v-model="analyticSolutionInput"
            :errors="errors['analytic_solution_type']"
            :loaded="fieldsLoaded['analytic_solution_type']"
        ></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4">
        <form-input
            id="boundaryEffectInput"
            label="Boundary effect"
            type="text"
            v-model="boundaryEffectInput"
            :errors="errors['boundary_effect']"
            :loaded="fieldsLoaded['boundary_effect']"
        ></form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import debounce from 'lodash.debounce'
import ApiService from '@/common/services/ApiService.js'
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'

export default {
  mixins: [inputBindingsMixin, inputFormatMixin],
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
    boundaryEffectInput: 'boundaryEffect'
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
      ApiService.query(`aquifers/names/?search=${escape(search)}`).then((response) => {
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
