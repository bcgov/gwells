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
  <fieldset :id="id">
    <b-row>
      <b-col cols="12" lg="6">
        <legend :id="id">Yield</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col cols="12" md="4" lg="3">
        <form-input
            id="yieldEstimationMethod"
            label="Yield Estimation Method"
            select
            :options="codes.yield_estimation_methods"
            text-field="description"
            value-field="yield_estimation_method_code"
            v-model="yieldEstimationMethodInput"
            placeholder="Select method"></form-input>
      </b-col>
      <b-col cols="12" md="4" lg="3">
        <form-input
            id="yieldEstimationRate"
            label="Yield Estimation Rate"
            type="number"
            hint="USgpm"
            v-model="yieldEstimationRateInput"></form-input>
      </b-col>
      <b-col cols="12" md="4" lg="3">
        <form-input
            id="yieldEstimationDuration"
            label="Yield Estimation Duration"
            type="number"
            hint="Hours"
            v-model="yieldEstimationDurationInput"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4" lg="3">
        <form-input
            id="staticWaterLevelTest"
            label="SWL Before Test"
            type="number"
            v-model="staticLevelInput"
            hint="ft (btoc)"></form-input>
      </b-col>
      <b-col cols="12" md="4" lg="3">
        <b-form-group label="Hydro-fracturing Performed">
          <b-form-radio-group v-model="hydroFracturingPerformedInput"
            id="hydroFracPerformedOptions"
            name="hydroFracturingPerformed"
          >
            <b-form-radio :value="false">No</b-form-radio>
            <b-form-radio :value="true">Yes</b-form-radio>
          </b-form-radio-group>
        </b-form-group>
      </b-col>
      <b-col cols="12" md="4" lg="4">
        <form-input
          id="hydroFracturingYieldIncrease"
          label="Increase in Well Yield Due to Hydro-fracturing"
          type="number"
          v-model="hydroFracturingYieldIncreaseInput"
          hint="USgpm"
        ></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4" lg="3">
        <form-input
            id="drawdown"
            label="Drawdown"
            type="number"
            v-model="drawdownInput"
            hint="ft (btoc)"
            ></form-input>
      </b-col>
      <b-col v-if="isStaffEdit" cols="12" md="4" lg="3">
        <form-input
          id="recommendedPumpDepth"
          label="Recommended Pump Depth"
          type="number"
          v-model="recommendedPumpDepthInput"
          hint="ft (btoc)"
        />
      </b-col>
      <b-col v-if="isStaffEdit" cols="12" md="4" lg="3">
        <form-input
          id="recommendedPumpRate"
          label="Recommended Pump Rate"
          type="number"
          v-model="recommendedPumpRateInput"
          hint="USgpm"
        />
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'

import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    yieldEstimationMethod: String,
    yieldEstimationRate: String,
    yieldEstimationDuration: String,
    staticLevel: String,
    drawdown: String,
    hydroFracturingPerformed: Boolean,
    hydroFracturingYieldIncrease: String,
    recommendedPumpDepth: String,
    recommendedPumpRate: String,
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
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
