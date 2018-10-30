<template>
  <fieldset>
    <legend :id="id">Water Quality</legend>
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
