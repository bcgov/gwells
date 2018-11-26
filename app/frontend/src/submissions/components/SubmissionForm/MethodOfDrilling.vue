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
          <legend :id="id">Method of Drilling</legend>
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
          <form-input
              id="groundElevation"
              label="Ground Elevation"
              hint="ft (asl)"
              v-model.number="groundElevationInput"
              :errors="errors['ground_elevation']"
              :loaded="fieldsLoaded['ground_elevation']"></form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input
              id="groundElevationMethod"
              label="Method for Determining Ground Elevation"
              select
              placeholder="Select method"
              :options="codes.ground_elevation_methods"
              value-field="ground_elevation_method_code"
              text-field="description"
              v-model="groundElevationMethodInput"
              :errors="errors['ground_elevation_method']"
              :loaded="fieldsLoaded['ground_elevation_method']"></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input
              id="drillingMethod"
              label="Drilling Method *"
              select
              :options="codes.drilling_methods"
              placeholder="Select method"
              value-field="drilling_method_code"
              text-field="description"
              v-model="drillingMethodInput"
              :errors="errors['drilling_method']"
              :loaded="fieldsLoaded['drilling_method']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input
              id="otherDrillingMethod"
              label="Specify Other Method of Drilling"
              type="text"
              v-model="otherDrillingMethodInput"
              :errors="errors['other_drilling_method']"
              :loaded="fieldsLoaded['other_drilling_method']"
          ></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group label="Orientation of Well">
            <b-form-radio-group v-model="wellOrientationInput"
                                stacked
                                name="wellOrientationRadio">
              <b-form-radio :value="true">Vertical</b-form-radio>
              <b-form-radio :value="false">Horizontal</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import { mapGetters } from 'vuex'
export default {
  name: 'MethodOfDrilling',
  mixins: [inputBindingsMixin],
  props: {
    groundElevation: null,
    groundElevationMethod: String,
    drillingMethod: String,
    otherDrillingMethod: String,
    wellOrientation: null,
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
    return {

    }
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
