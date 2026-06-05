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
  <form-subsection title="Well Completion Data" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
    <responsive-grid :cols="12" :md="6" :lg="4">
      <form-input
        id="totalDepthDrilled"
        :label="totalDepthDrilledLabel"
        v-model="totalDepthDrilledInput"
        type="number"
        hint="ft (bgl)"
        :errors="errors['total_depth_drilled']"
        :loaded="fieldsLoaded['total_depth_drilled']"/>
      <form-input
        id="finishedWellDepth"
        :label="finishedWellDepthLabel"
        v-model="finishedWellDepthInput"
        type="number"
        hint="ft (bgl)"
        :errors="errors['finished_well_depth']"
        :loaded="fieldsLoaded['finished_well_depth']"/>
    </responsive-grid>
    <responsive-grid :cols="12" :md="6" :lg="4">
      <form-input
        id="finalCasingStickUp"
        label="Final Casing Stick Up"
        type="number"
        v-model="finalCasingStickUpInput"
        hint="in"
        :errors="errors['final_casing_stick_up']"
        :loaded="fieldsLoaded['final_casing_stick_up']"/>
      <form-input
        id="bedrockDepth"
        label="Depth to Bedrock"
        type="number"
        v-model="bedrockDepthInput"
        hint="ft (bgl)"
        :errors="errors['depth_to_bedrock']"
        :loaded="fieldsLoaded['depth_to_bedrock']"/>
    </responsive-grid>
    <responsive-grid :cols="12" :md="6" :lg="4">
      <form-input
        id="staticWaterLevel"
        label="Static Water Level"
        v-model="staticWaterLevelInput"
        type="number"
        hint="ft (btoc)"
        :errors="errors['static_water_level']"
        :loaded="fieldsLoaded['static_water_level']"/>
      <form-input
        id="wellYield"
        label="Estimated Well Yield"
        type="number"
        v-model="wellYieldInput"
        hint="USgpm"
        :errors="errors['well_yield']"
        :loaded="fieldsLoaded['well_yield']"/>
    </responsive-grid>
    <responsive-grid :cols="12" :md="6" :lg="4">
      <div class="flex flex-col form-group">
        <label for="artesianConditionsInput">Artesian Well</label>
        <RadioButtonGroup class="mt-1" v-model="artesianConditionsInput" id="artesianConditionsInput">
          <div>
            <RadioButton inputId="artesianConditionsInput.false" :value="false"/>
            <label for="artesianConditionsInput.false" class="ml-2">No</label>
          </div>
          <div>
            <RadioButton inputId="artesianConditionsInput.true" :value="true"/>
            <label for="artesianConditionsInput.true" class="ml-2">Yes</label>
          </div>
        </RadioButtonGroup>
      </div>
      <form-input
        id="artesianFlow"
        label="Artesian Flow"
        v-model="artesianFlowInput"
        hint="USgpm"
        type="number"
        :errors="errors['artesian_flow']"
        :loaded="fieldsLoaded['artesian_flow']"/>
    </responsive-grid>
    <responsive-grid :cols="12" :md="6" :lg="4">
      <form-input
        id="artesianPressureHead"
        label="Artesian Pressure (head)"
        @input="handleArtesianPressureHeadChange"
        v-model="artesianPressure.head"
        hint="ft (agl)"
        type="number"
        :errors="errors['artesian_pressure_head']"
        :loaded="fieldsLoaded['artesian_pressure_head']"/>
      <form-input
        id="artesianPressurePSI"
        label="Artesian Pressure (PSI)"
        @input="handleArtesianPressurePSIChange"
        v-model="artesianPressure.psi"
        hint="PSI"
        type="number"
        :errors="errors['artesian_pressure']"
        :loaded="fieldsLoaded['artesian_pressure']"/>
    </responsive-grid>
    <responsive-grid :cols="12" :md="6" :lg="4">
      <form-input
        id="wellCapType"
        label="Well Cap Type"
        v-model="wellCapTypeInput"
        :errors="errors['well_cap_type']"
        :loaded="fieldsLoaded['well_cap_type']"/>
      <div class="flex flex-col form-group">
        <label for="wellDisinfectedStatusInput">Well Disinfected Status</label>
        <Select
          id="wellDisinfectedStatusInput"
          v-model="wellDisinfectedInput"
          optionValue="well_disinfected_code"
          optionLabel="well_disinfected_code"
          :options="disinfected_codes()"
          :loading="!fieldsLoaded['well_disinfected_status']"/>
      </div>
    </responsive-grid>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

