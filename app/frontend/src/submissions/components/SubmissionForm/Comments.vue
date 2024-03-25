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
        <legend :id="id">Comments</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="8">
        <b-form-group label="Comments" id="commentsGroup">
          <b-form-textarea
              id="commentsEntry"
              :rows="3"
              :max-rows="12"
              v-model="commentsInput"></b-form-textarea>
        </b-form-group>
      </b-col>
    </b-row>

    <b-row class="mt-3">
      <b-col cols="12" md="8">
        <b-form-group label="Internal Office Comments" id="commentsGroup">
          <b-form-textarea
              id="internalCommentsEntry"
              :rows="3"
              :max-rows="12"
              v-model="internalCommentsInput"></b-form-textarea>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col cols="12" sm="6">
        <b-form-group label="Alternative Specs Submitted">
        <b-form-radio-group
          id="alternativeSpecsCheckbox"
          class="mt-1"
          v-model="alternativeSpecsSubmittedInput"
        >
          <b-form-radio :value="false">No</b-form-radio>
          <b-form-radio :value="true">Yes</b-form-radio>
        </b-form-radio-group>
      </b-form-group>
    </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col cols="12" sm="6">
        <b-form-group label="Technical Report">
        <b-form-radio-group
          id="technicalReportCheckbox"
          class="mt-1"
          v-model="technicalReportInput"
        >
          <b-form-radio :value="false">No</b-form-radio>
          <b-form-radio :value="true">Yes</b-form-radio>
        </b-form-radio-group>
      </b-form-group>
    </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col cols="12" sm="6">
        <b-form-group label="Drinking Water Area Indicator">
        <b-form-radio-group
          id="drinkingWaterProtectionAreaCheckbox"
          class="mt-1"
          v-model="drinkingWaterProtectionAreaInput"
        >
          <b-form-radio :value="false">No</b-form-radio>
          <b-form-radio :value="true">Yes</b-form-radio>
        </b-form-radio-group>
      </b-form-group>
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
  fields: {
    commentsInput: 'comments',
    internalCommentsInput: 'internalComments',
    alternativeSpecsSubmittedInput: 'alternativeSpecsSubmitted',
    technicalReportInput: 'technicalReport',
    drinkingWaterProtectionAreaInput: 'drinkingWaterProtectionArea'
  },
  data () {
    return {
      status: 'False'
    }
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
