<template>
  <div>
    <fieldset>
      <legend>Step 7: Backfill</legend>
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
