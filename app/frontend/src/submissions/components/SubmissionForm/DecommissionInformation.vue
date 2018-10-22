<template>
  <fieldset>
    <legend>Well Decommission Information</legend>
    <b-row>
      <b-col cols="12" md="3" lg="2">
        <form-input
            id="finishedWellDepth"
            label="Finished Well Depth"
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
            :errors="errors['sealant_material']"
            :loaded="fieldsLoaded['sealant_material']"></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="backfillMaterial"
            label="Backfill Material"
            v-model="backfillMaterialInput"
            :errors="errors['backfill_material']"
            :loaded="fieldsLoaded['backfill_material']"></form-input>
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
export default {
  mixins: [inputBindingsMixin],
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
