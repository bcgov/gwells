<template>
  <fieldset>
    <legend :id="id">Well Completion Data</legend>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="totalDepthDrilled"
            label="Total Depth Drilled *"
            v-model="totalDepthDrilledInput"
            hint="ft"
            :errors="errors['total_depth_drilled']"
            :loaded="fieldsLoaded['total_depth_drilled']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="finishedWellDepth"
            label="Finished Well Depth *"
            v-model="finishedWellDepthInput"
            hint="ft (bgl)"
            :errors="errors['finished_well_depth']"
            :loaded="fieldsLoaded['finished_well_depth']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="finalCasingStickUp"
            label="Final Casing Stick Up *"
            v-model="finalCasingStickUpInput"
            hint="in"
            :errors="errors['final_casing_stick_up']"
            :loaded="fieldsLoaded['final_casing_stick_up']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="bedrockDepth"
            label="Depth to Bedrock *"
            v-model="bedrockDepthInput"
            hint="ft (bgl)"
            :errors="errors['depth_to_bedrock']"
            :loaded="fieldsLoaded['depth_to_bedrock']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="staticWaterLevel"
            label="Static Water Level"
            v-model="staticWaterLevelInput"
            hint="ft (btoc)"
            :errors="errors['static_water_level']"
            :loaded="fieldsLoaded['static_water_level']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="wellYield"
            label="Estimated Well Yield"
            v-model="wellYieldInput"
            hint="USgpm"
            :errors="errors['well_yield']"
            :loaded="fieldsLoaded['well_yield']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="artesianFlow"
            label="Artesian Flow"
            v-model="artesianFlowInput"
            hint="USgpm"
            :errors="errors['artesian_flow']"
            :loaded="fieldsLoaded['artesian_flow']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="artesianPressure"
            label="Artesian Pressure"
            v-model="artesianPressureInput"
            hint="ft"
            :errors="errors['artesian_pressure']"
            :loaded="fieldsLoaded['artesian_pressure']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="wellCapType"
            label="Well Cap Type"
            v-model="wellCapTypeInput"
            :errors="errors['well_cap_type']"
            :loaded="fieldsLoaded['well_cap_type']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <b-form-group label="Well Disinfected?">
          <b-form-radio-group id="wellDisinfectedRadio" class="mt-1" v-model="wellDisinfectedInput">
            <b-form-radio value="False">No</b-form-radio>
            <b-form-radio value="True">Yes</b-form-radio>
          </b-form-radio-group>
        </b-form-group>
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
    totalDepthDrilled: String,
    finishedWellDepth: String,
    finalCasingStickUp: String,
    bedrockDepth: String,
    staticWaterLevel: String,
    wellYield: String,
    artesianFlow: String,
    artesianPressure: String,
    wellCapType: String,
    wellDisinfected: String,
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
    }
  },
  fields: {
    totalDepthDrilledInput: 'totalDepthDrilled',
    finishedWellDepthInput: 'finishedWellDepth',
    finalCasingStickUpInput: 'finalCasingStickUp',
    bedrockDepthInput: 'bedrockDepth',
    staticWaterLevelInput: 'staticWaterLevel',
    wellYieldInput: 'wellYield',
    artesianFlowInput: 'artesianFlow',
    artesianPressureInput: 'artesianPressure',
    wellCapTypeInput: 'wellCapType',
    wellDisinfectedInput: 'wellDisinfected'
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
