<template>
    <fieldset>
      <legend>Method of Drilling</legend>
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
              <b-form-radio value="VERTICAL">Vertical</b-form-radio>
              <b-form-radio value="HORIZONTAL">Horizontal</b-form-radio>
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
    wellOrientation: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
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
