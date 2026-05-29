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
  <form-subsection title="Well Decommission Information" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
    <responsive-grid :cols="12" :md="3" :lg="2">
      <form-input
        id="finishedWellDepth"
        label="Finished Well Depth"
        type="number"
        v-model="finishedWellDepthInput"
        hint="feet (below ground level)"
        :errors="errors['finished_well_depth']"
        :loaded="fieldsLoaded['finished_well_depth']"/>
    </responsive-grid>
    <responsive-grid :cols="12" :md="6" :lg="4">
      <form-input
        id="decommissionReason"
        label="Reason for Well Decommission"
        v-model="decommissionReasonInput"
        :errors="errors['decommission_reason']"
        :loaded="fieldsLoaded['decommission_reason']"/>
      <div class="flex flex-col gap-2">
        <label>Decommission Method</label>
        <RadioButtonGroup id="decommissionMethodRadio" class="mt-1" v-model="decommissionMethodInput">
          <div v-for="(method, index) in codes.decommission_methods" class="flex align-items-center" :key="`decommissionMethodOption${index}`">
            <RadioButton :inputId="`decommissionMethodInput.${method.decommission_method_code}`" :value="method.decommission_method_code"/>
            <label :for="`decommissionMethodInput.${method.decommission_method_code}`" class="ml-2">{{method.description}}</label>
          </div>
        </RadioButtonGroup>
      </div>
    </responsive-grid>
    <responsive-grid :cols="12" :md="6" :lg="4">
      <form-input
        id="sealantMaterial"
        label="Sealant Material"
        v-model="sealantMaterialInput"
        :errors="errors['decommission_sealant_material']"
        :loaded="fieldsLoaded['decommission_sealant_material']"/>
      <form-input
        id="backfillMaterial"
        label="Backfill Material"
        v-model="backfillMaterialInput"
        :errors="errors['decommission_backfill_material']"
        :loaded="fieldsLoaded['decommission_backfill_material']"/>
    </responsive-grid>
    <responsive-grid :cols="12" :lg="8">
      <form-input
        id="decommissionDetails"
        label="Decommission Details"
        v-model="decommissionDetailsInput"
        :errors="errors['decommission_details']"
        :loaded="fieldsLoaded['decommission_details']"/>
    </responsive-grid>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  mixins: [inputBindingsMixin],
  props: {
    finishedWellDepth: String,
    decommissionReason: String,
    decommissionMethod: String,
    sealantMaterial: String,
    backfillMaterial: String,
    decommissionDetails: String,
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
  data () {
    return {
      submissionStore: null
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
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
