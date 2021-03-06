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
        <legend :id="id">Well Decommission Information</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="3" lg="2">
        <form-input
            id="finishedWellDepth"
            label="Finished Well Depth"
            type="number"
            v-model="finishedWellDepthInput"
            hint="feet (below ground level)"
            :errors="errors['finished_well_depth']"
            :loaded="fieldsLoaded['finished_well_depth']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="decommissionReason"
            label="Reason for Well Decommission"
            v-model="decommissionReasonInput"
            :errors="errors['decommission_reason']"
            :loaded="fieldsLoaded['decommission_reason']"></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <b-form-group label="Decommission Method">
          <b-form-radio-group id="decommissionMethodRadio" class="mt-1" v-model="decommissionMethodInput">
            <b-form-radio
                v-for="(method, index) in codes.decommission_methods"
                :key="`decommissionMethodOption${index}`"
                :value="method.decommission_method_code">{{method.description}}</b-form-radio>
          </b-form-radio-group>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="sealantMaterial"
            label="Sealant Material"
            v-model="sealantMaterialInput"
            :errors="errors['decommission_sealant_material']"
            :loaded="fieldsLoaded['decommission_sealant_material']"></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="backfillMaterial"
            label="Backfill Material"
            v-model="backfillMaterialInput"
            :errors="errors['decommission_backfill_material']"
            :loaded="fieldsLoaded['decommission_backfill_material']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" lg="8">
        <form-input
            id="decommissionDetails"
            label="Decommission Details"
            v-model="decommissionDetailsInput"
            :errors="errors['decommission_details']"
            :loaded="fieldsLoaded['decommission_details']"></form-input>
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
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
