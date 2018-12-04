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
        <legend :id="id">Water Quality</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <a href="#top" v-if="isStaffEdit">Back to top</a>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6">
        <b-form-group label="Characteristics" id="waterCharacteristicsGroup">
          <v-select
              :options="codes.water_quality_characteristics"
              label="description"
              index="code"
              id="waterCharacteristicsInput"
              placeholder="Select characteristics"
              v-model="waterQualityCharacteristicsInput"
              multiple
          ></v-select>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="5" lg="4">
        <form-input
            id="waterQualityColour"
            label="Water Quality Colour"
            select
            :options="codes.water_quality_colours"
            text-field="description"
            value-field="code"
            placeholder="Select colour"
            v-model="waterQualityColourInput"
            :errors="errors['water_quality_colour']"
            :loaded="fieldsLoaded['water_quality_colour']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="5" lg="4">
        <form-input
            id="waterQualityOdour"
            label="Water Quality Odour"
            v-model="waterQualityOdourInput"
            :errors="errors['water_quality_odour']"
            :loaded="fieldsLoaded['water_quality_odour']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="5" lg="4">
        <form-input
            id="emsID"
            label="Environmental Monitoring System (EMS) ID"
            v-model="emsIDInput"
            :errors="errors['ems_id']"
            :loaded="fieldsLoaded['ems_id']"></form-input>
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
    waterQualityCharacteristics: {
      type: Array,
      default: () => ([])
    },
    waterQualityColour: String,
    waterQualityOdour: String,
    emsID: String,
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
    waterQualityColourInput: 'waterQualityColour',
    waterQualityCharacteristicsInput: 'waterQualityCharacteristics',
    waterQualityOdourInput: 'waterQualityOdour',
    emsIDInput: 'emsID'
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
