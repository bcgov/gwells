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
  <form-subsection title="Comments" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
    <responsive-grid :cols="12" :md="8">
      <b-form-group label="Comments" id="commentsGroup">
        <Textarea id="commentsEntry" :rows="3" autoResize v-model="commentsInput"/>
      </b-form-group>
    </responsive-grid>
    <responsive-grid class="mt-4 mb-4" :cols="12" :md="8">
      <b-form-group label="Internal Office Comments" id="commentsGroup">
        <Textarea id="internalCommentsEntry" :rows="3" autoResize v-model="internalCommentsInput"/>
      </b-form-group>
    </responsive-grid>
    <responsive-grid :cols="12" :sm="6" :gap="4">
      <b-form-group label="Alternative Specs Submitted">
        <RadioButtonGroup class="mt-1" v-model="alternativeSpecsSubmittedInput">
          <div>
            <RadioButton inputId="alternativeSpecsSubmittedInput.false" :value="false"/>
            <label for="alternativeSpecsSubmittedInput.false" class="ml-2">No</label>
          </div>
          <div>
            <RadioButton inputId="alternativeSpecsSubmittedInput.true" :value="true"/>
            <label for="alternativeSpecsSubmittedInput.true" class="ml-2">Yes</label>
          </div>
        </RadioButtonGroup>
      </b-form-group>
      <b-form-group label="Technical Report">
        <RadioButtonGroup class="mt-1" v-model="technicalReportInput">
          <div>
            <RadioButton inputId="technicalReportInput.false" :value="false"/>
            <label for="technicalReportInput.false" class="ml-2">No</label>
          </div>
          <div>
            <RadioButton inputId="technicalReportInput.true" :value="true"/>
            <label for="technicalReportInput.true" class="ml-2">Yes</label>
          </div>
        </RadioButtonGroup>
      </b-form-group>
      <b-form-group label="Drinking Water Area Indicator">
        <RadioButtonGroup class="mt-1" v-model="drinkingWaterProtectionAreaInput">
          <div>
            <RadioButton inputId="drinkingWaterProtectionAreaInput.false" :value="false"/>
            <label for="drinkingWaterProtectionAreaInput.false" class="ml-2">No</label>
          </div>
          <div>
            <RadioButton inputId="drinkingWaterProtectionAreaInput.true" :value="true"/>
            <label for="drinkingWaterProtectionAreaInput.true" class="ml-2">Yes</label>
          </div>
        </RadioButtonGroup>
      </b-form-group>
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
    comments: String,
    internalComments: String,
    alternativeSpecsSubmitted: null,
    technicalReport: null,
    drinkingWaterProtectionArea: null,
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
    commentsInput: 'comments',
    internalCommentsInput: 'internalComments',
    alternativeSpecsSubmittedInput: 'alternativeSpecsSubmitted',
    technicalReportInput: 'technicalReport',
    drinkingWaterProtectionAreaInput: 'drinkingWaterProtectionArea'
  },
  data () {
    return {
      submissionStore: null,
      status: 'False'
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
