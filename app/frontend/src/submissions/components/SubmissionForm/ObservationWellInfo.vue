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
        <legend :id="id">Observation Well Information</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <a href="#top" v-if="isStaffEdit">Back to top</a>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="3" xl="2">
        <form-input
          id="obsWellNumber"
          label="Observation Well Number"
          v-model="obsWellNumberInput"
          :errors="errors['observation_well_number']"
          :loaded="fieldsLoaded['observation_well_number']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="3" xl="2">
        <form-input
          id="obsWellStatus"
          label="Observation Well Status"
          select
          :options="codes.observation_well_status"
          :errors="errors['observation_well_status']"
          :loaded="fieldsLoaded['observation_well_status']"
          text-field="obs_well_status_code"
          value-field="obs_well_status_code"
          placeholder="Select status"
          v-model="obsWellStatusInput"
        ></form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    comments: String,
    alternativeSpecsSubmitted: null,
    obsWellStatus: null,
    obsWellNumber: null,
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
    alternativeSpecsSubmittedInput: 'alternativeSpecsSubmitted',
    obsWellStatusInput: 'obsWellStatus',
    obsWellNumberInput: 'obsWellNumber'
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