export default {
  mixins: [inputBindingsMixin],
  props: {
    totalDepthDrilled: String,
    finishedWellDepth: String,
    finalCasingStickUp: String,
    bedrockDepth: String,
    staticWaterLevel: String,
    wellYield: String,
    artesianFlow: String,
    artesianPressurePSI: String,
    artesianPressureHead: String,
    artesianConditions: Boolean,
    wellCapType: String,
    totalDepthDrilledLabel: String,
    finishedWellDepthLabel: String,
    wellDisinfected: null,
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
  components: {
    FormSubsection,
    ResponsiveGrid
  },
  fields: {
    totalDepthDrilledInput: 'totalDepthDrilled',
    finishedWellDepthInput: 'finishedWellDepth',
    finalCasingStickUpInput: 'finalCasingStickUp',
    bedrockDepthInput: 'bedrockDepth',
    staticWaterLevelInput: 'staticWaterLevel',
    wellYieldInput: 'wellYield',
    artesianFlowInput: 'artesianFlow',
    artesianPressurePSIInput: 'artesianPressurePSI',
    artesianPressureHeadInput: 'artesianPressureHead',
    artesianConditionsInput: 'artesianConditions',
    wellCapTypeInput: 'wellCapType',
    wellDisinfectedInput: 'wellDisinfected'
  },
  data () {
    return {
      submissionStore: null,
      artesianPressure: {
        head: null,
        psi: null
      }
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
    this.artesianPressure.psi = this.artesianPressurePSI
    this.artesianPressure.head = this.artesianPressureHead
    if (this.artesianPressurePSI || this.artesianPressureHead) {
      this.updateArtesianPressure(null, this.artesianPressurePSI)
    }
  },
  methods: {
    disinfected_codes () { // make the unknown selection disabled for users
      if (this.codes != null && this.codes.well_disinfected_codes != null) {
        this.codes.well_disinfected_codes.forEach((code, index, object) => {
          if (code.well_disinfected_code === 'Unknown') {
            if (!this.isStaffEdit) {
              object.splice(index, 1)
            }
          }
        })
        return this.codes.well_disinfected_codes
      }
    },
    handleArtesianPressureHeadChange () {
      this.updateArtesianPressure(this.artesianPressure.head, null)
    },
    handleArtesianPressurePSIChange () {
      this.updateArtesianPressure(null, this.artesianPressure.psi)
    },
    updateArtesianPressure (head, psi) {
      if (head != null) {
        const newPsi = this.calculateArtesianPressurePSI(head)
        this.artesianPressurePSIInput = newPsi
        this.artesianPressure.psi = newPsi
        this.artesianPressureHeadInput = head
        this.artesianPressure.head = head
      }
      if (psi != null) {
        const newHead = this.calculateArtesianPressureHead(psi)
        this.artesianPressureHeadInput = newHead
        this.artesianPressure.head = newHead
        this.artesianPressurePSIInput = psi
        this.artesianPressure.psi = psi
      }
      this.resetArtesianPressure()
    },
    calculateArtesianPressureHead (psi) {
      return String(Math.round((psi == null || psi === 0 ? 0 : psi * 2.31) * 100) / 100)
    },
    calculateArtesianPressurePSI (head) {
      return String(Math.round((head == null || head === 0 ? 0 : head / 2.31) * 100) / 100)
    },
    resetArtesianPressure () {
      if (this.artesianPressure.psi == null || this.artesianPressure.head == null) {
        this.artesianPressureHeadInput = null
        this.artesianPressure.head = null
        this.artesianPressurePSIInput = null
        this.artesianPressure.psi = null
      }
    }
  },
  computed: {
    codes () {
      return this.submissionStore.codes
    }
  }
}
</script>

<style>

</style>
