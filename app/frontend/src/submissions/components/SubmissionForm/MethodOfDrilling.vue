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
  <form-subsection title="Method of Drilling" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
    <responsive-grid :cols="12" :md="6">
      <form-input
        id="groundElevation"
        label="Ground Elevation"
        hint="ft (asl)"
        v-model.number="groundElevationInput"
        type="number"
        :errors="errors['ground_elevation']"
        :loaded="fieldsLoaded['ground_elevation']"/>
      <form-input
        select
        id="groundElevationMethod"
        label="Method for Determining Ground Elevation"
        v-model="groundElevationMethodInput"
        value-field="ground_elevation_method_code"
        text-field="description"
        placeholder="Select Method"
        :options="method_codes()"
        :errors="errors['ground_elevation_method']"
        :loaded="fieldsLoaded['ground_elevation_method']"/>
      <form-input
        id="drillingMethod"
        :label="drillingMethodsLabel"
        select
        :options="codes?.drilling_methods"
        value-field="drilling_method_code"
        text-field="description"
        hint="Select one or more drilling methods. Hold the Ctrl (PC) or Command (Mac) key to select more than one option."
        v-model="drillingMethodInput"
        :errors="errors['drilling_methods']"
        :loaded="fieldsLoaded['drilling_methods']"/>
      <form-input
        select
        id="wellOrientationStatus"
        label="Orientation of Well"
        v-model="wellOrientationStatusInput"
        value-field="well_orientation_code"
        text-field="description"
        placeholder="Select Orientation"
        :options="codes?.well_orientation_codes"
        :errors="errors['well_orientation_status']"
        :loaded="fieldsLoaded['well_orientation_status']"/>
    </responsive-grid>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  name: 'MethodOfDrilling',
  mixins: [inputBindingsMixin],
  props: {
    groundElevation: null,
    groundElevationMethod: String,
    drillingMethod: Array,
    otherDrillingMethod: String,
    wellOrientationStatus: null,
    drillingMethodsLabel: String,
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
      options: [
      ]
    }
  },
  methods: {
    method_codes () { // make the unknown selection disabled for users
      if (this.codes != null && this.codes.ground_elevation_methods != null) {
        this.codes.ground_elevation_methods.forEach((code) => {
          if (code.ground_elevation_method_code === 'UNKNOWN') {
            code['disabled'] = true
          }
        })
        return this.codes.ground_elevation_methods
      }
    }
  },
  computed: {
    codes () {
      return this.submissionStore?.codes
    }
  }
}
</script>

<style>

</style>
