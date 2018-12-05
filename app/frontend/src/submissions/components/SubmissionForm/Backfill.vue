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
  <div>
    <fieldset>
      <b-row>
        <b-col cols="12" lg="6">
          <legend :id="id">Surface Seal and Backfill Information</legend>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" sm="4" md="3">
          <form-input
              label="Surface Seal Material"
              id="surfaceSealMaterial"
              select
              v-model="surfaceSealMaterialInput"
              :options="codes.surface_seal_materials"
              placeholder="Select material"
              text-field="description"
              value-field="surface_seal_material_code"
              :errors="errors['surface_seal_material']"
              :loaded="fieldsLoaded['surface_seal_material']"></form-input>
        </b-col>
        <b-col cols="12" sm="4" md="3">
          <form-input
              label="Surface Seal Depth (ft)"
              id="surfaceSealDepth"
              v-model="surfaceSealDepthInput"
              :errors="errors['surface_seal_depth']"
              :loaded="fieldsLoaded['surface_seal_depth']"></form-input>
        </b-col>
        <b-col cols="12" sm="4" md="3">
          <form-input
              label="Surface Seal Thickness (in)"
              id="surfaceSealThickness"
              v-model="surfaceSealThicknessInput"
              :errors="errors['surface_seal_thickness']"
              :loaded="fieldsLoaded['surface_seal_thickness']"></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" sm="6" md="4">
          <form-input
              label="Surface Seal Method of Installation"
              id="surfaceSealMethod"
              select
              :options="codes.surface_seal_methods"
              placeholder="Select method"
              text-field="description"
              value-field="surface_seal_method_code"
              v-model="surfaceSealMethodInput"
              :errors="errors['surface_seal_method']"
              :loaded="fieldsLoaded['surface_seal_method']"></form-input>
        </b-col>
      </b-row>
    </fieldset>
    <fieldset>
      <legend>Backfill Information</legend>
      <b-row>
        <b-col cols="12" sm="4" md="3">
          <form-input
              label="Backfill Material Above Surface Seal"
              id="backfillAboveSurfaceSeal"
              select
              v-model="backfillAboveSurfaceSealInput"
              :options="codes.surficial_material_codes"
              text-field="description"
              value-field="surficial_material_code"
              placeholder="Select material"
              :errors="errors['backfill_above_surface_seal']"
              :loaded="fieldsLoaded['backfill_above_surface_seal']"></form-input>
        </b-col>
        <b-col cols="12" sm="4" md="3">
          <form-input
              label="Backfill Depth (ft)"
              id="backfillDepth"
              v-model="backfillDepthInput"
              :errors="errors['backfill_above_surface_seal_depth']"
              :loaded="fieldsLoaded['backfill_above_surface_seal_depth']"></form-input>
        </b-col>
      </b-row>
    </fieldset>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    surfaceSealMaterial: String,
    surfaceSealDepth: String,
    surfaceSealThickness: String,
    surfaceSealMethod: String,
    backfillAboveSurfaceSeal: String,
    backfillDepth: String,
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
    surfaceSealMaterialInput: 'surfaceSealMaterial',
    surfaceSealDepthInput: 'surfaceSealDepth',
    surfaceSealThicknessInput: 'surfaceSealThickness',
    surfaceSealMethodInput: 'surfaceSealMethod',
    backfillAboveSurfaceSealInput: 'backfillAboveSurfaceSeal',
    backfillDepthInput: 'backfillDepth'
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
