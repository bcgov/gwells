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
    <div class="grid grid-cols-12">
      <div class="col-span-12 lg:col-span-6">
        <legend :id="id">Aquifer Information</legend>
      </div>
      <div class="col-span-12 lg:col-span-6">
        <div class="float-right">
          <Button v-if="isStaffEdit" label="Save" class="ml-2" @click="$emit('save')" :disabled="saveDisabled"/>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-12">
      <div class="col-span-12 md:col-span-6 xl:col-span-3">
        <div class="flex flex-col gap-2">
          <label for="aquiferSelect">Associated Aquifer</label>
          <v-select
            v-model="aquiferInput"
            id="aquiferSelect"
            :filterable="false"
            :options="aquiferList"
            :reduce="aquifer => aquifer.aquifer_id"
            label="description"
            index="aquifer_id"
            @search="onAquiferSearch">
            <template v-slot:no-options>
                Search for an aquifer by name or id number
            </template>
            <template v-slot:cell(option)="option">
              <div>
                {{ option.description }}
              </div>
            </template>
            <template v-slot:cell(selected-option)="option">
              <div>
                {{ option.description }}
              </div>
            </template>
          </v-select>
        </div>
      </div>
      <div class="col-span-12 md:col-span-4">
        <b-form-group
          id="aquiferLithology"
          label="Aquifer Material">
          <b-form-select
            v-model="aquiferLithologyInput"
            value-field="aquifer_lithology_code"
            :options="codes?.aquifer_lithology_codes"
            :errors="errors['aquifer_lithology']"
            :loaded="fieldsLoaded['aquifer_lithology']"
            text-field="description">
            <template v-slot:first>
              <option :value="null" disabled>Select Lithology</option>
            </template>
          </b-form-select>
        </b-form-group>
      </div>
    </div>
  </fieldset>
</template>

<script>
import { debounce } from 'lodash'
import { useSubmissionStore } from '@/stores/submission'

import ApiService from '@/common/services/ApiService.js'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'

export default {
  mixins: [inputBindingsMixin],
  props: {
    aquifer: null,
    aquiferVulnerabilityIndex: null,
    storativity: null,
    transmissivity: null,
    hydraulicConductivity: null,
    specificStorage: null,
    specificYield: null,
    testingMethod: null,
    testDuration: null,
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
    testDurationInput: 'testDuration',
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
    codes () {
      return this.submissionStore.codes
    }
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
